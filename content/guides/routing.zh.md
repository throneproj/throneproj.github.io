+++
title = "路由"
description = "借助现成的路由配置档或你自己编写的规则，决定哪些流量经过代理、哪些直连、哪些被阻止。"
weight = 40
toc = true
+++

路由决定每个连接的去向：经过代理、直连，或者哪里也不去。内置的 `Default` 配置档会让所有流量经过代理，所以只有在你需要其他效果时才需要本页。

## 路由的工作原理 {#how-routing-works}

路由配置档由一组规则和 `其余流量`（Everything else goes to）组成，后者是没有任何规则匹配的流量所使用的出站。Throne 从上到下检查这些规则，第一条匹配的规则决定连接的去向。

| 出站 | 流量去向 |
| --- | --- |
| `代理`（Proxy） | 经过正在运行的配置档；开启了 WARP 或 Tor 时，还会经过它。 |
| `直连`（Direct） | 直接连接互联网。 |
| `阻止`（Block） | 哪里也不去。连接会被拒绝。 |
| `不经 WARP 的代理`（Proxy without WARP） | 经过正在运行的配置档，但不经过 WARP 或 Tor。参见 [WARP](@/advanced/warp.zh.md#warp-bypass)。 |
| 已保存的配置档 | 改为经过该配置档。仅可在规则中使用，参见[规则](#advanced-rules)。 |

`路由`（Routing）→ `出口方式`（Exit through）为 `代理` 流量添加最后一跳：`Cloudflare WARP`（参见 [WARP](@/advanced/warp.zh.md)）或 `Tor`（参见 [Tor](@/advanced/tor.zh.md)）。`所选配置档`（Selected profile）不添加任何跳点。

同一时间只有一个路由配置档处于活动状态。可以在 `路由`（Routing）菜单顶部的列表中切换，或通过托盘菜单 → `路由：<name>`（`Routing: <name>`）切换。正在运行的连接会以新规则重启。分组也可以使用自己的路由配置档，参见[按分组设置路由配置档](#group-routing)。

## 下载现成的配置档 {#download-profiles}

1. 打开 `路由`（Routing）→ `下载路由配置档`（Download routing profile），然后选择 `China`、`Iran` 或 `Russia`。
2. 保持勾选 `自动更新`（Auto update），然后点击 `确定`（OK）。
3. 在 `路由` 菜单顶部选择其中一个新配置档。仅下载并不会启用它。

| 配置档 | 作用 |
| --- | --- |
| `Bypass China`、`Bypass Iran`、`Bypass Russia` | 除该国的网站和 IP 地址以及你的本地网络外，其余流量全部走代理。 |
| `Proxy China Blocked`、`Proxy Russia Blocked` | 所有流量都直连，但在该国被封锁的网站除外。 |
| `Proxy Antizapret`、`Proxy Refilter`（俄罗斯） | 所有流量都直连，但 Antizapret 或 Re:filter 封锁列表中的网站除外。 |

如果你访问的大多数网站都在境外，请使用“Bypass”类配置档。“Proxy … Blocked”类配置档经过你服务器的流量更少，但被封锁却不在列表中的网站将无法打开。

这些列表维护在 [throneproj/routeprofiles](https://github.com/throneproj/routeprofiles) 中。如果下载失败，请另选一个 `远程规则集镜像`（Remote Rule-set Mirror，参见[规则集](#rule-sets)），然后重试。

## 路由配置档 {#profiles}

路由配置档在 `设置`（Settings）→ `路由设置`（Routing Settings）的 `路由`（Routing）标签页上管理，`路由`（Routing）菜单的最后一项也能打开它。`路由` → `编辑当前配置档`（Edit current profile）会在编辑器中打开活动配置档，在 `路由` 菜单中右键点击某个配置档则会打开该配置档。编辑器中的 `保存`（Save）会立即保存配置档，`路由设置` 中的 `取消`（Cancel）不会撤销这次保存。如果有连接正在运行，请点击“设置已更改，重启进行应用”提示中的 `重启`（Restart）。

配置档分为三种：

- **结构化配置档**，在 Throne 中通过[列表](#simple-rules)和[规则](#advanced-rules)编辑。大多数人只需要这一种。
- **[远程配置档](#remote-profiles)**，从 URL 下载。
- **[原始配置档](#raw-profiles)**，以 sing-box JSON 编写。

创建结构化配置档的步骤：

1. 在 `路由`（Routing）标签页上，点击 `新建`（New）→ `结构化配置档`（Structured profile）。
2. 输入 `名称`（Name），并选择 `其余流量`（Everything else goes to）。
3. 向列表中添加条目或添加规则，然后点击 `保存`（Save）。
4. 在 `路由`（Routing）菜单中启用它。

新配置档一开始就带有 `DNS 查询`（DNS queries）规则，它把 DNS 查询交给 Throne 的 DNS 处理。配置档的 `DNS` 标签页可以为它设置自己的 DNS 服务器，参见[按路由配置档设置 DNS](@/guides/dns.zh.md#route-dns)。当你有 OpenVPN 或 OpenConnect 配置档时会出现 `端点`（Endpoints）标签页，它会让这些配置档与代理同时运行，参见[分离隧道](@/advanced/vpn_profiles.zh.md#split-tunnel)。

`路由`（Routing）标签页上还有以下设置：

| 设置 | 作用 |
| --- | --- |
| `域名策略`（Domain Strategy）→ `默认域策略`（Default Domain Strategy） | Throne 解析服务器或直连网站的地址时，对 IPv4 或 IPv6 的偏好。 |
| `域名策略`（Domain Strategy）→ `解析域策略`（Resolve Domain Strategy） | 在规则运行之前解析每个域名，这样 IP 规则也能匹配域名。 |
| `更新`（Updates）→ `远程规则集镜像`（Remote Rule-set Mirror） | 存放在 GitHub 上的规则集和配置档从何处下载。默认值：`jsDelivr(Cloudflare)`。 |

## 列表 {#simple-rules}

配置档有四个列表：`直连`（Direct）、`代理`（Proxy）、`阻止`（Block）和 `不经 WARP 的代理`（Proxy without WARP）。在配置档的 `规则`（Rules）标签页上，它们是标有 `快速列表`（Quick list）的行；选中其中一行即可编辑它。输入一个条目后按 `Enter` 或点击 `添加`（Add）；粘贴多行会把它们全部添加。双击条目即可编辑它。

没有前缀的行会按其形式识别类型：`example.com` 成为域名后缀，`10.0.0.0/8` 成为 IP 范围，`app.exe` 成为程序，完整路径成为程序路径。内置规则集名称和 `.srs` URL 会成为规则集。前缀则明确指定类型：

| 行 | 匹配 |
| --- | --- |
| `domain:example.com` | 仅 `example.com`。 |
| `suffix:example.com` | `example.com` 及其所有子域名。 |
| `keyword:example` | 所有包含 `example` 的域名。 |
| `regex:^cdn[0-9]*\.example\.com$` | 匹配某个正则表达式（Go RE2 语法）的域名。 |
| `ruleset:geosite-youtube` | [规则集](#rule-sets)中的所有内容，按名称或 `.srs` URL 指定。 |
| `ip:10.0.0.0/8` | 一个 IP 范围，或单个地址，例如 `1.2.3.4`。 |
| `processName:Telegram.exe` | 某个程序，按文件名匹配。 |
| `processPath:C:\Program Files\App\app.exe` | 某个程序，按完整路径匹配。 |

- 前缀区分大小写：写 `processName`，而不是 `processname`。不带 `.exe` 的程序名（例如在 Linux 和 macOS 上）需要加上 `processName:`。
- 进程名必须完全匹配，包括大小写，在 Windows 上还包括 `.exe`。[连接标签页](#connections-tab)会显示确切的名称。
- 无法使用的条目会被拒绝，并说明原因，例如填写了带 `https://` 的 URL 而不是域名。

{% alert_info() %}
进程规则只能看到到达 Throne 的流量。在系统代理模式下，忽略代理的程序根本不会到达 Throne，因此请将进程规则与 `Tun 模式`（Tun mode）配合使用。参见 [Tun 模式](@/guides/tun_mode.zh.md#enable)。
{% end %}

**示例：除本国网站外全部走代理，并屏蔽广告。** 将 `其余流量`（Everything else goes to）设为 `代理`（Proxy）。在 `直连`（Direct）中填写：

```text
ruleset:geosite-ir
ruleset:geoip-ir
```

在 `阻止`（Block）中填写：

```text
ruleset:geosite-category-ads-all
```

将 `ir` 替换为你所在国家的代码，例如 `cn` 或 `ru`。

**示例：只让一个程序和一个网站走代理。** 将 `其余流量`（Everything else goes to）设为 `直连`（Direct）。在 `代理`（Proxy）中填写：

```text
processName:Telegram.exe
suffix:example.org
```

每个列表的作用相当于一条规则。默认情况下，它们按 `直连`、`代理`、`阻止`、`不经 WARP 的代理` 的顺序运行，而第一条匹配的规则胜出，因此如果 `直连` 中范围更广的某个条目匹配了同样的流量，`代理` 中的条目就不会生效。要设置例外，例如在 `geosite-ir` 走直连时让 `example.ir` 走代理，请将 `example.ir` 添加到 `代理`，然后在 `规则`（Rules）标签页上把 `代理` 行拖到 `直连` 行之上。

## 规则 {#advanced-rules}

`规则`（Rules）标签页按顺序列出配置档的所有规则。四个列表显示为标有 `快速列表`（Quick list）的行，`其余流量`（Everything else）始终排在最后。

- 拖动某一行即可调整顺序，也可以使用 `Alt+Up` 和 `Alt+Down`，或者右键点击 → `移到顶部`（Move to top）或 `移到底部`（Move to bottom）。
- 取消勾选某一行或按 `Space`，即可将其关闭而不删除。
- `复制`（Duplicate）和 `删除`（Delete）作用于所选规则，筛选框可以按名称、域名或应用查找规则。
- 有问题的规则会被标出，在修正之前无法保存该配置档。

要添加规则，请点击 `新建规则`（New rule）并输入 `名称`（Name）。在 `条件`（When）下点击 `+ 添加条件`（+ Add condition），选择一个条件并填写它的值（`+ 添加`（+ Add）可再添加一个值）。在 `动作`（Then）下选择如何处理匹配的流量：

| 动作 | 作用 |
| --- | --- |
| `代理`（Proxy）、`直连`（Direct）、`不经 WARP 的代理`（Proxy without WARP） | 把流量发往该处。 |
| `阻止`（Block） | 拒绝流量。`拒绝方式`（Reject with）决定如何拒绝。 |
| 某个特定配置档 | 让流量经过一个已保存的配置档，它显示为 `[group] name`。Throne 会在你启动的配置档之外同时运行它。 |
| `劫持 DNS`（Hijack DNS） | 用 Throne 的 DNS 应答 DNS 查询。 |
| `嗅探`（Sniff） | 探测连接的协议和域名，然后继续执行下一条规则。 |
| `解析`（Resolve） | 查询域名的 IP 地址，然后继续。 |
| `设置路由选项`（Set route options） | 应用 `连接选项`（Connection options），然后继续。 |
| `绕过`（Bypass） | 仅限 Linux 自动重定向。参见 [sing-box 文档](https://sing-box.sagernet.org/configuration/route/rule_action/)。 |

把流量发往某处的选项还带有 `连接选项`（Connection options）。`分片 TLS 握手`（Fragment the TLS handshake）和 `拆分为 TLS 记录`（Split into TLS records）的作用与配置档的 [TLS 分片](@/advanced/presets.zh.md#tls-fragment)选项相同，有助于直连访问被过滤器按名称拦截的网站；`伪造 SNI`（Spoof SNI）的作用与 [TLS 伪装](@/advanced/presets.zh.md#tls-spoof)相同。

| 条件 | 匹配内容 |
| --- | --- |
| `域名`（Domain）、`域名后缀`（Domain suffix）、`域名关键词`（Domain keyword）、`域名正则`（Domain regex） | 请求的域名。 |
| `IP 范围`（IP range）、`私有 IP`（Private IP） | 目标地址。 |
| `规则集`（Rule-set） | 规则集名称或 `.srs` URL。 |
| `端口`（Port）、`端口范围`（Port range） | 目标端口，例如 `443` 或 `1000:2000`。 |
| `来源 IP 范围`（Source IP range）、`来源端口`（Source port）等 | 连接的来源，例如你网络中的另一台设备。 |
| `进程名`（Process name）、`进程路径`（Process path）、`进程路径正则`（Process path regex） | 本机上的程序。`选择应用`（Choose app）可以从正在运行的程序和使用过网络的程序中选取一个。 |
| `网络`（Network）、`协议（嗅探）`（Protocol (sniffed)）、`IP 版本`（IP version） | `tcp`、`udp` 或 `icmp`；探测到的协议，例如 `tls` 或 `bittorrent`；`4` 或 `6`。 |
| `入站`（Inbound） | `mixed-in`（代理端口）或 `tun-in`（Tun 模式）。 |
| `Wi-Fi 名称（SSID）`（Wi-Fi name (SSID)）、`Wi-Fi BSSID` | 你所连接的 Wi-Fi 网络。在 macOS 上不可用。 |

每个条件是一个框：框中任意一个值匹配，该框即匹配；所有框都必须匹配。域名、IP 和规则集条件共用一个框，两个目标端口条件、来源地址以及来源端口也分别共用一个框。`反转`（Invert）让规则匹配它原本不会匹配的流量。没有条件的规则是错误的，因为它会捕获所有流量。底部的 `sing-box JSON` 显示核心实际收到的规则。

额外核心（Extra Core）配置档、完整的自定义配置以及包含自动选择器的代理链不能作为规则的配置档。

## 规则集 {#rule-sets}

规则集是存放在单独文件中的域名或 IP 范围列表。可以在列表中以 `ruleset:<name>` 的形式使用，或在规则的 `规则集`（Rule-set）条件中使用。

- **内置名称**：2000 多个。以 `geosite-` 开头的名称包含域名，例如 `geosite-youtube` 或 `geosite-category-ads-all`。以 `geoip-` 开头的名称包含 IP 范围，例如 `geoip-ir` 或 `geoip-telegram`。编辑器会在你输入时提示名称。
- **你自己的文件**：任何 sing-box 二进制规则集的 URL。文件名必须包含 `.srs`。

规则集会在配置档启动时下载。`路由`（Routing）→ `更新规则集`（Update rule-sets）会下载最新副本。如果 GitHub 在你的网络中被封锁或速度很慢，请更改 `路由设置`（Routing Settings）→ `路由`（Routing）→ `更新`（Updates）→ `远程规则集镜像`（Remote Rule-set Mirror）。该镜像同样适用于[屏蔽广告](#adblock)的广告列表和存放在 GitHub 上的路由配置档。

## 远程配置档 {#remote-profiles}

远程配置档是 Throne 从 URL 下载的结构化配置档，例如通过[下载路由配置档](#download-profiles)获得的那些。服务商也可以通过 [`throne://remoteroute/` 链接](@/advanced/deeplinks.zh.md#remoteroute)分享远程配置档。

要添加远程配置档，请在 `路由`（Routing）标签页上点击 `新建`（New）→ `远程配置档`（Remote profile），输入 `URL`，勾选 `自动更新`（Auto update），然后点击 `保存`（Save）。`预览`（Preview）会显示该 URL 提供的内容，`立即获取`（Fetch now）会立即用它替换规则。该 URL 可以提供 `throne://route/` 链接、链接的 Base64 文本或配置档的 JSON。原始配置档不能作为远程配置档。

自动更新还需要开启 `路由设置`（Routing Settings）→ `路由`（Routing）→ `更新`（Updates）→ `路由配置档自动更新`（Routing profiles auto update）→ `启用`（Enable），该项默认关闭。要立即更新，请点击 `路由`（Routing）标签页上的 `更新`（Update）。

{% alert_warning() %}
更新会替换规则和 `其余流量`（Everything else goes to），因此你对该配置档所做的更改会丢失。要自定义远程配置档，请先 `克隆`（Clone）它，然后在副本中取消勾选 `自动更新`（Auto update）。你禁用的规则和配置档自己的 DNS 设置会保留。
{% end %}

## 按分组设置路由配置档 {#group-routing}

分组可以使用自己的路由配置档连接，而不是使用 `路由`（Routing）菜单中的那个。例如，某个服务商的服务器可以使用 `Bypass Iran`，而其他所有分组都使用 `Default`。

1. 右键点击该分组的标签页并选择 `编辑分组`（Edit group）。
2. 选择一个 `路由配置档`（Routing Profile）。`默认（…）`（Default (…)）跟随 `路由` 菜单。
3. 点击 `确定`（OK）。

由你启动的配置档所在的分组决定。对于代理链或自动选择器，看的是代理链或自动选择器本身所在的分组，而不是其中各个配置档所在的分组。窗口标题和托盘提示会显示正在使用的路由配置档，[连接标签页](#connections-tab)修改的也是这个配置档。分组的路由配置档也会带上它自己的 [DNS 设置](@/guides/dns.zh.md#route-dns)（如果有的话）。

### 来自订阅 {#subscription-routing}

有些服务商会随订阅一起发送 Happ 格式的路由配置档。要使用它，请打开分组设置，在 `订阅`（Subscription）下勾选 `使用订阅提供的路由配置档`（Use the subscription's routing profile），点击 `确定`（OK），然后更新该订阅。

Throne 会把它保存为一个结构化路由配置档，使用服务商给出的名称。如果该分组的 `路由配置档`（Routing Profile）是 `默认（…）`（Default (…)），新配置档会成为该分组的路由配置档。每次更新都会替换它的规则。订阅中的 DNS 设置从不使用。

- 要永久修改它，请 `克隆`（Clone）它，并把副本选为该分组的 `路由配置档`（Routing Profile）。
- 该配置档属于这个分组。删除分组会同时删除它。

## 原始配置档 {#raw-profiles}

原始配置档是一个完整的 JSON 格式的 sing-box `route` 对象，用于规则编辑器未提供的功能。可通过 `新建`（New）→ `原始配置档`（Raw profile）创建。

出站以数字表示：`-1` 是 `proxy`，`-2` 是 `direct`，`-5` 是 `warp-bypass`（`不经 WARP 的代理`），配置档 ID 则表示该已保存的配置档。在 `"outbound":` 之后，编辑器会提示你的配置档。如果缺少 `final`，Throne 会使用 `proxy`。

原始配置档中没有定义内置规则集名称，Throne 也不会添加结构化配置档会获得的 DNS 步骤。对于 Tun 模式，请像这样开始编写规则：

```json
{
  "rules": [
    { "action": "sniff" },
    { "protocol": "dns", "action": "hijack-dns" },
    { "domain_suffix": ["example.com"], "outbound": -2 }
  ],
  "final": -1
}
```

`防止修改`（Prevent modifications）会完全按原样使用该 JSON，这可能导致 DNS、Xray 配置档和代理链失效。`屏蔽广告`（Block ads）、`启用 DNS 路由`（Enable DNS routing）以及连接标签页的操作都不适用于原始配置档，Throne for Android 也无法使用原始配置档。

## 连接标签页 {#connections-tab}

主窗口底部的 `连接`（Connections）标签页按程序分组列出当前打开的连接，并显示它们的目标、协议、出站和流量。将鼠标悬停在 `出站`（Outbound）列上可以查看连接匹配的规则；`final` 表示没有规则匹配。

右键点击某个连接，可以在正在使用的路由配置档中更改此类流量的去向：

- `直连`（Direct）、`代理`（Proxy）或 `阻止`（Block）会列出带复选框的目标：每一级域名（例如 `*.example.com`）、作为关键字的网站名称、连接没有域名时的 IP 地址，以及程序。勾选的目标会被添加到对应的列表中，并从其他列表中移除；取消勾选则会移除该目标。
- `特定配置档`（Specific profile）的作用相同，但会让目标经由你选择的配置档。

然后点击“设置已更改，重启进行应用”提示中的 `重启`（Restart）。目标会加入该列表已有的规则。如果该列表原本为空，它的新规则会添加到末尾，位于其上方、范围更广的规则仍可能先匹配，因此请在 `规则`（Rules）标签页上检查顺序。

对于原始配置档、启用了 `防止修改`（Prevent modifications）的配置档、开启了 `自动更新`（Auto update）的远程配置档、由订阅更新的配置档，以及在 `路由设置`（Routing Settings）打开期间，这些操作都不可用。要修改远程配置档或来自订阅的配置档，请先克隆它，参见[远程配置档](#remote-profiles)和[来自订阅](#subscription-routing)。

如果没有该标签页，请开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `核心`（Core）→ `统计`（Statistics）→ `启用连接统计`（Enable connection statistics）。

## 测试路由 {#route-lookup}

`路由`（Routing）→ `路由查询`（Route lookup）会显示一个连接将去往何处，而不会真正建立它。输入 `进程`（Process）、`域名`（Domain）或 `IP 地址`（IP address），根据需要调整 `端口`（Port）、`网络`（Network）和 `嗅探到的协议`（Sniffed protocol），然后点击 `测试`（Test）。结果会给出出站和作出决定的规则，以及连接沿途经过的每一条规则。

- 配置档运行时，测试的是正在运行的配置。否则请选择一个 `路由配置档`（Routing profile）：Throne 会构建它启动时将使用的配置，跳过端点规则，并用系统的解析器解析域名。
- `进程` 旁边的 `选取`（Pick）会列出正在运行的程序和曾被发现建立连接的程序，也可以让你浏览选择文件。

## 屏蔽广告 {#adblock}

`路由`（Routing）→ `屏蔽广告`（Block ads）会使用 217heidai/adblockfilters 项目的 `adblocksingbox` 列表，在当前活动的结构化或远程配置档中屏蔽广告。它在你自己的规则之前运行，因此无论是直连流量还是代理流量，广告都会被屏蔽。

如果某个网站无法正常使用，请关闭 `屏蔽广告`，检查是否是该列表屏蔽了它。如果只想在某一个配置档中屏蔽广告，请改为在该配置档的 `阻止`（Block）列表中填写 `ruleset:geosite-category-ads-all`。

## 分享配置档 {#share-profiles}

在 `路由`（Routing）标签页上选中一个配置档，然后点击 `导出`（Export）（`Ctrl+C`），即可将其复制为 `throne://route/` 链接。

要导入配置档，请点击链接，或者复制链接后在主窗口中按 `Ctrl+V`。这会添加该配置档，但不会将其设为活动配置档。在 `路由`（Routing）标签页上使用 `导入`（Import）（`Ctrl+V`）还会选中它，因此点击 `确定`（OK）后它就会成为活动配置档。

链接包含名称、`其余流量`（Everything else goes to）、规则（包括已禁用的规则）以及配置档自己的 DNS 设置。将流量发送到已保存配置档的规则会按名称引用该配置档；如果另一台设备上没有同名配置档，这些规则会使用 `代理`（Proxy）。OpenVPN 和 OpenConnect 端点在分享时不包含其凭据。关于链接格式，请参见[深度链接](@/advanced/deeplinks.zh.md#route)。

## Android 版 {#android}

Throne for Android 拥有相同的路由配置档、规则和规则集。从侧边菜单打开 `路由`（Routing），点按某个配置档即可将其设为活动配置档。不同之处如下：

- **应用规则。** `应用`（Apps）字段匹配 Android 应用；`未知应用`（Unknown apps）匹配找不到所属应用的连接。`包名正则`（Package name regex）匹配包名。这些规则在桌面版上永远不会匹配。
- **网络规则。** `网络类型`（Network type）匹配 Wi-Fi、移动数据或以太网，`按流量计费网络`（Metered network）匹配按流量计费的网络。桌面版在导入链接时会排除这些规则。
- **Wi-Fi 规则**需要将位置权限设为“始终允许”（Allow all the time），并开启位置信息。
- 不支持**原始配置档**，也不支持导入的链接中的 VPN 端点。
- `AdBlock` 和 `自动更新远程配置`（Auto update remote profiles）位于 `设置`（Settings）→ `路由`（Routing）中。
- 如果某个规则集无法下载，`仍然连接`（Connect anyway）会在没有它的情况下连接。在通过代理下载到它之前，使用它的规则不会匹配任何内容。
