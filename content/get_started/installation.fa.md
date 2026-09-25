+++
title = "نصب"
description = "Throne را روی Windows، macOS یا Linux نصب کنید، آن را به‌روز نگه دارید یا از سورس بسازید."
weight = 1
toc = true
+++

این صفحه توضیح می‌دهد که چگونه Throne را روی Windows، macOS و Linux نصب کنید، چگونه آن را به‌روزرسانی کنید و چگونه آن را از سورس بسازید. فایل‌ها را از صفحهٔ [دانلود](@/downloads.fa.md) دریافت کنید. برای Android، [نصب و ارتقا](@/android/installation.fa.md) را ببینید.

## Windows {#windows}

### کدام فایل را دانلود کنم {#windows-files}

| رایانهٔ شما | فایل |
|---|---|
| هر رایانهٔ Windows، اگر مطمئن نیستید | `Throne-<version>-windows-universal-installer.exe` |
| Windows 10 1809 یا جدیدتر، x64 | `Throne-<version>-windows64.zip` |
| Windows روی ARM64 | `Throne-<version>-windows-arm64.zip` |
| Windows 7 SP1 تا Windows 10 1803 (x64)، یا پردازنده‌ای بدون SSE4.2 | `Throne-<version>-windowslegacy64.zip` |
| Windows 7 SP1 یا جدیدتر، 32 بیتی (x86) | `Throne-<version>-windows32.zip` |

### نصب‌کننده {#windows-installer}

نصب‌کنندهٔ universal ساده‌ترین گزینه است:

- Throne را برای حساب کاربری شما در `%LOCALAPPDATA%\Throne` نصب می‌کند. به دسترسی مدیر (administrator) نیازی ندارید.
- بیلد مناسب رایانهٔ شما را انتخاب می‌کند: x64، ARM64 یا 32 بیتی. روی Windows x64 قدیمی‌تر از Windows 10 1809، بیلد legacy را نصب می‌کند.
- Throne را به منوی Start و به دسکتاپ اضافه می‌کند.
- Throne نصب‌شده در هر بار اجرا لینک‌های `throne://` را ثبت می‌کند تا این لینک‌ها در Throne باز شوند. [لینک‌های عمیق](@/advanced/deeplinks.fa.md#receive) را ببینید.

Throne نمایه‌ها و تنظیمات شما را در پوشهٔ `config` داخل پوشهٔ نصب نگه می‌دارد. اگر Throne را با نصب‌کنندهٔ قدیمی (پیش از 1.3.0) نصب کرده بودید، نصب‌کنندهٔ جدید از همان پوشه استفاده می‌کند و داده‌های شما را نگه می‌دارد.

برنامهٔ نصب می‌تواند Throne را برای همهٔ کاربران هم در `Program Files` نصب کند. این کار به دسترسی مدیر نیاز دارد. Throne نمی‌تواند در `Program Files` بنویسد، بنابراین داده‌های شما را به‌جای آن در `%LOCALAPPDATA%\Throne\config` نگه می‌دارد و به‌روزرسانی با یک کلیک در دسترس نیست.

برای حذف Throne، آن را از فهرست برنامه‌های نصب‌شده در Windows حذف کنید. برنامهٔ حذف می‌پرسد که آیا نمایه‌ها، تنظیمات و گزارش‌های شما هم پاک شوند یا نه. این برنامه ثبت لینک‌های `throne://` را هم حذف می‌کند.

### ZIP قابل حمل {#windows-zip}

1. فایل ZIP مناسب سیستم خود را دانلود کنید (جدول بالا را ببینید).
2. آن را در پوشه‌ای استخراج کنید که بتوانید در آن فایل بنویسید، برای مثال پوشه‌ای در پوشهٔ کاربری‌تان.
3. پوشهٔ `Throne` را باز کنید و `Throne.exe` را اجرا کنید.

همهٔ فایل‌های این پوشه را کنار هم نگه دارید. Throne داده‌های شما را در پوشهٔ `config` در کنار `Throne.exe` ذخیره می‌کند، بنابراین می‌توانید کل پوشه را جابه‌جا کنید یا از آن پشتیبان بگیرید. اگر Throne نتواند در پوشهٔ خودش بنویسد، به‌جای آن از `%LOCALAPPDATA%\Throne\config` استفاده می‌کند.

نسخه‌های ZIP به‌طور پیش‌فرض لینک‌های `throne://` را ثبت نمی‌کنند. برای روشن کردن این قابلیت، گزینهٔ `تنظیمات` (Settings) ← `تنظیمات پایه` (Basic Settings) ← `متداول` (Common) ← `Register throne:// links at startup` را تیک بزنید.

## macOS {#macos}

| Mac شما | فایل |
|---|---|
| Apple Silicon، macOS 13 یا جدیدتر | `Throne-<version>-macos-arm64.zip` |
| Intel، macOS 13 یا جدیدتر | `Throne-<version>-macos-amd64.zip` |
| Intel، macOS 10.15 تا 12 | `Throne-<version>-macoslegacy-amd64.zip` |

1. فایل ZIP را دانلود و استخراج کنید. این فایل شامل پوشهٔ `Throne` با `Throne.app` است.
2. پیش از اینکه `Throne.app` را برای نخستین بار باز کنید، آن را به `/Applications` منتقل کنید. برای حالت TUN، Throne از طریق Terminal به هستهٔ خود دسترسی root می‌دهد و اگر برنامه در `~/Downloads` باشد، این کار ممکن است شکست بخورد.
3. Throne با گواهی Apple امضا نشده است، بنابراین پرچم قرنطینه (quarantine) را در Terminal حذف کنید. بدون این مرحله، macOS می‌گوید Throne «is damaged and can't be opened» (آسیب دیده است و باز نمی‌شود).

   ```bash
   xattr -d com.apple.quarantine /Applications/Throne.app
   ```

4. Throne را باز کنید.

Throne داده‌های شما را در پوشهٔ کاربری‌تان نگه می‌دارد، نه داخل `Throne.app`، بنابراین می‌توانید برنامه را بدون از دست دادن نمایه‌هایتان جایگزین کنید. `تنظیمات` (Settings) ← `پوشه Config باز شود` (Open Config Folder) این پوشه را نشان می‌دهد. حالت TUN به یک حساب مدیر نیاز دارد؛ [حالت TUN](@/guides/tun_mode.fa.md#privileges) را ببینید.

## Linux {#linux}

| فایل | کاربرد |
|---|---|
| اسکریپت نصب (پایین‌تر) | هر توزیعی. بیلد ZIP را در `/opt/Throne` نصب می‌کند. |
| `Throne-<version>-linux-amd64.zip`، `…-linux-arm64.zip` | یک نسخهٔ قابل حمل در پوشه‌ای به انتخاب شما |
| `Throne-<version>-debian-amd64.deb`، `…-debian-arm64.deb` | Debian، Ubuntu، Linux Mint و دیگر سیستم‌های مبتنی بر Debian |
| `Throne-<version>-fedora-amd64.rpm`، `…-fedora-arm64.rpm` | Fedora و سیستم‌های مبتنی بر RHEL (از نسخهٔ 1.3.0) |
| فایل‌هایی که به `-system-qt.deb` یا `-system-qt.rpm` ختم می‌شوند | همان بسته‌ها، اما از کتابخانه‌های Qt سیستم شما استفاده می‌کنند |

بیلدهای Linux به glibc 2.34 یا جدیدتر نیاز دارند. فایل‌های ARM64 که Qt را همراه دارند به glibc 2.38 یا جدیدتر نیاز دارند.

{% alert_warning() %}
Throne را با `sudo` یا به‌عنوان root اجرا نکنید. برای حالت TUN، Throne فقط به هستهٔ خود، یعنی `ThroneCore`، دسترسی root می‌دهد و گذرواژهٔ شما را از طریق `pkexec` می‌پرسد. [حالت TUN](@/guides/tun_mode.fa.md#privileges) را ببینید.
{% end %}

### اسکریپت نصب {#linux-script}

این اسکریپت بیلد مناسب پردازندهٔ شما را دانلود می‌کند، آن را در `/opt/Throne` نصب می‌کند و Throne را به منوی برنامه‌ها اضافه می‌کند. به Python 3 و دسترسی root نیاز دارد:

```bash
curl -fsSL https://raw.githubusercontent.com/throneproj/Throne/dev/script/install_linux.py | sudo python3
```

اسکریپت آخرین نسخه‌های پایدار و ناپایدار را نشان می‌دهد، و اگر نسخه‌ای نصب شده باشد، نسخهٔ نصب‌شده را هم. `Install` یا `Uninstall` را انتخاب کنید. برای `Install`، شاخه را هم انتخاب کنید: `Stable` یا `Unstable`.

برای به‌روزرسانی یا حذف Throne، همین دستور را دوباره اجرا کنید. حذف، `/opt/Throne` و گزینهٔ منو را پاک می‌کند، اما تنظیمات شما را در `~/.config/Throne` نگه می‌دارد.

### ZIP قابل حمل {#linux-zip}

فایل ZIP شامل پوشهٔ `Throne` است. Throne داده‌های شما را در پوشهٔ `config` داخل آن نگه می‌دارد.

```bash
unzip Throne-x.x.x-linux-amd64.zip
cd Throne
./Throne
```

### Debian و Ubuntu (.deb) {#deb}

```bash
sudo apt install ./Throne-x.x.x-debian-amd64.deb
```

### Fedora و RHEL (.rpm) {#rpm}

```bash
sudo dnf install ./Throne-x.x.x-fedora-amd64.rpm
```

هر دو بسته Throne را در `/opt/Throne` نصب می‌کنند و آن را به منوی برنامه‌ها اضافه می‌کنند. در این حالت Throne داده‌های شما را در `~/.config/Throne` نگه می‌دارد.

### بسته‌های System Qt {#system-qt}

Qt جعبه‌ابزار پنجرهٔ Throne است. بسته‌های معمولی نسخهٔ خودشان از Qt را همراه دارند. بسته‌های `-system-qt` به‌جای آن از کتابخانه‌های Qt 6 توزیع شما استفاده می‌کنند و مدیر بستهٔ شما آن‌ها را به‌عنوان وابستگی نصب می‌کند. وقتی بستهٔ معمولی اجرا نمی‌شود، برای مثال چون پردازندهٔ شما بیش از حد قدیمی است ([عیب‌یابی](@/get_started/installation.fa.md#troubleshooting) را ببینید)، یا وقتی می‌خواهید Throne از پوستهٔ Qt محیط دسکتاپ شما استفاده کند، از بستهٔ system-Qt استفاده کنید. [پرسش‌های متداول](@/help/faq.fa.md#deb-variants) را هم ببینید.

## مدیران بسته {#package-managers}

{% alert_warning() %}
بسته‌های WinGet، Scoop، AUR و Nix را اعضای جامعهٔ کاربری ساخته‌اند، نه توسعه‌دهندگان Throne. این بسته‌ها ممکن است از آخرین نسخهٔ منتشرشده قدیمی‌تر باشند و رفتارشان با بیلدهای رسمی فرق کند. مشکلات چنین بسته‌ای را به نگه‌دارندهٔ آن گزارش دهید. اگر مطمئن نیستید مشکل از Throne است یا از بسته، ابتدا یک بیلد رسمی را از صفحهٔ [دانلود](@/downloads.fa.md) امتحان کنید. [پرسش‌های متداول](@/help/faq.fa.md#third-party-packages) را هم ببینید.
{% end %}

### WinGet {#winget}

```powershell
winget install -e --id Throneproj.Throne
```

### Scoop {#scoop}

```powershell
scoop bucket add extras
scoop install extras/throne
```

### Fedora، RHEL و openSUSE {#rpm-repository}

مخزن RPM در [parhelia512.github.io](https://parhelia512.github.io/) را parhelia512، یکی از اعضای سازمان throneproj در GitHub، اداره می‌کند و README پروژهٔ Throne به آن لینک داده است. این مخزن از فایل‌های منتشرشده جداست. فایل‌های رسمی `.rpm` از نسخهٔ 1.3.0 به هر نسخهٔ منتشرشده پیوست می‌شوند.

Fedora و RHEL 9 یا جدیدتر:

```bash
sudo curl -o /etc/yum.repos.d/throne.repo https://parhelia512.github.io/throne.repo
sudo dnf install -y throne --refresh
```

openSUSE و SLES:

```bash
sudo zypper addrepo -fc https://parhelia512.github.io/throne-sle.repo
sudo zypper install -y throne
```

برای RHEL 8، مراحل صفحهٔ مخزن را دنبال کنید.

### Arch Linux (AUR) {#aur}

Throne با نام `throne` در Arch User Repository موجود است. آن را با یک AUR helper نصب کنید، برای مثال `yay -S throne` یا `paru -S throne`.

### NixOS {#nixos}

این را به پیکربندی NixOS خود اضافه کنید:

```nix
programs.throne = {
  enable = true;
  tunMode.enable = true; # optional, needed for TUN mode
};
```

### Nix {#nix}

در NixOS، نام کانال معمولاً `nixos` است:

```bash
nix-env -iA nixos.throne
```

در توزیع‌های دیگر، نام کانال معمولاً `nixpkgs` است، پس از `nixpkgs.throne` استفاده کنید. برای امتحان کردن Throne بدون نصب آن، `nix-shell -p throne` را اجرا کنید.

## ساخت از سورس {#build-from-source}

Throne دو بخش دارد که جداگانه ساخته می‌شوند: رابط کاربری (`Throne`، نوشته‌شده با C++ و Qt) و هسته (`ThroneCore`، نوشته‌شده با Go). رابط کاربری بدون هسته نمی‌تواند متصل شود، بنابراین هسته باید در کنار فایل اجرایی `Throne` باشد. مخزن هیچ Git submodule ندارد، بنابراین یک `git clone` معمولی کافی است.

| بخش | پیش‌نیازها |
|---|---|
| رابط کاربری | CMake 3.20 یا جدیدتر، یک کامپایلر C++20، Qt 6.2 یا جدیدتر (Widgets، Network، LinguistTools و در Linux، DBus)، هدرهای توسعهٔ X11 در Linux |
| هسته | Go 1.26 یا جدیدتر، `protoc`، `protoc-gen-go` و `protoc-gen-go-grpc`. CGO در Linux و macOS: در Linux زنجیرهٔ ابزار Chromium از cronet-go (خروجی NaïveProxy به آن نیاز دارد) و در macOS ابزارهای خط فرمان Xcode. |

نمونه برای Ubuntu 22.04 یا جدیدتر روی x64:

1. ابزارهای ساخت و Qt را نصب کنید:

   ```bash
   sudo apt update
   sudo apt install build-essential cmake ninja-build git curl protobuf-compiler libx11-dev \
     qt6-base-dev qt6-tools-dev qt6-tools-dev-tools qt6-l10n-tools libqt6svg6-dev \
     qt6-translations-l10n libglx-dev libgl1-mesa-dev
   ```

2. Go 1.26 یا جدیدتر را از [go.dev/dl](https://go.dev/dl/) نصب کنید. بسته‌های Go در بیشتر توزیع‌ها قدیمی‌ترند.
3. رابط کاربری را بسازید. فرایند ساخت به `srslist.h`، یعنی فهرست نام‌های مجموعه‌قوانین، در پوشهٔ `build` نیاز دارد:

   ```bash
   git clone https://github.com/throneproj/Throne.git ~/Throne
   cd ~/Throne
   mkdir build
   cd build
   curl -fLso srslist.h https://raw.githubusercontent.com/throneproj/routeprofiles/rule-set/srslist.h
   cmake -GNinja -DCMAKE_BUILD_TYPE=Release ..
   ninja
   ```

4. پلاگین‌های protobuf را با همان نسخه‌هایی که بیلدهای رسمی به کار می‌برند نصب کنید و پوشهٔ `bin` مربوط به Go را به `PATH` اضافه کنید:

   ```bash
   go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.12
   go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.6.2
   export PATH="$PATH:$(go env GOPATH)/bin"
   ```

5. زنجیرهٔ ابزار Chromium را دانلود کنید. `<commit>` را با همان commit از cronet-go جایگزین کنید که مرحلهٔ `Clone cronet-go` در `.github/workflows/build.yml` آن را checkout می‌کند:

   ```bash
   git clone https://github.com/throneproj/cronet-go.git ~/cronet-go
   cd ~/cronet-go
   git checkout <commit>
   git submodule update --init --recursive --depth=1
   go run ./cmd/build-naive --target=linux/amd64 download-toolchain
   eval "$(go run ./cmd/build-naive --target=linux/amd64 env --export)"
   ```

   آخرین دستور، `CC`، `CXX` و `CGO_LDFLAGS` را فقط برای ترمینال فعلی تنظیم می‌کند. مرحلهٔ بعد را در همین ترمینال اجرا کنید.

6. هسته را بسازید و آن را در کنار رابط کاربری کپی کنید. `build_go.sh` پیش از ساخت، پوشهٔ `DEST` را پاک می‌کند، پس یک پوشهٔ مخصوص به آن بدهید:

   ```bash
   cd ~/Throne
   GOOS=linux GOARCH=amd64 DEST="$PWD/deployment/linux-amd64" ./script/build_go.sh
   cp deployment/linux-amd64/ThroneCore build/
   ```

7. Throne را با `./build/Throne` اجرا کنید.

روی ARM64، از `--target=linux/arm64` و `GOARCH=arm64` استفاده کنید.

- **macOS:** گزینهٔ `-DNKR_PACKAGE_MACOS=1` را به دستور `cmake` اضافه کنید؛ با این کار `Throne.app` ساخته می‌شود. هسته را با `GOOS=darwin` بسازید و `ThroneCore` را در `Throne.app/Contents/MacOS/` کپی کنید.
- **Windows:** بیلدهای رسمی رابط کاربری را با MSVC و Ninja کامپایل می‌کنند و هسته را با `GOOS=windows` روی Linux کراس‌کامپایل می‌کنند (اسکریپت برای Windows، CGO را خاموش می‌کند). `ThroneCore.exe` و `libcronet.dll` را از پوشهٔ `DEST` در کنار `Throne.exe` کپی کنید.

مراحل دقیق بیلدهای رسمی در `.github/workflows/build.yml` در [مخزن Throne](https://github.com/throneproj/Throne) آمده است.

## به‌روزرسانی {#updating}

نسخه‌های ZIP و نصب پیش‌فرضِ مخصوص کاربر با نصب‌کنندهٔ Windows می‌توانند خودشان را به‌روزرسانی کنند: روی `Tools` → `Check For Update` و سپس `بروزرسانی` (Update) کلیک کنید. بقیهٔ نسخه‌ها را به همان روشی به‌روزرسانی کنید که نصب کرده‌اید: نصب‌کنندهٔ جدید را اجرا کنید، بستهٔ `.deb` یا `.rpm` جدید را نصب کنید، اسکریپت نصب را دوباره اجرا کنید، در macOS `Throne.app` را جایگزین کنید، یا از مدیر بستهٔ خود استفاده کنید. نمایه‌ها و تنظیمات شما باقی می‌مانند.

برای جزئیات، نسخه‌های بتا و پشتیبان‌گیری، [پشتیبان‌گیری، به‌روزرسانی و مهاجرت](@/guides/backup.fa.md#updating) را ببینید. پس از به‌روزرسانی در Linux یا macOS، Throne ممکن است دسترسی‌هایی را که برای حالت TUN لازم دارد دوباره درخواست کند.

## عیب‌یابی {#troubleshooting}

- **هشدار آنتی‌ویروس.** برخی آنتی‌ویروس‌ها Throne یا `ThroneCore` را خطرناک تشخیص می‌دهند، بیشتر به این دلیل که به‌روزرسان فایل‌های برنامه را دانلود و جایگزین می‌کند. [پرسش‌های متداول](@/help/faq.fa.md#antivirus) را ببینید.
- **Throne اجرا نمی‌شود و پیام «Incompatible processor. This Qt build requires the following features: sse4.2 popcnt» (پردازنده ناسازگار است) را نشان می‌دهد.** پردازندهٔ شما برای Qt همراه برنامه بیش از حد قدیمی است. در Windows، از `windowslegacy64.zip` استفاده کنید. در Linux، از یک بستهٔ `-system-qt` استفاده کنید. [پرسش‌های متداول](@/help/faq.fa.md#old-systems) را هم ببینید.
- **Linux: Throne اعلام می‌کند که نتوانسته پلاگین پلتفرم Qt با نام «xcb» را بارگذاری کند.** `libxcb-cursor0` (Debian، Ubuntu) یا `xcb-util-cursor` (Fedora، RHEL) را نصب کنید، یا از یک بستهٔ `-system-qt` استفاده کنید.
- **Linux با GNOME: آیکون سینی سیستم دیده نمی‌شود.** افزونهٔ AppIndicator را برای GNOME نصب کنید.
- **macOS: «Throne is damaged and can't be opened» (Throne آسیب دیده است و باز نمی‌شود).** پرچم قرنطینه هنوز فعال است. دستور `xattr` را از مراحل [macOS](@/get_started/installation.fa.md#macos) اجرا کنید.

برای مشکلات پس از نصب، [عیب‌یابی](@/help/troubleshooting.fa.md#startup) را ببینید.
