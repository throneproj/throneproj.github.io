+++
title = "键盘快捷键与托盘"
description = "Throne 桌面版的键盘快捷键、如何更改它们、全局热键，以及托盘图标及其菜单的作用。"
weight = 20
toc = true
+++

本页列出了 Throne 桌面版的键盘快捷键、可以设置的全局热键，以及托盘图标的作用。快捷键在 Throne 窗口处于活动状态时生效。全局热键在任何应用中都有效，即使 Throne 窗口已隐藏也是如此。

**macOS：** 本页中的 `Ctrl` 在 Mac 上指 `Cmd`，`Alt` 指 `Option`。例如，`Ctrl+Shift+S` 即 `Cmd+Shift+S`。在 Mac 笔记本键盘上，`Del` 为 `Fn+Delete`。

## 主窗口 {#main-window}

工具栏按钮 `程序`（Program）、`设置`（Settings）、`分组`（Groups）、`路由`（Routing）和 `工具`（Tools）用于打开主窗口的各个菜单。`设置`（Settings）和 `路由`（Routing）菜单没有快捷键。

“可更改”一列表示能否在 `设置`（Settings）→ `热键设置`（Hotkey Settings）中为该操作设置其他快捷键。参见[更改快捷键](#change-shortcuts)。

### 程序菜单 {#program-menu}

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `隐藏窗口`（Hide window） | `Ctrl+H`（macOS 上还可用 `Cmd+W`） | 是 |
| `新建配置档`（New profile） | `Ctrl+N` | 是 |
| `添加剪贴板中的配置档`（Add profile from clipboard） | `Ctrl+V` | 否 |
| `添加文件中的配置档`（Add profile from File(s)） | `Ctrl+O` | 是 |
| `扫描二维码`（Scan QR Code） | `Ctrl+Shift+Q` | 是 |

你也可以把文件、含二维码的图片或链接拖放到窗口上来导入它们。

### 分组菜单 {#groups-menu}

分组操作作用于当前打开的标签页所对应的分组。

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `URL 测试本组`（Url Test Group） | `Ctrl+Shift+G` | 是 |
| `速度测试本组`（Speedtest Group） | `Ctrl+Alt+P` | 是 |
| `为本组解析域名`（Resolve Domain for group） | `Ctrl+Shift+I` | 是 |
| `清除本组测试结果`（Clear Group test result） | `Ctrl+Shift+C` | 是 |
| `更新订阅`（Update subscription） | `Ctrl+U` | 是 |
| `移除重复项`（Remove Duplicates） | `Ctrl+Shift+D` | 是 |
| `移除不可用项`（Remove Unavailable） | `Ctrl+Shift+R` | 是 |
| `移除无效项`（Remove Invalid） | `Ctrl+Alt+I` | 是 |
| `停止测试`（Stop Testing） | `Ctrl+.` | 是 |

`停止测试`（Stop Testing）仅在测试运行时才会出现在菜单中。

右键点击分组标签页，即可打开该分组及其菜单。标签页菜单包含 `添加新分组`（Add new Group）、`编辑选定分组`（Edit selected Group）、`删除选定分组`（Delete selected Group）、`更新订阅`（Update subscription）、`URL 测试选定分组`（Url Test selected Group）和 `速度测试选定分组`（Speed Test selected Group）。拖动标签页可以调整分组的顺序。

### 工具菜单 {#tools-menu}

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `速度测试当前项`（Speedtest Current） | `F6` | 是 |

`速度测试当前项`（Speedtest Current）仅在有配置档运行时可用。

### 状态栏 {#status-bar}

- 点击状态栏左侧正在运行的配置档，可以对它进行 URL 测试。
- 点击状态栏中间的 `Mixed: …`，可以打开 `基本设置`（Basic Settings）。

## 配置档列表 {#profile-list}

右键点击配置档列表可以打开它的菜单。该菜单包含与 `程序`（Program）菜单相同的四个“添加”操作，另外还有以下操作：

| 操作 | 快捷键 | 可更改 |
| --- | --- | --- |
| `启动`（Start） | `Enter` | 否 |
| `停止`（Stop） | `Ctrl+S` | 否 |
| `分享`（Share）→ `导出 Sing-box 配置`（Export Sing-box config） | `Ctrl+E` | 是 |
| `分享` → `复制选定项的链接`（Copy links of selected） | `Ctrl+C` | 否 |
| `分享` → `复制选定项的链接 (深度链接)`（Copy links of selected (Deep Links)） | `Ctrl+Alt+C` | 否 |
| `删除`（Delete） | `Del` | 否 |
| `全选`（Select All） | `Ctrl+A` | 否 |
| `克隆`（Clone） | `Ctrl+D` | 是 |
| `URL 测试选定项`（Url Test Selected） | `Ctrl+Shift+S` | 是 |
| `速度测试选定项`（Speedtest Selected） | `Ctrl+Shift+P` | 是 |
| `重置流量`（Reset Traffic） | `Ctrl+R` | 是 |

列表中的其他按键和鼠标操作：

| 按键或操作 | 作用 |
| --- | --- |
| 双击配置档 | 打开配置档编辑器。 |
| `Esc` | 清除选择。 |
| 拖动某一行 | 移动该配置档。筛选生效时无法移动。 |
| 点击列标题 | 按该列排序。再次点击则按相反方向排序。 |
| `Ctrl+F` | 显示或隐藏筛选行。隐藏筛选行会清除筛选条件。 |
| 在第一行按 `Up` | 移到筛选行（如果筛选行已打开）。 |
| 在筛选行按 `Down` | 返回列表。 |
| 在筛选行按 `Esc` | 关闭筛选行。 |

### 没有默认快捷键的操作 {#no-default}

以下操作默认没有快捷键，你可以为它们设置快捷键：`二维码和链接`（QR Code and link）、`复制测试结果`（Copy Test Result）、`解析选定域名`（Resolve Selected Domain）、`解析选定的出口 IP`（Resolve Selected Out IP）、`清理测试结果`（Clear Test Result）、`为本组解析 IP`（Resolve out IP for group）、`更新所有订阅`（Update all subscriptions）、`移除不安全的配置`（Remove Insecure Configs）和 `刷新列宽`（Refresh Column Widths）。

## 更改快捷键 {#change-shortcuts}

1. 打开 `设置`（Settings）→ `热键设置`（Hotkey Settings）。
2. 打开 `快捷键`（Shortcuts）标签页。其中列出了所有可以更改快捷键的操作。
3. 点击某个操作旁边的输入框，然后按下新的组合键。要删除快捷键，请点击输入框并按 `Backspace`。
4. 点击 `确定`（OK）。

如果两个操作使用相同的快捷键，则两者都不会生效。上面表格中标为“否”的快捷键无法更改，`Ctrl+F` 也无法更改。

## 全局热键 {#global-hotkeys}

全局热键在任何应用中都有效，即使 Throne 窗口已隐藏也是如此。所有全局热键默认都为空。

1. 打开 `设置`（Settings）→ `热键设置`（Hotkey Settings）。
2. 在 `全局`（Global）标签页中，点击某个热键的输入框。
3. 按下组合键。
4. 点击 `确定`（OK）。

| 热键 | 作用 |
| --- | --- |
| `显示/隐藏主窗口`（Trigger main window） | 显示主窗口；如果主窗口处于活动状态，则将其隐藏。与点击托盘图标的效果相同。 |
| `显示分组`（Show groups） | 打开 `管理分组`（Manage Groups）窗口。 |
| `显示路由`（Show routes） | 打开 `路由设置`（Routing Settings）。 |
| `代理模式`（Proxy mode） | 在鼠标指针处打开 `操作模式`（Operation Mode）菜单，其中包含 `系统代理`（System Proxy）和 `Tun 模式`（Tun Mode）。 |
| `切换系统代理`（Toggle System Proxy） | 开启或关闭 `系统代理`。 |

- 如果两个全局热键使用相同的按键，Throne 不会注册其中任何一个。
- 如果某个组合键已被其他程序占用，该热键将无法生效。请换一个组合键。
- `热键设置`（Hotkey Settings）窗口打开期间，全局热键会暂停工作。
- **macOS：** `显示/隐藏主窗口`（Trigger main window）不起作用。请改用托盘菜单中的 `显示窗口`（Show Window）。
- **Linux：** 全局热键使用 X11。在 Wayland 会话中它们可能无法工作。

## 托盘图标 {#tray}

Throne 会在系统托盘中显示一个图标。在 macOS 上，该图标位于菜单栏中。当有配置档正在运行，以及 `系统代理`（System Proxy）或 `Tun 模式`（Tun Mode）开启时，图标会发生变化。将鼠标悬停在图标上，可以查看正在运行的配置档及其地理位置。开启了某种模式时，提示信息中还会显示该模式；当活动的路由配置档不是 `Default` 时，也会显示该路由配置档。

- **Windows 和 Linux：** 点击图标可以显示窗口；如果窗口处于活动状态，则会将其隐藏。右键点击图标可以打开托盘菜单。
- **macOS：** 点击图标可以打开托盘菜单。

关闭窗口并不会退出 Throne。窗口会隐藏，Throne 继续在托盘中运行。要退出，请在托盘菜单或 `程序`（Program）菜单中选择 `退出`（Exit）。

**macOS：** 窗口隐藏时，Throne 不会在程序坞（Dock）中显示图标。

**Linux：** GNOME 只有在安装了 AppIndicator 扩展后才会显示托盘图标（[#1623](https://github.com/throneproj/Throne/issues/1623)）。即使没有托盘图标，你仍然可以找回隐藏的窗口：再次启动 Throne，正在运行的 Throne 就会显示它的窗口。

### 托盘菜单 {#tray-menu}

| 菜单项 | 作用 |
| --- | --- |
| `显示窗口`（Show Window） | 显示主窗口。 |
| `随系统启动`（Start with system） | 在你登录时启动 Throne。 |
| `记住上次的配置档`（Remember last profile） | 下次启动时，Throne 会重新启动上次运行的配置档；如果之前开启了 `系统代理` 和 `Tun 模式`，也会重新开启它们。 |
| `允许其他设备连接`（Allow other devices to connect） | 向你网络中的其他设备开放本地代理端口。参见[局域网共享](@/guides/proxy_modes.zh.md#lan-sharing)。 |
| `选择配置档`（Select Profile） | 打开一个列出你的分组的小列表。先选择一个分组，再选择其中的配置档即可启动它；也可以直接输入文字来搜索所有配置档。正在运行的配置档带有勾选标记，`停止: <name>`（`Stop: <name>`）按钮可以停止它。 |
| `选择路由`（Select Routing） | 列出你的路由配置档。选择其中一个会将其设为活动的路由配置档，并重新启动正在运行的配置档。 |
| `OTP 代码`（OTP Codes） | 列出你的 OTP 配置档。点击其中一个即可复制它当前的代码。 |
| `操作模式`（Operation Mode）→ `系统代理`、`Tun 模式` | 开启或关闭系统代理或 TUN 模式。 |
| `重启核心`（Restart Core） | 重新启动核心。 |
| `重启程序`（Restart Program） | 重新启动 Throne。 |
| `退出`（Exit） | 退出 Throne。 |

`随系统启动`（Start with system）在各个系统上的工作方式不同：

- **Windows：** Throne 会添加一个任务计划程序（Task Scheduler）任务。除非开启了 `启动时隐藏仪表盘`（Hide dashboard at startup），否则登录时会打开窗口。Throne 每次启动时，都会把该任务设置为与当前运行的 Throne 相同的权限：如果 Throne 以管理员身份运行，该任务也会以管理员身份启动它，除非开启了 `始终以标准用户身份启动`（Always Start as Standard User）。
- **Linux：** Throne 会把带有 `-tray` 选项的 `Throne.desktop` 添加到 `~/.config/autostart`，因此它会在托盘中启动。
- **macOS：** Throne 会添加一个登录项。除非开启了 `启动时隐藏仪表盘`（Hide dashboard at startup），否则登录时会打开窗口。

### 托盘设置 {#tray-settings}

这些设置位于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `样式`（Style）。

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `启动时隐藏仪表盘`（Hide dashboard at startup） | 关闭 | Throne 启动时只显示托盘图标，窗口保持隐藏。命令行选项 `-tray` 的效果相同。 |
| `禁用托盘`（Disable tray） | 关闭 | 移除托盘图标。此时关闭窗口就会退出 Throne。 |

{% alert_warning() %}
不要在开启 `启动时隐藏仪表盘`（Hide dashboard at startup）或使用 `-tray` 的同时开启 `禁用托盘`（Disable tray）。否则 Throne 启动后既没有窗口，也没有托盘图标。如果出现这种情况，请再次启动 Throne：正在运行的 Throne 会显示它的窗口。
{% end %}
