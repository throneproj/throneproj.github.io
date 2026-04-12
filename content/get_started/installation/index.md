+++
title = "Installation"
description = "How to install Throne and get started."
weight = 1
sort_by = "weight"

[extra]
+++

Throne supports Windows, Linux, and macOS. Choose the appropriate installation method for your platform.

## Download the binary

Go to [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) and download the file for your platform.

### Version Matrix

| Platform | Architecture | Package Type / Distro | Min. Version | File Suffix |
| :--- | :--- | :--- | :--- | :--- |
| **Windows** | x64 | Installer | Windows 10 | `windows64-installer.exe` |
| | x64 | Portable (ZIP) | Windows 10 | `windows64.zip` |
| | ARM64 | Portable (ZIP) | Windows 10 | `windows-arm64.zip` |
| | x64 | Legacy (Win 7/8) | Windows 7 SP1 | `windowslegacy64.zip` |
| | x86 | Legacy (32-bit) | Windows 7 SP1 | `windows32.zip` |
| |
| **Linux** | x64 | **Generic** (Binary) | GLIBC 2.34 | `linux-amd64.zip` |
| | x64 | **Debian / Ubuntu** | GLIBC 2.34 | `debian-amd64.deb` |
| | x64 | **Debian / Ubuntu** (System Qt) | GLIBC 2.34 | `debian-amd64-system-qt.deb` |
| | ARM64 | **Generic** (Binary) | GLIBC 2.38 | `linux-arm64.zip` |
| | ARM64 | **Debian / Ubuntu** | GLIBC 2.38 | `debian-arm64.deb` |
| | ARM64 | **Debian / Ubuntu** (System Qt) | GLIBC 2.34 | `debian-arm64-system-qt.deb` |
| |
| **macOS** | ARM64 | Apple Silicon | macOS 13 | `macos-arm64.zip` |
| | x64 | Intel | macOS 13 | `macos-amd64.zip` |
| | x64 | Legacy (Intel) | macOS 10.15 | `macoslegacy-amd64.zip` |

### Windows

#### Portable (ZIP)

Extract the ZIP file and run `Throne.exe`.

#### Installer (.exe)

Run `Throne-x.x.x-windows64-installer.exe`.

#### Scoop/WinGet
  
You can also install Throne on Windows using [Scoop](https://scoop.sh/#/apps?id=b77aee518a6b60c7a582cc24dfb3269c93f697c6&q=throne) or [WinGet](https://winstall.app/apps/Throneproj.Throne).

### macOS

Extract the ZIP file. Due to Apple's strict security policy, you must remove the quarantine attribute:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

To enable built-in privilege escalation, grant `Throne` (or `Terminal` if running from CLI) Full Disk Access in `System Settings` → `Privacy & Security` → `Full Disk Access`.

### Linux

Throne provides several ways to install depending on your distribution.

#### Portable (ZIP)

Download the ZIP package:

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

#### Debian/Ubuntu (.deb)

```bash
sudo apt install ./Throne-x.x.x-debian-*.deb
```

Note: The -system-qt version does not bundle Qt libraries and relies on system-installed ones. Use this version if you encounter theme conflicts or if the standard GUI fails to load.

### Fedora/RHEL9+

```bash
sudo curl -o /etc/yum.repos.d/throne.repo https://parhelia512.github.io/throne.repo
sudo dnf install -y throne --refresh
```
For older RHEL versions, visit the [Throne RPM repository](https://parhelia512.github.io/).

### openSUSE/SLES
```bash
sudo zypper addrepo -fc https://parhelia512.github.io/throne-sle.repo
sudo zypper install -y throne
```

### Arch Linux (AUR)

Throne is available in the **Arch User Repository** as `throne-bin`. You can install it using your favourite AUR helper.

```bash
# If you use yay
yay -S throne-bin

# If you use paru
paru -S throne-bin
```

#### NixOS

Add the following Nix code to your NixOS Configuration.

```nix
programs.throne = {
   enable = true;
   # tunMode.enable = true; Add this line to enable tun mode
};
```

### Nix

You can also install Throne using the Nix package manager on any supported distribution.

```bash
nix-env -iA nixos.throne
```
Or you can use nix-shell to try it out without installing.
```bash
nix-shell -p throne
```

## Build from source

You also have an option to build Throne from source.

```bash
git clone --recursive https://github.com/throneproj/Throne.git
cd Throne
mkdir build
cd build
curl -fLso srslist.h "https://raw.githubusercontent.com/throneproj/routeprofiles/rule-set/srslist.h"
cmake ..
make -j$(nproc)
```

## Updating

Throne has a built-in update function. You can also download new releases manually from the [Releases page](https://github.com/throneproj/Throne/releases).

## Troubleshooting

### Antivirus Detection

Some antivirus software may flag Throne as malware because its update functionality downloads, removes, and replaces files—similar to ransomware behavior. Additionally, the `System DNS` feature modifies system DNS settings, which some antivirus applications consider dangerous.

## Next Steps

After installation, proceed to [Configuration](/get_started/configuration/) to set up your proxy profiles.
