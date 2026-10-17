+++
title = "Kill Switch"
description = "Block all traffic that does not go through Throne, also while no profile runs, and get your connection back if the kill switch locks you out."
weight = 65
toc = true
+++

Since 1.4.0, Throne has a kill switch. While it is on, your computer can send traffic only through Throne: through TUN mode, through the local proxy port, or as Throne's own connections. Everything else is blocked, also while no profile runs. If the proxy stops or the connection drops, apps cannot fall back to your normal connection.

{% alert_warning() %}
The kill switch is experimental in 1.4.0. Read [If it locks you out](#recovery) before you turn it on.
{% end %}

## What it does {#what-it-does}

The kill switch works while Throne runs, whether a profile runs or not:

| Situation | What gets through |
| --- | --- |
| A profile runs in TUN mode | Everything, because all traffic goes through the TUN adapter. |
| A profile runs with the system proxy only | Apps that use the proxy. Apps that ignore it are blocked. |
| No profile runs | Almost nothing: only the local network and the exceptions listed below. |

Throne itself is not affected: its core can always reach your servers and send traffic that your rules send `direct`. For the full list, see [What is always allowed](#allowed).

The kill switch ends when Throne exits. It also ends when Throne crashes, so a crash does not cut you off, but it also does not protect you after that. Use TUN mode together with the kill switch: then all apps keep working while a profile runs.

## Turn it on {#enable}

1. Open `Settings` → `Basic Settings` → `Security`.
2. Tick `Kill Switch`.
3. Click `OK`.

The kill switch needs the same rights as TUN mode; see [Requirements](#requirements). On Linux and macOS, turning it on restarts Throne's core, and a running profile with it. While the kill switch starts, Throne waits with starting a profile.

To check that it works:

- The log shows "[Kill switch] On: only traffic through Throne can leave this device."
- The window title and the tray tooltip show `[Kill switch]`.
- The Start button has a small lock. Its tooltip says what the kill switch does now:

| Lock | Tooltip | Meaning |
| --- | --- | --- |
| Grey | "Kill switch: starting…" | The kill switch is starting. |
| Green | "Kill switch: on — traffic only flows through Throne's Tun" | A profile runs in TUN mode. |
| Amber | "Kill switch: Tun is not running, so most traffic is blocked" | No profile runs, or TUN mode is off. |
| Red | "Kill switch is not active" or "Kill switch is blocking traffic" | The kill switch has a problem; see [When it cannot work](#failures). |

The setting is saved. The kill switch starts again each time Throne starts.

## What is always allowed {#allowed}

- **Throne's core** (`ThroneCore`): connections to your servers, traffic that your rules send `direct`, URL tests and the DNS queries of Throne's own DNS servers. The programs of [Extra Core](@/advanced/chains.md#extra-core) profiles are allowed too.
- **The TUN adapter.** Everything that goes into Throne's TUN adapter.
- **Loopback** (`127.0.0.1`, `::1`). Apps reach the local proxy port this way.
- **The local network**, unless `Private Range Bypass` is turned off in `Settings` → `Tun Settings`. These ranges count as local: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `224.0.0.0/4`, `255.255.255.255`, `fc00::/7`, `fe80::/10` and `ff00::/8`. Your own changes to the `Private Range Bypass` list do not change this list.
- **Network basics:** DHCP and DHCPv6, IPv6 neighbor and router discovery, and multicast group messages (IGMP and MLD). Your computer keeps its network address.
- **The Throne API.** When the [Throne API](@/advanced/api.md) listens on a network address, its replies to clients get through.

Even with the local network allowed, DNS queries (ports 53 and 853) of other programs to local addresses are blocked. A DNS server in your router would send them on outside the tunnel. On Linux, Throne warns when `/etc/resolv.conf` names such a server: "the system DNS server … is on the local network and the kill switch blocks DNS to it". In TUN mode, use systemd-resolved, which Throne points at the tunnel, or a DNS server outside your local network.

Everything else is blocked, for example:

- Throne's own requests, such as subscription updates, update checks and WARP registration. They work only in TUN mode, or while a profile runs with `Settings` → `Basic Settings` → `Miscellaneous` → `Use proxy` or `System Proxy` on.
- Traffic that this computer forwards for other devices, containers or virtual machines, unless it goes through the TUN adapter or stays in the local network.
- Traffic of other VPN apps.

On macOS, connections that are open when the kill switch starts are cut once. Apps connect again.

## How it works {#how-it-works}

Throne starts a separate guard process, `ThroneCore --guard`. It adds firewall rules, checks every 5 seconds that they are still there, and removes them when Throne stops it, when Throne exits or when Throne crashes.

- **Linux:** an nftables table named `throne-guard-…`. The kernel deletes it when the guard ends. Throne's core is recognized by its group: the core switches to the group ID 1950896719, and Extra Core programs run with this group too.
- **macOS:** a pf anchor named `com.apple/000.throne-guard.…`. The guard turns pf on for as long as it needs it. The core is recognized by the same group ID as on Linux. If a guard ends without removing its rules, Throne removes them the next time its core starts.
- **Windows:** Windows Filtering Platform (WFP) filters named "Throne kill switch". Windows deletes them when the guard ends. `ThroneCore.exe` and the programs of Extra Core profiles are recognized by their path. When you start an Extra Core profile, Throne adds its program to the kill switch first ("[Kill switch] Allowing the extra core …").

If another program removes the rules or turns the firewall off, Throne starts the kill switch again, at most once every 30 seconds.

## Requirements {#requirements}

| System | What the kill switch needs |
| --- | --- |
| Windows | Throne runs as administrator, and the Windows service `Base Filtering Engine` runs. |
| Linux | The core runs as root through the SUID bit. This is the setup that Throne makes for TUN mode. A core that only has capabilities (`setcap`) is not enough. Linux 5.12 or newer, with nftables and conntrack labels (`CONFIG_NFT_CT` and `CONFIG_NF_CONNTRACK_LABELS`). |
| macOS | The core runs as root through the SUID bit, as for TUN mode. `/etc/pf.conf` must load the `com.apple` anchors, as it does by default. |

See [TUN mode privileges](@/guides/tun_mode.md#privileges) for how Throne sets up these rights.

## When it cannot work {#failures}

When the kill switch is on but cannot start, or stops working, Throne shows "Kill switch is not active" with the reason. The window title shows `[Kill switch: not active]`. The buttons:

- **`Restart as Administrator`** (Windows) or **`Grant Privileges`** (Linux and macOS), when rights are missing. They work as for TUN mode.
- **`Retry`**, for other problems.
- **`Disable Kill Switch`**, which turns the setting off.

While the kill switch is on but not active, nothing is blocked, and Throne does not start profiles. The log says "[Kill switch] Not starting …: the kill switch is not active." This way, you never use a profile and think you are protected when you are not. Fix the problem or turn the kill switch off.

The reason has a code. It appears in the log ("[Kill switch] Not active: …") and as `kill_switch_error` in the [Throne API](@/advanced/api.md):

| Code | Meaning |
| --- | --- |
| `privilege` | Rights are missing: Throne does not run as administrator (Windows), or the core has no root rights (Linux, macOS). |
| `unsupported` | This system cannot run the kill switch: for example Linux without nftables, older than 5.12 or without conntrack labels, a Linux core with capabilities instead of root, a pf setup without the `com.apple` anchors, or a stopped `Base Filtering Engine` service. |
| `config` | The kill switch rejected its settings, for example an invalid TUN address. |
| `tampered` | Another program removed the rules or turned the firewall off, and starting again did not help. |
| `crash`, `timeout`, `internal` | The guard process stopped, or was not ready within 15 seconds. `Retry` often helps. |
| `overridden` | Headless Throne only: it was started with `--no-kill-switch`. |

### Kill switch is blocking traffic {#blocking}

On Linux, the core must switch to the kill switch's group. Where it cannot, for example in a container or user namespace without `CAP_SETGID`, the kill switch keeps blocking, but Throne refuses to start profiles. The window title and the tray tooltip show `[Kill switch is blocking traffic]`, and the warning offers only `Disable Kill Switch`. Your computer then has no internet access until you turn the kill switch off.

## Turn it off {#disable}

Use one of these:

- Untick `Settings` → `Basic Settings` → `Security` → `Kill Switch` and click `OK`.
- Right-click the Start button → `Disable Kill Switch`. Throne asks "Turn off the kill switch? Traffic that does not go through Throne will no longer be blocked." Click `Disable Kill Switch`.
- Click `Disable Kill Switch` in a kill switch warning.

The log shows "[Kill switch] Off." Your apps can use your normal connection again.

## If it locks you out {#recovery}

The settings of Throne work without internet access. Open them and turn the kill switch off as described above.

If Throne does not respond:

1. Quit Throne, or end it in the task manager. The guard notices this and removes its rules within a few seconds.
2. If traffic is still blocked, end the guard process yourself:
   - **Windows:** in Task Manager → `Details`, end every `ThroneCore.exe`. Windows removes the filters with the process. A restart of Windows removes them too.
   - **Linux:** run `sudo pkill -f 'ThroneCore --guard'`. The kernel removes the table with the process.
   - **macOS:** run `sudo pkill -f 'ThroneCore --guard'`. If the rules stay, start Throne again: its core removes them. Or list the anchors with `sudo pfctl -a com.apple -s Anchors` and clear the one that starts with `000.throne-guard.` with `sudo pfctl -a 'com.apple/000.throne-guard.…' -F all`. A restart of macOS also removes them.
3. Start Throne and turn the kill switch off before you do anything else. It starts again with Throne until you turn it off.

## On Android {#android}

Throne for Android has no kill switch. Android has its own: set Throne as the always-on VPN and turn on "Block connections without VPN". See [Always-on VPN](@/android/permissions.md#always-on).

## Headless Throne {#headless}

[Headless Throne](@/headless/_index.md) has the same kill switch. Turn it on with `thronectl settings set kill_switch=true`. Things that differ:

- The rights depend on how you install it. On Linux, the kill switch needs a unit that runs as root or a core with the SUID bit; capabilities alone give `unsupported`. See [Privileges on Linux](@/headless/installation.md#linux-privileges).
- When the kill switch cannot work, headless Throne logs the reason, refuses profiles (`kill_switch_inactive`) and reports `kill_switch_failed`.
- If the kill switch cuts you off from the computer, start Throne once with `--no-kill-switch`. See [Recovering access](@/headless/recovery.md#recovery).
