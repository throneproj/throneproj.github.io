+++
title = "Tor"
description = "Send proxied traffic out through Tor behind your proxy, and open .onion sites."
weight = 42
toc = true
+++

Throne can add Tor as the last hop after your proxy: your device → the profile you start → Tor → Internet. Websites then see a Tor exit address instead of your proxy server's, and `.onion` sites open.

- Tor carries TCP only. UDP that goes to the proxy, such as QUIC or voice calls, does not get through; browsers fall back to TCP.
- Tor and [WARP](@/advanced/warp.md) are choices of the same `Exit through` setting, so only one of them can be on.
- Tor is available on Windows, macOS and 64-bit Linux (x86-64 and ARM).

## Turn Tor on {#enable}

Choose `Routing` → `Exit through` → `Tor`, or the same choice on the `Exit` tab of `Routing Settings`. `Selected profile` turns Tor off again. A running profile restarts with the new setting.

The first time, Throne downloads Tor. From the menu, Tor turns on when the download finishes; in `Routing Settings`, the line under `Tor` says whether Tor is installed, and the download starts when you click `OK`. The `Logs` tab shows the progress.

- Throne downloads the Tor Expert Bundle from the Tor Project, checks it against the project's checksums and keeps it in the `tor` folder of the [config folder](@/reference/files.md#data-folder).
- The download goes through the running profile, or direct when no profile runs.

## Traffic that skips Tor {#skip-tor}

Rules that send traffic to `Proxy without WARP` skip Tor as well and leave through the selected profile, see [Skip WARP for some traffic](@/advanced/warp.md#warp-bypass). `Direct` and `Block` work as usual. `.onion` addresses always go to Tor, before your own rules.
