+++
title = "深层链接"
description = "使用 throne:// 深层链接，一键添加订阅和导入路由配置文件。"
weight = 2

[extra]
+++

Throne 会向你的操作系统注册一个自定义的 `throne://` URL 协议。深层链接（Deep Link）其实就是一个 `throne://` 网址，它告诉正在运行（或尚未运行）的 Throne 实例执行某项操作——例如添加订阅或导入路由配置文件——而无需用户手动在对话框中输入各项数值。

这对于服务商网站、支持页面、二维码、脚本，或者只是想把某个路由配置文件分享给朋友，都非常方便。

> 每个深层链接在保存任何内容之前都会请求确认。Throne 会准确地告诉你将要添加的内容，并等待你的同意，因此打开一个链接绝不会在你不知情的情况下更改你的配置。

## Throne 如何接收深层链接

`throne://` 协议会在你首次运行 Throne 时，于 **Windows、Linux 和 macOS** 上自动注册。由于 Throne 以无需安装的便携式压缩包形式发布，注册会在启动时进行，不需要管理员权限，并且当你移动或更新程序文件夹后会自动修复。

注册完成后，Throne 可从以下任意来源接收深层链接：

- **点击 `throne://` 链接**：在浏览器、聊天软件或文档中点击，操作系统会将其交给 Throne。
- **粘贴**：在主界面按 `Ctrl+V` 粘贴该链接。
- **拖放**：将链接文本拖放到主界面。
- **`服务器`（Server）→ `从剪贴板添加配置`（Add profile from clipboard）**：从剪贴板读取该链接。
- **作为启动参数传入**：在命令行中传入（Windows/Linux）。

如果 Throne 已经打开，链接会交给现有窗口处理，而不会启动第二个实例。

## 命令参考

深层链接的格式为：

```
throne://<command>/?<parameters>
```

命令**不区分大小写**（`throne://AddSub` 和 `throne://addsub` 相同），`?` 前结尾的斜杠是可选的。Throne 目前支持两个命令。

| 命令 | 用途 |
| --- | --- |
| `addsub` | 添加一个订阅分组并立即更新 |
| `route`  | 导入一个路由配置文件 |

无法识别的命令会被忽略，并记录到日志中。

## `addsub` — 添加订阅

添加一个新的订阅分组并立即更新它。

```
throne://addsub/?url=<subscription_url>&name=<group_name>&autoupdate=<value>
```

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `url` | **是** | 订阅链接。必须经过 **百分号编码（percent-encoding）**（参见下方提示）。如果缺失，Throne 会显示警告并且不执行任何操作。 |
| `name` | 否 | 新分组的名称。省略时默认使用订阅链接的主机名。 |
| `autoupdate` | 否 | 该分组是否自动更新。取值 `1`、`true`、`on` 或 `yes`（不区分大小写）表示启用。该参数**缺失时默认启用**。其他任何值都会将其禁用。 |

### 示例

```
throne://addsub/?url=https%3A%2F%2Fexample.com%2Fsub%2Fabc123&name=My%20Provider&autoupdate=yes
```

该链接会为 `https://example.com/sub/abc123` 添加一个名为 **My Provider** 的分组，并开启自动更新。Throne 会请求你确认：

> 添加此订阅？
> 名称：My Provider
> URL：https://example.com/sub/abc123
> 自动更新：开

确认后，分组即被创建，订阅也会立即拉取。

> **务必对 `url` 的值进行百分号编码。** 订阅链接包含 `:`、`/`、`?`、`&` 等字符，否则它们会被误认为深层链接本身的一部分。例如，`https://example.com/sub?id=1` 应写成 `https%3A%2F%2Fexample.com%2Fsub%3Fid%3D1`。`name` 中的空格和特殊字符同理（空格写成 `%20`）。

## `route` — 导入路由配置文件

导入链接中携带的完整路由配置文件（默认出站连接及规则）。

```
throne://route?data=<base64>
```

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `data` | **是** | 经过 Base64 编码的路由配置文件。推荐使用 URL 安全的 Base64（可带或不带填充）；标准 Base64 也可接受。 |

### 如何生成 route 链接

通常你无需手动构造这些链接——Throne 会为你生成：

1. 打开 `路由`（Routes）→ `路由设置`（Routing Settings）。
2. 选择你想分享的路由配置文件。
3. 按 `Ctrl+C`（或使用导出操作）。

Throne 会把一个可直接分享的 `throne://route?data=...` 链接复制到你的剪贴板。把它发送给任何人；当对方打开它（或粘贴它／使用 `从剪贴板添加配置`）时，Throne 会显示配置文件名称及相关提示，并在确认后导入。

### `data` 里面是什么

Base64 负载会解码为一个描述该配置文件的小型 JSON 结构：

```json
{
  "kind": "throne-route-profile",
  "v": 1,
  "name": "Bypass LAN",
  "default_outbound": "proxy",
  "rules": []
}
```

因此上面的链接如下所示（`data` 的值就是该 JSON 的 Base64 编码）：

```
throne://route?data=eyJraW5kIjoidGhyb25lLXJvdXRlLXByb2ZpbGUiLCJ2IjoxLCJuYW1lIjoiQnlwYXNzIExBTiIsImRlZmF1bHRfb3V0Ym91bmQiOiJwcm94eSIsInJ1bGVzIjpbXX0
```

> 从剪贴板导入时，Throne 也会把同样的负载识别为普通 JSON 或裸 Base64，因此即使从其他设备复制的链接在传递过程中丢失了 `throne://route?data=` 前缀，仍然可以使用。

## 故障排除

- **点击链接没有反应／浏览器询问使用哪个应用打开。** 先运行一次 Throne 让它注册协议，然后重试。如果你移动了 Throne 文件夹，只需再次启动它——注册会在启动时自动修复。
- **“Ignored deeplink with unknown command”。** 命令部分不是 `addsub` 或 `route`。请检查 `throne://` 紧后面那个词的拼写。
- **“The link did not contain a subscription URL”。** `addsub` 链接缺少 `url` 参数，或其值在解码后为空。
- **订阅导入了错误的地址。** `url` 的值没有进行百分号编码，导致它在 `?`、`&` 或 `#` 处被截断。请对该值进行编码后重新生成链接。
