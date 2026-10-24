+++
title = "命令行、文件与日志"
description = "Throne 桌面版的命令行选项、它在各个系统上存放数据的位置、配置文件夹中各个文件的内容、日志，以及如何重置。"
weight = 30
toc = true
+++

本页介绍 Throne 桌面版的命令行选项、Throne 存放数据的位置、各个文件的用途、在哪里查找日志，以及如何使用默认设置从头开始。

## 命令行 {#command-line}

Throne 接受以下选项：

| 选项 | 作用 |
| --- | --- |
| `-appdata` | 将数据保存在你的用户文件夹中，而不是程序旁边。参见[数据文件夹](#data-folder)。 |
| `-appdata <folder>` | 将数据保存在 `<folder>` 中。Throne 会在其中创建一个 `config` 文件夹。 |
| `-tray` | 启动时隐藏窗口，只显示托盘图标。 |
| 一条 `throne://` 链接 | 像你点击了该链接一样处理它。参见[深度链接](@/advanced/deeplinks.zh.md)。 |
| 文件路径或 `file://` URL | 导入这些文件，效果与 `程序`（Program）→ `添加文件中的配置档`（Add profile from File(s)）相同。 |
| `--headless` | 以无窗口方式运行 Throne，作为服务或在容器中运行（自 1.4.0 起）。参见[无界面 Throne](@/headless/_index.zh.md)。 |
| `--check`、`--health`、`--print-connection` | 检查这台电脑能否运行无界面 Throne、询问正在运行的无界面 Throne 的状态，或打印 `thronectl` 所需的设置（自 1.4.0 起）。 |

示例：

```bash
/opt/Throne/Throne -appdata
./Throne -appdata "$HOME/throne-test"
./Throne -tray
```

```powershell
.\Throne.exe -appdata D:\ThroneData
```

- Throne 会把 `-appdata` 后面的词当作文件夹，除非它以 `-` 开头。
- 每个数据文件夹只能运行一个 Throne。如果 Throne 已在运行，新启动的实例会把它收到的链接或文件交给正在运行的 Throne，将其窗口调到前台，然后退出。如果某个无界面 Throne 正在使用该数据文件夹，新启动的实例会显示“Throne is running in the background”（Throne 正在后台运行）并退出；参见[故障排除](@/help/troubleshooting.zh.md#background-throne)。
- 无界面 Throne 有更多选项，也有自己的数据文件夹。参见[命令行与数据目录](@/headless/command_line.zh.md)。
- **macOS：** 要传递选项，请运行应用包内的程序，例如 `/Applications/Throne.app/Contents/MacOS/Throne -tray`。你点击的链接会由 macOS 交给正在运行的 Throne。

## 数据文件夹 {#data-folder}

Throne 将你的数据保存在一个名为 `config` 的文件夹中。要打开它，请选择 `设置`（Settings）→ `打开配置文件夹`（Open Config Folder）（仅在高级模式下可用，参见[简洁模式与高级模式](@/get_started/configuration.zh.md#interface-mode)）。

Throne 有两种工作模式：

- **便携模式：** `config` 文件夹位于 Throne 程序文件夹中。
- **Appdata 模式：** `config` 文件夹位于你的用户文件夹中。Throne 在以下情况下使用此模式：以 `-appdata` 启动时、在 macOS 上（始终如此），以及无法写入自己的文件夹时。

在 appdata 模式下，该文件夹位于：

| 系统 | 数据文件夹 |
| --- | --- |
| Windows | `%LOCALAPPDATA%\Throne\config`，例如 `C:\Users\<you>\AppData\Local\Throne\config` |
| Linux | `~/.config/Throne/config`；如果你设置了 `XDG_CONFIG_HOME`，则为 `$XDG_CONFIG_HOME/Throne/config` |
| macOS | `~/Library/Preferences/Throne/config` |

你的 Throne 使用哪种模式，取决于它的安装方式：

| Throne 的安装方式 | 模式 | 数据文件夹 |
| --- | --- | --- |
| Windows ZIP | 便携 | 解压出的 `Throne` 文件夹中的 `config` |
| Windows 安装程序，为当前用户安装（默认） | 便携 | 安装文件夹中的 `config`，默认为 `%LOCALAPPDATA%\Throne\config` |
| Windows 安装程序，为所有用户安装 | Appdata（自动） | 每个用户各自的 `%LOCALAPPDATA%\Throne\config` |
| Linux ZIP | 便携 | 解压出的 `Throne` 文件夹中的 `config` |
| Linux `.deb`、`.rpm` 或安装脚本 | Appdata | `~/.config/Throne/config` |
| macOS | Appdata | `~/Library/Preferences/Throne/config` |

- `.deb` 和 `.rpm` 软件包以及 Linux 安装脚本所创建的应用菜单项，启动的是 `/opt/Throne/Throne -appdata`。
- 如果 Throne 无法写入自己的文件夹（例如位于 `Program Files` 中时），它会自动切换到 appdata 模式。第一次切换时，它会把你现有的 `config` 文件夹复制过去。此后，即使你以管理员身份运行，它也会继续使用这个用户专属文件夹。
- 来自其他来源的软件包（WinGet、Scoop、AUR、Nix）可能使用其他文件夹。`打开配置文件夹`（Open Config Folder）总会打开正确的那个。

有少数文件存放在 `config` 文件夹旁边，而不是其中：Xray 的 geo 文件 `geoip.dat` 和 `geosite.dat`，以及存放 `基本设置`（Basic Settings）→ `诊断`（Diagnostics）所生成文件的 `diagnostics` 文件夹。在便携模式下，这个位置是 Throne 程序文件夹；在 appdata 模式下，则是用户专属文件夹，例如 `%LOCALAPPDATA%\Throne`。如果你通过 `-appdata` 指定了其他文件夹，自 1.4.0 起就是那个文件夹；首次启动时，Throne 会把 geo 文件从用户专属文件夹复制过去。1.4.0 之前，这些文件始终留在用户专属文件夹中。

### 配置文件夹中的文件 {#config-files}

| 文件或文件夹 | 内容 |
| --- | --- |
| `throne.db` | 你的配置档、分组、路由配置档、OTP 配置档和设置，保存在一个 SQLite 数据库中。Throne 运行期间，它旁边会出现 `throne.db-wal` 和 `throne.db-shm`。 |
| `throne_stats.db` | `工具`（Tools）→ `流量统计`（Traffic Stats）所用的流量历史：最近 48 小时的每分钟数据，以及 90 天的每小时数据。`基本设置` → `样式`（Style）→ `禁用流量聚合`（Disable Traffic Aggregation）可以停止记录。 |
| `cache.db` | 核心的缓存：已下载的规则集、自动选择器上一次的选择；如果开启了 `保存缓存到文件`（Save Cache To File），还包括 DNS 缓存。 |
| `logs/` | 日志文件。参见[日志](#logs)。 |
| `crashes/` | 崩溃转储（仅限 Windows）。保留最新的 5 个。 |
| `icons/` | 来自 `基本设置` → `样式` → `启用自定义图标`（Enable Custom Icons）的自定义托盘图标：`Off.png`、`Throne.png`（有配置档运行）、`Proxy.png`、`Tun.png`，以及自 1.4.0 起的 `Connecting.png`。没有 `Connecting.png` 时，配置档启动或停止期间 Throne 会显示 `Off.png`。 |
| `hwid` | 仅限 Linux，自 1.4.0 起：由于系统中没有可用的 `/etc/machine-id` 或 `/var/lib/dbus/machine-id`，Throne 自行创建的设备 ID。参见 [HWID](@/reference/privacy.zh.md#hwid)。 |
| `.lock` | 自 1.4.0 起：表示有一个 Throne 正在使用此文件夹。Throne 从不删除它。 |
| `dashboard/` | 用于 Clash API 的网络仪表盘文件。Throne 创建该文件夹时会放入一个占位页面；请将它替换为仪表盘文件。 |
| `sb-dashboard/` | `工具` → `打开网络仪表盘`（Open Web dashboard）所打开的网络仪表盘。 |

要把数据迁移到另一台电脑或 Android 上，请创建 `.thrbackup` 备份，而不是复制文件。参见[备份与恢复](@/guides/backup.zh.md#backup-restore)。

## 日志 {#logs}

主窗口底部的 `日志`（Logs）标签页显示来自 Throne 和核心的消息。右键点击日志可以复制文本，或选择 `清除`（Clear）将其清空。

- **滚动：** 当你位于底部时，标签页会显示每一行新日志。自 1.4.0 起，当你向上滚动时，视图会停留在原处，新的行会等待显示。标签页右上角的 `回到最新`（Jump to latest）按钮会显示有多少行在等待；点击它或滚动回底部即可看到这些行。
- **筛选：** 自 1.4.0 起，标签页右上角的筛选按钮会打开一个筛选栏。在 `筛选日志`（Filter logs）中输入文字，即可只显示匹配的行，并高亮匹配的内容。`区分大小写`（Match case）和 `正则表达式`（Regular expression）会改变文字的匹配方式，筛选栏还会显示有多少行匹配。按 `Esc` 或再次点击筛选按钮会关闭筛选栏，并重新显示所有行。此筛选只改变显示，不会改变 Throne 保留的行。

日志设置位于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `日志`（Logging）（仅在高级模式下可用）：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `最多日志行数`（Max log lines） | `500`（1.4.0 之前为 `200`） | `日志` 标签页保留的行数。 |
| `Sing-box 日志级别`（Sing-box Log level） | `info` | 核心写入日志的详细程度：`trace`、`debug`、`info`、`warn`、`error`、`fatal` 或 `panic`。 |
| `Xray 日志级别`（Xray Log level） | `warning` | Xray 写入日志的详细程度：`debug`、`info`、`warning`、`error` 或 `none`。 |
| `日志筛选`（Log Filtering） | 关闭 | `启用「包含」规则`（Enable Include Rules）只显示与你的关键词或正则表达式匹配的行；`启用「排除」规则`（Enable Exclude Rules）会隐藏匹配的行。被这些规则隐藏的行永远不会出现在 `日志` 标签页中，但仍会保留在日志文件中。 |

`自动滚动日志`（Auto-scroll log）设置已在 1.4.0 中移除。

自 1.4.0 起，`日志` 标签页使用等宽字体。要选择其他字体，请使用 `设置`（Settings）→ `基本设置`（Basic Settings）→ `样式`（Style）中的 `日志浏览器字体`（Log Browser Font）和 `日志浏览器字体大小`（Log Browser Font Size）（仅在高级模式下可用）。列表中只显示等宽字体。默认情况下，Throne 会使用 Consolas、Menlo、SF Mono、DejaVu Sans Mono、Noto Sans Mono 和 Ubuntu Mono 中第一个已安装的字体，字号与界面字体相同。

如需提交 Bug 报告，请将 `Sing-box 日志级别`（Sing-box Log level）设为 `debug`，重新启动配置档，然后复现问题。之后请按照[报告 Bug](@/help/bug_reports.zh.md#logs) 中的说明操作。

### 日志文件 {#log-file}

Throne 还会把日志写入配置文件夹中的 `logs/throne.log`。

- 文件开头记录了 Throne 版本、你的操作系统、命令行选项和日志文件夹。
- 它包含 `日志`（Logs）标签页中的全部内容，以及来自 Throne 本身的更多细节。
- Throne 每次启动都会新建一个文件。文件达到 4 MB 时，Throne 会将其重命名为 `throne.log.1`，然后开始写入新文件。它最多保留三个旧文件，即 `throne.log.1` 到 `throne.log.3`。
- 如果 Throne 没有正常退出，它会把那次会话的日志以 `crashed-YYYYMMDD-HHMMSS.log` 的名称保存在同一文件夹中，并保留最新的 5 个。下次启动时，`日志`（Logs）标签页会显示“[警告] 上次 Throne 没有正常干净的关闭。诊断信息已被保存到： …”，后面接着是日志文件夹的路径。

{% alert_warning() %}
日志中可能包含你访问过的域名和你的服务器地址。公开分享日志之前，请先检查一遍。
{% end %}

**Android：** 打开侧边菜单并点按 `日志`（Logs）。`分享日志`（Share logs）和 `保存日志…`（Save logs…）可以导出日志。`隐藏敏感数据`（Hide sensitive data）默认开启，它会在导出的内容中隐藏密码、密钥、UUID、服务器名称、公网 IP 地址、Wi-Fi 名称以及 URL 中的路径。日志级别位于 `设置`（Settings）→ `核心`（Core）→ `日志级别`（Log level），默认为 `warn`。参见 [Android 故障排除](@/android/troubleshooting.zh.md#logs)。

## 重置 Throne {#reset}

Throne 没有重置按钮。要使用默认设置从头开始，请给 Throne 一个全新的空配置文件夹：

1. 如果想保留某些内容，请先创建备份：`设置`（Settings）→ `基本设置`（Basic Settings）→ `备份和恢复`（Backup and Restore）→ `创建备份...`（Create Backup...）。
2. 选择 `设置`（Settings）→ `打开配置文件夹`（Open Config Folder），查看该文件夹的位置。
3. 通过托盘菜单或 `程序`（Program）菜单中的 `退出`（Exit）退出 Throne。仅关闭窗口是不够的。
4. 重命名 `config` 文件夹，例如改为 `config-old`。
5. 启动 Throne。它会创建一个使用默认设置的新 `config` 文件夹。

要恢复部分旧数据，请在同一标签页中使用 `从备份恢复...`（Restore from Backup...），并只选择你需要的部分。参见[备份与恢复](@/guides/backup.zh.md#backup-restore)。

要撤销重置，请退出 Throne，删除新的 `config` 文件夹，并将 `config-old` 改回 `config`。

重置不会改变存放在配置文件夹之外的内容：`随系统启动`（Start with system）在操作系统中创建的自启动项、`throne://` 链接的注册，以及 Xray geo 文件。

**Windows：** 如果你是用安装程序安装的 Throne，卸载时会询问“Also delete your Throne profiles, settings and logs?”（是否同时删除你的 Throne 配置档、设置和日志？）。选择 `Yes` 即可同时删除配置文件夹。

**Android：** `设置`（Settings）→ `恢复默认设置`（Restore default settings）会重置所有设置，但保留你的配置档、分组和路由配置档。随后应用会重新启动。要删除所有内容，请在 Android 的应用设置中清除该应用的数据。Throne for Android 将数据保存在应用的私有存储中，文件管理器无法打开，因此请使用 `.thrbackup` 备份把数据复制出来。
