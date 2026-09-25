+++
title = "测试与自动选择器"
description = "测试配置档的延迟、出口 IP 和速度，对列表进行排序和筛选，移除失效的配置档，并让自动选择器挑选最佳服务器。"
weight = 60
toc = true
+++

Throne 可以测试你的配置档，帮助你只保留好用的那些。本页介绍 URL 测试、IP 与国家测试、速度测试、排序与筛选、清理，以及会替你挑选最佳服务器的自动选择器。

测试不会停止正在运行的配置档。测试会跳过自动选择器配置档；请改为测试自动选择器所使用的分组。

## URL 测试 {#url-test}

URL 测试会检查配置档是否可用，并测量其延迟。Throne 会通过该配置档请求两次 `延迟测试 URL`（Latency Test URL），并显示第二次请求所用的时间（以毫秒为单位）。

要开始 URL 测试：

- **选定的配置档：** 右键点击它们，选择 `URL 测试选定项`（Url Test Selected，`Ctrl+Shift+S`）。
- **整个分组：** 选择 `分组`（Groups）→ `URL 测试本组`（Url Test Group，`Ctrl+Shift+G`），或者右键点击分组标签页，选择 `URL 测试选定分组`（Url Test selected Group）。
- **正在运行的配置档：** 点击状态栏左侧的配置档名称。Throne 会对当前连接测试一次，并在状态栏中显示 `测试结果:`（Test Result:）加上时间，或者显示 `不可用`（Unavailable）。

测试进行期间，右键菜单和 `分组`（Groups）菜单中会出现 `停止测试`（Stop Testing，`Ctrl+.`）。

`测试结果`（Test Result）列会显示以下内容之一：

| 结果 | 含义 |
| --- | --- |
| 时间，例如 `85 ms` | 该配置档可用。时间在 100 毫秒以内显示为绿色，300 毫秒以内为黄色，超过 300 毫秒为红色。 |
| `不可用`（Unavailable） | 测试失败。日志中会有一行包含 `测试错误`（test error）及其原因。 |
| `连接成功`（Connect OK） | OpenVPN 或 OpenConnect 配置档已连接，但测试 URL 没有通过它返回响应。 |

测试设置位于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `通用`（Common）中的 `测试`（Testing）部分：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `延迟测试 URL`（Latency Test URL） | `http://cp.cloudflare.com/` | Throne 通过每个配置档请求的地址。 |
| `超时`（Timeout，位于 `并发数` 旁边） | `3000` 毫秒 | 每次请求的时间限制。不要设置得太低：启用多路复用的配置档在首次请求时需要更多时间，超时过短会把它们误判为失败。 |
| `并发数`（Concurrency） | `10` | 同时测试的配置档数量。 |
| `直连测试 URL`（Direct Test URL） | 空 | 不经过任何代理直接获取，使自动选择器能够分辨是互联网连接断开还是服务器失效。请使用在你的网络中无需代理即可访问的地址。留空表示 Throne 使用操作系统的网络状态。 |

要复制选定配置档的结果，请右键点击它们，选择 `分享`（Share）→ `复制测试结果`（Copy Test Result）。

## IP 与国家测试 {#ip-test}

此测试会显示每个配置档的出口 IP 地址及其所属国家。这就是网站看到的地址。

- **选定的配置档：** 右键点击它们，选择 `解析选定的出口 IP`（Resolve Selected Out IP）。
- **整个分组：** 选择 `分组`（Groups）→ `为本组解析 IP`（Resolve out IP for group）。

Throne 会通过每个配置档请求 `https://api.ip2location.io/`。之后，`测试结果`（Test Result）列会显示国旗；如果包含了 `出口 IP`（Out IP），还会显示出口 IP（参见[排序与筛选](#sort-filter)）。该测试使用 URL 测试的 `超时`（Timeout）和 `并发数`（Concurrency）设置。

国家信息会被国家筛选器以及自动选择器的 `仅指定国家`（Only countries）选项使用。关于 Throne 会联系哪些服务，请参见[隐私与网络请求](@/reference/privacy.zh.md#network-requests)。

## 速度测试 {#speed-test}

速度测试会测量配置档的下载和上传速度。

- **选定的配置档：** 右键点击它们，选择 `速度测试选定项`（Speedtest Selected，`Ctrl+Shift+P`）。
- **整个分组：** 选择 `分组`（Groups）→ `速度测试本组`（Speedtest Group，`Ctrl+Alt+P`），或者右键点击分组标签页，选择 `速度测试选定分组`（Speed Test selected Group）。
- **当前连接：** 在配置档运行时，选择 `工具`（Tools）→ `速度测试当前项`（Speedtest Current，`F6`）。

Throne 会逐个测试配置档。之后，如果包含了 `速度`（Speed），`测试结果`（Test Result）列会在 `↓` 后显示下载速度，在 `↑` 后显示上传速度。

在 `设置`（Settings）→ `基本设置`（Basic Settings）→ `通用`（Common）→ `速度测试模式`（Speedtest mode）中选择测试的内容：

| 模式 | 作用 |
| --- | --- |
| `下载 + 上传`（Download + Upload，默认） | 先找到附近的 Speedtest 服务器，然后测量下载和上传速度。 |
| `仅下载`（Only Download） | 仅测量下载速度。 |
| `仅上传`（Only Upload） | 仅测量上传速度。 |
| `简单下载`（Simple Download） | 下载 `简单下载 URL`（Simple Download URL）处的文件，默认为 `http://cachefly.cachefly.net/1mb.test`。不搜索服务器。 |
| `仅国别`（Only Country） | 只查找最近的 Speedtest 服务器并显示其所在国家。速度快，几乎不消耗流量，并且可以同时测试许多配置档。 |

`速度测试模式`（Speedtest mode）旁边的 `超时`（Timeout，默认 `5000` 毫秒）限制测试中每个部分的时长。

{% alert_warning() %}
对于每个配置档，速度测试都会在超时之前尽可能多地传输数据。测试一个大型分组可能会消耗大量流量，如果你的套餐有流量限制，这一点尤其需要注意。这些数据会计入每个配置档的 `流量`（Traffic）列。
{% end %}

## 排序与筛选 {#sort-filter}

要对分组中的配置档排序：

- 点击列标题即可按该列排序。再次点击会反转顺序。Throne 会保存新的顺序。
- 首次点击按延迟排序时，最快的配置档排在最前。随后是测试失败的配置档，未测试的配置档排在最后。
- 右键点击 `测试结果`（Test Result）列标题，可以选择该列显示的内容（`包含:`（Include:）`出口 IP`、`速度`）以及排序依据（`排序依据:`（Sort By:）`延迟`（Latency）、`下载速度(↓)`（Download Speed）、`上传速度(↑)`（Upload Speed）、`IP 出口`（IP Out））。
- 右键点击 `流量`（Traffic）列标题，可以按 `合计(Σ)`（Total）、`下载(↓)`（Downloaded）或 `上传(↑)`（Uploaded）排序。
- 拖动行可以把它们排成任意顺序。筛选开启时无法拖动。

订阅更新会把配置档恢复为服务商列表中的顺序。要在每次更新后对订阅分组排序，请使用它的 `Sort by latency` 选项；参见[每次更新之后](@/guides/subscriptions.zh.md#after-update)。

要筛选列表：

1. 按 `Ctrl+F`，或点击分组标签栏右端的筛选按钮。
2. 在 `类型`（Type）、`地址`（Address）或 `名称`（Name）列标题下方的字段中输入，或在 `测试结果`（Test Result）下方的 `按国别筛选...`（Filter by country...）中输入。

之后列表只显示包含该文本的配置档；不区分大小写。在 `地址`（Address）字段中，`port=443` 显示端口为 443 的配置档，`port=1000:2000` 显示端口在 1000 到 2000 之间的配置档。范围的一端可以留空，例如 `port=8000:`。国家字段匹配来自 IP 测试或速度测试的国家代码，例如 `DE`。再次按 `Ctrl+F` 会隐藏这些字段，同时也会清空它们。

## 清理 {#clean-up}

这些命令位于 `分组`（Groups）菜单中，作用于当前分组。

| 命令 | 快捷键 | 移除的内容 |
| --- | --- | --- |
| `移除重复项`（Remove Duplicates） | `Ctrl+Shift+D` | 与之前某个配置档完全相同（包括名称）的配置档。保留第一个副本。 |
| `移除不可用项`（Remove Unavailable） | `Ctrl+Shift+R` | 上次测试失败的配置档。它从不移除正在运行的配置档。 |
| `移除无效项`（Remove Invalid） | `Ctrl+Alt+I` | 被核心判定为无效而拒绝的配置档。 |
| `移除不安全的配置`（Remove Insecure Configs） | – | 流量没有得到妥善保护的配置档：未加密、TLS 不校验证书，或者使用旧的 Shadowsocks 加密方式。 |
| `清除本组测试结果`（Clear Group test result） | `Ctrl+Shift+C` | 仅清除测试结果。配置档保留。 |

除非开启了 `设置`（Settings）→ `基本设置`（Basic Settings）→ `样式`（Style）→ `删除配置档时跳过确认`（Skip confirmation When Deleting Profiles），否则 Throne 在删除任何内容之前都会询问。如果 `移除重复项`（Remove Duplicates）、`移除无效项`（Remove Invalid）或 `移除不安全的配置`（Remove Insecure Configs）移除了正在运行的配置档，Throne 会停止它。

要查看哪些配置档被视为不安全，请开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `样式`（Style）→ `显示配置安全信息`（Show Config Security）。之后 `类型`（Type）列会显示每个配置档的安全性，不安全的配置档会带有警告标志。

要自动清理：

- 分组选项 `自动清除不可用配置档`（Auto Clear Unavailable Profiles）会在该分组每次 URL 测试后，不经询问直接删除测试失败的配置档。参见[分组选项](@/guides/subscriptions.zh.md#group-options)。
- 订阅分组可以在每次更新后移除重复、不安全、无效和测试失败的配置档。参见[每次更新之后](@/guides/subscriptions.zh.md#after-update)。

## 自动选择器 {#auto-selector}

自动选择器是一种特殊的配置档。启动它后，它会从一个分组中挑选最好的可用配置档，持续检查其他配置档，并在当前配置档变差或失效时切换。订阅更新带来的新服务器会自动加入其中。

要创建一个自动选择器：

1. 选中它要使用的分组的标签页。
2. 选择 `程序`（Program）→ `新建配置档`（New profile，`Ctrl+N`）。编辑器打开时，`类型`（Type）已选为 `自动选择器`（Auto Selector）。
3. 输入 `名称`（Name）。
4. 检查 `服务器来自`（Servers from）。它是自动选择器从中挑选配置档的分组。
5. 点击 `确定`（OK），然后像启动其他配置档一样启动这个新配置档。

编辑器会显示将会发生什么的摘要，例如该分组中有多少配置档可以使用。基本选项如下：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `服务器来自`（Servers from） | 当前分组 | 自动选择器使用其配置档的分组。 |
| `仅名称匹配`（Only names matching） | 空 | 可选的正则表达式。只使用名称与之匹配的配置档，例如用来挑选某个国家或服务商。不区分大小写。 |
| `最优配置档间分享流量`（Share traffic between the best profiles） | 关闭 | 关闭：由一个配置档承载全部流量，其他就绪的配置档待命。开启：流量分散到多个可用的配置档上；参见下文的 `负载均衡`（Load balancing）。 |
| `首选配置档`（Preferred profile） | – | 仅当你在统计窗口中用 `使用这个配置档`（Use this profile）选择了某个配置档后才会出现。`使用自动(模式)`（Use automatic）会把选择权交还给自动选择器。 |

`高级…`（Advanced…）会显示更多选项，分为 `要使用的配置档`（Which profiles to use）、`健康度检查`（Health checks）、`切换`（Switching）、`负载均衡`（Load balancing）和 `测试端点`（Test endpoints）几个部分。所有选项都有可用的默认值。

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `仅指定国家`（Only countries） | 空 | 以逗号分隔的国家代码，例如 `DE,NL,FR`。使用 IP 测试得出的国家，因此设置此项后，从未进行过 IP 测试的配置档会被跳过。 |
| `运行最优的`（Run the best） | 300 个配置档 | 加载到运行配置中的配置档数量。自动选择器在它们之间切换时无需重新连接。 |
| `最多排名`（Rank at most） | 1000 个配置档 | 被测量并保留在排名列表中的配置档数量。替补配置档从这个列表中选取。 |
| `信任结果维持`（Trust results for） | 1440 分钟 | 不超过此时长的 URL 测试结果会被直接复用，不再重新测试。0 表示总是重新测试。 |
| `跳过失败的配置档`（Skip failed profiles） | 开启 | 在上次测试失败的结果仍被信任期间，排除这些配置档。 |
| `保持就绪`（Keep ready） | 3 个配置档 | 保持在确认可用状态的配置档数量，以便出现故障时能立即接替。 |
| `仔细检查`（Check closely） | 8 个配置档 | 在每个 `检查间隔` 内被检查的最佳配置档数量。 |
| `检查间隔`（Check interval） | 300 秒 | 被仔细检查的配置档多久测量一次。 |
| `完整扫描每隔`（Full sweep every） | 600 秒 | 对所有运行中的配置档完整检查一轮所用的时长。 |
| `监视使用中的配置档`（Watch profile in use） | 15 秒 | 单独检查承载你流量的配置档的频率。 |
| `保留样本`（Samples kept） | 10 | 排名在计算平均延迟和抖动时使用的最近检查次数。 |
| `切换容差`（Switch tolerance） | 300 毫秒 | 另一个配置档必须至少快这么多，自动选择器才会切换到它。 |
| `最大延迟`（Maximum latency） | 无限制 | 比此值更慢的配置档永远不会被选中。 |
| `故障切换尝试次数`（Failover attempts） | 2 | 当选中的配置档连接失败时，在应用看到错误之前立即尝试的其他配置档数量。 |
| `切换时断开连接`（Drop connections on switch） | 开启 | 开启：因出现问题而切换后，所有连接会立即转移到新的配置档。关闭：正在进行的下载会在旧配置档上完成。 |
| `模式`（Mode，负载均衡） | `按计时器轮换(保持会话稳定)`（Rotate on a timer (keeps sessions stable)） | 与 `最优配置档间分享流量` 配合使用。另一种模式是 `按连接(分布最广泛分散)`（Per connection (widest spread)），在该模式下，每个新连接都可以使用不同的配置档，你的出口 IP 可能会在会话过程中改变。 |
| `轮换每隔`（Rotate every） | 30 秒 | 用于计时器模式：自动选择器在一个配置档上停留多久，之后新连接会转到下一个配置档。 |
| `测试 URL`（Test URL） | 空 | 用于测量配置档的地址。留空表示使用全局的 `延迟测试 URL`。 |
| `连通性 URL`（Connectivity URL） | 空 | 不经过代理直接获取，用于发现你的互联网连接何时中断。留空表示使用测试设置中的 `直连测试 URL`。 |

运行方式：

- 启动之前，它会对在 `信任结果维持`（Trust results for）时限内没有测试结果的配置档进行 URL 测试，并进行排名。然后把其中最好的配置档（数量为 `运行最优的`（Run the best）的值）加载到运行配置中。日志中会显示以 `[自动选择器]`（[Auto selector]）开头的行。
- 如果所有运行中的配置档都停止工作达 20 秒，它会改用排名其次的配置档重新构建。多次重建之间的等待时间会逐渐变长，从 60 秒起，最长 10 分钟。
- 如果你的电脑没有网络连接，检查会暂停，直到网络恢复。

自动选择器运行期间，`工具`（Tools）→ `自动选择器统计`（Auto Selector Stats）会打开它的统计窗口。表格按配置档列出 `配置档`（Profile）、`状态`（Status）、`延迟`（Latency）、`抖动`（Jitter）、`检查数`（Checks）、`连接数`（Connects）、`上次通过`（Last OK）和 `备注`（Notes），其中 `状态` 为 `运作中`（Working）、`不稳定`（Unstable）、`未检查`（Not checked）、`失败中`（Failing）或 `已暂停`（Paused）之一。`仅显示有问题的配置档`（Only show profiles with problems）会隐藏正常工作的配置档。按钮如下：

- `使用这个配置档`（Use this profile）：让所选配置档保持使用，而不采用排名的选择。
- `切回自动`（Back to automatic）：让排名重新进行选择。
- `立即检查全部`（Check all now）：立即测量所有运行中的配置档。

限制：

- 自动选择器不能作为代理链中的一跳，也不能作为分组的 `前置代理`（Front Proxy）或 `落地代理`（Landing Proxy）。
- 它会跳过分组中的以下配置档：代理链和其他自动选择器、OpenVPN 和 OpenConnect、Tailscale、额外核心（Extra Core）、自定义 sing-box 完整配置，以及无法读取的自定义配置。当 Xray 完整配置无法与分组的前置代理或落地代理组合时，也会被跳过。

## Android 版 {#android}

Throne for Android 提供相同的测试和相同的自动选择器。

- 在 `配置`（Profiles）界面上，`⋮` 菜单为当前分组提供 `URL test`、`IP & country test`、`Speed test`、`Speed test current connection` 和 `Stop testing`。它还提供 `清理测试结果`（Clear test results）、`Remove`（`Duplicates`、`Unavailable`、`Invalid`、`Insecure configs`）和 `Sort`。对于选中的配置档，请使用选择菜单中的 `Test`。
- 在对多个配置档进行速度测试之前，应用会请求确认：“速度测试可能消耗大量流量。”
- 测试面板会显示进度、`Working`、`Failed`、`Pending` 和 `Skipped` 的计数、延迟图表（≤100 ms、≤300 ms、>300 ms、fail）、最快的配置档、各个国家以及不同出口 IP 的数量。它还提供一些操作，例如 `Sort by latency` 或 `Sort by speed`、`Remove unavailable`（附带失败配置档的数量）、`Connect to fastest`（未连接时为 `Select fastest`）以及 `Dismiss test results`。
- 连接后，点按统计栏（“已连接 , 点击此处测试连接”）即可测试当前连接。结果类似于“连接成功: HTTP 握手耗时 120ms”或“失败: …”。
- 要创建自动选择器，请选择 `添加服务器配置`（Add profile）→ `手动输入`（Manual settings）→ `Auto selector`。选项和默认值与桌面版相同，只是名称采用句首大写的写法，例如 `Servers from`、`Only names matching` 和 `Run the best`。在 `配置`（Profiles）界面上点击自动选择器的状态行，即可打开 `Auto selector stats`，其中有 `Use this profile`、`Back to automatic` 和 `Check all now`。
