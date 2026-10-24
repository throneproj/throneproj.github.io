+++
title = "Troubleshooting"
description = "Common problems with headless Throne, from a unit that will not start to TUN conflicts and refused API requests, and what to include in a bug report."
weight = 60
toc = true
+++

Start with `Throne --check` and `Throne --health`, run as Throne's user and with the same `--data-dir` (see [Health Checks & Logs](@/headless/monitoring.md)), and read the last lines of the log. The line `EXIT <code>: <reason>` says why Throne exited; [Exit codes](@/headless/command_line.md#exit-codes) explains each code.

## Common problems {#symptoms}

| Symptom | Cause and fix |
| --- | --- |
| The unit fails at once, and the log says `refusing to run as root with /var/lib/throne` | Other users can write to the data directory. Run `sudo chmod go-w /var/lib/throne /var/lib/throne/config`. |
| Exit code 3: `… is in use by …` | Another Throne holds the data directory: the desktop app, a user unit, or a second service. Stop the other one. |
| The desktop app says `Throne is running in the background` and exits | A headless Throne (usually a user unit) uses the desktop app's data directory. Run `systemctl --user stop throne`, or manage it with `thronectl`. See [Running beside a desktop Throne](@/headless/_index.md#beside-desktop). |
| `degraded: api_unavailable`, and the log says `[API] Not listening on 127.0.0.1:9095` | Another program holds port 9095. Throne tries again every 30 seconds. `--api-listen PORT` picks another port. |
| `--print-connection`: `The API key is not in a file` | The data directory's settings turned the API on with a key of their own, as the desktop app does. Use that key as `THRONE_KEY` (in the desktop app: `Integration Settings` → `Throne API` → `Copy for scripts`), or start Throne with `--api-key-file`. |
| `--health` or `--print-connection`: `No headless Throne answered` | Run it as Throne's user, with the same `--data-dir`. For the system unit, use `sudo`. |
| Windows: `[Instance] Not talking to … access denied` | The service's pipe is only for Administrators and SYSTEM. Run the command from an elevated prompt, with `--data-dir C:\ProgramData\Throne`. |
| thronectl: `Throne closed the connection without a response` | A wrong key, or your address is refused for 60 seconds after 5 failed attempts, for example by another client with an old key. Check `THRONE_KEY_FILE` and wait a minute. |
| thronectl: `forbidden` | An [admin request](@/headless/thronectl.md#admin-requests) from another device. Start Throne with `--api-admin-lan`, or run the command on Throne's own device. |
| thronectl: no connection | Throne is not running, or `THRONE_ADDR` points elsewhere. Check `systemctl status throne` and `Throne --print-connection`. |
| `thronectl tun on`: `needs_privileges` | Throne lacks the privileges for TUN. Run `Throne --check`, and see [Privileges on Linux](@/headless/installation.md#linux-privileges). |
| `thronectl proxy on`: `system_proxy_unsupported` | Headless Throne has no system proxy. Point other programs at the mixed inbound, or use TUN. |
| `tun_conflict`: `the Tun address 172.19.0.1 is already used by the network interface br-…` | A Docker network (or another network) uses Throne's TUN range. Move TUN to a free range with `thronectl settings set tun_ipv4_cidr=172.29.0.1/24` (any range that no network interface on the computer uses), then run `thronectl tun on` again. Or give that Docker network another subnet. |
| `tun_conflict`: `port 5533 on 127.0.0.1 (the core's DNS server, dns_in_port) is in use` | Another program holds the DNS port. Run `thronectl settings set dns_in_port=PORT` with a free port, then `thronectl tun on` again. |
| `tun_conflict` naming another Throne | Another Throne on the computer runs TUN, for example a desktop Throne. Only one Throne can run TUN at a time. |
| Profiles refused: `kill_switch_inactive` | The kill switch is on but cannot work. `kill_switch_error` in `thronectl --json status` and the log line `[Kill switch] Not active (<code>)` say why: `privilege`, `unsupported`, `config` or `overridden`. `thronectl settings set kill_switch=false` turns it off. See [Kill Switch](@/advanced/kill_switch.md). |
| `degraded: resume_suppressed` | The resumed profile made Throne or its core stop at three starts in a row. Fix the profile, then start it with `thronectl connect <id>`. |
| `degraded: core_gave_up` | The core keeps failing. Throne [stays up](@/headless/recovery.md#protection) and tries again every 5 minutes. The give-up line in the log ends with the core's last error. |
| `degraded: vpn_challenge_pending` or `vpn_auth_failed` | A VPN profile needs a sign-in that headless Throne cannot give, or its saved credentials were rejected. Give the profile an [OTP account](@/advanced/vpn_profiles.md#otp-manager) for one-time codes, or fix the credentials in a desktop Throne and move them over with a [backup](@/headless/thronectl.md#from-desktop). |
| `previous_crash: true` | The last run did not end cleanly. Its log is `config/logs/crashed-<time>.log` in the data directory. |
| Docker: the published port 2080 does not answer | The inbound listens on `127.0.0.1`. Run `thronectl settings set inbound_address=0.0.0.0` and start the profile again. |
| Docker: the container comes back after `thronectl shutdown` | `restart: unless-stopped` starts it after every exit. Stop it with `docker compose stop`. |
| macOS: Throne starts every 10 seconds and exits | A configuration error that launchd retries. Read `/Library/Logs/Throne/throne.log`. |
| Windows: the service stops at once | `sc.exe query Throne` shows Throne's exit code as `SERVICE_EXIT_CODE`. The log is in `C:\ProgramData\Throne\config\logs`. Code 78 often means a problem with [the data folder](@/headless/installation.md#windows-data-folder). |
| Windows: `tun_failed` with `open existing adapter`, or the log line `Windows still held the Tun adapter of an earlier session; start the profile again` | Windows still holds the TUN adapter of an earlier run that did not end cleanly. Start the profile again with `thronectl connect last`; that usually works. Throne does not try again on its own. If it keeps failing, restart Windows. |
| You are locked out by the kill switch or TUN | Start Throne once with `--no-resume --no-kill-switch`. See [Recovering access](@/headless/recovery.md#recovery). |

## What to include in a bug report {#reporting}

If the problem stays, [report a bug](@/help/bug_reports.md) and include:

- the output of `Throne --check`,
- the output of `Throne --health`,
- how Throne runs: the package or image and its version, and the service manager,
- the log, from the start until the problem, with `--debug` if you can reproduce it. For a crash, also `config/logs/crashed-<time>.log`.

Remove server addresses, subscription URLs and keys from what you post. Never post `api.key`.
