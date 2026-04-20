+++
title = "Установка"
description = "Как установить Throne и начать работу."
weight = 1
sort_by = "weight"

[extra]
+++

Throne поддерживает Windows, Linux и macOS. Выберите подходящий метод установки для вашей платформы.

## Скачать исполняемый файл

Перейдите на страницу [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) и скачайте файл для вашей платформы.

### Таблица версий

| Платформа | Архитектура | Тип пакета / Дистрибутив | Мин. версия | Суффикс файла |
| :--- | :--- | :--- | :--- | :--- |
| **Windows** | x64 | Установщик | Windows 10 | `windows64-installer.exe` |
| | x64 | Портативная (ZIP) | Windows 10 | `windows64.zip` |
| | ARM64 | Портативная (ZIP) | Windows 10 | `windows-arm64.zip` |
| | x64 | Legacy (Win 7/8) | Windows 7 SP1 | `windowslegacy64.zip` |
| | x86 | Legacy (32-бит) | Windows 7 SP1 | `windows32.zip` |
| |
| **Linux** | x64 | **Общий** (Бинарный файл) | GLIBC 2.34 | `linux-amd64.zip` |
| | x64 | **Debian / Ubuntu** | GLIBC 2.34 | `debian-amd64.deb` |
| | x64 | **Debian / Ubuntu** (System Qt) | GLIBC 2.34 | `debian-amd64-system-qt.deb` |
| | ARM64 | **Общий** (Бинарный файл) | GLIBC 2.38 | `linux-arm64.zip` |
| | ARM64 | **Debian / Ubuntu** | GLIBC 2.38 | `debian-arm64.deb` |
| | ARM64 | **Debian / Ubuntu** (System Qt) | GLIBC 2.34 | `debian-arm64-system-qt.deb` |
| |
| **macOS** | ARM64 | Apple Silicon | macOS 13 | `macos-arm64.zip` |
| | x64 | Intel | macOS 13 | `macos-amd64.zip` |
| | x64 | Legacy (Intel) | macOS 10.15 | `macoslegacy-amd64.zip` |

### Windows

#### Портативная версия (ZIP)

Распакуйте ZIP-архив и запустите `Throne.exe`.

#### Установщик (.exe)

Запустите `Throne-x.x.x-windows64-installer.exe`.

#### Scoop/WinGet
  
Вы также можете установить Throne в Windows с помощью [Scoop](https://scoop.sh/#/apps?id=b77aee518a6b60c7a582cc24dfb3269c93f697c6&q=throne) или [WinGet](https://winstall.app/apps/Throneproj.Throne).

### macOS

Распакуйте ZIP-архив. Из-за строгой политики безопасности Apple необходимо удалить атрибут карантина:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

Чтобы включить встроенную функцию повышения привилегий, предоставьте `Throne` (или `Terminal`, если запуск идет через CLI) полный доступ к диску в разделе `Системные настройки` → `Конфиденциальность и безопасность` → `Полный доступ к диску`.

### Linux

Throne можно установить несколькими способами в зависимости от вашего дистрибутива.

#### Портативная версия (ZIP)

Скачайте ZIP-пакет:

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

#### Debian/Ubuntu (.deb)

```bash
sudo apt install ./Throne-x.x.x-debian-*.deb
```

Примечание: Версия `-system-qt` не содержит библиотек Qt и полагается на системные. Используйте эту версию, если возникают конфликты тем или графический интерфейс не загружается.

### Fedora/RHEL9+

```bash
sudo curl -o /etc/yum.repos.d/throne.repo https://parhelia512.github.io/throne.repo
sudo dnf install -y throne --refresh
```
Для старых версий RHEL посетите [RPM-репозиторий Throne](https://parhelia512.github.io/).

### openSUSE/SLES
```bash
sudo zypper addrepo -fc https://parhelia512.github.io/throne-sle.repo
sudo zypper install -y throne
```

### Arch Linux (AUR)

Throne доступен в **Arch User Repository** под именем `throne-bin`. Вы можете установить его с помощью вашего любимого AUR-помощника.

```bash
# Если вы используете yay
yay -S throne-bin

# Если вы используете paru
paru -S throne-bin
```

#### NixOS

Добавьте следующий код в конфигурацию NixOS.

```nix
programs.throne = {
   enable = true;
   # tunMode.enable = true; # Добавьте эту строку для включения tun-режима
};
```

### Nix

Вы также можете установить Throne с помощью менеджера пакетов Nix в любом поддерживаемом дистрибутиве.

```bash
nix-env -iA nixos.throne
```
Или воспользуйтесь nix-shell, чтобы попробовать программу без установки.
```bash
nix-shell -p throne
```

## Сборка из исходного кода

Вы также можете собрать Throne из исходного кода самостоятельно.

```bash
git clone --recursive https://github.com/throneproj/Throne.git
cd Throne
mkdir build
cd build
curl -fLso srslist.h "https://raw.githubusercontent.com/throneproj/routeprofiles/rule-set/srslist.h"
cmake ..
make -j$(nproc)
```

## Обновление

В Throne есть встроенная функция обновления. Вы также можете скачивать новые версии вручную со [страницы релизов](https://github.com/throneproj/Throne/releases).

## Устранение неполадок

### Обнаружение антивирусом

Некоторые антивирусные программы могут помечать Throne как вредоносное ПО, поскольку его функция обновления скачивает, удаляет и заменяет файлы — что похоже на поведение программ-вымогателей. Кроме того, функция `System DNS` изменяет системные настройки DNS, что некоторые антивирусные приложения считают опасным.

## Следующие шаги

После установки перейдите к разделу [Конфигурация](/get_started/configuration/) для настройки профилей прокси.
