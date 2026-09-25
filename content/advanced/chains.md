+++
title = "Proxy Chains & Custom Configs"
description = "Chain several profiles, add front and landing proxies to a group, write raw sing-box or Xray JSON, and run another proxy program as an Extra Core."
weight = 20
toc = true
+++

Use this page when one server is not enough, or when a profile needs options that the normal editors do not have. It covers proxy chains, front and landing proxies for groups, custom JSON configs and Extra Core profiles.

## Proxy chains {#chains}

A chain profile sends your traffic through several profiles, one after another. Each server sees only the server before it, and the last one connects to the website.

### Create a chain {#create-chain}

1. Open `Program` → `New profile` (`Ctrl+N`).
2. Set `Type` to `Chain Proxy` and enter a `Name`.
3. Click `Select Profile`. The editor hides, and the main window switches to select mode.
4. Double-click the profile for the next hop, or select it and press `Enter`. The editor comes back with the profile added.
5. Repeat steps 3 and 4 for every hop.
6. Drag the rows into the right order. The buttons on each row replace or remove that hop.
7. Click `OK`.

Select mode ends only when you choose a profile. If you chose the wrong one, remove it with the button on its row.

### Hop order {#hop-order}

The editor says "Traffic order is from top to bottom". Your device connects to the top profile first. The traffic then passes each profile below it, and the bottom profile connects to the website. Websites see the address of the bottom profile.

With `A` on top and `B` below it, traffic goes: your device → `A` → `B` → Internet.

### Rules and limits {#chain-limits}

- A chain cannot contain another chain.
- An auto selector cannot be a hop, because it changes servers by itself. The auto selector also skips chain profiles.
- `Custom (sing-box config)` profiles cannot be hops. `Custom (sing-box outbound)` and `Custom (Xray outbound)` profiles can.
- A chain can hold one Extra Core profile, and it must be the top hop. Throne's warning calls it the "final hop"; this means the hop your device connects to first.
- A chain can hold one `Custom (Xray config)` profile. It must also be the top hop, and it cannot be combined with an Extra Core profile or with other Xray hops.
- All Xray hops must be next to each other: sing-box hops, then Xray hops, then sing-box hops. See [Xray in chains](@/advanced/xray.md#xray-in-chains).
- URL tests skip chains that contain an Extra Core or `Custom (Xray config)` profile.

Throne checks some rules when you add a hop or save the chain, and the others when you start it. A failed check shows its reason in a message or in the log.

A chain can also be the outbound of a routing rule, if none of its hops is an Extra Core or full-config profile.

## Front and landing proxies {#front-landing}

A group can add one hop before and one hop after every profile in it. This works like a chain, but you do not need to create chain profiles.

1. Right-click the group tab and choose `Edit selected Group`.
2. Choose a `Front Proxy`, a `Landing Proxy`, or both. Type part of a name to search all profiles. `None` removes the hop.
3. Click `OK`.

Traffic then goes: your device → `Front Proxy` → the profile you start → `Landing Proxy` → Internet. When WARP is on, it comes after the landing proxy.

- A front proxy helps when the group's servers cannot be reached directly but can be reached through another server.
- A landing proxy makes websites see the same exit server, whichever profile of the group you start.

Throne builds a chain from these hops, so the chain limits apply. For example, a front or landing proxy cannot be a chain profile, and a group with a front proxy cannot start an Extra Core or `Custom (Xray config)` profile. Auto selectors are not offered in these lists. For the other group settings, see [Subscriptions & Groups](@/guides/subscriptions.md#front-landing-proxy).

## Custom configs {#custom-config}

A custom profile holds raw JSON for the core. Use it for options that the normal editors do not offer. Create one with `Program` → `New profile` and one of these types:

| `Type` | What you enter | `Type` column |
| --- | --- | --- |
| `Custom (sing-box outbound)` | One sing-box outbound or endpoint | `Custom … Outbound` |
| `Custom (sing-box config)` | A complete sing-box config | `Custom Config` |
| `Custom (Xray outbound)` | One Xray outbound | `Custom Xray … Outbound` |
| `Custom (Xray config)` | A complete Xray config | `Custom Xray Config` |

`Json Editor` opens the JSON in a larger window. For the two sing-box types, it checks the JSON against the sing-box schema and lists the problems. `Format` tidies the text.

A minimal `Custom (sing-box outbound)`:

```json
{
  "type": "socks",
  "server": "203.0.113.10",
  "server_port": 1080
}
```

When you import JSON:

- A sing-box config with `outbounds` or `endpoints` is split into one normal profile per supported outbound. A single sing-box outbound object becomes a `Custom (sing-box outbound)`.
- In Xray JSON, VLESS outbounds become `VLESS (Xray)` and other outbounds become `Custom (Xray outbound)`. A JSON list of complete Xray configs becomes one `Custom (Xray config)` per config; Throne removes their inbounds and adds its own.
- No import creates a `Custom (sing-box config)`. You create that type by hand.

### Full configs {#full-configs}

- **`Custom (sing-box config)`:** Throne starts your config exactly as written. It does not add its own inbounds, TUN, routing profile, DNS settings, WARP, or front and landing proxies. Your config must bring its own inbounds.
- **`Custom (Xray config)`:** Throne adds a local SOCKS inbound to your config and puts sing-box in front of it. TUN mode, the routing profile and DNS settings still apply. Inside Xray, your config's own `routing` chooses the outbound.

Full configs cannot be the outbound of a routing rule or a routing-profile endpoint. The auto selector can use `Custom (Xray config)` profiles, each in its own Xray instance, but it skips `Custom (sing-box config)` profiles.

## Extra Core {#extra-core}

An Extra Core profile starts another proxy program on your computer and sends traffic to it. Use it for a protocol that Throne does not support. The program must open a local SOCKS server; Throne connects to it as it would to any SOCKS proxy. Extra Core is available on desktop only.

1. Open `Program` → `New profile`.
2. Set `Type` to `Extra Core`.
3. Fill in the fields below.
4. Click `OK` and start the profile.

| Field | What it does |
| --- | --- |
| `Core path` | The program to run. `Choose from file` selects it; Throne remembers the paths you chose before. |
| `Args` | Command-line arguments. Throne replaces `%s` with the path of a temporary file that holds the `Config` text. Quote values that contain spaces, as in a shell. |
| `Config` | The content of the program's config file. It reaches the program only when `Args` contains `%s`. |
| `Socks address` | The address of the program's SOCKS server. Default `127.0.0.1`. |
| `Socks port` | The port of the program's SOCKS server. It must match the program's config, and it must not be Throne's own listen port. |
| `No logs` | Hides the program's output from the `Logs` tab. |

For example, if the program reads its config with `-c <file>`, set `Args` to `-c %s` and paste the config into `Config`.

How it runs:

- Throne starts the program when you start the profile and stops it when you stop the profile. The temporary config file is then deleted.
- The program's output appears in the `Logs` tab, in lines that contain `Extra Core:`, unless `No logs` is ticked.
- If the program exits by itself, Throne stops the profile ("Extra Core exited, stopping profile...").
- The program runs with normal user rights, even when Throne's core has administrator or root rights for TUN mode.

An Extra Core profile cannot be the outbound of a routing rule. In a chain, it must be the top hop. URL tests and the auto selector skip it.

## Android {#android}

- Proxy chains work the same way: `Add profile` → `Manual settings` → `Proxy chain`. The top row is the first server your device connects to, and the bottom row is the exit. The same limits apply.
- Groups have the same `Front proxy` and `Landing proxy` options.
- `Custom config` has the same four types (`Config type`), with sing-box schema checking in the JSON editor.
- Extra Core profiles are desktop only. If a desktop backup contains one, Android keeps it but cannot start it.
