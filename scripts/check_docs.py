#!/usr/bin/env python3
"""Consistency checks for the Throne docs. CI runs this before every deploy.

    python3 scripts/check_docs.py

Needs Python 3.11+ and PyYAML. Exits non-zero when any check fails.
"""
import re
import sys
import tomllib
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# Pages rendered by their own template: no sidebar entry, no description needed.
SPECIAL_TEMPLATES = {"landing", "downloads", "download"}
# The download redirect helper exists in the default language only.
SINGLE_LANGUAGE = {"download"}
STATIC_PREFIXES = ("/images/", "/logos/", "/css/", "/js/", "/fonts/", "/assets/")
HTML_TAGS = {"a", "abbr", "b", "br", "code", "details", "div", "em", "i", "img", "kbd", "li", "ol", "p", "pre",
             "s", "small", "span", "strong", "sub", "summary", "sup", "table", "tbody", "td", "th", "thead", "tr",
             "u", "ul"}

errors = []


def error(path, message):
    rel = path.relative_to(ROOT).as_posix() if isinstance(path, Path) else path
    errors.append(f"{rel}: {message}")


config = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))
DEFAULT_LANG = config.get("default_language", "en")
LANGS = sorted(config.get("languages", {}), key=lambda c: config["languages"][c].get("weight", 0))


class Page:
    def __init__(self, path):
        self.path = path
        rel = path.relative_to(CONTENT).as_posix()
        parts = rel[:-3].rsplit(".", 1)
        if len(parts) == 2 and parts[1] in LANGS:
            self.key, self.lang = parts
        else:
            self.key, self.lang = rel[:-3], DEFAULT_LANG
        self.front, self.body = {}, ""
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\+\+\+\r?\n(.*?)\r?\n\+\+\+\r?\n?(.*)", text, re.S)
        if not match:
            error(path, "missing +++ TOML front matter")
            return
        try:
            self.front = tomllib.loads(match.group(1))
        except tomllib.TOMLDecodeError as exc:
            error(path, f"front matter is not valid TOML: {exc}")
        self.body = match.group(2)

    @property
    def special(self):
        return self.front.get("template") in SPECIAL_TEMPLATES

    @property
    def url(self):
        """URL of a page without a custom path, e.g. guides/routing -> /guides/routing/."""
        key = self.key[: -len("_index")] if self.key.endswith("_index") else self.key + "/"
        prefix = "" if self.lang == DEFAULT_LANG else f"/{self.lang}"
        return f"{prefix}/{key}".replace("//", "/")

    def headings(self):
        """(level, text, explicit id or None) for every heading outside code fences."""
        result, fence = [], None
        for line in self.body.splitlines():
            stripped = line.lstrip()
            marker = re.match(r"(`{3,}|~{3,})", stripped)
            if marker:
                if fence is None:
                    fence = marker.group(1)[0] * len(marker.group(1))
                elif stripped.startswith(fence):
                    fence = None
                continue
            if fence is not None:
                continue
            heading = re.match(r"(#{1,6})\s+(.*?)\s*$", line)
            if heading:
                ident = re.search(r"\{#([A-Za-z0-9_-]+)\}$", heading.group(2))
                result.append((len(heading.group(1)), heading.group(2), ident.group(1) if ident else None))
        return result

    def ids(self):
        return [ident for _, _, ident in self.headings() if ident]


pages = {}
for path in sorted(CONTENT.rglob("*.md")):
    page = Page(path)
    pages[(page.key, page.lang)] = page

# 1. Every page exists in every language, and translations agree on structure.
for key in sorted({key for key, _ in pages}):
    base = pages.get((key, DEFAULT_LANG))
    if base is None:
        error(CONTENT / f"{key}.md", "translation without a default-language page")
        continue
    if key in SINGLE_LANGUAGE:
        continue
    for lang in LANGS:
        page = pages.get((key, lang))
        if page is None:
            error(base.path, f"missing {lang} translation ({key}.{lang}.md)")
            continue
        if page.front.get("weight") != base.front.get("weight"):
            error(page.path, f"weight {page.front.get('weight')} differs from {DEFAULT_LANG} ({base.front.get('weight')})")
        if page.front.get("template") != base.front.get("template"):
            error(page.path, "template differs from the default-language page")
        if page.ids() != base.ids():
            missing = [i for i in base.ids() if i not in page.ids()]
            extra = [i for i in page.ids() if i not in base.ids()]
            detail = []
            if missing:
                detail.append(f"missing {missing}")
            if extra:
                detail.append(f"extra {extra}")
            error(page.path, "heading ids differ from the default-language page: " + ("; ".join(detail) or "different order"))
        base_aliases = base.front.get("aliases", [])
        prefix = "" if lang == DEFAULT_LANG else f"/{lang}"
        if page.front.get("aliases", []) != [prefix + alias for alias in base_aliases]:
            error(page.path, f"aliases must be {[prefix + a for a in base_aliases]}")

# 2. Front matter and headings of documentation pages.
for page in pages.values():
    if page.special or page.key in SINGLE_LANGUAGE or not page.front:
        continue
    for field in ("title", "description"):
        if not str(page.front.get(field, "")).strip():
            error(page.path, f"front matter needs a non-empty '{field}'")
    if not isinstance(page.front.get("weight"), int):
        error(page.path, "front matter needs an integer 'weight'")
    for field in ("path", "slug"):
        if field in page.front:
            error(page.path, f"'{field}' breaks the sidebar and edit links; rename the file instead")
    seen = set()
    for level, text, ident in page.headings():
        if level == 1:
            error(page.path, f"H1 in the body ('{text}'); the title comes from front matter")
        if level == 2 and ident is None:
            error(page.path, f"H2 without an explicit id: '{text}'")
        if ident is not None:
            if ident in seen:
                error(page.path, f"duplicate heading id '{ident}'")
            seen.add(ident)

# 3. Links: `@/` targets must exist in the same language, anchors must be explicit ids.
for page in pages.values():
    for target, anchor in re.findall(r"\]\(@/([^)#\s]+)(?:#([^)\s]+))?\)", page.body):
        target_page = None
        if target.endswith(".md"):
            stem = target[:-3]
            parts = stem.rsplit(".", 1)
            key, lang = (parts[0], parts[1]) if len(parts) == 2 and parts[1] in LANGS else (stem, DEFAULT_LANG)
            target_page = pages.get((key, lang))
            if target_page is not None and lang != page.lang and key not in SINGLE_LANGUAGE:
                error(page.path, f"@/{target} points at the {lang} page; use the {page.lang} one")
        if target_page is None:
            error(page.path, f"broken link @/{target}")
        elif anchor and anchor not in target_page.ids():
            error(page.path, f"@/{target}#{anchor}: no heading with that id")
    for url in re.findall(r"\]\((/[^)\s]*)\)", page.body):
        if not url.startswith(STATIC_PREFIXES):
            error(page.path, f"absolute link {url}; use an @/ link so translations stay in their language")
    # Markdown passes raw HTML through, so a bare <name> placeholder in prose vanishes from the page.
    if not page.special:
        fence = False
        for line in page.body.splitlines():
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
                continue
            if fence:
                continue
            for tag in re.findall(r"<(?!!--)/?([A-Za-z][\w-]*)", re.sub(r"`[^`]*`", "", line)):
                if tag.lower() not in HTML_TAGS:
                    error(page.path, f"<{tag}> outside code would be read as HTML; put it in backticks")

# 4. Sidebars list every page once, in weight order, with the same shape in every language.
def flatten(items):
    for item in items:
        if "items" in item:
            yield from flatten(item["items"])
        else:
            yield item


docs_pages = {(p.key, p.lang) for p in pages.values() if not p.special and p.key not in SINGLE_LANGUAGE}
by_url = {p.url: p for p in pages.values()}
shapes = {}
for lang in LANGS:
    sidebar_path = ROOT / "data" / f"sidebar_{lang}.yml"
    if not sidebar_path.exists():
        error(sidebar_path, "missing sidebar")
        continue
    try:
        groups = yaml.safe_load(sidebar_path.read_text(encoding="utf-8")) or []
    except yaml.YAMLError as exc:
        error(sidebar_path, f"invalid YAML: {exc}")
        continue
    prefix = "" if lang == DEFAULT_LANG else f"/{lang}"
    listed, shape = set(), []
    for group in groups:
        urls = []
        for item in flatten(group.get("items", [])):
            if not item.get("title"):
                error(sidebar_path, f"item without a title: {item}")
            url = item.get("url", "")
            page = by_url.get(prefix + url)
            if page is None or page.lang != lang:
                error(sidebar_path, f"{url} does not match a {lang} page")
                continue
            if (page.key, lang) in listed:
                error(sidebar_path, f"{url} is listed twice")
            listed.add((page.key, lang))
            urls.append(url)
            if not page.key.startswith(group.get("section", "") + "/") and page.key != group.get("section"):
                error(sidebar_path, f"{url} is in the '{group.get('section')}' group but lives elsewhere")
        weights = [by_url[prefix + u].front.get("weight", 0) for u in urls if not by_url[prefix + u].key.endswith("_index")]
        if weights != sorted(weights):
            error(sidebar_path, f"group '{group.get('section')}' is not in page-weight order")
        shape.append((group.get("section"), urls))
    shapes[lang] = shape
    for key, page_lang in sorted(docs_pages):
        if page_lang == lang and (key, lang) not in listed:
            error(sidebar_path, f"{pages[(key, lang)].url} is not in the sidebar")
for lang, shape in shapes.items():
    if lang != DEFAULT_LANG and DEFAULT_LANG in shapes and shape != shapes[DEFAULT_LANG]:
        error(ROOT / "data" / f"sidebar_{lang}.yml", f"groups or URLs differ from sidebar_{DEFAULT_LANG}.yml")

# 5. UI strings and release versions.
i18n = {}
for lang in LANGS:
    path = ROOT / "i18n" / f"{lang}.toml"
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        error(path, f"cannot read: {exc}")
        continue
    i18n[lang] = {f"{table}.{key}" for table, values in data.items() for key in values}
for lang, keys in i18n.items():
    if DEFAULT_LANG in i18n and keys != i18n[DEFAULT_LANG]:
        error(ROOT / "i18n" / f"{lang}.toml", f"keys differ from {DEFAULT_LANG}.toml: {sorted(keys ^ i18n[DEFAULT_LANG])}")

versions = yaml.safe_load((ROOT / "data" / "versions.yml").read_text(encoding="utf-8")) or {}
for app in ("desktop", "android"):
    if not re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?", str(versions.get(app, ""))):
        error(ROOT / "data" / "versions.yml", f"'{app}' must be a version like 1.2.3 (no leading v)")

if errors:
    print(f"{len(errors)} problem(s):")
    for line in errors:
        print(f"  {line}")
    sys.exit(1)
print(f"OK: {len(pages)} files, {len(LANGS)} languages")
