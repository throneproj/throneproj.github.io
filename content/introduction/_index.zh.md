+++
title = "简介"
description = "Throne简介"
weight = 1
sort_by = "weight"

[extra]
+++

Throne（原 Nekoray）是一个基于 Qt 的跨平台桌面 GUI 代理工具，由 [Sing-box](https://github.com/SagerNet/sing-box) 驱动。

原生支持 Windows 11/10/8/7 / Linux / macOS。

<img width="1002" height="789" alt="image" src="https://github.com/user-attachments/assets/3c9bf428-e3bd-426b-8ca1-cc57ecbedd7e" />

## 支持的协议

- SOCKS
- HTTP(S)
- Shadowsocks
- Trojan
- VMess
- VLESS
- TUIC
- Hysteria
- Hysteria2
- AnyTLS
- Mieru
- NaïveProxy
- Juicity
- TrustTunnel
- ShadowTLS
- Wireguard
- AmneziaWG
- SSH
- Xray VLESS
- Custom Outbound（Sing-box 和 Xray 均支持）
- Custom Config（Sing-box 和 Xray 均支持）
- 链式出站
- Extra Core

## 订阅格式

支持多种订阅格式，包括分享链接、多种 Sing-box 配置的 JSON 表示形式、v2rayN 链接格式，以及对 Shadowsocks 和 Clash 格式的有限支持。

深层链接同样受支持——详见[深层链接](/advanced/deeplinks/)文档。

## 致谢

- [sing-box](https://github.com/SagerNet/sing-box)
- [Xray-core](https://github.com/xtls/xray-core)
- [Qv2ray](https://github.com/Qv2ray/Qv2ray)
- [Qt](https://www.qt.io/)
- [simple-protobuf](https://github.com/tonda-kriz/simple-protobuf)
- [fkYAML](https://github.com/fktn-k/fkYAML)
- [quirc](https://github.com/dlbeer/quirc)
- [QHotkey](https://github.com/Skycoder42/QHotkey)
- [SQLiteCpp](https://github.com/srombauts/sqlitecpp)

## 常见问题

**这个项目与原始的 Nekoray 有什么不同？**

Nekoray 的原始开发者从 2023 年 12 月开始部分放弃了项目，最近只做了一些小更新，而该项目现已正式归档。本项目旨在延续原项目的方向，带来大量改进、众多新功能，同时移除了过时的功能并进行了简化。

**为什么我的杀毒软件会把 Throne 及/或其核心（Core）检测为恶意软件？**

Throne 的内置更新功能会下载新版本、删除旧文件并用新文件替换，这与恶意软件的行为颇为相似（删除你的文件并用加密后的版本替换）。此外，`System DNS` 功能会更改系统的 DNS 设置，这也被某些杀毒软件视为危险行为。

**在 Linux 上真的需要设置 `SUID` 位吗？**

为了创建和管理系统 TUN 接口，需要 root 权限；否则你必须为核心（Core）授予一些 `Cap_xxx_admin` 权限，而且每次启用 TUN 时仍需输入 3 到 4 次密码。你也可以在 `Basic Settings`（基本设置）→ `Security`（安全）中禁用自动提权，但请注意，除非你手动授予所需权限，否则需要 root 权限的功能将无法使用。

**为什么强制退出 Throne 后我的网络无法使用？**

如果在启用 `System proxy`（系统代理）时强制退出 Throne，进程会立即结束，Throne 来不及重置代理设置。

解决方法：

- 始终正常关闭 Throne。
- 如果不小心强制退出，请重新打开 Throne，启用 `System proxy`，然后再将其禁用——这样即可重置设置。

**可下载的路由配置文件／规则集来自哪里？**

它们位于 [routeprofiles](https://github.com/throneproj/routeprofiles) 仓库。

**`Throne-<version>-debian-system-qt-x64.deb` 与 `Throne-<version>-debian-x64.deb` 有何区别？为什么后者比前者大约重 3 倍？**

前者不打包 Qt 库，依赖宿主系统中已安装的 Qt；后者将所需的一切都打包在内，因此体积更大。前者之所以存在，是因为在某些旧系统上，随附的 Qt 库会用到不受支持的系统特性。如果图形界面在你的系统上无法加载，可以尝试下载 system-qt 版本，并通过包管理器安装合适的 Qt 库，或从源码编译。
