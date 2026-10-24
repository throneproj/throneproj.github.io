+++
title = "命令行与数据目录"
description = "无界面 Throne 的所有选项和环境变量、它存放数据的位置、它的重启方式，以及各个退出码的含义。"
weight = 30
toc = true
+++

本页列出无界面 Throne 的选项和环境变量、它存放数据的位置、它的重启方式以及其退出码的含义。桌面版的命令行选项请参见[命令行](@/reference/files.zh.md#command-line)。

## 选项与变量 {#options}

`Throne --headless --help` 会列出所有选项。一个或两个短横线都可以（`-data-dir` 与 `--data-dir` 相同），值跟在空格或 `=` 之后。选项优先于对应的变量。设为空值的变量视为未设置，`THRONE_API_ALLOW` 除外。

| 选项 | 变量 | 作用 |
| --- | --- | --- |
| `--headless` | `THRONE_HEADLESS=1` | 不带窗口运行。该变量除空值、`0`、`false`、`no` 和 `off` 以外的任何值都会开启它。 |
| `--data-dir DIR`（`-appdata DIR`） | `THRONE_DATA_DIR` | [数据目录](#data-dir)。 |
| `--restart-mode MODE` | `THRONE_RESTART_MODE` | `auto`（默认）、`exit` 或 `exec`。参见[重启模式](#restart-modes)。 |
| `--no-resume` | `THRONE_RESUME=0` | 启动时不启动上次的配置档。 |
| `--no-kill-switch` | `THRONE_KILL_SWITCH=0` | 即使 `kill_switch` 设置处于开启状态，本次运行也让 [Kill Switch](@/advanced/kill_switch.zh.md) 保持关闭。在该设置关闭之前，配置档仍会被拒绝。用于[恢复访问](@/headless/recovery.zh.md#recovery)。 |
| `--log-format FORMAT` | `THRONE_LOG_FORMAT` | `auto`（默认）、`journal` 或 `plain`。参见[日志](@/headless/monitoring.zh.md#logs)。 |
| `--api-listen LISTEN` | `THRONE_API_LISTEN` | Throne API 的监听位置：`PORT`（在 `127.0.0.1` 上）、`IPv4:PORT`、`[IPv6]:PORT`、`*:PORT`（所有地址）或 `off`。默认：`127.0.0.1:9095`，除非已保存的设置开启了 API。 |
| `--api-key-file FILE` | `THRONE_API_KEY_FILE` | 从这个文件读取 API 密钥，该文件必须存在。`thronectl keygen -o FILE` 可以生成一个。默认：数据目录中的 `config/api.key`，首次启动时创建。 |
| `--api-admin-lan` | `THRONE_API_ADMIN_LAN=1` | 也响应来自网络的[管理请求](@/headless/thronectl.zh.md#admin-requests)（导入、设置、备份、重启），而不仅仅是来自本设备的。 |
| `--api-allow LIST` | `THRONE_API_ALLOW` | 可以使用非环回监听器的地址和子网，以逗号或空格分隔。空列表会以退出码 64 退出。不设置该变量即允许所有地址。 |
| `--debug` | | 调试日志。 |
| `--service` | | 仅限 Windows：在服务控制管理器下运行，即使没有 `--headless` 也以无界面方式运行。以其他任何方式启动时，会以退出码 64 退出。 |
| `--health` | | 询问正在运行的 Throne 状态如何。参见 [Throne --health](@/headless/monitoring.zh.md#health)。 |
| `--print-connection` | | 为 `thronectl` 打印 `THRONE_ADDR` 和 `THRONE_KEY_FILE`。参见[将 thronectl 连接到 Throne](@/headless/thronectl.zh.md#connect)。 |
| `--check` | | 检查这台电脑能否运行无界面 Throne。参见 [Throne --check](@/headless/monitoring.zh.md#check)。 |
| `--help`、`--version` | | 打印选项或版本。 |

- 是/否类变量接受 `1`、`true`、`yes`、`on`、`0`、`false`、`no` 或 `off`。其他任何值都会以退出码 64 退出。
- `--api-*` 选项和变量会在每次启动时覆盖已保存的 API 设置，并且从不保存。这样，错误的已保存 API 设置总能通过命令行修正。
- `--health`、`--print-connection` 和 `--check` 不需要 `--headless` 也能使用。一次只能使用其中一个，并且不能与 `--service` 一起使用。
- 在命令行中传入链接或文件时，会以退出码 64 退出。请改用 [`thronectl import`](@/headless/thronectl.zh.md#profiles) 导入它。

使用 systemd 单元时，请在 `/etc/throne/throne.env` 中设置变量，用 drop-in 文件设置选项。参见 [Debian、Ubuntu、Raspberry Pi OS、Fedora、openSUSE](@/headless/installation.zh.md#linux-packages)。

## 数据目录 {#data-dir}

无界面 Throne 使用以下各项中第一个适用的：

1. `--data-dir`，然后是 `THRONE_DATA_DIR`。相对路径从 Throne 启动时所在的文件夹算起。
2. `STATE_DIRECTORY`，systemd 会为 `StateDirectory=` 设置它。
3. 以 root 身份运行时：Linux 上为 `/var/lib/throne`，macOS 上为 `/Library/Application Support/Throne`。在 Windows 上，使用 `--service` 或以 LocalSystem 身份运行时：`C:\ProgramData\Throne`。
4. 用户的配置文件夹，桌面版也使用它：Linux 上为 `~/.config/Throne`，macOS 上为 `~/Library/Preferences/Throne`，Windows 上为 `%LOCALAPPDATA%\Throne`。在 Linux 和 macOS 上，如果没有 `HOME`，Throne 会以退出码 78 退出；请用 `--data-dir` 指定目录。

无界面 Throne 从不像便携版桌面安装那样把数据保存在程序旁边。如果想共用这种安装的数据，请用 `--data-dir` 传入程序所在的文件夹。

在 Linux 和 macOS 上，它会把缺失的目录创建为只有其用户可以读取。以 root 身份运行时，它会拒绝其他用户可以写入的数据目录（退出码 78），因为设置中指定了 Throne 会启动的程序。在 Windows 上，`C:\ProgramData\Throne` 只供 SYSTEM 和 Administrators 使用（参见[数据文件夹](@/headless/installation.zh.md#windows-data-folder)）；普通用户可以写入的其他目录只会在日志中产生一条警告。

其中的内容：

| 路径 | 内容 |
| --- | --- |
| `config/throne.db` | 配置档、分组、路由配置档和设置，与桌面版相同 |
| `config/api.key` | API 密钥，只有 Throne 的用户可以读取 |
| `config/logs/throne.log` | 本次运行的日志。`crashed-<time>.log` 保存未正常结束的那次运行的日志。 |
| `config/crashes/` | 崩溃报告 |
| `config/headless-state.json` | 用于恢复配置档和统计崩溃的计数器，以及上次运行是如何结束的 |
| `config/hwid` | 系统没有设备 ID 时使用的[设备 ID](@/headless/_index.zh.md#device-id) |
| `config/.lock`、`config/.instance` | 数据目录的锁，以及 `--health` 询问的套接字。在 Windows 上，实例是一个命名管道，而不是文件。 |
| `web/` | 仅限 Docker 镜像：[Web 界面](@/headless/web.zh.md#docker)的密码哈希和 TLS 证书 |

## 重启模式 {#restart-modes}

`thronectl restart`、恢复备份和 `SIGHUP` 信号都会重启 Throne。`--restart-mode` 决定重启的方式：

| 模式 | 会发生什么 |
| --- | --- |
| `exit` | Throne 以退出码 75 退出，由服务管理器再次启动它。 |
| `exec` | Throne 在同一个进程中重新启动（Linux 和 macOS；进程 ID 保持不变）。在 Windows 上，它会启动一个新的 Throne 进程，并以退出码 0 退出。Windows 服务始终使用 `exit`。 |
| `auto` | 当 Throne 由 systemd（其通知套接字或用户管理器）、launchd 或容器的 init 启动，或者作为 Windows 服务运行时，使用 `exit`。否则使用 `exec`，例如从终端启动时。 |

随附的单元、plist 和 Docker 镜像需要 `auto` 或 `exit`。`Throne --check` 会显示 `auto` 选择了哪种模式。在终端中运行时，关闭终端（挂断）会让 Throne 以退出码 0 停止，而不是重启它。

## 退出码 {#exit-codes}

Throne 在退出之前会向日志写入 `EXIT <code>: <reason>`。随附的服务文件对每个退出码的处理方式如下：

| 退出码 | 含义 | systemd 单元 | Docker `unless-stopped` | launchd plist | Windows 服务 |
| --- | --- | --- | --- | --- | --- |
| 0 | 已停止：`SIGTERM`、`SIGINT`、`thronectl shutdown`；在 Windows 上还包括服务停止、`Ctrl+C`、关闭控制台、注销或不带 `/F` 的 `taskkill`。也包括在 Windows 上于服务之外进行的重启，此时它已经启动了一个新的 Throne。 | 保持停止 | 再次启动，除非使用了 `docker stop` | 保持停止 | 保持停止 |
| 1 | 启动因可能会自行消失的原因而失败：锁、实例套接字、数据库、核心的 IPC 监听器，或者 `--api-listen` 地址在 30 秒内没有出现 | 3 秒后再次启动 | 再次启动 | 10 秒后再次启动 | 恢复操作 |
| 3 | 另一个 Throne 正在使用该数据目录 | 保持停止 | 再次启动 | 每 10 秒重试一次 | 恢复操作 |
| 64 | 错误的选项、选项值或变量，或者 `--service` 不是由服务控制管理器启动的 | 保持停止 | 再次启动 | 每 10 秒重试一次 | 恢复操作 |
| 70 | 核心反复失败，Throne 已放弃它，或者核心在 60 秒内一直不可用 | 再次启动 | 再次启动 | 再次启动 | 恢复操作 |
| 71 | 某个配置档处于连接中的状态达 180 秒，或处于停止中的状态达 90 秒 | 再次启动 | 再次启动 | 再次启动 | 恢复操作 |
| 75 | 请求了重启，且使用 `--restart-mode exit` 或作为 Windows 服务运行；或者 `exec` 重启无法进行 | 再次启动 | 再次启动 | 再次启动 | 恢复操作 |
| 78 | 配置错误：数据目录（也包括没有可用来找到它的 `HOME`，或者在 Windows 上 `C:\ProgramData\Throne` 属于其他用户、允许其他用户写入或者是一个链接）、API 密钥文件、`--api-listen` 监听器，或者无法使用的数据库文件 | 保持停止 | 再次启动 | 每 10 秒重试一次 | 恢复操作 |

“恢复操作”指 Windows 服务的恢复操作：参见 [Windows 服务](@/headless/installation.zh.md#windows)。

- systemd 单元没有启动次数限制（`StartLimitIntervalSec=0`）。每次 `thronectl restart`、恢复和 `SIGHUP` 都是一次新的启动，如果有限制，Throne 可能会停在停止状态，并且没有 API 可用。
- 连续重启时，Docker 每次等待的时间会越来越长。
- 连续三次启动都没有可用的核心之后，Throne 不再以退出码 70 和 71 退出，而是[保持运行](@/headless/recovery.zh.md#protection)。
- 对于与数据库相关的退出码 78，日志会说明该怎么做：把损坏的 `config/throne.db` 连同它的 `-wal` 和 `-shm` 文件一起移到别处，或者放回一份副本。让只读文件可被 Throne 的用户写入。

检查类命令有各自的退出码：

| 命令 | 0 | 1 | 2 | 64 |
| --- | --- | --- | --- | --- |
| `--health` | 健康 | 不健康，或仍在启动中 | 没有 Throne 回应，或者 Windows 服务拒绝了未以管理员身份运行的命令行窗口 | 错误的选项 |
| `--check` | 没有 `[FAIL]` 行 | 有 `[FAIL]` 行 | | 错误的选项 |
| `--print-connection` | 已打印两行 | | API 已关闭或未在监听，或者其密钥不在文件中；或者 Windows 服务拒绝了该命令行窗口 | 错误的选项 |

当 `--health` 和 `--print-connection` 找不到数据目录（没有 `HOME`）时，会以退出码 78 退出；请用 `--data-dir` 指定它。
