+++
title = "Kill Switch（断网保护）"
description = "拦截所有不经过 Throne 的流量（即使没有配置档运行时也是如此），并在断网保护把你锁在网络之外时恢复连接。"
weight = 65
toc = true
+++

自 1.4.0 起，Throne 提供断网保护（kill switch）。开启后，你的电脑只能通过 Throne 发送流量：通过 TUN 模式、通过本地代理端口，或者作为 Throne 自身的连接。其他所有流量都会被拦截，即使没有配置档运行时也是如此。如果代理停止或连接中断，应用也无法退回到你的普通连接。

{% alert_warning() %}
断网保护在 1.4.0 中属于实验性功能。开启之前，请先阅读[被锁在网络之外时](#recovery)。
{% end %}

## 它的作用 {#what-it-does}

只要 Throne 在运行，无论是否有配置档运行，断网保护都会生效：

| 情况 | 哪些流量能通过 |
| --- | --- |
| 配置档以 TUN 模式运行 | 全部流量，因为所有流量都经过 TUN 网卡。 |
| 配置档仅以系统代理运行 | 使用代理的应用。忽略代理的应用会被拦截。 |
| 没有配置档运行 | 几乎没有：只有本地网络和下文列出的例外。 |

Throne 自身不受影响：它的核心始终可以连接你的服务器，并发送被你的规则设为 `direct` 的流量。完整列表请参见[始终允许的流量](#allowed)。

Throne 退出时，断网保护随之结束。Throne 崩溃时它也会结束，因此崩溃不会让你断网，但此后它也不再保护你。请将 TUN 模式与断网保护配合使用：这样在配置档运行期间，所有应用都能正常工作。

## 开启断网保护 {#enable}

1. 打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `安全`（Security）。
2. 勾选 `Kill Switch`。
3. 点击 `确定`（OK）。

断网保护需要与 TUN 模式相同的权限；参见[要求](#requirements)。在 Linux 和 macOS 上，开启它会重启 Throne 的核心，正在运行的配置档也会随之重启。断网保护启动期间，Throne 会等它启动完成后再启动配置档。

检查它是否生效：

- 日志显示“[Kill switch] On: only traffic through Throne can leave this device.”（[Kill switch] 已开启：只有经过 Throne 的流量才能离开此设备。）
- 窗口标题和托盘提示显示 `[Kill switch]`。
- 启动按钮上有一个小锁。它的提示文字会说明断网保护当前的状态：

| 锁 | 提示文字 | 含义 |
| --- | --- | --- |
| 灰色 | “Kill switch: starting…” | 断网保护正在启动。 |
| 绿色 | “Kill switch: on — traffic only flows through Throne's Tun” | 配置档正以 TUN 模式运行。 |
| 琥珀色 | “Kill switch: Tun is not running, so most traffic is blocked” | 没有配置档运行，或者 TUN 模式已关闭。 |
| 红色 | “Kill switch is not active”或“Kill switch is blocking traffic” | 断网保护出现了问题；参见[无法工作时](#failures)。 |

该设置会被保存。每次 Throne 启动时，断网保护都会再次启动。

## 始终允许的流量 {#allowed}

- **Throne 的核心**（`ThroneCore`）：到你服务器的连接、被你的规则设为 `direct` 的流量、URL 测试，以及 Throne 自身 DNS 服务器的 DNS 查询。[额外核心](@/advanced/chains.zh.md#extra-core)（Extra Core）配置档的程序也会被放行。
- **TUN 网卡。** 所有进入 Throne TUN 网卡的流量。
- **环回地址**（`127.0.0.1`、`::1`）。应用通过它访问本地代理端口。
- **本地网络**，除非在 `设置`（Settings）→ `Tun 设置`（Tun Settings）中关闭了 `私有地址范围绕过`（Private Range Bypass）。以下范围算作本地：`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`、`169.254.0.0/16`、`224.0.0.0/4`、`255.255.255.255`、`fc00::/7`、`fe80::/10` 和 `ff00::/8`。你对 `私有地址范围绕过` 列表所做的修改不会改变这份列表。
- **网络基础协议：** DHCP 和 DHCPv6、IPv6 邻居发现和路由器发现，以及组播组消息（IGMP 和 MLD）。你的电脑会保留它的网络地址。
- **Throne API。** 当 [Throne API](@/advanced/api.zh.md) 在某个网络地址上监听时，它对客户端的回复可以通过。

即使允许了本地网络，其他程序发往本地地址的 DNS 查询（端口 53 和 853）仍会被拦截。路由器中的 DNS 服务器会把这些查询转发到隧道之外。在 Linux 上，如果 `/etc/resolv.conf` 中指定了这样的服务器，Throne 会发出警告：“the system DNS server … is on the local network and the kill switch blocks DNS to it”（系统 DNS 服务器 … 位于本地网络中，断网保护会拦截发往它的 DNS）。在 TUN 模式下，请使用 systemd-resolved（Throne 会把它指向隧道），或者使用本地网络之外的 DNS 服务器。

其他所有流量都会被拦截，例如：

- Throne 自身的请求，例如订阅更新、更新检查和 WARP 注册。它们只有在 TUN 模式下，或者在配置档运行且开启了 `设置`（Settings）→ `基本设置`（Basic Settings）→ `杂项`（Miscellaneous）→ `使用代理`（Use proxy）或 `系统代理`（System Proxy）时才能工作。
- 这台电脑为其他设备、容器或虚拟机转发的流量，除非它经过 TUN 网卡或留在本地网络内。
- 其他 VPN 应用的流量。

在 macOS 上，断网保护启动时已打开的连接会被断开一次。应用会重新连接。

## 工作原理 {#how-it-works}

Throne 会启动一个单独的守卫进程 `ThroneCore --guard`。它会添加防火墙规则，每 5 秒检查一次这些规则是否仍然存在，并在 Throne 停止它、Throne 退出或 Throne 崩溃时移除这些规则。

- **Linux：** 一个名为 `throne-guard-…` 的 nftables 表。守卫进程结束时，内核会删除它。Throne 的核心通过其所属的组来识别：核心会切换到组 ID 1950896719，额外核心程序也以这个组运行。
- **macOS：** 一个名为 `com.apple/000.throne-guard.…` 的 pf 锚点（anchor）。守卫进程会在需要期间开启 pf。核心通过与 Linux 上相同的组 ID 来识别。如果某个守卫进程结束时没有移除它的规则，Throne 会在下次核心启动时移除它们。
- **Windows：** 名为“Throne kill switch”的 Windows 筛选平台（WFP）筛选器。守卫进程结束时，Windows 会删除它们。`ThroneCore.exe` 和额外核心配置档的程序通过路径来识别。当你启动额外核心配置档时，Throne 会先把它的程序添加到断网保护中（“[Kill switch] Allowing the extra core …”）。

如果其他程序移除了这些规则或关闭了防火墙，Throne 会重新启动断网保护，最多每 30 秒一次。

## 要求 {#requirements}

| 系统 | 断网保护需要什么 |
| --- | --- |
| Windows | Throne 以管理员身份运行，并且 Windows 服务 `Base Filtering Engine` 正在运行。 |
| Linux | 核心通过 SUID 位以 root 身份运行。这正是 Throne 为 TUN 模式所做的设置。只具有能力（`setcap`）的核心是不够的。需要 Linux 5.12 或更高版本，并支持 nftables 和 conntrack 标签（`CONFIG_NFT_CT` 和 `CONFIG_NF_CONNTRACK_LABELS`）。 |
| macOS | 核心通过 SUID 位以 root 身份运行，与 TUN 模式相同。`/etc/pf.conf` 必须加载 `com.apple` 锚点，默认情况下就是如此。 |

Throne 如何设置这些权限，请参见 [TUN 模式的权限](@/guides/tun_mode.zh.md#privileges)。

## 无法工作时 {#failures}

当断网保护已开启但无法启动，或者停止工作时，Throne 会显示“Kill switch is not active”（断网保护未生效）及其原因。窗口标题显示 `[Kill switch: not active]`。可用的按钮：

- **`Restart as Administrator`**（Windows）或 **`Grant Privileges`**（Linux 和 macOS），在缺少权限时显示。它们的作用与 TUN 模式中的相同。
- **`Retry`**，用于其他问题。
- **`Disable Kill Switch`**，关闭该设置。

断网保护已开启但未生效时，不会拦截任何流量，Throne 也不会启动配置档。日志显示“[Kill switch] Not starting …: the kill switch is not active.”（[Kill switch] 未启动 …：断网保护未生效。）这样可以避免你在实际未受保护时，误以为自己受到保护而使用配置档。请解决问题，或者关闭断网保护。

原因带有一个代码。它会出现在日志中（“[Kill switch] Not active: …”），也会作为 [Throne API](@/advanced/api.zh.md) 中的 `kill_switch_error` 出现：

| 代码 | 含义 |
| --- | --- |
| `privilege` | 缺少权限：Throne 没有以管理员身份运行（Windows），或者核心没有 root 权限（Linux、macOS）。 |
| `unsupported` | 这个系统无法运行断网保护：例如没有 nftables、版本低于 5.12 或不支持 conntrack 标签的 Linux，使用能力而不是 root 的 Linux 核心，没有 `com.apple` 锚点的 pf 配置，或者已停止的 `Base Filtering Engine` 服务。 |
| `config` | 断网保护拒绝了它的设置，例如无效的 TUN 地址。 |
| `tampered` | 其他程序移除了规则或关闭了防火墙，并且重新启动也无济于事。 |
| `crash`、`timeout`、`internal` | 守卫进程已停止，或者未能在 15 秒内就绪。`Retry` 通常有效。 |
| `overridden` | 仅限无界面 Throne：它是以 `--no-kill-switch` 启动的。 |

### Kill Switch 正在阻断流量 {#blocking}

在 Linux 上，核心必须切换到断网保护的组。如果无法切换，例如在没有 `CAP_SETGID` 的容器或用户命名空间中，断网保护会继续拦截流量，但 Throne 会拒绝启动配置档。窗口标题和托盘提示显示 `[Kill Switch 正在阻断流量]`，警告中只提供 `Disable Kill Switch`。此时你的电脑无法访问互联网，直到你关闭断网保护为止。

## 关闭断网保护 {#disable}

使用以下任一方式：

- 取消勾选 `设置`（Settings）→ `基本设置`（Basic Settings）→ `安全`（Security）→ `Kill Switch`，然后点击 `确定`（OK）。
- 右键点击启动按钮 → `Disable Kill Switch`。Throne 会询问“Turn off the kill switch? Traffic that does not go through Throne will no longer be blocked.”（要关闭断网保护吗？不经过 Throne 的流量将不再被拦截。）点击 `Disable Kill Switch`。
- 在断网保护的警告中点击 `Disable Kill Switch`。

日志显示“[Kill switch] Off.”（[Kill switch] 已关闭。）你的应用可以再次使用普通连接。

## 被锁在网络之外时 {#recovery}

Throne 的设置无需互联网连接即可使用。打开设置，按上述方法关闭断网保护。

如果 Throne 没有响应：

1. 退出 Throne，或者在任务管理器中结束它。守卫进程会察觉到这一点，并在几秒内移除它的规则。
2. 如果流量仍被拦截，请自行结束守卫进程：
   - **Windows：** 在任务管理器 → `详细信息`（Details）中，结束所有 `ThroneCore.exe`。Windows 会随进程一起移除筛选器。重启 Windows 也会移除它们。
   - **Linux：** 运行 `sudo pkill -f 'ThroneCore --guard'`。内核会随进程一起移除该表。
   - **macOS：** 运行 `sudo pkill -f 'ThroneCore --guard'`。如果规则仍然存在，请再次启动 Throne：它的核心会移除这些规则。或者用 `sudo pfctl -a com.apple -s Anchors` 列出锚点，再用 `sudo pfctl -a 'com.apple/000.throne-guard.…' -F all` 清除以 `000.throne-guard.` 开头的那个锚点。重启 macOS 也会移除它们。
3. 启动 Throne，并在做其他任何事情之前先关闭断网保护。在你关闭它之前，它每次都会随 Throne 一起启动。

## Android 版 {#android}

Throne for Android 没有断网保护。Android 自带这项功能：将 Throne 设为始终开启的 VPN，并开启“屏蔽未使用 VPN 的所有连接”（Block connections without VPN）。参见[始终开启的 VPN](@/android/permissions.zh.md#always-on)。

## 无界面 Throne {#headless}

[无界面 Throne](@/headless/_index.zh.md) 具有相同的断网保护。用 `thronectl settings set kill_switch=true` 开启它。不同之处如下：

- 所需的权限取决于你的安装方式。在 Linux 上，断网保护需要一个以 root 身份运行的单元（unit），或者一个带有 SUID 位的核心；只有能力会得到 `unsupported`。参见 [Linux 上的权限](@/headless/installation.zh.md#linux-privileges)。
- 当断网保护无法工作时，无界面 Throne 会在日志中记录原因，拒绝配置档（`kill_switch_inactive`），并报告 `kill_switch_failed`。
- 如果断网保护让你无法访问这台电脑，请用 `--no-kill-switch` 启动 Throne 一次。参见[恢复访问](@/headless/recovery.zh.md#recovery)。
