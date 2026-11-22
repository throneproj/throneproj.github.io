+++
title = "Tor"
description = "在你的代理之后经由 Tor 发出代理流量，并打开 .onion 网站。"
weight = 42
toc = true
+++

Throne 可以在你的代理之后加上 Tor，作为最后一跳：你的设备 → 你启动的配置档 → Tor → 互联网。这样网站看到的是 Tor 出口节点的地址，而不是你的代理服务器的地址，并且可以打开 `.onion` 网站。

- Tor 只承载 TCP。发往代理的 UDP 流量（例如 QUIC 或语音通话）无法通过；浏览器会回退到 TCP。
- Tor 和 [WARP](@/advanced/warp.zh.md) 是同一个 `出口方式`（Exit through）设置中的选项，因此两者只能开启其一。
- Tor 可在 Windows、macOS 和 64 位 Linux（x86-64 和 ARM）上使用。

## 开启 Tor {#enable}

选择 `路由`（Routing）→ `出口方式` → `Tor`，或在 `路由设置`（Routing Settings）的 `出口`（Exit）标签页中做同样的选择。选择 `所选配置档`（Selected profile）会再次关闭 Tor。正在运行的配置档会以新设置重新启动。

第一次开启时，Throne 会下载 Tor。从菜单开启时，Tor 会在下载完成后开启；在 `路由设置` 中，`Tor` 下方的一行文字会说明 Tor 是否已安装，点击 `确定`（OK）后开始下载。`日志`（Logs）标签页会显示下载进度。

- Throne 从 Tor Project 下载 Tor Expert Bundle，用该项目公布的校验和进行核对，并将其保存在[配置文件夹](@/reference/files.zh.md#data-folder)中的 `tor` 文件夹里。
- 下载会经由正在运行的配置档进行；没有配置档运行时则直接连接。

## 不经过 Tor 的流量 {#skip-tor}

把流量发往 `不经 WARP 的代理`（Proxy without WARP）的规则同样会跳过 Tor，流量经由所选配置档发出，参见[让部分流量绕过 WARP](@/advanced/warp.zh.md#warp-bypass)。`直连`（Direct）和 `阻止`（Block）照常工作。`.onion` 地址总是发往 Tor，并且优先于你自己的规则。
