+++
title = "Quick Start"
description = "Add your servers, test them, choose a routing profile and connect with Throne on Windows, Linux or macOS."
weight = 2
toc = true
+++

This page takes you from a new installation to a working connection. You need a subscription link or a share link from your provider, or the details of your own server. If Throne is not installed yet, see [Installation](@/get_started/installation.md). For Android, see [Throne for Android](@/android/_index.md#quick-start).

Since 1.4.0, a new installation starts in Simple mode, which hides advanced options. All steps on this page work in Simple mode. See [Simple and Advanced mode](#interface-mode).

## Add servers {#add-servers}

Throne stores each server as a **profile**. Profiles belong to **groups**, which are the tabs above the profile list. A **subscription** is a group that Throne downloads from a URL and can update later.

### Paste a subscription link {#paste-subscription}

1. Copy the subscription URL. It starts with `https://`.
2. In the main window, press `Ctrl+V`, or click `Program` → `Add profile from clipboard`.
3. Throne asks "How to update?". Choose `Create new subscription group` in the list and click `OK`.

Throne creates a group named after the host name in the URL and downloads its profiles right away. If your provider sends details about your plan, a card above the profile list shows the traffic you used and the expiry date (since 1.3.2). See [Provider information](@/guides/subscriptions.md#provider-info).

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

To delete the profiles that failed, click `Groups` → `Clean up` → `Remove Unavailable` (`Ctrl+Shift+R`). Before 1.4.0, `Remove Unavailable` was directly in the `Groups` menu. In a subscription group, the next update adds them again if the provider still lists them.

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

The bottom left corner of the window shows the running profile as `[group] profile`. A moment later, the country and city of your exit IP address appear below it, unless `Look up exit country` is off (see [IP and country test](@/guides/testing.md#ip-test)).

Click this text to test the running profile. Throne shows `Test Result: <n> ms` if the connection works, or `Test Result: Unavailable` if it does not. If the test fails, try another profile or see [Troubleshooting](@/help/troubleshooting.md).

### Stop and quit {#stop-and-quit}

- To disconnect, click the same button again (its tooltip now says `Stop`), or press `Ctrl+S`.
- Closing the window only hides Throne in the system tray. To quit, click `Program` → `Exit`, or use `Exit` in the tray menu.
- With `Program` → `Remember last profile` on, Throne starts your last profile again when it starts, and turns `System Proxy` and `Tun Mode` back on if they were on. `Program` → `Start with system` starts Throne when you log in.

{% alert_warning() %}
Always quit Throne with `Exit`. If Throne is killed while a profile runs with `System Proxy` on, your system keeps using a proxy that no longer runs, and websites stop loading. See the [FAQ](@/help/faq.md#force-quit).
{% end %}

## Simple and Advanced mode {#interface-mode}

Since 1.4.0, the Throne window has two interface modes. **Simple** mode shows the options that most people need and hides the others. **Advanced** mode shows every option. A new installation starts in Simple mode. When you update from an older version, Throne keeps the full interface, which is Advanced mode.

Simple mode only hides options. Hidden settings keep their values and still apply, so switching the mode does not change your profiles or settings.

To switch the mode:

1. Open `Settings` → `Basic Settings` → `Style`.
2. Set `Interface` to `Simple` or `Advanced`.
3. Click `OK`.

The main window and the tray menu change at once. Settings windows show the new mode the next time you open them.

To find a setting by name, press `Ctrl+K` and type a few letters of its name. In Simple mode, this search also finds the hidden settings and lists them under "Settings in Advanced mode". When you choose one, Throne switches to Advanced mode and opens the setting. See [Command palette](@/reference/shortcuts.md#command-palette).

### What Simple mode hides {#simple-mode-hidden}

These menu items are hidden in Simple mode:

| Menu | Hidden items |
|---|---|
| `Settings` | `Preset Settings`, `Integration Settings`, `Open Config Folder` |
| `Groups` | `Resolve out IP for group`, `Resolve Domain for group` |
| `Tools` | `Open Web dashboard`, `OTP Manager`, `IP Scanner` |
| Menu of the profile list | `Share` → `Export config`, `Share` → `Copy links of selected (Deep Links)`, `Resolve Selected Out IP`, `Resolve Selected Domain`, `Reset Traffic` |
| Tray menu | `OTP Codes` |

The `Runtime Stats` tab at the bottom of the main window is hidden too.

In the settings windows, Simple mode hides these options:

- `Basic Settings`: the `Logging` and `Core` tabs. On `Common`, all options except `Listen Port`, `Latency Test URL` and `Look up exit country`. On `Subscription`, all options except `Clear servers before updating subscription` and `Subscription auto update`. On `Style`, the log font, `Connection statistics` and the custom icons. On `Miscellaneous`, all options except `Use proxy` and `Allow updating to beta versions`. On `Security`, all options except `Kill Switch`.
- `Routing Settings`: `Default Domain Strategy`, `Resolve Domain Strategy` and `Remote Rule-set Mirror`, the WARP config fields and `Registration Domains…`, and all DNS options except `Remote DNS`, `Direct DNS` and `Default DNS server`.
- `Tun Settings`: `MTU`, `Auto Redirect`, `L3 Bridge Bypass`, `Tun Address` and `Private Range Bypass`.
- The group editor: `Front Proxy`, `Landing Proxy` and the `Advanced` button.
- The profile editor: the `Advanced Settings` button, the TLS fragment and TLS tricks options, the `Custom` choice of `Multiplex`, the Xray `Finalmask`, and the advanced XHTTP and XDrive groups. For a new profile, the `Type` list leaves out `Direct`, `Chain Proxy`, `Extra Core` and the custom types.
- The routing profile editor: the `Advanced` tab with the rule list, the `DNS` tab and the `Endpoints` tab, unless the profile already uses them.

A few switches stay in view while they are on, so that you can turn them off: `Random port`, `Disable Mixed Inbound`, `Enable Custom Icons` and `Use Custom DNS Object`.

Simple mode also moves some tabs into others, so a tab that these docs name can be a section of another tab:

- `Basic Settings`: the `Subscription` and `Security` tabs and the `Network Settings` group of `Miscellaneous` are sections at the bottom of the `Common` tab. The window has the tabs `Common`, `Style`, `Backup and Restore` and `Diagnostics`.
- `Routing Settings`: the `Warp` tab and the `Simple DNS Settings` group of the `DNS` tab are sections of the `Common` tab. The window has the tabs `Common` and `Route`. While `Use Custom DNS Object` is on, the `DNS` tab stays.

## Next steps {#next-steps}

- [Subscriptions & Groups](@/guides/subscriptions.md): automatic updates, and the User-Agent and HWID settings that some providers need.
- [Routing](@/guides/routing.md): your own rules, for example to send only a few websites through the proxy.
- [Testing & Auto Selector](@/guides/testing.md): speed tests, and automatic switching to a working server.
- [TUN Mode](@/guides/tun_mode.md): TUN settings and side effects.
- [DNS](@/guides/dns.md): DNS servers and leak tests.
- [Troubleshooting](@/help/troubleshooting.md) and [FAQ](@/help/faq.md): help when something does not work.
