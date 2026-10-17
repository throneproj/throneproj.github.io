+++
title = "防锁定与恢复"
description = "无界面 Throne 如何让 API 始终可以访问，以及当 Kill Switch 或 TUN 等已保存的设置把你锁在外面时，如何重新获得访问。"
weight = 50
toc = true
+++

没有屏幕的设备必须保持可访问：如果某项设置切断了它的连接，你可能没有键盘可以用来修复。无界面 Throne 的设计目标是让 Throne API 始终可以访问；对于已保存的设置仍然把你锁在外面的情况，它还提供了一种恢复启动方式。

## Throne 如何保持可访问 {#protection}

**API 始终可用。**

- 从首次启动起，API 就在 `127.0.0.1:9095` 上开启，并使用生成的密钥。
- `--api-*` 选项和变量会在每次启动时覆盖已保存的 API 设置，因此错误的已保存监听器可以通过命令行修正。参见[选项与变量](@/headless/command_line.zh.md#options)。
- 从备份恢复设置时，会保留本设备的 API、入站、TUN 和 Kill Switch 设置。
- 空的 `api.key`（首次启动被中断时会留下这样的文件）会获得一个新密钥。其他任何无法使用的密钥文件都会让 API 保持关闭；删除它，Throne 就会在下次启动时创建新密钥。

**API 的端口。**

- 当另一个程序占用了默认或已保存的 API 端口时，Throne 会在没有 API 的情况下继续运行（`degraded` 为 `api_unavailable`），并每 30 秒重试一次。
- 当另一个 Throne 的 API 占用了该端口时，Throne 会记录这一情况，并且不去动它。请用 `--api-listen PORT` 为这个 Throne 指定另一个端口。
- 而用 `--api-listen` 指定的监听器如果无法监听，会让 Throne 以退出码 78 退出，以便你注意到。如果其地址尚未出现在这台电脑上，Throne 最多等待 30 秒，然后以退出码 1 退出。

**登录失败。** 同一地址在一分钟内认证失败 5 次后，Throne 会在 60 秒内拒绝该地址，并记录到日志中。它从不拒绝环回地址，也不拒绝在过去 10 分钟内有客户端成功认证过的地址。

**Kill Switch 与 TUN。**

- [Kill Switch](@/advanced/kill_switch.zh.md) 始终放行环回流量。对于监听其他地址的 API 监听器，它会放行来自 API 端口的回复（Linux、macOS 和 Windows）。
- 当核心无法使用 Kill Switch 的组（GID 1950896719）时，例如在缺少 `CAP_SETGID` 或该 GID 的 rootless Docker 或其他使用用户命名空间的容器中，核心会以退出码 86 退出。Throne 不会将其计为崩溃：它会在不使用该组的情况下运行核心，Kill Switch 以代码 `unsupported` 进入失败即关闭（fail closed）状态并继续阻断流量，配置档会被拒绝（`kill_switch_inactive`），直到你关闭 `kill_switch` 设置。
- 在 Linux 上，如果 API 监听网络地址时启动 TUN，而远程客户端可能会失去对 API 的访问，Throne 会警告一次：除非开启了 `tun_auto_redirect`，否则发往被绕过地址范围之外的客户端的回复会进入隧道；而开启严格路由但未开启 `tun_ipv6` 时，IPv6 客户端会被丢弃。

**导致 Throne 崩溃的配置档。** 如果在最近三次启动中，每一次 Throne 或其核心都在恢复同一个配置档后一分钟内停止，Throne 就不会再恢复它（`resume_suppressed`）。请用 `thronectl connect` 手动启动它一次。它运行满一分钟后，此状态会清除。

**反复失败的核心。** 如果连续三次启动中核心都没有保持连接满一分钟，Throne 就不再以退出码 70 或 71 退出。它会带着 API 保持运行（`degraded` 为 `core_gave_up`），并每 5 分钟重试一次核心，直到某个核心保持连接满一分钟。

## 恢复访问 {#recovery}

如果已保存的设置仍然把你锁在外面，例如 Kill Switch 中断了你的 SSH 会话，或者 TUN 截走了 API 的回复，请用 `--no-resume --no-kill-switch`（或变量 `THRONE_RESUME=0` 和 `THRONE_KILL_SWITCH=0`）启动 Throne 一次：

- 不会启动任何配置档；
- 本次运行中 Kill Switch 保持关闭（在 `kill_switch` 设置关闭之前，配置档仍会被拒绝）；并且
- 同一设备上的 `thronectl` 可以修正设置。

然后修正把你锁在外面的设置，例如使用 `thronectl settings set kill_switch=false` 或 `thronectl tun off`，再正常启动 Throne。

### systemd {#recovery-systemd}

```bash
printf 'THRONE_RESUME=0\nTHRONE_KILL_SWITCH=0\n' | sudo tee -a /etc/throne/throne.env >/dev/null
sudo systemctl restart throne
thronectl settings set kill_switch=false        # 或：thronectl tun off
# 再从 /etc/throne/throne.env 中删除这两行，然后：
sudo systemctl restart throne
```

### Docker {#recovery-docker}

在 `compose.yaml` 的 `environment:` 下添加这两个变量，然后运行 `docker compose up -d`：

```yaml
    environment:
      THRONE_RESUME: "0"
      THRONE_KILL_SWITCH: "0"
```

用 `docker compose exec throne thronectl …` 修正设置，再删除这两个变量，然后运行 `docker compose up -d`。

### macOS {#recovery-macos}

把这两个变量添加到 plist 的 `EnvironmentVariables` 中，然后重新加载它：

```bash
sudo launchctl bootout system/moe.Throne.headless
sudo launchctl bootstrap system /Library/LaunchDaemons/moe.Throne.headless.plist
```

用 `thronectl` 修正设置，删除这两个变量，然后用同样的方法重新加载 plist。

### Windows 服务 {#recovery-windows}

1. 停止服务：`sc.exe stop Throne`。
2. 在以管理员身份运行的命令行窗口中，针对同一个数据目录手动启动 Throne：

   ```bat
   start "" /wait "C:\Program Files\Throne\Throne.exe" --headless --data-dir C:\ProgramData\Throne --no-resume --no-kill-switch
   ```

3. 在另一个以管理员身份运行的命令行窗口中用 `thronectl` 修正设置（参见[在命令行窗口中运行命令](@/headless/installation.zh.md#windows-prompt)）。
4. 用 `Ctrl+C` 停止 Throne，然后再次启动服务：`sc.exe start Throne`。

### 从头开始 {#start-over}

如果其他方法都无效，请停止 Throne，并把它的数据目录移到别处（对于系统单元，即 `/var/lib/throne`）。下次启动时会创建一个新的空数据目录和新的 API 密钥。请从[备份](@/headless/thronectl.zh.md#from-desktop)中恢复你的配置档。
