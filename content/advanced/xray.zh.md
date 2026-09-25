+++
title = "sing-box 与 Xray"
description = "哪个核心运行你的配置档、Xray VLESS 首选项如何起作用，以及如何修复较新 Xray 服务器导致的 Reality 错误。"
weight = 10
toc = true
+++

Throne 的核心基于 sing-box 构建，其中也包含 Xray。大多数配置档运行在 sing-box 上，部分 VLESS 配置档和所有 Xray 自定义配置运行在 Xray 上。本页说明 Throne 如何选择核心、如何针对 VLESS 链接更改这一选择，以及如何修复 Reality 连接错误。

## 合二为一的两个核心 {#two-cores}

sing-box 始终在运行，负责本地代理端口、TUN 模式、路由规则和 DNS。Xray 作为辅助组件运行在同一个核心中，只有当正在运行的配置档需要它时才会启动，例如该配置档本身、其代理链中的某个跳点或某条路由规则的出站运行在 Xray 上时。sing-box 通过内部的本地连接把这部分流量交给 Xray，因此 TUN 模式、路由配置档和 DNS 设置在两个核心下的效果相同。

以下配置档运行在 Xray 上：

| `类型`（Type）列 | 来源 |
| --- | --- |
| `VLESS (Xray)` | `vless://` 链接（取决于 [Xray VLESS 首选项](#vless-preference)）；Xray JSON 中的 VLESS 出站；配置档编辑器中的 `VLESS (Xray)` 类型。 |
| `Custom Xray … Outbound` | `自定义 (Xray 出站)`（Custom (Xray outbound)）类型；导入的 Xray JSON 中的其他出站。 |
| `Custom Xray Config` | `自定义 (Xray 配置)`（Custom (Xray config)）类型；导入的完整 Xray 配置列表。 |

其他所有配置档（包括 `VLESS`）都运行在 sing-box 上。

有些 VLESS 功能只有 Xray 支持。使用了其中任一功能的 `vless://` 链接总会被导入为 `VLESS (Xray)`，无论首选项如何设置：

- XHTTP 传输（`type=xhttp`）及其 `extra` 设置；
- VLESS 加密（`encryption` 的值不是 `none`）；
- Finalmask；
- 带 HTTP 头部并同时启用 TLS 的 TCP（`raw`）传输。

Xray 的消息同样显示在 `日志`（Logs）标签页中。其详细程度在 `设置`（Settings）→ `基本设置`（Basic Settings）→ `日志`（Logging）→ `Xray 日志级别`（Xray Log level）中设置。

## 为 VLESS 链接选择核心 {#vless-preference}

`设置` → `基本设置` → `核心`（Core）→ `Xray VLESS 首选项`（Xray VLESS Preference）决定导入 `vless://` 链接时使用哪个核心：

| 选项 | 导入为 `VLESS (Xray)` 的链接 |
| --- | --- |
| `XHTTP Only` | 仅限需要 Xray 独有功能的链接（见上方列表）。Reality 链接仍使用 sing-box。 |
| `XHTTP And Reality`（默认） | 上述链接，外加所有 Reality 链接。 |
| `All VLESS` | 所有 `vless://` 链接。 |

其余 `vless://` 链接都会成为运行在 sing-box 上的 `VLESS` 配置档。

该首选项只对 `vless://` 链接生效：

- **Clash / Mihomo YAML：** VLESS 条目只有在使用 XHTTP 或 VLESS 加密时才会使用 Xray。Reality 条目仍使用 sing-box。
- **Xray JSON：** 每个 VLESS 出站都会成为 `VLESS (Xray)`。
- **sing-box JSON：** VLESS 出站仍使用 sing-box。
- **配置档编辑器：** 由你自己在 `类型` 列表中选择 `VLESS` 或 `VLESS (Xray)`。

{% alert_info() %}
`XHTTP And Reality` 从 1.2.0 起成为默认值，`All VLESS` 也是在该版本加入的。更新 Throne 会保留你已保存的值。如果你从 1.2.0 之前就开始使用 Throne，你的设置可能仍是 `XHTTP Only`。
{% end %}

### 更改首选项之后 {#after-change}

该首选项只影响更改之后导入的配置档，已有的配置档保持原来的核心。要把它们换到另一个核心：

- **订阅分组：** 更新订阅（`分组`（Groups）→ `更新订阅`（Update subscription），或右键点击分组标签页 → `更新订阅`）。Throne 会用另一种类型的新配置档替换受影响的配置档，因此它们原有的测试结果会丢失。
- **从链接添加的配置档：** 重新添加该链接，然后删除旧配置档。
- **手动创建的配置档：** 其类型无法更改。请用另一种类型新建一个配置档。

如果在分组的 `Advanced` 订阅设置中开启了 `Keep working profiles`，旧的可用配置档可能会与新配置档并存。请自行删除它们。

### 配置档使用的是哪个核心？ {#which-core}

查看配置档列表中的 `类型` 列。`VLESS` 运行在 sing-box 上；`VLESS (Xray)`、`Custom Xray … Outbound` 和 `Custom Xray Config` 运行在 Xray 上。

如果想在该列中同时看到安全层（例如 Reality），请开启 `设置` → `基本设置` → `样式`（Style）→ `显示配置安全信息`（Show Config Security）。对于 `VLESS (Xray)` 和 `自定义 (Xray 出站)` 配置档以及代理链，右键菜单中还有 `分享`（Share）→ `导出 Xray 配置`（Export Xray config）。

## 较新 Xray 服务器的 Reality 错误 {#reality}

较新的 Xray 服务器会拒绝 sing-box 的 Reality 客户端。此时配置档无法连接，日志中显示 `reality verification failed`（[#1780](https://github.com/throneproj/Throne/issues/1780)）。

- Xray 26.7.11 至 26.7.28 只接受报告较新 Xray 版本的客户端。
- Xray 26.9.9 及更新版本要求使用较新的密钥交换（X25519MLKEM768），而 sing-box 的 Reality 客户端不提供这种密钥交换。

解决方法是让该配置档运行在 Xray 上：

1. 打开 `设置` → `基本设置` → `核心`。
2. 将 `Xray VLESS 首选项` 设为 `XHTTP And Reality` 或 `All VLESS`。
3. 点击 `确定`（OK）。
4. 更新订阅，或重新添加链接（见[更改首选项之后](#after-change)）。
5. 确认 `类型` 列现在显示为 `VLESS (Xray)`。

对于来自 Clash / Mihomo YAML 订阅的 Reality 条目，这种方法无效，因为它们始终使用 sing-box。如果你的服务商也以链接列表的形式提供订阅，请改用该格式。

如果你自己运行的是 26.7.11 至 26.7.28 版本的 Xray 服务器，也可以在其 VLESS 入站的 `realitySettings` 中添加 `"minClientVer": "0.0.0"`，以允许较旧的客户端连接。此方法对 Xray 26.9.9 及更新版本无效。

## 代理链中的 Xray {#xray-in-chains}

代理链可以混用 sing-box 和 Xray 配置档，但有两项限制：

- 所有 Xray 跳点必须相邻。流量只能从 sing-box 切换到 Xray 再切换回来一次：先是 sing-box 跳点，然后是 Xray 跳点，最后是 sing-box 跳点。否则配置档无法启动，日志中显示“Too many core transitions”（核心切换次数过多）。
- `自定义 (Xray 配置)` 配置档必须是最上面的跳点，并且不能与其他 Xray 跳点位于同一条代理链中，因为一条代理链只能使用一个 Xray 实例。

分组的前置代理和落地代理以及 WARP 也算作跳点。参见[代理链与自定义配置](@/advanced/chains.zh.md#chains)。

## Xray geo 文件 {#geo-files}

`自定义 (Xray 配置)` 配置档可以带有自己的 `routing` 规则，并在其中使用 `geoip:` 或 `geosite:` 值。为此，Xray 需要 `geoip.dat` 和 `geosite.dat` 这两个文件。其他配置档以及 Throne 的路由配置档不使用这些文件，而是使用规则集。

缺少这些文件时，Throne 会显示“需要 Geo 资源文件”（Geo asset files required）并提供下载。点击 `是`（Yes），等待出现“Geo 资源已安装”（Geo assets installed），然后重新启动该配置档。

下载地址位于 `设置` → `基本设置` → `杂项`（Miscellaneous）→ `Xray Geo 资源`（Xray Geo Assets）中的 `GeoIP 资源 URL`（GeoIP Asset URL）和 `GeoSite 资源的 URL`（GeoSite Asset URL）字段。它们的列表提供四个来源的地址：Loyalsoldier（全球和中国，默认）、Chocolate4U（伊朗）、runetfreedom（俄罗斯）和 v2fly。两个文件请从同一来源获取。每个 `下载`（Download）按钮都会重新下载对应的文件并替换旧文件。

如果某条规则引用了文件中不存在的类别，Throne 会显示“Geo 资源缺失类别”（Geo asset missing category）。请选择包含该类别的来源，然后点击该文件对应的 `下载`。

## Android 版 {#android}

- 同样的设置位于 `设置`（Settings）→ `Core` → `Xray VLESS preference`，选项为 `XHTTP only`、`XHTTP and Reality`（默认）和 `All VLESS`。它同样只在导入时生效，因此更改后请更新订阅。
- 配置档类型同样为 `VLESS` 和 `VLESS (Xray)`，代理链中使用 Xray 的限制也相同。
