+++
title = "Installation"
description = "How to install Throne and get started."
weight = 1
sort_by = "weight"

[extra]
+++

Throne supports Windows, Linux, and macOS. Choose the appropriate installation method for your platform.

## System Requirements

| Platform | Minimum Version | Architecture |
|----------|-----------------|--------------|
| Windows  | Windows 7 SP1   | x64, ARM64   |
| Linux    | GLIBC 2.31+     | x64, ARM64   |
| macOS    | macOS 10.15+    | x64, ARM64   |

## Windows

Download the latest release from [GitHub Releases](https://github.com/throneproj/Throne/releases/latest):

- `Throne-x.x.x-windows-arm64.zip` - for ARM64 devices
- `Throne-x.x.x-windows-*.zip` - for x64 devices

Extract the ZIP file and run `Throne.exe`.

## Linux

### Debian/Ubuntu (.deb)

Download the `.deb` package from [GitHub Releases](https://github.com/throneproj/Throne/releases/latest):

```bash
# For systems with Qt libraries installed
sudo dpkg -i Throne-x.x.x-debian-amd64.deb

# For legacy systems (includes bundled Qt libraries)
sudo dpkg -i Throne-x.x.x-debian-amd64.deb
```

The `-system-qt` version does not bundle Qt libraries and relies on system-installed ones. If the GUI fails to load, try the system-qt version.

### RPM-based Distributions

For Fedora, RHEL, and openSUSE, use the [RPM repository](https://parhelia512.github.io/).

### Arch Linux (AUR)

For Arch Linux and Arch-based distributions, install from the [AUR](https://aur.archlinux.org/packages/throne):

```bash
# Using yay or paru
yay -S throne-git

# Or build from source
git clone --recursive https://github.com/throneproj/Throne.git
cd Throne
mkdir build
cd build
cmake ..
make -j$(nproc)
```

### Portable (ZIP)

Download the ZIP package:

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

### Post-Installation (Linux)

To use TUN mode (system proxy), set the SUID bit on the Throne binary:

```bash
sudo chmod +s /usr/bin/Throne
```

## macOS

Download the appropriate version from [GitHub Releases](https://github.com/throneproj/Throne/releases/latest):

- `Throne-x.x.x-macos-arm64.zip` - for Apple Silicon (M1/M2/M3)
- `Throne-x.x.x-macos-amd64.zip` - for Intel Macs
- `Throne-x.x.x-macoslegacy-amd64.zip` - for older macOS versions

### After Downloading

Due to Apple's strict security policy, you must remove the quarantine attribute:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

To enable built-in privilege escalation, grant `Terminal` Full Disk Access in `System Preferences` → `Security & Privacy` → `Privacy` → `Full Disk Access`.

## Updating

Throne has a built-in update function. You can also download new releases manually from the [Releases page](https://github.com/throneproj/Throne/releases).

## Troubleshooting

### Antivirus Detection

Some antivirus software may flag Throne as malware because its update functionality downloads, removes, and replaces files—similar to ransomware behavior. Additionally, the `System DNS` feature modifies system DNS settings, which some antivirus applications consider dangerous.

## Next Steps

After installation, proceed to [Configuration](/get_started/configuration/) to set up your proxy profiles.
