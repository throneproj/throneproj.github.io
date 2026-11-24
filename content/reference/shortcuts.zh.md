+++
title = "键盘快捷键与托盘"
description = "Throne 桌面版的键盘快捷键、搜索设置、全局热键和托盘图标。"
weight = 20
toc = true
+++

快捷键在 Throne 窗口处于活动状态时生效。**macOS：** `Ctrl` 指 `Cmd`，`Alt` 指 `Option`，因此 `Ctrl+Shift+S` 即 `Cmd+Shift+S`。在 Mac 笔记本键盘上，`Del` 为 `Fn+Delete`。

## 主窗口 {#main-window}

`设置`（Settings）和 `路由`（Routing）菜单没有默认快捷键。“可更改”一列表示能否设置其他快捷键，参见[更改快捷键](#change-shortcuts)。

在状态栏中，点击正在运行的配置档可以对它进行 URL 测试，点击 `Mixed: …` 可以打开 `基本设置`（Basic Settings）。

### 程序菜单 {#program-menu}

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `隐藏窗口`（Hide window） | `Ctrl+H`（macOS 上还可用 `Cmd+W`） | 是 |
| `新建配置档`（New profile） | `Ctrl+N` | 是 |
| `从剪贴板粘贴`（Paste from clipboard） | `Ctrl+V` | 否 |
| `从文件导入`（Import from file） | `Ctrl+O` | 是 |
| `扫描二维码`（Scan QR code） | `Ctrl+Shift+Q` | 是 |

你也可以把文件、二维码图片或链接拖放到窗口上来导入它们。

### 分组菜单 {#groups-menu}

分组操作作用于当前打开的标签页所对应的分组。

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `更新订阅`（Update subscription） | `Ctrl+U` | 是 |
| `测试`（Test）→ `URL 测试`（URL test） | `Ctrl+Shift+G` | 是 |
| `测试` → `速度测试`（Speed test） | `Ctrl+Alt+P` | 是 |
| `测试` → `解析域名`（Resolve domains） | `Ctrl+Shift+I` | 是 |
| `测试` → `停止测试`（Stop testing） | `Ctrl+.` | 是 |
| `测试` → `清除结果`（Clear results） | `Ctrl+Shift+C` | 是 |

`停止测试`（Stop testing）仅在测试运行时可用。右键点击分组标签页可以打开该分组的菜单；拖动标签页可以调整分组的顺序。

### 工具菜单 {#tools-menu}

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `Search Settings` | `Ctrl+K` | 是 |
| `速度测试当前连接`（Speed test current connection） | `F6` | 是 |

`搜索设置`（Search Settings）会打开[搜索设置](#command-palette)窗口。`速度测试当前连接`（Speed test current connection）仅在有配置档运行时可用。

## 搜索设置 {#command-palette}

`搜索设置`（Search Settings）可以按名称查找菜单命令和设置。在主窗口中按 `Ctrl+K`，或点击 `工具`（Tools）→ `搜索设置`。

- 输入一个或多个词。如果某一项的名称或路径包含所有这些词，它就会被匹配，例如 `基本设置 › 连接 › 本地代理`。在翻译后的界面中，输入英文单词也能找到许多项。
- 以 `>` 开头只搜索命令，以 `@` 开头只搜索设置。只输入 `@` 会列出所有设置。
- 按 `Enter` 或双击某一项即可运行它。`Esc` 会关闭该窗口。

它可以找到 `基本设置`（Basic Settings）、`路由设置`（Routing Settings）、`Tun 设置`（Tun Settings）、`预设设置`（Preset Settings）和 `Integration Settings` 中的设置，以及菜单当前显示的命令，包括配置档列表的菜单和你的路由配置档。

以下窗口同一时间只能打开一个：设置窗口、`管理分组`（Manage Groups）、`OTP 管理器`（OTP Manager）、`流量统计`（Traffic Statistics）和 `关于`（About）。当其中一个窗口打开时，`搜索设置` 会将会打开其他窗口的项显示为灰色。

## 配置档列表 {#profile-list}

右键点击配置档可以打开它的菜单。右键点击列表中的空白区域，则可以使用 `新建配置档`（New profile）、`从剪贴板粘贴`（Paste from clipboard）、`从文件导入`（Import from file）、`扫描二维码`（Scan QR code）、`添加订阅`（Add subscription）和 `全选`（Select all）。

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `启动`（Start） | `Enter` | 否 |
| `停止`（Stop） | `Ctrl+S` | 是 |
| `测试`（Test）→ `URL 测试`（URL test） | `Ctrl+Shift+S` | 是 |
| `测试` → `速度测试`（Speed test） | `Ctrl+Shift+P` | 是 |
| `分享`（Share）→ `复制链接`（Copy link） | `Ctrl+C` | 否 |
| `分享` → `复制深度链接`（Copy deep link） | `Ctrl+Alt+C` | 否 |
| `分享` → `导出配置`（Export config） | `Ctrl+E` | 是 |
| `克隆`（Clone） | `Ctrl+D` | 是 |
| `置顶`（Pin to top）/ `取消置顶`（Unpin）（[置顶配置档](@/guides/testing.zh.md#pin)） | – | 是 |
| `重置流量`（Reset traffic） | `Ctrl+R` | 是 |
| `删除`（Delete） | `Del` | 否 |
| `全选`（Select all） | `Ctrl+A` | 否 |

列表中的其他按键和鼠标操作：

| 按键或操作 | 作用 |
| --- | --- |
| 双击配置档 | 打开配置档编辑器。 |
| `Esc` | 清除选择。在筛选行中则关闭筛选行。 |
| 拖动某一行 | 移动该配置档。筛选生效时无法移动。 |
| `Ctrl+F` | 显示或隐藏筛选行。隐藏筛选行会清除筛选条件。 |
| 在第一行按 `Up`，在筛选行按 `Down` | 在列表和筛选行之间移动。 |

### 没有默认快捷键的操作 {#no-default}

其他大多数菜单项都没有默认快捷键，但可以为它们设置，例如 `编辑`（Edit）、`置顶`（Pin to top）、`添加订阅`（Add subscription）、`服务检查`（Service check）、`出口 IP`（Exit IP）、`复制测试结果`（Copy test result）、`清理`（Clean up）中的命令、`管理分组`（Manage groups）、各个设置窗口、`工具`（Tools）菜单中的窗口、`出口方式`（Exit through）的各个选项、`屏蔽广告`（Block ads）、`路由查询`（Route lookup）、`切换 WARP`（Toggle WARP）、`重启核心`（Restart core）和 `刷新列宽`（Refresh column widths）。

## 更改快捷键 {#change-shortcuts}

1. 打开 `设置`（Settings）→ `Integration Settings` → `快捷键`（Shortcuts）。每个操作都会连同其菜单路径一起列出，例如 `分组 › 测试 › URL 测试`。
2. 点击某个操作旁边的输入框，然后按下新的组合键。`Backspace` 会删除快捷键。
3. 点击 `确定`（OK）。

上面标为“否”的快捷键以及 `Ctrl+F` 无法更改。如果某个组合键已被另一个操作或某个全局热键使用，窗口会写明冲突，并且在你更改其中一个之前不会保存。

## 全局热键 {#global-hotkeys}

全局热键在任何应用中都有效，即使 Throne 窗口已隐藏也是如此。所有全局热键默认都为空。

1. 打开 `设置`（Settings）→ `Integration Settings` → `Global Hotkeys`。
2. 点击某个热键的输入框，然后按下组合键。
3. 点击 `确定`（OK）。

| 热键 | 作用 |
| --- | --- |
| `显示/隐藏主窗口`（Trigger main window） | 显示主窗口；如果主窗口处于活动状态，则将其隐藏，与点击托盘图标相同。 |
| `管理分组`（Manage groups） | 打开 `管理分组`（Manage Groups）。 |
| `打开路由设置`（Open Routing Settings） | 打开 `路由设置`（Routing Settings）。 |
| `代理模式`（Proxy mode） | 在鼠标指针处打开 `代理模式` 菜单，其中包含 `系统代理`（System proxy）和 `Tun 模式`（Tun mode）。 |
| `切换系统代理`（Toggle system proxy） | 开启或关闭 `系统代理`。 |
| `Start/Stop Profile` | 停止正在运行的配置档；如果没有配置档在运行，则启动上次的配置档。 |
| `切换 Tun 模式`（Toggle Tun mode） | 开启或关闭 `Tun 模式`。 |

- 热键必须包含 `Ctrl`、`Alt` 或 `Meta`（macOS 上为 `Cmd`），除非它是 `F9` 这样的功能键。
- 已被其他程序或系统占用的组合键无法生效。点击 `确定`（OK）后，Throne 会列出它无法注册的热键。
- `Integration Settings` 窗口打开期间，全局热键会暂停工作。
- **Linux：** 全局热键可以在 X11 会话和 KDE Plasma Wayland 会话中使用（在 KDE Plasma 上，它们还会出现在系统设置的快捷键部分中，位于 `Throne` 下），但不能在其他 Wayland 会话中使用。

要通过宏键盘、Stream Deck 或脚本控制 Throne，请使用 [thronectl](@/advanced/api.zh.md#example-hotkey)。

## 托盘图标 {#tray}

Throne 会在系统托盘中显示一个图标（在 macOS 上位于菜单栏中）。当有配置档在运行，以及 `系统代理`（System proxy）或 `Tun 模式`（Tun mode）开启时，图标会发生变化。将鼠标悬停在图标上，可以查看正在运行的配置档和模式。

- **Windows 和 Linux：** 点击图标可以显示或隐藏窗口。右键点击图标可以打开托盘菜单。
- **macOS：** 点击图标可以打开托盘菜单。

关闭窗口并不会退出 Throne：它会继续在托盘中运行。要退出，请在托盘菜单或 `程序`（Program）菜单中选择 `退出`（Quit）。

**macOS：** 窗口隐藏时，Throne 不会在程序坞（Dock）中显示图标。如果你将 Throne 保留在程序坞中，点击它在程序坞中的图标，或从“访达”（Finder）中再次打开 Throne，即可显示窗口。

**Linux：** GNOME 只有在安装了 AppIndicator 扩展后才会显示托盘图标（[#1623](https://github.com/throneproj/Throne/issues/1623)）。没有托盘图标时，再次启动 Throne 即可找回隐藏的窗口。

### 托盘菜单 {#tray-menu}

托盘菜单的第一行显示已连接的配置档。它的 `程序`（Program）子菜单中有 `随系统启动`（Start with system）、`记住上次的配置档`（Remember last profile）和 `允许其他设备连接`（Allow other devices to connect），与主窗口的 `程序` 菜单相同。

| 菜单项 | 作用 |
| --- | --- |
| `连接`（Connect）/ `断开连接`（Disconnect） | 停止正在运行的配置档，或启动列表中选中的配置档；没有选中时启动上次的配置档，否则启动当前打开的分组中的第一个配置档。 |
| `配置档：<name>`（`Profile: <name>`） | 启动按分组选择或输入名称搜索到的配置档。没有可显示的配置档时，显示为 `选择配置档`（Select profile）。 |
| `路由：<name>`（`Routing: <name>`） | 将一个路由配置档设为活动配置档，并重新启动正在运行的配置档。 |
| `系统代理`（System proxy）、`Tun 模式`（Tun mode） | 开启或关闭这些模式，与主窗口中相同。 |
| `OTP 代码`（OTP codes） | 点击一个 OTP 条目即可复制它当前的代码。 |
| `显示窗口`（Show window） | 显示主窗口。 |
| `程序` → `记住上次的配置档` | 下次启动时，Throne 会重新启动退出时正在运行的配置档；如果之前开启了 `系统代理` 和 `Tun 模式`，也会重新开启它们。你自己停止的配置档不会被记住。 |
| `程序` → `允许其他设备连接` | 向你的网络开放本地代理端口，参见[局域网共享](@/guides/proxy_modes.zh.md#lan-sharing)。 |
| `重启`（Restart）→ `重启核心`（Restart core）、`重启程序`（Restart program） | 重启核心或 Throne 本身。 |
| `退出`（Quit） | 退出 Throne。 |

`随系统启动`（Start with system）会在你登录时启动 Throne。为此，Throne 在 Windows 上添加一个任务计划程序（Task Scheduler）任务，在 macOS 上添加一个登录项，在 Linux 上把带有 `-tray` 选项的 `Throne.desktop` 添加到 `~/.config/autostart`。在 Windows 和 macOS 上，除非开启了 `启动时隐藏主窗口`（Hide main window at startup），否则登录时会打开窗口。在 Windows 上，该任务会以标准用户身份启动 Throne，即使核心拥有[管理员权限](@/guides/tun_mode.zh.md#privileges-windows)也是如此。只有在使用 `以管理员身份重启`（Restart as administrator）这一后备方案之后，它才会以管理员身份启动 Throne，除非开启了 `始终以标准用户身份启动`（Always start as standard user）。

### 托盘设置 {#tray-settings}

位于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `通用`（General）→ `窗口`（Window）：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `启动时隐藏主窗口`（Hide main window at startup） | 关闭 | Throne 启动时只显示托盘图标，与命令行选项 `-tray` 相同。 |
| `禁用托盘`（Disable tray） | 关闭 | 移除托盘图标。此时关闭窗口就会退出 Throne。 |

{% alert_warning() %}
不要在开启 `启动时隐藏主窗口`（Hide main window at startup）或使用 `-tray` 的同时开启 `禁用托盘`（Disable tray）：Throne 启动后既没有窗口，也没有托盘图标。如果出现这种情况，请再次启动 Throne，正在运行的 Throne 会显示它的窗口。
{% end %}
