+++
title = "Lockout Protection & Recovery"
description = "How headless Throne keeps its API within reach, and how to get back in when saved settings such as the kill switch or TUN lock you out."
weight = 50
toc = true
+++

A box without a screen must stay reachable: if a setting cuts it off, you may have no keyboard to fix it. Headless Throne is built to keep the Throne API within reach, and has a recovery start for the cases where saved settings still lock you out.

## How Throne stays reachable {#protection}

**The API is always there.**

- The API is on from the first start, on `127.0.0.1:9095`, with a generated key.
- The `--api-*` options and variables override the saved API settings at every start, so a bad saved listener can be fixed from the command line. See [Options and variables](@/headless/command_line.md#options).
- A settings restore from a backup keeps this device's API, inbound, TUN and kill switch settings.
- An empty `api.key`, as a first start that was cut short leaves behind, gets a new key. Any other key file that cannot be used keeps the API off; delete it, and Throne creates a new key at the next start.

**The API's port.**

- When another program holds the default or saved API port, Throne runs on without the API (`degraded` is `api_unavailable`) and tries again every 30 seconds.
- When another Throne's API holds the port, Throne logs that and leaves it alone. Give this one another port with `--api-listen PORT`.
- A listener given with `--api-listen` that cannot listen makes Throne exit with code 78 instead, so you notice. If its address is not on the computer yet, Throne waits up to 30 seconds for it, then exits with code 1.

**Failed sign-ins.** After 5 failed authentications within a minute from one address, Throne refuses that address for 60 seconds and logs it. It never refuses loopback, or an address where a client authenticated in the last 10 minutes.

**The kill switch and TUN.**

- The [kill switch](@/advanced/kill_switch.md) always lets loopback through. For an API listener on another address, it lets out the replies from the API's port (Linux, macOS and Windows).
- When the core cannot take on the kill switch's group (GID 1950896719), for example in rootless Docker or another user-namespaced container that lacks `CAP_SETGID` or that GID, the core exits with code 86. Throne does not count that as a crash: it runs the core without the group, the kill switch fails closed with code `unsupported` and keeps blocking, and profiles are refused (`kill_switch_inactive`) until you turn the `kill_switch` setting off.
- On Linux, when TUN starts while the API listens on a network address, Throne warns once if remote clients may lose the API: replies to clients outside the bypassed address ranges go into the tunnel unless `tun_auto_redirect` is on, and strict route without `tun_ipv6` drops IPv6 clients.

**A profile that crashes Throne.** When Throne or its core stopped within a minute of resuming the same profile at each of the last three starts, Throne does not resume it (`resume_suppressed`). Start it once with `thronectl connect`. After it has run for a minute, this clears.

**A core that keeps failing.** After three starts in a row in which the core never stayed connected for a minute, Throne no longer exits with codes 70 or 71. It stays up with the API (`degraded` is `core_gave_up`) and tries the core again every 5 minutes, until a core has stayed connected for a minute.

## Recovering access {#recovery}

If saved settings still lock you out, for example a kill switch that ends your SSH session, or TUN that takes the API's replies, start Throne once with `--no-resume --no-kill-switch` (or the variables `THRONE_RESUME=0` and `THRONE_KILL_SWITCH=0`):

- no profile starts,
- the kill switch stays off for that run (profiles stay refused until the `kill_switch` setting is off), and
- `thronectl` on the same device can fix the settings.

Then fix the setting that locked you out, for example with `thronectl settings set kill_switch=false` or `thronectl tun off`, and start Throne normally again.

### systemd {#recovery-systemd}

```bash
printf 'THRONE_RESUME=0\nTHRONE_KILL_SWITCH=0\n' | sudo tee -a /etc/throne/throne.env >/dev/null
sudo systemctl restart throne
thronectl settings set kill_switch=false        # or: thronectl tun off
# remove the two lines from /etc/throne/throne.env again, then:
sudo systemctl restart throne
```

### Docker {#recovery-docker}

Add the two variables under `environment:` in `compose.yaml` and run `docker compose up -d`:

```yaml
    environment:
      THRONE_RESUME: "0"
      THRONE_KILL_SWITCH: "0"
```

Fix the settings with `docker compose exec throne thronectl …`, remove the variables again and run `docker compose up -d`.

### macOS {#recovery-macos}

Add the two variables to the plist's `EnvironmentVariables`, then load it again:

```bash
sudo launchctl bootout system/moe.Throne.headless
sudo launchctl bootstrap system /Library/LaunchDaemons/moe.Throne.headless.plist
```

Fix the settings with `thronectl`, remove the variables and load the plist again the same way.

### Windows service {#recovery-windows}

1. Stop the service: `sc.exe stop Throne`.
2. From an elevated prompt, start Throne by hand for the same data directory:

   ```bat
   start "" /wait "C:\Program Files\Throne\Throne.exe" --headless --data-dir C:\ProgramData\Throne --no-resume --no-kill-switch
   ```

3. Fix the settings with `thronectl` from another elevated prompt (see [Commands from a prompt](@/headless/installation.md#windows-prompt)).
4. Stop Throne with `Ctrl+C`, then start the service again: `sc.exe start Throne`.

### Starting over {#start-over}

If nothing else helps, stop Throne and move its data directory aside (for the system unit, `/var/lib/throne`). The next start creates a new, empty one with a new API key. Restore your profiles from a [backup](@/headless/thronectl.md#from-desktop).
