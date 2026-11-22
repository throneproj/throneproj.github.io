+++
title = "Tun Mode"
description = "Turn on Tun mode, give Throne the rights it needs on Windows, Linux and macOS, change the Tun Settings, and fix common Tun mode problems."
weight = 30
toc = true
+++

In Tun mode, Throne creates a virtual network adapter and sends the traffic of the whole computer through it, also DNS queries and apps that ignore proxy settings. To choose between Tun mode and the system proxy, see [Which mode to use](@/guides/proxy_modes.md#which-mode).

## Turn on Tun mode {#enable}

1. Tick `Tun mode` on the main window or in the tray menu.
2. The first time, Throne asks for the rights that Tun mode needs. Accept the request, see [Privileges](#privileges).
3. Start a profile, if none is running.

Turning Tun mode on or off restarts the running profile. Tun mode works only while a profile runs; to block traffic while none runs, turn on the [kill switch](@/advanced/kill_switch.md).

## Privileges {#privileges}

Tun mode needs system rights to create the adapter and change the routes of the computer. If you give the rights yourself, for example with the Linux capabilities below, `Settings` → `Basic Settings` → `Security` → `Privileges` → `Disable privilege request` stops Throne from asking.

### Windows {#privileges-windows}

- Only the core, `ThroneCore`, needs administrator rights; Throne itself keeps running as a standard user. The first time you tick `Tun mode`, click `Grant privileges` and accept the Windows prompt. The core restarts with the rights; then tick `Tun mode` again. If Windows Firewall asks about `ThroneCore`, allow it.
- The rights stay granted, so Throne does not ask at each start. After an update, it may ask once more.
- If the grant fails, or the core still lacks the rights after it, Throne offers `Restart as administrator` instead. The `Logs` tab shows why.
- On an account that cannot grant rights, such as a standard account, Throne asks to run as administrator instead. Click `Yes`: Throne restarts as administrator with Tun mode on, and from then on asks for administrator rights each time it starts. To stop this, tick `Settings` → `Basic Settings` → `Security` → `Privileges` → `Always start as standard user`. While Throne runs as administrator this way, `Program` → `Start with system` starts it as administrator at sign-in, without a prompt.

See also [FAQ](@/help/faq.md#tun-admin).

### Linux {#privileges-linux}

- Only the core, `ThroneCore`, needs root rights. The first time you tick `Tun mode`, click `Yes` and enter your password: Throne uses `pkexec` (part of polkit) to make root the owner of `ThroneCore` and set its SUID bit. Then tick `Tun mode` again.
- Never start Throne itself with `sudo`.
- Instead of the SUID bit, you can give the core these five capabilities. Throne accepts the core only with all five:

```bash
sudo setcap cap_net_admin,cap_net_raw,cap_net_bind_service,cap_sys_ptrace,cap_dac_read_search+ep /path/to/Throne/ThroneCore
```

Some third-party packages cannot change the core themselves and show the package's own instructions instead. See also [FAQ](@/help/faq.md#linux-suid).

### macOS {#privileges-macos}

- Move `Throne.app` to `/Applications` before you turn on Tun mode. Setting the rights can fail while the app is in `Downloads`.
- The first time you tick `Tun mode`, click `Yes`. Terminal opens with a `sudo` command for the core. Enter your password there, then tick `Tun mode` again.
- `sudo` needs an administrator account. On a standard account, use the system proxy instead.

## Tun Settings {#settings}

Open `Settings` → `Tun Settings`. If Tun mode is on, turn it off and on again to apply changes.

| Setting | Default | What it does |
| --- | --- | --- |
| `MTU` | `1500` | The largest packet size of the adapter, from 1000 to 10000. With `Enable IPv6`, use at least 1280, or IPv6 may fail. |
| `Enable IPv6` | off | Sends IPv6 traffic through the tunnel. Turn it on only if your server supports IPv6. |
| `Strict route` | on for Windows 10 and later, off elsewhere | On Windows, blocks DNS queries that go around the tunnel; see [Windows DNS Leak Protection](@/advanced/windows_tun_mode.md#strict-route). |
| `Enable Tun routing` | off | Keeps IP ranges and `geoip-*` rule-sets that your routing sends `direct` out of the tunnel. Large rule-sets can cause very high CPU use on Windows. |
| `Auto redirect` | on | Linux only. Improves routing and speed with nftables. While it is on, this computer cannot be a network gateway for other devices. |
| `L3 bridge bypass` | off | Sends direct UDP and ICMP traffic straight out of the network adapter: faster, and keeps NAT working for games and P2P. Not on Windows on ARM. |
| `IPv4 CIDR`, `IPv6 CIDR` | `172.19.0.1/24`, `fdfe:dcba:9876::1/96` | The addresses of the adapter. Change them only if they clash with a network you use. |
| `Private Range Bypass` | on | Address ranges that go straight to your network adapter instead of through the tunnel, one per line. |
| `Restart core` | – | Stops the running profile and restarts the core, for when Tun mode does not start. |

The default `Private Range Bypass` list is `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `224.0.0.0/4`, `fc00::/7`, `fe80::/10` and `ff00::/8`.

## Side effects {#side-effects}

### Local network and virtual machines {#side-effects-vms}

With `Private Range Bypass` on, printers, network drives, your router and other local devices are reached directly, outside the tunnel, unless a routing rule sends their range to the proxy or blocks it. Docker, WSL and virtual machines bypass the tunnel the same way; if their network uses a range that is not in the list, add it. See [Recipes](@/guides/recipes.md#docker-wsl-vms).

### Mobile hotspot on Windows {#side-effects-hotspot}

If Windows Mobile Hotspot or Internet Connection Sharing shares your normal network adapter, Tun mode fails, and Throne warns "IPv4 forwarding breaks Tun mode". In the Mobile hotspot settings, set "Share my internet connection from" to `throne-tun`, or turn the hotspot off while you use Tun mode. See [Recipes](@/guides/recipes.md#hotspot).

### Other VPNs {#side-effects-vpn}

Two VPNs on one computer compete for routes and DNS. Turn off other VPN apps while Tun mode is on. To reach a company network at the same time, see [Recipes](@/guides/recipes.md#corporate-vpn).

### DNS {#side-effects-dns}

All DNS queries reach Throne, but a leak test can still show your internet provider for sites that go direct; see [DNS](@/guides/dns.md#leak-tests).

On macOS, while Tun mode runs, Throne sets the DNS server of your network services, such as `Wi-Fi`, to `127.0.0.53`, where the core answers with Throne's DNS settings. When Tun mode stops, it puts your previous servers back.

## Troubleshooting {#troubleshooting}

Open the `Logs` tab and look for errors when Tun mode starts. For general steps, see [Troubleshooting](@/help/troubleshooting.md#tun).

### Windows {#troubleshooting-windows}

**Connected, but nothing loads.** Windows Firewall may block `ThroneCore`. Allow it in `Windows Security` → `Firewall & network protection` → `Allow an app through firewall`, for private and public networks.

**Antivirus.** Some antivirus programs, such as Avast and ESET, block the adapter or the core. Add an exception for the Throne folder.

**"Strict routing unavailable".** Untick `Strict route` in `Tun Settings` and start the profile again. Without it, DNS queries can leak; see [Windows DNS Leak Protection](@/advanced/windows_tun_mode.md).

**"Tun device misbehaving".** Click `Reset` to restart the core, then start the profile again.

**"Leftover Tun adapter".** After a crash or force-quit, Windows can keep the adapter of the old session. Click `Start again`. If it keeps failing, restart Windows.

**Tun mode takes very long to start.** Throne clears the Windows DNS cache when Tun mode starts, which is very slow with a huge HOSTS file, such as an ad-blocking list. Make it smaller.

### Linux {#troubleshooting-linux}

**"Please install "pkexec" first."** Install polkit with your package manager, or set the capabilities shown in [Linux privileges](#privileges-linux).

**"file exists" when Tun mode starts.** Turn off `Auto redirect` in `Tun Settings`.

**No DNS with systemd-resolved.** If `DNSOverTLS` is on for all interfaces in `/etc/systemd/resolved.conf`, Tun mode breaks. Turn it off there, or for the Throne adapter while it exists:

```bash
sudo resolvectl dnsovertls throne-tun no
```

**DNS stays broken after Tun mode stops, with a local DNS proxy.** A local DNS proxy on `127.0.0.1`, such as `dnscrypt-proxy`, `unbound` or `dnsmasq`, can have its connection to an upstream server by IP caught in the tunnel; restarting the proxy brings DNS back. To prevent this, add the upstream address to `Private Range Bypass` in `Tun Settings`, for example `1.1.1.1/32` for `https://1.1.1.1/dns-query`. Then turn Tun mode off and on, and restart the proxy.

**Packages from AUR, Nix or other repositories.** They are maintained by the community. If Tun mode fails there, try the official build; see [FAQ](@/help/faq.md#third-party-packages).

### macOS {#troubleshooting-macos}

**An error about "the system DNS" when Tun mode starts.** The core could not point the system DNS to itself (see [DNS](#side-effects-dns)); the rest of the message says why. Click `Restart core` in `Tun Settings`, then start the profile again.

**No DNS after Throne was force-quit or crashed.** If a network service still uses the DNS server `127.0.0.53`, start Throne once: its core puts back your previous servers. Or remove `127.0.0.53` from that service in the macOS network settings.

## On Android {#android}

In `VPN` mode, Throne for Android works like Tun mode. Its settings are in `Settings` → `TUN / VPN`; see [VPN & Proxy Modes](@/android/modes.md#tun-settings).
