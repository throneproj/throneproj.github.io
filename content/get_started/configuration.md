+++
title = "Quick Start"
description = "Add your servers, test them, choose a routing profile and connect with Throne on Windows, Linux or macOS."
weight = 2
toc = true
+++

This page takes you from a new installation to a working connection. You need a subscription link or a share link from your provider, or the details of your own server. If Throne is not installed yet, see [Installation](@/get_started/installation.md). For Android, see [Throne for Android](@/android/_index.md#quick-start).

## Add servers {#add-servers}

Throne stores each server as a **profile**. Profiles belong to **groups**, which are the tabs above the profile list. A **subscription** is a group that Throne downloads from a URL and can update later.

### Paste a subscription link {#paste-subscription}

1. Copy the subscription URL. It starts with `https://`.
2. In the main window, press `Ctrl+V`, or click `Program` → `Add profile from clipboard`.
3. Throne asks "How to update?". Choose `Create new subscription group` in the list and click `OK`.

Throne creates a group named after the host name in the URL and downloads its profiles right away.

The other two choices do not create a subscription:

| Choice | What it does |
|---|---|
| `Add profiles to this group` | Imports the profiles once into the current group. Throne does not keep the URL, so you cannot update these profiles later. |
| `Import HTTP proxy profile` | Treats the URL as the address of an HTTP proxy server. |

### Add a subscription from the Groups menu {#groups-menu}

1. Click `Groups` → `Add new Group`.
2. Enter a `Name`.
3. Set `Type` to `Subscription`. You cannot change the type later.
4. Paste the subscription URL into `URL`.
5. Click `OK`.
6. Right-click the tab of the new group and choose `Update subscription`.

Creating the group does not download anything; step 6 does. Later, you can update the current group with `Groups` → `Update subscription` (`Ctrl+U`). For automatic updates and provider settings, see [Subscriptions & Groups](@/guides/subscriptions.md#auto-update).

### Add single profiles {#single-profiles}

Profiles that you add this way go into the group whose tab is selected.

- **Share links** such as `vless://`, `ss://` or `trojan://`: copy one or more links, one per line, and press `Ctrl+V`.
- **A QR code on your screen**: click `Program` → `Scan QR Code` (`Ctrl+Shift+Q`). Throne reads QR codes on all your screens.
- **Files and images**: drag config files, QR code images or link text onto the main window, or click `Program` → `Add profile from File(s)` (`Ctrl+O`).
- **By hand**: click `Program` → `New profile` (`Ctrl+N`).

All supported links and files are listed in [Protocols & Import Formats](@/reference/protocols.md#import-formats).

## Test servers {#test-servers}

A URL test connects through each profile and measures the delay.

1. Click any profile in the list, then press `Ctrl+A` to select all profiles of the group.
2. Right-click the selection and choose `Url Test Selected` (`Ctrl+Shift+S`).

To test the whole group without selecting, click `Groups` → `Url Test Group` (`Ctrl+Shift+G`).

The `Test Result` column shows the delay in milliseconds, or `Unavailable` if the test failed. Click the `Test Result` column header to sort by it, and click it again to reverse the order.

To delete the profiles that failed, click `Groups` → `Remove Unavailable` (`Ctrl+Shift+R`). In a subscription group, the next update adds them again if the provider still lists them.

For speed tests, IP tests and automatic server choice, see [Testing & Auto Selector](@/guides/testing.md).

## Choose routing {#choose-routing}

Routing decides which traffic goes through the proxy and which goes directly to the Internet. This step is optional: the built-in routing profile `Default` sends all traffic through the proxy.

If you want the websites of your own country to open directly, without the proxy, download a ready-made routing profile:

1. Click `Routing` → `Download Profiles` and choose `China`, `Iran` or `Russia`.
2. Throne asks "Add these remote routing profiles?" and lists them. Keep `Auto update` ticked and click `OK`.
3. Open the `Routing` menu again. Your routing profiles are listed at the bottom, and the ticked one is active.
4. Click the routing profile that you want. If a profile is running, Throne restarts it with the new routing.

| Routing profile | Through the proxy | Directly |
|---|---|---|
| `Bypass China`, `Bypass Iran`, `Bypass Russia` | All other traffic | Websites and IP addresses in that country, and your local network |
| `Proxy China Blocked`, `Proxy Russia Blocked` | Only websites that are blocked in that country | All other traffic |
| `Proxy Antizapret`, `Proxy Refilter` (Russia) | Only websites on these block lists | All other traffic |

Only one routing profile is active at a time, so choose one of them. You do not need to delete `Default` or the other profiles. To write your own rules, see [Routing](@/guides/routing.md).

## Connect {#connect}

1. Click the profile that you want to use.
2. Press `Enter`, or click the Start button to the right of `Tools`. Its tooltip says `Start`.
3. Tick `System Proxy` or `Tun Mode`, next to the Start button.

| Mode | What it does |
|---|---|
| `System Proxy` | Sets the proxy settings of your system to Throne's local port (`127.0.0.1:2080` by default) while a profile runs. Browsers and other apps that follow the system proxy settings use it. See [System proxy](@/guides/proxy_modes.md#system-proxy). |
| `Tun Mode` | Creates a virtual network adapter that captures the traffic of all apps, including apps that ignore proxy settings. It needs administrator or root rights. See [TUN mode](@/guides/proxy_modes.md#tun-mode). |

You can turn on both modes at the same time. The window title then shows `[Tun+System Proxy]`. If you tick neither, apps that you set up yourself can still use Throne as a SOCKS5 or HTTP proxy at `127.0.0.1:2080`. To choose a mode, see [Which mode to use](@/guides/proxy_modes.md#which-mode).

The first time you tick `Tun Mode`, Throne asks for the rights it needs:

- **Windows:** Throne asks you to run it as administrator. Click `Yes` and confirm the Windows prompt. Throne restarts as administrator with `Tun Mode` on. If Windows Firewall asks whether to allow `ThroneCore`, allow it.
- **Linux:** Throne asks to give its core root privileges. Click `Yes` and enter your password. Then tick `Tun Mode` again.
- **macOS:** Throne asks to give its core root privileges. Click `Yes`, and Terminal opens. Enter your password in Terminal, then tick `Tun Mode` again.

For details and alternatives, see [TUN privileges](@/guides/tun_mode.md#privileges).

### Check the connection {#check-connection}

The bottom left corner of the window shows the running profile as `[group] profile`. A moment later, the country and city of your exit IP address appear below it.

Click this text to test the running profile. Throne shows `Test Result: <n> ms` if the connection works, or `Test Result: Unavailable` if it does not. If the test fails, try another profile or see [Troubleshooting](@/help/troubleshooting.md).

### Stop and quit {#stop-and-quit}

- To disconnect, click the same button again (its tooltip now says `Stop`), or press `Ctrl+S`.
- Closing the window only hides Throne in the system tray. To quit, click `Program` → `Exit`, or use `Exit` in the tray menu.
- With `Program` → `Remember last profile` on, Throne starts your last profile again when it starts, and turns `System Proxy` and `Tun Mode` back on if they were on. `Program` → `Start with system` starts Throne when you log in.

{% alert_warning() %}
Always quit Throne with `Exit`. If Throne is killed while a profile runs with `System Proxy` on, your system keeps using a proxy that no longer runs, and websites stop loading. See the [FAQ](@/help/faq.md#force-quit).
{% end %}

## Next steps {#next-steps}

- [Subscriptions & Groups](@/guides/subscriptions.md): automatic updates, and the User-Agent and HWID settings that some providers need.
- [Routing](@/guides/routing.md): your own rules, for example to send only a few websites through the proxy.
- [Testing & Auto Selector](@/guides/testing.md): speed tests, and automatic switching to a working server.
- [TUN Mode](@/guides/tun_mode.md): TUN settings and side effects.
- [DNS](@/guides/dns.md): DNS servers and leak tests.
- [Troubleshooting](@/help/troubleshooting.md) and [FAQ](@/help/faq.md): help when something does not work.
