+++
title = "常用方案"
description = "常见任务的分步设置：仅代理被封锁的网站、共享代理、移动热点、通话与游戏、虚拟机、企业 VPN 以及按应用分流。"
weight = 80
toc = true
+++

本页为常见任务提供简短的分步设置方法。每个方案都附有链接，指向详细介绍相关功能的页面。

## 仅代理被封锁的网站 {#proxy-only-blocked-sites}

只让被封锁的网站走代理，其余全部直连。这样本国网站依然访问迅速，你的服务器承担的流量也更少。

**使用现成的配置档（中国、俄罗斯）：**

1. 打开 `路由`（Routing）菜单 → `下载配置档`（Download Profiles），然后选择 `China` 或 `Russia`。
2. 保持勾选 `自动更新`（Auto update），然后点击 `确定`（OK）。
3. 再次打开 `路由` 菜单，选择 `Proxy China Blocked`；如果是俄罗斯，则选择 `Proxy Russia Blocked`、`Proxy Antizapret` 或 `Proxy Refilter`。

**使用你自己的列表（适用于任何国家）：**

1. 打开 `设置`（Settings）→ `路由设置`（Routing Settings）→ `路由`（Route），然后点击 `新建`（New）→ `结构化配置档`（Structured profile）。
2. 输入 `名称`（Name），例如 `Blocked sites`，并将 `默认出站`（Default outbound）设为 `direct`。
3. 在 `基本`（Basic）标签页上，将网站填入 `代理`（Proxy）输入框，每行一个（参见下面的示例）。
4. 点击 `确定`（OK）。在 `通用`（Common）标签页上，将 `Blocked sites` 选为 `路由配置档`（Routing Profile），然后点击 `确定`。

```text
ruleset:geosite-youtube
ruleset:geosite-telegram
ruleset:geoip-telegram
suffix:example.com
```

如果某个被封锁的网站仍然无法打开，说明它使用的域名比你列出的更多。打开该网站，在 `连接`（Connections）标签页中找到它的连接，右键点击其中一个，然后选择 `追加 "<host>" 到`（`Append "<host>" to`）→ `代理`（Proxy）。对于大型服务，使用 `geosite-` 规则集比逐个添加域名更方便。有些应用（例如 Telegram）还会直接连接 IP 地址，因此请添加它们的 `geoip-` 规则集，并使用 `Tun 模式`（Tun Mode）。参见[路由](@/guides/routing.zh.md#simple-rules)。

## 与其他设备共享代理 {#share-with-devices}

你网络中的其他设备（例如手机、电视或游戏机）可以把你电脑上的 Throne 用作代理。

1. 打开 `程序`（Program）菜单，开启 `允许其他设备连接`（Allow other devices to connect）。托盘菜单中也有此选项。
2. 查看状态栏的中部，此时会显示 `Mixed: <address>:2080`，即其他设备要使用的地址和端口。
3. 建议：打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `通用`（Common），勾选 `启用认证`（Enable Authorization），并设置 `入站用户名`（Inbound Username）和 `入站密码`（Inbound Password）。
4. 在其他设备上，使用该地址和端口设置 HTTP 或 SOCKS5 代理；如果你设置了用户名和密码，也一并填写。

注意事项：

- Throne 必须在电脑上保持运行。其他设备的流量会遵循你当前活动的路由配置档。
- 认证对所有使用该端口的用户都有效，包括你电脑上使用系统代理的应用。
- 如果某台设备无法连接，请检查电脑的防火墙是否允许 `ThroneCore` 接受传入连接。
- **Android：** 开启 `设置`（Settings）→ `Inbound` → `允许来自局域网的连接`（Allow connections from the LAN）。参见 [Android 上的局域网共享](@/android/modes.zh.md#lan-sharing)。

关于代理端口的更多信息，请参见[局域网共享](@/guides/proxy_modes.zh.md#lan-sharing)。

## 在 TUN 模式下使用 Windows 移动热点 {#hotspot}

当 `Tun 模式`（Tun Mode）开启时，如果 Windows 通过移动热点或 Internet 连接共享来共享你的常规网卡，Throne 会显示“IPv4 forwarding breaks Tun mode”（IPv4 转发会破坏 TUN 模式）。这时 Windows 会忽略那项让 Throne 自身连接不进入隧道的设置，导致这些连接绕回隧道并失败。

Throne 的警告中给出了一个变通方法，用户也在 [#1916](https://github.com/throneproj/Throne/issues/1916) 中报告过：改为共享 Throne 的 TUN 网卡的连接。

1. 在 Throne 中开启 `Tun 模式`（Tun Mode）并启动一个配置档。
2. 在 Windows 中打开 `设置`（Settings）→ `移动热点`（Mobile hotspot）→ `从以下位置共享我的 Internet 连接`（Share my internet connection from），然后选择 `throne-tun`。
3. 开启热点。

`throne-tun` 网卡仅在 `Tun 模式`（Tun Mode）开启时存在。连接共享是 Windows 的功能，Throne 无法控制。如果这个变通方法对你无效，请在使用 `Tun 模式` 时关闭热点，或者让设备改用代理端口（参见[与其他设备共享代理](#share-with-devices)）。

## 语音通话和游戏 {#calls-and-games}

Discord 和 Telegram 中的语音通话以及许多游戏都使用 UDP，并且经常忽略系统代理。

- 使用 `Tun 模式`（Tun Mode），这样这些流量才能到达 Throne。
- 你的服务器及其协议必须能够承载 UDP。并非所有协议都可以（HTTP 代理就不行），有些服务器也会关闭 UDP。如果在某个服务器上通话失败，请换一个服务器试试。
- 为了降低延迟，请选择距离较近的服务器。参见 [URL 测试](@/guides/testing.zh.md#url-test)。
- 如果某个游戏不需要代理，就让它直连：将它的程序填入 `直连`（Direct）输入框，例如 `processName:game.exe`。
- 对于在 TUN 模式下直连的游戏和点对点应用，可以试试 `设置`（Settings）→ `Tun 设置`（Tun Settings）→ `L3 桥接绕过`（L3 Bridge Bypass）。它会让直连的 UDP 和 ICMP 流量直接从你的网卡发出，速度更快，并能让 NAT 保持正常工作。

## Docker、WSL 和虚拟机 {#docker-wsl-vms}

容器、WSL 和虚拟机都有各自的虚拟网络。有两种方法可以让它们使用代理。

**让它们指向 Throne 的代理端口。** 这是最简单、最可靠的方法。

1. 开启 `程序`（Program）→ `允许其他设备连接`（Allow other devices to connect）。
2. 在容器或虚拟机内部，将代理设为 `http://<address>:2080`。请使用客户机能够访问到的电脑地址，例如状态栏中显示的地址。

Linux 上的许多命令行工具都会读取以下变量：

```bash
export http_proxy=http://192.168.1.10:2080
export https_proxy=http://192.168.1.10:2080
```

同一端口也接受 SOCKS5。

**在电脑上使用 TUN 模式。** 客户机的流量是否进入隧道，取决于其虚拟网络的构建方式。如果客户机断网，或者你无法从电脑访问它们，请检查 `设置`（Settings）→ `Tun 设置`（Tun Settings）中的以下设置：

- 保持 `私有地址范围绕过`（Private Range Bypass）开启（默认开启）。它会让私有地址范围（虚拟网络通常使用这些地址）不进入隧道。
- `启用 Tun 路由`（Enable Tun Routing）还会让 `direct` 规则中的 IP 范围不进入隧道。在 Windows 上，大型规则集可能导致 CPU 占用过高，因此请谨慎开启。
- **Linux：** 在较新的内核上，`system` 和 `mixed` 协议栈需要 `自动重定向`（Auto Redirect，默认开启）。开启时，这台电脑无法作为其他设备的网络网关，由它转发流量的容器或虚拟机也可能受到影响。请改为让它们使用代理端口。

参见 [TUN 模式](@/guides/tun_mode.zh.md#settings)。

## 与企业 VPN 并存 {#corporate-vpn}

如果要通过企业 VPN 访问公司资源，同时让其他所有流量使用 Throne，就需要让公司的流量避开代理。请选择以下方法之一。

**让公司流量直连。** 将公司的域名和网络添加到路由配置档的 `直连`（Direct）输入框中：

```text
suffix:corp.example.com
ip:10.20.0.0/16
```

开启 `启用 DNS 路由`（Enable DNS Routing，默认开启）时，公司的域名会使用直连 DNS 而不是远程 DNS 查询。在 TUN 模式下，`10.0.0.0/8` 等私有地址范围本来就不会进入隧道（`私有地址范围绕过`）。对于使用公网地址范围的公司网络，请开启 `Tun 设置`（Tun Settings）→ `启用 Tun 路由`（Enable Tun Routing），它会让 `direct` 规则中的 IP 范围不进入隧道。

**绑定到 VPN 的网卡。** 当直连流量从错误的网卡发出时，请使用此方法。

1. 打开 `程序`（Program）→ `新建配置档`（New profile），选择类型 `直连`（Direct），并为其命名，例如 `Corporate`。
2. 点击 `高级设置`（Advanced Settings），在 `绑定接口`（Bind Interface）中输入企业 VPN 网卡的名称，然后点击 `确定`（OK）。再点击 `确定` 保存该配置档。
3. 在你的路由配置档中添加一条[高级规则](@/guides/routing.zh.md#advanced-rules)，填入公司的 `domain_suffix` 和 `ip_cidr`，动作选择 `route`，并将 `outbound` 设为 `[group] Corporate`。将它移到其他规则之上。

**在 Throne 内运行 VPN。** Throne 可以在代理之外同时运行 OpenVPN 或 OpenConnect 配置档，仅用于该 VPN 所通告的网络。参见[分离隧道](@/advanced/vpn_profiles.zh.md#split-tunnel)。

其他 VPN 程序可能会干扰 `Tun 模式`（Tun Mode）。如果问题只在 TUN 模式下出现，请在企业 VPN 连接期间使用系统代理模式。

## 按应用分流 {#per-app}

选择哪些程序使用代理。

**桌面版：**

1. 开启 `Tun 模式`（Tun Mode）。只有在 TUN 模式下，所有程序的流量才会到达 Throne。
2. 启动该程序，让它建立连接。
3. 在 `连接`（Connections）标签页中，右键点击它的某个连接，然后选择 `追加进程 "<name>" 到`（`Append process "<name>" to`）→ `代理`（Proxy）、`直连`（Direct）或 `阻止`（Block）。
4. 点击“设置已更改，重启进行应用”提示中的 `重启`（Restart）。

你也可以在路由配置档的 `基本`（Basic）标签页上自行编写规则，例如 `processName:Telegram.exe` 或 `processPath:C:\Program Files\App\app.exe`。名称必须完全匹配，包括大小写。

- **只让部分程序走代理：** 将 `默认出站`（Default outbound）设为 `direct`，并把这些程序填入 `代理`（Proxy）输入框。
- **除部分程序外全部走代理：** 保持 `默认出站` 为 `proxy`，并把例外的程序填入 `直连`（Direct）输入框。

如果 `追加`（Append）菜单项被禁用，说明无法从那里修改当前活动的路由配置档，例如它是一个会自动更新的远程配置档。参见[连接标签页](@/guides/routing.zh.md#connections-tab)。

**Android：** 在 `设置`（Settings）→ `TUN / VPN` → `分应用代理`（Apps VPN mode）中选择应用，或者使用路由规则中的 `Apps` 字段。参见[分应用代理](@/android/modes.zh.md#per-app-proxy)。
