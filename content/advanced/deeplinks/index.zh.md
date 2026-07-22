+++
title = "深层链接"
description = "使用 throne:// 深层链接，一键添加订阅、分享节点和导入路由配置文件。"
weight = 2

[extra]
+++

Throne 会向你的操作系统注册一个自定义的 `throne://` URL 协议。深层链接（Deep Link）其实就是一个 `throne://` 网址，它告诉正在运行（或尚未运行）的 Throne 实例执行某项操作——例如添加订阅或导入路由配置文件——而无需用户手动在对话框中输入各项数值。

这对于服务商网站、支持页面、二维码、脚本，或者只是想把某个路由配置文件分享给朋友，都非常方便。

> 添加订阅或路由配置文件的链接会先请求确认：Throne 会准确地告诉你将要添加的内容，并等待你的同意。唯一的例外是 `add` 命令，它会不经询问直接把一个节点配置添加到当前分组——就和粘贴一条 `vless://` 链接一样。

## Throne 如何接收深层链接

`throne://` 协议会在你首次运行 Throne 时，于 **Windows、Linux 和 macOS** 上自动注册。由于 Throne 以无需安装的便携式压缩包形式发布，注册会在启动时进行，不需要管理员权限，并且当你移动或更新程序文件夹后会自动修复。

注册完成后，Throne 可从以下任意来源接收深层链接：

- **点击 `throne://` 链接**：在浏览器、聊天软件或文档中点击，操作系统会将其交给 Throne。
- **`程序`（Program）→ `从剪贴板添加配置`（Add profile from clipboard）**：该菜单项在 `服务器`（Server）菜单下也有，快捷键为 `Ctrl+V`，它会从剪贴板读取该链接。
- **拖放**：将链接文本拖放到主界面。
- **作为启动参数传入**：在命令行中传入（Windows/Linux）。在 macOS 上，系统会直接把网址交给已在运行的程序。

如果 Throne 已经打开，链接会交给现有窗口处理，而不会启动第二个实例。

## 链接格式

所有深层链接的结构都相同——一个命令、一个斜杠，以及一段 Base64 数据：

```
throne://<command>/<base64_payload>
```

- 命令**不区分大小写**（`throne://AddSub/...` 和 `throne://addsub/...` 相同）。
- **斜杠和数据部分是必需的。** 命令后面没有 `/<payload>` 的链接会被静默丢弃——既不会有任何反应，也不会记录日志。
- 没有查询参数。链接携带的所有内容都在这段 Base64 数据里。

| 命令 | 用途 | 是否先确认？ |
| --- | --- | --- |
| `addsub` | 添加一个订阅分组并立即更新 | 是 |
| `route` | 导入链接内携带的路由配置文件 | 是 |
| `remoteroute` | 通过 URL 添加一个或多个远程路由配置文件 | 是 |
| `add` | 向当前分组添加一个节点配置 | 否 |

无法识别的命令会被忽略，并以 `Ignored deeplink with unknown command` 记录到日志中。

### 该使用哪种 Base64 字母表

这一点很重要，而且各命令并不相同：

| 命令 | 可接受的编码 |
| --- | --- |
| `addsub` | 仅限**标准** Base64（`+` 和 `/` 字母表）。请保留结尾的 `=` 填充。 |
| `remoteroute` | 仅限**标准** Base64（`+` 和 `/` 字母表）。请保留结尾的 `=` 填充。 |
| `route` | URL 安全 Base64、标准 Base64，甚至未编码的纯 JSON 均可。 |
| `add` | 由 Throne 生成——见下文 [`add`](#add)。 |

对于 `addsub` 和 `remoteroute`，含有 `-` 或 `_` 的 URL 安全数据将无法解码，链接会被拒绝。请使用标准字母表编码。

## `addsub` — 添加订阅

添加一个新的订阅分组并立即更新它。

```
throne://addsub/<base64>
```

数据部分是下面这一行文本的 Base64：

```
<subscription_url>[#<group_name>]
```

| 部分 | 必需 | 说明 |
| --- | --- | --- |
| `<subscription_url>` | **是** | 订阅地址。 |
| `#<group_name>` | 否 | 新分组的名称，写作网址的片段（fragment）部分。省略时默认使用订阅地址的主机名。 |

自动更新**不包含在链接中**。Throne 会在确认对话框里询问，其中的 **Auto update** 复选框默认为勾选状态。

### 示例

要把 `https://example.com/sub/abc123` 添加为名为 **MyProvider** 的分组，请对下面这行文本做 Base64 编码：

```
https://example.com/sub/abc123#MyProvider
```

然后把结果作为数据部分：

```
throne://addsub/aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWIvYWJjMTIzI015UHJvdmlkZXI=
```

Throne 会请你确认：

> 添加此订阅？
>
> 名称：MyProvider
> 地址（URL）：https://example.com/sub/abc123
>
> ☑ 自动更新

确认之后，分组会被创建，订阅也会立即拉取。

> 因为整段文本都经过 Base64 编码，所以**不需要**对订阅地址做百分号编码——其中的 `?`、`&` 和 `/` 都安全地藏在数据里。但如果分组名称含有空格或其他特殊字符，请对其做百分号编码（空格写作 `%20`）。

## `route` — 导入路由配置文件

导入链接内携带的完整路由配置文件（默认出站加规则）。

```
throne://route/<base64>
```

数据部分是经 Base64 编码的路由配置文件。Throne 自己生成的是 URL 安全 Base64（带或不带填充均可）；标准 Base64 和未编码的纯 JSON 同样可用。

### 如何生成 route 链接

通常你不需要手动构造这类链接——Throne 会替你生成：

1. 打开 `路由菜单`（Routing Menu）→ `路由设置`（Routing Settings）。
2. 选中你想分享的路由配置文件。
3. 按 `Ctrl+C`（或使用导出操作）。

Throne 会把一条可直接分享的 `throne://route/...` 链接复制到你的剪贴板。把它发给任何人；当对方打开它（或在`路由设置`中按 `Ctrl+V` 粘贴，或使用`从剪贴板添加配置`）时，Throne 会显示配置文件名称和相关提示，经确认后导入。

### 数据里是什么

这段 Base64 解码后，是一个描述该配置文件的小型 JSON 结构：

```json
{
  "kind": "throne-route-profile",
  "v": 1,
  "name": "Bypass LAN",
  "default_outbound": "proxy",
  "rules": []
}
```

因此链接是这样的（数据部分就是该 JSON 的 Base64）：

```
throne://route/eyJraW5kIjoidGhyb25lLXJvdXRlLXByb2ZpbGUiLCJ2IjoxLCJuYW1lIjoiQnlwYXNzIExBTiIsImRlZmF1bHRfb3V0Ym91bmQiOiJwcm94eSIsInJ1bGVzIjpbXX0
```

由手写 route 段落创建的配置文件带有 `"raw": true` 和一个 `route` 对象，而不是 `rules`；Throne 在导入时会按名称重新映射其中的出站引用，并告知你有哪些无法解析。

> 从剪贴板导入时，Throne 同样能识别纯 JSON 或裸 Base64 形式的相同数据，因此即使链接在传递过程中丢掉了 `throne://route/` 前缀，从另一台机器复制来的链接依然可用。旧版的纯规则数组也可接受——它会在编辑器中打开，以便你为其补上名称和默认出站。

## `remoteroute` — 添加远程路由配置文件

通过 URL 添加一个或多个**远程**路由配置文件。`route` 把整个配置文件塞进链接里，而 `remoteroute` 携带的是托管在网上的配置文件地址：Throne 会从每个地址下载规则，并在你允许时自动保持更新。服务商正是用这种方式提供持续维护的路由配置文件——无需你重新导入，它就会不断改进。

```
throne://remoteroute/<base64>
```

数据部分是一份**以换行分隔的纯 URL 列表**的 Base64，而不是 JSON：

```
<profile_url_1>[#<name_1>]
<profile_url_2>[#<name_2>]
...
```

| 部分 | 必需 | 说明 |
| --- | --- | --- |
| `<profile_url>` | **是** | 指向路由配置文件的 `http://` 或 `https://` 地址。不是有效 http(s) 网址的行会被跳过。 |
| `#<name>` | 否 | 配置文件的显示名称，写作网址的片段（fragment）部分。省略时默认使用该网址的主机名。 |

自动更新**不是逐条设置的**。Throne 只在确认对话框里询问一次，你的回答会应用到该链接中的所有配置文件。**Auto update** 复选框默认为勾选状态。

### 示例

对下面这两行列表做 Base64 编码：

```
https://example.com/routes/bypass-iran.json#BypassIran
https://example.com/routes/ads.json
```

然后把结果作为数据部分：

```
throne://remoteroute/aHR0cHM6Ly9leGFtcGxlLmNvbS9yb3V0ZXMvYnlwYXNzLWlyYW4uanNvbiNCeXBhc3NJcmFuCmh0dHBzOi8vZXhhbXBsZS5jb20vcm91dGVzL2Fkcy5qc29u
```

Throne 会列出该链接将要添加的全部内容，并等待你的确认：

> 添加这些远程路由配置文件？
>
> 1. https://example.com/routes/bypass-iran.json
> 2. https://example.com/routes/ads.json
>
> ☑ 自动更新

确认之后，每个配置文件都会被添加并立即拉取。启用了自动更新的配置文件，随后会依照**基础设置（Basic Settings）**中 **Routing profiles auto update** 的间隔在后台刷新（间隔小于 30 分钟将关闭更新）。

每个远程地址提供的路由配置文件，可以是 `route` 所接受的任意形式——一条 `throne://route/...` 链接、它的 Base64，或原始 JSON。

## `add` — 添加单个节点配置 {#add}

从一段 JSON 出站配置向当前分组添加一个节点。

```
throne://add/<base64>
```

数据部分是该节点出站 JSON 的 Base64——也就是 Throne 为某个服务器导出的那个对象。与其他三个命令不同，这个命令**不会请求确认**：配置会直接添加到当前分组，就和你粘贴一条 `vless://` 或 `ss://` 链接完全一样。

你不需要手动构造这类链接。Throne 会替你生成：

- `服务器`（Server）→ `分享`（Share）→ `Copy links of selected (Deep Links)`（快捷键 `Ctrl+Alt+C`）
- 分享/二维码窗口会在普通分享链接旁一并显示深层链接
- 分组编辑器中的 `Copy profile share links (Deep Links)` 按钮

对于没有标准 `://` 分享网址的协议和选项，深层链接尤其有用，因为完整的 JSON 配置能原样传递。

## 疑难解答

- **点击链接没有反应／浏览器询问用哪个程序打开。** 先运行一次 Throne 让它注册协议，然后再试。如果你移动过 Throne 文件夹，只需再启动一次即可——注册会在启动时自我修复。
- **完全没有反应，日志也是空的。** 链接很可能在命令后面缺少斜杠和数据（写成了 `throne://addsub` 而不是 `throne://addsub/<base64>`），或者它的 Base64 无法解码。这两种情况都会被静默丢弃。
- **「Ignored deeplink with unknown command」。** 命令部分不是 `addsub`、`route`、`remoteroute` 或 `add`。请检查 `throne://` 后面那个词的拼写。
- **「The link did not contain a subscription URL」。** `addsub` 的数据解码成功了，但 `#` 前面没有网址——请确认你编码的是 `<url>#<name>`，而不只是 `#<name>`。
- **「Base64 is invalid.」／「Deep link has no data」。** 数据为空或无法解码。对于 `addsub` 和 `remoteroute`，请确保使用了**标准** Base64：含有 `-` 或 `_` 的 URL 安全数据会被拒绝。
- **「The link did not contain any valid remote routing profiles」。** 解码后没有任何一行以 `http://` 或 `https://` 开头。请记住数据是以换行分隔的网址列表，而不是 JSON 数组。
- **「The link could not be parsed」。** `route` 的数据不是有效的 JSON、Base64 或 Throne route 链接——或者是一个缺少 `"kind": "throne-route-profile"` 标记的 JSON 对象。
