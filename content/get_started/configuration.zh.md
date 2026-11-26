+++
title = "快速入门"
description = "在 Windows、Linux 或 macOS 上使用 Throne 添加服务器、测试服务器、选择路由配置档并连接。"
weight = 2
toc = true
+++

你需要服务商提供的订阅链接或分享链接，或者你自己服务器的详细信息。Android 版请参阅 [Throne for Android](@/android/_index.zh.md#quick-start)。

{% alert_info() %}
没有服务器？Throne 可以免费通过 Cloudflare WARP 连接，无需任何配置：它会找到在你的网络上可用的端点。参见[无需服务器即可连接](@/advanced/warp.zh.md#no-server)。
{% end %}

## 添加服务器 {#add-servers}

Throne 将每个服务器保存为一个**配置档**。配置档属于**分组**，分组就是配置档列表上方的标签页。**订阅**是一种分组，Throne 从某个 URL 下载它，之后还可以更新。

### 添加订阅 {#paste-subscription}

1. 复制订阅 URL。它以 `https://` 开头。
2. 在主窗口中按 `Ctrl+V`（或点击 `程序`（Program）→ `从剪贴板粘贴`（Paste from clipboard））。
3. 选择 `创建新的订阅分组`（Create new subscription group），然后点击 `确定`（OK）。

Throne 会创建一个以 URL 中的主机名命名的分组，并下载其中的配置档。如果服务商发送了你的套餐信息，配置档列表上方会出现一张卡片，显示已用流量和到期日期。`添加配置档到这个分组`（Add profiles to this group）只会一次性导入配置档，不保存 URL，因此之后无法更新。

之后，你可以通过 `分组`（Groups）→ `更新订阅`（Update subscription）（`Ctrl+U`）更新当前分组。自动更新请参阅[订阅与分组](@/guides/subscriptions.zh.md#auto-update)。

### 添加单个配置档 {#single-profiles}

配置档会进入当前选中的标签页所对应的分组。

- **分享链接**，例如 `vless://`、`ss://` 或 `trojan://`：复制一条或多条链接（每行一条），然后按 `Ctrl+V`。
- **屏幕上的二维码**：`程序` → `扫描二维码`（Scan QR code，`Ctrl+Shift+Q`）。
- **文件和二维码图片**：将它们拖放到主窗口，或点击 `程序` → `从文件导入`（Import from file，`Ctrl+O`）。
- **手动添加**：`程序` → `新建配置档`（New profile，`Ctrl+N`）。

所有支持的链接和文件都列在[协议与导入格式](@/reference/protocols.zh.md#import-formats)中。

## 测试服务器 {#test-servers}

点击 `分组` → `测试`（Test）→ `URL 测试`（URL test，`Ctrl+Shift+G`）即可测量分组中所有配置档的延迟。如果只想测试部分配置档，请选中它们，右键点击并选择 `测试` → `URL 测试`（`Ctrl+Shift+S`）。

`测试结果`（Test Result）列以毫秒为单位显示延迟，或显示 `不可用`（Unavailable）。点击列标题可以排序。`分组` → `清理`（Clean up）→ `移除不可用项`（Remove unavailable）会删除测试失败的配置档；如果服务商仍然提供它们，订阅更新时会重新添加。

速度测试和自动选择服务器请参阅[测试与自动选择器](@/guides/testing.zh.md)。

## 选择路由 {#choose-routing}

这一步是可选的：内置路由配置档 `Default` 会让所有流量都经过代理。如果你希望本国网站直接打开：

1. 点击 `路由`（Routing）→ `下载路由配置档`（Download routing profile），然后选择 `China`、`Iran` 或 `Russia`。保持勾选 `自动更新`（Auto update），然后点击 `确定`。
2. 再次打开 `路由` 菜单，在顶部选择 `Bypass China`、`Bypass Iran` 或 `Bypass Russia`。正在运行的配置档会使用新的路由重新启动。

“Bypass”配置档会让除该国网站和 IP 地址以及你的本地网络之外的所有流量经过代理。其他下载的配置档和自定义规则请参阅[路由](@/guides/routing.zh.md#download-profiles)。

## 连接 {#connect}

1. 点击你想使用的配置档。
2. 按 `Enter`，或点击 `工具`（Tools）右侧的启动按钮。
3. 勾选启动按钮旁边的 `系统代理`（System proxy）或 `Tun 模式`（Tun mode）。

| 模式 | 作用 |
|---|---|
| `系统代理` | 将系统的代理设置指向 Throne（默认为 `127.0.0.1:2080`）。浏览器和其他遵循这些设置的应用会使用代理。 |
| `Tun 模式` | 捕获所有应用的流量，包括忽略代理设置的应用。需要管理员或 root 权限。 |

你可以同时开启两者。如果两者都不勾选，你自行设置的应用仍然可以通过 `127.0.0.1:2080` 将 Throne 用作 SOCKS5 或 HTTP 代理。参见[该用哪种模式](@/guides/proxy_modes.zh.md#which-mode)。

第一次勾选 `Tun 模式` 时，Throne 会请求所需的权限：

- **Windows：** 点击 `赋予特权`（Grant privileges），确认 Windows 的提示，然后再次勾选 `Tun 模式`。只有核心会获得[管理员权限](@/guides/tun_mode.zh.md#privileges-windows)；Throne 本身仍以标准用户身份运行。如果 Windows 防火墙询问 `ThroneCore`，请允许。
- **Linux：** 点击 `是`（Yes），输入你的密码，然后再次勾选 `Tun 模式`。
- **macOS：** 点击 `是`，在打开的“终端”（Terminal）窗口中输入你的密码，然后再次勾选 `Tun 模式`。

详细信息请参阅 [Tun 权限](@/guides/tun_mode.zh.md#privileges)。

### 检查连接 {#check-connection}

窗口左下角会显示正在运行的配置档，片刻之后还会显示你的出口 IP 地址所在的国家和城市。点击它可以测试连接：`测试结果: <n> ms`（`Test Result: <n> ms`）表示连接正常。如果显示 `不可用`（Unavailable），请尝试其他配置档，或参阅[故障排除](@/help/troubleshooting.zh.md)。

### 停止和退出 {#stop-and-quit}

- 要断开连接，请再次点击启动按钮（此时为 `停止`（Stop）），或者按 `Ctrl+S`。
- 关闭窗口只会将 Throne 隐藏到系统托盘。要退出，请使用 `程序` → `退出`（Quit），或托盘菜单中的 `退出`。
- `程序` → `记住上次的配置档`（Remember last profile）会在 Throne 启动时重新连接，`程序` → `随系统启动`（Start with system）会在你登录时启动 Throne。

{% alert_warning() %}
请始终使用 `退出` 来关闭 Throne。如果在 `系统代理` 开启时强行结束 Throne，系统会继续使用一个已不再运行的代理，网站将无法加载。参见[常见问题](@/help/faq.zh.md#force-quit)。
{% end %}

## 查找设置 {#find-setting}

要查找任意设置，请按 `Ctrl+K` 并输入其名称的一部分；选择其中一项即可打开它。参见[搜索设置](@/reference/shortcuts.zh.md#command-palette)。

## 后续步骤 {#next-steps}

- [订阅与分组](@/guides/subscriptions.zh.md)：自动更新，以及部分服务商要求的 User-Agent 和 HWID 设置。
- [路由](@/guides/routing.zh.md)：你自己的规则，例如只让少数网站经过代理。
- [测试与自动选择器](@/guides/testing.zh.md)：速度测试，以及自动切换到可用的服务器。
- [Tun 模式](@/guides/tun_mode.zh.md)和 [DNS](@/guides/dns.zh.md)：设置、副作用和泄漏测试。
- [故障排除](@/help/troubleshooting.zh.md)和[常见问题](@/help/faq.zh.md)：遇到问题时的帮助。
