+++
title = "Get Started"
description = "What Throne is, which systems it runs on, and where to begin."
weight = 1
sort_by = "weight"
aliases = ["/introduction/"]
+++

This section explains what Throne is, which systems it supports, and which pages to read first. Start here if you are new to Throne.

## What is Throne {#what-is-throne}

Throne (formerly Nekoray) is a free, open-source (GPL-3.0) proxy client for Windows, Linux and macOS. It has a Qt graphical interface and uses ThroneCore, a core based on sing-box that also runs Xray for the profiles that need it. You add servers from your provider or from your own server, choose which traffic goes through them, and connect in system proxy mode or TUN mode.

Throne for Android (formerly NekoBox for Android) is the Android app. Since version 2.0.0 it uses the same core, the same settings model and the same backup format as the desktop app, so you can move your setup between your computer and your phone. See [Throne for Android](@/android/_index.md).

If you used Nekoray or NekoBox before, read [Coming from Nekoray / NekoBox](@/help/migrating.md).

## Platforms {#platforms}

| System | Requirements | Package types |
|---|---|---|
| Windows | Windows 10 1809 or newer (x64, ARM64). Windows 7 SP1 or newer with the legacy builds (x64, 32-bit x86). | Installer, portable ZIP |
| Linux | x64 or ARM64, glibc 2.34 or newer (2.38 for ARM64 builds that bundle Qt) | Portable ZIP, `.deb`, `.rpm`, install script |
| macOS | macOS 13 or newer (Apple Silicon and Intel). macOS 10.15 or newer with the legacy build (Intel). | ZIP |
| Android | Android 7.0 or newer | APK |

Get the files from [Downloads](@/downloads.md).

## Highlights {#highlights}

- Many protocols, including VLESS with REALITY and XHTTP, Shadowsocks, Trojan, Hysteria, TUIC, WireGuard and AmneziaWG, NaïveProxy, OpenVPN and OpenConnect: [Protocols & Import Formats](@/reference/protocols.md).
- Subscriptions that update on a schedule, with User-Agent and HWID settings for each group: [Subscriptions & Groups](@/guides/subscriptions.md).
- System proxy or TUN mode for all apps, and proxy sharing with other devices on your network: [System Proxy, TUN & LAN sharing](@/guides/proxy_modes.md).
- Routing profiles with rules and rule-sets, and ready-made profiles for China, Iran and Russia: [Routing](@/guides/routing.md).
- Latency, IP and speed tests, and an Auto Selector that keeps you on a working server: [Testing & Auto Selector](@/guides/testing.md).
- Proxy chains and your own sing-box or Xray configs: [Proxy Chains & Custom Configs](@/advanced/chains.md).
- Anti-censorship options such as TLS fragment, uTLS and ECH: [Anti-Censorship Presets](@/advanced/presets.md).
- Built-in Cloudflare WARP: [Cloudflare WARP](@/advanced/warp.md).
- Backups that work in both the desktop and the Android app: [Backup, Updates & Migration](@/guides/backup.md).

## Where to start {#where-to-start}

1. Install Throne: [Installation](@/get_started/installation.md).
2. Add your servers and connect: [Quick Start](@/get_started/configuration.md).
3. Read the [Guides](@/guides/_index.md) for the features you need, such as subscriptions, routing and TUN mode.

On Android, start with [Throne for Android](@/android/_index.md). If something does not work, see [Troubleshooting](@/help/troubleshooting.md) and the [FAQ](@/help/faq.md).

## Credits {#credits}

Throne is built on these projects:

- [SagerNet/sing-box](https://github.com/SagerNet/sing-box): the proxy engine of the core
- [XTLS/Xray-core](https://github.com/xtls/xray-core): the Xray engine
- [Qv2ray](https://github.com/Qv2ray/Qv2ray): parts of the interface and the system proxy code
- [Qt](https://www.qt.io/): the interface toolkit
- [simple-protobuf](https://github.com/tonda-kriz/simple-protobuf): messages between the interface and the core
- [fkYAML](https://github.com/fktn-k/fkYAML): Clash YAML import
- [quirc](https://github.com/dlbeer/quirc): QR code reading
- [QHotkey](https://github.com/Skycoder42/QHotkey): global hotkeys
- [srombauts/sqlitecpp](https://github.com/srombauts/sqlitecpp): the profile and settings database
