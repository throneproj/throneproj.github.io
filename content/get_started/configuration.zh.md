+++
title = "快速入门"
description = "在 Windows、Linux 或 macOS 上使用 Throne 添加服务器、测试服务器、选择路由配置档并连接。"
weight = 2
toc = true
+++

本页将引导你从全新安装开始，一步步建立可用的连接。你需要服务商提供的订阅链接或分享链接，或者你自己服务器的详细信息。如果尚未安装 Throne，请参阅[安装](@/get_started/installation.zh.md)。Android 版请参阅 [Throne for Android](@/android/_index.zh.md#quick-start)。

## 添加服务器 {#add-servers}

Throne 将每个服务器保存为一个**配置档**。配置档属于**分组**，分组就是配置档列表上方的标签页。**订阅**是一种分组，Throne 从某个 URL 下载它，之后还可以更新。

### 粘贴订阅链接 {#paste-subscription}

1. 复制订阅 URL。它以 `https://` 开头。
2. 在主窗口中按 `Ctrl+V`，或点击 `程序`（Program）→ `添加剪贴板中的配置档`（Add profile from clipboard）。
3. Throne 会询问“如何更新？”（How to update?）。在列表中选择 `创建新的订阅分组`（Create new subscription group），然后点击 `确定`（OK）。

Throne 会创建一个以 URL 中的主机名命名的分组，并立即下载其中的配置档。

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

要删除测试失败的配置档，请点击 `分组` → `移除不可用项`（Remove Unavailable，`Ctrl+Shift+R`）。在订阅分组中，如果服务商仍然提供这些配置档，下次更新时它们会被重新添加。

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

窗口左下角会以 `[分组] 配置档` 的形式显示正在运行的配置档。片刻之后，其下方会显示你的出口 IP 地址所在的国家和城市。

点击这段文字可以测试正在运行的配置档。如果连接正常，Throne 会显示 `测试结果: <n> ms`（`Test Result: <n> ms`）；如果连接失败，则显示 `测试结果: 不可用`（`Test Result: Unavailable`）。如果测试失败，请尝试其他配置档，或参阅[故障排除](@/help/troubleshooting.zh.md)。

### 停止和退出 {#stop-and-quit}

- 要断开连接，请再次点击同一个按钮，此时它的提示文字为 `停止`（Stop）；或者按 `Ctrl+S`。
- 关闭窗口只会将 Throne 隐藏到系统托盘。要退出，请点击 `程序` → `退出`（Exit），或使用托盘菜单中的 `退出`。
- 开启 `程序` → `记住上次的配置档`（Remember last profile）后，Throne 启动时会再次启动你上次使用的配置档；如果 `系统代理` 和 `Tun 模式` 之前处于开启状态，也会重新开启它们。`程序` → `随系统启动`（Start with system）会在你登录时启动 Throne。

{% alert_warning() %}
请始终使用 `退出` 来关闭 Throne。如果在配置档运行且 `系统代理` 开启时强行结束 Throne，系统会继续使用一个已不再运行的代理，网站将无法加载。参见[常见问题](@/help/faq.zh.md#force-quit)。
{% end %}

## 后续步骤 {#next-steps}

- [订阅与分组](@/guides/subscriptions.zh.md)：自动更新，以及部分服务商要求的 User-Agent 和 HWID 设置。
- [路由](@/guides/routing.zh.md)：你自己的规则，例如只让少数网站经过代理。
- [测试与自动选择器](@/guides/testing.zh.md)：速度测试，以及自动切换到可用的服务器。
- [TUN 模式](@/guides/tun_mode.zh.md)：TUN 设置及其副作用。
- [DNS](@/guides/dns.zh.md)：DNS 服务器和泄漏测试。
- [故障排除](@/help/troubleshooting.zh.md)和[常见问题](@/help/faq.zh.md)：遇到问题时的帮助。
