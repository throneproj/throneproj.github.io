+++
title = "OpenVPN、OpenConnect 与 Tailscale"
description = "导入并设置 OpenVPN、OpenConnect 和 Tailscale 配置档，使用一次性验证码登录，并让工作 VPN 与代理同时运行。"
weight = 50
toc = true
+++

Throne 可以连接 OpenVPN 服务器以及 Cisco AnyConnect 和兼容的 VPN（OpenConnect），还可以加入 Tailscale 网络。这些 VPN 客户端内置于核心中，因此无需另行安装 OpenVPN 或 OpenConnect。本页介绍导入方式、主要选项、使用一次性验证码登录，以及如何让工作 VPN 与代理同时运行。

## OpenVPN {#openvpn}

可通过以下任一方式导入 `.ovpn` 文件：

- `程序`（Program）→ `添加文件中的配置档`（Add profile from File(s)），快捷键 `Ctrl+O`。
- 将文件拖到主窗口上。
- 复制文件的文本内容，然后在主窗口中按 `Ctrl+V`。

要手动创建配置档，请使用 `程序` → `新建配置档`（New profile），并将 `类型`（Type）设为 `OpenVPN`。

关于导入，需要了解以下几点：

- 只支持 `dev tun` 的客户端配置。TAP 配置（`dev tap`）和服务器端配置会被拒绝。
- 不支持 PKCS#12 证书包（`pkcs12`）。请将 CA、证书和密钥导出为 PEM 格式，然后分别粘贴到 `CA 证书`（CA Certificate）、`客户端证书`（Client Certificate）和 `客户端钥匙`（Client Key）中。
- 如果该文件把登录信息保存在单独的文件中（`auth-user-pass <file>`），请在配置档中填写 `用户名`（Username）和 `密码`（Password）。
- 未知或不受支持的选项会列在日志中以 `OpenVPN:` 开头的行里。不适用于 Throne 的选项（例如 `up` 和 `down` 脚本或 `persist-tun`）会被直接跳过，不作提示。
- 如果该文件让所有流量都经过 VPN（`redirect-gateway`），Throne 会为该配置档关闭 `仅路由通告的网络`（Only route advertised network）。

编辑器中还有 `网络协议`（Network，留空表示 `udp`）、`静态质询`（Static Challenge）、`MTU`、`OTP`、`隧道 DNS`（Tunnel DNS）、TLS 文件，以及用于 `tls-auth` 和 `tls-crypt` 密钥的 `控制通道封装`（Control Channel Wrap）。`高级`（Advanced）中还有更多选项。

## OpenConnect {#openconnect}

配置档中的 `类型`（Flavor）用于选择服务器类型：

| `类型`（Flavor） | 服务器类型 |
| --- | --- |
| 留空或 `anyconnect` | Cisco AnyConnect 及兼容服务器 |
| `gp` | Palo Alto GlobalProtect |
| `fortinet` | Fortinet |
| `f5` | F5 BIG-IP |
| `pulse` | Pulse Connect Secure |
| `nc` | Juniper Network Connect |

Throne 可以从文件、剪贴板或订阅导入以下格式：

- AnyConnect XML 配置文件。其 `<ServerList>` 中的每台服务器都会成为一个配置档。使用 IPsec（IKEv2）的服务器以及没有地址的条目会被跳过，并附带说明。
- `openconnect` 命令行，例如 `openconnect --protocol=gp --user=alice vpn.example.com`。
- 每行一个选项、且包含 `protocol=` 行（例如 `protocol=fortinet`）的配置文件。

其他主要字段包括 `用户名`、`密码`、`认证组`（Auth Group，用于预先选择组、认证域或网关）、`服务器路径`（Server Path，服务器 URL 中的路径部分，部分 GlobalProtect、F5 和 Fortinet 门户需要）、`MTU`、`OTP` 以及 TLS 选项。`高级` 中还有更多选项，例如会话 `Cookie` 和 `软件令牌`（Software Token）。

## 两种 VPN 共有的选项 {#vpn-options}

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `仅路由通告的网络` | 开启 | 启动此配置档时，只有发往 VPN 服务器所通告网络的流量才会进入隧道，到达该配置档的其他流量会被阻止。指定此配置档的路由规则不受影响。如果 VPN 需要承载所有流量，请关闭此项。 |
| `隧道 DNS` | `优先`（Prefer） | Throne 如何使用 VPN 服务器下发的 DNS 服务器。`无`（None）：忽略它们。`优先`：只通过它们解析服务器声明的域名（即其 split DNS 域名）。`严格`（Strict）：还把所有远程 DNS 查询都发给它们，它们无法解析的域名将解析失败。 |
| `用户名`、`密码` | 空 | 登录凭据。这些字段中的 `{otp}` 会被替换为一次性验证码，参见[在 VPN 配置档中使用验证码](#bind-otp)。 |

对于路由配置档端点，`优先` 和 `严格` 都只解析服务器声明的域名。

## 登录 {#sign-in}

Throne 使用已保存的 `用户名` 和 `密码` 登录。当服务器要求提供更多信息时，会打开 `VPN 认证`（VPN Authentication）窗口：

- **问题或表单**，例如第二个密码：填写后点击 `提交`（Submit）。有些请求会显示时间限制（“… 后过期”，Expires in …）。
- **登录页面：** 窗口中会显示一个地址和 `在浏览器中打开`（Open in Browser）按钮。在浏览器中完成登录，然后关闭该窗口。服务器接受登录后，连接会继续进行。
- **只能在浏览器内完成的单点登录（SSO）** 目前尚不支持。请使用用户名和密码登录；对于 OpenConnect，也可以在配置档的 `高级` 设置中填写会话 `Cookie`。

如果服务器拒绝了已保存的登录凭据，Throne 会请你输入本次会话使用的用户名和密码，并提供 `重连`（Reconnect）。这些凭据不会保存到配置档中，你手动停止配置档后 Throne 就会将其遗忘。最多询问三次。

主窗口底部的 `运行时统计`（Runtime Stats）标签页列出了每个 VPN 连接及其状态，并提供 `详情`（Details）按钮。

## OTP 管理器 {#otp-manager}

许多工作 VPN 要求输入身份验证器应用生成的一次性验证码。从 1.3.0 起，Throne 内置了自己的身份验证器：`工具`（Tools）→ `OTP 管理器`（OTP Manager）。

添加条目：

- `导入`（Import）→ `手动添加...`（Add manually...）：填写 `名称`（Name）和 `密钥`（Secret，Base32 格式）。只有在服务商要求时，才需要更改 `类型`、`算法`（Algorithm）、`位数`（Digits，4 到 10，默认 6）或 `周期 (秒)`（Period (seconds)，默认 30）；其中 `类型` 可选 `TOTP (基于时间)`（TOTP (time based)）或 `HOTP (基于计数器)`（HOTP (counter based)）。窗口中会显示当前验证码，方便你与其他身份验证器进行比对。
- `导入` → `来自链接或文本...`（From link or text...）：粘贴 `otpauth://` 链接、`otpauth-migration://` 链接（Google Authenticator 的导出格式）、JSON 导出内容，或者仅粘贴一个 Base32 密钥。
- `导入` → `来自剪贴板`（From clipboard，也可以在窗口中按 `Ctrl+V`），或 `来自 QR 图像文件...`（From QR image file...）。
- `扫描二维码`（Scan QR Code）会在屏幕上查找二维码。

使用条目：

- 点击条目即可复制其当前验证码。
- 拖动条目可调整顺序。
- 条目上的 `导出`（Export）提供 `这一个为 otpauth:// 链接和 QR 形式`（This one as otpauth:// link and QR）、`全部为 otpauth-migration:// 链接和 QR 形式`（All as otpauth-migration:// link and QR）和 `全部为 JSON 文件...`（All as JSON file...）。
- `删除`（Delete）会移除条目，其密钥无法恢复。
- 托盘菜单中有 `OTP 代码`（OTP Codes），这是一个包含所有验证码的可搜索列表。点击验证码即可复制。

OTP 条目会包含在备份中，对应 `设置`（Settings）→ `基本设置`（Basic Settings）→ `备份和恢复`（Backup and Restore）中的 `OTP 配置档`（OTP profiles）一项。请妥善保管备份文件，不要泄露。

### 在 VPN 配置档中使用验证码 {#bind-otp}

1. 打开 OpenVPN 或 OpenConnect 配置档。
2. 在 `OTP` 中选择对应条目。
3. 如果服务器要求把验证码作为密码的一部分，请在验证码所在的位置写上 `{otp}`，例如 `MyPassword{otp}`。对于 OpenConnect，`{otp}` 在软件令牌和表单字段中同样有效。
4. 点击 `确定`（OK）。

此后 Throne 每次连接时都会填入新的验证码。它还会自动回应服务器的验证码提示：OpenVPN 质询（如果服务器使用静态质询，请在 `静态质询` 中填写质询文本）以及 OpenConnect 登录表单。如果服务器拒绝了某个验证码，Throne 会换一个新的重试，最多三次。如果服务器拒绝了整个登录，Throne 会用新的验证码重启配置档（最多三次），而不是询问你。

## 分离隧道：让工作 VPN 与代理并行 {#split-tunnel}

从 1.3.0 起，路由配置档可以在你运行的配置档之外，同时启动 OpenVPN 或 OpenConnect 配置档。发往 VPN 服务器所通告网络的流量经由 VPN 传输，其余流量则按路由配置档处理，例如经由你的代理。

1. 导入或创建 VPN 配置档。
2. 打开 `路由`（Routing）→ `路由设置`（Routing Settings）→ `路由`（Route）标签页。
3. 选中你正在使用的路由配置档，点击 `编辑`（Edit）。
4. 打开 `端点`（Endpoints）标签页。只有当你拥有 OpenVPN 或 OpenConnect 配置档，或者以此类配置档结尾的代理链时，该标签页才会出现。
5. 在列表中选择该 VPN 配置档，点击 `添加`（Add）。
6. 点击 `确定`，并确认该路由配置档是当前启用的路由配置档（在 `路由` 菜单底部处于勾选状态）。
7. 启动你平时使用的配置档，VPN 会随之启动。

每个端点都会在 `高级`（Advanced）标签页中添加一条名为 `<name> 路由优选`（`<name> route prefer`）的规则，其中 `<name>` 是 VPN 配置档的名称。你无法编辑这条规则，但可以在你自己的规则之间移动它：位于它上方的规则会先被检查。删除这条规则时，会询问是否移除该端点。

限制：

- 用作端点的配置档不能同时是你启动的配置档，也不能是其中的跳点。
- 端点可以是一条出口（代理链的最下面一行）为 OpenVPN 或 OpenConnect 配置档的代理链。勾选 `允许路由到内部跳点`（Allow routing to inner hops）后，代理链内部的每个 OpenVPN 或 OpenConnect 跳点也会各自获得一条规则。
- 端点中的跳点不能运行在 Xray 上，也不能是额外核心或完整配置类配置档。

完整示例请参见[常用方案](@/guides/recipes.zh.md#corporate-vpn)。

## Tailscale {#tailscale}

Tailscale 配置档会加入你的 tailnet，让你可以访问自己的 Tailscale 设备，或将其中一台用作出口节点。Tailscale 配置档仅在桌面版中提供。

1. 打开 `程序` → `新建配置档`。
2. 将 `类型` 设为 `Tailscale`。
3. 填写下列字段。`认证钥匙`（Auth key）需要在 Tailscale 管理控制台中创建。
4. 点击 `确定` 并启动该配置档。

| 字段 | 默认值 | 作用 |
| --- | --- | --- |
| `状态目录`（State directory） | `$HOME/.tailscale` | 保存登录状态的位置。 |
| `认证钥匙`（Auth key） | 空 | 用于登录你的 tailnet 的密钥。 |
| `控制 URL`（Control URL） | `https://controlplane.tailscale.com` | 协调服务器。仅在使用自建控制服务器时才需更改。 |
| `主机名`（Hostname） | 空 | 此设备在 tailnet 中的名称。 |
| `接受路由`（Accept routes） | 关闭 | 使用其他设备通告的子网路由。 |
| `Ephemeral (短暂)` | 关闭 | 注册为临时设备，该设备离线后会被 tailnet 移除。 |
| `出口节点`（Exit node） | 空 | 通过该 tailnet 设备发送互联网流量。 |
| `出口节点允许LAN访问`（Exit node allow lan access） | 关闭 | 使用出口节点时仍可访问本地网络。 |
| `通告出口节点`（Advertise exit node） | 关闭 | 将这台电脑作为出口节点提供出去。 |
| `通告路由`（Advertise routes） | 空 | 向 tailnet 提供的子网，以逗号分隔。 |
| `全局 DNS`（Global DNS） | 关闭 | 让 Tailscale 的 DNS 也使用 tailnet 的全局域名服务器。 |

Throne 使用 Tailscale 的 DNS 解析你的 tailnet 设备名称（位于 `ts.net` 下），其他域名则使用你平常的 DNS 设置。URL 测试和自动选择器会跳过 Tailscale 配置档。

## Android 版 {#android}

- OpenVPN 和 OpenConnect 配置档在 Android 上同样可用，支持相同的导入格式。编辑器中的选项较少：没有 OTP 绑定，也没有 `仅路由通告的网络` 和 `隧道 DNS`。
- 没有 OTP 管理器，也没有 `VPN 认证` 窗口。配置档必须使用已保存的用户名和密码登录。桌面版备份中的 OTP 条目不会被恢复。
- 路由配置档端点（分离隧道）无法在 Android 上运行。来自桌面版备份的路由配置档会保留其端点，但 Android 不会启动它们。
- 不支持 Tailscale 配置档。
- 在两个平台上，自动选择器都会跳过 OpenVPN、OpenConnect 和 Tailscale 配置档。
