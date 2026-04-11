+++
title = "نصب"
description = "چگونه Throne را نصب کنیم و شروع به کار کنیم."
weight = 1
sort_by = "weight"

[extra]
+++

Throne از Windows، Linux و macOS پشتیبانی می کند. روش نصب مناسب برای پلتفرم خود را انتخاب کنید.

## دریافت فایل اجرایی

به [GitHub Releases](https://github.com/throneproj/Throne/releases/latest) بروید و فایل مربوط به پلتفرم خود را دانلود کنید.

### ماتریس نسخه ها

پلتفرم | معماری | حداقل نسخه | پسوند فایل
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

#### نسخه پرتابل (ZIP)

فایل ZIP را استخراج کرده و `Throne.exe` را اجرا کنید.

#### نصب‌کننده (.exe)

فایل `Throne-x.x.x-windows64-installer.exe` را اجرا کنید.

### Linux

#### نسخه پرتابل (ZIP)

بسته ZIP را دانلود کنید:

```bash
unzip Throne-x.x.x-linux-*.zip
./Throne
```

#### Debian/Ubuntu (.deb)

```bash
sudo dpkg -i Throne-x.x.x-debian-*.deb
```

نسخه `-system-qt` کتابخانه های Qt را به همراه ندارد و به نسخه های نصب شده در سیستم وابسته است. اگر GUI بارگذاری نشد، نسخه system-qt را امتحان کنید.

### macOS

فایل ZIP را استخراج کنید. با توجه به سیاست های امنیتی سختگیرانه اپل، باید ویژگی قرنطینه را حذف کنید:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

برای فعال کردن ارتقای دسترسی داخلی، به `Terminal` دسترسی کامل به دیسک (Full Disk Access) را در `System Preferences` → `Security & Privacy` → `Privacy` → `Full Disk Access` بدهید.

## مدیران بسته (Package managers)

توزیع | مخزن
-- | --
Fedora/RHEL | [Throne RPM repository](https://parhelia512.github.io/)
Fedora/RHEL | [Terra](https://github.com/terrapkg/packages/tree/frawhide/anda/apps/throne)
openSUSE/SLES | [Throne RPM repository](https://parhelia512.github.io/)
Arch Linux | [AUR](https://aur.archlinux.org/packages/throne-bin)
Any distro | [Nix](https://search.nixos.org/packages?channel=unstable&show=throne)
Windows | [Scoop](https://scoop.sh/#/apps?id=b77aee518a6b60c7a582cc24dfb3269c93f697c6&q=throne)
Windows | [WinGet](https://winstall.app/apps/Throneproj.Throne)

## ساخت از روی سورس کد

```bash
git clone --recursive https://github.com/throneproj/Throne.git
cd Throne
mkdir build
cd build
curl -fLso srslist.h "https://raw.githubusercontent.com/throneproj/routeprofiles/rule-set/srslist.h"
cmake ..
make -j$(nproc)
```

## بروزرسانی

Throne دارای یک عملکرد داخلی برای بروزرسانی است. همچنین می توانید نسخه های جدید را به صورت دستی از [صفحه Releases](https://github.com/throneproj/Throne/releases) دانلود کنید.

## عیب یابی

### تشخیص توسط آنتی ویروس

برخی نرم افزارهای آنتی ویروس ممکن است Throne را به عنوان بدافزار شناسایی کنند زیرا قابلیت بروزرسانی آن فایل ها را دانلود، حذف و جایگزین می کند—که شبیه به رفتار باج افزارها است. به علاوه، ویژگی `System DNS` تنظیمات DNS سیستم را تغییر می دهد، که برخی از برنامه های آنتی ویروس آن را خطرناک می دانند.

## مراحل بعدی

پس از نصب، برای تنظیم پروفایل های پروکسی خود به بخش [پیکربندی](/get_started/configuration/) بروید.
