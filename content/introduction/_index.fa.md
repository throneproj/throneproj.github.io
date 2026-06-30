+++
title = "مقدمه"
description = "Throne مقدمه"
weight = 1
sort_by = "weight"

[extra]
+++

Throne (پیش‌تر با نام Nekoray) یک ابزار پروکسی گرافیکی (GUI) دسکتاپ و چندسکویی مبتنی بر Qt است که با [Sing-box](https://github.com/SagerNet/sing-box) قدرت گرفته است.

به‌صورت پیش‌فرض از Windows 11/10/8/7 / Linux / MacOS پشتیبانی می‌کند.

<img width="1002" height="789" alt="image" src="https://github.com/user-attachments/assets/3c9bf428-e3bd-426b-8ca1-cc57ecbedd7e" />

## پروتکل‌های پشتیبانی‌شده

- SOCKS
- HTTP(S)
- Shadowsocks
- Trojan
- VMess
- VLESS
- TUIC
- Hysteria
- Hysteria2
- AnyTLS
- Mieru
- NaïveProxy
- Juicity
- TrustTunnel
- ShadowTLS
- Wireguard
- AmneziaWG
- SSH
- Xray VLESS
- Custom Outbound (هم Sing-box و هم Xray)
- Custom Config (هم Sing-box و هم Xray)
- Chaining outbounds
- Extra Core

## قالب‌های اشتراک

قالب‌های گوناگونی پشتیبانی می‌شوند، از جمله لینک‌های اشتراک‌گذاری، نمایش‌های JSON گوناگونِ پیکربندی‌های Sing-box و قالب لینک v2rayN، و همچنین پشتیبانی محدود از قالب‌های Shadowsocks و Clash.

## سپاس‌گزاری

- [sing-box](https://github.com/SagerNet/sing-box)
- [Xray-core](https://github.com/xtls/xray-core)
- [Qv2ray](https://github.com/Qv2ray/Qv2ray)
- [Qt](https://www.qt.io/)
- [simple-protobuf](https://github.com/tonda-kriz/simple-protobuf)
- [fkYAML](https://github.com/fktn-k/fkYAML)
- [quirc](https://github.com/dlbeer/quirc)
- [QHotkey](https://github.com/Skycoder42/QHotkey)
- [SQLiteCpp](https://github.com/srombauts/sqlitecpp)

## پرسش‌های متداول

**این پروژه چه تفاوتی با Nekoray اصلی دارد؟**

توسعه‌دهندهٔ Nekoray در دسامبر ۲۰۲۳ پروژه را تا حدی رها کرد؛ اخیراً چند به‌روزرسانی جزئی انجام شد، اما اکنون پروژه به‌طور رسمی بایگانی شده است. این پروژه قصد دارد راه پروژهٔ اصلی را ادامه دهد، با بهبودهای فراوان، انبوهی از ویژگی‌های جدید و نیز حذف ویژگی‌های منسوخ و ساده‌سازی.

**چرا آنتی‌ویروس من Throne و/یا هستهٔ (Core) آن را به‌عنوان بدافزار شناسایی می‌کند؟**

قابلیت به‌روزرسانی داخلی Throne نسخهٔ جدید را دانلود می‌کند، فایل‌های قدیمی را حذف و با فایل‌های جدید جایگزین می‌کند؛ این رفتار بسیار شبیه کاری است که بدافزارها انجام می‌دهند (حذف فایل‌های شما و جایگزینی آن‌ها با نسخه‌ای رمزگذاری‌شده). همچنین قابلیت `System DNS` تنظیمات DNS سیستم شما را تغییر می‌دهد که از سوی برخی آنتی‌ویروس‌ها نیز اقدامی خطرناک تلقی می‌شود.

**آیا تنظیم بیت `SUID` در لینوکس واقعاً لازم است؟**

برای ساخت و مدیریت یک رابط TUN سیستمی به دسترسی root نیاز است؛ بدون آن باید به Core برخی مجوزهای `Cap_xxx_admin` را بدهید و باز هم هنگام هر بار فعال‌سازی TUN باید ۳ تا ۴ بار رمز عبور خود را وارد کنید. می‌توانید ارتقای خودکار سطح دسترسی را در `Basic Settings` (تنظیمات پایه) → `Security` (امنیت) غیرفعال کنید، اما توجه داشته باشید که ویژگی‌های نیازمند دسترسی root تا زمانی که مجوزهای لازم را به‌صورت دستی اعطا نکنید، کار نخواهند کرد.

**چرا پس از بستن اجباری Throne، اینترنت من قطع می‌شود؟**

اگر Throne در حالی که `System proxy` فعال است به‌صورت اجباری بسته شود، فرایند بلافاصله پایان می‌یابد و Throne نمی‌تواند تنظیمات پروکسی را بازنشانی کند.

راه‌حل:

- همیشه Throne را به‌صورت عادی ببندید.
- اگر به‌اشتباه آن را به‌صورت اجباری بستید، دوباره Throne را باز کنید، `System proxy` را فعال و سپس غیرفعال کنید — این کار تنظیمات را بازنشانی می‌کند.

**پروفایل‌های مسیریابی/مجموعه‌قوانینِ قابل دانلود از کجا می‌آیند؟**

آن‌ها در مخزن [routeprofiles](https://github.com/throneproj/routeprofiles) قرار دارند.

**فایل `Throne-<version>-debian-system-qt-x64.deb` چه تفاوتی با `Throne-<version>-debian-x64.deb` دارد و چرا دومی حدود ۳ برابر سنگین‌تر از اولی است؟**

اولی کتابخانه‌های Qt را در خود جای نمی‌دهد و به نسخه‌های نصب‌شده روی میزبان متکی است. دومی همهٔ موارد لازم را همراه خود بسته‌بندی می‌کند و به همین دلیل سنگین‌تر است. دلیل وجود نسخهٔ اول این است که در سیستم‌های قدیمی، کتابخانه‌های Qt ارائه‌شده از ویژگی‌های سیستمیِ پشتیبانی‌نشده استفاده می‌کنند. اگر رابط گرافیکی روی سیستم شما بارگذاری نشد، می‌توانید نسخهٔ system-qt را دانلود کرده و کتابخانه‌های Qt مناسب را از مدیر بستهٔ خود نصب کنید یا آن‌ها را از منبع کامپایل کنید.
