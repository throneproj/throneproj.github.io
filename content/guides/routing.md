+++
title = "Routing"
description = "Choose which traffic goes through the proxy, which goes direct and which is blocked, with ready-made profiles or your own rules."
weight = 40
toc = true
+++

Routing decides where each connection goes: through your proxy, directly to the internet, or nowhere. This page shows how to download a ready-made routing profile for your country, write your own rules, and share profiles. If you want everything to go through the proxy, you do not need to change anything.

## How routing works {#how-routing-works}

A routing profile is a list of rules plus a default outbound. When a connection starts, Throne checks the rules from top to bottom. The first rule that matches decides where the connection goes. If no rule matches, the connection uses the default outbound.

An outbound is a place where traffic can go:

| Outbound | Where the traffic goes |
| --- | --- |
| `proxy` | Through the profile you started. When WARP is on, WARP is added as the last hop. |
| `direct` | Straight to the internet, without the proxy. |
| `block` | Nowhere. The connection is refused. |
| `warp-bypass` | Through the profile you started, but without WARP. When WARP is off, the same as `proxy`. See [WARP](@/advanced/warp.md#warp-bypass). |
| A saved profile | Through that profile instead of the one you started. Only in advanced rules. |

Exactly one routing profile is active at a time. The built-in `Default` profile has only a DNS rule (`Route DNS`) and sends everything to `proxy`.

To change the active routing profile, use one of these:

- The list at the bottom of the `Routing` menu. The active profile has a check mark.
- Tray menu → `Select Routing`.
- `Settings` → `Routing Settings` → `Common` → `Routing Profile`, then `OK`.

Choosing a routing profile in the `Routing` menu or the tray restarts the running connection, so the new rules apply at once. The window title shows the active routing profile when it is not `Default`.

## Download ready-made profiles {#download-profiles}

Throne can download routing profiles that are maintained for China, Iran and Russia.

1. Open the `Routing` menu → `Download Profiles` and choose `China`, `Iran` or `Russia`.
2. Throne lists the profiles it will add ("Add these remote routing profiles?"). Keep `Auto update` ticked and click `OK`.
3. Open the `Routing` menu again and choose one of the new profiles at the bottom. Downloading alone does not change your active profile.

| Country | Profile | What it does |
| --- | --- | --- |
| China | `Bypass China` | Proxies everything except Chinese sites, Chinese IP addresses and your local network, which go direct. Sites on an anti-censorship list always use the proxy. |
| China | `Proxy China Blocked` | Sends everything direct, except sites known to be blocked in China. |
| Iran | `Bypass Iran` | Proxies everything except Iranian sites, Iranian IP addresses and your local network. |
| Russia | `Bypass Russia` | Proxies everything except Russian sites and IP addresses, sites that work only inside Russia, and your local network. |
| Russia | `Proxy Russia Blocked` | Sends everything direct, except sites and IP addresses blocked in Russia. |
| Russia | `Proxy Antizapret` | Sends everything direct, except sites on the Antizapret block list. |
| Russia | `Proxy Refilter` | Sends everything direct, except sites and IP addresses on the Re:filter block list. |

A "Bypass" profile suits you when most sites you visit are abroad. A "Proxy … Blocked" profile sends less traffic through your server, which helps when the server is slow or has a data limit. The downside: a blocked site that is missing from the list does not load.

These profiles are alternatives. Activate the one you want and leave the others; there is no need to delete them. They are [remote profiles](#remote-profiles), so they can update themselves. The lists are maintained in the [throneproj/routeprofiles](https://github.com/throneproj/routeprofiles) repository and can change over time.

If the download fails with "Requesting profile error", choose another `Remote Rule-set Mirror` (see below) and try again.

## Routing profiles {#profiles}

`Settings` → `Routing Settings` (also the first item of the `Routing` menu) opens the Routes window:

| Tab | What it contains |
| --- | --- |
| `Common` | The active routing profile, domain strategies and the rule-set mirror. |
| `Hijack` | Deprecated. Use `Tun Mode` instead; see [DNS](@/guides/dns.md#deprecated). |
| `Warp` | Cloudflare WARP; see [WARP](@/advanced/warp.md#generate). |
| `DNS` | DNS servers and options; see [DNS](@/guides/dns.md#settings). |
| `Route` | Your routing profiles. |

Settings on the `Common` tab:

| Setting | Default | What it does |
| --- | --- | --- |
| `Routing Profile` | `Default` | The active routing profile. |
| `Default Domain Strategy` | empty | IPv4 or IPv6 preference when Throne looks up the address of a server or of a site that goes direct. |
| `Resolve Domain Strategy` | empty | When set, Throne looks up the IP address of every requested domain before the rules run, so IP rules can match domains too. |
| `Remote Rule-set Mirror` | `jsDelivr(Cloudflare)` | Where rule-sets and profiles stored on GitHub are downloaded from. `GitHub` downloads them directly. |

The strategies are `ipv4_only`, `ipv6_only`, `prefer_ipv4` and `prefer_ipv6`. Do not choose `ipv6_only` on a network without IPv6.

Buttons on the `Route` tab:

| Button | What it does |
| --- | --- |
| `New` | Creates a `Structured profile`, a `Raw profile` or a `Remote profile`. |
| `Clone` | Copies the selected profile. |
| `Export` | Copies the selected profile as a `throne://route/` link (`Ctrl+C`). |
| `Import` | Adds a profile from the clipboard (`Ctrl+V`). |
| `Edit` | Opens the selected profile. Double-clicking it does the same. |
| `Delete` | Deletes the selected profile (`Del`). The last profile cannot be deleted. |
| `Update` | `Update selected` or `Update all` downloads remote profiles again. |

Changes in the Routes window are saved when you click `OK`. If a connection is running, the main window then shows "Settings changed, restart to apply". Click `Restart` there to use the new rules.

There are three kinds of routing profiles: structured profiles, which you edit in Throne with [simple rules](#simple-rules) and [advanced rules](#advanced-rules); [remote profiles](#remote-profiles), which are downloaded from a URL; and [raw profiles](#raw-profiles), written as sing-box JSON. Most people only need structured ones.

To create a structured profile:

1. On the `Route` tab, click `New` → `Structured profile`.
2. Enter a `Name` and choose the `Default outbound`.
3. Add rules on the `Basic` tab or the `Advanced` tab.
4. Click `OK`. On the `Common` tab, choose the profile as `Routing Profile`, then click `OK`.

A new profile starts with a `dns-hijack` rule. Throne adds the same DNS step to every structured profile anyway (see [DNS](@/guides/dns.md#how-dns-works)), so you can leave the rule as it is.

The `Endpoints` tab appears when you have OpenVPN or OpenConnect profiles. It runs them next to your proxy for the networks they announce; see [split tunnel](@/advanced/vpn_profiles.md#split-tunnel).

## Simple rules {#simple-rules}

The `Basic` tab of a profile has four boxes: `Direct`, `Proxy`, `Block` and `Warp-bypass`. Each line in a box sends matching traffic there. `How to use` shows a short summary of the syntax.

| Line | Matches |
| --- | --- |
| `domain:example.com` | Only `example.com`. |
| `suffix:example.com` | `example.com` and all its subdomains, such as `www.example.com`. |
| `keyword:example` | Every domain that contains `example`. |
| `regex:^cdn[0-9]*\.example\.com$` | Domains that match a regular expression (Go RE2 syntax). |
| `ruleset:geosite-youtube` | Everything in a [rule-set](#rule-sets): a built-in name or the URL of an `.srs` file. |
| `ip:10.0.0.0/8` | IP addresses in a range. A single address such as `1.2.3.4` also works. |
| `processName:Telegram.exe` | Connections of a program, by file name. |
| `processPath:C:\Program Files\App\app.exe` | Connections of a program, by full path. |

Rules for writing lines:

- Write one entry per line. Empty lines are ignored.
- Write the prefix exactly as shown, including upper and lower case (`processName`, not `processname`).
- `domain:`, `suffix:` and `keyword:` values are saved in lower case.
- A process name must match exactly, including upper and lower case and `.exe` on Windows. The [Connections tab](#connections-tab) shows the exact name.
- Throne checks the lines when you switch tabs or click `OK`, and lists the lines it cannot use under "Some rules could not be added". Switching tabs drops those lines. `OK` does not save until you fix them.

{% alert_info() %}
Process rules only see traffic that reaches Throne. In system proxy mode, programs that ignore the proxy never reach it, so use process rules together with `Tun Mode`. See [TUN Mode](@/guides/tun_mode.md#enable).
{% end %}

**Example 1: proxy everything except local sites, and block ads.** Set `Default outbound` to `proxy`. In `Direct`:

```text
suffix:example.com
ruleset:geosite-ir
ruleset:geoip-ir
```

In `Block`:

```text
ruleset:geosite-category-ads-all
```

Replace `ir` with your country code, for example `cn` or `ru`.

**Example 2: only one program and one site through the proxy.** Set `Default outbound` to `direct`. In `Proxy`:

```text
processName:Telegram.exe
suffix:example.org
```

### Order of simple rules {#simple-rules-order}

Each box becomes ordinary rules on the `Advanced` tab, named after the box, such as `Simple Address Bypass` (addresses in `Direct`) or `Simple Process Name Proxy` (programs in `Proxy`). In a new profile they are added in this order: `Direct`, `Block`, `Proxy`, `Warp-bypass`. Because the first match wins, a line in `Proxy` has no effect when a broader line in `Direct` already matches the same traffic.

To make an exception, move it up on the `Advanced` tab. For example, to proxy `example.ir` in a profile that sends `geosite-ir` direct:

1. Add `suffix:example.ir` to the `Proxy` box.
2. Open the `Advanced` tab and select `Simple Address Proxy`.
3. Click `Move Up` until it is above the rule that contains `geosite-ir`.

## Advanced rules {#advanced-rules}

The `Advanced` tab shows every rule of the profile in order, with `New`, `Move Up`, `Move Down` and `Delete`. The right side shows the rule's `Name` and a `Preview` of the rule in sing-box JSON.

To add a rule:

1. Click `New`.
2. Choose an `Action`.
3. Open the `+` tab and tick the attributes you need. Each attribute becomes a tab. Unticking an attribute clears its value.
4. Fill in the tabs. Lists take one entry per line.

| Action | What it does |
| --- | --- |
| `route` | Sends matching traffic to the rule's `outbound`: `proxy`, `direct`, `warp-bypass` or a saved profile. A new rule sends to `direct` until you tick `outbound` and choose another one. |
| `reject` | Blocks matching traffic. `method` and `no_drop` change how. |
| `hijack-dns` | Answers DNS queries with Throne's DNS. |
| `route-options` | Sets options such as `override_address`, `override_port` or `tls_spoof`, then continues with the next rules. |
| `sniff` | Detects the protocol and the domain of a connection, then continues. |
| `resolve` | Looks up the IP address of the domain (with `strategy`), then continues. |
| `bypass` | Linux only, for advanced setups. See the [sing-box documentation](https://sing-box.sagernet.org/configuration/route/rule_action/). |

To block traffic in an advanced rule, use `reject`. The name `block` exists only as a default outbound and as the `Block` box.

| Attributes | What they match |
| --- | --- |
| `domain`, `domain_suffix`, `domain_keyword`, `domain_regex` | The requested domain. |
| `ip_cidr`, `ip_is_private` | The destination address; `ip_is_private` covers private and local ranges. |
| `rule_set` | Built-in rule-set names or `.srs` URLs. |
| `port`, `port_range` | The destination port, for example `443` or `1000:2000`. |
| `source_ip_cidr`, `source_ip_is_private`, `source_port`, `source_port_range` | Where the connection comes from, for example another device on your network. |
| `process_name`, `process_path`, `process_path_regex` | The program on this computer. |
| `network`, `protocol`, `ip_version` | `tcp`, `udp` or `icmp`; a detected protocol such as `tls`, `quic` or `bittorrent`; `4` or `6`. |
| `inbound` | Where the connection entered Throne: `mixed-in` (the proxy port) or `tun-in` (TUN mode). |
| `wifi_ssid`, `wifi_bssid` | The Wi-Fi network you are connected to. Not available on macOS. |
| `package_name` | Android apps. On the desktop, a rule with this attribute never matches. |
| `invert` | `true` makes the rule match when its conditions do not match. |

Inside one rule, the domain, IP and `rule_set` attributes match when any one of them matches. Other attributes, such as `port` or `process_name`, must match as well.

Tips:

- **Exceptions go first.** Put a rule for one site above the rule for the whole country or list.
- **Process rules** only see programs whose traffic reaches Throne. Use TUN mode to include programs that ignore the system proxy; see the note under [Simple rules](#simple-rules).
- **Send traffic to a specific server.** Tick `outbound` and choose a saved profile, shown as `[group] name`. Throne runs that profile next to the one you started. Extra Core profiles and full custom configs cannot be used here.
- **Rules you cannot edit.** A rule named "… route prefer" belongs to the `Endpoints` tab. You can only move it.

## Rule-sets {#rule-sets}

A rule-set is a list of domains or IP ranges stored in a separate file. Use it in a simple rule (`ruleset:<name>`) or in the `rule_set` attribute of an advanced rule.

- **Built-in names.** Throne knows more than 2,000 rule-sets by name. Names that start with `geosite-` hold domains, for example `geosite-youtube`, `geosite-cn` or `geosite-category-ads-all`. Names that start with `geoip-` hold IP ranges, for example `geoip-ir`, `geoip-telegram` or `geoip-private`. When you type `ruleset:` in a simple-rule box, or in the `rule_set` tab, Throne suggests matching names.
- **Your own files.** The URL of any sing-box binary rule-set works, for example `ruleset:https://example.com/lists/my-sites.srs`. The file name in the URL must contain `.srs`.

Throne downloads the rule-sets of a profile when the profile starts and keeps them in the core's cache. `Routing` → `Update Rule-Sets` downloads fresh copies. It is available while a connection runs and reports how many rule-sets it refreshed.

Built-in rule-sets are stored on GitHub. If GitHub is blocked or slow on your network, change `Routing Settings` → `Common` → `Remote Rule-set Mirror`. The mirror also applies to the AdBlock list and to routing profiles stored on GitHub. Your own `.srs` URLs are always used as written.

## Remote profiles {#remote-profiles}

A remote profile is a structured profile that Throne downloads from a URL. The profiles from [Download Profiles](#download-profiles) are remote profiles. A provider can also give you one with a [`throne://remoteroute/` link](@/advanced/deeplinks.md#remoteroute).

To add one yourself:

1. On the `Route` tab, click `New` → `Remote profile`.
2. Enter a `Name` and the `URL`. The address can serve a `throne://route/` link, its Base64 text, or the profile's JSON.
3. Click `Preview` to look at the profile without changing anything, or `Fetch` to load its rules now.
4. Tick `Auto update` to keep the profile up to date, then click `OK`.

The URL must serve a structured profile. Raw profiles cannot be remote profiles.

Automatic updates need two things: the profile's `Auto update` box, and `Settings` → `Basic Settings` → `Subscription` → `Routing profiles auto update`. The second one is off by default. Its interval is in minutes (default 1440, once a day); values under 30 turn it off. The `Runtime Stats` tab shows `Next remote route update`. To update at once, use `Update` on the `Route` tab.

An update replaces the rules and the default outbound with the downloaded ones, so your own changes to the profile are lost. To change a remote profile safely, `Clone` it, open the copy and untick `Auto update`. An update does not restart a running connection: the new rules are used the next time you start a profile.

## Raw profiles {#raw-profiles}

A raw profile is a complete sing-box `route` object in JSON. Use it when you need sing-box features that the rule editor does not offer.

On the `Route` tab, click `New` → `Raw profile`. The editor checks the JSON and has a `Format JSON` button. Outbounds are written as numbers:

| Number | Outbound |
| --- | --- |
| `-1` | `proxy` |
| `-2` | `direct` |
| `-5` | `warp-bypass` |
| A profile ID | A saved profile. After `"outbound":` or `"final":`, the editor suggests your profiles by name and inserts the number. |

If `final` is missing, Throne uses `proxy`. Built-in rule-set names are not defined for you: add your own `rule_set` entries to the JSON. Throne also does not add the DNS step that structured profiles get automatically. For TUN mode, start your rules like this:

```json
{
  "rules": [
    { "action": "sniff" },
    { "protocol": "dns", "action": "hijack-dns" },
    { "domain_suffix": ["example.com"], "outbound": -2 }
  ],
  "final": -1
}
```

`Prevent modifications` uses the object exactly as written; Throne only turns the outbound numbers into tags. Throne then adds nothing of its own, so DNS, Xray profiles, chains and other features may stop working. Use it only if you know sing-box well.

`Enable AdBlock`, `Enable DNS Routing` and the `Append` actions of the Connections tab do not work with raw profiles. Throne for Android cannot use raw profiles.

## Connections tab {#connections-tab}

The `Connections` tab at the bottom of the main window lists open connections, grouped by program. For each connection it shows the destination, the protocol, the outbound it used and its traffic. It is the quickest way to see where a site goes and to add a rule for it.

Right-click a connection:

| Menu item | What it does |
| --- | --- |
| `Append "<host>" to` → `Direct` / `Proxy` / `Block` | Adds `suffix:<host>` to that box of the active routing profile. For an IP address it adds `ip:<address>`. |
| `Append process "<name>" to` → `Direct` / `Proxy` / `Block` | Adds `processName:<name>` to that box. |
| `Copy Destination`, `Copy Process Name` | Copies the value. |
| `Close connection` | Closes the connection. |

After you add a rule, click `Restart` in the "Settings changed, restart to apply" notice. The new line joins the existing simple rule of that box. If the box was empty, its rule is added at the end of the list, where a broader rule above it can still match first. Check the order on the `Advanced` tab.

The `Append` items are disabled when the active routing profile is raw, is locked with `Prevent modifications`, or is a remote profile with `Auto update` on. Hover over the item to see the reason. For a remote profile, clone it first as described in [Remote profiles](#remote-profiles).

The tab needs `Settings` → `Basic Settings` → `Style` → `Connection statistics` → `Enable`, which is on by default.

## AdBlock {#adblock}

`Routing` → `Enable AdBlock` blocks ads in whichever routing profile is active. Throne adds a block rule for a public ad-blocking rule-set (`adblocksingbox` from the 217heidai/adblockfilters project). The rule runs before your own `route` rules, so ads are blocked for direct and proxied traffic alike. Turning AdBlock on or off restarts the running connection.

- AdBlock works with structured and remote profiles, not with raw profiles.
- If a site stops working, turn AdBlock off to check whether the list blocks it.
- To block ads in one profile only, put `ruleset:geosite-category-ads-all` in its `Block` box instead.

## Share profiles {#share-profiles}

To share a routing profile, select it on the `Route` tab and click `Export` (or press `Ctrl+C` in the list). Throne copies a `throne://route/` link. Send the link to anyone.

To import a profile:

- **In Routing Settings.** Copy the link, open the `Route` tab and click `Import` (or press `Ctrl+V` in the list). Throne asks "Import routing profile … from the clipboard?". If the clipboard holds no profile, a box opens where you can paste a Throne route link, a remote route link, Base64 text or a JSON rule array. The imported profile is also selected on the `Common` tab, so it becomes active when you click `OK`.
- **From anywhere.** Click the link, or copy it and press `Ctrl+V` in the main window. Throne asks "Add this routing profile?" and adds it without making it active.

What the link carries:

- The name, the default outbound and the rules.
- Rules that send traffic to a saved profile refer to it by name. On the other computer, Throne uses a profile with the same name, or `proxy` if there is none, and tells you.
- VPN endpoints, shared without their credentials. When you import such a link, Throne creates the OpenVPN or OpenConnect profiles before it asks "Add this routing profile?", and keeps them if you cancel.

For the link format, see [Deep Links](@/advanced/deeplinks.md#route).

## On Android {#android}

Throne for Android has the same routing profiles, rules and rule-sets. Open `Routing` from the drawer; tap a profile to make it active. The differences:

- **App rules.** The rule editor has an `Apps` field that matches Android apps. The desktop cannot see Android apps, so there a rule with an app condition never matches. Android shows a note when you export a profile with such rules.
- **Wi-Fi rules.** `Wi-Fi SSID` and `Wi-Fi BSSID` need precise location access set to "Allow all the time", and location turned on, because Android hides the Wi-Fi name otherwise. Throne asks when you save such a rule. If access is missing, the notification "Wi-Fi rules are inactive" appears.
- **Raw profiles.** Android refuses raw `throne://route/` links ("raw routing profiles are not supported on Android"). Raw profiles from a desktop backup are kept but cannot be used ("Raw (Throne desktop) · read-only").
- **VPN endpoints** in an imported link are dropped with a warning.
- **Quick switch.** On the Profiles screen, the menu (⋮) → `Routing profile` lists your routing profiles. The same dialog has an `Enable WARP` / `Disable WARP` button.
- **Links.** A `throne://route/` link adds the profile but does not make it active.

`Download profiles`, `Update rule-sets` and remote profiles work as on the desktop. `AdBlock` and `Auto update remote profiles` are in `Settings` → `Routing`.
