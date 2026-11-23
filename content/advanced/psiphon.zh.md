+++
title = "Psiphon"
description = "无需自己的服务器即可经由 Psiphon 网络连接，或经由 Psiphon 发出代理流量。"
weight = 43
toc = true
+++

Psiphon 是由 Psiphon Inc. 运营的免费反审查网络。Throne 使用与其他开源客户端相同的公开设置连接它，因此你不需要服务器或账户。与任何 VPN 提供商一样，Psiphon 能看到你访问了哪些网站。

Throne 以两种方式使用 Psiphon：

- [Psiphon 配置档](#psiphon-profile)直接连接 Psiphon 网络。
- [Psiphon 出口](#psiphon-exit)在你的代理之后加上 Psiphon，作为最后一跳：你的设备 → 你启动的配置档 → Psiphon → 互联网。

Psiphon 承载 TCP 和 UDP。它可在 Windows、macOS 和 Linux 上使用，不支持 Android。

## Psiphon 配置档 {#psiphon-profile}

打开 `程序`（Program）→ `新建配置档`（New profile），将 `类型`（Type）设为 `Psiphon`。`地区`（Region）选择 Psiphon 服务器所在的国家；选择 `最佳性能`（Best performance）时由 Psiphon 自行选择。

首次连接时 Psiphon 会逐个尝试服务器，最多可能需要一分钟；之后的连接通常只需一两秒。Psiphon 配置档也可用于[代理链](@/advanced/chains.zh.md#chains)和分组：Psiphon 配置档在上、你的服务器在下的代理链会经由 Psiphon 连接到你的服务器。

Psiphon 自己的应用还可以通过 Conduit（由志愿者运营的代理）连接。Throne 不行：这需要只有 Psiphon 应用才有的密钥。

## Psiphon 出口 {#psiphon-exit}

选择 `路由`（Routing）→ `出口方式`（Exit through）→ `Psiphon`，或在 `路由设置`（Routing Settings）的 `出口`（Exit）标签页中做同样的选择，在那里 `地区` 用于选择服务器所在的国家。选择 `所选配置档`（Selected profile）会再次关闭 Psiphon。正在运行的配置档会以新设置重新启动。

- Psiphon、[WARP](@/advanced/warp.zh.md) 和 [Tor](@/advanced/tor.zh.md) 是同一个 `出口方式` 设置中的选项，因此只能开启其中一个。
- 如果你启动的配置档是 Psiphon 配置档，或是以 Psiphon 配置档结尾的代理链，Psiphon 出口会被拒绝。
- 把流量发往 `不经出口的代理`（Proxy without exit）的规则会跳过 Psiphon，参见[让部分流量绕过出口](@/advanced/warp.zh.md#warp-bypass)。

## 服务器列表 {#server-list}

Psiphon 通过一份签名的服务器列表找到它的服务器。Throne 自带一份副本，并从 Throne 在 GitHub 上的镜像或 Psiphon 自己的地址（哪个有响应就用哪个）更新它。Psiphon 会自行验证列表的签名，因此镜像无法篡改它。该列表和 Psiphon 的其他数据保存在[配置文件夹](@/reference/files.zh.md#data-folder)中的 `psiphon` 文件夹里。
