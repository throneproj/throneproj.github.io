+++
title = "Health Checks & Logs"
description = "Check whether a computer can run headless Throne, ask a running Throne how it is doing, read its systemd status and find its logs."
weight = 40
toc = true
+++

Headless Throne has two built-in checks: `Throne --check` before the first start or when something does not work, and `Throne --health` for a running Throne. It also reports its state to systemd and writes a log.

## Throne --check {#check}

`Throne --check` tells you whether this computer can run headless Throne as it is set up. Run it as Throne's user, with the options and variables Throne starts with. It changes nothing: it creates no file, takes no lock, opens the database read-only, and runs beside a running Throne.

It prints one line per item, with `fix:` lines where there is a fix:

```text
$ sudo /opt/Throne/Throne --check
[INFO] build: Throne <version>, Qt 6.x, Debian GNU/Linux 12 (bookworm) x86_64, kernel 6.1.0-28-amd64, euid 0, ruid 0
[INFO] data dir /var/lib/throne (root default): does not exist yet; the first start creates it
[ OK ] instance: none (no data dir yet)
...
[INFO] API key: /var/lib/throne/config/api.key is created on the first start
[ OK ] port 127.0.0.1:9095 (the Throne API, the headless default): free
[ OK ] port 127.0.0.1:2080 (the mixed proxy, inbound_port): free
...
result: 0 failed, 0 warnings
```

It covers the build, the data directory, a running instance, the settings, TLS, the core, TUN, the kill switch, the API key, the ports (the API, the mixed inbound, the DNS port, and the Clash and sing-box APIs when they are on), other headless Thrones and TUN owners on the computer, the service manager and restart mode, and the [device ID](@/headless/_index.md#device-id).

Only what keeps Throne from working at all is `[FAIL]`, and then the command exits with code 1. Missing privileges for TUN or the kill switch are `[WARN]`, with the `setcap` or `chmod u+s` commands to fix them, or with `--cap-add NET_ADMIN` and `--device /dev/net/tun` in a container.

## Throne --health {#health}

`Throne --health` asks the running Throne over its instance socket and prints one line of JSON. Run it as Throne's user and for the same data directory:

```bash
$ sudo /opt/Throne/Throne --health
{"api":"listening","core_restarts":0,"degraded":null,"headless_dialogs":0,"ok":true,"previous_crash":false,"previous_exit":{"at":1760700000,"code":75,"reason":"restart requested"},"ready":true,"state":"running","stuck_s":0}
```

It exits with code 0 when Throne is healthy. See [Exit codes](@/headless/command_line.md#exit-codes) for the others.

| Field | Meaning |
| --- | --- |
| `ok` | Throne works: it has started, the core is connected, nothing is stuck, the core has not been given up on, and the kill switch is off or works. A kill switch that cannot work as set up, or that `--no-kill-switch` turned off, leaves it `true`, because a restart cannot fix it. It never depends on a remote server or on a running profile, so restarting Throne when it is `false` does not loop during a server outage. |
| `ready` | Throne has finished starting. |
| `state` | `idle`, `connecting`, `running`, `stopping`, or `starting` until Throne has started. |
| `degraded` | `null`, or why Throne cannot work as set up. See the table below. |
| `stuck_s` | How many seconds a profile has been connecting beyond the first 90 seconds, or stopping beyond the first 45; otherwise 0. While it is above 0, `ok` is `false`. |
| `core_restarts` | How often the core was restarted. |
| `headless_dialogs` | Questions skipped because there is no window. It should stay 0. The log names them in `HEADLESS-DIALOG` lines. |
| `previous_crash` | The previous run did not end cleanly: a crash, `kill -9` or a power loss. |
| `previous_exit` | How the previous run ended, as `{code, reason, at}` (`at` in seconds since 1970), or `null`. After the service manager restarted Throne (codes 75, 70, 71), this is where the reason survives. |
| `api` | The API listener: `off`, `listening`, `key_invalid`, `failed`, `retrying` (waiting up to 30 seconds for its address) or `address_missing` (its address left every network interface). |

In the first moments of a start, the line has only `ok`, `ready`, `state` and `headless_dialogs`.

The values of `degraded`. When several apply, Throne reports the first one in this order:

| Value | Meaning |
| --- | --- |
| `core_gave_up` | The core kept failing and Throne gave up on it. Throne exits with code 70 for the service manager, or, after three such starts in a row, [stays up](@/headless/recovery.md#protection) and tries the core again every 5 minutes. |
| `core_unavailable` | The core process is not up. |
| `kill_switch_failed` | The kill switch is on but failed. Profiles are refused. See [Kill Switch](@/advanced/kill_switch.md). |
| `api_unavailable` | The API is on but does not listen, for example because another program holds its port or its key file cannot be used. `ok` stays `true`. |
| `tun_unavailable` | TUN was on when Throne last stopped, and Throne cannot turn it on now: it lacks the privileges, or something else holds TUN (a [TUN conflict](@/headless/_index.md#beside-desktop)). Throne did not start the profile without TUN. `thronectl tun off` clears this; then start the profile with `thronectl connect`. |
| `resume_suppressed` | Throne did not resume the last profile, because each of the last three times it did, Throne or its core stopped within a minute. Start the profile with `thronectl connect`; once it has run for a minute, this clears. |
| `vpn_auth_failed` | The server of a VPN profile rejected its saved credentials. It clears when the profile stops. |
| `vpn_challenge_pending` | The server of a VPN profile asks for something that Throne cannot answer on its own, such as a web sign-in. Throne cancels the question when it expires, after 5 minutes at most. |

The [API specification](https://github.com/throneproj/Throne-api/blob/main/spec/api.md#headless-throne) describes these values in detail.

The Docker image uses `Throne --health` as its health check. A monitoring script that wants more can send the line `HEALTH` to the socket `config/.instance` in the data directory:

```bash
echo HEALTH | sudo socat -t 3 - UNIX-CONNECT:/var/lib/throne/config/.instance
```

The answer adds `mode`, `pid`, `uptime_s`, `version`, `tun_running`, the full `api` block and the fields of `thronectl status`. If the data directory's path is 100 bytes or longer, or its file system has no sockets, the socket moves to `headless-<hash>` in `/run/throne` (`/var/run/throne` on macOS) for root, or in `/tmp/throne-<uid>` for other users. On Windows, use `--health`.

## systemd: readiness, status and watchdog {#systemd}

The shipped unit is `Type=notify`. Throne reports to systemd from its main process:

- **`READY=1`** once it holds the data directory, the database is open, the API listens (or failed), the core is connected, the kill switch has settled and the resumed profile is on its way. This usually takes less than 20 seconds. Until then Throne extends the start timeout, so `TimeoutStartSec=90` ends only a start that hangs. After three starts without a working core it reports ready anyway.
- **`STATUS=`**, which `systemctl status` shows: `Starting`, `Starting core`, `Core restarting 2/5`, `Idle`, `Connecting <profile>`, `Connected <profile>` (with ` (Tun)` when TUN is on), `Stopping <profile>`, `Degraded: <reason>`, `Stopping` and `Restarting`.
- **`WATCHDOG=1`** every 20 seconds while its main loop runs (a third of `WatchdogSec=60`). If the main loop hangs, systemd sends `SIGABRT` and starts Throne again.
- **`STOPPING=1`** when it begins to exit, or `RELOADING=1` before it restarts in place (`--restart-mode exec`).

Throne also watches its own progress, with or without systemd: a profile that is connecting for 180 seconds or stopping for 90 makes it exit with code 71, and a core that has not been usable for 60 seconds makes it exit with code 70. The service manager then starts it again.

`KillMode=mixed` is required. With it, systemd sends `SIGTERM` to Throne alone, and Throne stops its core and the kill switch in order, then exits, usually within seconds (`TimeoutStopSec=45`). A second `SIGTERM` or `SIGINT` kills the core at once. Do not use `systemctl kill`: it signals the core and the kill switch helper directly.

## Logs {#logs}

Throne writes its log to standard error and to `config/logs/throne.log` in the data directory. Where to read it:

| How Throne runs | Log |
| --- | --- |
| systemd system unit | `journalctl -u throne -f` |
| systemd user unit | `journalctl --user -u throne -f` |
| Docker | `docker compose logs -f throne` |
| macOS LaunchDaemon | `/Library/Logs/Throne/throne.log` |
| Windows service | `C:\ProgramData\Throne\config\logs\throne.log` (a service has no standard error) |

`thronectl logs` reads the log through the API, from any device that may send [admin requests](@/headless/thronectl.md#admin-requests): `thronectl logs -n 500` prints the last 500 lines, and `thronectl logs -f` then keeps printing new ones, also across restarts of Throne. These are the lines that the desktop app's log window shows, core output included; Throne keeps the newest 5000 in memory. The `Logs` page of the [web UI](@/headless/web.md) shows the same lines in a browser.

Headless Throne logs in English. `--debug` adds debug lines. `--log-format` sets the format of standard error:

| Format | Lines |
| --- | --- |
| `auto` | `journal` when standard error goes to the systemd journal, else `plain` |
| `journal` | Each line starts with a syslog priority such as `<4>`, which journald turns into the message's priority. journald adds the time. |
| `plain` | Each line starts with the local time. |

Lines worth searching for:

- `EXIT <code>: <reason>`: why Throne exited. See [Exit codes](@/headless/command_line.md#exit-codes).
- `Ready <n> ms after launch`: the start has finished.
- `[API] Listening on …`: where the API listens.
- `[Resume] …`: whether the last profile was started again.
- `[Kill switch] Not active (<code>): …`: why the kill switch does not work.
- `[Watchdog] …`: Throne's own progress checks.
- `HEADLESS-DIALOG`: a question nobody could answer.

When a run does not end cleanly, its log is kept as `config/logs/crashed-<time>.log`, and crash reports go to `config/crashes/`.
