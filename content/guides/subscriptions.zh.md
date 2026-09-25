+++
title = "订阅与分组"
description = "添加和更新订阅，设置分组选项、User-Agent 和 HWID、前置代理与落地代理，并解决更新问题。"
weight = 10
toc = true
+++

订阅是服务商提供的一个链接，它会返回一份服务器列表。Throne 把每个订阅放在单独的分组中，并可以替你更新它。本页介绍如何添加和更新订阅、分组有哪些选项，以及更新失败时该怎么办。

## 分组与订阅 {#groups}

配置档列表上方的每个标签页都是一个分组。分组属于以下两种类型之一：

- **基本（Basic）。** 存放你自己添加的配置档，例如来自链接、文件、二维码或 `程序`（Program）→ `新建配置档`（New profile）的配置档。
- **订阅（Subscription）。** 另外带有一个 `URL`。Throne 从该地址下载配置档列表，并让分组与之保持一致。

类型在创建分组时选择，之后无法更改。

{% alert_info() %}
更新会让订阅分组与服务商的列表保持一致。它会删除不在列表中的配置档，并撤销你对其他配置档所做的修改。请把你自己的配置档放在基本分组中。
{% end %}

## 添加订阅 {#add-subscription}

### 从剪贴板添加 {#from-clipboard}

1. 复制订阅地址。它以 `https://` 或 `http://` 开头。
2. 在 Throne 中按 `Ctrl+V`，或选择 `程序`（Program）→ `添加剪贴板中的配置档`（Add profile from clipboard）。
3. Throne 会显示该地址并询问“如何更新？”。选择 `创建新的订阅分组`（Create new subscription group），然后点击 `确定`（OK）。

Throne 会创建一个以地址中的主机名命名的分组，并立即下载其中的配置档。当地址来自文件、二维码或你拖放到窗口上的文本时，也会出现同样的询问。三个选项的作用如下：

| 选项 | 结果 |
| --- | --- |
| `添加配置档到这个分组`（Add profiles to this group） | 下载一次列表，并把配置档添加到当前分组。Throne 不会保存该地址，因此这些配置档永远不会更新。 |
| `创建新的订阅分组` | 创建一个订阅分组并下载它。 |
| `导入 HTTP 代理配置档`（Import HTTP proxy profile） | 把该地址当作一台 HTTP 代理服务器，并将其添加为一个配置档。 |

### 自行创建分组 {#create-group}

1. 选择 `分组`（Groups）→ `添加新分组`（Add new Group）。
2. 输入 `名称`（Name）。
3. 将 `类型`（Type）设为 `订阅`（Subscription）。
4. 把地址粘贴到 `URL` 中。
5. 点击 `确定`（OK）。
6. 右键点击新的标签页，选择 `更新订阅`（Update subscription）。

创建分组并不会下载它。在第 6 步首次更新之前，分组一直是空的。

`分组`（Groups）→ `管理分组`（Manage Groups）会打开一个列出所有分组的窗口。你也可以在那里用 `新建分组`（New group）创建分组。每一行显示类型、配置档数量、地址和上次更新的时间。如果服务商发送了配额信息（`Subscription-UserInfo` 响应头），该行还会显示 `已用`（Used）、`剩余`（Remain）和 `过期`（Expire）。每一行都有 `编辑`（Edit）和 `删除`（Remove）按钮，订阅分组的行还有 `更新订阅`（Update Subscription）按钮。

### 通过 throne:// 链接添加 {#from-link}

`throne://addsub/…` 链接（例如服务商网站上的链接）会打开 `添加订阅`（Add subscription）窗口，并填好名称和地址。如果该分组应参与自动更新，请保持勾选 `自动更新`（Auto update），然后点击 `确定`（OK）。Throne 随后会创建该分组并下载它。参见[深度链接](@/advanced/deeplinks.zh.md#addsub)。

## 更新订阅 {#update}

要更新单个分组，可以使用以下任一方式：

- 右键点击该分组的标签页，选择 `更新订阅`（Update subscription）。
- 选中该标签页后按 `Ctrl+U`，或选择 `分组`（Groups）→ `更新订阅`（Update subscription）。
- 在 `分组`（Groups）→ `管理分组`（Manage Groups）中，点击该分组旁边的 `更新订阅`（Update Subscription）。

`分组`（Groups）→ `更新所有订阅`（Update all subscriptions）会更新每一个订阅分组，包括设置了 `跳过自动更新`（Skip automatic update）的分组。

更新期间，Throne 会：

- 下载列表，并与分组中的配置档进行比较。没有变化的配置档保留其测试结果。有变化的配置档会被更新。新的配置档会被添加，不再出现在列表中的配置档会被删除。
- 按服务商列表的顺序排列配置档。
- 如果响应中完全没有配置档，则不做任何更改。此时日志会显示“No profiles found in the subscription: *group* was left unchanged.”（订阅中未找到配置档：*分组* 保持不变）。这可以防止空响应或被封锁的响应破坏你的分组。
- 如果服务器 10 秒内没有发送任何数据，或者响应大于 64 MB，则放弃更新。

开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `订阅`（Subscription）→ `更新订阅前清除服务器`（Clear servers before updating subscription）后（默认关闭），Throne 会在每次更新前删除该分组的配置档，因此它们的测试结果会丢失。

### 变更报告 {#change-report}

每次更新都会向 `日志`（Logs）标签页写入一份报告。报告的开头是 `「分组名称」的变化`（`Change of` 加分组名称）。每一行以 `[+]`（新增）、`[~]`（更新）、`[-]`（删除）或 `[=]`（保留）开头。如果没有任何变化，报告会显示 `无`（Nothing）。

手动更新单个分组后，Throne 还会在一个窗口中显示该报告。要关闭这个窗口，请取消勾选 `设置`（Settings）→ `基本设置`（Basic Settings）→ `订阅`（Subscription）→ `订阅手动更新后显示变化窗口`（Show the changes window after a manual subscription update）。自动更新和 `更新所有订阅`（Update all subscriptions）只会写入日志。

### 正在使用的配置档 {#running-profile}

更新不会停止或删除你当前连接的配置档。如果服务商移除了它，Throne 会保留它，并在报告中把它列在“仍在使用中，因此保留而不是删除”之下。如果你希望 Throne 改为停止并删除这类配置档，请开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `订阅`（Subscription）→ `允许停止活动配置档`（Allow stopping the active profile）。

如果服务商更改了正在运行的配置档的设置，Throne 会保存新设置，但连接仍使用旧设置。请重新启动该配置档以使用新设置。当更新替换了正在运行的[自动选择器](@/guides/testing.zh.md#auto-selector)所使用的配置档时，该自动选择器会自行重启。

## 自动更新 {#auto-update}

自动更新默认关闭。要开启它：

1. 打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `订阅`（Subscription）。
2. 在 `订阅自动更新`（Subscription auto update）旁边勾选 `启用`（Enable）。
3. 设置 `时间间隔 (分钟，少于 30 则无效)`（Interval (minute, invalid if less than 30)）。默认值为 30。
4. 点击 `确定`（OK）。

自动更新的工作方式：

- 所有分组共用一个时间间隔。每当该间隔过去，Throne 就会更新所有订阅分组，设置了 `跳过自动更新`（Skip automatic update）的分组除外。
- 小于 30 分钟的间隔视为关闭。
- Throne 每分钟检查一次，并在启动 10 秒后检查一次。在 Throne 关闭期间到期的更新，会在你打开它后不久运行。
- `运行时统计`（Runtime Stats）标签页中的 `下次订阅更新`（Next sub update）显示剩余时间。
- 每次自动更新时，日志都会显示 `自动更新： 正在运行 订阅`（Auto-update: running subscriptions）。自动更新从不打开变化窗口。

## 分组选项 {#group-options}

要更改分组，请右键点击其标签页并选择 `编辑选定分组`（Edit selected Group），或选择 `分组`（Groups）→ `编辑当前分组`（Edit current Group）。

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `名称`（Name） | – | 标签页上显示的名称。 |
| `类型`（Type） | `基本`（Basic） | `基本` 或 `订阅`。分组创建后无法更改。 |
| `前置代理`（Front Proxy） | `None` | 该分组的每个配置档都会先经由此配置档连接。参见[前置代理与落地代理](#front-landing-proxy)。 |
| `落地代理`（Landing Proxy） | `None` | 流量经过该分组的配置档之后，再从此配置档离开。 |
| `自动清除不可用配置档`（Auto Clear Unavailable Profiles） | 关闭 | 对该分组的配置档进行 URL 测试后，不经询问直接删除测试失败的配置档。 |
| `URL` | – | 订阅地址。仅用于订阅分组。 |
| `跳过自动更新`（Skip automatic update） | 关闭 | 让该分组不参与自动更新。手动更新仍然有效。 |
| `Advanced` | – | 打开 `Advanced Subscription Settings` 窗口（自 1.3.1 起）。参见[每次更新之后](#after-update)和 [User-Agent 与 HWID](#user-agent-and-hwid)。 |

如果分组中有配置档，该窗口还会显示 `复制配置档分享链接`（Copy profile share links）和 `复制配置档分享链接(深度链接)`（Copy profile share links (Deep Links)）。它们会复制分组中所有配置档的链接。

## 每次更新之后 {#after-update}

自 1.3.1 起，订阅分组可以在每次更新后自行清理。打开分组选项，点击 `Advanced`，然后使用 `Update` 部分。所有选项默认关闭。

| 设置 | 作用 |
| --- | --- |
| `Keep working profiles` | 当订阅不再列出上次测试成功的配置档时，仍保留这些配置档。 |
| `Remove duplicate profiles` | 删除与另一个配置档完全相同的配置档。 |
| `Remove insecure profiles` | 删除流量没有得到妥善保护的配置档，效果与 `分组`（Groups）→ `移除不安全的配置`（Remove Insecure Configs）相同。 |
| `Remove invalid profiles` | 删除被核心拒绝的配置档。核心无法连接时跳过。 |
| `Run URL test` | 更新完成后测试该分组的配置档；如果已有测试正在进行，则在其结束后再测试。 |
| `Remove unavailable profiles` | 需要开启 `Run URL test`。删除测试失败的配置档。 |
| `Sort by latency` | 需要开启 `Run URL test`。对分组排序，最快的排在最前。 |

变更报告会列出这些选项删除的每一个配置档。它们不会删除你当前连接的配置档，除非开启了 `允许停止活动配置档`（Allow stopping the active profile）。

## User-Agent 与 HWID {#user-agent-and-hwid}

Throne 下载订阅时，会发送一个标明应用名称的 `User-Agent` 请求头。有些服务商会为不同的应用发送不同的列表，或者拒绝它们不认识的应用。你可以更改这个值：

- 对所有分组：`设置`（Settings）→ `基本设置`（Basic Settings）→ `订阅`（Subscription）→ `User Agent (用户代理)标识`。如果留空，Throne 会发送 `Throne/` 加上其版本号，例如 `Throne/1.3.1`。
- 对单个分组（自 1.3.1 起）：分组选项 → `Advanced` → `Request` → `User Agent`。如果留空，该分组使用全局值。

有些服务商还要求提供设备 ID（HWID）。只有在你开启后，Throne 才会发送它：

- 对所有分组：在 `订阅`（Subscription）标签页上勾选 `启用在更新订阅时发送硬件ID、设备型号以及 OS 版本`（Enable sending HWID, device model, and OS version when updating subscription）。它默认关闭。将鼠标悬停在该选项上，可以查看 Throne 将会发送的值。
- 对单个分组：将 `Send HWID` 设为 `Keep Default`（遵循全局设置）、`On` 或 `Off`。`HWID`、`OS`、`OS Version` 和 `Device Model` 字段会为该分组覆盖对应的值。只有当该分组开启了 HWID 发送时，你才能编辑这些字段。

要为所有分组发送其他值，请在 `订阅`（Subscription）标签页上填写 `自定义系统参数(可选)`（Custom System Parameters (optional)）。使用以下格式，并省略你不想更改的值：

```text
hwid=value,os=value,osVersion=value,model=value
```

Throne 会在 `x-hwid`、`x-device-os`、`x-ver-os` 和 `x-device-model` 请求头中发送这些值。关于它们包含的内容，请参见[隐私与网络请求](@/reference/privacy.zh.md#hwid)。

## 前置代理与落地代理 {#front-landing-proxy}

分组可以让其所有配置档的流量再经过两个额外的配置档：

**你的设备 → `前置代理` → 本分组中的某个配置档 → `落地代理` → WARP（如已启用）→ 互联网**

- 当你的设备无法直接连接该分组的服务器时，使用 `前置代理`（Front Proxy）。
- 当你希望网站看到的是落地代理的地址，而不是该分组服务器的地址时，使用 `落地代理`（Landing Proxy）。

你可以从任意分组中选择任意已保存的配置档；在字段中输入文字即可搜索。自动选择器不在可选之列，因为它们会自行更换服务器。关于代理链以及混用不同核心的规则，请参见[代理链与自定义配置](@/advanced/chains.zh.md#front-landing)。

## 支持的格式 {#formats}

订阅可以返回：

- 分享链接，例如 `vless://`、`vmess://`、`trojan://`、`ss://`、`hysteria2://` 或 `tuic://`，每行一个，可以是纯文本，也可以经过 Base64 编码。
- 带有 `proxies:` 列表的 Clash 或 Mihomo YAML。
- sing-box JSON：完整配置或出站列表。每个受支持的出站都会成为一个配置档。单个出站对象会成为一个自定义出站配置档。
- Xray JSON。配置中的出站会成为配置档。由多个完整 Xray 配置组成的列表，会为每个配置生成一个 `Custom Xray Config` 配置档。
- SIP008（Shadowsocks JSON）、WireGuard 和 AmneziaWG 的 `.conf` 文件、OpenVPN 的 `.ovpn` 文件、AnyConnect XML 配置文件，以及 AmneziaVPN 的 `vpn://` 链接。

`vless://` 链接会成为 sing-box 配置档还是 Xray 配置档，取决于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `核心`（Core）→ `Xray VLESS 首选项`（Xray VLESS Preference）。Throne 在导入时应用这一设置，因此更改它之后，请重新更新你的订阅。参见 [sing-box 与 Xray](@/advanced/xray.zh.md#vless-preference)。完整的格式列表见[协议与导入格式](@/reference/protocols.zh.md#import-formats)。

## 问题排查 {#problems}

请先打开 `日志`（Logs）标签页。每次更新都会写入以 `>>>>>>>>` 和 `<<<<<<<<` 开头的行，如果出错，其中也包含错误信息。

### 服务商拒绝 Throne 或不发送配置档 {#problem-user-agent}

有些服务商只响应它们认识的应用。此时日志会显示诸如状态码 403 之类的错误，或者“No profiles found in the subscription”（订阅中未找到配置档）。请将该分组的 `User Agent`（分组选项 → `Advanced`）设为你的服务商所要求的值。用户曾经需要用到的值包括 `ClashMeta`、`sing-box` 和 `Happ/1.0`。

### 服务商要求提供设备 ID {#problem-hwid}

如果服务商要求提供设备 ID 或设备指纹，请开启 HWID 发送：为该分组将 `Send HWID` 设为 `On`，或者在 `订阅`（Subscription）标签页上为所有分组开启。

### “有用代理的请求，但未启动配置档。” {#problem-no-profile}

当 `设置`（Settings）→ `基本设置`（Basic Settings）→ `杂项`（Miscellaneous）→ `使用代理`（Use proxy）开启时，Throne 会通过本地代理端口发送它自己的请求，例如订阅更新。只要勾选了 `系统代理`（System Proxy），它也会这样做。如果没有配置档在运行，就没有可用的代理，请求便会失败并显示此消息。请先启动一个配置档，或者关闭 `使用代理`（Use proxy）和 `系统代理`（System Proxy）。

### 订阅地址在你所在的国家被封锁 {#problem-blocked}

1. 启动一个可用的配置档。
2. 开启 `设置`（Settings）→ `基本设置`（Basic Settings）→ `杂项`（Miscellaneous）→ `使用代理`（Use proxy）。
3. 更新订阅。

`使用代理`（Use proxy）需要本地代理端口，因此在开启 `禁用混合入站`（Disable Mixed Inbound）时无法使用。

### Happ 和 v2RayTun 的“crypt”链接 {#problem-crypt}

以 `happ://crypt` 或 `v2raytun://crypt` 开头的链接是专为这些应用加密的，Throne 无法读取。诸如 `…/dl/happ-link/…` 之类的网页也不是订阅。请向你的服务商索要以 `https://` 开头的普通订阅地址。

### 配置档显示为 `Custom Xray Config` {#problem-custom-config}

如果订阅返回的是由多个完整 Xray 配置组成的列表，Throne 会把每个配置导入为一个类型为 `Custom Xray Config` 的配置档（在配置档编辑器中称为 `自定义 (Xray 配置)`（Custom (Xray config)））。它会移除每个配置中的 `inbounds`，其余部分按原样运行。这是有意为之：这类配置可能包含只有作为整体才能工作的负载均衡器和代理链。相比之下，sing-box 配置会被拆分，每个出站成为一个配置档。

更多帮助请参见[故障排除](@/help/troubleshooting.zh.md#subscriptions)。

## Android 版 {#android}

Throne for Android 具有相同的分组、选项和更新行为。

- 从侧边菜单打开 `分组`（Groups）。使用顶部的 `New group` 和 `更新所有订阅`（Update all subscriptions）。每个分组都会显示其类型、配置档数量、上次更新时间，以及服务商发送的配额信息（“Used … · … left · expires …”，即已用、剩余和到期时间）。
- 分组编辑器具有相同的选项，只是名称采用句首大写的写法：`Front proxy`、`Landing proxy`、`Auto clear unavailable profiles`、`Skip automatic update` 和 `Advanced`。
- `URL` 也接受 `content://` 地址，因此订阅可以来自另一个应用提供的文件。对于普通的 `http://` 地址，编辑器会警告“纯文本 HTTP 流量并不安全”。
- 全局选项位于 `设置`（Settings）→ `订阅`（Subscriptions）。如果 `User agent` 为空，应用会发送 `Throne/Android/` 加上其版本号。
- 通过 `添加服务器配置`（Add profile）→ `从剪切板导入`（Import from clipboard）导入地址时，会出现同样的“How to update?”（如何更新？）询问。
- 只有手动更新单个分组后才会出现变化窗口。自动更新只会写入日志。

Android 特有的问题请参见 [Android 故障排除](@/android/troubleshooting.zh.md#subscriptions)。
