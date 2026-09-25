+++
title = "隐私与网络请求"
description = "Throne 会向订阅服务商发送哪些信息、应用自行发出的所有网络请求，以及谁可以使用它的本地代理端口。"
weight = 40
toc = true
+++

Throne 会按照你的配置档和路由规则发送你的流量。本页介绍 Throne 自行发送的内容：用于订阅的设备信息（HWID）、应用自行发出的网络请求，以及谁可以使用它的本地代理端口。Throne 不会发送使用统计，也不会上传日志或崩溃转储。

## HWID 与设备信息 {#hwid}

有些服务商想知道是哪台设备在请求订阅。Throne 可以在订阅请求中附带四个请求头。此功能默认关闭。

| 请求头 | Windows | Linux | macOS |
| --- | --- | --- | --- |
| `x-hwid` | Windows 的 `MachineGuid` | `/etc/machine-id`（或 `/var/lib/dbus/machine-id`）的内容 | Mac 的硬件 UUID |
| `x-device-os` | `Windows` | `Linux` | `macOS` |
| `x-ver-os` | Windows 版本，例如 `10.0.26100` | 内核版本 | macOS 版本，例如 `14.5` |
| `x-device-model` | Windows 报告的电脑型号（及主板） | 发行版名称，例如 `Ubuntu 24.04.1 LTS` | macOS 名称和版本，例如 `macOS Sonoma (14.5)` |

开启方法：

1. 打开 `设置`（Settings）→ `基本设置`（Basic Settings）→ `订阅`（Subscription）。
2. 开启 `启用在更新订阅时发送硬件ID、设备型号以及 OS 版本`（Enable sending HWID, device model, and OS version when updating subscription）。
3. 点击 `确定`（OK）。

将鼠标悬停在该复选框上，可以查看 Throne 在你的电脑上获取到的值。

- Throne 只在订阅请求中发送这些请求头，绝不会在其他任何请求中发送。
- `自定义系统参数(可选)`（Custom System Parameters (optional)）可以替换 Throne 发送的值。请使用 `hwid=value,os=value,osVersion=value,model=value` 的格式，并且只列出你想替换的值。
- 每个订阅分组都可以单独决定：选择 `分组`（Groups）→ `编辑当前分组`（Edit current Group），然后在 `订阅`（Subscription）部分点击 `Advanced`。`Send HWID` 可以是 `Keep Default`（即沿用上面的设置）、`On` 或 `Off`。`HWID`、`OS`、`OS Version` 和 `Device Model` 字段只替换该分组的值。
- 每个订阅请求还会发送 User-Agent：`Throne/<version>`，例如 `Throne/1.3.1`，除非你在同一标签页中或为该分组设置了其他 `User Agent`。

关于服务商何时需要这些设置，参见 [User-Agent 与 HWID](@/guides/subscriptions.zh.md#user-agent-and-hwid)。

**Android：** `设置`（Settings）→ `订阅`（Subscriptions）中有相同的开关（默认关闭）以及 `Custom HWID parameters (optional)`。Throne for Android 将 Android ID（`ANDROID_ID`）作为 HWID 发送。如果无法获取 Android ID，它会生成一次随机 ID，并在之后一直发送这个 ID。它会将 `Android` 作为操作系统发送，同时发送 Android 版本和设备型号。它的默认 User-Agent 为 `Throne/Android/<version>`。

## 网络请求 {#network-requests}

除了你的应用产生的流量之外，Throne 还会发出下表中的请求。其中许多请求遵循“`使用代理`（Use proxy）规则”：

- 默认情况下，它们直接发出。
- 如果开启了 `设置`（Settings）→ `基本设置`（Basic Settings）→ `杂项`（Miscellaneous）→ `使用代理`（Use proxy），或开启了 `系统代理`（System Proxy），它们会改为经由 Throne 的本地代理端口发出。
- 如果它们应当使用本地代理端口，但没有配置档在运行，请求就会失败，并提示“有用代理的请求，但未启动配置档。”

经由本地代理端口发出的请求，会像其他任何应用的流量一样进入 Throne，因此由你的路由配置档决定它的去向。

| 请求 | 发出时机 | 目标 | 路由方式 |
| --- | --- | --- | --- |
| 订阅更新 | 添加或更新订阅时；如果开启了 `订阅自动更新`（Subscription auto update），还会定时进行（该选项默认关闭） | 你的服务商的 URL | `使用代理` 规则 |
| 远程路由配置档 | 添加或更新远程路由配置档时；如果开启了 `路由配置档自动更新`（Routing profiles auto update），还会定时进行（该选项默认关闭） | 该配置档的 URL。位于 `raw.githubusercontent.com` 上的地址会经由 `远程规则集镜像`（Remote Rule-set Mirror）访问。 | `使用代理` 规则 |
| 路由配置档列表 | 选择 `路由`（Routing）→ `下载配置档`（Download Profiles）→ 某个国家时 | GitHub 上的 throneproj/routeprofiles 仓库，经由镜像访问 | `使用代理` 规则 |
| 规则集 | 配置档启动时，如果其路由或 `启用 AdBlock (广告屏蔽)`（Enable AdBlock）需要一个尚未存入 `cache.db` 的规则集；配置档运行期间大约每天一次；以及选择 `路由` → `更新规则集`（Update Rule-Sets）时 | 经由 `远程规则集镜像`（默认为 `jsDelivr(Cloudflare)`）访问 GitHub，或你添加的 `.srs` URL | 由核心通过你的路由配置档的默认出站发送（如果默认出站为 `block`，则直接发送） |
| 位置查询 | 每次启动配置档后，以及在配置档运行期间打开 `运行时统计`（Runtime Stats）标签页时 | `http://ip-api.com/json/` | 始终经由本地代理端口 |
| URL 测试 | 运行 URL 测试或点击状态栏时、打开 `运行时统计` 标签页时、自动选择器运行期间，以及分组开启了 `Run URL test` 时在订阅更新之后 | `延迟测试 URL`（Latency Test URL），默认为 `http://cp.cloudflare.com/` | 经由每个被测试的配置档 |
| IP 测试 | 仅在选择 `解析选定的出口 IP`（Resolve Selected Out IP）或 `为本组解析 IP`（Resolve out IP for group）时 | `https://api.ip2location.io/` | 经由每个被测试的配置档 |
| 速度测试 | 仅在运行速度测试时 | Speedtest.net 服务器列表和附近的一台 Speedtest 服务器。在 `简单下载`（Simple Download）模式下，则为 `简单下载 URL`（Simple Download URL），默认为 `http://cachefly.cachefly.net/1mb.test`。 | 经由每个被测试的配置档 |
| 连通性检查 | 自动选择器运行期间，且仅当你设置了 `直连测试 URL`（Direct Test URL）或 `连通性 URL`（Connectivity URL）时（两者默认均为空） | 该 URL | 直连 |
| 域名解析 | 仅在选择 `为本组解析域名`（Resolve Domain for group）或 `解析选定域名`（Resolve Selected Domain）时 | 对你的服务器域名进行 DNS 查询 | 你的系统 DNS 解析器 |
| 更新检查 | 仅在选择 `工具`（Tools）→ `检查更新`（Check For Update）时。只有点击 `更新`（Update）后才会开始下载。在 macOS 上、使用系统 Qt 的软件包中，以及通过 Linux 安装脚本安装的副本中，该菜单项处于禁用状态。 | `api.github.com` 以及 GitHub 上的发布文件 | `使用代理` 规则 |
| WARP 注册 | 仅在生成 WARP 配置或身份时 | `api.cloudflareclient.com`，或你在 `注册域名...`（Registration Domains…）中设置的域名 | `使用代理` 规则 |
| Xray geo 文件 | 仅当某个 Xray 配置需要 `geoip.dat` 或 `geosite.dat` 且你同意下载时，或你点击 `下载`（Download）时 | `GeoIP 资源 URL`（GeoIP Asset URL）和 `GeoSite 资源的 URL`（GeoSite Asset URL），默认指向 GitHub | `使用代理` 规则 |
| 网络仪表盘 | `工具` → `打开网络仪表盘`（Open Web dashboard），仅当你的版本没有内置仪表盘时。官方版本都内置了仪表盘。 | GitHub | 始终经由本地代理端口 |
| NTP | 仅当你开启 `NTP 设置`（NTP Settings）时 | 你输入的 NTP 服务器 | 你选择的 `出站`（outbound），默认为 `direct` |

关于位置查询：

- Throne 用它在状态栏、窗口标题和 `运行时统计`（Runtime Stats）标签页中显示你的连接所在的国家和城市。
- 它始终经由本地代理端口。使用内置的 `Default` 路由配置档时，它会通过你的代理发出，因此 ip-api.com 看到的是你的代理地址，而不是你自己的地址。
- 它使用明文 HTTP，并发送 Throne 的 User-Agent。
- 启动之后，如果正在运行的配置档的出口是 OpenVPN 或 OpenConnect 配置档，Throne 会跳过此查询。
- 没有可以关闭它的设置。

你的应用流量所产生的 DNS 查询，会发往 `路由设置`（Routing Settings）→ `DNS` 中设置的服务器。参见 [DNS](@/guides/dns.zh.md)。

**Android：** Throne for Android 会为订阅、路由配置档、规则集、测试和 WARP 注册发出同类请求。开启 `设置`（Settings）→ `订阅`（Subscriptions）→ `Use proxy` 时，或处于 `仅代理`（Proxy only）模式时，它自身的请求会使用本地代理。此时如果没有配置档在运行，订阅更新和 WARP 注册会失败，并提示“Request with proxy but no profile started.”（请求需要经过代理，但没有启动任何配置档。）；但更新检查、路由配置档下载和规则集列表仍然可用：它们会直接发出。Throne for Android 在你连接后不会查询你的位置。它只在你点按 `Check for updates` 时，或在你开启 `Check for updates daily`（该选项默认关闭）后每天一次，向 GitHub 检查更新。`路由`（Routing）界面上的 `Refresh repository list` 会从 GitHub 下载路由配置档列表。

## 本地代理端口 {#local-proxy}

配置档运行期间，Throne 会监听一个本地代理端口，它同时接受 SOCKS5 和 HTTP 连接。该端口默认为 `127.0.0.1:2080`。只有你自己电脑上的程序才能访问 `127.0.0.1`，但其中任何程序都无需密码即可使用该端口。

相关设置位于 `设置`（Settings）→ `基本设置`（Basic Settings）→ `通用`（Common）→ `入站设置`（Inbound Settings）：

| 设置 | 默认值 | 作用 |
| --- | --- | --- |
| `监听地址`（Listen Address） | `127.0.0.1` | 设为 `::` 或 `0.0.0.0` 会向其他设备开放该端口。 |
| `监听端口`（Listen Port） | `2080` | 端口号。 |
| `随机端口`（Random port） | 关闭 | 每次启动时使用一个空闲的随机端口。 |
| `启用认证`（Enable Authorization） | 关闭 | 要求提供 `入站用户名`（Inbound Username）和 `入站密码`（Inbound Password）。 |
| `禁用混合入站`（Disable Mixed Inbound） | 关闭 | 关闭该端口。此时无法使用 `系统代理`（System Proxy）。 |

`程序`（Program）菜单和托盘菜单中的 `允许其他设备连接`（Allow other devices to connect）会把 `监听地址`（Listen Address）设为 `::`。此后，任何能访问你电脑的设备都可以使用你的代理。这样做时，请开启 `启用认证`（Enable Authorization）。参见[局域网共享](@/guides/proxy_modes.zh.md#lan-sharing)。

其他本地端口：

| 端口 | 默认值 | 谁可以访问 |
| --- | --- | --- |
| `DNS 服务器端口`（DNS Server Port）：`基本设置` → `杂项` | `5533` | 仅限本机（`127.0.0.1`）。 |
| Clash API：`基本设置` → `核心`（Core） | 关闭（`监听端口` 为空） | Clash API 的 `监听地址`，默认为 `127.0.0.1`。开启时请设置 `密钥`（Secret）。 |
| sing-box API / 仪表盘：`基本设置` → `核心` | 关闭（`监听端口` 为空） | 仅限本机。由随机生成的 `密钥` 保护。 |

当配置档使用 Xray 时，核心还会在 `127.0.0.1` 上打开若干内部端口，每个端口都由随机密码保护。Throne 与其核心之间通过本地套接字通信，而不是通过网络端口。

**Android：** `设置`（Settings）→ `Inbound` 中有同类选项：`代理端口`（Proxy port）、`允许来自局域网的连接`（Allow connections from the LAN）和 `Enable authorization`，其中 `允许来自局域网的连接` 默认关闭。

## 本网站 {#website}

本文档站点使用 Yandex Metrika 统计访问量。它会记录页面浏览量、来源页面、页面上和链接上的点击，以及访问者的停留时长。会话录制功能已关闭。Throne 应用中不包含此统计代码。
