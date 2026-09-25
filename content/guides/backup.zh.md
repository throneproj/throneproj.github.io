+++
title = "备份、更新与迁移"
description = "备份和恢复 Throne，在桌面版与 Android 之间迁移数据，更新桌面版，以及从旧版本升级。"
weight = 70
toc = true
+++

本页介绍如何将你的配置档和设置保存到文件、如何恢复它们，以及如何在 Throne 桌面版与 Throne for Android 之间迁移它们。本页还说明如何更新桌面版，以及从旧版本升级时需要做什么。每次更新前都请先备份。

## 备份与恢复 {#backup-restore}

打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `备份和恢复`（Backup and Restore）。

创建备份：

1. 在 `创建备份`（Create Backup）下，勾选你需要的部分。默认勾选所有部分。
2. 点击 `创建备份...`（Create Backup...），然后选择文件的保存位置。默认建议保存为主文件夹中的 `Throne-backup.thrbackup`。
3. Throne 会确认已创建的文件，并列出其中包含的部分。

| 部分 | 包含内容 |
| --- | --- |
| `配置档(分组和代理)`（Profiles (groups and proxies)） | 你的分组、订阅和配置档。 |
| `路由配置档`（Routing profiles） | 你的路由配置档及其规则。 |
| `设置`（Settings） | 所有设置，包括 DNS、TUN、WARP 和入站设置。 |
| `OTP 配置档`（OTP profiles） | OTP 管理器中的条目。 |
| `自定义图标`（Custom icons） | 你的自定义托盘图标。 |

备份不包含流量历史、日志或核心的缓存文件。它也不会记录 `Tun 模式`（Tun Mode）或 `系统代理`（System Proxy）是否处于开启状态。

{% alert_warning() %}
备份中包含你的服务器密码、订阅链接和其他机密信息。请妥善保管该文件，切勿将其附在 Bug 报告中。
{% end %}

恢复备份：

1. 点击 `从备份恢复...`（Restore from Backup...），然后选择一个 `.thrbackup` 文件。
2. Throne 会显示备份的创建时间。勾选你想要恢复的部分。文件中不包含的部分会显示为灰色。
3. 点击 `恢复`（Restore）。每个选中的部分都会替换你当前的数据。此操作无法撤销。
4. Throne 会重启。

旧版本 Throne 创建的备份可以正常恢复。较新版本创建的备份可能会被拒绝，并提示“不支持的备份格式版本”；请先更新 Throne。

## 在桌面版与 Android 之间迁移 {#desktop-android}

Throne 桌面版和 Throne for Android 使用相同的备份格式，因此你可以在两者之间双向迁移数据。

从桌面版迁移到手机：

1. 在桌面版中按上述方法创建备份。
2. 将 `.thrbackup` 文件复制到手机上。
3. 在手机上打开 `设置`（Settings）→ `Backup & restore`，或打开侧边菜单中的 `工具`（Tools），点按 `Restore` 并选择该文件。从文件管理器中打开该文件时，也会提示恢复。
4. 勾选要恢复的部分并确认。Throne 会重启。

从手机迁移到桌面版：

1. 在手机上打开 `设置`（Settings）→ `Backup & restore`，勾选要备份的部分，然后点按 `Create backup`。`分享`（Share）可将文件发送到其他应用。
2. 将该文件复制到电脑上。
3. 在桌面版中按上述方法恢复。

**Android：** 你还可以把备份保存在 WebDAV 服务器上：`备份到 WebDAV`（Back up to WebDAV）、`从 WebDAV 恢复`（Restore from WebDAV）以及 `WebDAV 设置`（WebDAV settings）——其中包括 `服务器地址`（Server address）、`账号`（Username）、`密码`（Password）、`备份目录`（Backup path）和 `测试连接`（Test connection）。Throne 桌面版不支持 WebDAV，但可以恢复你从服务器下载的文件。WebDAV 凭据永远不会包含在备份中。

在 Android 上恢复桌面版备份时，有几处会发生变化：

| 项目 | 在 Android 上的结果 |
| --- | --- |
| `OTP 配置档` 和 `自定义图标` | 不会恢复。 |
| 两个应用都有的设置 | 采用备份中的值。例如，TUN MTU 会变为 1500（Android 默认值：9000），日志级别会变为 `info`（Android 默认值：`warn`）。 |
| 仅 Android 才有的设置 | 保留当前值。 |
| 来自其他设备的连接 | 当你恢复 `Settings` 部分，且备份允许其他设备连接而你的手机原先不允许时，Throne 会关闭 `允许来自局域网的连接`（Allow connections from the LAN）并显示警告。 |
| 原始路由配置档 | 会保留，但为只读。Android 无法使用它们；如果其中某个原本处于活动状态，则第一个可用的路由配置档会成为活动配置档。 |
| 路由配置档中的 OpenVPN 和 OpenConnect 端点 | 随配置档一起保留，但不会在 Android 上运行。 |
| Tailscale 和额外核心（Extra Core）配置档 | 会恢复，但无法在 Android 上启动。 |

反过来，匹配 Android 应用的规则以及分应用代理设置在桌面版上不起作用。

## 更新桌面版 {#updating}

你的配置档和设置存放在数据文件夹中，更新时会保留该文件夹（参见[数据文件夹](@/reference/files.zh.md#data-folder)）。尽管如此，仍请先创建备份。

1. 打开 `工具`（Tools）→ `检查更新`（Check For Update）。Throne 会向 GitHub 查询最新版本。如果你运行的已经是最新版本，会看到“无更新”。
2. 如果有更新的版本，Throne 会显示其发行说明，并提供 `更新`（Update）、`浏览器中打开`（Open in browser）和 `关闭`（Close）按钮。
3. 点击 `更新`（Update）。Throne 会下载新版本，并询问“更新已准备好，重启进行安装吗？”。
4. 点击 `是`（Yes）。Throne 会关闭，由更新程序安装新版本。

一键 `更新`（Update）仅适用于 ZIP 版本，以及 Windows 安装程序为当前用户执行的默认安装——在这两种情况下，Throne 会把数据保存在程序旁边。其他安装方式只有 `浏览器中打开`（Open in browser）按钮。在 macOS 上、使用系统 Qt 的软件包以及通过 Linux 安装脚本安装的版本中，Throne 不附带更新程序，因此 `检查更新`（Check For Update）会显示为灰色。各种安装方式的更新方法如下：

| 安装方式 | 更新方法 |
| --- | --- |
| ZIP 文件 | 使用 `更新`，或下载新的 ZIP 并替换程序文件。保留 `config` 文件夹。 |
| Windows 安装程序，为当前用户安装（默认） | 使用 `更新`，或下载并运行新的安装程序。 |
| Windows 安装程序，为所有用户安装 | 下载并运行新的安装程序。 |
| `.deb` 或 `.rpm` 软件包 | 下载并安装新的软件包。 |
| Linux 安装脚本 | 再次运行该脚本。 |
| macOS | 下载新版本并替换 `Throne.app`。参见[安装](@/get_started/installation.zh.md#macos)。 |
| WinGet、Scoop、AUR、Nix 或 RPM 仓库 | 使用包管理器更新。参见[包管理器](@/get_started/installation.zh.md#package-managers)。 |

如果你使用 Windows 安装程序卸载后重新安装，当卸载程序询问“Also delete your Throne profiles, settings and logs?”（是否同时删除你的 Throne 配置档、设置和日志？）时，请选择 `否`（No）。否则你的数据会被删除。

由于更新程序会替换程序文件，一些杀毒软件会将其标记为可疑。如果更新失败，请确认 Throne 不在你的“下载”（Downloads）文件夹中（[#1109](https://github.com/throneproj/Throne/issues/1109)），然后重试；或者从[下载页面](@/downloads.zh.md)下载新版本。

## Beta 版 {#beta}

Beta 版（预发布版本）会率先获得新功能和修复，但可能存在更多错误。安装 Beta 版之前请先备份。

- **桌面版：** 开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `杂项`（Miscellaneous）→ `允许更新到 beta 版`（Allow updating to beta versions）。此后 `检查更新`（Check For Update）也会提供预发布版本，其窗口标题会显示“(Pre-release)”（预发布）。
- **Android：** 开启 `设置`（Settings）→ `General` → `Allow updating to beta versions`。此后 `关于`（About）→ `Check for updates` 会显示“Channel: stable and pre-releases”（渠道：稳定版和预发布版）。参见[应用内更新程序](@/android/installation.zh.md#updater)。

如需退回，请关闭该选项。更新程序只提供比你当前运行的版本更新的版本，因此在更新的稳定版发布之前，你会一直停留在 Beta 版上，除非你自行安装稳定版。

## 旧版本 {#old-versions}

- **早于 1.1.0 的 Throne 桌面版。** 1.1.0 版本将所有数据移入了一个数据库文件 `throne.db`。旧的配置不会被转换。请重新添加你的订阅和配置档，或者试试 [#1202](https://github.com/throneproj/Throne/issues/1202) 中的社区脚本。`备份和恢复`（Backup and Restore）自 1.1.3 起提供，因此 1.1.3 及更高版本创建的备份可以在更新的版本中恢复。
- **Nekoray 或 NekoBox。** 参见[从 Nekoray / NekoBox 迁移](@/help/migrating.zh.md)。
- **早于 2.0.0 的 Throne for Android。** 2.0.0 版本使用新的密钥签名，因此无法覆盖安装在旧版本之上。请先卸载旧应用；2.0.0 会以空白状态启动。旧的 Android 备份（`throne_backup_*.json` 文件和 WebDAV `.zip` 文件）无法恢复，只能恢复 `.thrbackup` 文件。卸载前，请记下你的订阅链接。如果你同时使用 Throne 桌面版，也可以改用桌面版备份来迁移全部数据。参见[安装与升级](@/android/installation.zh.md#upgrading)。
