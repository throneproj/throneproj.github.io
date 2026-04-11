+++
title = "Установка"
description = "Как установить Throne и начать работу."
weight = 1
sort_by = "weight"

[extra]
+++

Throne поддерживает Windows, Linux и macOS. Выберите подходящий метод установки для вашей платформы.

## Скачать исполняемый файл

Перейдите в [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) и скачайте файл для вашей платформы.

### Таблица версий

Платформа | Архитектура | Мин. версия | Суффикс файла
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

#### Портативная (ZIP)

Распакуйте ZIP-файл и запустите `Throne.exe`.

#### Установщик (.exe)

Запустите `Throne-x.x.x-windows64-installer.exe`.

### Linux

#### Портативная (ZIP)

Скачайте ZIP-пакет:

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

#### Debian/Ubuntu (.deb)

```bash
sudo dpkg -i Throne-x.x.x-debian-*.deb
```

Версия `-system-qt` не включает библиотеки Qt и зависит от установленных в системе. Если графический интерфейс не загружается, попробуйте версию system-qt.

### macOS

Распакуйте ZIP-файл. Из-за строгой политики безопасности Apple вам необходимо удалить атрибут карантина:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

Чтобы включить встроенную функцию повышения привилегий, предоставьте `Terminal` полный доступ к диску в `Системные настройки` → `Безопасность и конфиденциальность` → `Конфиденциальность` → `Полный доступ к диску` (System Preferences → Security & Privacy → Privacy → Full Disk Access).

## Менеджеры пакетов

Дистрибутив | Репозиторий
-- | --
Fedora/RHEL | [Репозиторий Throne RPM](https://parhelia512.github.io/)
Fedora/RHEL | [Terra](https://github.com/terrapkg/packages/tree/frawhide/anda/apps/throne)
openSUSE/SLES | [Репозиторий Throne RPM](https://parhelia512.github.io/)
Arch Linux | [AUR](https://aur.archlinux.org/packages/throne-bin)
Любой дистрибутив | [Nix](https://search.nixos.org/packages?channel=unstable&show=throne)
Windows | [Scoop](https://scoop.sh/#/apps?id=b77aee518a6b60c7a582cc24dfb3269c93f697c6&q=throne)
Windows | [WinGet](https://winstall.app/apps/Throneproj.Throne)

## Сборка из исходного кода

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

В Throne есть встроенная функция обновления. Вы также можете скачивать новые версии вручную со [страницы Releases](https://github.com/throneproj/Throne/releases).

## Устранение неполадок

### Обнаружение антивирусом

Некоторые антивирусные программы могут помечать Throne как вредоносное ПО, поскольку его функция обновления скачивает, удаляет и заменяет файлы, что похоже на поведение программ-вымогателей. Кроме того, функция `System DNS` изменяет системные настройки DNS, что некоторые антивирусные приложения считают опасным.

## Что дальше

После установки перейдите в [Конфигурация](/get_started/configuration/) для настройки профилей прокси.
