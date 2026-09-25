+++
title = "Privacy & Network Requests"
description = "What Throne sends to subscription providers, every network request the app makes by itself, and who can use its local proxy port."
weight = 40
toc = true
+++

Throne sends your traffic where your profiles and routing rules say. This page covers what Throne sends on its own: device information for subscriptions (HWID), the network requests the app makes by itself, and who can use its local proxy port. Throne does not send usage statistics, and it does not upload logs or crash dumps.

## HWID and device information {#hwid}

Some providers want to know which device requests a subscription. Throne can send four headers with subscription requests. This is off by default.

| Header | Windows | Linux | macOS |
| --- | --- | --- | --- |
| `x-hwid` | The Windows `MachineGuid` | The content of `/etc/machine-id` (or `/var/lib/dbus/machine-id`) | The hardware UUID of the Mac |
| `x-device-os` | `Windows` | `Linux` | `macOS` |
| `x-ver-os` | The Windows version, for example `10.0.26100` | The kernel version | The macOS version, for example `14.5` |
| `x-device-model` | The computer model (and motherboard) reported by Windows | The name of the distribution, for example `Ubuntu 24.04.1 LTS` | The macOS name and version, for example `macOS Sonoma (14.5)` |

To turn it on:

1. Open `Settings` → `Basic Settings` → `Subscription`.
2. Turn on `Enable sending HWID, device model, and OS version when updating subscription`.
3. Click `OK`.

Hover over the checkbox to see the values that Throne found on your computer.

- Throne sends these headers only with subscription requests, never with any other request.
- `Custom System Parameters (optional)` replaces values that Throne sends. Use the form `hwid=value,os=value,osVersion=value,model=value` and list only the values you want to replace.
- Each subscription group can decide for itself: choose `Groups` → `Edit current Group`, and click `Advanced` in the `Subscription` section. `Send HWID` is `Keep Default` (follow the setting above), `On` or `Off`. The `HWID`, `OS`, `OS Version` and `Device Model` fields replace the values for this group only.
- Every subscription request also sends a User-Agent: `Throne/<version>`, for example `Throne/1.3.1`, unless you set another `User Agent` in the same tab or for the group.

See [User-Agent and HWID](@/guides/subscriptions.md#user-agent-and-hwid) for when a provider needs these settings.

**Android:** `Settings` → `Subscriptions` has the same switch (off by default) and `Custom HWID parameters (optional)`. Throne for Android sends the Android ID (`ANDROID_ID`) as HWID. If the Android ID is not available, it creates a random ID once and keeps sending that. It sends `Android` as OS, the Android version, and the device model. Its default User-Agent is `Throne/Android/<version>`.

## Network requests {#network-requests}

Besides the traffic of your apps, Throne sends the requests in the table below. Many of them follow the "`Use proxy` rule":

- They go out directly by default.
- If `Settings` → `Basic Settings` → `Miscellaneous` → `Use proxy` is on, or `System Proxy` is on, they go through Throne's local proxy port instead.
- If they should use the local proxy port but no profile is running, they fail with "Request with proxy but no profile started."

A request that goes through the local proxy port enters Throne like the traffic of any other app, so your routing profile decides where it goes.

| Request | When | Destination | Route |
| --- | --- | --- | --- |
| Subscription update | When you add or update a subscription, and on schedule if `Subscription auto update` is on (off by default) | The URL of your provider | `Use proxy` rule |
| Remote routing profile | When you add or update one, and on schedule if `Routing profiles auto update` is on (off by default) | The URL of the profile. Addresses on `raw.githubusercontent.com` go through the `Remote Rule-set Mirror`. | `Use proxy` rule |
| Routing profile list | When you choose `Routing` → `Download Profiles` → a country | The throneproj/routeprofiles repository on GitHub, through the mirror | `Use proxy` rule |
| Rule-sets | When a profile starts and its routing needs a rule-set (or `Enable AdBlock`) that is not in `cache.db` yet, about once a day while a profile runs, and when you choose `Routing` → `Update Rule-Sets` | GitHub through the `Remote Rule-set Mirror` (`jsDelivr(Cloudflare)` by default), or a `.srs` URL you added | Sent by the core through the default outbound of your routing profile (directly if it is `block`) |
| Location lookup | After every start of a profile, and when you open the `Runtime Stats` tab while a profile runs | `http://ip-api.com/json/` | Always the local proxy port |
| URL test | When you run a URL test or click the status bar, when you open the `Runtime Stats` tab, while an auto selector runs, and after a subscription update if the group's `Run URL test` is on | The `Latency Test URL`, by default `http://cp.cloudflare.com/` | Through each tested profile |
| IP test | Only when you choose `Resolve Selected Out IP` or `Resolve out IP for group` | `https://api.ip2location.io/` | Through each tested profile |
| Speed test | Only when you run a speed test | The Speedtest.net server list and a nearby Speedtest server. In `Simple Download` mode, the `Simple Download URL` (by default `http://cachefly.cachefly.net/1mb.test`). | Through each tested profile |
| Connectivity check | While an auto selector runs, only if you set a `Direct Test URL` or a `Connectivity URL` (both empty by default) | That URL | Direct |
| Domain lookup | Only when you choose `Resolve Domain for group` or `Resolve Selected Domain` | DNS lookups of the domain names of your servers | Your system's DNS resolver |
| Update check | Only when you choose `Tools` → `Check For Update`. The download starts only when you click `Update`. On macOS, in the system-Qt packages and in copies from the Linux install script, this menu item is disabled. | `api.github.com` and the release file on GitHub | `Use proxy` rule |
| WARP registration | Only when you generate a WARP config or identity | `api.cloudflareclient.com`, or the `Registration Domains…` you set | `Use proxy` rule |
| Xray geo files | Only when an Xray config needs `geoip.dat` or `geosite.dat` and you agree to download them, or when you click `Download` | The `GeoIP Asset URL` and `GeoSite Asset URL` (GitHub by default) | `Use proxy` rule |
| Web dashboard | `Tools` → `Open Web dashboard`, only if your build has no built-in dashboard. Official builds have one. | GitHub | Always the local proxy port |
| NTP | Only if you turn on `NTP Settings` | The NTP server you enter | The `outbound` you choose, `direct` by default |

About the location lookup:

- Throne uses it to show the country and city of your connection in the status bar, the window title and the `Runtime Stats` tab.
- It always goes through the local proxy port. With the built-in `Default` routing profile it leaves through your proxy, so ip-api.com sees the address of your proxy, not your own.
- It uses plain HTTP and sends Throne's User-Agent.
- After a start, Throne skips it when the exit of the running profile is an OpenVPN or OpenConnect profile.
- There is no setting to turn it off.

DNS queries for the traffic of your apps go to the servers in `Routing Settings` → `DNS`. See [DNS](@/guides/dns.md).

**Android:** Throne for Android makes the same kinds of requests for subscriptions, routing profiles, rule-sets, tests and WARP registration. With `Settings` → `Subscriptions` → `Use proxy` on, or in `Proxy only` mode, its own requests use the local proxy. While no profile runs, subscription updates and WARP registration fail with "Request with proxy but no profile started.", but update checks, routing profile downloads and the rule-set list still work: they go out directly. Throne for Android does not look up your location after you connect. It checks GitHub for updates only when you tap `Check for updates`, or once a day if you turn on `Check for updates daily` (off by default). `Refresh repository list` on the `Routing` screen downloads the list of routing profiles from GitHub.

## Local proxy port {#local-proxy}

While a profile runs, Throne listens on a local proxy port that accepts SOCKS5 and HTTP connections. By default this is `127.0.0.1:2080`. Only programs on your own computer can reach `127.0.0.1`, but every one of them can use the port without a password.

The settings are in `Settings` → `Basic Settings` → `Common` → `Inbound Settings`:

| Setting | Default | What it does |
| --- | --- | --- |
| `Listen Address` | `127.0.0.1` | `::` or `0.0.0.0` opens the port to other devices. |
| `Listen Port` | `2080` | The port number. |
| `Random port` | Off | Uses a free random port at every start. |
| `Enable Authorization` | Off | Requires the `Inbound Username` and `Inbound Password`. |
| `Disable Mixed Inbound` | Off | Turns the port off. `System Proxy` then cannot be used. |

`Allow other devices to connect` in the `Program` menu and in the tray menu sets `Listen Address` to `::`. Then every device that can reach your computer can use your proxy. Turn on `Enable Authorization` when you do this. See [LAN sharing](@/guides/proxy_modes.md#lan-sharing).

Other local ports:

| Port | Default | Who can reach it |
| --- | --- | --- |
| `DNS Server Port` (`Basic Settings` → `Miscellaneous`) | `5533` | Only this computer (`127.0.0.1`). |
| Clash API (`Basic Settings` → `Core`) | Off (empty `Listen Port`) | The Clash API `Listen Address`, `127.0.0.1` by default. Set a `Secret` when you turn it on. |
| sing-box API / Dashboard (`Basic Settings` → `Core`) | Off (empty `Listen Port`) | Only this computer. A random `Secret` protects it. |

When a profile uses Xray, the core also opens internal ports on `127.0.0.1`, each protected by a random password. Throne and its core talk to each other through a local socket, not through a network port.

**Android:** `Settings` → `Inbound` has the same kind of options: `Proxy port`, `Allow connections from the LAN` (off by default) and `Enable authorization`.

## This website {#website}

This documentation site counts visits with Yandex Metrika. It records page views, the referring page, clicks on the page and on links, and how long visitors stay. Session recording is turned off. The Throne apps do not include this counter.
