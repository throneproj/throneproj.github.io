+++
title = "Command Line, Files & Logs"
description = "Command-line options of Throne desktop, where it keeps your data on each system, what the files in the config folder hold, the logs, and how to reset."
weight = 30
toc = true
+++

This page explains the command-line options of Throne desktop, where Throne stores your data, what each file is for, where to find the logs, and how to start over with default settings.

## Command line {#command-line}

Throne accepts these options:

| Option | What it does |
| --- | --- |
| `-appdata` | Keeps the data in your user folder instead of next to the program. See [Data folder](#data-folder). |
| `-appdata <folder>` | Keeps the data in `<folder>`. Throne creates a `config` folder inside it. |
| `-tray` | Starts with the window hidden. Only the tray icon appears. |
| A `throne://` link | Handles the link as if you had clicked it. See [Deep Links](@/advanced/deeplinks.md). |
| File paths or `file://` URLs | Imports the files, like `Program` → `Add profile from File(s)`. |

Examples:

```bash
/opt/Throne/Throne -appdata
./Throne -appdata "$HOME/throne-test"
./Throne -tray
```

```powershell
.\Throne.exe -appdata D:\ThroneData
```

- Throne reads the word after `-appdata` as the folder, unless it starts with `-`.
- Only one Throne runs per data folder. If Throne is already running, a new start passes its link or files to the running Throne, brings its window to the front, and exits.
- **macOS:** to pass options, run the program inside the app bundle, for example `/Applications/Throne.app/Contents/MacOS/Throne -tray`. Links that you click are passed to the running Throne by macOS.

## Data folder {#data-folder}

Throne keeps your data in a folder named `config`. To open it, choose `Settings` → `Open Config Folder`.

Throne works in one of two modes:

- **Portable mode:** the `config` folder is inside the Throne program folder.
- **Appdata mode:** the `config` folder is in your user folder. Throne uses this mode when it starts with `-appdata`, always on macOS, and when it cannot write to its own folder.

In appdata mode, the folder is:

| System | Data folder |
| --- | --- |
| Windows | `%LOCALAPPDATA%\Throne\config`, for example `C:\Users\<you>\AppData\Local\Throne\config` |
| Linux | `~/.config/Throne/config`, or `$XDG_CONFIG_HOME/Throne/config` if you set `XDG_CONFIG_HOME` |
| macOS | `~/Library/Preferences/Throne/config` |

Which mode your copy uses depends on how you installed it:

| How you installed Throne | Mode | Data folder |
| --- | --- | --- |
| Windows ZIP | Portable | `config` in the unpacked `Throne` folder |
| Windows installer, for the current user (default) | Portable | `config` in the install folder, by default `%LOCALAPPDATA%\Throne\config` |
| Windows installer, for all users | Appdata (automatic) | `%LOCALAPPDATA%\Throne\config` of each user |
| Linux ZIP | Portable | `config` in the unpacked `Throne` folder |
| Linux `.deb`, `.rpm` or install script | Appdata | `~/.config/Throne/config` |
| macOS | Appdata | `~/Library/Preferences/Throne/config` |

- The app-menu entry that the `.deb` and `.rpm` packages and the Linux install script create starts `/opt/Throne/Throne -appdata`.
- If Throne cannot write to its own folder, for example in `Program Files`, it switches to appdata mode by itself. The first time, it copies your existing `config` folder there. After that, it keeps using the per-user folder, even when you run it as administrator.
- Packages from other sources (WinGet, Scoop, AUR, Nix) may use other folders. `Open Config Folder` always shows the right one.

A few files are stored next to the `config` folder, not inside it: the Xray geo files `geoip.dat` and `geosite.dat`, and the `diagnostics` folder with the files from `Basic Settings` → `Diagnostics`. In portable mode this is the Throne program folder. In appdata mode it is the per-user folder, for example `%LOCALAPPDATA%\Throne`, even when you give `-appdata` another folder.

### Files in the config folder {#config-files}

| File or folder | What it holds |
| --- | --- |
| `throne.db` | Your profiles, groups, routing profiles, OTP profiles and settings, in an SQLite database. While Throne runs, `throne.db-wal` and `throne.db-shm` appear next to it. |
| `throne_stats.db` | Traffic history for `Tools` → `Traffic Stats`: data per minute for the last 48 hours, and data per hour for 90 days. `Basic Settings` → `Style` → `Disable Traffic Aggregation` stops it. |
| `cache.db` | The cache of the core: downloaded rule-sets, the last choice of an auto selector and, if `Save Cache To File` is on, the DNS cache. |
| `logs/` | Log files. See [Logs](#logs). |
| `crashes/` | Crash dumps (Windows only). The newest 5 are kept. |
| `icons/` | Custom tray icons from `Basic Settings` → `Style` → `Enable Custom Icons`. |
| `dashboard/` | Files of a web dashboard for the Clash API. Throne creates the folder with a placeholder page; replace it with the dashboard files. |
| `sb-dashboard/` | The web dashboard that `Tools` → `Open Web dashboard` opens. |

To move your data to another computer or to Android, create a `.thrbackup` backup instead of copying files. See [Backup and restore](@/guides/backup.md#backup-restore).

## Logs {#logs}

The `Logs` tab at the bottom of the main window shows messages from Throne and from the core. Right-click the log to copy text or to `Clear` it.

The log settings are in `Settings` → `Basic Settings` → `Logging`:

| Setting | Default | What it does |
| --- | --- | --- |
| `Max log lines` | `200` | How many lines the `Logs` tab keeps. |
| `Auto-scroll log` | On | Keeps the newest line in view. |
| `Sing-box Log level` | `info` | How much detail the core writes: `trace`, `debug`, `info`, `warn`, `error`, `fatal` or `panic`. |
| `Xray Log level` | `warning` | How much detail Xray writes: `debug`, `info`, `warning`, `error` or `none`. |
| `Log Filtering` | Off | `Enable Include Rules` shows only lines that match your keywords or regular expressions. `Enable Exclude Rules` hides matching lines. Filters change only the `Logs` tab, not the log file. |

For a bug report, set `Sing-box Log level` to `debug`, start the profile again, and reproduce the problem. Then follow [Reporting a Bug](@/help/bug_reports.md#logs).

### Log file {#log-file}

Throne also writes the log to `logs/throne.log` in the config folder.

- The file starts with the Throne version, your operating system, the command-line options and the log folder.
- It contains everything from the `Logs` tab and more detail from Throne itself.
- Throne starts a new file at every start. When the file reaches 4 MB, Throne renames it to `throne.log.1` and starts a new one. It keeps up to three old parts, `throne.log.1` to `throne.log.3`.
- If Throne did not quit cleanly, it keeps the log of that session as `crashed-YYYYMMDD-HHMMSS.log` in the same folder. The newest 5 are kept. At the next start, the `Logs` tab shows "[Warn] Throne did not shut down cleanly last time. Diagnostics were saved to: …", followed by the path of the log folder.

{% alert_warning() %}
Logs can contain the domains you visited and the addresses of your servers. Check a log before you share it publicly.
{% end %}

**Android:** open the drawer and tap `Logs`. `Share logs` and `Save logs…` export the log. `Hide sensitive data` is on by default. In the export, it hides passwords, keys, UUIDs, server names, public IP addresses, Wi-Fi names and the paths of URLs. The log level is in `Settings` → `Core` → `Log level` (default `warn`). See [Android Troubleshooting](@/android/troubleshooting.md#logs).

## Reset Throne {#reset}

Throne has no reset button. To start over with default settings, give Throne a new, empty config folder:

1. To keep anything, create a backup first: `Settings` → `Basic Settings` → `Backup and Restore` → `Create Backup...`.
2. Choose `Settings` → `Open Config Folder` to see where the folder is.
3. Quit Throne with `Exit` in the tray menu or the `Program` menu. Closing the window is not enough.
4. Rename the `config` folder, for example to `config-old`.
5. Start Throne. It creates a new `config` folder with default settings.

To bring back part of your old data, use `Restore from Backup...` on the same tab and select only the parts you need. See [Backup and restore](@/guides/backup.md#backup-restore).

To undo the reset, quit Throne, delete the new `config` folder, and rename `config-old` back to `config`.

A reset does not change what is stored outside the config folder: `Start with system` (it is an autostart entry of the operating system), the `throne://` link registration, and the Xray geo files.

**Windows:** if you installed Throne with the installer, uninstalling asks "Also delete your Throne profiles, settings and logs?". Choose `Yes` to delete the config folder too.

**Android:** `Settings` → `Restore default settings` resets all settings but keeps your profiles, groups and routing profiles. The app then restarts. To remove everything, clear the app's data in the Android app settings. Throne for Android keeps its data in the app's private storage, which file managers cannot open, so use a `.thrbackup` backup to copy your data out.
