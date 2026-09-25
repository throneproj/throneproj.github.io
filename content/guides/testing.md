+++
title = "Testing & Auto Selector"
description = "Test profiles for latency, exit IP and speed, sort and filter the list, remove dead profiles, and let the auto selector pick the best server."
weight = 60
toc = true
+++

Throne can test your profiles and help you keep only the good ones. This page covers the URL test, the IP and country test and the speed test, sorting and filtering, cleaning up, and the auto selector, which picks the best server for you.

Tests do not stop the running profile. They skip auto selector profiles; test the group that the auto selector uses instead.

## URL test {#url-test}

The URL test checks that a profile works and measures its latency. Throne requests the `Latency Test URL` through the profile two times and shows how long the second request took, in milliseconds.

To start a URL test:

- **Selected profiles:** right-click them and choose `Url Test Selected` (`Ctrl+Shift+S`).
- **The whole group:** choose `Groups` → `Url Test Group` (`Ctrl+Shift+G`), or right-click the group tab and choose `Url Test selected Group`.
- **The running profile:** click the profile name at the left of the status bar. Throne tests the live connection once and shows `Test Result:` with the time, or `Unavailable`, in the status bar.

While a test runs, `Stop Testing` (`Ctrl+.`) appears in the right-click menu and in the `Groups` menu.

The `Test Result` column shows one of these:

| Result | Meaning |
| --- | --- |
| A time such as `85 ms` | The profile works. The time is green up to 100 ms, yellow up to 300 ms and red above that. |
| `Unavailable` | The test failed. The log has a line with `test error` and the reason. |
| `Connect OK` | An OpenVPN or OpenConnect profile connected, but the test URL did not answer through it. |

The test settings are in `Settings` → `Basic Settings` → `Common`, under `Testing`:

| Setting | Default | What it does |
| --- | --- | --- |
| `Latency Test URL` | `http://cp.cloudflare.com/` | The address that Throne requests through each profile. |
| `Timeout` (next to `Concurrency`) | `3000` ms | The time limit for each request. Do not set it too low: profiles with multiplexing need more time for their first request, and a short timeout marks them as failed. |
| `Concurrency` | `10` | How many profiles are tested at the same time. |
| `Direct Test URL` | empty | Fetched without any proxy, so that the auto selector can tell a dead Internet connection from dead servers. Use an address that works on your network without a proxy. Empty means that Throne uses the network state of the operating system. |

To copy the results of selected profiles, right-click them and choose `Share` → `Copy Test Result`.

## IP and country test {#ip-test}

This test shows the exit IP address of each profile and its country. This is the address that websites see.

- **Selected profiles:** right-click them and choose `Resolve Selected Out IP`.
- **The whole group:** choose `Groups` → `Resolve out IP for group`.

Throne requests `https://api.ip2location.io/` through each profile. The `Test Result` column then shows the country flag, and the exit IP if `Out IP` is included (see [Sort and filter](#sort-filter)). The test uses the `Timeout` and `Concurrency` of the URL test.

The country is used by the country filter and by the auto selector's `Only countries` option. For the services that Throne contacts, see [Privacy](@/reference/privacy.md#network-requests).

## Speed test {#speed-test}

The speed test measures the download and upload speed of a profile.

- **Selected profiles:** right-click them and choose `Speedtest Selected` (`Ctrl+Shift+P`).
- **The whole group:** choose `Groups` → `Speedtest Group` (`Ctrl+Alt+P`), or right-click the group tab and choose `Speed Test selected Group`.
- **The live connection:** while a profile runs, choose `Tools` → `Speedtest Current` (`F6`).

Throne tests the profiles one at a time. The `Test Result` column then shows the download speed after `↓` and the upload speed after `↑`, if `Speed` is included.

Choose what the test does in `Settings` → `Basic Settings` → `Common` → `Speedtest mode`:

| Mode | What it does |
| --- | --- |
| `Download + Upload` (default) | Finds a nearby Speedtest server, then measures download and upload. |
| `Only Download` | Measures download only. |
| `Only Upload` | Measures upload only. |
| `Simple Download` | Downloads the file at `Simple Download URL`, by default `http://cachefly.cachefly.net/1mb.test`. No server search. |
| `Only Country` | Only finds the nearest Speedtest server and shows its country. It is fast, uses almost no data and tests many profiles at the same time. |

The `Timeout` next to `Speedtest mode` (default `5000` ms) limits each part of the test.

{% alert_warning() %}
A speed test transfers as much data as it can until the timeout, for every profile. Testing a large group can use a lot of data, which matters if your plan has a data limit. The data counts in the `Traffic` column of each profile.
{% end %}

## Sort and filter {#sort-filter}

To sort the profiles of a group:

- Click a column header to sort by that column. Click it again to reverse the order. Throne saves the new order.
- When you sort by latency with the first click, the fastest profiles come first. Failed profiles follow, and untested profiles come last.
- Right-click the `Test Result` header to choose what the column shows (`Include:` `Out IP`, `Speed`) and what it sorts by (`Sort By:` `Latency`, `Download Speed`, `Upload Speed`, `IP Out`).
- Right-click the `Traffic` header to sort by `Total`, `Downloaded` or `Uploaded`.
- Drag rows to put them in any order. This does not work while the filter is on.

A subscription update puts the profiles back in the provider's order. To sort a subscription group after each update, use its `Sort by latency` option; see [After each update](@/guides/subscriptions.md#after-update).

To filter the list:

1. Press `Ctrl+F`, or click the filter button at the right end of the group tab bar.
2. Type in the field under the `Type`, `Address` or `Name` header, or in `Filter by country...` under `Test Result`.

The list then shows only the profiles that contain the text; case does not matter. In the `Address` field, `port=443` shows the profiles on port 443, and `port=1000:2000` the profiles on a port from 1000 to 2000. One end of the range can be empty, for example `port=8000:`. The country field matches the country code from the IP or speed test, for example `DE`. Press `Ctrl+F` again to hide the fields; this also clears them.

## Clean up {#clean-up}

These commands are in the `Groups` menu. They work on the current group.

| Command | Shortcut | What it removes |
| --- | --- | --- |
| `Remove Duplicates` | `Ctrl+Shift+D` | Profiles that are exact copies of an earlier profile, including the name. The first copy stays. |
| `Remove Unavailable` | `Ctrl+Shift+R` | Profiles whose last test failed. It never removes the running profile. |
| `Remove Invalid` | `Ctrl+Alt+I` | Profiles that the core rejects as invalid. |
| `Remove Insecure Configs` | – | Profiles whose traffic is not properly protected: no encryption, TLS without certificate checks, or old Shadowsocks ciphers. |
| `Clear Group test result` | `Ctrl+Shift+C` | Only the test results. The profiles stay. |

Throne asks before it deletes anything, unless `Settings` → `Basic Settings` → `Style` → `Skip confirmation When Deleting Profiles` is on. If `Remove Duplicates`, `Remove Invalid` or `Remove Insecure Configs` removes the running profile, Throne stops it.

To see which profiles count as insecure, turn on `Settings` → `Basic Settings` → `Style` → `Show Config Security`. The `Type` column then shows the security of each profile, and insecure profiles get a warning sign.

To clean up automatically:

- The group option `Auto Clear Unavailable Profiles` deletes failed profiles after every URL test of the group, without asking. See [Group options](@/guides/subscriptions.md#group-options).
- A subscription group can remove duplicate, insecure, invalid and failed profiles after each update. See [After each update](@/guides/subscriptions.md#after-update).

## Auto selector {#auto-selector}

An auto selector is a special profile. When you start it, it picks the best working profile from one group, keeps checking the others, and switches when the current one gets worse or fails. New servers from a subscription update join it by themselves.

To create one:

1. Select the tab of the group that it should use.
2. Choose `Program` → `New profile` (`Ctrl+N`). The editor opens with `Auto Selector` already chosen as the `Type`.
3. Enter a `Name`.
4. Check `Servers from`. It is the group that the auto selector picks from.
5. Click `OK`, then start the new profile like any other profile.

The editor shows a summary of what will happen, for example how many profiles of the group can be used. The basic options are:

| Setting | Default | What it does |
| --- | --- | --- |
| `Servers from` | the current group | The group whose profiles the auto selector uses. |
| `Only names matching` | empty | An optional regular expression. Only profiles whose name matches are used, for example to pick one country or provider. Case does not matter. |
| `Share traffic between the best profiles` | off | Off: one profile carries all traffic, and the other ready profiles stand by. On: traffic is spread over the working profiles; see `Load balancing` below. |
| `Preferred profile` | – | Appears only after you chose a profile with `Use this profile` in the stats window. `Use automatic` returns the choice to the auto selector. |

`Advanced…` shows more options, in the parts `Which profiles to use`, `Health checks`, `Switching`, `Load balancing` and `Test endpoints`. All of them have working defaults.

| Setting | Default | What it does |
| --- | --- | --- |
| `Only countries` | empty | Country codes separated by commas, for example `DE,NL,FR`. Uses the country from the IP test, so profiles that were never IP-tested are skipped while this is set. |
| `Run the best` | 300 profiles | How many profiles are loaded into the running config. The auto selector switches between them without reconnecting. |
| `Rank at most` | 1000 profiles | How many profiles are measured and kept in the ranked list. Replacements come from this list. |
| `Trust results for` | 1440 min | URL test results this recent are reused instead of testing again. 0 means always test again. |
| `Skip failed profiles` | on | Leaves out profiles whose last test failed, while that result is still trusted. |
| `Keep ready` | 3 profiles | How many profiles are kept confirmed working, so that a failure is covered at once. |
| `Check closely` | 8 profiles | How many of the best profiles are checked at every `Check interval`. |
| `Check interval` | 300 s | How often the closely checked profiles are measured. |
| `Full sweep every` | 600 s | How long one pass over all running profiles takes. |
| `Watch profile in use` | 15 s | How often the profile that carries your traffic is checked on its own. |
| `Samples kept` | 10 | How many recent checks the ranking uses for average latency and jitter. |
| `Switch tolerance` | 300 ms | Another profile must be at least this much faster before the auto selector switches to it. |
| `Maximum latency` | no limit | Profiles slower than this are never chosen. |
| `Failover attempts` | 2 | When the chosen profile fails to connect, how many others are tried at once before the app sees an error. |
| `Drop connections on switch` | on | On: after a switch caused by a problem, all connections move to the new profile at once. Off: open downloads finish on the old profile. |
| `Mode` (load balancing) | `Rotate on a timer (keeps sessions stable)` | Used with `Share traffic between the best profiles`. The other mode is `Per connection (widest spread)`, where every new connection can take a different profile and your exit IP can change during a session. |
| `Rotate every` | 30 s | For the timer mode: how long the auto selector stays on one profile before new connections move to the next. |
| `Test URL` | empty | The address used to measure profiles. Empty means the global `Latency Test URL`. |
| `Connectivity URL` | empty | Fetched without the proxy to notice when your Internet connection is down. Empty means the `Direct Test URL` from the test settings. |

How it runs:

- Before it starts, it URL-tests the profiles that have no result newer than `Trust results for` and ranks them. Then it loads the best of them, as many as `Run the best`, into the running config. The log shows lines that start with `[Auto selector]`.
- If all running profiles stop working for 20 seconds, it rebuilds from the next best profiles. It waits longer between repeated rebuilds, from 60 seconds up to 10 minutes.
- If your computer has no network connection, the checks pause until it comes back.

While an auto selector runs, `Tools` → `Auto Selector Stats` opens its stats window. The table shows each profile with `Profile`, `Status` (`Working`, `Unstable`, `Not checked`, `Failing` or `Paused`), `Latency`, `Jitter`, `Checks`, `Connects`, `Last OK` and `Notes`. `Only show profiles with problems` hides the working ones. The buttons are:

- `Use this profile`: keep the selected profile in use instead of the ranking's choice.
- `Back to automatic`: let the ranking choose again.
- `Check all now`: measure all running profiles now.

Limits:

- An auto selector cannot be a hop in a chain, or the `Front Proxy` or `Landing Proxy` of a group.
- It skips these profiles of the group: chains and other auto selectors, OpenVPN and OpenConnect, Tailscale, Extra Core, custom sing-box full configs, and custom configs that cannot be read. Xray full configs are skipped when they cannot be combined with the group's front or landing proxy.

## On Android {#android}

Throne for Android has the same tests and the same auto selector.

- On the Profiles screen, the `⋮` menu has `URL test`, `IP & country test`, `Speed test`, `Speed test current connection` and `Stop testing` for the current group. It also has `Clear test results`, `Remove` (`Duplicates`, `Unavailable`, `Invalid`, `Insecure configs`) and `Sort`. For selected profiles, use `Test` in the selection menu.
- Before a speed test of more than one profile, the app asks for confirmation: "Speed testing can use significant data."
- A test panel shows the progress, the counts `Working`, `Failed`, `Pending` and `Skipped`, a latency chart (≤100 ms, ≤300 ms, >300 ms, fail), the fastest profile, the countries and the number of distinct exit IPs. It also offers actions such as `Sort by latency` or `Sort by speed`, `Remove unavailable` (with the number of failed profiles), `Connect to fastest` (`Select fastest` when you are not connected) and `Dismiss test results`.
- While connected, tap the statistics bar ("Connected, tap to check connection") to test the live connection. The result looks like "Success: HTTP handshake took 120ms" or "Failed: …".
- To create an auto selector, choose `Add profile` → `Manual settings` → `Auto selector`. The options and defaults are the same as on desktop, written in sentence case, for example `Servers from`, `Only names matching` and `Run the best`. Tap the auto selector's status line on the Profiles screen to open `Auto selector stats`, with `Use this profile`, `Back to automatic` and `Check all now`.
