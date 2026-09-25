+++
title = "Throne for Android"
description = "介绍 Throne for Android 是什么、它与 Throne 桌面版的关系、快速入门，以及两个应用之间的主要区别。"
weight = 3
sort_by = "weight"
toc = true
+++

Throne for Android 是 Throne 的 Android 版本，前身名为 NekoBox for Android。从 2.0.0 版起，它运行与 Throne 桌面版相同的核心（ThroneCore），因此分组、订阅、路由配置、DNS、预设、自动选择器、WARP 和备份在两个应用中的工作方式相同。

本部分的页面介绍 Android 特有的内容：安装、权限、VPN 与代理模式、小部件、Android TV 以及故障排除。如果你刚开始使用本应用，请先按照[快速入门](#quick-start)操作，然后阅读[权限与后台运行](@/android/permissions.zh.md)，以免 Android 停止 VPN。

两个应用共有的功能在以下指南中说明：

- [订阅与分组](@/guides/subscriptions.zh.md)
- [路由](@/guides/routing.zh.md)
- [DNS](@/guides/dns.zh.md)
- [测试与自动选择器](@/guides/testing.zh.md)
- [Cloudflare WARP](@/advanced/warp.zh.md)
- [在桌面版与 Android 之间迁移](@/guides/backup.zh.md#desktop-android)

应用侧边菜单（抽屉式导航栏）中的 `文档`（Documentation）项会打开本网站。

## 快速入门 {#quick-start}

1. 为你的设备安装对应的 APK。大多数手机需要 `arm64-v8a`。参见[选择合适的 APK](@/android/installation.zh.md#choose-apk)。
2. 打开 Throne。在 Android 13 及更高版本上，请允许通知。
3. 当 Throne 询问“Keep Throne running”（让 Throne 保持运行）时，点按 `Allow`，并在 Android 对话框中确认。参见[权限与后台运行](@/android/permissions.zh.md)。
4. 复制你的订阅 URL。
5. 在 `配置`（Profiles）界面，点按工具栏中的 `添加服务器配置`（Add profile）图标（一个带加号的页面），然后点按 `从剪切板导入`（Import from clipboard）。如果想扫描二维码，请改为选择 `扫描二维码`（Scan QR code）。
6. Throne 会识别出该 URL 并询问“How to update?”（如何更新？）。点按 `Create new subscription group`。Throne 会添加一个以 URL 中的主机名命名的分组，并下载其中的配置。
7. 点按新分组的标签页。
8. 点按 ⋮（`More options`）→ `URL test`。面板会显示测试进度和结果摘要。每个配置会在列表中显示各自的结果。
9. 测试完成后，点按 `Select fastest`，或点按一个可用的配置。
10. 点按屏幕底部的圆形连接按钮。首次连接时，Android 会询问是否允许 Throne 建立 VPN 连接。请允许。
11. 要检查连接，请点按屏幕底部的横栏（“已连接 , 点击此处测试连接”）。当流量经由该配置通过时，它会显示“连接成功: HTTP 握手耗时 …ms”。

如果你的服务商提供的是 `throne://addsub/…` 链接，请在手机上打开它，以代替第 4–6 步。Throne 会询问“Add this subscription?”（添加此订阅？），然后添加该分组、下载其中的配置，并打开 `分组`（Groups）界面。之后打开 `配置`（Profiles）界面，从第 7 步继续。

当你从其他应用分享文本链接时，Throne 不会出现在 Android 的分享菜单中。请复制链接，改用 `从剪切板导入`（Import from clipboard）。

## 与桌面版的区别 {#differences}

两个应用共用同一个核心和大部分设置。以下方面有所不同：

| 方面 | Throne 桌面版 | Throne for Android |
| --- | --- | --- |
| 流量如何进入 Throne | `Tun 模式`（Tun Mode）和 `系统代理`（System Proxy）复选框 | `设置`（Settings）→ `General` → `运行模式`（Service mode）：`VPN`（默认）或 `仅代理`（Proxy only）。参见 [VPN 与代理模式](@/android/modes.zh.md)。 |
| 选择应用 | 按进程名或路径匹配的路由规则 | `分应用代理`（Apps VPN mode）以及按应用匹配的路由规则 |
| 备份 | `.thrbackup` 文件 | `.thrbackup` 文件，也可以存放在 WebDAV 服务器上 |
| 默认 TUN MTU | 1500 | 9000 |
| 默认核心日志级别 | `info` | `warn` |
| 从其他应用打开的 `throne://add/…` 链接 | 立即导入该配置 | 先询问“导入配置” |
| 原始（raw）路由配置 | 支持 | 不支持。来自桌面版备份的原始路由配置会以只读形式保留。 |
| TLS 伪装、Tailscale 和额外核心（Extra Core）配置、OTP 管理器，以及路由配置中的 OpenVPN 和 OpenConnect 端点 | 可用 | 不可用 |

从其他应用打开的 `vless://…` 等分享链接同样会先询问“导入配置”。通过 `从剪切板导入`（Import from clipboard）粘贴或以二维码扫描的配置链接会直接导入，不会询问。

Android 版还提供主屏幕小部件、快捷设置图块以及系统自带的“始终开启的 VPN”（Always-on VPN）功能。参见[小部件、图块与自动化](@/android/widgets.zh.md)和[始终开启的 VPN](@/android/permissions.zh.md#always-on)。在 Android 上，匹配所连接 Wi-Fi 网络的路由规则需要位置权限。参见[用于 Wi-Fi 规则的位置权限](@/android/permissions.zh.md#location)。

## Android 上的桌面版菜单 {#menus}

共用指南中展示的是桌面版的菜单。在 Android 上，相同的选项位于：

| Throne 桌面版 | Throne for Android |
| --- | --- |
| `分组`（Groups）→ `管理分组`（Manage Groups） | 侧边菜单 → `分组`（Groups） |
| `路由`（Routing）→ `路由设置`（Routing Settings）→ `路由`（Route）标签页 | 侧边菜单 → `路由`（Routing） |
| `路由设置` → `通用`（Common）标签页 | `设置`（Settings）→ `Routing` |
| `路由设置` → `DNS` 标签页 | `设置` → `DNS` |
| `路由设置` → `Warp` 标签页 | `设置` → `Routing` → `WARP` |
| `设置`（Settings）→ `Tun 设置`（Tun Settings） | `设置` → `TUN / VPN` |
| `设置` → `预设设置`（Preset Settings） | `设置` → `Presets` |
| `设置` → `基本设置`（Basic Settings）→ `订阅`（Subscription） | `设置` → `订阅`（Subscriptions） |
| `设置` → `基本设置` → `备份和恢复`（Backup and Restore） | 侧边菜单 → `工具`（Tools） |
