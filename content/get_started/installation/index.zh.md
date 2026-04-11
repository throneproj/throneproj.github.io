+++
title = "安装"
description = "如何安装 Throne 并开始使用。"
weight = 1
sort_by = "weight"

[extra]
+++

Throne 支持 Windows、Linux 和 macOS。请根据您的平台选择合适的安装方式。

## 下载二进制文件

前往 [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) 下载适合您平台的文件。

### 版本矩阵

平台 | 架构 | 最低版本要求 | 文件后缀
-- | -- | -- | --
Windows | x64 | Windows 10 | windows64-installer.exe
Windows | x64 | Windows 10 | windows64.zip
Windows | ARM64 | Windows 10 | windows-arm64.zip
Windows | x64 | Windows 7 SP1 | windowslegacy64.zip
Windows | x86 | Windows 7 SP1 | windows32.zip
Linux | x64 | GLIBC 2.34 | linux-amd64.zip
Linux | x64 | GLIBC 2.34 | debian-amd64.deb
Linux | x64 | GLIBC 2.34 | debian-amd64-system-qt.deb
Linux | ARM64 | GLIBC 2.38 | linux-arm64.zip
Linux | ARM64 | GLIBC 2.38 | debian-arm64.deb
Linux | ARM64 | GLIBC 2.34 | debian-arm64-system-qt.deb
macOS | ARM64 | macOS 13 | macos-arm64.zip
macOS | x64 | macOS 13 | macos-amd64.zip
macOS | x64 | macOS 10.15 | macoslegacy-amd64.zip

### Windows

#### 便携版 (ZIP)

解压 ZIP 文件并运行 `Throne.exe`。

#### 安装版 (.exe)

运行 `Throne-x.x.x-windows64-installer.exe`。

### Linux

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

`-system-qt` 版本不捆绑 Qt 库，而是依赖于系统安装的库。如果 GUI 无法加载，请尝试 system-qt 版本。

### macOS

解压 ZIP 文件。由于 Apple 严格的安全策略，您必须移除隔离属性：

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

要启用内置提权功能，请在 `系统偏好设置` → `安全性与隐私` → `隐私` → `完全磁盘访问权限` 中授予 `终端` 完全磁盘访问权限。

## 包管理器

发行版 | 仓库
-- | --
Fedora/RHEL | [Throne RPM 仓库](https://parhelia512.github.io/)
Fedora/RHEL | [Terra](https://github.com/terrapkg/packages/tree/frawhide/anda/apps/throne)
openSUSE/SLES | [Throne RPM 仓库](https://parhelia512.github.io/)
Arch Linux | [AUR](https://aur.archlinux.org/packages/throne-bin)
任何发行版 | [Nix](https://search.nixos.org/packages?channel=unstable&show=throne)
Windows | [Scoop](https://scoop.sh/#/apps?id=b77aee518a6b60c7a582cc24dfb3269c93f697c6&q=throne)
Windows | [WinGet](https://winstall.app/apps/Throneproj.Throne)

## 从源码编译

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

## 下一步

安装完成后，请前往 [配置](/get_started/configuration/) 设置您的代理配置。
