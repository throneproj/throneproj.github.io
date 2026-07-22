+++
title = "Deep Links"
description = "Use throne:// deep links to add subscriptions, share proxies, and import routing profiles with a single click."
weight = 2

[extra]
+++

Throne registers a custom `throne://` URL scheme with your operating system. A deep link is just a `throne://` URL that tells a running (or not‑yet‑running) Throne instance to perform an action — such as adding a subscription or importing a routing profile — without the user copying values into dialogs by hand.

This is handy for provider websites, support pages, QR codes, scripts, or simply sharing a routing profile with a friend.

> Links that add a subscription or a routing profile ask for confirmation first: Throne shows you exactly what will be added and waits for you to approve it. The one exception is `add`, which imports a single proxy profile straight into the current group without a prompt — the same as pasting a `vless://` link.

## How Throne receives a deep link

The `throne://` scheme is registered automatically the first time you run Throne, on **Windows, Linux, and macOS**. Because Throne ships as a portable archive with no installer, registration runs at startup, requires no administrator rights, and repairs itself automatically if you move or update the app folder.

Once registered, Throne accepts a deep link from any of these sources:

- **Clicking a `throne://` link** in a browser, chat app, or document — the OS hands it to Throne.
- **`Program` → `Add profile from clipboard`** (also under the `Server` menu, shortcut `Ctrl+V`), which reads the link from your clipboard.
- **Dragging and dropping** the link text onto the main window.
- **Passing it as a launch argument** on the command line (Windows/Linux). On macOS the system delivers the URL to the already-running app instead.

If Throne is already open, the link is handed to the existing window instead of starting a second instance.

## Link format

Every deep link has the same shape — a command, a slash, and a Base64 payload:

```
throne://<command>/<base64_payload>
```

- The command is **case‑insensitive** (`throne://AddSub/...` and `throne://addsub/...` are the same).
- **The slash and the payload are required.** A link with no `/<payload>` after the command is dropped silently — nothing happens and nothing is logged.
- There are no query parameters. Everything the link carries lives inside the Base64 payload.

| Command | Purpose | Confirms first? |
| --- | --- | --- |
| `addsub` | Add a subscription group and fetch it immediately | Yes |
| `route` | Import a routing profile carried inside the link | Yes |
| `remoteroute` | Add one or more remote routing profiles by URL | Yes |
| `add` | Add a single proxy profile to the current group | No |

An unrecognized command is ignored and noted in the log as `Ignored deeplink with unknown command`.

### Which Base64 alphabet to use

This matters, and it differs per command:

| Command | Accepted encoding |
| --- | --- |
| `addsub` | **Standard** Base64 only (the `+` and `/` alphabet). Keep the `=` padding. |
| `remoteroute` | **Standard** Base64 only (the `+` and `/` alphabet). Keep the `=` padding. |
| `route` | URL‑safe Base64, standard Base64, or even plain unencoded JSON. |
| `add` | Produced by Throne — see [`add`](#add) below. |

For `addsub` and `remoteroute`, a URL‑safe payload containing `-` or `_` will fail to decode and the link will be rejected. Encode with the standard alphabet.

## `addsub` — Add a subscription

Adds a new subscription group and updates it right away.

```
throne://addsub/<base64>
```

The payload is the Base64 of a single line:

```
<subscription_url>[#<group_name>]
```

| Part | Required | Description |
| --- | --- | --- |
| `<subscription_url>` | **Yes** | The subscription URL. |
| `#<group_name>` | No | The name for the new group, written as the URL fragment. Defaults to the host of the subscription URL when omitted. |

Auto‑update is **not** part of the link. Throne asks about it in the confirmation dialog, with the **Auto update** checkbox ticked by default.

### Example

To add `https://example.com/sub/abc123` as a group named **MyProvider**, Base64‑encode:

```
https://example.com/sub/abc123#MyProvider
```

and use the result as the payload:

```
throne://addsub/aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWIvYWJjMTIzI015UHJvdmlkZXI=
```

Throne asks you to confirm:

> Add this subscription?
>
> Name: MyProvider
> URL: https://example.com/sub/abc123
>
> ☑ Auto update

After you confirm, the group is created and the subscription is fetched immediately.

> Because the whole thing is Base64‑encoded, you do **not** percent‑encode the subscription URL — its `?`, `&`, and `/` characters are safely hidden inside the payload. Do percent‑encode the group name if it contains spaces or other special characters (a space becomes `%20`).

## `route` — Import a routing profile

Imports a complete routing profile (default outbound plus rules) carried inside the link.

```
throne://route/<base64>
```

The payload is the routing profile encoded as Base64. URL‑safe Base64 (with or without padding) is what Throne itself generates; standard Base64 and plain unencoded JSON are also accepted.

### How to create a route link

You normally don't build these by hand — Throne generates them for you:

1. Open `Routing Menu` → `Routing Settings`.
2. Select the routing profile you want to share.
3. Press `Ctrl+C` (or use the export action).

Throne copies a ready‑to‑share `throne://route/...` link to your clipboard. Send it to anyone; when they open it (or paste it into `Routing Settings` with `Ctrl+V`, or use `Add profile from clipboard`), Throne shows the profile name and any notes, then imports it on confirmation.

### What's inside the payload

The Base64 decodes to a small JSON envelope describing the profile:

```json
{
  "kind": "throne-route-profile",
  "v": 1,
  "name": "Bypass LAN",
  "default_outbound": "proxy",
  "rules": []
}
```

So the link looks like this (the payload is the Base64 of that JSON):

```
throne://route/eyJraW5kIjoidGhyb25lLXJvdXRlLXByb2ZpbGUiLCJ2IjoxLCJuYW1lIjoiQnlwYXNzIExBTiIsImRlZmF1bHRfb3V0Ym91bmQiOiJwcm94eSIsInJ1bGVzIjpbXX0
```

Profiles built from a hand‑written route section carry `"raw": true` and a `route` object instead of `rules`; Throne re‑maps the outbound references by name when it imports them, and tells you about anything it could not resolve.

> Throne also recognizes the same payload as plain JSON or bare Base64 when you import from the clipboard, so a link copied from another machine works even if it loses the `throne://route/` prefix along the way. A legacy bare array of rules is accepted too — it opens in the editor so you can give it a name and a default outbound.

## `remoteroute` — Add remote routing profiles

Adds one or more **remote** routing profiles by URL. Where `route` packs an entire profile inside the link, `remoteroute` carries links to profiles hosted online: Throne downloads the rules from each URL and, when you allow it, keeps them current automatically. This is how a provider hands you a maintained routing profile — one that keeps improving without you re‑importing it.

```
throne://remoteroute/<base64>
```

The payload is the Base64 of a plain **newline‑separated list of URLs** — not JSON:

```
<profile_url_1>[#<name_1>]
<profile_url_2>[#<name_2>]
...
```

| Part | Required | Description |
| --- | --- | --- |
| `<profile_url>` | **Yes** | An `http://` or `https://` link to the routing profile. Lines that aren't valid http(s) URLs are skipped. |
| `#<name>` | No | Display name for the profile, written as the URL fragment. Defaults to the host of the URL when omitted. |

Auto‑update is **not** per entry. Throne asks once in the confirmation dialog, and the answer applies to every profile in the link. The **Auto update** checkbox is ticked by default.

### Example

Base64‑encode this two‑line list:

```
https://example.com/routes/bypass-iran.json#BypassIran
https://example.com/routes/ads.json
```

and use the result as the payload:

```
throne://remoteroute/aHR0cHM6Ly9leGFtcGxlLmNvbS9yb3V0ZXMvYnlwYXNzLWlyYW4uanNvbiNCeXBhc3NJcmFuCmh0dHBzOi8vZXhhbXBsZS5jb20vcm91dGVzL2Fkcy5qc29u
```

Throne lists everything the link will add and waits for your confirmation:

> Add these remote routing profiles?
>
> 1. https://example.com/routes/bypass-iran.json
> 2. https://example.com/routes/ads.json
>
> ☑ Auto update

After you confirm, each profile is added and fetched immediately. Profiles with auto‑update enabled are then refreshed in the background by the **Routing profiles auto update** interval in **Basic Settings** (an interval under 30 minutes turns updates off).

Each remote URL should serve a routing profile in any form `route` accepts — a `throne://route/...` link, its Base64, or the raw JSON.

## `add` — Add a single proxy profile {#add}

Adds one proxy profile to the current group from a JSON outbound config.

```
throne://add/<base64>
```

The payload is the Base64 of the profile's outbound JSON — the same object Throne exports for a server. Unlike the other three commands, this one **does not ask for confirmation**: the profile is added straight to the current group, exactly as if you had pasted a `vless://` or `ss://` link.

You don't build these by hand. Throne produces them for you:

- `Server` → `Share` → `Copy links of selected (Deep Links)` (`Ctrl+Alt+C`)
- The share/QR window shows the deep link alongside the ordinary share link
- `Copy profile share links (Deep Links)` in the group editor

Deep links are useful for protocols and options that have no standard `://` share URL, since the full JSON config survives the round trip.

## Troubleshooting

- **Clicking a link does nothing / the browser asks which app to use.** Launch Throne once so it can register the scheme, then try again. If you moved the Throne folder, simply start it again — registration self‑heals on startup.
- **Nothing happens at all, and the log is empty.** The link is probably missing the slash and payload after the command (`throne://addsub` instead of `throne://addsub/<base64>`), or its Base64 could not be decoded. Both cases are dropped silently.
- **"Ignored deeplink with unknown command".** The command portion isn't `addsub`, `route`, `remoteroute`, or `add`. Check the spelling of the word right after `throne://`.
- **"The link did not contain a subscription URL".** The `addsub` payload decoded, but there was no URL in front of the `#` — check that you encoded `<url>#<name>` and not just `#<name>`.
- **"Base64 is invalid." / "Deep link has no data".** The payload is empty or isn't decodable. For `addsub` and `remoteroute`, make sure you used **standard** Base64: a URL‑safe payload containing `-` or `_` is rejected.
- **"The link did not contain any valid remote routing profiles".** None of the decoded lines started with `http://` or `https://`. Remember the payload is a newline‑separated URL list, not a JSON array.
- **"The link could not be parsed".** A `route` payload that isn't valid JSON, Base64, or a Throne route link — or a JSON object without the `"kind": "throne-route-profile"` marker.
