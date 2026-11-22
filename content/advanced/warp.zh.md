+++
title = "Cloudflare WARP"
description = "将 Cloudflare WARP 添加为代理之后的额外出口，并让指定流量绕过它。"
weight = 40
toc = true
+++

WARP 是 Cloudflare 的免费 VPN 服务。Throne 可以在你的代理之后加上 WARP，作为额外的一跳：你的设备 → 你启动的配置档 → WARP → 互联网。这样网站看到的是 Cloudflare 的地址，而不是你的代理服务器的地址，这对那些封锁 VPN 或数据中心地址的网站很有帮助。

- WARP 适用于你启动的每个配置档，包括代理链和自动选择器，并位于分组的落地代理之后。只有 `自定义 (sing-box 配置)`（Custom (sing-box config)）配置档不经过 WARP。
- WARP 的流量要经由你的代理传输，因此配置档必须能承载它：`WireGuard` 和 `AmneziaWG` 模式需要 UDP，基于 HTTP/3 的 `MASQUE` 也需要。基于 HTTP/2 的 `MASQUE` 只需要 TCP。
- WARP 是 `出口方式`（Exit through）的一个选项，另一个选项是 [Tor](@/advanced/tor.zh.md)。两者只能开启其一。

## 生成 WARP 配置 {#generate}

1. 打开 `路由`（Routing）→ `路由设置`（Routing Settings）→ `出口`（Exit）标签页。
2. 选择 `模式`（Mode）：`WireGuard`、`MASQUE` 或 `AmneziaWG`。
3. 点击 `生成 WARP 配置`（Generate WARP config），首次生成时接受 Cloudflare WARP 服务条款。
4. 按钮上显示“成功!”（Success!）后，点击 `确定`（OK）。

`WireGuard` 和 `MASQUE` 的配置相互独立，在两者之间切换后需要重新生成。`AmneziaWG` 使用 `WireGuard` 的配置。

对于 `MASQUE`，默认的 `HTTP 版本`（HTTP Version）使用基于 UDP 的 HTTP/3；`HTTP/2` 基于 TCP 运行，在 UDP 被封锁的网络中也能工作。

### AmneziaWG 模式 {#amneziawg}

当 `WireGuard` 模式因为连接 Cloudflare 的 WireGuard 被封锁而无法连接时，请使用 `AmneziaWG`。它在握手之前发送一些看起来像是连接 `www.cloudflare.com` 的 HTTP/3 (QUIC) 连接的数据包（即签名），以及几个 WARP 能接受的垃圾数据包。WARP 的数据包从你的代理服务器发出，因此起作用的是服务器所在的网络，而不是你的网络。

选择 `AmneziaWG` 时，Throne 会生成签名。之前生成的 WireGuard 配置仍然可用。

### 如果注册失败 {#registration-fails}

Cloudflare 的注册服务器 `api.cloudflareclient.com` 在一些国家被封锁（[#1874](https://github.com/throneproj/Throne/issues/1874)）。请通过你的代理进行注册：

1. 启动一个可用的配置档。
2. 勾选 `设置`（Settings）→ `基本设置`（Basic Settings）→ `通用`（General）→ `更新与下载`（Updates and Downloads）→ `通过代理发送 Throne 自身的请求`（Send Throne's own requests through the proxy）。如果已开启 `系统代理`（System proxy），Throne 已经会这样做。
3. 再次点击 `生成 WARP 配置`。

- “有用代理的请求，但未启动配置档。”（Request with proxy but no profile started.）：请先启动一个配置档。
- 如果开启了 `禁用混合入站`（Disable mixed inbound），该请求还需要 Tun 模式。
- 开启[断网保护（kill switch）](@/advanced/kill_switch.zh.md)后，请在配置档以 Tun 模式运行时生成配置，或者开启 `通过代理发送 Throne 自身的请求` 后再生成。

`注册域名` 中按顺序列出要尝试的 Cloudflare API 域名，每行一个。列表为空时使用 `api.cloudflareclient.com`。

## 开启 WARP {#enable}

选择 `路由` → `出口方式`（Exit through）→ `Cloudflare WARP`，或在 `路由设置` 的 `出口`（Exit）标签页中做同样的选择。选择 `所选配置档`（Selected profile）会再次关闭 WARP，选择 `Tor` 则会用 Tor 取代它。正在运行的配置档会以新设置重新启动。

如果当前模式没有配置，或者 `AmneziaWG` 缺少签名，就无法开启 WARP：请先生成配置。要确认 WARP 是否生效，请打开一个显示 IP 地址的网站，它应当显示一个 Cloudflare 的地址。

## 让部分流量绕过 WARP {#warp-bypass}

`不经 WARP 的代理`（Proxy without WARP）会让流量经过你的配置档，但不经过 WARP 这一跳。请在路由配置档编辑器中设置（`路由` → `编辑当前配置档`（Edit current profile））：

| 目标 | `其余流量`（Everything else goes to） | 网站填入 |
| --- | --- | --- |
| 大部分流量经过 WARP，部分网站不经过 | `代理`（Proxy） | `不经 WARP 的代理` 列表 |
| 大部分流量不经过 WARP，部分网站经过 | `不经 WARP 的代理` | `代理` 列表 |

规则也可以把流量发送到 `不经 WARP 的代理`（参见[路由](@/guides/routing.zh.md#advanced-rules)）。它以同样的方式跳过 [Tor](@/advanced/tor.zh.md)。WARP 和 Tor 都未开启时，它与 `代理` 的效果相同。

## 将 WARP 用作普通配置档 {#warp-profiles}

要在没有其他代理的情况下使用 WARP，或将其作为代理链中的一个跳点，请把它单独做成一个配置档：

1. 打开 `程序`（Program）→ `新建配置档`（New profile），将 `类型`（Type）设为 `WireGuard` 或 `MASQUE`。
2. 点击 `生成 WARP 配置`（Generate WARP config，WireGuard）或 `生成 WARP 身份标识`（Generate WARP identity，MASQUE）。
3. 填写 `名称`（Name）并点击 `确定`。

这样的配置档会直接连接 Cloudflare。使用它时请让 `出口方式`（Exit through）保持为 `所选配置档`（Selected profile），否则 Throne 会在它之后再添加一个 WARP 跳点。

`路由设置` 中的 `模式` 不会影响它。要让 WireGuard 配置档具备 `AmneziaWG` 模式的混淆效果，请勾选 `启用 Amnezia`（Enable Amnezia），点击 `Amnezia 选项`（Amnezia Options），将 `垃圾数据包数量 (Jc)`（Junk Packet Count (Jc)）设为 4、`垃圾数据包最小大小 (Jmin)`（Junk Packet Min Size (Jmin)）设为 40、`垃圾数据包最大大小 (Jmax)`（Junk Packet Max Size (Jmax)）设为 70，并将 H1 到 H4 分别设为 1、2、3 和 4。然后点击 `生成 QUIC 签名`（Generate QUIC signature），输入 `www.cloudflare.com` 并点击 `确定`。

## Android 版 {#android}

- 相关设置位于 `设置`（Settings）→ `路由`（Routing）→ `WARP`，其工作方式与桌面版相同，包括 `AmneziaWG`。
- 如果注册被封锁，请先连接，然后开启 `设置` → `订阅`（Subscriptions）→ `使用代理`（Use proxy）。
- 要快速切换 WARP，请打开 `设置` → `路由` → `当前路由配置`（Current routing profile），然后点按 `启用 WARP`（Enable WARP）或 `禁用 WARP`（Disable WARP）。
- WireGuard 和 MASQUE 配置档编辑器中都有 `生成 WARP 身份`（Generate WARP identity）按钮。
