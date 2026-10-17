+++
title = "健康检查与日志"
description = "检查一台电脑能否运行无界面 Throne，询问正在运行的 Throne 状态如何，查看它的 systemd 状态并找到它的日志。"
weight = 40
toc = true
+++

无界面 Throne 有两项内置检查：`Throne --check` 用于首次启动之前或出现问题时，`Throne --health` 用于正在运行的 Throne。它还会向 systemd 报告自身状态，并写入日志。

## Throne --check {#check}

`Throne --check` 会告诉你这台电脑能否按当前的设置运行无界面 Throne。请以 Throne 的用户身份运行它，并使用 Throne 启动时所用的选项和变量。它不会更改任何内容：不创建文件、不获取锁、以只读方式打开数据库，并且可以与正在运行的 Throne 同时运行。

它为每一项打印一行，有解决方法时还会打印 `fix:` 行：

```text
$ sudo /opt/Throne/Throne --check
[INFO] build: Throne <version>, Qt 6.x, Debian GNU/Linux 12 (bookworm) x86_64, kernel 6.1.0-28-amd64, euid 0, ruid 0
[INFO] data dir /var/lib/throne (root default): does not exist yet; the first start creates it
[ OK ] instance: none (no data dir yet)
...
[INFO] API key: /var/lib/throne/config/api.key is created on the first start
[ OK ] port 127.0.0.1:9095 (the Throne API, the headless default): free
[ OK ] port 127.0.0.1:2080 (the mixed proxy, inbound_port): free
...
result: 0 failed, 0 warnings
```

它检查的内容包括：构建版本、数据目录、正在运行的实例、设置、TLS、核心、TUN、Kill Switch、API 密钥、端口（API、混合入站、DNS 端口，以及开启时的 Clash API 和 sing-box API）、这台电脑上的其他无界面 Throne 和 TUN 占用者、服务管理器和重启模式，以及[设备 ID](@/headless/_index.zh.md#device-id)。

只有会让 Throne 完全无法工作的问题才标记为 `[FAIL]`，此时该命令以退出码 1 退出。缺少 TUN 或 Kill Switch 所需的权限会标记为 `[WARN]`，并附上用于修复的 `setcap` 或 `chmod u+s` 命令；在容器中则附上 `--cap-add NET_ADMIN` 和 `--device /dev/net/tun`。

## Throne --health {#health}

`Throne --health` 通过实例套接字询问正在运行的 Throne，并打印一行 JSON。请以 Throne 的用户身份、针对同一个数据目录运行它：

```bash
$ sudo /opt/Throne/Throne --health
{"api":"listening","core_restarts":0,"degraded":null,"headless_dialogs":0,"ok":true,"previous_crash":false,"previous_exit":{"at":1760700000,"code":75,"reason":"restart requested"},"ready":true,"state":"running","stuck_s":0}
```

Throne 健康时，它以退出码 0 退出。其他退出码请参见[退出码](@/headless/command_line.zh.md#exit-codes)。

| 字段 | 含义 |
| --- | --- |
| `ok` | Throne 工作正常：已完成启动、核心已连接、没有卡住的操作、核心没有被放弃，并且 Kill Switch 处于关闭状态或正常工作。按当前设置无法工作的 Kill Switch，或者被 `--no-kill-switch` 关闭的 Kill Switch，会让它保持为 `true`，因为重启无法解决这些问题。它从不取决于远程服务器或正在运行的配置档，因此在它为 `false` 时重启 Throne，不会在服务器故障期间陷入循环。 |
| `ready` | Throne 已完成启动。 |
| `state` | `idle`、`connecting`、`running`、`stopping`；在 Throne 完成启动之前为 `starting`。 |
| `degraded` | `null`，或者 Throne 无法按设置工作的原因。参见下表。 |
| `stuck_s` | 某个配置档在连接中超出最初 90 秒的秒数，或在停止中超出最初 45 秒的秒数；否则为 0。只要它大于 0，`ok` 就为 `false`。 |
| `core_restarts` | 核心被重启的次数。 |
| `headless_dialogs` | 因为没有窗口而跳过的询问。它应保持为 0。日志会在 `HEADLESS-DIALOG` 行中列出它们。 |
| `previous_crash` | 上一次运行没有正常结束：崩溃、`kill -9` 或断电。 |
| `previous_exit` | 上一次运行是如何结束的，格式为 `{code, reason, at}`（`at` 是自 1970 年起的秒数），或者为 `null`。在服务管理器重启 Throne 之后（退出码 75、70、71），原因会保留在这里。 |
| `api` | API 监听器：`off`、`listening`、`key_invalid`、`failed`、`retrying`（最多等待 30 秒，等其地址出现）或 `address_missing`（其地址已从所有网卡上消失）。 |

在刚开始启动的片刻，这一行只包含 `ok`、`ready`、`state` 和 `headless_dialogs`。

`degraded` 的取值如下。当多个值同时适用时，Throne 按以下顺序报告第一个：

| 值 | 含义 |
| --- | --- |
| `core_gave_up` | 核心反复失败，Throne 已放弃它。Throne 会以退出码 70 退出，交给服务管理器处理；或者在连续三次这样的启动之后，[保持运行](@/headless/recovery.zh.md#protection)，并每 5 分钟重试一次核心。 |
| `core_unavailable` | 核心进程没有运行。 |
| `kill_switch_failed` | Kill Switch 已开启，但失败了。配置档会被拒绝。参见 [Kill Switch](@/advanced/kill_switch.zh.md)。 |
| `api_unavailable` | API 已开启，但没有在监听，例如因为另一个程序占用了其端口，或者其密钥文件无法使用。`ok` 保持为 `true`。 |
| `tun_unavailable` | Throne 上次停止时 TUN 处于开启状态，而现在 Throne 无法开启它：缺少权限，或者有其他东西占用了 TUN（[TUN 冲突](@/headless/_index.zh.md#beside-desktop)）。Throne 没有在不开启 TUN 的情况下启动该配置档。`thronectl tun off` 可以清除此状态；然后用 `thronectl connect` 启动配置档。 |
| `resume_suppressed` | Throne 没有恢复上次的配置档，因为在最近三次恢复中，每一次 Throne 或其核心都在一分钟内停止了。请用 `thronectl connect` 启动该配置档；它运行满一分钟后，此状态会清除。 |
| `vpn_auth_failed` | VPN 配置档的服务器拒绝了其已保存的凭据。该配置档停止时，此状态会清除。 |
| `vpn_challenge_pending` | VPN 配置档的服务器要求提供 Throne 无法自行回答的内容，例如网页登录。Throne 会在该询问过期时将其取消，最长 5 分钟。 |

[API 规范](https://github.com/throneproj/Throne-api/blob/main/spec/api.md#headless-throne)详细描述了这些值。

Docker 镜像使用 `Throne --health` 作为健康检查。需要更多信息的监控脚本可以向数据目录中的套接字 `config/.instance` 发送一行 `HEALTH`：

```bash
echo HEALTH | sudo socat -t 3 - UNIX-CONNECT:/var/lib/throne/config/.instance
```

回答中还会包含 `mode`、`pid`、`uptime_s`、`version`、`tun_running`、完整的 `api` 块以及 `thronectl status` 的各个字段。如果数据目录的路径长度达到或超过 100 字节，或者其文件系统不支持套接字，该套接字会移到 `headless-<hash>`：对 root 而言位于 `/run/throne`（macOS 上为 `/var/run/throne`）中，对其他用户而言位于 `/tmp/throne-<uid>` 中。在 Windows 上，请使用 `--health`。

## systemd：就绪、状态与看门狗 {#systemd}

随附的单元为 `Type=notify`。Throne 从其主进程向 systemd 报告：

- **`READY=1`**：在它已持有数据目录、数据库已打开、API 已在监听（或已失败）、核心已连接、Kill Switch 的状态已确定，并且恢复的配置档正在启动时发送。这通常不到 20 秒。在此之前，Throne 会延长启动超时，因此 `TimeoutStartSec=90` 只会终止卡住的启动。三次启动都没有可用的核心之后，它无论如何都会报告就绪。
- **`STATUS=`**：`systemctl status` 会显示它：`Starting`、`Starting core`、`Core restarting 2/5`、`Idle`、`Connecting <profile>`、`Connected <profile>`（TUN 开启时带有 ` (Tun)`）、`Stopping <profile>`、`Degraded: <reason>`、`Stopping` 和 `Restarting`。
- **`WATCHDOG=1`**：主循环运行期间每 20 秒发送一次（`WatchdogSec=60` 的三分之一）。如果主循环卡住，systemd 会发送 `SIGABRT` 并再次启动 Throne。
- **`STOPPING=1`**：开始退出时发送；或者在原地重启（`--restart-mode exec`）之前发送 `RELOADING=1`。

无论有没有 systemd，Throne 都会监视自己的运行进度：配置档处于连接中达 180 秒或处于停止中达 90 秒，会让它以退出码 71 退出；核心在 60 秒内一直不可用，会让它以退出码 70 退出。之后由服务管理器再次启动它。

必须使用 `KillMode=mixed`。这样，systemd 只向 Throne 发送 `SIGTERM`，Throne 会依次停止其核心和 Kill Switch，然后退出，通常在几秒钟内完成（`TimeoutStopSec=45`）。第二个 `SIGTERM` 或 `SIGINT` 会立即杀死核心。不要使用 `systemctl kill`：它会直接向核心和 Kill Switch 辅助程序发送信号。

## 日志 {#logs}

Throne 会把日志写到标准错误输出，以及数据目录中的 `config/logs/throne.log`。在哪里查看日志：

| Throne 的运行方式 | 日志 |
| --- | --- |
| systemd 系统单元 | `journalctl -u throne -f` |
| systemd 用户单元 | `journalctl --user -u throne -f` |
| Docker | `docker compose logs -f throne` |
| macOS LaunchDaemon | `/Library/Logs/Throne/throne.log` |
| Windows 服务 | `C:\ProgramData\Throne\config\logs\throne.log`（服务没有标准错误输出） |

无界面 Throne 的日志使用英文。`--debug` 会添加调试行。`--log-format` 设置标准错误输出的格式：

| 格式 | 行 |
| --- | --- |
| `auto` | 标准错误输出发往 systemd 日志（journal）时为 `journal`，否则为 `plain` |
| `journal` | 每行以 `<4>` 这样的 syslog 优先级开头，journald 会将其转换为该消息的优先级。时间由 journald 添加。 |
| `plain` | 每行以本地时间开头。 |

值得搜索的日志行：

- `EXIT <code>: <reason>`：Throne 退出的原因。参见[退出码](@/headless/command_line.zh.md#exit-codes)。
- `Ready <n> ms after launch`：启动已完成。
- `[API] Listening on …`：API 的监听位置。
- `[Resume] …`：上次的配置档是否已再次启动。
- `[Kill switch] Not active (<code>): …`：Kill Switch 无法工作的原因。
- `[Watchdog] …`：Throne 自身的进度检查。
- `HEADLESS-DIALOG`：一个无人能回答的询问。

当某次运行没有正常结束时，它的日志会保存为 `config/logs/crashed-<time>.log`，崩溃报告则保存到 `config/crashes/`。
