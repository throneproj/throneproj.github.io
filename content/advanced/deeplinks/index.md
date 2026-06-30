+++
title = "Deep Links"
description = "Use throne:// deep links to add subscriptions and import routing profiles with a single click."
weight = 2

[extra]
+++

Throne registers a custom `throne://` URL scheme with your operating system. A deep link is just a `throne://` URL that tells a running (or not‑yet‑running) Throne instance to perform an action — such as adding a subscription or importing a routing profile — without the user copying values into dialogs by hand.

This is handy for provider websites, support pages, QR codes, scripts, or simply sharing a routing profile with a friend.

> Every deep link asks for confirmation before anything is saved. Throne shows you exactly what will be added and waits for you to approve it, so opening a link can never silently change your configuration.

## How Throne receives a deep link

The `throne://` scheme is registered automatically the first time you run Throne, on **Windows, Linux, and macOS**. Because Throne ships as a portable archive with no installer, registration runs at startup, requires no administrator rights, and repairs itself automatically if you move or update the app folder.

Once registered, Throne accepts a deep link from any of these sources:

- **Clicking a `throne://` link** in a browser, chat app, or document — the OS hands it to Throne.
- **Pasting** the link onto the main window with `Ctrl+V`.
- **Dragging and dropping** the link text onto the main window.
- **`Server` → `Add profile from clipboard`**, which reads the link from your clipboard.
- **Passing it as a launch argument** on the command line (Windows/Linux).

If Throne is already open, the link is handed to the existing window instead of starting a second instance.

## Command reference

A deep link has the form:

```
throne://<command>/?<parameters>
```

The command is **case‑insensitive** (`throne://AddSub` and `throne://addsub` are the same), and the trailing slash before `?` is optional. Throne currently supports two commands.

| Command | Purpose |
| --- | --- |
| `addsub` | Add a subscription group and fetch it immediately |
| `route`  | Import a routing profile |

An unrecognized command is ignored and noted in the log.

## `addsub` — Add a subscription

Adds a new subscription group and updates it right away.

```
throne://addsub/?url=<subscription_url>&name=<group_name>&autoupdate=<value>
```

| Parameter | Required | Description |
| --- | --- | --- |
| `url` | **Yes** | The subscription URL. Must be **percent‑encoded** (see note below). If omitted, Throne shows a warning and does nothing. |
| `name` | No | The name for the new group. Defaults to the host of the subscription URL when omitted. |
| `autoupdate` | No | Whether the group updates automatically. Accepts `1`, `true`, `on`, or `yes` (case‑insensitive) to enable. **Defaults to enabled** when the parameter is absent. Any other value disables it. |

### Example

```
throne://addsub/?url=https%3A%2F%2Fexample.com%2Fsub%2Fabc123&name=My%20Provider&autoupdate=yes
```

This adds a group named **My Provider** for `https://example.com/sub/abc123` with automatic updates turned on. Throne asks you to confirm:

> Add this subscription?
> Name: My Provider
> URL: https://example.com/sub/abc123
> Auto update: On

After you confirm, the group is created and the subscription is fetched immediately.

> **Always percent‑encode the `url` value.** A subscription URL contains characters such as `:`, `/`, `?`, and `&` that would otherwise be misread as part of the deep link. For example, `https://example.com/sub?id=1` becomes `https%3A%2F%2Fexample.com%2Fsub%3Fid%3D1`. The same applies to spaces and special characters in `name` (a space becomes `%20`).

## `route` — Import a routing profile

Imports a complete routing profile (default outbound plus rules) carried inside the link.

```
throne://route?data=<base64>
```

| Parameter | Required | Description |
| --- | --- | --- |
| `data` | **Yes** | The routing profile encoded as Base64. URL‑safe Base64 (with or without padding) is recommended; standard Base64 is also accepted. |

### How to create a route link

You normally don't build these by hand — Throne generates them for you:

1. Open `Routes` → `Routing Settings`.
2. Select the routing profile you want to share.
3. Press `Ctrl+C` (or use the export action).

Throne copies a ready‑to‑share `throne://route?data=...` link to your clipboard. Send it to anyone; when they open it (or paste it / use `Add profile from clipboard`), Throne shows the profile name and any notes, then imports it on confirmation.

### What's inside `data`

The Base64 payload decodes to a small JSON envelope describing the profile:

```json
{
  "kind": "throne-route-profile",
  "v": 1,
  "name": "Bypass LAN",
  "default_outbound": "proxy",
  "rules": []
}
```

So the link above looks like this (the `data` value is the Base64 of that JSON):

```
throne://route?data=eyJraW5kIjoidGhyb25lLXJvdXRlLXByb2ZpbGUiLCJ2IjoxLCJuYW1lIjoiQnlwYXNzIExBTiIsImRlZmF1bHRfb3V0Ym91bmQiOiJwcm94eSIsInJ1bGVzIjpbXX0
```

> Throne also recognizes the same payload as plain JSON or bare Base64 when you import from the clipboard, so a link copied from another machine works even if it loses the `throne://route?data=` prefix along the way.

## Troubleshooting

- **Clicking a link does nothing / the browser asks which app to use.** Launch Throne once so it can register the scheme, then try again. If you moved the Throne folder, simply start it again — registration self‑heals on startup.
- **"Ignored deeplink with unknown command".** The command portion isn't `addsub` or `route`. Check the spelling of the word right after `throne://`.
- **"The link did not contain a subscription URL".** The `addsub` link is missing its `url` parameter, or the value was empty after decoding.
- **The subscription imports the wrong address.** The `url` value wasn't percent‑encoded, so part of it was cut off at a `?`, `&`, or `#`. Encode the value and rebuild the link.
