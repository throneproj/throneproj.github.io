+++
title = "安装"
description = "如何安装 Throne 并开始使用。"
weight = 1
sort_by = "weight"

[extra]
+++

Throne 支持 Windows、Linux 和 macOS。请根据您的平台选择合适的安装方式。

## 系统要求

| 平台    | 最低版本       | 架构         |
|---------|----------------|--------------|
| Windows | Windows 7 SP1  | x64, ARM64   |
| Linux   | GLIBC 2.31+    | x64, ARM64   |
| macOS   | macOS 10.15+   | x64, ARM64   |

## Windows

从 [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) 下载最新版本：

- `Throne-x.x.x-windows-arm64.zip` - ARM64 设备
- `Throne-x.x.x-windows-*.zip` - x64 设备

解压 ZIP 文件并运行 `Throne.exe`。

## Linux

### Debian/Ubuntu (.deb)

从 [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) 下载 `.deb` 包：

```bash
# 系统已安装 Qt 库
sudo dpkg -i Throne-x.x.x-debian-amd64.deb

# 系统未安装 Qt 库
sudo dpkg -i Throne-x.x.x-debian-amd64.deb
```

`-system-qt` 版本不包含 Qt 库，依赖系统已安装的 Qt 库。如果 GUI 无法加载，请尝试 system-qt 版本。

### RPM 发行版

对于 Fedora、RHEL 和 openSUSE，请使用 [RPM 仓库](https://parhelia512.github.io/)。

### Arch Linux (AUR)

对于 Arch Linux 及基于 Arch 的发行版，请从 [AUR](https://aur.archlinux.org/packages/throne) 安装：

```bash
# 使用 yay 或 paru
yay -S throne-git

# 或从源代码构建
git clone --recursive https://github.com/throneproj/Throne.git
cd Throne
mkdir build
cd build
cmake ..
make -j$(nproc)
```

### 便携版 (ZIP)

下载 ZIP 包：

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

### 安装后配置 (Linux)

要使用 TUN 模式（系统代理），请设置 SUID 位：

```bash
sudo chmod +s /usr/bin/Throne
```

## macOS

从 [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) 下载对应版本：

- `Throne-x.x.x-macos-arm64.zip` - Apple Silicon (M1/M2/M3)
- `Throne-x.x.x-macos-amd64.zip` - Intel Mac
- `Throne-x.x.x-macoslegacy-amd64.zip` - 旧版 macOS

### 下载后配置

由于 Apple 的严格安全策略，您必须移除隔离属性：

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

要启用内置提权功能，请在 `系统偏好设置` → `安全性与隐私` → `隐私` → `完全磁盘访问权限` 中授予 `终端` 完全磁盘访问权限。

## 更新

Throne 具有内置更新功能。您也可以手动从 [Releases 页面](https://github.com/throneproj/Throne/releases) 下载新版本。

## 故障排除

### 杀毒软件误报

某些杀毒软件可能会将 Throne 标记为恶意软件，因为其更新功能会下载、删除和替换文件——这与勒索软件行为类似。请自行解决。

## 下一步

安装完成后，请前往 [配置](/get_started/configuration/) 设置您的代理配置。
