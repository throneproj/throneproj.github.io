+++
title = "深度链接"
description = "在桌面版和 Android 上使用 throne:// 链接，一键添加订阅、路由配置档和代理配置档。"
weight = 70
toc = true
+++

深度链接是一种 `throne://` URL，用来让 Throne 完成一项操作：添加订阅、导入路由配置档、添加远程路由配置档，或添加一个代理配置档。服务商会把深度链接放在网站上或二维码中。你也可以用它来分享自己的路由配置档。

## Throne 如何接收深度链接 {#receive}

你的系统必须知道由 Throne 打开 `throne://` 链接。Throne 只为你当前的用户账户注册自己，因此不需要管理员权限。

| 系统 | 是否默认注册 |
| --- | --- |
| Linux | 是 |
| macOS | 是（从 `Throne.app` 运行 Throne 时） |
| Windows，通过安装程序安装 | 是 |
| Windows，从 ZIP 文件解压 | 否 |

要开启注册（例如对于从 ZIP 解压的 Windows 副本）：

1. 打开 `设置`（Settings）→ `基本设置`（Basic Settings）。
2. 在 `通用`（Common）标签页的 `链接和文件`（Links and Files）下，勾选 `启动时注册 throne:// 链接`（Register throne:// links at startup）。
3. 点击 `确定`（OK）。Throne 会立即完成注册。

开启此选项后，Throne 每次启动时都会检查注册，并在需要时修复，例如在你移动 Throne 文件夹之后。如果你在 Windows 或 Linux 上保留了多个副本，链接会在最后一个开启此选项并启动的副本中打开。

当链接会在当前这份 Throne 中打开时，选项旁边的状态显示为 `已安装`（Installed）。`安装`（Install）按钮只注册一次，不会开启该选项。`卸载`（Uninstall）会移除注册并关闭该选项。仅取消勾选该选项则会保留现有的注册。

**macOS：** 链接处理程序是 `Throne.app` 的一部分，因此没有 `安装` 和 `卸载` 按钮。如果 Throne 不是从应用包中运行的，该选项会显示 `不可用于这个安装`（Not available for this installation）。

Throne 可以通过以下方式接收深度链接：

- 在浏览器、聊天应用或文档中**点击链接**。如果 Throne 没有运行，它会先启动，然后处理该链接。
- **复制链接**，然后在主窗口中按 `Ctrl+V`，对应菜单 `程序`（Program）→ `添加剪贴板中的配置档`（Add profile from clipboard）。即使没有开启注册，此方法也有效。
- 将**链接文本拖放**到主窗口上。
- 启动 Throne 时**将链接作为参数传入**。参见[命令行](@/reference/files.zh.md#command-line)。

{% alert_info() %}
在桌面版上，`扫描二维码`（Scan QR Code）和拖放的二维码图片只会导入 `add` 链接。如果二维码中是其他深度链接，请从 `日志`（Logs）标签页复制 `QR Code Result:` 之后的文本，然后按 `Ctrl+V`。
{% end %}

## 链接格式 {#format}

所有深度链接的形式都相同：

```text
throne://<command>/<payload>
```

- `throne://` 必须小写。命令不区分大小写：`throne://AddSub/…` 也有效。
- 命令后面必须跟一个斜杠和载荷（payload）。缺少斜杠时，大多数链接不会产生任何效果。
- Throne 会忽略链接中 `?` 或 `#` 之后的所有内容。链接携带的全部信息都在载荷中。
- 如果载荷经过了百分号编码（例如用 `%2B` 代替 `+`），Throne 会先对其解码。

| 命令 | 作用 | 是否先询问？ |
| --- | --- | --- |
| `addsub` | 添加一个订阅分组并更新它 | 是 |
| `route` | 导入链接中携带的路由配置档 | 是 |
| `remoteroute` | 按 URL 添加远程路由配置档 | 是 |
| `add` | 向当前分组添加一个代理配置档 | 否。在 Android 上，在其他应用中点按该链接时会询问。 |

### Base64 规则 {#base64}

载荷是 Base64 文本。可以使用哪种 Base64 字母表取决于命令：

| 命令 | 接受的载荷 |
| --- | --- |
| `addsub`、`remoteroute` | 仅限标准 Base64：字母、数字、`+` 和 `/`。末尾的 `=` 填充可有可无。 |
| `route`、`add` | URL 安全的 Base64（`-` 和 `_`）或标准 Base64，带不带填充均可。Throne 自己生成的是不带填充的 URL 安全 Base64。 |

对于 `addsub` 和 `remoteroute`，包含 `-` 或 `_` 的 URL 安全载荷会失败。请让载荷保持在一行内，不要包含空格。

在 Linux 或 Windows 的 Git Bash 中编码载荷：

```bash
printf '%s' 'https://example.com/sub/abc123#MyProvider' | base64 -w 0
```

在 macOS 上，请去掉 `-w 0`。在 PowerShell 中：

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('https://example.com/sub/abc123#MyProvider'))
```

这两条命令输出的都是带填充的标准 Base64。

## `addsub`：添加订阅 {#addsub}

添加一个新的订阅分组，并立即更新它。

```text
throne://addsub/<base64>
```

载荷是以下这一行文本的 Base64：

```text
<subscription_url>#<group_name>
```

| 部分 | 必需 | 说明 |
| --- | --- | --- |
| `<subscription_url>` | 是 | 订阅 URL，保持原样。其中的 `?`、`&` 和 `/` 在 Base64 中是安全的，因此无需进行百分号编码。 |
| `#<group_name>` | 否 | 新分组的名称。省略时，分组以 URL 的主机名命名。名称的百分号编码是可选的：直接使用空格也可以。 |

例如，要将 `https://example.com/sub/abc123` 添加为名为 `MyProvider` 的分组，请对 `https://example.com/sub/abc123#MyProvider` 进行编码：

```text
throne://addsub/aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWIvYWJjMTIzI015UHJvdmlkZXI=
```

Throne 会显示“添加这个订阅吗?”（Add this subscription?），其中包含分组名称和 URL，以及一个默认已勾选的 `自动更新`（Auto update）复选框。确认后，Throne 会创建该分组并更新它。

{% alert_info() %}
`自动更新` 只决定新分组是否参与自动更新：勾选时，分组设置中的 `跳过自动更新`（Skip automatic update）为关闭状态。自动更新还需要开启 `基本设置` → `订阅`（Subscription）→ `订阅自动更新`（Subscription auto update）→ `启用`（Enable），该选项默认关闭。参见[订阅与分组](@/guides/subscriptions.zh.md#auto-update)。
{% end %}

## `route`：导入路由配置档 {#route}

导入链接中携带的完整路由配置档（默认出站和规则）。

```text
throne://route/<base64>
```

你无需手动构造这类链接。在 `路由设置`（Routing Settings）的 `路由`（Route）标签页中选中该配置档并点击 `导出`（Export），或在列表中按 `Ctrl+C`。Throne 会把一条 `throne://route/…` 链接复制到剪贴板。

当有人打开该链接时，Throne 会显示“添加这个路由配置档吗?”（Add this routing profile?）及其名称，并附上无法导入内容的说明。对方确认后，该配置档会被添加到其列表中。如果该配置档包含 VPN 端点，Throne 会在询问之前先创建相应的 OpenVPN 或 OpenConnect 配置档，并且即使取消导入也会保留它们。导入的配置档不会自动启用：请在 `路由`（Routing）菜单底部的列表中选择它。

载荷是类似下面这样一个小型 JSON 对象的 Base64：

```json
{
  "kind": "throne-route-profile",
  "v": 1,
  "name": "Example",
  "default_outbound": "proxy",
  "rules": []
}
```

下面这条链接携带的就是该 JSON：

```text
throne://route/eyJraW5kIjoidGhyb25lLXJvdXRlLXByb2ZpbGUiLCJ2IjoxLCJuYW1lIjoiRXhhbXBsZSIsImRlZmF1bHRfb3V0Ym91bmQiOiJwcm94eSIsInJ1bGVzIjpbXX0
```

`default_outbound` 的值为 `proxy`、`direct`、`block` 或 `warp-bypass`。原始配置档（手写的 sing-box `route` 段落）带有 `"raw": true` 和一个 `route` 对象，而不是 `rules`。Throne 会按名称查找规则中使用的服务器，并告诉你哪些没有找到。关于分享的更多信息，请参见[路由](@/guides/routing.zh.md#share-profiles)。

### 在路由设置中导入 {#routing-settings-import}

你也可以在 `路由设置` 的 `路由` 标签页中粘贴链接：点击 `导入`（Import），或在列表中按 `Ctrl+V`。在主窗口中，只有以 `throne://` 开头的文本才会被视为深度链接；而在这里，Throne 还接受单独的 Base64 载荷、纯 JSON，以及旧式的 JSON 规则列表（它会在编辑器中打开，以便你为其命名）。通过 `route` 链接、其 Base64 或其 JSON 导入的配置档，在你点击 `确定` 后还会成为 `通用` 标签页中选中的 `路由配置档`（Routing Profile）。

在这里粘贴的 `remoteroute` 链接添加的配置档会关闭自动更新，因为这里的提示框没有 `自动更新` 复选框。你可以稍后在每个配置档的编辑器中勾选 `自动更新`。

## `remoteroute`：添加远程路由配置档 {#remoteroute}

添加一个或多个远程路由配置档。`route` 链接携带整个配置档，而 `remoteroute` 链接只携带 URL：Throne 会下载每个配置档，并可以使其保持最新。可用它来分发你自己维护的路由配置档。

```text
throne://remoteroute/<base64>
```

载荷是一份纯 URL 列表（每行一个）的 Base64，而不是 JSON：

```text
<profile_url_1>#<name_1>
<profile_url_2>#<name_2>
```

| 部分 | 必需 | 说明 |
| --- | --- | --- |
| `<profile_url>` | 是 | 一个 `http://` 或 `https://` URL。不以二者之一开头的行会被跳过。 |
| `#<name>` | 否 | 配置档名称。省略时，配置档以 URL 的主机名命名。 |

每个 URL 都必须提供一个结构化路由配置档：一条 `throne://route/` 链接、其 Base64 载荷，或其中的 JSON。原始配置档不能用作远程配置档。

例如，对下面两行进行编码：

```bash
printf '%s\n%s' 'https://example.com/routes/bypass-iran.json#BypassIran' 'https://example.com/routes/ads.json' | base64 -w 0
```

得到的链接如下：

```text
throne://remoteroute/aHR0cHM6Ly9leGFtcGxlLmNvbS9yb3V0ZXMvYnlwYXNzLWlyYW4uanNvbiNCeXBhc3NJcmFuCmh0dHBzOi8vZXhhbXBsZS5jb20vcm91dGVzL2Fkcy5qc29u
```

Throne 会在“添加这些远程路由配置档吗?”（Add these remote routing profiles?）下列出这些 URL，并为它们提供一个共用的 `自动更新` 复选框，该复选框默认已勾选。确认后，Throne 会添加并下载这些配置档，日志中会显示成功获取了多少个。

- 只有勾选了 `基本设置` → `订阅` → `路由配置档自动更新`（Routing profiles auto update）→ `启用` 时，Throne 才会刷新开启了 `自动更新` 的配置档。该选项默认关闭。要手动更新，请使用 `路由设置` 中 `路由` 标签页上的 `更新`（Update）。参见[远程配置档](@/guides/routing.zh.md#remote-profiles)。
- 更新会用下载到的规则和默认出站替换配置档原有的内容，配置档名称保持不变。
- 位于 `raw.githubusercontent.com` 上的 URL 会通过 `路由设置` 的 `通用` 标签页中选择的 `远程规则集镜像`（Remote Rule-set Mirror）下载（默认为 jsDelivr 镜像）。在你修改文件后的一段时间内，镜像可能仍提供旧版本。
- `路由` → `下载配置档`（Download Profiles）的工作方式相同：它会从 Throne 的路由配置档仓库下载一条 `remoteroute` 链接，并显示同样的提示。

## `add`：添加一个代理配置档 {#add}

向当前分组添加一个代理配置档。

```text
throne://add/<base64>
```

载荷是该配置档出站设置（JSON 格式）的 Base64。在桌面版上，这种链接不会请求确认：配置档会被立即添加，就像你粘贴了一条 `vless://` 或 `ss://` 链接一样。

Throne 可以为你生成这类链接：

- 在列表中右键点击配置档 → `分享`（Share）→ `复制选定项的链接 (深度链接)`（Copy links of selected (Deep Links)），快捷键 `Ctrl+Alt+C`。
- 右键点击配置档 → `分享` → `二维码和链接`（QR Code and link）。窗口中显示普通分享链接或深度链接，勾选 `Deep Link` 即可在两者之间切换。
- `分组`（Groups）→ `编辑当前分组`（Edit current Group）→ `复制配置档分享链接(深度链接)`（Copy profile share links (Deep Links)）。

深度链接携带完整的配置档设置，因此也适用于没有标准分享链接的配置档类型和选项。对于这类配置档，`复制选定项的链接`（Copy links of selected，`Ctrl+C`）通常会自动复制深度链接，二维码窗口打开时也会勾选 `Deep Link`。如果这类配置档设置了高级连接选项（例如绑定网络接口），请改用 `复制选定项的链接 (深度链接)`。

凡是普通分享链接可用的地方，`add` 链接也同样可用：订阅中、文件中以及二维码中。

## Android 版 {#android}

Throne for Android 2.0.0 支持同样的四个命令。它还接受 `clash://install-config?url=…&name=…` 链接，这类链接会像 `addsub` 一样添加订阅。在这类链接中，`url` 的值需要进行百分号编码。`throne://` 协议在安装应用时即完成注册，没有相关设置项。

在其他应用中点按链接，或在 `配置`（Profiles）界面使用 `添加服务器配置`（Add profile）→ `从剪切板导入`（Import from clipboard）或 `扫描二维码`（Scan QR code）。在 Android 上，二维码适用于全部四个命令。`route` 和 `remoteroute` 链接也可以通过 `路由`（Routing）界面上的 `Import` 导入。

与桌面版的区别：

- 在其他应用中点按 `add` 链接时，会先询问“确认要导入配置 …？”（Confirm you want to import profile …?）。在其他应用中点按 `vless://` 等链接时也会同样询问。通过剪贴板或二维码导入时则不会询问。
- 导入的路由配置档会被添加，但不会自动启用。请在 `路由` 界面点按它以使用。
- 来自桌面版的原始路由配置档（`"raw": true`）会被拒绝，并提示“raw routing profiles are not supported on Android”（Android 不支持原始路由配置档）。分享的路由配置档中的端点会被丢弃，并附带说明。
- 未知命令会在屏幕上显示“Ignored deeplink with unknown command: …”（已忽略带有未知命令的深度链接），而不仅仅记录在日志中。
- 定时更新需要开启相应设置：订阅对应 `设置`（Settings）→ `订阅`（Subscriptions）→ `Subscription auto update`，远程路由配置档对应 `设置` → `Routing` → `Auto update remote profiles`。两者默认均为关闭。

Android 应用也可以生成这些链接：为配置档生成 `add` 链接，为路由配置档生成 `route` 链接。

## 故障排除 {#troubleshooting}

以下消息来自 Throne 桌面版。

- **点击链接没有反应，或浏览器询问要使用哪个应用。** 当前副本没有注册链接处理程序。对于从 ZIP 解压的 Windows 副本，请开启 `启动时注册 throne:// 链接`（见 [Throne 如何接收深度链接](#receive)）。在 macOS 上，请从 `Throne.app` 运行 Throne。其他情况下，启动一次 Throne 即可。如果你保留了多个副本，请在应当打开链接的那个副本中点击 `安装`。你也始终可以复制链接，然后在 Throne 中按 `Ctrl+V`。
- **Linux：链接仍然无法打开。** 注册过程会运行 `desktop-file-utils` 软件包中的 `update-desktop-database` 工具。如果之前缺少该工具，请先安装，然后点击 `启动时注册 throne:// 链接` 旁边的 `安装`。
- **没有任何反应，日志也是空的。** Throne 会不加提示地丢弃以下链接：
  - 载荷不是有效标准 Base64 的 `addsub` 链接，例如带有 `-` 或 `_` 的 URL 安全 Base64，或者包含空格或换行的载荷；
  - 命令后面缺少斜杠的链接（`add` 和 `remoteroute` 链接除外）；
  - 命令未知且载荷无法解码的链接。
- **日志中出现“忽略了带未知命令的深度链接: …”（Ignored deeplink with unknown command: …）。** `throne://` 后面的单词不是 `addsub`、`route`、`remoteroute` 或 `add`。请检查拼写。
- **“该链接不包含订阅 URL。”（The link did not contain a subscription URL.）** `addsub` 载荷已成功解码，但 `#` 前面没有 URL。请编码 `<url>#<name>`，而不是只编码 `#<name>`。
- **“Deep link has no data”（深度链接没有数据）或“Base64 is invalid.”（Base64 无效）。** 这些消息来自 `remoteroute` 链接：`throne://remoteroute/` 后面没有内容，或者载荷不是标准 Base64。
- **“The link did not contain any valid http(s) routing profile URLs.”（该链接不包含任何有效的 http(s) 路由配置档 URL）** `remoteroute` 载荷已成功解码，但没有任何一行以 `http://` 或 `https://` 开头。载荷必须是 URL 列表（每行一个），而不是 JSON。
- **“该链接不包含任何有效的远程路由配置档。”（The link did not contain any valid remote routing profiles.）** 链接中 `remoteroute` 后面缺少斜杠。
- **“该链接无法解析:”（The link could not be parsed:）及其原因。** 这些消息来自 `route` 链接：
  - “Empty input”（输入为空）：`throne://route/` 后面没有内容。
  - “Input is not valid JSON, base64, or a Throne route link”（输入不是有效的 JSON、base64 或 Throne 路由链接）：载荷已损坏或被截断。
  - “Unrecognized route object”（无法识别的路由对象）：JSON 中没有 `"kind": "throne-route-profile"`。
- **日志中出现“导入了 0 个配置档”（Imported 0 profile(s)）。** `add` 载荷已损坏或被截断；或者你扫描的二维码中是 `addsub`、`route` 或 `remoteroute` 链接：请从日志中复制 `QR Code Result:` 之后的文本，然后按 `Ctrl+V`。
- **日志中出现“远程路由配置档 … 失败: …”（Remote routing profile … failed: …）。** 配置档已添加，但其 URL 无法下载，或者提供的不是结构化路由配置档。请修正 URL 或文件，然后使用 `路由设置` 中 `路由` 标签页上的 `更新`。
