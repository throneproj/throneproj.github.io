+++
title = "Cloudflare WARP"
description = "Add Cloudflare WARP as an extra exit behind your proxy, generate its config, turn it on, and let chosen traffic skip it."
weight = 40
toc = true
+++

WARP is Cloudflare's free VPN service. Throne can add WARP as an extra hop after your proxy. Websites then see a Cloudflare address instead of the address of your proxy server. This helps with sites that block VPN or data-center addresses.

## How WARP works in Throne {#how-it-works}

With WARP on, traffic goes: your device → the profile you start → WARP → Internet.

- WARP applies to every profile you start, including chains and auto selectors. Only `Custom (sing-box config)` profiles run without it. If the group has a landing proxy, WARP comes after it.
- WARP runs through your proxy, so the proxy must carry WARP's traffic:
  - `WireGuard` mode uses UDP. The profile must forward UDP.
  - `MASQUE` mode over HTTP/3 also needs UDP. MASQUE over HTTP/2 needs only TCP.
- Rules and the default outbound can send traffic through your proxy without WARP. See [Skip WARP for some traffic](#warp-bypass).

Setting up WARP takes two steps: generate a config once, then turn WARP on.

## Generate a WARP config {#generate}

1. Open `Routing` → `Routing Settings`.
2. Open the `Warp` tab.
3. Choose the `Mode`: `WireGuard` or `MASQUE`.
4. Click `Generate Warp Config`.
5. The first time, Throne asks whether you accept the Cloudflare WARP terms of service. Click `Yes`.
6. Wait until the button shows "Success!". The fields of the chosen mode are now filled in.
7. Click `OK`.

Each mode has its own fields. If you switch the `Mode` later, generate a config for that mode too.

| Mode | Fields |
| --- | --- |
| `WireGuard` | `Endpoint`, `Private Key`, `Public Key`, `Interface Addresses`, `Reserved` |
| `MASQUE` | `Endpoint`, `Private Key`, `Peer Public Key`, `Interface Addresses`, `SNI`, `HTTP Version` |

The MASQUE `HTTP Version` can be `HTTP/3 (fallback to HTTP/2)` (default), `HTTP/3 only` or `HTTP/2`. HTTP/3 runs over UDP. HTTP/2 runs over TLS on TCP and works where UDP is blocked.

Each generation registers a new device with Cloudflare.

### If registration fails {#registration-fails}

Cloudflare's registration server, `api.cloudflareclient.com`, is blocked in some countries ([#1874](https://github.com/throneproj/Throne/issues/1874)). In that case, register through your proxy:

1. Start a profile that works.
2. Open `Settings` → `Basic Settings` → `Miscellaneous` and tick `Use proxy`. When `System Proxy` is on, Throne already sends its own requests through the proxy.
3. Click `Generate Warp Config` again.

If no profile is running while `Use proxy` or `System Proxy` is on, generation fails with "Request with proxy but no profile started."

`Registration Domains…` holds the domains of the Cloudflare API, one per line. Throne tries them in order and uses the first one that accepts the registration. An empty list means `api.cloudflareclient.com`.

## Turn WARP on {#enable}

Click `Routing` → `Enable Warp`. A tick shows that WARP is on. Click it again to turn WARP off. A running profile restarts with the new setting.

You can also tick `Enable Warp` on the `Warp` tab and click `OK`. Then start the profile again to apply the change.

If WARP is on but the current mode has no generated config, the profile does not start, and Throne shows "Warp is enabled but its config has not been generated. Please generate the Warp config first in Routing Settings."

To check that WARP works, open a website that shows your IP address. It should show a Cloudflare address.

## Skip WARP for some traffic {#warp-bypass}

`warp-bypass` is an outbound that uses your profile without the WARP hop. Use it in a routing profile:

| Goal | `Default outbound` | Rules |
| --- | --- | --- |
| Most traffic through WARP, some sites without it | `proxy` | Put those sites in the `Warp-bypass` box. |
| Most traffic without WARP, some sites through it | `warp-bypass` | Put those sites in the `Proxy` box. |

The `Default outbound` list and the `Warp-bypass` box are in the routing profile editor: `Routing Settings` → `Route` tab → select a profile → `Edit`. Advanced rules can also use `warp-bypass` as their outbound. See [Routing](@/guides/routing.md#simple-rules) for the rule format.

When WARP is off, `warp-bypass` works the same as `proxy`.

## WARP as a normal profile {#warp-profiles}

You can also make WARP a profile of its own, for example to use it without another proxy, or as a hop in a chain.

1. Open `Program` → `New profile`.
2. Set `Type` to `WireGuard` or `MASQUE`.
3. Click `Generate Warp Config` (WireGuard) or `Generate WARP identity` (MASQUE). Throne fills in the keys, addresses, MTU and server address.
4. Enter a `Name` and click `OK`.

On its own, such a profile connects to Cloudflare directly. Keep `Enable Warp` off while you use it, or Throne adds a second WARP hop after it.

## Android {#android}

- The settings are in `Settings` → `Routing` → `WARP`: `Enable WARP`, `Mode`, the fields of each mode, `Generate WARP config` and `Registration domains`.
- The first generation asks you to accept the Cloudflare WARP terms of service.
- If registration is blocked, connect first and turn on `Settings` → `Subscriptions` → `Use proxy`. In `Proxy only` mode, the request always goes through the proxy.
- To switch WARP quickly, open the menu (⋮) of the Profiles screen → `Routing profile`, then tap `Enable WARP` or `Disable WARP`.
- If WARP is on without a generated config, Android shows "WARP is enabled but its config has not been generated. Generate it in Settings › Routing › WARP."
- The WireGuard and MASQUE profile editors have a `Generate WARP identity` button.
