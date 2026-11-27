+++
title = "Testing & Auto Selector"
description = "Test profiles and the services they reach, sort, pin and clean up the list, and let the auto selector pick the best profile."
weight = 60
toc = true
+++

Tests do not stop the running profile. They skip auto selectors; test the groups that an auto selector uses instead.

## URL test {#url-test}

The URL test checks that a profile works and measures its latency. Throne requests the `Latency Test URL` through the profile twice and shows how long the second request took.

- **Selected profiles:** right-click them and choose `Test` → `URL test` (`Ctrl+Shift+S`).
- **The whole group:** choose `Groups` → `Test` → `URL test` (`Ctrl+Shift+G`).
- **The running profile:** click its name at the left of the status bar. The result appears in the status bar.

`Test` → `Stop testing` (`Ctrl+.`) stops a running test.

The `Test Result` column shows the latency (green up to 100 ms, yellow up to 300 ms, red above), `Unavailable` when the test failed (the log has a `test error` line with the reason), or `Connect OK` when an OpenVPN or OpenConnect profile connected but the test URL did not answer through it. `Unknown` means your own network was down during the test, so the result says nothing about the profile: it sorts with untested profiles, `Remove unavailable` and automatic clean-up leave it alone, and the next test replaces it.

The settings are in `Settings` → `Basic Settings` → `Testing` → `Latency`.

| Setting | Default | What it does |
| --- | --- | --- |
| `Latency Test URL` | `http://cp.cloudflare.com/` | The address requested through each profile. |
| `Timeout` (next to `Concurrency`) | `3000` ms | The time limit for each request. Too low a value fails profiles with multiplexing, whose first request takes longer. |
| `Concurrency` | `10` | How many profiles are tested at the same time. |
| `Direct Test URL` | empty | An address that works without a proxy on your network. The auto selector fetches it directly to tell a dead Internet connection from dead servers. Empty uses the network state of the operating system. |

## Exit IP test {#ip-test}

This test shows the exit IP address of each profile and its country: the address that websites see. Right-click profiles and choose `Test` → `Exit IP`, or choose `Groups` → `Test` → `Exit IP`. The `Test Result` column then shows the country flag, and the exit IP if `Exit IP` is included (see [Sort and filter](#sort-filter)). The country filter and the auto selector's `Only countries` use this country.

After a profile starts, Throne also shows the country and city of its exit at the bottom left of the window and in the window title. In `Testing` → `Exit Country`, `Look up exit country` turns this off and `Lookup service` chooses the service; `Automatic` starts with IP2Location.io, which the exit IP test also uses. For the services Throne contacts, see [Privacy](@/reference/privacy.md#network-requests).

## Speed test {#speed-test}

The speed test measures the download and upload speed of a profile.

- **Selected profiles:** right-click them and choose `Test` → `Speed test` (`Ctrl+Shift+P`).
- **The whole group:** choose `Groups` → `Test` → `Speed test` (`Ctrl+Alt+P`).
- **The live connection:** while a profile runs, choose `Tools` → `Speed test current connection` (`F6`).

Throne tests the profiles one at a time. The `Test Result` column shows the download speed after `↓` and the upload speed after `↑`, if `Speed` is included.

`Settings` → `Basic Settings` → `Testing` → `Speed Test` → `Speed test mode` chooses what the test does: `Download + upload` (default), `Only download`, `Only upload` or `Simple download`, which fetches the `Simple Download URL` without a server search. The `Timeout` in the same box (default `5000` ms) limits each part of the test.

{% alert_warning() %}
A speed test transfers as much data as it can until the timeout, for every profile. Testing a large group can use a lot of data.
{% end %}

## Service check {#service-check}

A service check shows which services work through a profile, such as AI assistants, streaming and social networks, and what kind of exit IP the profile has. Right-click profiles and choose `Test` → `Service check`, or choose `Groups` → `Test` → `Service check`.

The `Test Result` column then shows a logo for each service with a green, amber or red badge. Hover over a logo for its status (`Available`, `Partial`, `Restricted`, `Blocked`, `Unknown` or `Failed`), and over the cell for the date and the kind of IP: datacenter, mobile, business or residential. To find the profiles on which a service works, type its name in the `Test Result` filter (see [Sort and filter](#sort-filter)).

`Settings` → `Basic Settings` → `Testing` → `Service Check` chooses the services; the others are neither checked nor shown. `Check` on the `Runtime Stats` tab of the main window checks the running profile.

- One run checks at most 100 profiles. Above 20, Throne asks first, because each profile sends about 20 requests to the checked services.
- The list of checks is downloaded at most once a day; see [Privacy](@/reference/privacy.md#network-requests).

## Sort and filter {#sort-filter}

Click a column header to sort by it, and click it again to reverse the order. Sorting by latency puts the fastest profiles first, then failed ones, then untested ones. The group stays sorted, also after tests, subscription updates and imports, until you right-click a column header and choose `Stop sorting`, or drag a row to another place.

Right-click the `Test Result` header to choose what the column shows (`Exit IP`, `Speed`) and what it sorts by (`Latency`, `Download speed`, `Upload speed`, `Exit IP`).

To filter the list, press `Ctrl+F` and type in the field under `Type`, `Address` or `Name`, or in `Filter by country or service...` under `Test Result`. In the `Address` field, `port=443` shows the profiles on port 443 and `port=1000:2000` those on ports 1000 to 2000. Press `Ctrl+F` again to hide and clear the fields.

The `Test Result` field takes country codes from the exit IP test, such as `DE`, and the names or categories of the services of a [service check](#service-check): `gemini` shows the profiles on which Gemini works, and `!netflix` those on which Netflix is refused. All words must match, so `DE gemini` shows the German profiles on which Gemini works.

### Pin profiles {#pin}

Right-click profiles and choose `Pin to top` to keep them above the other profiles of their group, in the order you pinned them. Sorting moves only the unpinned profiles, and a line separates the two. When all selected profiles are pinned, the item reads `Unpin`. Dragging a row among the pinned ones also pins it. Pins stay through subscription updates as long as the profile is still in the subscription.

## Clean up {#clean-up}

`Groups` → `Clean up`, also in the right-click menu of the group's tab, removes profiles from the current group:

| Command | What it removes |
| --- | --- |
| `Remove duplicates` | Exact copies of an earlier profile, including the name. |
| `Remove unavailable` | Profiles whose last test failed. Never the running profile. |
| `Remove invalid` | Profiles that the core rejects as invalid. |
| `Remove insecure profiles` | Profiles without encryption, with TLS that does not check certificates, or with old Shadowsocks ciphers. |

The other commands stop the running profile if they remove it. `Groups` → `Test` → `Clear results` (`Ctrl+Shift+C`) clears only the test results.

To see which profiles count as insecure, turn on `Settings` → `Basic Settings` → `Appearance` → `Profile List` → `Show profile security`: insecure profiles then get a warning sign in the `Type` column.

To clean up automatically, use the group option `Auto clear unavailable profiles`, which deletes failed profiles after every URL test of the group, or the [After each update](@/guides/subscriptions.md#after-update) options of a subscription group, which can also test and sort it.

## Auto selector {#auto-selector}

An auto selector is a profile that picks the best working profile from one or more groups, keeps checking the others, and switches when the current one gets worse or fails. New profiles from a subscription update join it by themselves.

1. Select the tab of the group it should use.
2. Choose `Program` → `New profile` (`Ctrl+N`). The editor opens with `Auto Selector` as the `Type`.
3. Enter a `Name`.
4. In `Profiles from`, check the groups to pick from. The current group is already checked.
5. Click `OK`, then start the new profile like any other.

| Setting | What it does |
| --- | --- |
| `Profiles from` | The groups whose profiles are used. Profiles from all checked groups are ranked together. |
| `Only names matching` | An optional regular expression; only profiles whose name matches are used. It matches anywhere in the name and ignores case: `germany\|nl` uses every name that contains `germany` or `nl`, and `^(?!.*(germany\|🇩🇪)).*$` every name that contains neither `germany` nor 🇩🇪. |
| `Choose` | `Fastest` (default) uses the best measured profile. `In priority order` uses the `Priority tiers`. |
| `Priority tiers` | Shown with `In priority order`. Each row is a `Group` (or `Any group`) with an optional `Names matching` expression. A profile belongs to the first row it matches, and profiles that match none come last. The auto selector uses the highest row that has a working profile and, in it, the best measured one. |
| `Share traffic between the best profiles` | Off (default): one profile carries all traffic and the other ready profiles stand by. On: traffic is spread over the ready profiles. With `Rotate every 30 s` (default), new connections move to the next profile every 30 seconds; with `Per connection`, each new connection may use another profile, so your exit IP can change during a session. |
| `Preferred profile` | Appears after you chose a profile with `Use this profile` in the stats window. `Use automatic` returns the choice to the auto selector. |

Each profile goes through the `Front Proxy` and `Landing Proxy` of its own group, as if you started it on its own; those of the auto selector's group do not apply.

`Advanced ▾` shows more options, each with a working default and a tooltip. The ones most often changed:

| Setting | Default | What it does |
| --- | --- | --- |
| `Only countries` | empty | Country codes such as `DE,NL,FR`. `!` leaves a country out: `!RU,!IR` uses every country except these two. Uses the country found by the [exit IP test](#ip-test), so profiles without one are skipped while this is set. |
| `Run the best` | 300 profiles | How many profiles are loaded into the running config. The auto selector switches between them without reconnecting. |
| `Switch tolerance` | 300 ms | How much faster another profile must be before the auto selector switches to it. |
| `Maximum latency` | no limit | Profiles slower than this are used only when no faster one works. |
| `Drop connections when a profile fails` | on | When the current profile fails, open connections move to the new one at once. Off lets them finish on the failed profile. |
| `Learn from real connections` | off | Also judges profiles by the real connections of your apps and sets aside the ones that keep failing. |

With more usable profiles than `Run the best`, the auto selector first URL-tests those without a recent result (a success counts for 24 hours, a failure for one hour) and loads the best. It starts as soon as a few of them work, finishes the tests in the background and restarts once if the ranking changed. If all running profiles fail, it rebuilds from the next best ones. It pauses while your computer is offline. Its log lines start with `[Auto selector]`.

While an auto selector runs, `Tools` → `Auto Selector Stats` shows the status and latency of each profile. `Use this profile` keeps the selected profile in use, `Back to automatic` lets the ranking choose again, and `Check all now` measures all running profiles at once.

Limits:

- A chain can hold one auto selector as a hop, but not together with an Extra Core profile or a custom config; see [chain limits](@/advanced/chains.md#chain-limits) and [Test a chain](@/advanced/chains.md#test-chain). An auto selector cannot be a `Front Proxy` or `Landing Proxy`.
- It skips chains, other auto selectors, OpenVPN, OpenConnect, Tailscale, Extra Core, sing-box full configs, custom configs that cannot be read, and Xray full configs that cannot be combined with the front or landing proxy of their group.

## On Android {#android}

Throne for Android has the same tests and the same auto selector. The differences:

- **Menus.** On the Profiles screen, the `⋮` menu has `Test` (`URL test`, `IP & country test`, `Speed test`, `Stop testing`), `Remove` and `Sort`. For selected profiles, use `Test` in the selection menu; for one profile, its `⋮` button.
- **Test panel.** A panel shows the progress and results of a test, with actions such as `Sort by latency`, `Remove unavailable` and `Connect to fastest`.
- **Live connection.** While connected, tap the statistics bar to test the connection. Touch and hold it for `Live graphs` and `Speed test current connection`. The bar also shows the exit country; `Settings` → `Testing` has `Look up exit country` and `Lookup service`.
- **Auto selector.** Create it with `Add profile` → `Manual settings` → `Auto selector`. Tap its status line on the Profiles screen to open `Auto selector stats`.
