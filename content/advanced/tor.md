+++
title = "Tor"
description = "Connect through Tor with bridges where it is blocked, send proxied traffic out through Tor, and open .onion sites."
weight = 42
toc = true
+++

Throne uses Tor in two ways:

- A [Tor profile](#tor-profile) connects to the Tor network itself, through bridges where Tor is blocked. It needs no server of your own.
- The [Tor exit](#tor-exit) adds Tor as the last hop after your proxy: your device → the profile you start → Tor → Internet.

Either way, websites see a Tor exit address, and `.onion` sites open.

- Tor carries TCP only. UDP, such as QUIC or voice calls, does not get through; browsers fall back to TCP.
- Tor is available on Windows, macOS and 64-bit Linux (x86-64 and ARM), not on Android.

## Download Tor {#download}

Throne downloads Tor the first time it is needed. Starting a profile that uses Tor asks first: click `Download`, and the profile starts when Tor is installed. Choosing the Tor exit starts the download and turns the exit on when it finishes. The `Tor` profile editor and the `Exit` tab of `Routing Settings` say whether Tor is installed, and the `Logs` tab shows the progress.

- Throne downloads the Tor Expert Bundle from the Tor Project and checks it against the project's checksums. When torproject.org cannot be reached, it uses Throne's copy on GitHub, which is checked against the Tor Project's signature before it is published.
- The download goes through the running profile, or direct when no profile runs.
- Tor is kept in the `tor` folder of the [config folder](@/reference/files.md#data-folder).

## Tor profile {#tor-profile}

Open `Program` → `New profile` and set `Type` to `Tor`. `Bridges` decides how Throne reaches the Tor network:

| Choice | When to use it |
| --- | --- |
| `None` | Tor is not blocked on your network. |
| `Built-in` | The bridges built into Throne: `Snowflake` (works in most censored networks), `obfs4` or `meek`. |
| `Custom` | Bridge lines from the Tor Project or someone you trust, one per line, with or without the `Bridge` keyword. Throne supports `obfs4`, `webtunnel`, `snowflake`, `meek_lite` and plain bridges. |

`Exit country` picks the country of the last Tor relay; `Any` lets Tor choose.

The first connection takes up to a minute or two while Tor downloads its view of the network. Throne keeps that data for each bridge setting, so later starts are faster. Tor profiles also work in [chains](@/advanced/chains.md#chains) and groups: a chain with the Tor profile on top and your server below it reaches the server through Tor.

The bridge transports (obfs4, WebTunnel, Snowflake, meek) run inside Throne and connect the same way as your other profiles, so they also work in Tun mode.

### Get bridges {#get-bridges}

`Get bridges` asks the Tor Project's bridge service which bridges work in a country:

1. Choose the `Country`. `Automatic` lets the service tell from your connection.
2. Click `Request`. The request goes through a disguised (domain-fronted) connection, as in Tor Browser, and can take a minute.
3. Choose one of the suggestions and click `OK`. A built-in suggestion switches the profile to `Built-in`; the others fill `Custom`.

While a profile runs, the request may go through it, and `Automatic` then answers for the proxy's location: choose your country instead. When the service cannot be reached, Throne shows its built-in list for that country.

Other ways to get bridges: [bridges.torproject.org](https://bridges.torproject.org), the Tor Project's Telegram bot `@GetBridgesBot`, or an email to `bridges@torproject.org`.

### Import bridge lines {#import}

Copy the bridge lines and press `Ctrl+V` in the main window. Consecutive bridge lines become one `Tor` profile with `Custom` bridges. The QR code form from the bridge website, `['obfs4 …', 'obfs4 …']`, works too. Lines for transports Throne does not support (obfs2, obfs3, ScrambleSuit, Conjure) are skipped with a warning.

## Tor exit {#tor-exit}

Choose `Routing` → `Exit through` → `Tor`, or the same choice on the `Exit` tab of `Routing Settings`, where `Exit country` picks the country of the last Tor relay. `Selected profile` turns Tor off again. A running profile restarts with the new setting.

- Tor, [WARP](@/advanced/warp.md) and [Psiphon](@/advanced/psiphon.md) are choices of the same `Exit through` setting, so only one of them can be on.
- The exit needs no bridges: it reaches Tor through your proxy.
- When the profile you start is a Tor profile, or a chain that ends in one, the Tor exit is refused.

## New Tor circuit {#new-circuit}

`Tools` → `New Tor circuit` makes new connections take a different path through Tor, usually with a different exit address. Open connections keep theirs. It is available while the running config uses Tor.

## Traffic that skips Tor {#skip-tor}

Rules that send traffic to `Proxy without exit` skip the Tor exit and leave through the selected profile, see [Skip the exit for some traffic](@/advanced/warp.md#warp-bypass). `Direct` and `Block` work as usual. `.onion` addresses always go to Tor, before your own rules.
