+++
title = "Cloudflare WARP"
description = "Add Cloudflare WARP as an extra exit behind your proxy, and let chosen traffic skip it."
weight = 40
toc = true
+++

WARP is Cloudflare's free VPN service. Throne can add it as an extra hop after your proxy: your device → the profile you start → WARP → Internet. Websites then see a Cloudflare address instead of your proxy server's, which helps with sites that block VPN or data-center addresses.

- WARP applies to every profile you start, including chains and auto selectors, and comes after a group's landing proxy. Only `Custom (sing-box config)` profiles run without it.
- WARP runs through your proxy, so the profile must carry its traffic: `WireGuard` and `AmneziaWG` modes need UDP, and so does `MASQUE` over HTTP/3. `MASQUE` over HTTP/2 needs only TCP.
- WARP is one choice of `Exit through`; the other is [Tor](@/advanced/tor.md). Only one can be on.

## Generate a WARP config {#generate}

1. Open `Routing` → `Routing Settings` → `Exit` tab.
2. Choose the `Mode`: `WireGuard`, `MASQUE` or `AmneziaWG`.
3. Click `Generate WARP config` and accept the Cloudflare WARP terms the first time.
4. When the button shows "Success!", click `OK`.

`WireGuard` and `MASQUE` have separate configs, so generate again after switching between them. `AmneziaWG` uses the `WireGuard` config.

For `MASQUE`, the default `HTTP Version` uses HTTP/3 over UDP; `HTTP/2` runs over TCP and works where UDP is blocked.

### AmneziaWG mode {#amneziawg}

Use `AmneziaWG` when `WireGuard` mode does not connect because WireGuard to Cloudflare is blocked. Before the handshake, it sends packets that look like an HTTP/3 (QUIC) connection to `www.cloudflare.com` (the signature) and a few junk packets, which WARP accepts. WARP's packets leave from your proxy server, so the server's network is what matters, not yours.

Throne creates the signature when you choose `AmneziaWG`. A WireGuard config you generated earlier keeps working.

### If registration fails {#registration-fails}

Cloudflare's registration server, `api.cloudflareclient.com`, is blocked in some countries ([#1874](https://github.com/throneproj/Throne/issues/1874)). Register through your proxy:

1. Start a profile that works.
2. Tick `Settings` → `Basic Settings` → `General` → `Updates and Downloads` → `Send Throne's own requests through the proxy`. With `System proxy` on, Throne already does this.
3. Click `Generate WARP config` again.

- "Request with proxy but no profile started.": start a profile first.
- With `Disable mixed inbound` on, the request also needs Tun mode.
- With the [kill switch](@/advanced/kill_switch.md) on, generate while a profile runs in Tun mode or with `Send Throne's own requests through the proxy` on.

`Registration Domains` lists Cloudflare API domains to try in order, one per line. Empty means `api.cloudflareclient.com`.

## Turn WARP on {#enable}

Choose `Routing` → `Exit through` → `Cloudflare WARP`, or the same choice on the `Exit` tab of `Routing Settings`. `Selected profile` turns WARP off again, and `Tor` replaces it. A running profile restarts with the new setting.

If the current mode has no config, or `AmneziaWG` has no signature, WARP cannot be turned on: generate one first. To check that WARP works, open a website that shows your IP address: it should show a Cloudflare address.

## Skip WARP for some traffic {#warp-bypass}

`Proxy without WARP` sends traffic through your profile without the WARP hop. Set it in the routing profile editor (`Routing` → `Edit current profile`):

| Goal | `Everything else goes to` | Put the sites in |
| --- | --- | --- |
| Most traffic through WARP, some sites without it | `Proxy` | the `Proxy without WARP` list |
| Most traffic without WARP, some sites through it | `Proxy without WARP` | the `Proxy` list |

Rules can send traffic to `Proxy without WARP` too (see [Routing](@/guides/routing.md#advanced-rules)). It skips [Tor](@/advanced/tor.md) the same way. With neither WARP nor Tor on, it works like `Proxy`.

## WARP as a normal profile {#warp-profiles}

To use WARP without another proxy, or as a hop in a chain, make it a profile of its own:

1. Open `Program` → `New profile` and set `Type` to `WireGuard` or `MASQUE`.
2. Click `Generate WARP config` (WireGuard) or `Generate WARP identity` (MASQUE).
3. Enter a `Name` and click `OK`.

Such a profile connects to Cloudflare directly. Keep `Exit through` on `Selected profile` while you use it, or Throne adds a second WARP hop after it.

The `Mode` in `Routing Settings` does not affect it. For the `AmneziaWG` obfuscation on a WireGuard profile, tick `Enable Amnezia`, click `Amnezia Options`, and set `Junk Packet Count (Jc)` to 4, `Junk Packet Min Size (Jmin)` to 40, `Junk Packet Max Size (Jmax)` to 70, and H1 to H4 to 1, 2, 3 and 4. Then click `Generate QUIC signature`, enter `www.cloudflare.com` and click `OK`.

## Android {#android}

- The settings are in `Settings` → `Routing` → `WARP` and work as on the desktop, `AmneziaWG` included.
- If registration is blocked, connect first and turn on `Settings` → `Subscriptions` → `Use proxy`.
- To switch WARP quickly, open `Settings` → `Routing` → `Current routing profile` and tap `Enable WARP` or `Disable WARP`.
- The WireGuard and MASQUE profile editors have a `Generate WARP identity` button.
