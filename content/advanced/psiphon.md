+++
title = "Psiphon"
description = "Connect through the Psiphon network without a server of your own, or send proxied traffic out through Psiphon."
weight = 43
toc = true
+++

Psiphon is a free circumvention network run by Psiphon Inc. Throne connects to it with the same public settings other open-source clients use, so you need no server or account. Like any VPN provider, Psiphon can see which sites you visit.

Throne uses Psiphon in two ways:

- A [Psiphon profile](#psiphon-profile) connects to the Psiphon network directly.
- The [Psiphon exit](#psiphon-exit) adds Psiphon as the last hop after your proxy: your device → the profile you start → Psiphon → Internet.

Psiphon carries TCP and UDP. It works on Windows, macOS and Linux, not on Android.

## Psiphon profile {#psiphon-profile}

Open `Program` → `New profile` and set `Type` to `Psiphon`. `Region` picks the country of the Psiphon server; `Best performance` lets Psiphon choose.

The first connection can take up to a minute while Psiphon tries its servers; later ones usually take a second or two. Psiphon profiles also work in [chains](@/advanced/chains.md#chains) and groups: a chain with the Psiphon profile on top and your server below it reaches the server through Psiphon.

Psiphon's own apps can also connect through Conduit, its volunteer-run proxies. Throne cannot: that needs a key that only Psiphon's apps have.

## Psiphon exit {#psiphon-exit}

Choose `Routing` → `Exit through` → `Psiphon`, or the same choice on the `Exit` tab of `Routing Settings`, where `Region` picks the server's country. `Selected profile` turns Psiphon off again. A running profile restarts with the new setting.

- Psiphon, [WARP](@/advanced/warp.md) and [Tor](@/advanced/tor.md) are choices of the same `Exit through` setting, so only one of them can be on.
- When the profile you start is a Psiphon profile, or a chain that ends in one, the Psiphon exit is refused.
- Rules that send traffic to `Proxy without exit` skip Psiphon, see [Skip the exit for some traffic](@/advanced/warp.md#warp-bypass).

## Server list {#server-list}

Psiphon finds its servers through a signed server list. Throne includes a copy and updates it from Throne's mirror on GitHub or from Psiphon's own address, whichever answers. Psiphon checks the list's signature itself, so a mirror cannot change it. The list and Psiphon's other data are kept in the `psiphon` folder of the [config folder](@/reference/files.md#data-folder).
