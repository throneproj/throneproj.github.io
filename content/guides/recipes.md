+++
title = "Recipes"
description = "Step-by-step setups for common tasks: proxy only blocked sites, share the proxy, hotspot, calls and games, VMs, a corporate VPN and per-app routing."
weight = 80
toc = true
+++

This page gives short, step-by-step setups for common tasks. Each recipe links to the pages that explain the features in detail.

## Proxy only blocked sites {#proxy-only-blocked-sites}

Send only blocked sites through the proxy and everything else directly. Local sites stay fast, and your server carries less traffic.

**With a ready-made profile (China, Russia):**

1. Open the `Routing` menu → `Download Profiles` and choose `China` or `Russia`.
2. Keep `Auto update` ticked and click `OK`.
3. Open the `Routing` menu again and choose `Proxy China Blocked`, or for Russia `Proxy Russia Blocked`, `Proxy Antizapret` or `Proxy Refilter`.

**With your own list (any country):**

1. Open `Settings` → `Routing Settings` → `Route` and click `New` → `Structured profile`.
2. Enter a `Name`, for example `Blocked sites`, and set `Default outbound` to `direct`.
3. On the `Basic` tab, write the sites in the `Proxy` box, one per line (see the example below).
4. Click `OK`. On the `Common` tab, choose `Blocked sites` as `Routing Profile` and click `OK`.

```text
ruleset:geosite-youtube
ruleset:geosite-telegram
ruleset:geoip-telegram
suffix:example.com
```

If a blocked site still does not load, it uses more domains than you listed. Open the site, find its connections in the `Connections` tab, right-click one and choose `Append "<host>" to` → `Proxy`. For large services, a `geosite-` rule-set is easier than single domains. Some apps, such as Telegram, also connect to IP addresses, so add their `geoip-` rule-set and use `Tun Mode`. See [Routing](@/guides/routing.md#simple-rules).

## Share the proxy with other devices {#share-with-devices}

Other devices on your network, such as a phone, a TV or a game console, can use Throne on your computer as their proxy.

1. Open the `Program` menu and turn on `Allow other devices to connect`. It is also in the tray menu.
2. Look at the middle of the status bar. It now shows `Mixed: <address>:2080`: the address and port that other devices use.
3. Recommended: open `Settings` → `Basic Settings` → `Common`, tick `Enable Authorization` and set `Inbound Username` and `Inbound Password`.
4. On the other device, set an HTTP or SOCKS5 proxy with that address and port, and the username and password if you set them.

Things to know:

- Throne must keep running on the computer. The other device's traffic follows your active routing profile.
- Authorization applies to everyone who uses the port, including apps on your computer that use the system proxy.
- If a device cannot connect, check that the computer's firewall allows incoming connections to `ThroneCore`.
- **Android:** turn on `Settings` → `Inbound` → `Allow connections from the LAN`. See [LAN sharing on Android](@/android/modes.md#lan-sharing).

For more about the proxy port, see [LAN sharing](@/guides/proxy_modes.md#lan-sharing).

## Windows Mobile Hotspot with TUN mode {#hotspot}

When Windows shares your normal network adapter through Mobile Hotspot or Internet Connection Sharing while `Tun Mode` is on, Throne shows "IPv4 forwarding breaks Tun mode". Windows then ignores the setting that keeps Throne's own connections out of the tunnel, so they loop back into it and fail.

Throne's warning suggests a workaround, which users also reported in [#1916](https://github.com/throneproj/Throne/issues/1916): share the connection of Throne's TUN adapter instead.

1. Turn on `Tun Mode` in Throne and start a profile.
2. In Windows, open `Settings` → `Mobile hotspot` → `Share my internet connection from` and choose `throne-tun`.
3. Turn on the hotspot.

The `throne-tun` adapter exists only while `Tun Mode` is on. Connection sharing is a Windows feature that Throne does not control. If the workaround does not work for you, turn the hotspot off while you use `Tun Mode`, or let the devices use the proxy port instead (see [Share the proxy with other devices](#share-with-devices)).

## Voice calls and games {#calls-and-games}

Voice calls in Discord and Telegram, and many games, use UDP and often ignore the system proxy.

- Use `Tun Mode`, so that this traffic reaches Throne at all.
- Your server and its protocol must carry UDP. Not every protocol can (an HTTP proxy cannot), and some servers turn UDP off. If calls fail on one server, try another one.
- For a low delay, choose a nearby server. See [URL test](@/guides/testing.md#url-test).
- If a game does not need the proxy, send it direct: put its program in the `Direct` box, for example `processName:game.exe`.
- For games and peer-to-peer apps that go direct in TUN mode, try `Settings` → `Tun Settings` → `L3 Bridge Bypass`. It sends direct UDP and ICMP traffic straight out of your network adapter, which is faster and keeps NAT working.

## Docker, WSL and virtual machines {#docker-wsl-vms}

Containers, WSL and virtual machines have their own virtual networks. There are two ways to give them the proxy.

**Point them at Throne's proxy port.** This is the simplest and most reliable way.

1. Turn on `Program` → `Allow other devices to connect`.
2. Inside the container or virtual machine, set the proxy to `http://<address>:2080`. Use an address of your computer that the guest can reach, for example the one in the status bar.

Many command-line tools on Linux read these variables:

```bash
export http_proxy=http://192.168.1.10:2080
export https_proxy=http://192.168.1.10:2080
```

The same port also accepts SOCKS5.

**Use TUN mode on the computer.** Whether a guest's traffic enters the tunnel depends on how its virtual network is built. If guests lose their connection, or you cannot reach them from the computer, check these settings in `Settings` → `Tun Settings`:

- Keep `Private Range Bypass` on (the default). It keeps private address ranges, which virtual networks usually use, out of the tunnel.
- `Enable Tun Routing` also keeps the IP ranges of your `direct` rules out of the tunnel. Large rule-sets can cause high CPU use on Windows, so turn it on with care.
- **Linux:** `Auto Redirect` (on by default) is needed on newer kernels for the `system` and `mixed` stacks. While it is on, this computer cannot act as a network gateway for other devices, and containers or virtual machines whose traffic it forwards can be affected. Use the proxy port for them instead.

See [TUN Mode](@/guides/tun_mode.md#settings).

## Corporate VPN side by side {#corporate-vpn}

To reach company resources through your corporate VPN while everything else uses Throne, keep the company's traffic away from the proxy. Choose one of these ways.

**Send company traffic direct.** Add the company's domains and networks to the `Direct` box of your routing profile:

```text
suffix:corp.example.com
ip:10.20.0.0/16
```

With `Enable DNS Routing` on (the default), the company's domains are looked up with Direct DNS instead of Remote DNS. In TUN mode, private ranges such as `10.0.0.0/8` already stay out of the tunnel (`Private Range Bypass`). For company networks in public ranges, turn on `Tun Settings` → `Enable Tun Routing`, which keeps the IP ranges of `direct` rules out of the tunnel.

**Bind to the VPN's network adapter.** Use this when direct traffic leaves through the wrong adapter.

1. Open `Program` → `New profile`, choose the type `Direct` and give it a name, for example `Corporate`.
2. Click `Advanced Settings`, enter the name of the corporate VPN adapter in `Bind Interface` and click `OK`. Save the profile with `OK`.
3. In your routing profile, add an [advanced rule](@/guides/routing.md#advanced-rules) with the company's `domain_suffix` and `ip_cidr`, the action `route`, and `outbound` set to `[group] Corporate`. Move it above your other rules.

**Run the VPN inside Throne.** Throne can run an OpenVPN or OpenConnect profile next to your proxy, only for the networks that it announces. See [split tunnel](@/advanced/vpn_profiles.md#split-tunnel).

Other VPN programs can interfere with `Tun Mode`. If problems appear only in TUN mode, use system proxy mode while the corporate VPN is connected.

## Per-app routing {#per-app}

Choose which programs use the proxy.

**Desktop:**

1. Turn on `Tun Mode`. Only in TUN mode does the traffic of every program reach Throne.
2. Start the program and let it connect.
3. In the `Connections` tab, right-click one of its connections and choose `Append process "<name>" to` → `Proxy`, `Direct` or `Block`.
4. Click `Restart` in the "Settings changed, restart to apply" notice.

You can also write the rules yourself on the `Basic` tab of your routing profile, for example `processName:Telegram.exe` or `processPath:C:\Program Files\App\app.exe`. Names must match exactly, including upper and lower case.

- **Only some programs through the proxy:** set `Default outbound` to `direct` and put the programs in the `Proxy` box.
- **All programs except some:** keep `Default outbound` at `proxy` and put the exceptions in the `Direct` box.

If the `Append` items are disabled, the active routing profile cannot be changed from there, for example because it is a remote profile that updates itself. See [Connections tab](@/guides/routing.md#connections-tab).

**Android:** choose the apps in `Settings` → `TUN / VPN` → `Apps VPN mode`, or use the `Apps` field of a routing rule. See [per-app proxy](@/android/modes.md#per-app-proxy).
