+++
title = "Установка"
description = "Как установить Throne и начать работу."
weight = 1
toc = true
+++

Throne поддерживает Windows, Linux и macOS. Выберите подходящий метод установки для вашей платформы.

## Скачать исполняемый файл

Перейдите на страницу [скачать](@/downloads.ru.md) файл для вашей платформы.

### Windows

#### Портативная версия (ZIP)

Распакуйте ZIP-архив и запустите `Throne.exe`.

#### Установщик (.exe)

Запустите `Throne-x.x.x-universal-installer.exe`.

### macOS

Распакуйте ZIP-архив. Из-за строгой политики безопасности Apple необходимо удалить атрибут карантина:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

Перед первым запуском переместите `Throne.app` в `/Applications`. Встроенное повышение привилегий открывает Terminal, чтобы установить для ядра бит setuid-root, и этот шаг может завершиться неудачей, пока приложение находится в `~/Downloads`.

### Linux

#### Установщик для командной строки (рекомендуется)

Самый быстрый способ установки на любом дистрибутиве. Скрипт скачивает сборку для вашей архитектуры, устанавливает её в `/opt/Throne` и добавляет ярлык приложения:

```bash
curl -fsSL https://raw.githubusercontent.com/throneproj/Throne/dev/script/install_linux.py | sudo python3
```

Он работает как интерактивное меню в терминале: показывает последние стабильную и нестабильную версии (а также уже установленную, если она есть), затем спрашивает, хотите ли вы выполнить **Install** или **Uninstall** и какую ветку установить. Требуются Python 3 и права root.

Запустите ту же команду повторно, чтобы обновиться до новой версии или удалить программу. При удалении стираются `/opt/Throne` и ярлык приложения, но ваши настройки в `~/.config/Throne` остаются нетронутыми.

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

## Менеджеры пакетов

Throne можно установить несколькими способами в зависимости от вашего дистрибутива.

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
Для старых версий RHEL посетите [RPM-репозиторий Throne](https://parhelia512.github.io/).

### openSUSE/SLES
```bash
sudo zypper addrepo -fc https://parhelia512.github.io/throne-sle.repo
sudo zypper install -y throne
```

### Arch Linux (AUR)

Throne доступен в **Arch User Repository** под именем `throne`. Вы можете установить его с помощью вашего любимого AUR-помощника.

```bash
# Если вы используете yay
yay -S throne

# Если вы используете paru
paru -S throne
```

### NixOS

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
