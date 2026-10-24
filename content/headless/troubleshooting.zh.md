+++
title = "故障排除"
description = "无界面 Throne 的常见问题，从无法启动的单元到 TUN 冲突和被拒绝的 API 请求，以及 Bug 报告中应包含的内容。"
weight = 60
toc = true
+++

首先以 Throne 的用户身份、使用相同的 `--data-dir` 运行 `Throne --check` 和 `Throne --health`（参见[健康检查与日志](@/headless/monitoring.zh.md)），并阅读日志的最后几行。`EXIT <code>: <reason>` 这一行说明了 Throne 退出的原因；[退出码](@/headless/command_line.zh.md#exit-codes)解释了每个退出码。

## 常见问题 {#symptoms}

| 症状 | 原因与解决方法 |
| --- | --- |
| 单元立即失败，日志显示 `refusing to run as root with /var/lib/throne` | 其他用户可以写入数据目录。请运行 `sudo chmod go-w /var/lib/throne /var/lib/throne/config`。 |
| 退出码 3：`… is in use by …` | 另一个 Throne 占用了该数据目录：桌面版、用户单元或第二个服务。请停止另一个。 |
| 桌面版提示“Throne 正在后台运行”（Throne is running in the background）后退出 | 有一个无界面 Throne（通常是用户单元）在使用桌面版的数据目录。请运行 `systemctl --user stop throne`，或者用 `thronectl` 管理它。参见[与桌面版 Throne 同时运行](@/headless/_index.zh.md#beside-desktop)。 |
| `degraded: api_unavailable`，并且日志显示 `[API] Not listening on 127.0.0.1:9095` | 另一个程序占用了端口 9095。Throne 每 30 秒重试一次。`--api-listen PORT` 可以选择另一个端口。 |
| `--print-connection`：`The API key is not in a file` | 数据目录的设置用自己的密钥开启了 API，就像桌面版那样。请把该密钥用作 `THRONE_KEY`（在桌面版中：`Integration Settings` → `Throne API` → `Copy for scripts`），或者用 `--api-key-file` 启动 Throne。 |
| `--health` 或 `--print-connection`：`No headless Throne answered` | 请以 Throne 的用户身份、使用相同的 `--data-dir` 运行它。对于系统单元，请使用 `sudo`。 |
| Windows：`[Instance] Not talking to … access denied` | 该服务的管道只供 Administrators 和 SYSTEM 使用。请在以管理员身份运行的命令行窗口中运行该命令，并加上 `--data-dir C:\ProgramData\Throne`。 |
| thronectl：`Throne closed the connection without a response` | 密钥错误，或者你的地址在 5 次失败尝试后被拒绝 60 秒，例如由另一个使用旧密钥的客户端造成。请检查 `THRONE_KEY_FILE`，并等待一分钟。 |
| thronectl：`forbidden` | 来自其他设备的[管理请求](@/headless/thronectl.zh.md#admin-requests)。请用 `--api-admin-lan` 启动 Throne，或者在 Throne 所在的设备上运行该命令。 |
| thronectl：无法连接 | Throne 没有运行，或者 `THRONE_ADDR` 指向了别处。请检查 `systemctl status throne` 和 `Throne --print-connection`。 |
| `thronectl tun on`：`needs_privileges` | Throne 缺少 TUN 所需的权限。请运行 `Throne --check`，并参见 [Linux 上的权限](@/headless/installation.zh.md#linux-privileges)。 |
| `thronectl proxy on`：`system_proxy_unsupported` | 无界面 Throne 没有系统代理。请让其他程序使用混合入站，或者使用 TUN。 |
| `tun_conflict`：`the Tun address 172.19.0.1 is already used by the network interface br-…` | Docker 网络（或其他网络）使用了 Throne 的 TUN 地址范围。请用 `thronectl settings set tun_ipv4_cidr=172.29.0.1/24`（任何没有被这台电脑上的网卡使用的范围都可以）把 TUN 移到空闲的范围，然后再次运行 `thronectl tun on`。或者为该 Docker 网络分配另一个子网。 |
| `tun_conflict`：`port 5533 on 127.0.0.1 (the core's DNS server, dns_in_port) is in use` | 另一个程序占用了 DNS 端口。请用一个空闲端口运行 `thronectl settings set dns_in_port=PORT`，然后再次运行 `thronectl tun on`。 |
| 提到另一个 Throne 的 `tun_conflict` | 这台电脑上的另一个 Throne（例如桌面版 Throne）正在运行 TUN。同一时间只能有一个 Throne 运行 TUN。 |
| 配置档被拒绝：`kill_switch_inactive` | Kill Switch 已开启，但无法工作。`thronectl --json status` 中的 `kill_switch_error` 和日志行 `[Kill switch] Not active (<code>)` 会说明原因：`privilege`、`unsupported`、`config` 或 `overridden`。`thronectl settings set kill_switch=false` 可以将其关闭。参见 [Kill Switch](@/advanced/kill_switch.zh.md)。 |
| `degraded: resume_suppressed` | 恢复的配置档在连续三次启动中都导致 Throne 或其核心停止。请修复该配置档，然后用 `thronectl connect <id>` 启动它。 |
| `degraded: core_gave_up` | 核心反复失败。Throne 会[保持运行](@/headless/recovery.zh.md#protection)，并每 5 分钟重试一次。日志中表示放弃的那一行末尾是核心的最后一个错误。 |
| `degraded: vpn_challenge_pending` 或 `vpn_auth_failed` | VPN 配置档需要无界面 Throne 无法提供的登录，或者其已保存的凭据被拒绝。请为该配置档关联一个用于一次性验证码的 [OTP 条目](@/advanced/vpn_profiles.zh.md#otp-manager)，或者在桌面版 Throne 中修正凭据，然后用[备份](@/headless/thronectl.zh.md#from-desktop)迁移过来。 |
| `previous_crash: true` | 上一次运行没有正常结束。它的日志是数据目录中的 `config/logs/crashed-<time>.log`。 |
| Docker：发布的端口 2080 没有响应 | 入站监听的是 `127.0.0.1`。请运行 `thronectl settings set inbound_address=0.0.0.0`，然后重新启动配置档。 |
| Docker：`thronectl shutdown` 之后容器又回来了 | `restart: unless-stopped` 会在每次退出后启动它。请用 `docker compose stop` 停止它。 |
| macOS：Throne 每 10 秒启动一次又退出 | 这是 launchd 不断重试的配置错误。请阅读 `/Library/Logs/Throne/throne.log`。 |
| Windows：服务立即停止 | `sc.exe query Throne` 会把 Throne 的退出码显示为 `SERVICE_EXIT_CODE`。日志位于 `C:\ProgramData\Throne\config\logs`。退出码 78 通常表示[数据文件夹](@/headless/installation.zh.md#windows-data-folder)有问题。 |
| Windows：`tun_failed` 且含有 `open existing adapter`，或日志中出现 `Windows still held the Tun adapter of an earlier session; start the profile again` | Windows 仍占用着上一次未正常结束的运行留下的 TUN 适配器。用 `thronectl connect last` 再次启动配置档，通常就能成功。Throne 不会自行重试。如果一直失败，请重启 Windows。 |
| Kill Switch 或 TUN 把你锁在外面 | 用 `--no-resume --no-kill-switch` 启动 Throne 一次。参见[恢复访问](@/headless/recovery.zh.md#recovery)。 |

## Bug 报告中应包含的内容 {#reporting}

如果问题仍然存在，请[报告 Bug](@/help/bug_reports.zh.md)，并附上：

- `Throne --check` 的输出；
- `Throne --health` 的输出；
- Throne 的运行方式：软件包或镜像及其版本，以及服务管理器；
- 从启动到出现问题为止的日志，如果能复现问题，请使用 `--debug`。如果是崩溃，还请附上 `config/logs/crashed-<time>.log`。

发布之前，请删除其中的服务器地址、订阅 URL 和密钥。切勿发布 `api.key`。
