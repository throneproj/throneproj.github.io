+++
title = "Windows DNS 泄漏防护"
description = "在 Windows 上，严格路由如何阻止 TUN 模式下的 DNS 泄漏，以及无法使用它时该怎么办。"
weight = 60
toc = true
aliases = ["/zh/advanced/windows-tun-mode/"]
+++

在 TUN 模式下，Windows 仍可能通过你平常的网卡（而不是隧道）发送 DNS 查询。这样你的运营商就能看到你查询了哪些网站，这就是 DNS 泄漏。本页介绍 Throne 如何防止 DNS 泄漏、如何确认防护已开启，以及无法使用该防护时该怎么办。

本页只涉及 [TUN 模式](@/guides/tun_mode.zh.md)。`严格路由`（Strict Route）在 `系统代理`（System Proxy）模式下不起作用；在该模式下，忽略代理的应用会自行连接并解析域名。

## 严格路由 {#strict-route}

Windows 可能会同时把同一个 DNS 查询发送给所有网卡的 DNS 服务器。即使 Windows 最终采用了来自隧道的应答，该查询也已经在隧道之外、通过你平常的网卡发送出去了。

`严格路由` 可以阻止这种情况。在 TUN 模式运行期间，Throne 会添加 Windows 防火墙过滤规则，用于：

- 在除隧道以外的所有网卡上阻止 DNS 查询（端口 53），使 Windows 从 Throne 获得应答；
- 在 `Tun 启用 IPv6`（Tun Enable IPv6）关闭时阻止其他应用的 IPv6 连接，以免经由 IPv6 泄漏。

ThroneCore 本身不会被阻止。TUN 模式停止或 Throne 退出时，这些过滤规则会随之消失。它们也可能阻止那些必须在隧道之外访问 DNS 服务器或使用 IPv6 的程序。

从 Throne 1.2.1 起，`严格路由` 在 Windows 10 和 11 上默认开启。开启后，你就不需要下文的注册表备用方案。

### 确认已开启 {#check}

1. 打开 `设置`（Settings）→ `Tun 设置`（Tun Settings）。
2. 确认已勾选 `严格路由`。
3. 点击 `确定`（OK）。
4. 如果 `Tun 模式`（Tun Mode）已开启，请将其关闭后再重新开启。Throne 会提示“重启 Tun 以生效。”（Restart Tun to take effect）

### 未开启的情况 {#when-off}

以下情况下，`严格路由` 可能处于关闭状态：

- **Windows 7、8 或 8.1。** `严格路由` 无法在 Windows 10 之前的 Windows 上工作，因此 Throne 不会开启它。
- **你在出错后关闭了它。** 如果 Windows 无法设置这些过滤规则，配置档将无法启动，Throne 会显示“严格的路由不可用”（Strict routing unavailable）。该消息建议关闭 `严格路由`，但这样也会失去防护。如果能排除故障原因，请重新开启它。
- **你是从 Throne 1.2.0 开始使用的。** 该版本中 `严格路由` 默认关闭，而更新会保留你已保存的设置。请现在勾选它。

如果无法使用 `严格路由`，请采用下文的注册表备用方案。

## 注册表备用方案 {#registry-fallback}

在不使用 `严格路由` 的情况下，你可以关闭 Windows 中同时向所有网卡发送 DNS 查询的功能。其组策略名称为 `关闭智能多宿主名称解析`（Turn off smart multi-homed name resolution）。这种方法的防护效果弱于 `严格路由`：它只改变 Windows 选择 DNS 服务器的方式，并不阻止任何流量。该策略存在于 Windows 8 及更高版本中，因此 Windows 7 上这两种防护都不可用。

### 使用组策略（专业版、企业版、教育版） {#group-policy}

1. 在开始菜单中搜索 `编辑组策略`（Edit group policy）并打开它。
2. 依次进入 `计算机配置`（Computer Configuration）→ `管理模板`（Administrative Templates）→ `网络`（Network）→ `DNS 客户端`（DNS Client）。
3. 双击 `关闭智能多宿主名称解析`。
4. 选择 `已启用`（Enabled），然后点击 `确定`（OK）。
5. 重启 Windows。

{% alert_warning() %}
请选择 `已启用`，而不是 `已禁用`（Disabled）。启用此策略才会关闭该功能。如果你之前按照旧的说明选择了 `已禁用`，请将其改为 `已启用`。
{% end %}

### 使用注册表（Windows 家庭版） {#windows-home}

Windows 家庭版没有组策略编辑器。以下命令会在注册表中设置相同的策略：

```text
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v DisableSmartNameResolution /t REG_DWORD /d 1 /f
```

1. 复制上面的命令。
2. 在开始菜单中搜索 `cmd`。
3. 右键点击 `命令提示符`（Command Prompt），选择 `以管理员身份运行`（Run as administrator）。
4. 粘贴命令并按 `Enter`。
5. 重启 Windows。

要撤销此设置，请以同样的方式运行以下命令，然后重启 Windows：

```text
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v DisableSmartNameResolution /f
```

如果你使用的是组策略，请改为将该策略设回 `未配置`（Not Configured）。

## 浏览器 {#browsers}

### 加密 DNS {#encrypted-dns}

浏览器可以使用自带的加密 DNS（DNS over HTTPS），Windows 11 也可以为网卡启用它。这些查询不使用端口 53，因此不会被 `严格路由` 阻止，也不会使用 Throne 的 DNS 设置。此时泄漏测试会显示该 DNS 服务商的服务器。

如果你希望所有查询都经过 Throne 的 DNS，请在浏览器的隐私或安全设置中关闭安全 DNS 选项，并在 Windows 设置中为网卡关闭 DNS over HTTPS。

### QUIC {#quic}

关闭 QUIC 并不能解决 DNS 泄漏，它针对的是另一个问题。许多网站（例如 Google 和 YouTube）使用 QUIC（基于 UDP 的 HTTP/3），而有些代理服务器对 UDP 的支持很差，甚至完全不支持。如果这些网站通过隧道访问时加载缓慢或无法打开，而其他网站正常，请在浏览器中关闭 QUIC，让它改用 TCP。

在 Chrome 中：

1. 打开 `chrome://flags/`。
2. 搜索 `QUIC`。
3. 将 `Experimental QUIC protocol` 设为 `Disabled`。
4. 点击 `Relaunch`。

## 仍有泄漏？ {#still-leaking}

- **检查路由设置。** 有些结果是正常的。例如，被规则设为直连的域名会有意使用 `直连 DNS`（Direct DNS）进行解析，而这通常就是你的运营商的 DNS 服务器。[DNS 泄漏测试](@/guides/dns.zh.md#leak-tests)中列出了预期的结果。
- **检查安全软件。** 有些杀毒软件和防火墙产品会自行过滤或重定向 DNS。请在暂停它们后再测试，或者为 Throne 添加例外。
- **检查其他 VPN 应用。** 使用 TUN 模式时，请断开其他 VPN 客户端，它们也可能修改 DNS 设置和防火墙规则。
