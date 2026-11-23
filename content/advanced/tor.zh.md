+++
title = "Tor"
description = "在 Tor 被封锁的地方借助网桥经由 Tor 连接，经由 Tor 发出代理流量，并打开 .onion 网站。"
weight = 42
toc = true
+++

Throne 以两种方式使用 Tor：

- [Tor 配置档](#tor-profile)自己连接 Tor 网络，在 Tor 被封锁的地方则经由网桥连接。它不需要你自己的服务器。
- [Tor 出口](#tor-exit)在你的代理之后加上 Tor，作为最后一跳：你的设备 → 你启动的配置档 → Tor → 互联网。

无论哪种方式，网站看到的都是 Tor 出口节点的地址，并且可以打开 `.onion` 网站。

- Tor 只承载 TCP。UDP（例如 QUIC 或语音通话）无法通过；浏览器会回退到 TCP。
- Tor 可在 Windows、macOS 和 64 位 Linux（x86-64 和 ARM）上使用，不支持 Android。

## 下载 Tor {#download}

Throne 会在第一次需要 Tor 时下载它。启动使用 Tor 的配置档时会先询问：点击 `下载`（Download），Tor 安装完成后配置档就会启动。选择 Tor 出口会开始下载，并在下载完成后开启该出口。`Tor` 配置档编辑器和 `路由设置`（Routing Settings）的 `出口`（Exit）标签页会显示 Tor 是否已安装，`日志`（Logs）标签页会显示下载进度。

- Throne 从 Tor Project 下载 Tor Expert Bundle，并用该项目公布的校验和进行核对。无法访问 torproject.org 时，它会使用 Throne 在 GitHub 上的副本，该副本在发布前已用 Tor Project 的签名验证。
- 下载会经由正在运行的配置档进行；没有配置档运行时则直接连接。
- Tor 保存在[配置文件夹](@/reference/files.zh.md#data-folder)中的 `tor` 文件夹里。

## Tor 配置档 {#tor-profile}

打开 `程序`（Program）→ `新建配置档`（New profile），将 `类型`（Type）设为 `Tor`。`网桥`（Bridges）决定 Throne 如何连接到 Tor 网络：

| 选项 | 适用场景 |
| --- | --- |
| `无`（None） | 你的网络没有封锁 Tor。 |
| `内置`（Built-in） | Throne 内置的网桥：`Snowflake`（在大多数受审查的网络中可用）、`obfs4` 或 `meek`。 |
| `自定义`（Custom） | 来自 Tor Project 或你信任的人的网桥行，每行一个，可带或不带 `Bridge` 关键字。Throne 支持 `obfs4`、`webtunnel`、`snowflake`、`meek_lite` 和普通网桥。 |

`出口国家`（Exit country）选择最后一个 Tor 中继所在的国家；选择 `任意`（Any）时由 Tor 自行选择。

首次连接时 Tor 需要下载网络信息，最多可能需要一两分钟。Throne 会为每种网桥设置保存这些数据，因此之后的启动会更快。Tor 配置档也可用于[代理链](@/advanced/chains.zh.md#chains)和分组：Tor 配置档在上、你的服务器在下的代理链会经由 Tor 连接到你的服务器。

网桥传输（obfs4、WebTunnel、Snowflake、meek）在 Throne 内部运行，连接方式与你的其他配置档相同，因此在 Tun 模式下也能使用。

### 获取网桥 {#get-bridges}

`获取网桥`（Get bridges）会向 Tor Project 的网桥服务查询某个国家可用的网桥：

1. 选择 `国家`（Country）。选择 `自动`（Automatic）时，由服务根据你的连接判断。
2. 点击 `请求`（Request）。与 Tor Browser 一样，请求会经由伪装的（域前置）连接发出，可能需要一分钟。
3. 选择一个建议，然后点击 `确定`（OK）。内置的建议会把配置档切换为 `内置`；其他建议会填入 `自定义`。

当有配置档正在运行时，请求可能会经由它发出，此时 `自动` 给出的是代理所在位置的结果：请改为选择你所在的国家。无法访问该服务时，Throne 会显示它为该国家内置的列表。

获取网桥的其他途径：[bridges.torproject.org](https://bridges.torproject.org)、Tor Project 的 Telegram 机器人 `@GetBridgesBot`，或发送邮件到 `bridges@torproject.org`。

### 导入网桥行 {#import}

复制网桥行，然后在主窗口中按 `Ctrl+V`。连续的网桥行会成为一个使用 `自定义` 网桥的 `Tor` 配置档。网桥网站上二维码所用的格式 `['obfs4 …', 'obfs4 …']` 也可以。Throne 不支持的传输（obfs2、obfs3、ScrambleSuit、Conjure）对应的行会被跳过，并给出警告。

## Tor 出口 {#tor-exit}

选择 `路由`（Routing）→ `出口方式`（Exit through）→ `Tor`，或在 `路由设置` 的 `出口` 标签页中做同样的选择，在那里 `出口国家` 用于选择最后一个 Tor 中继所在的国家。选择 `所选配置档`（Selected profile）会再次关闭 Tor。正在运行的配置档会以新设置重新启动。

- Tor、[WARP](@/advanced/warp.zh.md) 和 [Psiphon](@/advanced/psiphon.zh.md) 是同一个 `出口方式` 设置中的选项，因此只能开启其中一个。
- 该出口不需要网桥：它经由你的代理连接到 Tor。
- 如果你启动的配置档是 Tor 配置档，或是以 Tor 配置档结尾的代理链，Tor 出口会被拒绝。

## 新的 Tor 线路 {#new-circuit}

`工具`（Tools）→ `新的 Tor 线路`（New Tor circuit）会让新连接经由 Tor 中的另一条路径，通常会使用不同的出口地址。已打开的连接保持原来的路径。只有当正在运行的配置使用 Tor 时，此项才可用。

## 不经过 Tor 的流量 {#skip-tor}

把流量发往 `不经出口的代理`（Proxy without exit）的规则会跳过 Tor 出口，流量经由所选配置档发出，参见[让部分流量绕过出口](@/advanced/warp.zh.md#warp-bypass)。`直连`（Direct）和 `阻止`（Block）照常工作。`.onion` 地址总是发往 Tor，并且优先于你自己的规则。
