+++
title = "DNS"
description = "How Throne resolves domain names, what each DNS setting does, when FakeIP helps, and how to read a DNS leak test."
weight = 50
toc = true
+++

Before an app can open a site, a DNS lookup turns the site's name into an IP address. This page explains which DNS server Throne uses for which lookup, what the settings on the `DNS` tab do, and how to read a DNS leak test. The default settings work for most people.

## How DNS works in Throne {#how-dns-works}

Throne has its own DNS resolver inside the core. It uses three DNS servers:

| Server | How queries travel | What it is used for |
| --- | --- | --- |
| `Remote DNS` | Through the proxy | Answers the DNS queries of apps, unless a rule below sends them elsewhere. |
| `Direct DNS` | Directly, without the proxy | Answers queries for domains that your routing profile sends `direct`. Throne also uses it to look up the address of your proxy server, and the address of a site when it connects to that site directly by name. |
| `Local Override` | Directly | Looks up the names of the two servers above, for example `dns.google`. Empty means your system's resolver. |

When an app's query reaches Throne, Throne answers it in this order:

1. `Predefined Answers` and `Respect Hosts File` answer first.
2. With `Enable FakeIP`, address queries get a fake address (see [FakeIP](#fakeip)).
3. With `Enable DNS Routing` (on by default), domains that your routing profile sends `direct` go to Direct DNS. This covers `domain:`, `suffix:`, `keyword:` and `regex:` rules and built-in `geosite-*` rule-sets. It does not cover `geoip-*` rule-sets, IP rules or your own `.srs` files.
4. Everything else goes to the `Default DNS server`, which is `remote` by default. If you set it to `direct`, domains that your routing profile sends to `proxy` still use Remote DNS, under the same conditions as in step 3.

Where the queries come from depends on the mode:

- **TUN mode.** The DNS queries of your apps go into the tunnel and reach Throne. Throne adds a DNS step to every structured routing profile (the `Route DNS` or `dns-hijack` rule in the list does the same), so it answers these queries as described above. A raw routing profile only gets this step if you write it yourself; see [Raw profiles](@/guides/routing.md#raw-profiles).
- **System proxy mode.** Apps that use the proxy send the site's name to Throne. For proxied connections, the proxy server looks the name up. For direct connections, Throne looks it up with Direct DNS. Apps can also look names up themselves with your system's resolver. Those lookups do not pass through Throne.

## Settings {#settings}

Open `Settings` → `Routing Settings` → `DNS`. Changes apply after you click `OK` and restart the connection.

| Setting | Default | What it does |
| --- | --- | --- |
| `Remote DNS` | `https://8.8.8.8/dns-query` | The server used through the proxy. The list also offers `tls://8.8.8.8`, `tls://1.1.1.1`, `8.8.8.8` and `1.1.1.1`. |
| `Direct DNS` | `localhost` | The server used without the proxy. `localhost` means your system's resolver. Keep it unless it does not work; then choose a server that works on your network without the proxy. The list offers public resolvers in China (`223.5.5.5`, `119.29.29.29`), Iran (`178.22.122.100`) and Russia (`77.88.8.8`). |
| `Disable IPv6` (next to each server) | off | Answers IPv6 (AAAA) queries sent to that server with an empty result. |
| `Local Override` | empty | A DNS server used to look up the names of your DNS servers. Set an IP address here when your system's resolver cannot be used. |
| `Default DNS server` | `remote` | The server for queries that no other rule handles: `remote` or `direct`. |
| `Enable DNS Routing` | on | Sends queries for domains that go `direct` to Direct DNS. |
| `Respect Hosts File` | off | Answers A and AAAA queries from your system's hosts file first. Only domains listed in the file are affected. |
| `Predefined Answers` | on | Fixed answers in hosts-file syntax. The default entry is `127.0.0.1 localhost`. |
| `Enable FakeIP` | off | See [FakeIP](#fakeip). |
| `FakeIP Disable IPv6` | off | Hands out no fake IPv6 addresses; AAAA queries get an empty answer. |

`Remote DNS`, `Direct DNS` and `Local Override` accept these formats:

| Format | Example |
| --- | --- |
| Plain DNS | `8.8.8.8` or `8.8.8.8:53` |
| DNS over TCP | `tcp://8.8.8.8:53` |
| DNS over TLS | `tls://1.1.1.1` |
| DNS over HTTPS | `https://1.1.1.1/dns-query` |
| DNS over HTTP/3 | `h3://dns.example.com/dns-query` |
| DNS over QUIC | `quic://dns.example.com` |
| The server your network hands out | `dhcp://auto` |
| Your system's resolver (for `Direct DNS`) | `localhost` |

When the running profile uses Xray and `Remote DNS` is plain DNS or DNS over QUIC, Throne uses DNS over HTTPS instead. For example, `1.1.1.1` becomes `https://1.1.1.1/dns-query`; a server that Throne does not know becomes `https://8.8.8.8/dns-query`.

`Predefined Answers` opens an editor with one entry per line:

```text
127.0.0.1 localhost
10.0.0.5 nas.lan files.lan
```

A domain that has only an IPv4 address in this list gets "no such domain" for IPv6 queries, and the other way round. This way apps cannot go around your entry.

## FakeIP {#fakeip}

With `Enable FakeIP`, Throne answers address queries at once with a fake address from `198.18.0.0/15` (IPv6: `fc00::/18`), without asking a real DNS server. When the app connects to that address, Throne knows which domain it stands for and routes the connection by name. The real lookup happens later: on the proxy server for proxied connections, or with Direct DNS for direct ones.

This has two benefits:

- Connections start faster, because apps do not wait for a real DNS answer.
- No DNS query leaves your device before the connection is routed.

FakeIP only affects queries that reach Throne, so it is useful in TUN mode. It changes nothing for apps in system proxy mode.

Things to know:

- Answers from `Predefined Answers` and the hosts file stay real.
- Apps keep fake addresses in their own caches. After you stop Throne, an app that still holds a fake address cannot connect until it looks the name up again. Restart the app if it stays offline.
- `Advanced Settings` → `Save Cache To File` keeps the fake addresses when Throne restarts.

## Advanced {#advanced}

`Advanced Settings` on the `DNS` tab controls the DNS cache:

| Setting | Default | What it does |
| --- | --- | --- |
| `Cache Capacity` | `65536` | How many answers the cache keeps. |
| `Query Timeout` | `10s` | How long to wait for a DNS server. |
| `Optimistic Cache` | off | Keeps serving an expired answer while it is refreshed in the background. Cannot be combined with `Disable Cache` or `Disable Expire`. |
| `Optimistic Timeout` | `3d` | How long an expired answer may still be served. |
| `Disable Cache` | off | Turns the DNS cache off. |
| `Disable Expire` | off | Keeps cached answers after they expire. |
| `Save Cache To File` | off | Writes cached answers and FakeIP addresses to the core's cache file, so they survive a restart. Each entry costs a disk write. |
| `Reverse Mapping` | off | Remembers which domain an answered IP address belongs to, so domain rules can match connections to that address. |

Durations are a number followed by `ns`, `us`, `ms`, `s`, `m`, `h` or `d`, for example `5s` or `3d`.

`Use Custom DNS Object` replaces everything on this tab with a complete sing-box `dns` object that you write with `Edit DNS Object`. The simple settings and `Advanced Settings` are greyed out while it is on, and features such as DNS routing, FakeIP and predefined answers only work if your object sets them up. In the editor, `Format` tidies the JSON and `Document` shows the address of the [sing-box DNS documentation](https://sing-box.sagernet.org/configuration/dns/).

{% alert_warning() %}
Keep a server with the tag `dns-direct` in a custom DNS object. Throne's routing uses it to look up server addresses.
{% end %}

## DNS leak tests {#leak-tests}

A DNS leak test is a website that shows which DNS servers looked up its test names. The result depends on your mode and your routing profile.

These results are expected:

- **Your Remote DNS provider** (Google with the default setting). Your queries went through Remote DNS and the proxy. This is the normal result for sites you proxy.
- **Your internet provider, for sites that go direct.** Throne looks up domains that go direct with Direct DNS, which is your system's resolver by default and usually belongs to your internet provider. In system proxy mode, or with FakeIP, this also happens for sites that go direct only because the routing profile's default outbound is `direct`, as in the "Proxy … Blocked" profiles. Direct traffic reaches the site without the proxy anyway, so your provider sees it either way.
- **Your internet provider, in system proxy mode.** Browsers and apps can look up names themselves, outside Throne. Use TUN mode if this matters to you.
- **Your browser's own provider,** when the browser uses secure DNS (DNS over HTTPS). Those lookups are ordinary HTTPS connections that follow your routing rules.
- **Your internet provider for most names,** when `Default DNS server` is `direct`.

A real problem looks like this: you use TUN mode and a routing profile that sends the test site through the proxy (for example `Default`), and the test still shows your internet provider. Then some queries go around the tunnel. On Windows, check that `Settings` → `Tun Settings` → `Strict Route` is on (the default on Windows 10 and later), and follow [Windows DNS Leak Protection](@/advanced/windows_tun_mode.md#strict-route).

WebRTC tests check a different thing: your IP address, not your DNS. A WebRTC test that shows no public IP address is fine ([#1267](https://github.com/throneproj/Throne/issues/1267)). If it shows your real public IP address for a site you proxy, UDP traffic went around the proxy. This is common in system proxy mode; use TUN mode instead.

## Hijack and System DNS (deprecated) {#deprecated}

The `Hijack` tab of `Routing Settings` and the Windows `System DNS` option are deprecated in 1.3.1 and will be removed in the next release. Hijack ran a local DNS server that answered chosen domains with fixed addresses, and `System DNS` pointed Windows at that server. Both served apps that ignore the system proxy. `Tun Mode` covers the same use case, so turn them off and use `Tun Mode` instead.

While Hijack is enabled, Throne shows a warning at startup. The `System DNS` checkbox is hidden unless `Basic Settings` → `Style` → `Show System DNS option` is on.

## On Android {#android}

Throne for Android has the same DNS settings in `Settings` → `DNS`. FakeIP is called `Enable FakeDNS` there. In VPN mode, Throne always handles the DNS queries inside the VPN.
