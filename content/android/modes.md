+++
title = "VPN & Proxy Modes"
description = "Choose between VPN and Proxy only mode, pick which apps use Throne, share the proxy with other devices, and adjust the TUN and inbound settings."
weight = 30
toc = true
+++

Throne for Android has two service modes. `VPN` sends the traffic of your apps through Throne. `Proxy only` runs a local proxy that only the apps you configure will use. This page explains both modes, per-app proxy, sharing the proxy with other devices, and the TUN and inbound settings.

## Choose a service mode {#service-mode}

Set the mode in `Settings` → `General` → `Service mode`.

| Mode | What it does | Use it when |
| --- | --- | --- |
| `VPN` (default) | Android creates a VPN. Throne receives the traffic of all apps, or only of the apps you choose, through a virtual network interface (TUN). | You want every app to use Throne. This is the normal choice. |
| `Proxy only` | Throne opens only a local proxy (SOCKS5 and HTTP) on `127.0.0.1`, port `2080` by default. No VPN is created. | Another VPN app must stay connected, you only need Throne in apps that have proxy settings, or your device cannot grant VPN access. |

Changing the mode stops a running connection. Tap the connect button again to start in the new mode.

{% alert_info() %}
If Throne is the always-on VPN in the Android settings, Android starts it in VPN mode. On Android 10 and newer, Throne then switches `Service mode` back to `VPN`. See [Always-on VPN](@/android/permissions.md#always-on).
{% end %}

## VPN mode {#vpn-mode}

In VPN mode, Android sends the network traffic of your apps to Throne. Throne then sends each connection through a proxy, sends it directly, or blocks it, as your routing profile says.

- The first time you connect, Android asks you to allow the VPN. See [VPN permission](@/android/permissions.md#vpn-permission).
- Android runs only one VPN at a time. When Throne connects in VPN mode, the VPN of any other app disconnects.
- Devices connected to your phone's hotspot do not use the VPN, because Android does not send their traffic through VPN apps. To give them the proxy, use [LAN sharing](#lan-sharing).
- To keep some apps out of the VPN, or to send only some apps through it, use [per-app proxy](#per-app-proxy).

### HTTP proxy of the VPN {#http-proxy}

On Android 10 and later, Throne also sets its local proxy (`127.0.0.1` and the `Proxy port`) as the HTTP proxy of the VPN network. Apps that follow the system proxy settings, such as most browsers, then send their web traffic to this proxy directly. This traffic still follows your routing profile.

- To exclude domains from this proxy, add them to `Settings` → `Inbound` → `HTTP proxy bypass list`. Write one entry per line, for example `*example.com`. Lines that start with `#` are comments. Apps connect to these domains without the proxy.
- `Disable mixed inbound` removes this HTTP proxy.

## Proxy only mode {#proxy-only}

In `Proxy only` mode, Throne runs a local proxy and nothing else. Android does not ask for VPN permission, and no VPN key icon appears in the status bar. Only apps that you point at the proxy use Throne. The TUN settings and per-app proxy have no effect in this mode.

1. Open `Settings` → `General` → `Service mode` and choose `Proxy only`.
2. Go back to the profile list and tap the connect button.
3. In the app that should use Throne, set a SOCKS5 or HTTP proxy with server `127.0.0.1` and port `2080` (or the `Proxy port` you set).
4. If `Enable authorization` is on, also enter the username and password.

The local proxy accepts SOCKS5 and HTTP on the same port.

In this mode, Throne also sends its own requests through the local proxy, as if `Settings` → `Subscriptions` → `Use proxy` were on. Subscription updates and WARP registration therefore need a running profile. Without one, they fail with "Request with proxy but no profile started."

`Disable mixed inbound` has no effect in `Proxy only` mode, because the local proxy is the only way into Throne.

## Per-app proxy {#per-app-proxy}

Per-app proxy decides which apps use the VPN. It works only in VPN mode.

Open `Settings` → `TUN / VPN` → `Apps VPN mode`. The app list opens. Choose a mode at the top of the list:

| Mode | Effect |
| --- | --- |
| `Off` | Per-app proxy is off and all apps use the VPN. Choosing it closes the list. |
| `Proxy` | Only the selected apps use the VPN. All other apps connect directly. |
| `Bypass` | The selected apps skip the VPN and connect directly. All other apps use the VPN. |

Opening the list turns per-app proxy on, with `Bypass` preselected the first time. To turn it off, open the list again and choose `Off`. If no app is selected, all apps use the VPN in both modes.

To select apps:

1. Tap an app to select it. Tap it again to clear it.
2. Use `Search…` to find an app by name, package name or user ID.
3. Turn off `Show system apps` to hide system apps. They are shown by default.

Each row shows the app name, the package name and the user ID in parentheses. Apps that share a user ID are selected together. Selected apps are listed first when you open the list. Selected packages that are not installed stay in the list and are marked "(not installed)".

`Auto select proxy apps` selects apps from a built-in list of about 390 apps that often need a proxy, such as Google apps, YouTube, Facebook, Instagram and Netflix. It replaces the selection of the installed apps. Packages that you added by name, or that are not installed, stay selected. In `Proxy` mode it selects the apps on that list. In `Bypass` mode it selects all other apps. In both cases, the apps on that list use the VPN and other apps do not. Apps with user ID 1000 (the Android system) count as apps on the list. Throne asks "Auto select proxy apps?" first. Tap `Replace` to continue.

The toolbar and the ⋮ menu of the list have these actions:

| Action | What it does |
| --- | --- |
| `Invert selections` | Selects every app that is not selected and clears the others. |
| `Clear selections` | Clears the whole selection. |
| `Add package name…` | Adds apps by package name, for example apps that the list cannot show. Separate several names with spaces, commas or new lines. |
| `Export to clipboard` | Copies the mode and the selected package names. |
| `Import from clipboard` | Replaces the mode and the selection with the copied list. |

The clipboard format is plain text. The first line is `true` for `Bypass` or `false` for `Proxy`. Each following line is one package name:

```text
false
com.google.android.youtube
org.telegram.messenger
```

When you import, upper and lower case do not matter in the first line. Any first line other than `true` selects `Proxy`.

If Throne is connected, the new selection applies after the connection reloads. Stop and start the connection, or tap `Apply` when Throne shows "Reload proxy service to apply changes".

If the list stays empty, see [Installed apps](@/android/permissions.md#installed-apps).

To send an app to a specific outbound while it stays in the VPN, use a routing rule with the `Apps` condition instead. The desktop app has no app list. On the desktop, you use routing rules by process name. See [Routing](@/guides/routing.md#advanced-rules).

## LAN sharing {#lan-sharing}

LAN sharing lets other devices on the same network, such as a laptop or a TV, use Throne on your phone as a proxy. It works in both service modes, and it also works for devices connected to your phone's hotspot.

1. Open `Settings` → `Inbound` and turn on `Allow connections from the LAN`. Throne then listens on all network interfaces instead of only on `127.0.0.1`.
2. Turn on `Enable authorization` and set a `Username` and a `Password`.
3. Note the `Proxy port`. It is `2080` by default.
4. If Throne is connected, tap `Apply` when Throne shows "Reload proxy service to apply changes", or reconnect.
5. Find the IP address of the phone. It is shown in the Android Wi-Fi settings, in the details of the connected network. For devices on your hotspot, use the router (gateway) address that the other device shows for its connection.
6. On the other device, set a SOCKS5 or HTTP proxy with the phone's IP address, the port, the username and the password.

{% alert_warning() %}
Without authorization, any device on the same network can use your proxy.
{% end %}

When you restore the `Settings` part of a backup that allows LAN connections, Throne turns `Allow connections from the LAN` off, unless it was already on, and shows a warning.

On the desktop, the same feature is called `Allow other devices to connect`. See [System Proxy, TUN & LAN sharing](@/guides/proxy_modes.md#lan-sharing).

## TUN / VPN settings {#tun-settings}

These settings are in `Settings` → `TUN / VPN`. They apply only in VPN mode. If Throne is connected when you change a setting, tap `Apply` when Throne shows "Reload proxy service to apply changes".

| Setting | Default | What it does |
| --- | --- | --- |
| `TUN implementation` | `gVisor` | The network stack that handles the traffic of the VPN interface: `gVisor`, `System` or `Mixed`. If some apps do not work, try another one. |
| `MTU` | `9000` | The largest packet size of the VPN interface. Choose `1500` or `9000` from the list, or long-press the setting to enter any value from 1000 to 10000. |
| `Tun IPv6` | Off | Gives the VPN interface an IPv6 address and routes IPv6 through it. When it is off, IPv6 connections fail at once while Throne runs, so apps use IPv4. Turn it on only if your server supports IPv6. |
| `Tun routing` | Off | Keeps the IP ranges that your routing profile sends `direct` outside the VPN interface, so this traffic does not pass through Throne. |
| `Bypass private ranges` | On | Keeps the `Private ranges` outside the VPN interface, so devices on your local network are reached directly. |
| `Private ranges` | 8 ranges | The ranges that stay outside. One address or CIDR per line. Available while `Bypass private ranges` is on. |
| `Restore default ranges` | — | Puts back the default list of private ranges. |
| `Apps VPN mode` | Off | Per-app proxy. See [Per-app proxy](#per-app-proxy). |
| `IPv4 CIDR` | `172.19.0.1/24` | The IPv4 address of the VPN interface. |
| `IPv6 CIDR` | `fdfe:dcba:9876::1/96` | The IPv6 address of the VPN interface, used when `Tun IPv6` is on. |
| `Restore default addresses` | — | Puts back both default addresses. |

The default private ranges are `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `224.0.0.0/4`, `fc00::/7`, `fe80::/10` and `ff00::/8`. If a routing rule sends addresses in a private range to an outbound other than `direct`, or rejects them, Throne keeps that whole private range inside the VPN interface so that the rule works.

Strict route is always on in the Android app and has no setting. On the desktop it is a setting. See [TUN Mode](@/guides/tun_mode.md#settings).

### MTU {#mtu}

The Android default MTU is `9000`. The desktop default is `1500`. Keep the default unless you have problems. If some apps or websites fail while others work, set `MTU` to `1500` and reconnect. When you restore the settings of a desktop backup, the desktop MTU comes with them. It is `1500` unless you changed it there.

## Inbound settings {#inbound-settings}

`Settings` → `Inbound` controls the local proxy of Throne, called the mixed inbound. It accepts SOCKS5 and HTTP on one port.

| Setting | Default | What it does |
| --- | --- | --- |
| `Disable mixed inbound` | Off | In VPN mode, Throne does not open the local proxy. This also removes the [HTTP proxy of the VPN](#http-proxy) and LAN sharing. It has no effect in `Proxy only` mode. |
| `Proxy port` | `2080` | The port of the local proxy. In a work profile or another Android user, the default is 2080 plus the number of that user. |
| `Random port` | Off | Picks a free port each time the connection starts and saves it as `Proxy port`. |
| `Allow connections from the LAN` | Off | Listens on all network interfaces instead of `127.0.0.1`. See [LAN sharing](#lan-sharing). |
| `HTTP proxy bypass list` | Empty | Domains that do not use the HTTP proxy of the VPN. One entry per line. |
| `Enable authorization` | Off | Clients must send the `Username` and `Password`. This applies to every client, including apps on this phone that use the HTTP proxy of the VPN. |
| `Custom inbound` | `{"inbounds": []}` | Extra sing-box inbounds as JSON. Throne adds the `inbounds` array to its configuration unchanged. |

When `Disable mixed inbound` is on, all other settings on this screen except `Custom inbound` are disabled.

The desktop has similar settings. See [Inbound settings](@/guides/proxy_modes.md#inbound-settings).
