+++
title = "Command Line & Data Directory"
description = "Every option and environment variable of headless Throne, where it keeps its data, how it restarts, and what its exit codes mean."
weight = 30
toc = true
+++

This page lists the options and environment variables of headless Throne, where it keeps its data, how it restarts and what its exit codes mean. For the desktop app's command-line options, see [Command line](@/reference/files.md#command-line).

## Options and variables {#options}

`Throne --headless --help` lists the options. One or two dashes both work (`-data-dir` is the same as `--data-dir`), and a value follows a space or `=`. An option wins over its variable. A variable set to an empty value counts as unset, except `THRONE_API_ALLOW`.

| Option | Variable | What it does |
| --- | --- | --- |
| `--headless` | `THRONE_HEADLESS=1` | Run without a window. Any value of the variable except empty, `0`, `false`, `no` and `off` turns it on. |
| `--data-dir DIR` (`-appdata DIR`) | `THRONE_DATA_DIR` | The [data directory](#data-dir). |
| `--restart-mode MODE` | `THRONE_RESTART_MODE` | `auto` (default), `exit` or `exec`. See [Restart modes](#restart-modes). |
| `--no-resume` | `THRONE_RESUME=0` | Do not start the last profile at start. |
| `--no-kill-switch` | `THRONE_KILL_SWITCH=0` | Keep the [kill switch](@/advanced/kill_switch.md) off for this run even when the `kill_switch` setting is on. Profiles stay refused until the setting is turned off. Meant for [recovery](@/headless/recovery.md#recovery). |
| `--log-format FORMAT` | `THRONE_LOG_FORMAT` | `auto` (default), `journal` or `plain`. See [Logs](@/headless/monitoring.md#logs). |
| `--api-listen LISTEN` | `THRONE_API_LISTEN` | Where the Throne API listens: `PORT` (on `127.0.0.1`), `IPv4:PORT`, `[IPv6]:PORT`, `*:PORT` (every address) or `off`. Default: `127.0.0.1:9095`, unless the saved settings turn the API on. |
| `--api-key-file FILE` | `THRONE_API_KEY_FILE` | Read the API key from this file, which must exist. `thronectl keygen -o FILE` writes one. Default: `config/api.key` in the data directory, created at the first start. |
| `--api-admin-lan` | `THRONE_API_ADMIN_LAN=1` | Answer [admin requests](@/headless/thronectl.md#admin-requests) (imports, settings, backups, restart) from the network too, not only from this device. |
| `--api-allow LIST` | `THRONE_API_ALLOW` | Addresses and subnets that may use a listener that is not on loopback, separated by commas or spaces. An empty list exits with code 64. Leave the variable unset to allow every address. |
| `--debug` | | Debug logging. |
| `--service` | | Windows only: run under the Service Control Manager, headless even without `--headless`. Started any other way, it exits with code 64. |
| `--health` | | Ask the running Throne how it is doing. See [Throne --health](@/headless/monitoring.md#health). |
| `--print-connection` | | Print `THRONE_ADDR` and `THRONE_KEY_FILE` for `thronectl`. See [Connect thronectl to Throne](@/headless/thronectl.md#connect). |
| `--check` | | Check whether this computer can run headless Throne. See [Throne --check](@/headless/monitoring.md#check). |
| `--help`, `--version` | | Print the options or the version. |

- The yes/no variables take `1`, `true`, `yes`, `on`, `0`, `false`, `no` or `off`. Anything else exits with code 64.
- The `--api-*` options and variables override the saved API settings at every start and are never saved. That way a bad saved API setting can always be fixed from the command line.
- `--health`, `--print-connection` and `--check` work without `--headless`. Use only one of them at a time, and never with `--service`.
- A link or a file on the command line exits with code 64. Import it with [`thronectl import`](@/headless/thronectl.md#profiles).

With the systemd unit, set variables in `/etc/throne/throne.env` and options with a drop-in. See [Debian, Ubuntu, Raspberry Pi OS, Fedora, openSUSE](@/headless/installation.md#linux-packages).

## Data directory {#data-dir}

Headless Throne uses the first of these that applies:

1. `--data-dir`, then `THRONE_DATA_DIR`. A relative path counts from the folder Throne starts in.
2. `STATE_DIRECTORY`, which systemd sets for `StateDirectory=`.
3. As root: `/var/lib/throne` on Linux, `/Library/Application Support/Throne` on macOS. On Windows, with `--service` or as LocalSystem: `C:\ProgramData\Throne`.
4. The user's configuration folder, which the desktop app also uses: `~/.config/Throne` on Linux, `~/Library/Preferences/Throne` on macOS, `%LOCALAPPDATA%\Throne` on Windows. On Linux and macOS without a `HOME`, Throne exits with code 78; name the directory with `--data-dir`.

Headless Throne never keeps its data next to the program, as a portable desktop installation does. To share such an installation's data, pass `--data-dir` with the program's folder.

On Linux and macOS it creates missing directories readable only by its user. Run as root, it refuses a data directory that other users can write to (code 78), because the settings name programs that Throne starts. On Windows, `C:\ProgramData\Throne` is kept for SYSTEM and Administrators only (see [The data folder](@/headless/installation.md#windows-data-folder)); another directory that normal users can write to only gets a warning in the log.

What is in it:

| Path | Contents |
| --- | --- |
| `config/throne.db` | Profiles, groups, routing profiles and settings, as in the desktop app |
| `config/api.key` | The API key, readable only by Throne's user |
| `config/logs/throne.log` | The log of this run. `crashed-<time>.log` keeps the log of a run that did not end cleanly. |
| `config/crashes/` | Crash reports |
| `config/headless-state.json` | Counters for resuming the profile and for crashes, and how the last run ended |
| `config/hwid` | The [device ID](@/headless/_index.md#device-id), when the system has none |
| `config/.lock`, `config/.instance` | The data directory's lock, and the socket that `--health` asks. On Windows the instance is a named pipe, not a file. |
| `web/` | Docker image only: the password hash and the TLS certificate of the [web UI](@/headless/web.md#docker) |

## Restart modes {#restart-modes}

`thronectl restart`, a backup restore and the `SIGHUP` signal restart Throne. `--restart-mode` decides how:

| Mode | What happens |
| --- | --- |
| `exit` | Throne exits with code 75, and the service manager starts it again. |
| `exec` | Throne starts again in the same process (Linux and macOS; the process ID stays the same). On Windows it starts a new Throne process and exits with code 0. A Windows service always uses `exit`. |
| `auto` | `exit` when systemd (its notify socket, or the user manager), launchd or a container init started Throne, or when it runs as a Windows service. `exec` otherwise, for example from a terminal. |

The shipped units, the plist and the Docker image need `auto` or `exit`. `Throne --check` shows what `auto` picks. In a terminal, closing the terminal (a hang-up) stops Throne with code 0 instead of restarting it.

## Exit codes {#exit-codes}

Throne writes `EXIT <code>: <reason>` to the log before it exits. What the shipped service files do with each code:

| Code | Meaning | systemd unit | Docker `unless-stopped` | launchd plist | Windows service |
| --- | --- | --- | --- | --- | --- |
| 0 | Stopped: `SIGTERM`, `SIGINT`, `thronectl shutdown`; on Windows also a service stop, `Ctrl+C`, closing the console, signing out or `taskkill` without `/F`. Also a Windows restart outside the service, which has started a new Throne. | Stays down | Starts again, unless `docker stop` | Stays down | Stays stopped |
| 1 | The start failed for a reason that may pass: the lock, the instance socket, the database, the core's IPC listener, or an `--api-listen` address that did not appear within 30 seconds | Starts again after 3 s | Starts again | Starts again after 10 s | Recovery |
| 3 | Another Throne uses the data directory | Stays down | Starts again | Retried every 10 s | Recovery |
| 64 | A bad option, option value or variable, or `--service` not started by the Service Control Manager | Stays down | Starts again | Retried every 10 s | Recovery |
| 70 | The core kept failing and Throne gave up, or the core was not usable for 60 seconds | Starts again | Starts again | Starts again | Recovery |
| 71 | A profile was connecting for 180 seconds or stopping for 90 | Starts again | Starts again | Starts again | Recovery |
| 75 | Restart requested, with `--restart-mode exit` or as a Windows service, or an `exec` restart that could not happen | Starts again | Starts again | Starts again | Recovery |
| 78 | Configuration error: the data directory (also no `HOME` to find one, or on Windows a `C:\ProgramData\Throne` that another user owns, that other users can write to, or that is a link), the API key file, the `--api-listen` listener, or a database file that cannot be used | Stays down | Starts again | Retried every 10 s | Recovery |

"Recovery" means the Windows service's recovery actions: see [Windows service](@/headless/installation.md#windows).

- The systemd unit has no start limit (`StartLimitIntervalSec=0`). Every `thronectl restart`, restore and `SIGHUP` is a new start, and a limit would leave Throne down with no API.
- Docker waits longer before each restart in a row.
- After three starts in a row without a working core, Throne stops exiting with codes 70 and 71 and [stays up](@/headless/recovery.md#protection) instead.
- For code 78 with a database, the log says what to do: move a damaged `config/throne.db` aside together with its `-wal` and `-shm` files, or put back a copy. Make read-only files writable by Throne's user.

The check commands exit with their own codes:

| Command | 0 | 1 | 2 | 64 |
| --- | --- | --- | --- | --- |
| `--health` | Healthy | Not healthy, or still starting | No Throne answered, or a Windows service refused a prompt that is not elevated | Bad option |
| `--check` | No `[FAIL]` line | A `[FAIL]` line | | Bad option |
| `--print-connection` | Printed both lines | | The API is off or not listening, or its key is not in a file; or a Windows service refused the prompt | Bad option |

`--health` and `--print-connection` exit with code 78 when they find no data directory (no `HOME`); name it with `--data-dir`.
