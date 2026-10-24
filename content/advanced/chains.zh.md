+++
title = "代理链与自定义配置"
description = "串联多个配置档、为分组添加前置与落地代理、编写原始 sing-box 或 Xray JSON，以及将其他代理程序作为额外核心运行。"
weight = 20
toc = true
+++

当一台服务器不够用，或者某个配置档需要普通编辑器中没有的选项时，请参考本页。内容包括代理链、分组的前置与落地代理、自定义 JSON 配置以及额外核心（Extra Core）配置档。

在简洁模式下，`新建配置档`（New profile）不提供 `链式代理`（Chain Proxy）、各种 `自定义`（Custom）类型和 `额外核心`（Extra Core），分组编辑器也会隐藏 `前置代理`（Front Proxy）和 `落地代理`（Landing Proxy）（仅在高级模式下显示，参见[简洁模式与高级模式](@/get_started/configuration.zh.md#interface-mode)）。已有的配置档和分组设置仍然有效。

## 代理链 {#chains}

代理链配置档让你的流量依次经过多个配置档。每台服务器只能看到它前面的那台服务器，由最后一台服务器连接网站。

### 创建代理链 {#create-chain}

1. 打开 `程序`（Program）→ `新建配置档`（New profile），快捷键 `Ctrl+N`。
2. 将 `类型`（Type）设为 `链式代理`（Chain Proxy），并填写 `名称`（Name）。
3. 点击 `选择配置档`（Select Profile）。编辑器会隐藏，主窗口切换到选择模式。
4. 双击作为下一跳的配置档，或选中它后按 `Enter`。编辑器会重新出现，并已添加该配置档。
5. 为每个跳点重复第 3 步和第 4 步。
6. 拖动各行，将它们排成正确的顺序。每行上的按钮可替换或移除该跳点。
7. 点击 `确定`（OK）。

只有选中一个配置档后，选择模式才会结束。如果选错了，请用该行上的按钮将其移除。

### 跳点顺序 {#hop-order}

编辑器中写着“流量顺序是由上到下 (最底一个为流量的出口)”（Traffic order is from top to bottom）。你的设备首先连接最上面的配置档，流量随后依次经过其下方的每个配置档，最后由最下面的配置档连接网站。网站看到的是最下面那个配置档的地址。

如果 `A` 在最上面、`B` 在它下面，流量路径为：你的设备 → `A` → `B` → 互联网。

### 规则与限制 {#chain-limits}

- 代理链中不能包含另一条代理链。
- 自动选择器不能作为跳点，因为它会自行切换服务器。自动选择器也会跳过代理链配置档。
- `自定义 (sing-box 配置)`（Custom (sing-box config)）配置档不能作为跳点；`自定义 (sing-box 出站)`（Custom (sing-box outbound)）和 `自定义 (Xray 出站)`（Custom (Xray outbound)）配置档可以。
- 一条代理链可以包含一个额外核心配置档，且它必须是最上面的跳点。Throne 的警告中称之为“最后一跳”（final hop），指的是你的设备最先连接的那个跳点。
- 一条代理链可以包含一个 `自定义 (Xray 配置)`（Custom (Xray config)）配置档。它同样必须是最上面的跳点，并且不能与额外核心配置档或其他 Xray 跳点组合使用。
- 所有 Xray 跳点必须相邻：先是 sing-box 跳点，然后是 Xray 跳点，最后是 sing-box 跳点。参见[代理链中的 Xray](@/advanced/xray.zh.md#xray-in-chains)。
- URL 测试会跳过包含额外核心或 `自定义 (Xray 配置)` 配置档的代理链。
- 当某台服务器上方的跳点是 WireGuard、MASQUE、OpenVPN、OpenConnect、Tailscale 或 SOCKS4 配置档时，Throne 会使用直连 DNS 查询该服务器的名称。在 1.3.2 之前，这一查询会经过代理本身，这类代理链可能无法连接。

Throne 会在你添加跳点或保存代理链时检查其中一部分规则，其余规则则在启动时检查。检查失败时，原因会显示在提示消息或日志中。

如果代理链或分组用作跳点的配置档已被删除，该配置档将无法启动。自 1.4.0 起，提示消息会说明需要修改什么：“Chain "…" has a hop (profile id …) that no longer exists, edit the chain to remove it”（代理链中有一个已不存在的跳点，请编辑代理链将其移除），或“Group "…" has a front proxy that has been deleted.”（分组的前置代理已被删除），落地代理（landing proxy）也有相同的提示。

如果代理链中没有额外核心或完整配置类的跳点，它也可以作为路由规则的出站。

## 前置代理与落地代理 {#front-landing}

分组可以在其中每个配置档之前和之后各添加一个跳点。其效果与代理链相同，但无需创建代理链配置档。

1. 右键点击分组标签页，选择 `编辑选定分组`（Edit selected Group）。
2. 选择 `前置代理`（Front Proxy）、`落地代理`（Landing Proxy），或两者都选。输入名称的一部分即可在所有配置档中搜索。选择 `None` 可移除该跳点。
3. 点击 `确定`。

此后流量路径为：你的设备 → `前置代理` → 你启动的配置档 → `落地代理` → 互联网。开启 WARP 时，WARP 位于落地代理之后。

- 当分组中的服务器无法直接访问、但可以通过另一台服务器访问时，前置代理会很有用。
- 落地代理可以让网站始终看到同一个出口服务器，无论你启动的是分组中的哪个配置档。

Throne 会用这些跳点构建一条代理链，因此代理链的限制同样适用。例如，前置代理或落地代理不能是代理链配置档；设置了前置代理的分组无法启动额外核心或 `自定义 (Xray 配置)` 配置档。这些列表中不提供自动选择器。其他分组设置请参见[订阅与分组](@/guides/subscriptions.zh.md#front-landing-proxy)。

## 自定义配置 {#custom-config}

自定义配置档保存的是交给核心的原始 JSON，可用于普通编辑器不提供的选项。通过 `程序` → `新建配置档` 并选择以下类型之一来创建：

| `类型` | 填写的内容 | `类型` 列 |
| --- | --- | --- |
| `自定义 (sing-box 出站)` | 一个 sing-box 出站或端点（endpoint） | `Custom … Outbound` |
| `自定义 (sing-box 配置)` | 一份完整的 sing-box 配置 | `Custom Config` |
| `自定义 (Xray 出站)` | 一个 Xray 出站 | `Custom Xray … Outbound` |
| `自定义 (Xray 配置)` | 一份完整的 Xray 配置 | `Custom Xray Config` |

`JSON 编辑器`（Json Editor）会在更大的窗口中打开 JSON。对于两种 sing-box 类型，它会按照 sing-box 的 schema 检查 JSON 并列出问题。`格式化`（Format）用于整理文本格式。

一个最简的 `自定义 (sing-box 出站)` 示例：

```json
{
  "type": "socks",
  "server": "203.0.113.10",
  "server_port": 1080
}
```

如果想从 Throne 为某个可用的配置档或代理链生成的 JSON 开始编写，请右键点击它 → `分享`（Share）→ `导出配置`（Export config）（自 1.4.0 起，仅在高级模式下显示）。窗口会在不同的标签页上分别显示 sing-box 配置，以及配置档使用 Xray 时的 Xray 配置。`复制`（Copy）会复制你当前看到的标签页。

导入 JSON 时：

- 包含 `outbounds` 或 `endpoints` 的 sing-box 配置会被拆分，每个受支持的出站成为一个普通配置档。单个 sing-box 出站对象会成为 `自定义 (sing-box 出站)`。
- 在 Xray JSON 中，VLESS 出站会成为 `VLESS (Xray)`，其他出站会成为 `自定义 (Xray 出站)`。由完整 Xray 配置组成的 JSON 列表中，每份配置都会成为一个 `自定义 (Xray 配置)`；Throne 会移除它们的入站并添加自己的入站。
- 任何导入都不会生成 `自定义 (sing-box 配置)`，这种类型只能手动创建。

### 完整配置 {#full-configs}

- **`自定义 (sing-box 配置)`：** Throne 会完全按原样启动你的配置，不会添加它自己的入站、TUN、路由配置档、DNS 设置、WARP 或前置与落地代理。你的配置必须自带入站。
- **`自定义 (Xray 配置)`：** Throne 会在你的配置中添加一个本地 SOCKS 入站，并在它前面接入 sing-box。TUN 模式、路由配置档和 DNS 设置依然生效。在 Xray 内部，由你的配置自身的 `routing` 选择出站。

完整配置不能作为路由规则的出站，也不能作为路由配置档的端点。自动选择器可以使用 `自定义 (Xray 配置)` 配置档（每个都在各自的 Xray 实例中运行），但会跳过 `自定义 (sing-box 配置)` 配置档。

## 额外核心 {#extra-core}

额外核心配置档会在你的电脑上启动另一个代理程序，并把流量发送给它，可用于 Throne 不支持的协议。该程序必须开启一个本地 SOCKS 服务器，Throne 会像连接任何 SOCKS 代理一样连接它。额外核心仅在桌面版中提供。

1. 打开 `程序` → `新建配置档`。
2. 将 `类型` 设为 `额外核心`（Extra Core）。
3. 填写下列字段。
4. 点击 `确定` 并启动该配置档。

| 字段 | 作用 |
| --- | --- |
| `核心路径`（Core path） | 要运行的程序。用 `从文件中选择`（Choose from file）来选择它；Throne 会记住你之前选择过的路径。 |
| `参数`（Args） | 命令行参数。Throne 会把 `%s` 替换为一个临时文件的路径，该文件保存 `配置`（Config）中的文本。与在 shell 中一样，包含空格的值需要加引号。 |
| `配置`（Config） | 该程序配置文件的内容。只有当 `参数` 中包含 `%s` 时，它才会传递给程序。 |
| `Socks 地址`（Socks address） | 该程序 SOCKS 服务器的地址，默认为 `127.0.0.1`。 |
| `Socks 端口`（Socks port） | 该程序 SOCKS 服务器的端口。它必须与程序的配置一致，并且不能是 Throne 自身的监听端口。 |
| `无日志`（No logs） | 不在 `日志`（Logs）标签页中显示该程序的输出。 |

例如，如果该程序通过 `-c <file>` 读取配置，就将 `参数` 设为 `-c %s`，并把配置粘贴到 `配置` 中。

运行方式：

- 启动该配置档时，Throne 会启动该程序；停止配置档时，程序也随之停止，临时配置文件随后被删除。
- 除非勾选了 `无日志`，否则程序的输出会显示在 `日志` 标签页中包含 `Extra Core:` 的行里。
- 如果程序自行退出，Throne 会停止该配置档，并显示“Extra Core exited, stopping profile...”（额外核心已退出，正在停止配置档）。
- 即使 Throne 的核心为了 TUN 模式拥有管理员或 root 权限，该程序也以普通用户权限运行。

额外核心配置档不能作为路由规则的出站。在代理链中，它必须是最上面的跳点。URL 测试和自动选择器会跳过它。

## Android 版 {#android}

- 代理链的用法相同：`添加服务器配置`（Add profile）→ `手动输入`（Manual settings）→ `链式代理`（Proxy chain）。最上面一行是你的设备最先连接的服务器，最下面一行是出口。限制也相同。
- 分组同样有 `前置代理`（Front proxy）和 `落地代理`（Landing proxy）选项。
- `自定义配置`（Custom config）同样有四种类型（`配置类型`，Config type），JSON 编辑器也会按 sing-box schema 进行检查。
- 额外核心配置档仅限桌面版。如果桌面版备份中包含此类配置档，Android 会保留它，但无法启动。
