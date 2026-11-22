+++
title = "测试与自动选择器"
description = "测试配置档以及它们能访问的服务，排序、置顶和清理列表，让自动选择器挑选最佳配置档，并扫描可用的 IP 地址、DNS 解析器和设置。"
weight = 60
toc = true
+++

测试不会停止正在运行的配置档。测试会跳过自动选择器配置档；请改为测试自动选择器所使用的各个分组。

## URL 测试 {#url-test}

URL 测试会检查配置档是否可用，并测量其延迟。Throne 会通过该配置档请求两次 `延迟测试 URL`（Latency Test URL），并显示第二次请求所用的时间。

- **选定的配置档：** 右键点击它们，选择 `测试`（Test）→ `URL 测试`（URL test，`Ctrl+Shift+S`）。
- **整个分组：** 选择 `分组`（Groups）→ `测试`（Test）→ `URL 测试`（URL test，`Ctrl+Shift+G`）。
- **正在运行的配置档：** 点击状态栏左侧的配置档名称。结果会显示在状态栏中。

`测试`（Test）→ `停止测试`（Stop testing，`Ctrl+.`）会停止正在进行的测试。

`测试结果`（Test Result）列会显示延迟（100 毫秒以内为绿色，300 毫秒以内为黄色，更高为红色）；测试失败时显示 `不可用`（Unavailable）（日志中会有一行包含 `测试错误`（test error）及其原因）；OpenVPN 或 OpenConnect 配置档已连接、但测试 URL 没有通过它返回响应时，显示 `连接成功`（Connect OK）。

这些设置位于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `测试`（Testing）→ `延迟`（Latency）。

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `延迟测试 URL`（Latency Test URL） | `http://cp.cloudflare.com/` | 通过每个配置档请求的地址。 |
| `超时`（Timeout，位于 `并发数` 旁边） | `3000` 毫秒 | 每次请求的时间限制。设置得太低时，启用多路复用的配置档因首次请求需要更多时间而会被判为失败。 |
| `并发数`（Concurrency） | `10` | 同时测试的配置档数量。 |
| `直连测试 URL`（Direct Test URL） | 空 | 在你的网络中无需代理即可访问的地址。自动选择器直接获取它，以分辨是互联网连接断开还是服务器失效。留空表示使用操作系统的网络状态。 |

## 出口 IP 测试 {#ip-test}

此测试会显示每个配置档的出口 IP 地址及其所属国家，也就是网站看到的地址。右键点击配置档并选择 `测试`（Test）→ `出口 IP`（Exit IP），或者选择 `分组`（Groups）→ `测试`（Test）→ `出口 IP`（Exit IP）。之后，`测试结果`（Test Result）列会显示国旗；如果包含了 `出口 IP`（Exit IP），还会显示出口 IP（参见[排序与筛选](#sort-filter)）。国家筛选器和自动选择器的 `仅指定国家`（Only countries）使用的就是这个国家。

配置档启动后，Throne 还会在窗口左下角和窗口标题中显示其出口的国家和城市。在 `测试`（Testing）→ `出口国家`（Exit Country）中，`Look up exit country` 可以关闭此功能，`Lookup service` 用于选择查询服务；`Automatic` 会先使用 IP2Location.io，出口 IP 测试也使用该服务。关于 Throne 会联系哪些服务，请参见[隐私与网络请求](@/reference/privacy.zh.md#network-requests)。

## 速度测试 {#speed-test}

速度测试会测量配置档的下载和上传速度。

- **选定的配置档：** 右键点击它们，选择 `测试`（Test）→ `速度测试`（Speed test，`Ctrl+Shift+P`）。
- **整个分组：** 选择 `分组`（Groups）→ `测试`（Test）→ `速度测试`（Speed test，`Ctrl+Alt+P`）。
- **当前连接：** 在配置档运行时，选择 `工具`（Tools）→ `速度测试当前连接`（Speed test current connection，`F6`）。

Throne 会逐个测试配置档。如果包含了 `速度`（Speed），`测试结果`（Test Result）列会在 `↓` 后显示下载速度，在 `↑` 后显示上传速度。

`设置`（Settings）→ `基本设置`（Basic Settings）→ `测试`（Testing）→ `速度测试`（Speed Test）→ `速度测试模式`（Speed test mode）决定测试的内容：`下载 + 上传`（Download + upload，默认）、`仅下载`（Only download）、`仅上传`（Only upload）或 `简单下载`（Simple download），后者下载 `简单下载 URL`（Simple Download URL），不搜索服务器。同一分区中的 `超时`（Timeout，默认 `5000` 毫秒）限制测试中每个部分的时长。

{% alert_warning() %}
对于每个配置档，速度测试都会在超时之前尽可能多地传输数据。测试一个大型分组可能会消耗大量流量。
{% end %}

## 服务检查 {#service-check}

服务检查会显示哪些服务可以通过某个配置档使用，例如 AI 助手、流媒体和社交网络，以及该配置档的出口 IP 属于哪一类。右键点击配置档并选择 `测试`（Test）→ `服务检查`（Service check），或者选择 `分组`（Groups）→ `测试`（Test）→ `服务检查`（Service check）。

之后，`测试结果`（Test Result）列会为每个服务显示一个标志，标志上带有绿色、琥珀色或红色的角标。将鼠标悬停在标志上可以查看其状态（`可用`（Available）、`部分可用`（Partial）、`受限`（Restricted）、`已屏蔽`（Blocked）、`未知`（Unknown）或 `失败`（Failed）），悬停在单元格上可以查看检查日期和 IP 的类型：数据中心、移动网络、商业或住宅。要找出某个服务可用的配置档，请在 `测试结果` 筛选字段中输入该服务的名称（参见[排序与筛选](#sort-filter)）。

`设置`（Settings）→ `基本设置`（Basic Settings）→ `测试`（Testing）→ `服务检查`（Service Check）用于选择要检查的服务；其他服务既不检查也不显示。主窗口 `运行时统计`（Runtime Stats）标签页上的 `检查`（Check）会检查正在运行的配置档。

- 每次运行最多检查 100 个配置档。超过 20 个时，Throne 会先询问，因为每个配置档会向被检查的服务发送大约 20 个请求。
- 检查项列表每天最多下载一次；参见[隐私与网络请求](@/reference/privacy.zh.md#network-requests)。

## 排序与筛选 {#sort-filter}

点击列标题即可按该列排序，再次点击会反转顺序。按延迟排序时，最快的配置档排在最前，随后是测试失败的配置档，未测试的配置档排在最后。分组会一直保持排序，测试、订阅更新和导入之后也是如此，直到你右键点击某个列标题并选择 `停止排序`（Stop sorting），或者把某一行拖到别处。

右键点击 `测试结果`（Test Result）列标题，可以选择该列显示的内容（`出口 IP`、`速度`）以及排序依据（`延迟`（Latency）、`下载速度(↓)`（Download speed）、`上传速度(↑)`（Upload speed）、`出口 IP`（Exit IP））。

要筛选列表，请按 `Ctrl+F`，然后在 `类型`（Type）、`地址`（Address）或 `名称`（Name）列标题下方的字段中输入，或在 `测试结果`（Test Result）下方的 `按国家或服务筛选...`（Filter by country or service...）中输入。在 `地址`（Address）字段中，`port=443` 显示端口为 443 的配置档，`port=1000:2000` 显示端口在 1000 到 2000 之间的配置档。再次按 `Ctrl+F` 会隐藏并清空这些字段。

`测试结果` 字段接受来自出口 IP 测试的国家代码（例如 `DE`），以及[服务检查](#service-check)中服务的名称或类别：`gemini` 显示 Gemini 可用的配置档，`!netflix` 显示 Netflix 拒绝访问的配置档。所有词都必须匹配，因此 `DE gemini` 显示 Gemini 可用的德国配置档。

### 置顶配置档 {#pin}

右键点击配置档并选择 `置顶`（Pin to top），即可让它们按你置顶的顺序保持在所在分组的其他配置档之上。排序只会移动未置顶的配置档，两者之间以一条线分隔。当所选配置档全部已置顶时，该菜单项显示为 `取消置顶`（Unpin）。把某一行拖到已置顶的配置档之间也会将其置顶。只要配置档仍在订阅中，置顶在订阅更新后依然保留。

## 清理 {#clean-up}

`分组`（Groups）→ `清理`（Clean up）（右键点击分组标签页时也有）会从当前分组中移除配置档：

| 命令 | 移除的内容 |
| --- | --- |
| `移除重复项`（Remove duplicates） | 与之前某个配置档完全相同（包括名称）的配置档。 |
| `移除不可用项`（Remove unavailable） | 上次测试失败的配置档。它从不移除正在运行的配置档。 |
| `移除无效项`（Remove invalid） | 被核心判定为无效而拒绝的配置档。 |
| `移除不安全配置档`（Remove insecure profiles） | 未加密、TLS 不校验证书，或者使用旧的 Shadowsocks 加密方式的配置档。 |

其他命令如果移除了正在运行的配置档，会将其停止。`分组`（Groups）→ `测试`（Test）→ `清除结果`（Clear results，`Ctrl+Shift+C`）只清除测试结果。

要查看哪些配置档被视为不安全，请开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `外观`（Appearance）→ `配置列表`（Profile List）→ `显示配置档安全信息`（Show profile security）：之后不安全的配置档会在 `类型`（Type）列中带有警告标志。

要自动清理，可以使用分组选项 `自动清除不可用配置档`（Auto clear unavailable profiles），它会在该分组每次 URL 测试后删除测试失败的配置档；也可以使用订阅分组的[每次更新之后](@/guides/subscriptions.zh.md#after-update)选项，它们还能测试分组并排序。

## 自动选择器 {#auto-selector}

自动选择器是一种配置档，它会从一个或多个分组中挑选最好的可用配置档，持续检查其他配置档，并在当前配置档变差或失效时切换。订阅更新带来的新配置档会自动加入其中。

1. 选中它要使用的分组的标签页。
2. 选择 `程序`（Program）→ `新建配置档`（New profile，`Ctrl+N`）。编辑器打开时，`类型`（Type）已选为 `自动选择器`（Auto Selector）。
3. 输入 `名称`（Name）。
4. 在 `配置档来自`（Profiles from）中勾选要从中挑选的分组。当前分组已被勾选。
5. 点击 `确定`（OK），然后像启动其他配置档一样启动这个新配置档。

| 设置 | 作用 |
| --- | --- |
| `配置档来自`（Profiles from） | 使用其配置档的分组。所有勾选分组中的配置档会一起排名。 |
| `仅名称匹配`（Only names matching） | 可选的正则表达式；只使用名称与之匹配的配置档。可以匹配名称中的任意位置，且不区分大小写：`germany\|nl` 会使用所有包含 `germany` 或 `nl` 的名称，`^(?!.*(germany\|🇩🇪)).*$` 会使用所有既不包含 `germany` 也不包含 🇩🇪 的名称。 |
| `选择方式`（Choose） | `最快`（Fastest，默认）使用测量结果最好的配置档。`按优先级顺序`（In priority order）使用 `优先级层级`（Priority tiers）。 |
| `优先级层级`（Priority tiers） | 选择 `按优先级顺序` 时显示。每一行是一个 `分组`（Group）（或 `任意分组`（Any group）），并可带有一个可选的 `名称匹配`（Names matching）表达式。配置档归属于它匹配的第一行，不匹配任何一行的配置档排在最后。自动选择器使用含有可用配置档的最高一行，并在该行中选用测量结果最好的配置档。 |
| `最优配置档间分享流量`（Share traffic between the best profiles） | 关闭（默认）：由一个配置档承载全部流量，其他就绪的配置档待命。开启：流量分散到就绪的配置档上。使用 `每 30 秒轮换`（Rotate every 30 s，默认）时，新连接每 30 秒换到下一个配置档；使用 `按连接`（Per connection）时，每个新连接都可能使用另一个配置档，因此你的出口 IP 可能会在会话过程中改变。 |
| `首选配置档`（Preferred profile） | 在统计窗口中用 `使用这个配置档`（Use this profile）选择了某个配置档后出现。`使用自动(模式)`（Use automatic）会把选择权交还给自动选择器。 |

每个配置档都会像单独启动时一样，经由它自己所在分组的 `前置代理`（Front Proxy）和 `落地代理`（Landing Proxy）；自动选择器本身所在分组的这些代理不起作用。

`高级 ▾`（Advanced ▾）会显示更多选项，每个选项都有可用的默认值和工具提示。最常更改的是：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `仅指定国家`（Only countries） | 空 | 国家代码，例如 `DE,NL,FR`。`!` 表示排除某个国家：`!RU,!IR` 会使用除这两个国家以外的所有国家。使用[出口 IP 测试](#ip-test)得出的国家，因此设置此项后，没有国家信息的配置档会被跳过。 |
| `运行最优的`（Run the best） | 300 个配置档 | 加载到运行配置中的配置档数量。自动选择器在它们之间切换时无需重新连接。 |
| `切换容差`（Switch tolerance） | 300 毫秒 | 另一个配置档必须快多少，自动选择器才会切换到它。 |
| `最大延迟`（Maximum latency） | 无限制 | 比此值更慢的配置档只在没有更快的配置档可用时才会使用。 |
| `配置档失败时断开连接`（Drop connections when a profile fails） | 开启 | 当前配置档失败时，打开的连接会立即转移到新的配置档。关闭时，它们会在失败的配置档上自行结束。 |
| `从实际连接中学习`（Learn from real connections） | 关闭 | 还会根据你的应用的实际连接来评判配置档，并把屡次失败的配置档搁置一旁。 |

当可用的配置档多于 `运行最优的` 的值时，自动选择器会先对没有近期测试结果的配置档进行 URL 测试（成功结果的有效期为 24 小时，失败结果为 1 小时），再加载其中最好的。只要有几个配置档可用，它就会启动，在后台完成其余测试，如果排名发生变化则重新启动一次。如果所有运行中的配置档都失效，它会改用排名其次的配置档重新构建。电脑离线时它会暂停。它的日志行以 `[自动选择器]`（[Auto selector]）开头。

自动选择器运行期间，`工具`（Tools）→ `自动选择器统计`（Auto Selector Stats）会显示每个配置档的状态和延迟。`使用这个配置档`（Use this profile）让所选配置档保持使用，`切回自动`（Back to automatic）让排名重新进行选择，`立即检查全部`（Check all now）立即测量所有运行中的配置档。

限制：

- 代理链可以把一个自动选择器作为其中一跳，但不能同时包含额外核心（Extra Core）配置档或自定义配置；参见[代理链的限制](@/advanced/chains.zh.md#chain-limits)和[测试代理链](@/advanced/chains.zh.md#test-chain)。自动选择器不能作为 `前置代理`（Front Proxy）或 `落地代理`（Landing Proxy）。
- 它会跳过代理链、其他自动选择器、OpenVPN、OpenConnect、Tailscale、额外核心（Extra Core）、sing-box 完整配置、无法读取的自定义配置，以及无法与其所在分组的前置代理或落地代理组合的 Xray 完整配置。

## IP 扫描器 {#ip-scanner}

`工具`（Tools）→ `IP Scanner` 会检查 IP 地址列表，并保留在你的网络中可用的地址：你的服务器所在 CDN 的未被封锁的地址、可用的 Cloudflare WARP 端点，或者用于 DNS 隧道的 DNS 解析器。扫描结果会组成一个 IP 列表，分组或配置档可以把它用作[服务器地址](@/guides/subscriptions.zh.md#server-address)。

1. 点击 `New scan`，输入 `Name` 并选择扫描类型：
   - `Generic scan` 用 ping、TCP、TLS 或 HTTP 检查地址，也可以通过你的某个配置档进行检查。
   - `WARP scan` 查找能完成 WireGuard、AmneziaWG 或 MASQUE 连接的 WARP 端点。
   - `DNS 解析器扫描`（DNS resolver scan）为 DNS 隧道配置档查找解析器；参见 [DNS 解析器扫描](#dns-scan)。
   - `查找可用设置`（Find working settings）尝试的是某个配置档的各种设置，而不是地址；参见[查找可用设置](#find-working-settings)。
2. 点击 `确定`（OK）。扫描窗口随即打开。
3. 在 `Targets` 标签页上设置目标，在 `Phases` 标签页上设置检查项。
4. 点击 `Start`。通过检查的地址会逐渐填入 `Results` 标签页。

关闭扫描窗口后，扫描仍会继续运行。

`Targets` 标签页：

- `Base IP list` 是要扫描的地址；`Manage` 会打开 [IP 列表](#ip-lists)。在 WARP 扫描中，`Use built-in WARP ranges` 会为所选 WARP 模式选择列表和端口。
- `Ports` 会与列表中保存的端口合并，除非你在旁边另行选择。没有端口的地址会在 443 端口上扫描，纯 HTTP 则为 80 端口。
- `Stop after (results)` 在结果达到此数量时结束扫描。`Concurrency` 设置同时检查多少个地址。
- 除非勾选 `Scan IPv6 addresses`，否则会跳过 IPv6 地址。

`Phases` 标签页包含各项检查。地址必须按以下顺序通过所有已开启的检查：

| 阶段 | 默认值 | 检查内容 |
| --- | --- | --- |
| `ICMP (ping)` | 关闭 | 地址响应 ping。 |
| `TCP 连接`（TCP Connect） | 开启 | 端口接受 TCP 连接。仅限 `Generic scan`。 |
| `TLS / HTTP` | 关闭 | TLS 握手成功；并且除非 `Method` 为 `None (TLS handshake only)`，HTTP 请求会得到 200 OK 响应。仅限 `Generic scan`。 |
| `配置测试`（Config Test） | 关闭 | 将所选 `配置档`（Profile）的副本指向该地址，并加载 `Test URL`。这样可以找到真正适用于你的服务器的地址，例如 CDN 地址。仅限 `Generic scan`。 |
| `WARP 测试`（WARP Test） | 开启 | 通过该地址、以所选 `Mode`（`WireGuard`、`AmneziaWG` 或 `MASQUE`）建立的 WARP 连接可以工作。仅限 `WARP scan`。 |

`WARP 测试` 需要一个 WARP 身份。默认选项 `Dedicated for this scan (recommended)` 需要点击一次 `Register`，它会向 Cloudflare 注册一个新的 WARP 设备。

在 `Results` 标签页上，`Save as IP list` 会把结果复制到一个新的 IP 列表。

扫描已有结果时，`Start` 会询问要做什么：`Scan from the beginning` 会清空结果并重新扫描基础列表；`Rescan current results` 只重新检查已有结果，并移除不再可用的地址。

### DNS 解析器扫描 {#dns-scan}

DNS 解析器扫描用于查找能够中继你的某个 [DNS 隧道](@/advanced/dns_tunnels.zh.md)配置档的隧道的解析器，适用于 DNSTT（包括 VayDNS 模式）、MasterDNS，以及带 XDNS 的 VLESS (Xray)。它会把基础列表中的每个地址分别作为该配置档唯一的解析器进行尝试，并保留通过测试的解析器。

要创建这种扫描，请在 `New scan` 中选择 `DNS 解析器扫描`（DNS resolver scan），或者在已保存的 DNS 隧道配置档的编辑器中，点击 `IP 列表`（IP list）旁边的 `查找解析器`（Find resolvers），这会为该配置档打开或新建一个扫描。扫描测试的是配置档最后一次保存时的状态。

在 `Targets` 标签页上，把要尝试的解析器选为 `Base IP list`，例如 `Iran DNS resolvers` 或 `Russia DNS resolvers`。这里没有 `Ports` 字段：每个地址都在列表中保存的端口上尝试，没有端口时使用 53 端口。

`Phases` 标签页只有一项检查，即 `DNS 隧道测试`（DNS Tunnel Test），其中有 `配置档`（Profile）、`测试`（Test）以及测试单个解析器的总时限 `超时 (毫秒)`（Timeout (ms)）。对于每种配置档，每项测试都会同时完成排在它之前的测试的检查：

| 测试 | 配置档 | 检查内容 |
| --- | --- | --- |
| `轮询：中继一个隧道查询`（Poll: relays one tunnel query） | DNSTT、XDNS | 解析器把一个隧道查询转发给隧道服务器，并返回有效的应答。 |
| `查询名：还能中继与配置档所发送的同样长的名称`（Query names: also relays names as long as the profile sends）（默认） | DNSTT、XDNS | 解析器还能中继与配置档所发送的同样长的查询名。扫描会找出该解析器能中继的最长名称。 |
| `握手：还能建立隧道会话`（Handshake: also opens a tunnel session） | DNSTT | 能通过该解析器与服务器建立隧道会话。 |
| `快速：中继最小的数据包`（Quick: relays the smallest packets）（默认） | MasterDNS | 解析器能中继配置档所需的最小尺寸的查询和应答。 |
| `完整：还会测量上传和下载 MTU`（Full: also measures the upload and download MTU） | MasterDNS | 扫描还会找出该解析器能中继的最大查询和最大应答。 |

在 `Results` 标签页上，`Latency` 是解析器的应答用时。`最大 QNAME`（Max QNAME，DNSTT 和 XDNS）是解析器能中继的最长查询名，DNSTT 使用 `最大 QNAME 长度`（Max QNAME Length）的单位，XDNS 使用 `lenLimit` 的单位。`上传 MTU`（Upload MTU）和 `下载 MTU`（Download MTU）（MasterDNS）是每个查询和每个应答中的最大有效载荷。未通过的解析器不会保留；日志会显示每个解析器停在了哪一步。

在 `Results` 标签页上点击 `用作解析器`（Use as resolvers），扫描的结果列表就会成为该配置档的 `IP 列表`（IP list）。配置档中手动填写的解析器会保留，并优先使用。配置档每次启动时都会读取该列表，因此会随扫描而变化：`Scan from the beginning` 会清空列表，`Rescan current results` 会移除不再可用的解析器。如需固定不变的一组解析器，请点击 `Save as IP list`，再把那个列表选为配置档的 `IP 列表`。

### 查找可用设置 {#find-working-settings}

这种扫描会尝试某个配置档的反审查设置的各种变体，每种变体尝试多次，并对它们进行排名，以找出在你的网络中能够通过的设置。右键点击配置档并选择 `测试`（Test）→ `查找可用设置`（Find working settings），这会打开该配置档的扫描或新建一个扫描；也可以在 `新建扫描`（New scan）中选择 `查找可用设置`。

扫描窗口中用 `设置`（Settings）标签页代替了 `目标`（Targets）和 `阶段`（Phases）标签页：

- `要尝试的项目`（What to Try）用于选择要变化的设置：`uTLS 指纹`（uTLS fingerprint）、`TLS 分片`（TLS fragment）、`TLS 记录分片`（TLS record fragment）、`混合大小写 SNI`（Mixed-case SNI）、`QUIC 前导包`（QUIC opener）和 `MTU (WireGuard)`。每一项先单独尝试，然后把有帮助的更改组合起来。配置档无法使用的设置会显示为灰色，其工具提示中会说明原因。
- `节奏`（Pacing）用于限制尝试次数和时间，并设置 `测试 URL`（Test URL）和 `超时 (毫秒)`（Timeout (ms)）。

`启动`（Start）总是从头开始。`结果`（Results）标签页按 `通过`（Passed）和 `延迟中位数`（Median latency）对变体进行排名，并把最好的一个标为 `推荐`（Recommended）。在你选中某个结果并点击 `应用到配置档`（Apply to profile），或点击 `另存为新配置档`（Save as new profile）添加一个使用这些设置的副本之前，配置档不会有任何改动。

它无法搜索代理链（请改为搜索其中的跳点）、Xray 配置档，或者不使用 TCP 上的 TLS、QUIC 或 WireGuard 的配置档。配置档必须先保存。

### IP 列表 {#ip-lists}

在 `IP Scanner` 窗口中点击 `IP Lists`，即可管理扫描所读取、分组和配置档所使用的列表。Throne 自带 `Cloudflare CDN`、`Fastly CDN`、`Gcore CDN`、`Cloudflare WARP (WireGuard)`、`Cloudflare WARP (MASQUE)`、`Iran DNS resolvers` 和 `Russia DNS resolvers`。`Import` → `Add default lists` 可以恢复它们。

- `New` 创建一个列表。其 `Source` 为 `Manual`（由你填写条目）、`URL`（Throne 下载的地址）或 `Rule-set`（某个规则集的 IP 范围，例如 `geoip-ir`，或规则集 URL）。`URL` 或 `Rule-set` 列表可以通过 `Auto update` 自动刷新，间隔不少于 30 分钟。
- 每行写一个条目，例如 `1.2.3.4`、`1.2.3.0/24`、`1.2.3.4:443`、`[2606:4700::1]:443`、`1.2.3.0/24 443` 或 `1.2.3.1-1.2.3.9`。

每个扫描的结果也是一个列表，标有“Result of scan”和扫描名称。分组或配置档可以直接使用它，但 `Scan from the beginning` 会清空它；如需内容不变的列表，请使用 `Save as IP list`。

## Android 版 {#android}

Throne for Android 提供相同的测试和相同的自动选择器。不同之处：

- **菜单。** 在 `配置`（Profiles）界面上，`⋮` 菜单提供 `测试`（Test）（`URL 测试`（URL test）、`IP 与国家测试`（IP & country test）、`速度测试`（Speed test）、`停止测试`（Stop testing））、`删除`（Remove）和 `排序`（Sort）。对于选中的配置档，请使用选择菜单中的 `测试`（Test）；对于单个配置档，请使用它的 `⋮` 按钮。
- **测试面板。** 面板会显示测试的进度和结果，并提供一些操作，例如 `按延迟排序`（Sort by latency）、`删除不可用`（Remove unavailable）和 `连接最快的`（Connect to fastest）。
- **当前连接。** 连接后，点按统计栏即可测试连接。长按统计栏可打开 `实时图表`（Live graphs）和 `测试当前连接的速度`（Speed test current connection）。统计栏还会显示出口国家；`设置`（Settings）→ `测试`（Testing）中有 `Look up exit country` 和 `Lookup service`。
- **自动选择器。** 通过 `添加服务器配置`（Add profile）→ `手动输入`（Manual settings）→ `自动选择`（Auto selector）创建。在 `配置`（Profiles）界面上点击它的状态行，即可打开 `自动选择统计`（Auto selector stats）。
- **IP 扫描器。** Android 版没有。
