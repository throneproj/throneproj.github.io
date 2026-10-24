+++
title = "快速入门"
description = "在 Windows、Linux 或 macOS 上使用 Throne 添加服务器、测试服务器、选择路由配置档并连接。"
weight = 2
toc = true
+++

本页将引导你从全新安装开始，一步步建立可用的连接。你需要服务商提供的订阅链接或分享链接，或者你自己服务器的详细信息。如果尚未安装 Throne，请参阅[安装](@/get_started/installation.zh.md)。Android 版请参阅 [Throne for Android](@/android/_index.zh.md#quick-start)。

自 1.4.0 起，全新安装会以简洁模式启动，该模式会隐藏高级选项。本页的所有步骤都可以在简洁模式下完成。参见[简洁模式与高级模式](#interface-mode)。

## 添加服务器 {#add-servers}

Throne 将每个服务器保存为一个**配置档**。配置档属于**分组**，分组就是配置档列表上方的标签页。**订阅**是一种分组，Throne 从某个 URL 下载它，之后还可以更新。

### 粘贴订阅链接 {#paste-subscription}

1. 复制订阅 URL。它以 `https://` 开头。
2. 在主窗口中按 `Ctrl+V`，或点击 `程序`（Program）→ `添加剪贴板中的配置档`（Add profile from clipboard）。
3. Throne 会询问“如何更新？”（How to update?）。在列表中选择 `创建新的订阅分组`（Create new subscription group），然后点击 `确定`（OK）。

Throne 会创建一个以 URL 中的主机名命名的分组，并立即下载其中的配置档。如果服务商发送了你的套餐信息，配置档列表上方会出现一张卡片，显示已用流量和到期日期（自 1.3.2 起）。参见[服务商信息](@/guides/subscriptions.zh.md#provider-info)。

另外两个选项不会创建订阅：

| 选项 | 作用 |
|---|---|
| `添加配置档到这个分组`（Add profiles to this group） | 将配置档一次性导入当前分组。Throne 不会保存该 URL，因此之后无法更新这些配置档。 |
| `导入 HTTP 代理配置档`（Import HTTP proxy profile） | 将该 URL 视为 HTTP 代理服务器的地址。 |

### 通过“分组”菜单添加订阅 {#groups-menu}

1. 点击 `分组`（Groups）→ `添加新分组`（Add new Group）。
2. 输入 `名称`（Name）。
3. 将 `类型`（Type）设为 `订阅`（Subscription）。类型之后无法更改。
4. 将订阅 URL 粘贴到 `URL` 中。
5. 点击 `确定`。
6. 右键点击新分组的标签页，选择 `更新订阅`（Update subscription）。

创建分组时不会下载任何内容，第 6 步才会下载。之后，你可以通过 `分组` → `更新订阅`（`Ctrl+U`）更新当前分组。自动更新和服务商相关设置请参阅[订阅与分组](@/guides/subscriptions.zh.md#auto-update)。

### 添加单个配置档 {#single-profiles}

通过以下方式添加的配置档会进入当前选中的标签页所对应的分组。

- **分享链接**，例如 `vless://`、`ss://` 或 `trojan://`：复制一条或多条链接（每行一条），然后按 `Ctrl+V`。
- **屏幕上的二维码**：点击 `程序` → `扫描二维码`（Scan QR Code，`Ctrl+Shift+Q`）。Throne 会读取你所有屏幕上的二维码。
- **文件和图片**：将配置文件、二维码图片或链接文本拖放到主窗口，或点击 `程序` → `添加文件中的配置档`（Add profile from File(s)，`Ctrl+O`）。
- **手动添加**：点击 `程序` → `新建配置档`（New profile，`Ctrl+N`）。

所有支持的链接和文件都列在[协议与导入格式](@/reference/protocols.zh.md#import-formats)中。

## 测试服务器 {#test-servers}

URL 测试会通过每个配置档建立连接并测量延迟。

1. 点击列表中的任意配置档，然后按 `Ctrl+A` 选中该分组的所有配置档。
2. 右键点击所选内容，选择 `URL 测试选定项`（Url Test Selected，`Ctrl+Shift+S`）。

要在不选中的情况下测试整个分组，请点击 `分组` → `URL 测试本组`（Url Test Group，`Ctrl+Shift+G`）。

`测试结果`（Test Result）列以毫秒为单位显示延迟；如果测试失败，则显示 `不可用`（Unavailable）。点击 `测试结果` 列标题可按该列排序，再次点击可反转排序顺序。

要删除测试失败的配置档，请点击 `分组` → `清理`（Clean up）→ `移除不可用项`（Remove Unavailable，`Ctrl+Shift+R`）。在 1.4.0 之前，`移除不可用项` 直接位于 `分组` 菜单中。在订阅分组中，如果服务商仍然提供这些配置档，下次更新时它们会被重新添加。

速度测试、IP 测试和自动选择服务器请参阅[测试与自动选择器](@/guides/testing.zh.md)。

## 选择路由 {#choose-routing}

路由决定哪些流量经过代理、哪些流量直接访问互联网。这一步是可选的：内置路由配置档 `Default` 会让所有流量都经过代理。

如果你希望本国网站不经代理直接打开，请下载一个现成的路由配置档：

1. 点击 `路由`（Routing）→ `下载配置档`（Download Profiles），然后选择 `China`、`Iran` 或 `Russia`。
2. Throne 会询问“添加这些远程路由配置档吗?”（Add these remote routing profiles?）并列出它们。保持勾选 `自动更新`（Auto update），然后点击 `确定`。
3. 再次打开 `路由` 菜单。你的路由配置档列在菜单底部，已勾选的那个就是当前生效的配置档。
4. 点击你想使用的路由配置档。如果有配置档正在运行，Throne 会使用新的路由重新启动它。

| 路由配置档 | 经过代理 | 直连 |
|---|---|---|
| `Bypass China`、`Bypass Iran`、`Bypass Russia` | 其他所有流量 | 该国的网站和 IP 地址，以及你的本地网络 |
| `Proxy China Blocked`、`Proxy Russia Blocked` | 仅在该国被封锁的网站 | 其他所有流量 |
| `Proxy Antizapret`、`Proxy Refilter`（俄罗斯） | 仅这些封锁列表中的网站 | 其他所有流量 |

同一时间只有一个路由配置档生效，因此请从中选择一个。你不需要删除 `Default` 或其他配置档。要编写自己的规则，请参阅[路由](@/guides/routing.zh.md)。

## 连接 {#connect}

1. 点击你想使用的配置档。
2. 按 `Enter`，或点击 `工具`（Tools）右侧的启动按钮。它的提示文字是 `启动`（Start）。
3. 勾选启动按钮旁边的 `系统代理`（System Proxy）或 `Tun 模式`（Tun Mode）。

| 模式 | 作用 |
|---|---|
| `系统代理` | 在配置档运行期间，将系统的代理设置指向 Throne 的本地端口（默认为 `127.0.0.1:2080`）。浏览器和其他遵循系统代理设置的应用会使用它。参见[系统代理](@/guides/proxy_modes.zh.md#system-proxy)。 |
| `Tun 模式` | 创建一个虚拟网卡，捕获所有应用的流量，包括忽略代理设置的应用。它需要管理员或 root 权限。参见 [TUN 模式](@/guides/proxy_modes.zh.md#tun-mode)。 |

你可以同时开启这两种模式，此时窗口标题会显示 `[Tun+系统代理]`（`[Tun+System Proxy]`）。如果两者都不勾选，你自行设置的应用仍然可以通过 `127.0.0.1:2080` 将 Throne 用作 SOCKS5 或 HTTP 代理。如何选择模式，请参阅[该用哪种模式](@/guides/proxy_modes.zh.md#which-mode)。

第一次勾选 `Tun 模式` 时，Throne 会请求所需的权限：

- **Windows：** Throne 会请你以管理员身份运行它。点击 `是`（Yes）并确认 Windows 的提示。Throne 会以管理员身份重新启动，并开启 `Tun 模式`。如果 Windows 防火墙询问是否允许 `ThroneCore`，请允许。
- **Linux：** Throne 会请求为其核心授予 root 权限。点击 `是` 并输入你的密码。然后再次勾选 `Tun 模式`。
- **macOS：** Throne 会请求为其核心授予 root 权限。点击 `是` 后会打开“终端”（Terminal）。在终端中输入你的密码，然后再次勾选 `Tun 模式`。

详细信息和其他方式请参阅 [TUN 权限](@/guides/tun_mode.zh.md#privileges)。

### 检查连接 {#check-connection}

窗口左下角会以 `[分组] 配置档` 的形式显示正在运行的配置档。片刻之后，其下方会显示你的出口 IP 地址所在的国家和城市，除非关闭了 `Look up exit country`（参见 [IP 与国家测试](@/guides/testing.zh.md#ip-test)）。

点击这段文字可以测试正在运行的配置档。如果连接正常，Throne 会显示 `测试结果: <n> ms`（`Test Result: <n> ms`）；如果连接失败，则显示 `测试结果: 不可用`（`Test Result: Unavailable`）。如果测试失败，请尝试其他配置档，或参阅[故障排除](@/help/troubleshooting.zh.md)。

### 停止和退出 {#stop-and-quit}

- 要断开连接，请再次点击同一个按钮，此时它的提示文字为 `停止`（Stop）；或者按 `Ctrl+S`。
- 关闭窗口只会将 Throne 隐藏到系统托盘。要退出，请点击 `程序` → `退出`（Exit），或使用托盘菜单中的 `退出`。
- 开启 `程序` → `记住上次的配置档`（Remember last profile）后，Throne 启动时会再次启动你上次使用的配置档；如果 `系统代理` 和 `Tun 模式` 之前处于开启状态，也会重新开启它们。`程序` → `随系统启动`（Start with system）会在你登录时启动 Throne。

{% alert_warning() %}
请始终使用 `退出` 来关闭 Throne。如果在配置档运行且 `系统代理` 开启时强行结束 Throne，系统会继续使用一个已不再运行的代理，网站将无法加载。参见[常见问题](@/help/faq.zh.md#force-quit)。
{% end %}

## 简洁模式与高级模式 {#interface-mode}

自 1.4.0 起，Throne 窗口有两种界面模式。**简洁**模式只显示大多数人需要的选项，隐藏其余选项。**高级**模式显示所有选项。全新安装会以简洁模式启动。从旧版本更新时，Throne 会保留完整界面，也就是高级模式。

简洁模式只是隐藏选项。被隐藏的设置会保留原值并继续生效，因此切换模式不会改变你的配置档或设置。

切换模式的方法：

1. 打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `样式`（Style）。
2. 将 `界面`（Interface）设为 `简洁`（Simple）或 `高级`（Advanced）。
3. 点击 `确定`（OK）。

主窗口和托盘菜单会立即改变。设置窗口会在你下次打开时显示新的模式。

要按名称查找设置，请按 `Ctrl+K` 并输入其名称中的几个字。在简洁模式下，这项搜索也会找到被隐藏的设置，并将它们列在“高级模式中的设置”（Settings in Advanced mode）下。选择其中一项后，Throne 会切换到高级模式并打开该设置。参见[命令面板](@/reference/shortcuts.zh.md#command-palette)。

### 简洁模式隐藏的内容 {#simple-mode-hidden}

在简洁模式下，以下菜单项会被隐藏：

| 菜单 | 隐藏的菜单项 |
|---|---|
| `设置`（Settings） | `预设设置`（Preset Settings）、`Integration Settings`、`打开配置文件夹`（Open Config Folder） |
| `分组`（Groups） | `为本组解析 IP`（Resolve out IP for group）、`为本组解析域名`（Resolve Domain for group） |
| `工具`（Tools） | `打开网络仪表盘`（Open Web dashboard）、`OTP 管理器`（OTP Manager）、`IP Scanner` |
| 配置档列表的菜单 | `分享`（Share）→ `导出配置`（Export config）、`分享` → `复制选定项的链接 (深度链接)`（Copy links of selected (Deep Links)）、`解析选定的出口 IP`（Resolve Selected Out IP）、`解析选定域名`（Resolve Selected Domain）、`重置流量`（Reset Traffic） |
| 托盘菜单 | `OTP 代码`（OTP Codes） |

主窗口底部的 `运行时统计`（Runtime Stats）标签页也会被隐藏。

在设置窗口中，简洁模式会隐藏以下选项：

- `基本设置`（Basic Settings）：`日志`（Logging）和 `核心`（Core）标签页。在 `通用`（Common）中，除 `监听端口`（Listen Port）、`延迟测试 URL`（Latency Test URL）和 `Look up exit country` 外的所有选项。在 `订阅`（Subscription）中，除 `更新订阅前清除服务器`（Clear servers before updating subscription）和 `订阅自动更新`（Subscription auto update）外的所有选项。在 `样式`（Style）中，日志字体、`连接统计`（Connection statistics）和自定义图标。在 `杂项`（Miscellaneous）中，除 `使用代理`（Use proxy）和 `允许更新到 beta 版`（Allow updating to beta versions）外的所有选项。在 `安全`（Security）中，除 `Kill Switch` 外的所有选项。
- `路由设置`（Routing Settings）：`默认域策略`（Default Domain Strategy）、`解析域策略`（Resolve Domain Strategy）和 `远程规则集镜像`（Remote Rule-set Mirror），WARP 配置字段和 `注册域名...`（Registration Domains…），以及除 `远程 DNS`（Remote DNS）、`直连 DNS`（Direct DNS）和 `默认 DNS 服务器`（Default DNS server）外的所有 DNS 选项。
- `Tun 设置`（Tun Settings）：`MTU`、`自动重定向`（Auto Redirect）、`L3 桥接绕过`（L3 Bridge Bypass）、`Tun 地址`（Tun Address）和 `私有地址范围绕过`（Private Range Bypass）。
- 分组编辑器：`前置代理`（Front Proxy）、`落地代理`（Landing Proxy）和 `高级`（Advanced）按钮。
- 配置档编辑器：`高级设置`（Advanced Settings）按钮、TLS 分片和 TLS 技巧选项、`多路复用`（Multiplex）中的 `Custom` 选项、Xray 的 `最终掩码`（Finalmask），以及 XHTTP 和 XDrive 的高级分组。新建配置档时，`类型`（Type）列表中没有 `直连`（Direct）、`链式代理`（Chain Proxy）、`额外核心`（Extra Core）和各种自定义类型。
- 路由配置档编辑器：包含规则列表的 `高级`（Advanced）标签页、`DNS` 标签页和 `端点`（Endpoints）标签页，除非该配置档已经在使用它们。

有几个开关在开启时仍会显示，以便你将其关闭：`随机端口`（Random port）、`禁用混合入站`（Disable Mixed Inbound）、`启用自定义图标`（Enable Custom Icons）和 `使用自定义 DNS 对象`（Use Custom DNS Object）。

简洁模式还会把一些标签页并入其他标签页，因此本文档提到的某个标签页可能是另一个标签页中的一个区域：

- `基本设置`：`订阅` 和 `安全` 标签页，以及 `杂项` 中的 `网络设置`（Network Settings）分组，会成为 `通用` 标签页底部的区域。该窗口的标签页为 `通用`、`样式`、`备份和恢复`（Backup and Restore）和 `诊断`（Diagnostics）。
- `路由设置`：`Warp` 标签页和 `DNS` 标签页中的 `简易 DNS 设置`（Simple DNS Settings）分组会成为 `通用`（Common）标签页中的区域。该窗口的标签页为 `通用` 和 `路由`（Route）。开启 `使用自定义 DNS 对象` 时，`DNS` 标签页保持不变。

## 后续步骤 {#next-steps}

- [订阅与分组](@/guides/subscriptions.zh.md)：自动更新，以及部分服务商要求的 User-Agent 和 HWID 设置。
- [路由](@/guides/routing.zh.md)：你自己的规则，例如只让少数网站经过代理。
- [测试与自动选择器](@/guides/testing.zh.md)：速度测试，以及自动切换到可用的服务器。
- [TUN 模式](@/guides/tun_mode.zh.md)：TUN 设置及其副作用。
- [DNS](@/guides/dns.zh.md)：DNS 服务器和泄漏测试。
- [故障排除](@/help/troubleshooting.zh.md)和[常见问题](@/help/faq.zh.md)：遇到问题时的帮助。
