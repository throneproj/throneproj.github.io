+++
title = "DNS"
description = "Throne 如何解析域名、各项 DNS 设置的作用、FakeIP 何时有用，以及如何解读 DNS 泄漏测试。"
weight = 50
toc = true
+++

应用在打开网站之前，需要先通过 DNS 查询把网站的名称转换为 IP 地址。本页说明 Throne 在哪种查询中使用哪个 DNS 服务器、`DNS` 标签页上各项设置的作用，以及如何解读 DNS 泄漏测试。默认设置适用于大多数人。

## Throne 中的 DNS 工作方式 {#how-dns-works}

Throne 在核心中内置了自己的 DNS 解析器。它使用三个 DNS 服务器：

| 服务器 | 查询的传输方式 | 用途 |
| --- | --- | --- |
| `远程 DNS`（Remote DNS） | 经过代理 | 应答应用的 DNS 查询，除非下文的某条规则将查询发往别处。 |
| `直连 DNS`（Direct DNS） | 直接发送，不经过代理 | 当路由配置档将某个域名发往 `direct` 时，由它应答对该域名的查询。Throne 还用它查询代理服务器的地址，以及在按名称直接连接某个网站时查询该网站的地址。 |
| `本地覆盖`（Local Override） | 直接发送 | 查询上面两个服务器的名称，例如 `dns.google`。留空表示使用系统的解析器。 |

当应用的查询到达 Throne 时，Throne 按以下顺序应答：

1. `预定义回答`（Predefined Answers）和 `尊重 Hosts 文件`（Respect Hosts File）最先应答。
2. 开启 `启用 FakeIP`（Enable FakeIP）后，地址查询会得到一个虚假地址（参见 [FakeIP](#fakeip)）。
3. 开启 `启用 DNS 路由`（Enable DNS Routing，默认开启）后，路由配置档设为 `direct` 的域名会交给直连 DNS。这适用于 `domain:`、`suffix:`、`keyword:` 和 `regex:` 规则以及内置的 `geosite-*` 规则集。它不适用于 `geoip-*` 规则集、IP 规则或你自己的 `.srs` 文件。
4. 其余查询都交给 `默认 DNS 服务器`（Default DNS server），其默认值为 `remote`。如果你将其设为 `direct`，路由配置档发往 `proxy` 的域名仍会使用远程 DNS，条件与第 3 步相同。

查询的来源取决于所用的模式：

- **TUN 模式。** 应用的 DNS 查询会进入隧道并到达 Throne。Throne 会为每个结构化路由配置档添加一个 DNS 步骤（列表中的 `Route DNS` 或 `dns-hijack` 规则起同样的作用），因此它会按上述方式应答这些查询。原始路由配置档只有在你自行编写这一步骤时才会包含它；参见[原始配置档](@/guides/routing.zh.md#raw-profiles)。
- **系统代理模式。** 使用代理的应用会把网站名称发送给 Throne。对于经过代理的连接，由代理服务器查询该名称。对于直连的连接，由 Throne 使用直连 DNS 查询。应用也可以自行通过系统的解析器查询名称，这些查询不会经过 Throne。

## 设置 {#settings}

打开 `设置`（Settings）→ `路由设置`（Routing Settings）→ `DNS`。点击 `确定`（OK）并重启连接后，更改才会生效。

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `远程 DNS`（Remote DNS） | `https://8.8.8.8/dns-query` | 经过代理使用的服务器。列表中还提供 `tls://8.8.8.8`、`tls://1.1.1.1`、`8.8.8.8` 和 `1.1.1.1`。 |
| `直连 DNS`（Direct DNS） | `localhost` | 不经过代理使用的服务器。`localhost` 表示系统的解析器。除非它无法正常工作，否则请保留此设置；如果无法工作，请选择一个在你的网络中无需代理即可使用的服务器。列表中提供了中国（`223.5.5.5`、`119.29.29.29`）、伊朗（`178.22.122.100`）和俄罗斯（`77.88.8.8`）的公共解析器。 |
| `禁用 IPv6`（Disable IPv6，位于每个服务器旁边） | 关闭 | 对发往该服务器的 IPv6（AAAA）查询返回空结果。 |
| `本地覆盖`（Local Override） | 空 | 用于查询 DNS 服务器名称的 DNS 服务器。当系统的解析器无法使用时，请在此处填写一个 IP 地址。 |
| `默认 DNS 服务器`（Default DNS server） | `remote` | 用于其他规则都不处理的查询的服务器：`remote` 或 `direct`。 |
| `启用 DNS 路由`（Enable DNS Routing） | 开启 | 将对设为 `direct` 的域名的查询发送到直连 DNS。 |
| `尊重 Hosts 文件`（Respect Hosts File） | 关闭 | 优先使用系统 hosts 文件应答 A 和 AAAA 查询。只影响文件中列出的域名。 |
| `预定义回答`（Predefined Answers） | 开启 | 采用 hosts 文件语法的固定应答。默认条目为 `127.0.0.1 localhost`。 |
| `启用 FakeIP`（Enable FakeIP） | 关闭 | 参见 [FakeIP](#fakeip)。 |
| `FakeIP 禁用 IPv6`（FakeIP Disable IPv6） | 关闭 | 不分配虚假的 IPv6 地址；AAAA 查询会得到空应答。 |

`远程 DNS`、`直连 DNS` 和 `本地覆盖` 接受以下格式：

| 格式 | 示例 |
| --- | --- |
| 普通 DNS | `8.8.8.8` 或 `8.8.8.8:53` |
| DNS over TCP | `tcp://8.8.8.8:53` |
| DNS over TLS | `tls://1.1.1.1` |
| DNS over HTTPS | `https://1.1.1.1/dns-query` |
| DNS over HTTP/3 | `h3://dns.example.com/dns-query` |
| DNS over QUIC | `quic://dns.example.com` |
| 你的网络分配的服务器 | `dhcp://auto` |
| 系统的解析器（用于 `直连 DNS`） | `localhost` |

当正在运行的配置档使用 Xray，且 `远程 DNS`（Remote DNS）为普通 DNS 或 DNS over QUIC 时，Throne 会改用 DNS over HTTPS。例如，`1.1.1.1` 会变为 `https://1.1.1.1/dns-query`；Throne 不认识的服务器会变为 `https://8.8.8.8/dns-query`。

`预定义回答`（Predefined Answers）会打开一个编辑器，每行一个条目：

```text
127.0.0.1 localhost
10.0.0.5 nas.lan files.lan
```

如果某个域名在此列表中只有 IPv4 地址，那么它的 IPv6 查询会得到“域名不存在”的应答，反之亦然。这样，应用就无法绕过你设置的条目。

## FakeIP {#fakeip}

开启 `启用 FakeIP`（Enable FakeIP）后，Throne 会立即用 `198.18.0.0/15`（IPv6：`fc00::/18`）中的虚假地址应答地址查询，而不询问真实的 DNS 服务器。当应用连接到该地址时，Throne 知道它代表哪个域名，并按名称对连接进行路由。真正的查询稍后才会进行：经过代理的连接在代理服务器上查询，直连的连接则使用直连 DNS 查询。

这样做有两个好处：

- 连接建立得更快，因为应用无需等待真实的 DNS 应答。
- 在连接完成路由之前，不会有任何 DNS 查询离开你的设备。

FakeIP 只影响到达 Throne 的查询，因此它在 TUN 模式下才有用。在系统代理模式下，它对应用没有任何影响。

注意事项：

- 来自 `预定义回答` 和 hosts 文件的应答仍是真实的。
- 应用会在自己的缓存中保留虚假地址。停止 Throne 后，仍持有虚假地址的应用在重新查询该名称之前将无法连接。如果应用一直处于离线状态，请重启该应用。
- `高级设置`（Advanced Settings）→ `保存缓存到文件`（Save Cache To File）可在 Throne 重启后保留这些虚假地址。

## 高级设置 {#advanced}

`DNS` 标签页上的 `高级设置`（Advanced Settings）用于控制 DNS 缓存：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `缓存容量`（Cache Capacity） | `65536` | 缓存最多保留多少条应答。 |
| `查询超时`（Query Timeout） | `10s` | 等待 DNS 服务器的时长。 |
| `乐观缓存`（Optimistic Cache） | 关闭 | 在后台刷新已过期应答的同时，继续提供该应答。不能与 `禁用缓存`（Disable Cache）或 `禁用有效期`（Disable Expire）同时使用。 |
| `乐观超时`（Optimistic Timeout） | `3d` | 已过期的应答最多还能提供多长时间。 |
| `禁用缓存`（Disable Cache） | 关闭 | 关闭 DNS 缓存。 |
| `禁用有效期`（Disable Expire） | 关闭 | 缓存的应答过期后仍然保留。 |
| `保存缓存到文件`（Save Cache To File） | 关闭 | 将缓存的应答和 FakeIP 地址写入核心的缓存文件，使其在重启后仍然保留。每个条目都会产生一次磁盘写入。 |
| `反向映射`（Reverse Mapping） | 关闭 | 记住已应答的 IP 地址属于哪个域名，使域名规则能够匹配到该地址的连接。 |

时长由一个数字加上 `ns`、`us`、`ms`、`s`、`m`、`h` 或 `d` 组成，例如 `5s` 或 `3d`。

`使用自定义 DNS 对象`（Use Custom DNS Object）会用一个完整的 sing-box `dns` 对象替换此标签页上的所有设置，该对象由你通过 `编辑 DNS 对象`（Edit DNS Object）编写。开启后，简单设置和 `高级设置`（Advanced Settings）会变为灰色，DNS 路由、FakeIP 和预定义回答等功能只有在你的对象中配置了才会生效。在编辑器中，`格式化`（Format）用于整理 JSON，`文档`（Document）会显示 [sing-box DNS 文档](https://sing-box.sagernet.org/configuration/dns/)的地址。

{% alert_warning() %}
请在自定义 DNS 对象中保留一个标签（tag）为 `dns-direct` 的服务器。Throne 的路由会用它来查询服务器地址。
{% end %}

## DNS 泄漏测试 {#leak-tests}

DNS 泄漏测试是一类网站，它会显示是哪些 DNS 服务器查询了它的测试域名。测试结果取决于你使用的模式和路由配置档。

以下结果属于正常情况：

- **你的远程 DNS 服务商**（默认设置下为 Google）。你的查询经过了远程 DNS 和代理。对于你走代理的网站，这是正常结果。
- **你的运营商（针对直连的网站）。** Throne 使用直连 DNS 查询直连的域名，而直连 DNS 默认是系统的解析器，通常属于你的运营商。在系统代理模式下或开启 FakeIP 时，对于仅因路由配置档的默认出站为 `direct` 才直连的网站（例如“Proxy … Blocked”配置档中的情况），也会出现这种结果。直连流量本来就不经过代理直接到达网站，所以你的运营商无论如何都能看到它。
- **你的运营商（系统代理模式下）。** 浏览器和应用可以绕过 Throne 自行查询名称。如果你在意这一点，请使用 TUN 模式。
- **浏览器自己的 DNS 服务商**，当浏览器使用安全 DNS（DNS over HTTPS）时。这些查询是普通的 HTTPS 连接，会遵循你的路由规则。
- **大多数名称显示为你的运营商**，当 `默认 DNS 服务器`（Default DNS server）设为 `direct` 时。

真正有问题的情况是这样的：你使用 TUN 模式和一个让测试网站走代理的路由配置档（例如 `Default`），但测试结果仍然显示你的运营商。这说明有部分查询绕过了隧道。在 Windows 上，请检查 `设置`（Settings）→ `Tun 设置`（Tun Settings）→ `严格路由`（Strict Route）是否已开启（在 Windows 10 及更高版本上默认开启），并按照 [Windows DNS 泄漏防护](@/advanced/windows_tun_mode.zh.md#strict-route)中的说明操作。

WebRTC 测试检查的是另一件事：你的 IP 地址，而不是 DNS。WebRTC 测试未显示任何公网 IP 地址是正常的（[#1267](https://github.com/throneproj/Throne/issues/1267)）。如果对于你走代理的网站，它显示了你真实的公网 IP 地址，说明 UDP 流量绕过了代理。这在系统代理模式下很常见；请改用 TUN 模式。

## 劫持与系统 DNS（已弃用） {#deprecated}

`路由设置`（Routing Settings）中的 `劫持`（Hijack）标签页和 Windows 上的 `系统 DNS`（System DNS）选项已在 1.3.1 中弃用，并将在下一个版本中移除。劫持功能会运行一个本地 DNS 服务器，用固定地址应答选定的域名，而 `系统 DNS` 会让 Windows 使用该服务器。两者都是为忽略系统代理的应用而设的。`Tun 模式`（Tun Mode）可以覆盖相同的使用场景，因此请关闭它们，改用 `Tun 模式`。

启用劫持功能时，Throne 会在启动时显示警告。除非开启了 `基本设置`（Basic Settings）→ `样式`（Style）→ `显示系统 DNS 选项`（Show System DNS option），否则 `系统 DNS` 复选框会被隐藏。

## Android 版 {#android}

Throne for Android 在 `设置`（Settings）→ `DNS` 中提供相同的 DNS 设置。FakeIP 在那里称为 `启用 FakeDNS`（Enable FakeDNS）。在 VPN 模式下，Throne 始终会处理 VPN 内的 DNS 查询。
