+++
title = "Cloudflare WARP"
description = "将 Cloudflare WARP 添加为代理之后的额外出口：生成配置、开启 WARP，并让指定流量绕过它。"
weight = 40
toc = true
+++

WARP 是 Cloudflare 的免费 VPN 服务。Throne 可以在你的代理之后加上 WARP，作为额外的一跳。这样网站看到的是 Cloudflare 的地址，而不是你的代理服务器的地址。这对那些封锁 VPN 或数据中心地址的网站很有帮助。

## WARP 在 Throne 中的工作方式 {#how-it-works}

开启 WARP 后，流量路径为：你的设备 → 你启动的配置档 → WARP → 互联网。

- WARP 适用于你启动的每个配置档，包括代理链和自动选择器。只有 `自定义 (sing-box 配置)`（Custom (sing-box config)）配置档不经过 WARP。如果分组设置了落地代理，WARP 位于落地代理之后。
- WARP 的流量要经由你的代理传输，因此代理必须能承载 WARP 的流量：
  - `WireGuard` 模式使用 UDP，配置档必须能转发 UDP。
  - 基于 HTTP/3 的 `MASQUE` 模式同样需要 UDP；基于 HTTP/2 的 MASQUE 只需要 TCP。
- 规则和默认出站可以让流量只经过你的代理而不经过 WARP。参见[让部分流量绕过 WARP](#warp-bypass)。

设置 WARP 分两步：先生成一次配置，然后开启 WARP。

## 生成 WARP 配置 {#generate}

1. 打开 `路由`（Routing）→ `路由设置`（Routing Settings）。
2. 打开 `Warp` 标签页。
3. 选择 `模式`（Mode）：`WireGuard` 或 `MASQUE`。
4. 点击 `生成 Warp 配置`（Generate Warp Config）。
5. 首次生成时，Throne 会询问你是否接受 Cloudflare WARP 服务条款。点击 `是`（Yes）。
6. 等待按钮上显示“成功!”（Success!）。此时所选模式的各字段均已填好。
7. 点击 `确定`（OK）。

每种模式都有各自的字段。如果之后切换了 `模式`，也需要为该模式生成配置。

| 模式 | 字段 |
| --- | --- |
| `WireGuard` | `端点`（Endpoint）、`私钥`（Private Key）、`公钥`（Public Key）、`接口地址`（Interface Addresses）、`保留`（Reserved） |
| `MASQUE` | `端点`、`私钥`、`对端公钥`（Peer Public Key）、`接口地址`、`SNI`、`HTTP 版本`（HTTP Version） |

MASQUE 的 `HTTP 版本` 可以是 `HTTP/3 (回退到 HTTP/2)`（HTTP/3 (fallback to HTTP/2)，默认）、`仅 HTTP/3`（HTTP/3 only）或 `HTTP/2`。HTTP/3 基于 UDP 运行；HTTP/2 基于 TCP 上的 TLS 运行，在 UDP 被封锁的网络中也能工作。

每次生成都会在 Cloudflare 注册一台新设备。

### 如果注册失败 {#registration-fails}

Cloudflare 的注册服务器 `api.cloudflareclient.com` 在一些国家被封锁（[#1874](https://github.com/throneproj/Throne/issues/1874)）。这种情况下，请通过你的代理进行注册：

1. 启动一个可用的配置档。
2. 打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `杂项`（Miscellaneous），勾选 `使用代理`（Use proxy）。如果已开启 `系统代理`（System Proxy），Throne 自身的请求已经会经过代理。
3. 再次点击 `生成 Warp 配置`。

如果在开启了 `使用代理` 或 `系统代理` 的情况下没有运行任何配置档，生成会失败，并提示“有用代理的请求，但未启动配置档。”（Request with proxy but no profile started.）

`注册域名...`（Registration Domains…）中保存 Cloudflare API 的域名，每行一个。Throne 会按顺序尝试，并使用第一个接受注册的域名。列表为空时使用 `api.cloudflareclient.com`。

## 开启 WARP {#enable}

点击 `路由` → `启用 Warp`（Enable Warp）。出现勾选标记即表示 WARP 已开启。再次点击即可关闭 WARP。正在运行的配置档会以新设置重新启动。

你也可以在 `Warp` 标签页中勾选 `启用 Warp` 并点击 `确定`。之后需要重新启动配置档，更改才会生效。

如果已开启 WARP，但当前模式尚未生成配置，配置档将无法启动，Throne 会显示“Warp is enabled but its config has not been generated. Please generate the Warp config first in Routing Settings.”（已启用 Warp，但尚未生成其配置。请先在路由设置中生成 Warp 配置。）

要确认 WARP 是否生效，请打开一个显示 IP 地址的网站，它应当显示一个 Cloudflare 的地址。

## 让部分流量绕过 WARP {#warp-bypass}

`warp-bypass` 是一个出站，它使用你的配置档，但不经过 WARP 这一跳。可在路由配置档中这样使用它：

| 目标 | `默认出站`（Default outbound） | 规则 |
| --- | --- | --- |
| 大部分流量经过 WARP，部分网站不经过 | `proxy` | 把这些网站填入 `Warp-bypass` 输入框。 |
| 大部分流量不经过 WARP，部分网站经过 | `warp-bypass` | 把这些网站填入 `代理`（Proxy）输入框。 |

`默认出站` 列表和 `Warp-bypass` 输入框位于路由配置档编辑器中：`路由设置` → `路由`（Route）标签页 → 选择一个配置档 → `编辑`（Edit）。高级规则也可以把 `warp-bypass` 用作出站。规则格式请参见[路由](@/guides/routing.zh.md#simple-rules)。

WARP 关闭时，`warp-bypass` 与 `proxy` 的效果相同。

## 将 WARP 用作普通配置档 {#warp-profiles}

你也可以把 WARP 单独做成一个配置档，例如在没有其他代理的情况下使用它，或将其作为代理链中的一个跳点。

1. 打开 `程序`（Program）→ `新建配置档`（New profile）。
2. 将 `类型`（Type）设为 `WireGuard` 或 `MASQUE`。
3. 点击 `生成 Warp 配置`（WireGuard）或 `生成 WARP 身份标识`（Generate WARP identity，MASQUE）。Throne 会自动填入密钥、地址、MTU 和服务器地址。
4. 填写 `名称`（Name）并点击 `确定`。

这样的配置档单独使用时会直接连接 Cloudflare。使用它时请保持 `启用 Warp` 处于关闭状态，否则 Throne 会在它之后再添加一个 WARP 跳点。

## Android 版 {#android}

- 相关设置位于 `设置`（Settings）→ `Routing` → `WARP`：`Enable WARP`、`Mode`、各模式的字段、`生成配置`（Generate WARP config）以及 `Registration domains`。
- 首次生成时会要求你接受 Cloudflare WARP 服务条款。
- 如果注册被封锁，请先连接，然后开启 `设置` → `订阅`（Subscriptions）→ `Use proxy`。在 `仅代理`（Proxy only）模式下，该请求总是经过代理。
- 要快速切换 WARP，请打开 `配置`（Profiles）界面的菜单（⋮）→ `Routing profile`，然后点按 `Enable WARP` 或 `Disable WARP`。
- 如果开启了 WARP 却没有生成配置，Android 会显示“WARP is enabled but its config has not been generated. Generate it in Settings › Routing › WARP.”（已启用 WARP，但尚未生成其配置。请在“设置 › Routing › WARP”中生成。）
- WireGuard 和 MASQUE 配置档编辑器中都有 `Generate WARP identity` 按钮。
