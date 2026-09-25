+++
title = "Backup, Updates & Migration"
description = "Back up and restore Throne, move your data between desktop and Android, update the desktop app, and upgrade from old versions."
weight = 70
toc = true
+++

This page shows how to save your profiles and settings to a file, restore them, and move them between Throne desktop and Throne for Android. It also explains how to update the desktop app and what to do when you come from an old version. Make a backup before every update.

## Back up and restore {#backup-restore}

Open `Settings` → `Basic Settings` → `Backup and Restore`.

To create a backup:

1. Under `Create Backup`, tick the parts you want. All parts are ticked by default.
2. Click `Create Backup...` and choose where to save the file. The suggested name is `Throne-backup.thrbackup` in your home folder.
3. Throne confirms the file and lists the parts it included.

| Part | What it contains |
| --- | --- |
| `Profiles (groups and proxies)` | Your groups, subscriptions and profiles. |
| `Routing profiles` | Your routing profiles and their rules. |
| `Settings` | All settings, including DNS, TUN, WARP and inbound settings. |
| `OTP profiles` | The entries of the OTP Manager. |
| `Custom icons` | Your custom tray icons. |

A backup does not contain traffic history, logs or the core's cache files. It also does not remember whether `Tun Mode` or `System Proxy` was on.

{% alert_warning() %}
A backup contains your server passwords, subscription links and other secrets. Keep the file private and never attach it to a bug report.
{% end %}

To restore a backup:

1. Click `Restore from Backup...` and choose a `.thrbackup` file.
2. Throne shows when the backup was created. Tick the parts you want to restore. Parts that the file does not contain are greyed out.
3. Click `Restore`. Each selected part replaces your current data. This cannot be undone.
4. Throne restarts.

Backups from older versions of Throne restore normally. A backup from a newer version can be refused with "Unsupported backup format version"; update Throne first.

## Move between desktop and Android {#desktop-android}

Throne desktop and Throne for Android use the same backup format, so you can move your data in both directions.

From the desktop to a phone:

1. On the desktop, create a backup as described above.
2. Copy the `.thrbackup` file to the phone.
3. On the phone, open `Settings` → `Backup & restore` (or `Tools` in the drawer), tap `Restore` and choose the file. Opening the file from a file manager also offers to restore it.
4. Tick the parts to restore and confirm. Throne restarts.

From a phone to the desktop:

1. On the phone, open `Settings` → `Backup & restore`, tick the parts and tap `Create backup`. `Share` sends the file to another app.
2. Copy the file to the computer.
3. On the desktop, restore it as described above.

**Android:** you can also keep backups on a WebDAV server: `Back up to WebDAV`, `Restore from WebDAV` and `WebDAV settings` (`Server address`, `Username`, `Password`, `Backup path`, `Test connection`). Throne desktop has no WebDAV support, but it can restore a file that you download from the server. WebDAV credentials are never included in a backup.

A desktop backup changes a few things when you restore it on Android:

| Item | What happens on Android |
| --- | --- |
| `OTP profiles` and `Custom icons` | Not restored. |
| Settings that both apps have | Take the values from the backup. For example, the TUN MTU becomes 1500 (Android default: 9000) and the log level becomes `info` (Android default: `warn`). |
| Settings that only Android has | Keep their current values. |
| Connections from other devices | When you restore `Settings` and the backup allows other devices to connect, but your phone did not, Throne turns `Allow connections from the LAN` off and shows a warning. |
| Raw routing profiles | Kept, but read-only. Android cannot use them; if one was active, the first usable routing profile becomes active. |
| OpenVPN and OpenConnect endpoints of a routing profile | Kept with the profile, but they do not run on Android. |
| Tailscale and Extra Core profiles | Restored, but they cannot be started on Android. |

In the other direction, rules that match Android apps and the per-app proxy settings have no effect on the desktop.

## Update the desktop app {#updating}

Your profiles and settings live in the data folder, which an update keeps (see [data folder](@/reference/files.md#data-folder)). Still, create a backup first.

1. Open `Tools` → `Check For Update`. Throne asks GitHub for the latest release. If you already run it, you see "No update".
2. If there is a newer version, Throne shows its release notes with the buttons `Update`, `Open in browser` and `Close`.
3. Click `Update`. Throne downloads the new version and asks "Update is ready, restart to install?".
4. Click `Yes`. Throne closes and the updater installs the new version.

The one-click `Update` works only for ZIP copies and for the Windows installer's default install for the current user, where Throne keeps its data next to the program. Other installs only get `Open in browser`. On macOS, with the system-Qt packages and with the Linux install script, no updater ships with Throne, so `Check For Update` is greyed out. Update each kind of install like this:

| Installed with | How to update |
| --- | --- |
| ZIP file | `Update`, or download the new ZIP and replace the program files. Keep the `config` folder. |
| Windows installer, for the current user (default) | `Update`, or download and run the new installer. |
| Windows installer, for all users | Download and run the new installer. |
| `.deb` or `.rpm` package | Download and install the new package. |
| Linux install script | Run the script again. |
| macOS | Download the new version and replace `Throne.app`. See [Installation](@/get_started/installation.md#macos). |
| WinGet, Scoop, AUR, Nix or the RPM repository | Use the package manager. See [Package managers](@/get_started/installation.md#package-managers). |

If you uninstall and reinstall with the Windows installer, answer `No` when the uninstaller asks "Also delete your Throne profiles, settings and logs?". Otherwise your data is deleted.

Some antivirus programs flag the updater, because it replaces program files. If the update fails, check that Throne is not inside your Downloads folder ([#1109](https://github.com/throneproj/Throne/issues/1109)) and try again, or download the new version from the [download page](@/downloads.md).

## Beta versions {#beta}

Beta versions (pre-releases) get new features and fixes first, but they can have more bugs. Make a backup before you install one.

- **Desktop:** turn on `Settings` → `Basic Settings` → `Miscellaneous` → `Allow updating to beta versions`. `Check For Update` then also offers pre-releases, and its window title shows "(Pre-release)".
- **Android:** turn on `Settings` → `General` → `Allow updating to beta versions`. `About` → `Check for updates` then shows "Channel: stable and pre-releases". See [the in-app updater](@/android/installation.md#updater).

To go back, turn the option off. The updater only offers versions newer than the one you run, so you stay on the beta until a newer stable release comes out, unless you install a stable release yourself.

## Old versions {#old-versions}

- **Throne desktop older than 1.1.0.** Version 1.1.0 moved all data into one database file, `throne.db`. Older configurations are not converted. Add your subscriptions and profiles again, or try the community scripts in [#1202](https://github.com/throneproj/Throne/issues/1202). `Backup and Restore` exists since 1.1.3, so backups from 1.1.3 or later restore in newer versions.
- **Nekoray or NekoBox.** See [Coming from Nekoray / NekoBox](@/help/migrating.md).
- **Throne for Android older than 2.0.0.** Version 2.0.0 is signed with a new key, so it cannot be installed over an older version. Uninstall the old app first; 2.0.0 starts empty. Old Android backups (`throne_backup_*.json` files and WebDAV `.zip` files) cannot be restored, only `.thrbackup` files. Before you uninstall, note your subscription links. If you also use Throne desktop, you can move everything with a desktop backup instead. See [Installation & Upgrade](@/android/installation.md#upgrading).
