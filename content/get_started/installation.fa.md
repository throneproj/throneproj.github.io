+++
title = "نصب"
description = "چگونه Throne را نصب کنیم و شروع به کار کنیم."
weight = 1
toc = true
+++

Throne از Windows، Linux و macOS پشتیبانی می کند. روش نصب مناسب برای پلتفرم خود را انتخاب کنید.

## دریافت فایل اجرایی

به بروید و فایل مربوط به پلتفرم خود را [دانلود ](@/downloads.fa.md)کنید.

### Windows

#### نسخه پرتابل (ZIP)

فایل ZIP را استخراج کرده و `Throne.exe` را اجرا کنید.

#### نصب‌کننده (.exe)

فایل `Throne-x.x.x-universal-installer.exe` را اجرا کنید.

### macOS

فایل ZIP را استخراج کنید. با توجه به سیاست های امنیتی سختگیرانه اپل، باید ویژگی قرنطینه را حذف کنید:

```bash
xattr -d com.apple.quarantine /path/to/Throne.app
```

پیش از اولین اجرا، `Throne.app` را به پوشه `/Applications` منتقل کنید. ارتقای دسترسی داخلی، Terminal را باز می‌کند تا بیت setuid-root را روی هسته تنظیم کند و اگر برنامه همچنان داخل `~/Downloads` باشد، این مرحله ممکن است شکست بخورد.

### Linux

#### نصب‌کننده خط فرمان (پیشنهادی)

سریع‌ترین راه نصب روی هر توزیعی. اسکریپت، نسخهٔ متناسب با معماری سیستم شما را دانلود می‌کند، آن را در `/opt/Throne` نصب می‌کند و یک میان‌بر دسکتاپ می‌سازد:

```bash
curl -fsSL https://raw.githubusercontent.com/throneproj/Throne/dev/script/install_linux.py | sudo python3
```

این اسکریپت به‌صورت یک منوی تعاملی در ترمینال اجرا می‌شود: ابتدا آخرین نسخه‌های پایدار (Stable) و ناپایدار (Unstable) را نشان می‌دهد — و اگر از پیش نسخه‌ای نصب کرده باشید، آن را هم — سپس می‌پرسد که می‌خواهید **Install** کنید یا **Uninstall**، و کدام شاخه نصب شود. به Python 3 و دسترسی root نیاز دارد.

برای به‌روزرسانی به نسخه‌ای جدیدتر یا برای حذف برنامه، همین دستور را دوباره اجرا کنید. حذف، پوشهٔ `/opt/Throne` و میان‌بر دسکتاپ را پاک می‌کند اما تنظیمات شما در `~/.config/Throne` دست‌نخورده باقی می‌ماند.

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

## مدیران بسته (Package managers)

بستگی به توزیع شما، Throne روش‌های مختلفی را برای نصب ارائه می‌دهد.

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
برای نسخه‌های قدیمی‌تر RHEL، به [Throne RPM repository](https://parhelia512.github.io/) مراجعه کنید.

### openSUSE/SLES
```bash
sudo zypper addrepo -fc https://parhelia512.github.io/throne-sle.repo
sudo zypper install -y throne
```

### Arch Linux (AUR)

برنامه Throne در **Arch User Repository** با نام `throne` در دسترس است. می‌توانید آن را با استفاده از AUR helper مورد علاقه‌تان نصب کنید.

```bash
# اگر از yay استفاده می‌کنید
yay -S throne

# اگر از paru استفاده می‌کنید
paru -S throne
```

### NixOS

کد Nix زیر را به تنظیمات NixOS خود اضافه کنید.

```nix
programs.throne = {
   enable = true;
   # tunMode.enable = true; Add this line to enable tun mode
};
```

### Nix

همچنین می‌توانید Throne را با استفاده از مدیر بسته Nix روی هر توزیع پشتیبانی‌شده‌ای نصب کنید.

```bash
nix-env -iA nixos.throne
```
یا می‌توانید از nix-shell استفاده کنید تا بدون نیاز به نصب، آن را امتحان کنید.
```bash
nix-shell -p throne
```

## ساخت از روی سورس کد

همچنین این امکان را دارید که Throne را از روی سورس‌کد (کد منبع) کامپایل و نصب کنید.

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
