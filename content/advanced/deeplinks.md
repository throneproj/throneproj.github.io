+++
title = "Deep Links"
description = "Use throne:// links to add subscriptions, routing profiles and proxy profiles with one click, on desktop and Android."
weight = 70
toc = true
+++

A deep link is a `throne://` URL that tells Throne to do one job: add a subscription, import a routing profile, add remote routing profiles, or add one proxy profile. Providers put deep links on websites and in QR codes. You can also use them to share your own routing profiles.

## How Throne receives a deep link {#receive}

Your system must know that Throne opens `throne://` links. Throne registers itself for your user account only, and this needs no administrator rights.

| System | Registered by default |
| --- | --- |
| Linux | Yes |
| macOS | Yes, when you run Throne from `Throne.app` |
| Windows, installed with the installer | Yes |
| Windows, unpacked from a ZIP file | No |

To turn registration on, for example for a Windows ZIP copy:

1. Open `Settings` → `Basic Settings`.
2. On the `Common` tab, under `Links and Files`, tick `Register throne:// links at startup`.
3. Press `OK`. Throne registers itself right away.

While the option is on, Throne checks the registration at every start and repairs it, for example after you move the Throne folder. If you keep several copies on Windows or Linux, links open in the last copy that started with the option on.

The status next to the option shows `Installed` when links open this copy of Throne. The `Install` button registers once, without turning the option on. `Uninstall` removes the registration and turns the option off. Unticking the option alone keeps the existing registration.

**macOS:** the link handler is part of `Throne.app`, so there are no `Install` and `Uninstall` buttons. If Throne does not run from the app bundle, the option shows `Not available for this installation`.

Throne accepts a deep link in these ways:

- **Click the link** in a browser, chat app or document. If Throne is not running, it starts and then handles the link.
- **Copy the link** and press `Ctrl+V` in the main window (`Program` → `Add profile from clipboard`). This works even when registration is off.
- **Drag the link text** onto the main window.
- **Pass the link as an argument** when you start Throne. See [Command line](@/reference/files.md#command-line).

{% alert_info() %}
On desktop, `Scan QR Code` and dropped QR images import only `add` links. For another deep link in a QR code, copy the text after `QR Code Result:` from the `Logs` tab and press `Ctrl+V`.
{% end %}

## Link format {#format}

Every deep link has the same shape:

```text
throne://<command>/<payload>
```

- Write `throne://` in lowercase. The command is not case-sensitive: `throne://AddSub/…` works.
- A slash and the payload must follow the command. Without the slash, most links do nothing.
- Throne ignores anything after `?` or `#` in the link. Everything the link carries is inside the payload.
- If the payload is percent-encoded (for example `%2B` instead of `+`), Throne decodes it first.

| Command | What it does | Asks first? |
| --- | --- | --- |
| `addsub` | Adds a subscription group and updates it | Yes |
| `route` | Imports a routing profile carried inside the link | Yes |
| `remoteroute` | Adds remote routing profiles by URL | Yes |
| `add` | Adds one proxy profile to the current group | No. On Android, yes when you tap the link in another app. |

### Base64 rules {#base64}

The payload is Base64 text. Which Base64 alphabet works depends on the command:

| Command | Accepted payload |
| --- | --- |
| `addsub`, `remoteroute` | Standard Base64 only: letters, digits, `+` and `/`. The `=` padding at the end is optional. |
| `route`, `add` | URL-safe Base64 (`-` and `_`) or standard Base64, with or without padding. Throne itself writes URL-safe Base64 without padding. |

For `addsub` and `remoteroute`, a URL-safe payload that contains `-` or `_` fails. Keep the payload on one line, without spaces.

To encode a payload on Linux, or in Git Bash on Windows:

```bash
printf '%s' 'https://example.com/sub/abc123#MyProvider' | base64 -w 0
```

On macOS, leave out `-w 0`. In PowerShell:

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('https://example.com/sub/abc123#MyProvider'))
```

Both commands print standard Base64 with padding.

## `addsub`: add a subscription {#addsub}

Adds a new subscription group and updates it right away.

```text
throne://addsub/<base64>
```

The payload is the Base64 of one line:

```text
<subscription_url>#<group_name>
```

| Part | Required | Description |
| --- | --- | --- |
| `<subscription_url>` | Yes | The subscription URL, unchanged. Its `?`, `&` and `/` are safe inside the Base64, so you do not need to percent-encode it. |
| `#<group_name>` | No | The name of the new group. Without it, the group is named after the host of the URL. Percent-encoding the name is optional: a plain space works. |

For example, to add `https://example.com/sub/abc123` as a group named `MyProvider`, encode `https://example.com/sub/abc123#MyProvider`:

```text
throne://addsub/aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWIvYWJjMTIzI015UHJvdmlkZXI=
```

Throne shows "Add this subscription?" with the group name and the URL, and an `Auto update` checkbox that is ticked. After you confirm, Throne creates the group and updates it.

{% alert_info() %}
`Auto update` only sets whether the new group takes part in automatic updates: when it is ticked, `Skip automatic update` is off in the group settings. Automatic updates also need `Basic Settings` → `Subscription` → `Subscription auto update` → `Enable`, which is off by default. See [Subscriptions](@/guides/subscriptions.md#auto-update).
{% end %}

## `route`: import a routing profile {#route}

Imports a whole routing profile (default outbound and rules) that is carried inside the link.

```text
throne://route/<base64>
```

You do not need to build these links by hand. In `Routing Settings`, on the `Route` tab, select the profile and press `Export`, or press `Ctrl+C` in the list. Throne copies a `throne://route/…` link to the clipboard.

When someone opens the link, Throne shows "Add this routing profile?" with the name, plus notes about anything it could not import. After they confirm, the profile is added to their list. If the profile has VPN endpoints, Throne creates those OpenVPN or OpenConnect profiles before it asks, and keeps them even when the import is cancelled. The imported routing profile does not become active: choose it in the list at the bottom of the `Routing` menu.

The payload is the Base64 of a small JSON object like this one:

```json
{
  "kind": "throne-route-profile",
  "v": 1,
  "name": "Example",
  "default_outbound": "proxy",
  "rules": []
}
```

This link carries that JSON:

```text
throne://route/eyJraW5kIjoidGhyb25lLXJvdXRlLXByb2ZpbGUiLCJ2IjoxLCJuYW1lIjoiRXhhbXBsZSIsImRlZmF1bHRfb3V0Ym91bmQiOiJwcm94eSIsInJ1bGVzIjpbXX0
```

`default_outbound` is `proxy`, `direct`, `block` or `warp-bypass`. A raw profile (a hand-written sing-box `route` section) carries `"raw": true` and a `route` object instead of `rules`. Throne looks up the servers that the rules use by their names and tells you about any it could not find. For more about sharing, see [Routing](@/guides/routing.md#share-profiles).

### Import in Routing Settings {#routing-settings-import}

You can also paste a link on the `Route` tab of `Routing Settings`: press `Import`, or press `Ctrl+V` in the list. In the main window, only text that starts with `throne://` counts as a deep link. Here, Throne also accepts the Base64 payload alone, the plain JSON, and an old-style JSON list of rules, which opens in the editor so you can name it. A profile imported from a `route` link, its Base64 or its JSON also becomes the selected `Routing Profile` on the `Common` tab when you press `OK`.

A `remoteroute` link pasted here adds its profiles with auto update off, because this prompt has no `Auto update` checkbox. You can tick `Auto update` later in the editor of each profile.

## `remoteroute`: add remote routing profiles {#remoteroute}

Adds one or more remote routing profiles. A `route` link carries the whole profile. A `remoteroute` link carries only URLs: Throne downloads each profile and can keep it up to date. Use it to hand out a routing profile that you maintain.

```text
throne://remoteroute/<base64>
```

The payload is the Base64 of a plain list of URLs, one per line. It is not JSON:

```text
<profile_url_1>#<name_1>
<profile_url_2>#<name_2>
```

| Part | Required | Description |
| --- | --- | --- |
| `<profile_url>` | Yes | An `http://` or `https://` URL. Lines that do not start with one of these are skipped. |
| `#<name>` | No | The profile name. Without it, the profile is named after the host of the URL. |

Each URL must serve a structured routing profile: a `throne://route/` link, its Base64 payload, or the JSON inside it. Raw profiles cannot be used as remote profiles.

For example, encode these two lines:

```bash
printf '%s\n%s' 'https://example.com/routes/bypass-iran.json#BypassIran' 'https://example.com/routes/ads.json' | base64 -w 0
```

The result is this link:

```text
throne://remoteroute/aHR0cHM6Ly9leGFtcGxlLmNvbS9yb3V0ZXMvYnlwYXNzLWlyYW4uanNvbiNCeXBhc3NJcmFuCmh0dHBzOi8vZXhhbXBsZS5jb20vcm91dGVzL2Fkcy5qc29u
```

Throne lists the URLs under "Add these remote routing profiles?" with one `Auto update` checkbox for all of them. The checkbox is ticked. After you confirm, Throne adds the profiles and downloads them. The log shows how many it fetched.

- Throne refreshes profiles that have `Auto update` on only when `Basic Settings` → `Subscription` → `Routing profiles auto update` → `Enable` is ticked. It is off by default. To update by hand, use `Update` on the `Route` tab of `Routing Settings`. See [Remote profiles](@/guides/routing.md#remote-profiles).
- An update replaces the rules and the default outbound of the profile with the downloaded ones. The name of the profile stays.
- URLs on `raw.githubusercontent.com` are downloaded through the `Remote Rule-set Mirror` chosen on the `Common` tab of `Routing Settings` (a jsDelivr mirror by default). A mirror may serve an older copy for some time after you change the file.
- `Routing` → `Download Profiles` works the same way: it downloads a `remoteroute` link from Throne's routing profile repository and shows the same prompt.

## `add`: add one proxy profile {#add}

Adds one proxy profile to the current group.

```text
throne://add/<base64>
```

The payload is the Base64 of the profile's outbound settings as JSON. On desktop this link does not ask for confirmation: the profile is added at once, as if you had pasted a `vless://` or `ss://` link.

Throne generates these links for you:

- Right-click profiles in the list → `Share` → `Copy links of selected (Deep Links)` (`Ctrl+Alt+C`).
- Right-click a profile → `Share` → `QR Code and link`. The window shows either the normal share link or the deep link. Tick `Deep Link` to switch between them.
- `Groups` → `Edit current Group` → `Copy profile share links (Deep Links)`.

A deep link carries the full profile configuration, so it also works for profile types and options that have no standard share link. For such profiles, `Copy links of selected` (`Ctrl+C`) usually copies a deep link automatically, and the QR window opens with `Deep Link` ticked. If such a profile has advanced connection options, such as a bind interface, use `Copy links of selected (Deep Links)` instead.

`add` links also work wherever normal share links work: inside subscriptions, in files and in QR codes.

## On Android {#android}

Throne for Android 2.0.0 handles the same four commands. It also accepts `clash://install-config?url=…&name=…` links, which add a subscription like `addsub`. In these links, percent-encode the `url` value. The `throne://` scheme is registered when you install the app; there is no setting for it.

Tap the link in another app, or use `Add profile` → `Import from clipboard` or `Scan QR code` on the `Profiles` screen. On Android, QR codes work for all four commands. `route` and `remoteroute` links also work with `Import` on the `Routing` screen.

Differences from desktop:

- An `add` link that you tap in another app asks "Confirm you want to import profile …?" first. Links such as `vless://` tapped in another app ask the same. From the clipboard or a QR code, the profile is imported without a question.
- An imported routing profile is added but does not become active. Tap it on the `Routing` screen to use it.
- Raw routing profiles from desktop (`"raw": true`) are refused with "raw routing profiles are not supported on Android". Endpoints in a shared routing profile are dropped with a note.
- An unknown command shows "Ignored deeplink with unknown command: …" on the screen, not only in the log.
- Scheduled updates need `Settings` → `Subscriptions` → `Subscription auto update` for subscriptions, and `Settings` → `Routing` → `Auto update remote profiles` for remote routing profiles. Both are off by default.

The Android app can also create these links: `add` links for profiles and `route` links for routing profiles.

## Troubleshooting {#troubleshooting}

These messages are from Throne desktop.

- **Clicking a link does nothing, or the browser asks which app to use.** The link handler is not registered for this copy. On a Windows ZIP copy, turn on `Register throne:// links at startup` (see [How Throne receives a deep link](#receive)). On macOS, run Throne from `Throne.app`. Otherwise start Throne once. If you keep several copies, press `Install` in the copy that should open links. You can always copy the link and press `Ctrl+V` in Throne instead.
- **Linux: links still do not open.** Registration runs the `update-desktop-database` tool from the `desktop-file-utils` package. If the tool was missing, install it, then press `Install` next to `Register throne:// links at startup`.
- **Nothing happens and the log stays empty.** Throne drops these links without a message:
  - an `addsub` link whose payload is not valid standard Base64, for example URL-safe Base64 with `-` or `_`, or a payload with spaces or line breaks;
  - a link without the slash after the command, except `add` and `remoteroute` links;
  - a link with an unknown command whose payload does not decode.
- **"Ignored deeplink with unknown command: …" in the log.** The word after `throne://` is not `addsub`, `route`, `remoteroute` or `add`. Check the spelling.
- **"The link did not contain a subscription URL."** The `addsub` payload decoded, but there is no URL before the `#`. Encode `<url>#<name>`, not only `#<name>`.
- **"Deep link has no data" or "Base64 is invalid."** These come from `remoteroute` links: nothing follows `throne://remoteroute/`, or the payload is not standard Base64.
- **"The link did not contain any valid http(s) routing profile URLs."** The `remoteroute` payload decoded, but no line starts with `http://` or `https://`. The payload must be a list of URLs, one per line, not JSON.
- **"The link did not contain any valid remote routing profiles."** The link has no slash after `remoteroute`.
- **"The link could not be parsed:" and a reason.** This comes from `route` links:
  - "Empty input": nothing follows `throne://route/`.
  - "Input is not valid JSON, base64, or a Throne route link": the payload is damaged or cut off.
  - "Unrecognized route object": the JSON has no `"kind": "throne-route-profile"`.
- **"Imported 0 profile(s)" in the log.** An `add` payload is damaged or cut off. Or you scanned a QR code that holds an `addsub`, `route` or `remoteroute` link: copy the text after `QR Code Result:` from the log and press `Ctrl+V`.
- **"Remote routing profile … failed: …" in the log.** The profile was added, but its URL could not be downloaded or does not serve a structured routing profile. Fix the URL or the file, then use `Update` on the `Route` tab of `Routing Settings`.
