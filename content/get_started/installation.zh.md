+++
title = "安装"
description = "如何安装 Throne 并开始使用。"
weight = 1
toc = true
+++

Throne 支持 Windows、Linux 和 macOS。请根据您的平台选择合适的安装方式。

## 下载二进制文件

前往[下载](@/downloads.zh.md)适合您平台的文件。

### Windows

#### 便携版 (ZIP)

解压 ZIP 文件并运行 `Throne.exe`。

#### 安装版 (.exe)

运行 `Throne-x.x.x-universal-installer.exe`。

### macOS

解压 ZIP 文件。由于 Apple 严格的安全策略，您必须移除隔离属性：

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

首次启动前，请将 `Throne.app` 移动到 `/Applications`。内置提权功能会打开“终端”以将核心设置为 setuid-root，如果应用仍位于 `~/Downloads` 中，该步骤可能会失败。

### Linux

#### 命令行安装器（推荐）

在任意发行版上最快捷的安装方式。脚本会下载适配你的架构的构建版本，将其安装到 `/opt/Throne`，并添加桌面快捷方式：

```bash
curl -fsSL https://raw.githubusercontent.com/throneproj/Throne/dev/script/install_linux.py | sudo python3
```

它以交互式终端菜单运行：先显示最新的稳定版和非稳定版（以及你已安装的版本，如果有的话），然后询问你要执行 **Install** 还是 **Uninstall**，以及安装哪个分支。需要 Python 3 和 root 权限。

再次运行同一条命令即可更新到新版本或卸载。卸载会移除 `/opt/Throne` 和桌面快捷方式，但会保留 `~/.config/Throne` 中的设置。

#### 便携版 (ZIP)

下载 ZIP 包：

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

#### Debian/Ubuntu (.deb)

```bash
sudo dpkg -i Throne-x.x.x-debian-*.deb
```

注意：`-system-qt` 版本不捆绑 Qt 库，而是依赖于系统安装的库。如果主题冲突或 GUI 无法加载，请使用此版本。

## 包管理器

根据你所使用的发行版，Throne 提供多种安装方式。

### WinGet

```bash
winget install -e --id Throneproj.Throne
```

### Scoop

```bash
scoop bucket add extras
scoop install extras/throne
```

### Fedora/RHEL9+

```bash
sudo curl -o /etc/yum.repos.d/throne.repo https://parhelia512.github.io/throne.repo
sudo dnf install -y throne --refresh
```
对于旧版本的 RHEL，请访问 [Throne RPM 软件源](https://parhelia512.github.io/).

### openSUSE/SLES
```bash
sudo zypper addrepo -fc https://parhelia512.github.io/throne-sle.repo
sudo zypper install -y throne
```

### Arch Linux (AUR)

Throne 已上架 **Arch 用户软件仓库**， 包名为 `throne`。 你可以使用你偏好的 AUR 助手来进行安装。

```bash
# 如果你使用的是 yay
yay -S throne

# 如果你使用的是 paru
paru -S throne
```

### NixOS

将以下 Nix 代码添加到你的 NixOS 配置中。

```nix
programs.throne = {
   enable = true;
   # tunMode.enable = true; Add this line to enable tun mode
};
```

### Nix

你也可以在任何支持的 Linux 发行版上，使用 Nix 包管理器来安装 Throne。

```bash
nix-env -iA nixos.throne
```
或者，你可以使用 nix-shell 在不安装的情况下直接试用它。
```bash
nix-shell -p throne
```

## 从源码编译

你也可以从源代码编译安装 Throne。

```bash
git clone --recursive https://github.com/throneproj/Throne.git
cd Throne
mkdir build
cd build
curl -fLso srslist.h "https://raw.githubusercontent.com/throneproj/routeprofiles/rule-set/srslist.h"
cmake ..
make -j$(nproc)
```

## 更新

Throne 具有内置的更新功能。您也可以从 [Releases 页面](https://github.com/throneproj/Throne/releases) 手动下载新版本。

## 故障排除

### 杀毒软件检测

一些杀毒软件可能会将 Throne 标记为恶意软件，因为其更新功能会下载、删除和替换文件——这类似于勒索软件的行为。此外，`系统 DNS` 功能会修改系统的 DNS 设置，某些杀毒应用程序认为这具有危险性。
