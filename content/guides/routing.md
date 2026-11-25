+++
title = "Routing"
description = "Choose which traffic goes through the proxy, which goes direct and which is blocked, with ready-made profiles or your own rules."
weight = 40
toc = true
+++

Routing decides where each connection goes: through the proxy, direct, or nowhere. The built-in `Default` profile sends everything through the proxy, so you only need this page if you want something else.

## How routing works {#how-routing-works}

A routing profile is a list of rules plus `Everything else goes to`, the outbound for traffic that no rule matches. Throne checks the rules from top to bottom and the first match decides where the connection goes.

| Outbound | Where the traffic goes |
| --- | --- |
| `Proxy` | Through the running profile, and through the WARP exit when it is on. |
| `Direct` | Straight to the internet. |
| `Block` | Nowhere. The connection is refused. |
| `Proxy without exit` | Through the running profile, without the exit. See [Skip the exit](@/advanced/warp.md#warp-bypass). |
| A saved profile | Through that profile instead. Rules only, see [Rules](#advanced-rules). |

`Routing` → `Exit through` adds a last hop to `Proxy` traffic: `Cloudflare WARP` (see [WARP](@/advanced/warp.md)). `Selected profile` adds none.

One routing profile is active at a time. Switch it from the list at the top of the `Routing` menu, or from the tray menu → `Routing: <name>`. A running connection restarts with the new rules. A group can also use its own routing profile, see [Routing profile per group](#group-routing).

## Download ready-made profiles {#download-profiles}

1. Open `Routing` → `Download routing profile` and choose `China`, `Iran` or `Russia`.
2. Keep `Auto update` ticked and click `OK`.
3. Choose one of the new profiles at the top of the `Routing` menu. Downloading alone does not activate it.

| Profile | What it does |
| --- | --- |
| `Bypass China`, `Bypass Iran`, `Bypass Russia` | Proxies everything, except that country's sites and IP addresses and your local network. |
| `Proxy China Blocked`, `Proxy Russia Blocked` | Sends everything direct, except sites blocked in that country. |
| `Proxy Antizapret`, `Proxy Refilter` (Russia) | Sends everything direct, except sites on the Antizapret or Re:filter block list. |

Use a "Bypass" profile if most sites you visit are abroad. A "Proxy … Blocked" profile sends less traffic through your server, but a blocked site that is missing from the list will not load.

The lists are maintained in [throneproj/routeprofiles](https://github.com/throneproj/routeprofiles). If the download fails, choose another `Remote Rule-set Mirror` (see [Rule-sets](#rule-sets)) and try again.

## Routing profiles {#profiles}

Routing profiles are managed on the `Routing` tab of `Settings` → `Routing Settings`, which is also the last item of the `Routing` menu. `Routing` → `Edit current profile` opens the active profile in the editor, and right-clicking a profile in the `Routing` menu opens that one. `Save` in the editor stores the profile at once, and `Cancel` in `Routing Settings` does not undo it. If a connection is running, click `Restart` in the "Settings changed, restart to apply" notice.

There are three kinds:

- **Structured profiles**, edited in Throne with [lists](#simple-rules) and [rules](#advanced-rules). Most people only need these.
- **[Remote profiles](#remote-profiles)**, downloaded from a URL.
- **[Raw profiles](#raw-profiles)**, written as sing-box JSON.

To create a structured profile:

1. On the `Routing` tab, click `New` → `Structured profile`.
2. Enter a `Name` and choose `Everything else goes to`.
3. Add entries to the lists or add rules, and click `Save`.
4. Activate it from the `Routing` menu.

Throne hands DNS lookups to its DNS and sniffs connections by itself, so a new profile starts without rules. A profile's `DNS` tab can give it its own DNS servers, see [DNS per routing profile](@/guides/dns.md#route-dns). Its `Endpoints` tab, shown when you have OpenVPN or OpenConnect profiles, runs them next to the proxy, see [split tunnel](@/advanced/vpn_profiles.md#split-tunnel).

The `Routing` tab also has these settings:

| Setting | What it does |
| --- | --- |
| `Domain Strategy` → `Default Domain Strategy` | IPv4 or IPv6 preference when Throne resolves a server or a site that goes direct. |
| `Domain Strategy` → `Resolve Domain Strategy` | Resolves every domain before the rules run, so IP rules also match domains. |
| `Updates` → `Remote Rule-set Mirror` | Where rule-sets and profiles hosted on GitHub are downloaded from. Default: `jsDelivr(Cloudflare)`. |
| `IP Lists` → `Manage IP lists` | Opens the [IP lists](#ip-lists). |

## Lists {#simple-rules}

A profile has four lists: `Direct`, `Proxy`, `Block` and `Proxy without exit`. On the profile's `Rules` tab they are the rows tagged `Quick list`; select one to edit it. Type an entry and press `Enter` or click `Add`; pasting several lines adds them all. Double-click an entry to edit it.

A line without a prefix is typed by its shape: `example.com` becomes a domain suffix, `10.0.0.0/8` an IP range, `app.exe` a program and a full path a program path. Built-in rule-set names and `.srs` URLs become rule-sets. A prefix says it explicitly:

| Line | Matches |
| --- | --- |
| `domain:example.com` | Only `example.com`. |
| `suffix:example.com` | `example.com` and all its subdomains. |
| `keyword:example` | Every domain that contains `example`. |
| `regex:^cdn[0-9]*\.example\.com$` | Domains that match a regular expression (Go RE2 syntax). |
| `ruleset:geosite-youtube` | Everything in a [rule-set](#rule-sets), by name or by `.srs` URL. |
| `ip:10.0.0.0/8` | An IP range, or a single address such as `1.2.3.4`. |
| `processName:Telegram.exe` | A program, by file name. |
| `processPath:C:\Program Files\App\app.exe` | A program, by full path. |

- Prefixes are case-sensitive: `processName`, not `processname`. A program name without `.exe`, as on Linux and macOS, needs `processName:`.
- A process name must match exactly, including case and `.exe` on Windows. The [Connections tab](#connections-tab) shows the exact name.
- An entry that cannot be used is refused with the reason, for example a URL with `https://` instead of a domain.

{% alert_info() %}
Process rules only see traffic that reaches Throne. In system proxy mode, programs that ignore the proxy never reach it, so use process rules together with `Tun mode`. See [Tun mode](@/guides/tun_mode.md#enable).
{% end %}

**Example: proxy everything except local sites, and block ads.** Set `Everything else goes to` to `Proxy`. In `Direct`:

```text
ruleset:geosite-ir
ruleset:geoip-ir
```

In `Block`:

```text
ruleset:geosite-category-ads-all
```

Replace `ir` with your country code, for example `cn` or `ru`.

**Example: only one program and one site through the proxy.** Set `Everything else goes to` to `Direct`. In `Proxy`:

```text
processName:Telegram.exe
suffix:example.org
```

Each list works like one rule. By default they run in the order `Direct`, `Proxy`, `Block`, `Proxy without exit`, and the first match wins, so an entry in `Proxy` has no effect if a broader entry in `Direct` matches the same traffic. To make an exception, for example to proxy `example.ir` while `geosite-ir` goes direct, add `example.ir` to `Proxy`, then drag the `Proxy` row above the `Direct` row on the `Rules` tab.

## Rules {#advanced-rules}

The `Rules` tab lists every rule of the profile in order. The four lists are rows tagged `Quick list`, and `Everything else` is always last.

- Drag a row to change the order, or use `Alt+Up` and `Alt+Down`, or right-click → `Move to top` or `Move to bottom`.
- Untick a row, or press `Space`, to turn it off without deleting it.
- `Duplicate` and `Delete` act on the selected rule, and the filter box finds rules by name, domain or app.
- A rule with a problem is marked, and the profile cannot be saved until it is fixed.

To add a rule, click `New rule` and enter a `Name`. Under `When`, click `+ Add condition`, choose a condition and fill in its values (`+ Add` adds another value). Under `Then`, choose what happens to matching traffic:

| Then | What it does |
| --- | --- |
| `Proxy`, `Direct`, `Proxy without exit` | Sends it there. |
| `Block` | Refuses it. `Reject with` chooses how. |
| A specific profile | Sends it through a saved profile, shown as `[group] name`. Throne runs it next to the profile you started. |
| `Resolve` | Looks up the IP address of the domain, then continues. |
| `Set route options` | Applies the `Connection options`, then continues. |
| `Bypass` | Linux auto-redirect only. See the [sing-box documentation](https://sing-box.sagernet.org/configuration/route/rule_action/). |

`Hijack DNS` and `Sniff` appear only in rules from older versions, such as the `DNS queries` rule they added to new profiles. Throne does both by itself, so you can delete these rules.

The choices that send traffic somewhere also have `Connection options`. `Fragment TLS` works like the [TLS fragment](@/advanced/presets.md#tls-fragment) setting of a profile, which helps direct connections to sites that a filter blocks by name; `Spoof SNI` works like [TLS spoof](@/advanced/presets.md#tls-spoof).

| Conditions | What they match |
| --- | --- |
| `Domain`, `Domain suffix`, `Domain keyword`, `Domain regex` | The requested domain. |
| `IP range`, `Private IP` | The destination address. |
| `Rule-set` | Rule-set names or `.srs` URLs. |
| `Port`, `Port range` | The destination port, for example `443` or `1000:2000`. |
| `Source IP range`, `Source port` and the like | Where the connection comes from, for example another device on your network. |
| `Process name`, `Process path`, `Process path regex` | The program on this computer. `Choose app` picks one from the running programs and the ones that have used the network. |
| `Network`, `Protocol (sniffed)`, `IP version` | `tcp`, `udp` or `icmp`; a detected protocol such as `tls` or `bittorrent`; `4` or `6`. |
| `Inbound` | `mixed-in` (the proxy port) or `tun-in` (Tun mode). |
| `Wi-Fi name (SSID)`, `Wi-Fi BSSID` | The Wi-Fi network you are connected to. Not available on macOS. |

Each condition is a box that matches when any one of its values matches, and every box must match. The domain, IP and rule-set conditions share one box, as do the two destination port conditions, the source addresses and the source ports. `Invert` makes the rule match what it would otherwise not match. A rule without conditions is an error, because it would catch all traffic. `sing-box JSON` at the bottom shows the rule as the core gets it.

Extra Core profiles, full custom configs and chains that hold an auto selector cannot be the profile of a rule.

## Rule-sets {#rule-sets}

A rule-set is a list of domains or IP ranges in a separate file. Use it as `ruleset:<name>` in a list, or in the `Rule-set` condition of a rule.

- **Built-in names**: more than 2,000. Names starting with `geosite-` hold domains, such as `geosite-youtube` or `geosite-category-ads-all`. Names starting with `geoip-` hold IP ranges, such as `geoip-ir` or `geoip-telegram`. The editor suggests names as you type.
- **Your own files**: the URL of any sing-box binary rule-set. The file name must contain `.srs`.

Rule-sets are downloaded when a profile starts. `Routing` → `Update rule-sets` downloads fresh copies. If GitHub is blocked or slow on your network, change `Routing Settings` → `Routing` → `Updates` → `Remote Rule-set Mirror`. The mirror also applies to the ad list of [Block ads](#adblock) and to routing profiles hosted on GitHub.

## IP lists {#ip-lists}

An IP list is a list of addresses that profiles can use: a group's or a profile's [`Server Address`](@/guides/subscriptions.md#server-address) can take the first address of a list, and a [DNS tunnel](@/advanced/dns_tunnels.md#resolvers) profile can take its resolvers from one. Routing rules do not use them. To manage them, open `Routing Settings` → `Routing` → `IP Lists` → `Manage IP lists`.

Throne comes with `Cloudflare WARP (WireGuard)`, `Cloudflare WARP (MASQUE)`, `Iran DNS resolvers` and `Russia DNS resolvers`. `Import` → `Add default lists` restores them.

- `New` creates a list. Its `Source` is `Manual` (you write the entries) or `URL` (an address that Throne downloads). A `URL` list can update itself with `Auto update`, at most once every 30 minutes.
- Write one entry per line, for example `1.2.3.4`, `1.2.3.0/24`, `1.2.3.4:443`, `[2606:4700::1]:443`, `1.2.3.0/24 443` or `1.2.3.1-1.2.3.9`.

[Find resolvers](@/advanced/dns_tunnels.md#find-resolvers) keeps its results in a list too, named `Resolvers for <profile>`. The WARP scans of older versions became plain lists.

## Remote profiles {#remote-profiles}

A remote profile is a structured profile that Throne downloads from a URL, like the ones from [Download routing profile](#download-profiles). Providers can also share one as a [`throne://remoteroute/` link](@/advanced/deeplinks.md#remoteroute).

To add one, click `New` → `Remote profile` on the `Routing` tab, enter the `URL`, tick `Auto update` and click `Save`. `Preview` shows what the URL holds, and `Fetch now` replaces the rules with it right away. The URL can serve a `throne://route/` link, its Base64 text or the profile's JSON. Raw profiles cannot be remote.

Automatic updates also need `Routing Settings` → `Routing` → `Updates` → `Routing profiles auto update` → `Enable`, which is off by default. To update right away, click `Update` on the `Routing` tab.

{% alert_warning() %}
An update replaces the rules and `Everything else goes to`, so your changes to the profile are lost. To customize a remote profile, `Clone` it and untick `Auto update` in the copy. Rules you disabled and the profile's own DNS settings are kept.
{% end %}

## Routing profile per group {#group-routing}

A group can connect with its own routing profile instead of the one in the `Routing` menu. For example, the servers of one provider can use `Bypass Iran` while all other groups use `Default`.

1. Right-click the group's tab and choose `Edit group`.
2. Choose a `Routing Profile`. `Default (…)` follows the `Routing` menu.
3. Click `OK`.

The group of the profile you start decides. For a chain or an auto selector, that is the group of the chain or the auto selector, not of the profiles in it. The window title and the tray tooltip show the routing profile in use, and the [Connections tab](#connections-tab) changes that profile. A group's routing profile also brings its own [DNS settings](@/guides/dns.md#route-dns), if it has them.

### From the subscription {#subscription-routing}

Some providers send a routing profile with the subscription, in the Happ format. To use it, open the group's settings, tick `Use the subscription's routing profile` under `Subscription`, click `OK` and update the subscription.

Throne saves it as a structured routing profile named by the provider. If the group's `Routing Profile` is `Default (…)`, the new profile becomes the group's routing profile. Every update replaces its rules. DNS settings from the subscription are never used.

- To change it for good, `Clone` it and choose the clone as the group's `Routing Profile`.
- The profile belongs to the group. Deleting the group deletes it.

## Raw profiles {#raw-profiles}

A raw profile is a complete sing-box `route` object in JSON, for features that the rule editor does not offer. Create one with `New` → `Raw profile`.

Outbounds are written as numbers: `-1` is `proxy`, `-2` is `direct`, `-5` is `warp-bypass` (`Proxy without exit`), and a profile ID is that saved profile. The editor suggests your profiles after `"outbound":`. Without `final`, Throne uses `proxy`.

Built-in rule-set names are not defined in raw profiles, and Throne does not add the DNS step that structured profiles get. For Tun mode, start your rules like this:

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

`Prevent modifications` uses the JSON exactly as written, which can break DNS, Xray profiles and chains. `Block ads`, `Enable DNS routing` and the Connections tab actions do not work with raw profiles, and Throne for Android cannot use them.

## Connections tab {#connections-tab}

The `Connections` tab at the bottom of the main window lists open connections grouped by program, with their destination, protocol, outbound and traffic. Hover over the `Outbound` column to see the rule a connection matched; `final` means that no rule matched.

Right-click a connection to change where such traffic goes in the routing profile in use:

- `Direct`, `Proxy` or `Block` lists targets with check boxes: each domain level such as `*.example.com`, the site name as a keyword, the IP address when there is no domain, and the program. A ticked target is added to that list and removed from the other lists; unticking a target removes it.
- `Specific profile` does the same, but sends the targets through a profile you choose.

Then click `Restart` in the "Settings changed, restart to apply" notice. A target joins the existing rule of that list. If the list was empty, its new rule goes to the end, where a broader rule above it can still match first, so check the order on the `Rules` tab.

These actions are not available for raw profiles, for profiles with `Prevent modifications`, for remote profiles with `Auto update`, for profiles updated by a subscription, and while `Routing Settings` is open. To change a remote or subscription profile, clone it first, see [Remote profiles](#remote-profiles) and [From the subscription](#subscription-routing).

If the tab is missing, turn on `Settings` → `Basic Settings` → `Core` → `Statistics` → `Enable connection statistics`.

## Test a route {#route-lookup}

`Routing` → `Route lookup` shows where a connection would go, without making it. Enter a `Process`, a `Domain` or an `IP address`, adjust `Port`, `Network` and `Sniffed protocol` if needed, and click `Test`. The result names the outbound and the rule that decided, with every rule the connection passed on the way.

- While a profile runs, the running configuration is tested. Otherwise choose a `Routing profile`: Throne builds the configuration it would start with, skips endpoint rules and resolves domains with the system resolver.
- `Pick` next to `Process` lists running programs and the ones seen connecting, or lets you browse for a file.

## Block ads {#adblock}

`Routing` → `Block ads` blocks ads in whichever structured or remote profile is active, with the `adblocksingbox` list of the 217heidai/adblockfilters project. It runs before your own rules, so ads are blocked for direct and proxied traffic alike.

If a site stops working, turn `Block ads` off to check whether the list blocks it. To block ads in one profile only, put `ruleset:geosite-category-ads-all` in its `Block` list instead.

## Share profiles {#share-profiles}

Select a profile on the `Routing` tab and click `Export` (`Ctrl+C`) to copy it as a `throne://route/` link.

To import one, click the link, or copy it and press `Ctrl+V` in the main window. This adds the profile without activating it. `Import` (`Ctrl+V`) on the `Routing` tab also selects it, so it becomes active when you click `OK`.

The link carries the name, `Everything else goes to`, the rules (disabled ones included) and the profile's own DNS settings. Rules that send traffic to a saved profile refer to it by name; if the other device has no profile with that name, they use `Proxy`. OpenVPN and OpenConnect endpoints are shared without their credentials. For the link format, see [Deep Links](@/advanced/deeplinks.md#route).

## On Android {#android}

Throne for Android has the same routing profiles, rules and rule-sets. Open `Routing` from the drawer and tap a profile to activate it. The differences:

- **App rules.** The `Apps` field matches Android apps; `Unknown apps` matches connections whose app cannot be found. `Package name regex` matches package names. These rules never match on the desktop.
- **Network rules.** `Network type` matches Wi-Fi, mobile data or Ethernet, and `Metered network` matches metered networks. The desktop leaves these rules out when it imports a link.
- **Wi-Fi rules** need location access set to "Allow all the time", with location turned on.
- **Raw profiles** and the VPN endpoints of imported links are not supported.
- `AdBlock` and `Auto update remote profiles` are in `Settings` → `Routing`.
- If a rule-set cannot be downloaded, `Connect anyway` connects without it. Its rules match nothing until it has been downloaded through the proxy.
