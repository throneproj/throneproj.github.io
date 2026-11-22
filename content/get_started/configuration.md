+++
title = "Quick Start"
description = "Add your servers, test them, choose a routing profile and connect with Throne on Windows, Linux or macOS."
weight = 2
toc = true
+++

You need a subscription link or a share link from your provider, or the details of your own server. For Android, see [Throne for Android](@/android/_index.md#quick-start).

## Add servers {#add-servers}

Throne stores each server as a **profile**. Profiles belong to **groups**, the tabs above the profile list. A **subscription** is a group that Throne downloads from a URL and can update later.

### Add a subscription {#paste-subscription}

1. Copy the subscription URL. It starts with `https://`.
2. In the main window, press `Ctrl+V` (or `Program` → `Paste from clipboard`).
3. Choose `Create new subscription group` and click `OK`.

Throne creates a group named after the host in the URL and downloads its profiles. If your provider sends plan details, a card above the profile list shows your used traffic and expiry date. `Add profiles to this group` would import the profiles only once, without the URL, so they cannot be updated.

Update the current group later with `Groups` → `Update subscription` (`Ctrl+U`). For automatic updates, see [Subscriptions & Groups](@/guides/subscriptions.md#auto-update).

### Add single profiles {#single-profiles}

Profiles go into the group whose tab is selected.

- **Share links** such as `vless://`, `ss://` or `trojan://`: copy one or more, one per line, and press `Ctrl+V`.
- **A QR code on your screen**: `Program` → `Scan QR code` (`Ctrl+Shift+Q`).
- **Files and QR code images**: drag them onto the main window, or `Program` → `Import from file` (`Ctrl+O`).
- **By hand**: `Program` → `New profile` (`Ctrl+N`).

All supported links and files are listed in [Protocols & Import Formats](@/reference/protocols.md#import-formats).

## Test servers {#test-servers}

Click `Groups` → `Test` → `URL test` (`Ctrl+Shift+G`) to measure the delay of every profile in the group. To test only some, select them, right-click and choose `Test` → `URL test` (`Ctrl+Shift+S`).

The `Test Result` column shows the delay in milliseconds, or `Unavailable`. Click its header to sort. `Groups` → `Clean up` → `Remove unavailable` deletes the failed profiles; a subscription update adds them again if the provider still lists them.

For speed tests and automatic server choice, see [Testing & Auto Selector](@/guides/testing.md).

## Choose routing {#choose-routing}

This step is optional: the built-in `Default` routing profile sends all traffic through the proxy. To open the websites of your own country directly:

1. Click `Routing` → `Download routing profile` and choose `China`, `Iran` or `Russia`. Keep `Auto update` ticked and click `OK`.
2. Open the `Routing` menu again and choose `Bypass China`, `Bypass Iran` or `Bypass Russia` at the top. A running profile restarts with the new routing.

A "Bypass" profile proxies everything except the websites and IP addresses of that country and your local network. For the other downloaded profiles and your own rules, see [Routing](@/guides/routing.md#download-profiles).

## Connect {#connect}

1. Click the profile that you want to use.
2. Press `Enter`, or click the Start button to the right of `Tools`.
3. Tick `System proxy` or `Tun mode`, next to the Start button.

| Mode | What it does |
|---|---|
| `System proxy` | Points the proxy settings of your system to Throne (`127.0.0.1:2080` by default). Browsers and other apps that follow these settings use the proxy. |
| `Tun mode` | Captures the traffic of all apps, including apps that ignore proxy settings. Needs administrator or root rights. |

You can turn on both. With neither, apps that you set up yourself can still use Throne as a SOCKS5 or HTTP proxy at `127.0.0.1:2080`. See [Which mode to use](@/guides/proxy_modes.md#which-mode).

The first time you tick `Tun mode`, Throne asks for the rights it needs:

- **Windows:** click `Grant privileges`, confirm the Windows prompt, then tick `Tun mode` again. Only the core gets [administrator rights](@/guides/tun_mode.md#privileges-windows); Throne keeps running as a standard user. If Windows Firewall asks about `ThroneCore`, allow it.
- **Linux:** click `Yes`, enter your password, then tick `Tun mode` again.
- **macOS:** click `Yes`, enter your password in the Terminal window that opens, then tick `Tun mode` again.

See [Tun privileges](@/guides/tun_mode.md#privileges) for details.

### Check the connection {#check-connection}

The bottom left corner of the window shows the running profile and, a moment later, the country and city of your exit IP address. Click it to test the connection: `Test Result: <n> ms` means it works. If you see `Unavailable`, try another profile or see [Troubleshooting](@/help/troubleshooting.md).

### Stop and quit {#stop-and-quit}

- To disconnect, click the Start button again (now `Stop`), or press `Ctrl+S`.
- Closing the window only hides Throne in the tray. To quit, use `Program` → `Quit` or `Quit` in the tray menu.
- `Program` → `Remember last profile` reconnects when Throne starts, and `Program` → `Start with system` starts Throne when you log in.

{% alert_warning() %}
Always quit Throne with `Quit`. If Throne is killed while `System proxy` is on, your system keeps using a proxy that no longer runs, and websites stop loading. See the [FAQ](@/help/faq.md#force-quit).
{% end %}

## Find a setting {#find-setting}

To find any setting, press `Ctrl+K` and type part of its name; choosing one opens it. See [Search Settings](@/reference/shortcuts.md#command-palette).

## Next steps {#next-steps}

- [Subscriptions & Groups](@/guides/subscriptions.md): automatic updates, and the User-Agent and HWID settings that some providers need.
- [Routing](@/guides/routing.md): your own rules, for example to send only a few websites through the proxy.
- [Testing & Auto Selector](@/guides/testing.md): speed tests, and automatic switching to a working server.
- [Tun Mode](@/guides/tun_mode.md) and [DNS](@/guides/dns.md): settings, side effects and leak tests.
- [Troubleshooting](@/help/troubleshooting.md) and [FAQ](@/help/faq.md): help when something does not work.
