+++
title = "Troubleshooting"
description = "Fixes for Tun mode, DNS, subscription, system proxy, performance and startup problems in Throne desktop."
weight = 20
toc = true
+++

Find your problem and go through the checks in order. To find a setting named here, press `Ctrl+K` and type its name. For Android, see [Android Troubleshooting](@/android/troubleshooting.md). If nothing helps, [report a bug](@/help/bug_reports.md).

## First checks {#first-checks}

1. Update Throne with `Program` → `Check for updates`, or from the [downloads](@/downloads.md) page if that item is greyed out.
2. Read the `Logs` tab at the bottom of the main window.
3. Test the profile with `Test` → `URL test` (`Ctrl+Shift+S`). If the test fails, fix the server or the profile first.
4. If a profile works with `System proxy` but not with `Tun mode`, the problem is in the Tun setup.
5. If a site goes through the wrong route, look up which rule it hits with `Routing` → `Route lookup`; see [Test a route](@/guides/routing.md#route-lookup).

## Tun mode {#tun}

### Tun mode is on, but nothing loads {#tun-no-traffic}

1. Close other VPN apps. They can take over the routes.
2. **Windows:** allow `ThroneCore.exe` in Windows Firewall. If you denied it when Windows asked, Windows keeps blocking it without asking again ([#1433](https://github.com/throneproj/Throne/issues/1433)).
3. **Windows:** antivirus network protection, for example Avast or ESET, can block the Tun adapter without any message ([#1687](https://github.com/throneproj/Throne/issues/1687), [#1357](https://github.com/throneproj/Throne/issues/1357)). Add the Throne folder as an exception.
4. **Windows:** turn off `Strict route` in `Tun Settings` for a test. Without it, DNS can leak; see [Windows DNS Leak Protection](@/advanced/windows_tun_mode.md#strict-route).
5. **Linux:** turn off DNS over TLS for the whole system in systemd-resolved ([#1146](https://github.com/throneproj/Throne/issues/1146)), and keep `Auto redirect` on in `Tun Settings`.

### Tun mode does not start {#tun-start}

- **No rights:** accept Throne's request for administrator or root rights ([FAQ](@/help/faq.md#tun-admin)). On Windows, click `Grant privileges`, confirm the Windows prompt, then tick `Tun mode` again. With `Disable privilege request` on, you must give the rights yourself.
- **"The core did not get administrator rights, although they were granted"** (Windows): the log shows why. Click `Restart as administrator` to run Throne itself as administrator instead; see [Tun privileges on Windows](@/guides/tun_mode.md#privileges-windows).
- **"Strict routing unavailable"** (Windows): turn off `Strict route` in `Tun Settings` and start the profile again.
- **"Tun device misbehaving":** click `Reset` in the message, or `Restart core` in `Tun Settings`, and start the profile again. If it still fails, restart the computer.
- **The start hangs** (Windows): a very large HOSTS file can make the DNS cache flush hang ([#1906](https://github.com/throneproj/Throne/issues/1906)). Keep it small.
- **"A background Throne (PID …) owns Tun on this computer; stop it or use thronectl."** See [Throne is running in the background](#background-throne).

### Tun mode breaks other things {#tun-side-effects}

A mobile hotspot, virtual machines, Docker or a work VPN can stop working while Tun mode is on. See [Tun Mode](@/guides/tun_mode.md#side-effects) and [Recipes](@/guides/recipes.md).

## DNS {#dns}

### Sites do not open, or the log shows DNS errors {#dns-errors}

1. In `Settings` → `Routing Settings` → `DNS`, `Remote DNS` must be reachable through your proxy, and `Direct DNS` must work without it. Try one of the preset servers.
2. If your network has no IPv6, do not use `ipv6_only` in `Default Domain Strategy` or `Resolve Domain Strategy` in `Routing Settings` → `Routing` → `Domain Strategy` ([#1743](https://github.com/throneproj/Throne/issues/1743)). Leave them empty, or use `prefer_ipv4`.

### A leak test shows my ISP's DNS {#dns-leak}

This is usually expected; see the [FAQ](@/help/faq.md#dns-leak-test).

## Subscriptions {#subscriptions}

### The update fails {#sub-update-fails}

The log shows `Requesting subscription … error: …` with the reason.

- **"Request with proxy but no profile started."** With `Send Throne's own requests through the proxy` (`Basic Settings` → `General` → `Updates and Downloads`) or `System proxy` on, Throne sends its own requests through its proxy. Start a profile first, or turn both off. If `Disable mixed inbound` is on, turn `Send Throne's own requests through the proxy` off ([#1689](https://github.com/throneproj/Throne/issues/1689)).
- **The provider's site is blocked in your country:** start a working profile, turn on `Send Throne's own requests through the proxy`, and update again.
- **The server answers `403`, or sends nothing useful:** many providers answer only apps they know. Set the `User Agent` your provider expects, in `Basic Settings` → `Subscriptions` → `Requests` for all groups, or in `Groups` → `Edit group` → `Advanced` → `Request` for one. The default is `Throne/<version>`.
- **"Device fingerprint required"** or a similar message: the provider needs your [HWID](@/help/faq.md#hwid).

### The update finds no profiles {#sub-no-profiles}

The log says "No profiles found in the subscription". Check that the link is a subscription URL, not a web page or an app link: `happ://crypt` and `v2raytun://crypt` links are encrypted for those apps, and Throne cannot read them. Also try another `User Agent`.

### The group does not update {#sub-no-update}

- Profiles added with `Add profiles to this group` have no subscription URL. Paste the URL again with `Ctrl+V` and choose `Create new subscription group`.
- Automatic updates need `Basic Settings` → `Subscriptions` → `Auto Update` → `Enable`, which is off by default, and skip groups with `Skip automatic update`.

Profiles changed or disappeared after an update? See the [FAQ](@/help/faq.md#profile-after-update) and [Subscriptions & Groups](@/guides/subscriptions.md#problems).

## System proxy {#system-proxy}

### Some apps ignore the system proxy {#apps-ignore-proxy}

Terminals such as PowerShell, Windows Store apps, and Discord and Telegram calls usually ignore it ([#370](https://github.com/throneproj/Throne/issues/370), [#1631](https://github.com/throneproj/Throne/issues/1631)). Use `Tun mode` for them; see [Which mode to use](@/guides/proxy_modes.md#which-mode).

### The system proxy is not set {#proxy-not-set}

1. Start a profile. Throne sets the system proxy only while a profile runs.
2. **"Cannot set system proxy when mixed inbound is disabled."** Turn off `Disable mixed inbound` in `Basic Settings` → `Connection` → `Local Proxy`.
3. **Linux:** Throne sets the system proxy only on GNOME and KDE. On other desktops, enter the `Mixed: …` address from the status bar in your system settings, or use Tun mode. Do not run Throne as root ([#864](https://github.com/throneproj/Throne/issues/864)).

### No internet after Throne was closed {#no-internet-after-exit}

If Throne was force-closed while `System proxy` was on, the system proxy still points at Throne. See the [FAQ](@/help/faq.md#force-quit).

## Performance and crashes {#performance}

### High CPU or memory use {#high-cpu}

1. Keep fewer than about 10,000 profiles in total. After a URL test, remove dead ones with `Groups` → `Clean up` → `Remove unavailable`.
2. Torrent clients with Multiplex on can use a lot of CPU ([#1090](https://github.com/throneproj/Throne/issues/1090)). Multiplex is off by default; if you turned it on, turn it off in the profile, or turn off `Default on` (sing-box) and `Multiplex by default` (Xray) in `Settings` → `Preset Settings` → `Multiplex`.
3. Untick `Basic Settings` → `Core` → `Statistics` → `Enable connection statistics`. The `Connections` tab then stays empty.
4. **Windows:** `Enable Tun routing` with large rule-sets can cause very high CPU use. Turn it off in `Tun Settings`.

### Throne or the core crashes {#crashes}

- **"Core exits too frequently, stop automatic restart this profile."** The core keeps crashing, so Throne stopped restarting it with your profile.
- **"Throne did not shut down cleanly last time"** at the next start: Throne crashed. The log of that session is kept as `logs/crashed-<date>-<time>.log` in the config folder; on Windows, a crash report is also saved in the `crashes` folder.
- To rule out your configuration, quit Throne, rename the `config` folder and start Throne again; see [Command Line, Files & Logs](@/reference/files.md#reset).
- Report the crash with these files: [Reporting a Bug](@/help/bug_reports.md#logs).

## Startup and desktop problems {#startup}

### Throne does not start {#no-start}

- **"Incompatible processor. This Qt build requires the following features: sse4.2 popcnt"**: use `windowslegacy64.zip` on Windows, or a `-system-qt` package on Linux ([FAQ](@/help/faq.md#old-systems)).
- **Linux: `Could not load the Qt platform plugin "xcb"`**: with a Throne that uses the Qt of your system, install `libxcb-cursor0` (Debian, Ubuntu) or `xcb-util-cursor` (Fedora, RHEL) ([#1096](https://github.com/throneproj/Throne/issues/1096)). If the ZIP or a normal package shows it, use a `-system-qt` package, which also helps with other Qt errors.
- **macOS: "Throne is damaged and can't be opened":** Throne is not signed with an Apple certificate. Move `Throne.app` to `/Applications`, remove the quarantine flag in Terminal, and open Throne again:

  ```bash
  xattr -d com.apple.quarantine /Applications/Throne.app
  ```

On Linux, start Throne from a terminal to see the error: `/opt/Throne/Throne -appdata` for the packages, or `./Throne` in a ZIP copy. Do not use `sudo`; only the core needs root rights ([FAQ](@/help/faq.md#linux-suid)).

### No tray icon on GNOME {#gnome-tray}

Install and enable an AppIndicator extension. If the window is hidden, start Throne again to show it, or turn on `Basic Settings` → `General` → `Window` → `Disable tray` so that closing the window quits Throne.

### Throne does not reconnect after a restart {#reconnect}

Turn on `Program` → `Remember last profile`. At the next start, Throne starts the profile that was running when you quit, with `System proxy` and `Tun mode` as they were. `Program` → `Start with system` starts Throne when you log in; on Windows, it starts Throne as administrator only after the `Restart as administrator` fallback ([FAQ](@/help/faq.md#tun-admin)).

### `throne://` links do nothing {#deeplinks}

On Windows and Linux, ZIP copies do not register `throne://` links by default. Turn on `Basic Settings` → `General` → `Links and Files` → `Register throne:// links at startup`, or click `Install` next to it. More checks: [Deep Links](@/advanced/deeplinks.md#troubleshooting).

### Throne is running in the background {#background-throne}

A [headless Throne](@/headless/_index.md), for example a systemd service, can run on the same computer as the Throne window:

- **"Throne is running in the background (PID …). Stop the service or use thronectl."** and the window does not open: the headless Throne uses the same data folder. Stop it (for example `systemctl --user stop throne`) and start Throne again, or manage it with [thronectl](@/advanced/api.md).
- **"A background Throne (PID …) is running on this computer"**: a headless Throne with another data folder runs. The window works, but without Tun mode.
- **"A background Throne (PID …) owns Tun on this computer; stop it or use thronectl."** The window cannot use Tun mode while any headless Throne runs, even one without Tun mode. Stop the headless Throne.
- **"Update is unavailable while a background Throne (PID …) runs from this installation; stop it first."** Stop it, update, and start it again.
- **"Another Throne instance (PID …) is using this data directory"**: another Throne holds the data folder but does not answer. Quit it, or end that process, and start Throne again.
