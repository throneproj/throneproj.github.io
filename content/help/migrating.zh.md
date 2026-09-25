+++
title = "从 Nekoray / NekoBox 迁移"
description = "Nekoray 和 NekoBox 的功能在 Throne 中的位置，以及如何迁移你的服务器、订阅和设置。"
weight = 40
toc = true
+++

Throne 是 Nekoray 的延续，因此大多数功能的使用方式相同，但也有一些功能被移动或替换了。本页说明在哪里可以找到它们，以及如何迁移你的数据。背景信息请参阅 [Throne 与 Nekoray 有什么不同？](@/help/faq.zh.md#nekoray)

## 功能去哪儿了？ {#where-did-it-go}

| 在 Nekoray / NekoBox 中你使用的是… | 在 Throne 中你使用的是… |
| --- | --- |
| `服务器`（Server）菜单 | 右键点击配置档列表。菜单栏已隐藏。 |
| `首选项`（Preferences）菜单 | 工具栏中的 `设置`（Settings）按钮：`基本设置`（Basic Settings）、`路由设置`（Routing Settings）、`Tun 设置`（Tun Settings）、`热键设置`（Hotkey Settings）等。 |
| 订阅分组 | 同样的分组，位于 `分组`（Groups）按钮下。要更新某个分组，请右键点击其标签页 → `更新订阅`（Update subscription）。 |
| `Tun 设置` → `Bypass Process Name`（绕过隧道的程序） | 路由配置档中 `直连`（Direct）输入框里的 `processName:` 规则，例如 `processName:game.exe`。或者在 `连接`（Connections）标签页中右键点击某个连接 → `追加进程 "<name>" 到`（`Append process "<name>" to`）→ `直连`。 |
| `Tun 设置` → `Whitelist mode`（只有列出的程序使用隧道） | 一个 `默认出站`（Default outbound）设为 `direct` 的路由配置档，并将程序（`processName:…`）或网站放在 `代理`（Proxy）输入框中。 |
| `Tun 设置` → `Bypass CIDR` | `Tun 设置` → `私有地址范围绕过`（Private Range Bypass，即绕过隧道的地址范围），或 `直连` 输入框中的 `ip:` 规则。 |
| 适用于你所在国家的路由 `Preset` | `路由`（Routing）→ `下载配置档`（Download Profiles）→ `China`、`Iran` 或 `Russia`。 |
| `默认出站` 设为 `bypass` 或 `block` | 在路由配置档中将 `默认出站` 设为 `direct` 或 `block`。`block` 自 1.2.0 起可用。 |
| FlatGray、LightBlue 和 BlackSoft 等主题 | `基本设置` → `样式`（Style）→ `主题`（Theme）。这些主题自 1.1.5 起已恢复。 |
| `Copy links of selected (Neko Links)` | 标准分享链接。Throne 无法读取 `nekoray://` 或 `sn://` 链接。 |
| Throne 1.3.1 及更早版本中的 `劫持`（Hijack，包括其 DNS 服务器和 `重定向设置`（Redirect Settings））或 `系统 DNS`（System DNS） | `Tun 模式`（Tun Mode）。这些功能已在 1.3.1 中弃用，并将在下一个版本中移除。 |
| NekoBox for Android | Throne for Android 2.0.0。参见[下文](#from-nekobox-android)。 |

要按应用进行路由，请开启 `Tun 模式`。忽略系统代理的应用永远不会到达 Throne，因此在系统代理模式下，规则无法作用于这些应用。参见[路由](@/guides/routing.zh.md#simple-rules)和[连接标签页](@/guides/routing.zh.md#connections-tab)。

## 迁移你的数据 {#moving-data}

### 从 Nekoray 迁移 {#from-nekoray}

Throne 无法读取 Nekoray 的配置文件夹，也没有相应的导入工具。请手动迁移你的数据：

1. 在 Nekoray 中，从每个订阅的分组设置里复制其 URL。
2. 在 Throne 中，复制一个订阅 URL，在主窗口中按 `Ctrl+V`，然后选择 `创建新的订阅分组`（Create new subscription group）。对每个订阅重复此操作。
3. 对于你手动添加的服务器，在 Nekoray 中选中它们，然后使用 `服务器` → `分享`（Share）→ `复制选定项的链接`（Copy links of selected）。在 Throne 中按 `Ctrl+V` 导入它们。
4. 重新设置路由：通过 `路由` → `下载配置档` 下载适用于你所在国家的配置档，或者添加你自己的规则。参见[路由](@/guides/routing.zh.md)。
5. 检查你在 Nekoray 中修改过的设置，例如监听端口、DNS 服务器和热键，然后在 Throne 中重新设置。

开启 TUN 模式或系统代理时，不要同时运行 Nekoray 和 Throne。

### 从 Throne 1.0.x 迁移 {#from-1-0}

Throne 1.1.0 从 Nekoray 风格的 JSON 文件改为使用数据库（`throne.db`），并且无法读取旧文件。如果你直接在原位置将 1.0.x 更新到新版本，你的配置档、分组和设置不会出现在新版本中（[#1765](https://github.com/throneproj/Throne/issues/1765)）。请保留旧版本文件夹的副本，并按上述方法手动迁移你的订阅、分享链接和路由配置档。[#1202](https://github.com/throneproj/Throne/issues/1202) 列出了手动操作步骤和一个社区脚本，该脚本并非官方提供。

自 1.1.3 起，你可以使用 `基本设置` → `备份和恢复`（Backup and Restore）在不同的 Throne 版本和不同的电脑之间迁移数据。参见[备份、更新与迁移](@/guides/backup.zh.md#backup-restore)。

### 从 NekoBox for Android 迁移 {#from-nekobox-android}

Throne for Android 以前名为 NekoBox for Android。2.0.0 版本基于桌面版的核心重新构建，无法从旧版本直接升级：

- 它使用新的密钥签名，因此你必须先卸载旧版本。
- 它启动时没有任何数据，也无法恢复旧的 Android 备份（1.6.x 及更早版本的备份文件和 WebDAV `.zip` 文件）。它只能恢复 `.thrbackup` 文件，包括用 Throne 桌面版创建的备份。

卸载旧版本之前，请复制你的订阅 URL，以及你手动添加的服务器的分享链接。如果你也使用 Throne 桌面版，也可以改为在手机上恢复桌面版的备份；参见[备份、更新与迁移](@/guides/backup.zh.md#desktop-android)。详细信息：[安装与升级](@/android/installation.zh.md#upgrading)。
