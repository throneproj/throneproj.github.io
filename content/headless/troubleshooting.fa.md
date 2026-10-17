+++
title = "عیب‌یابی"
description = "مشکلات رایج Throne بدون رابط گرافیکی، از یونیتی که شروع نمی‌شود تا تداخل‌های TUN و درخواست‌های ردشدهٔ API، و آنچه باید در گزارش باگ بیاورید."
weight = 60
toc = true
+++

با `Throne --check` و `Throne --health` شروع کنید و آن‌ها را با کاربر Throne و با همان `--data-dir` اجرا کنید ([بررسی سلامت و گزارش‌ها](@/headless/monitoring.fa.md) را ببینید)، و آخرین خطوط گزارش را بخوانید. خط `EXIT <code>: <reason>` می‌گوید چرا Throne خارج شده است؛ [کدهای خروج](@/headless/command_line.fa.md#exit-codes) هر کد را توضیح می‌دهد.

## مشکلات رایج {#symptoms}

| نشانه | علت و راه‌حل |
| --- | --- |
| یونیت بی‌درنگ شکست می‌خورد و در گزارش آمده است `refusing to run as root with /var/lib/throne` | کاربران دیگر می‌توانند در پوشهٔ داده‌ها بنویسند. `sudo chmod go-w /var/lib/throne /var/lib/throne/config` را اجرا کنید. |
| کد خروج 3: `… is in use by …` | Throne دیگری پوشهٔ داده‌ها را در اختیار دارد: برنامهٔ دسکتاپ، یک یونیت کاربری، یا یک سرویس دوم. آن یکی را متوقف کنید. |
| برنامهٔ دسکتاپ پیام `Throne is running in the background` را نشان می‌دهد و خارج می‌شود | یک Throne بدون رابط گرافیکی (معمولاً یک یونیت کاربری) از پوشهٔ داده‌های برنامهٔ دسکتاپ استفاده می‌کند. `systemctl --user stop throne` را اجرا کنید، یا آن را با `thronectl` مدیریت کنید. [اجرا در کنار یک Throne دسکتاپ](@/headless/_index.fa.md#beside-desktop) را ببینید. |
| `degraded: api_unavailable`، و در گزارش آمده است `[API] Not listening on 127.0.0.1:9095` | برنامهٔ دیگری پورت 9095 را در اختیار دارد. Throne هر 30 ثانیه دوباره امتحان می‌کند. `--api-listen PORT` پورت دیگری انتخاب می‌کند. |
| `--print-connection`: `The API key is not in a file` | تنظیمات پوشهٔ داده‌ها، API را با کلید خودشان روشن کرده‌اند، همان‌طور که برنامهٔ دسکتاپ این کار را می‌کند. از آن کلید به‌عنوان `THRONE_KEY` استفاده کنید (در برنامهٔ دسکتاپ: `Integration Settings` → `Throne API` → `Copy for scripts`)، یا Throne را با `--api-key-file` اجرا کنید. |
| `--health` یا `--print-connection`: `No headless Throne answered` | آن را با کاربر Throne و با همان `--data-dir` اجرا کنید. برای یونیت سیستمی، از `sudo` استفاده کنید. |
| Windows: `[Instance] Not talking to … access denied` | pipe سرویس فقط برای Administrators و SYSTEM است. فرمان را از یک خط فرمان با دسترسی مدیر و با `--data-dir C:\ProgramData\Throne` اجرا کنید. |
| thronectl: `Throne closed the connection without a response` | کلید نادرست است، یا نشانی شما پس از 5 تلاش ناموفق به مدت 60 ثانیه رد می‌شود، برای مثال به خاطر کلاینت دیگری با کلید قدیمی. `THRONE_KEY_FILE` را بررسی کنید و یک دقیقه صبر کنید. |
| thronectl: `forbidden` | یک [درخواست مدیریتی](@/headless/thronectl.fa.md#admin-requests) از دستگاه دیگر. Throne را با `--api-admin-lan` اجرا کنید، یا فرمان را روی دستگاه خود Throne اجرا کنید. |
| thronectl: اتصال برقرار نمی‌شود | Throne در حال اجرا نیست، یا `THRONE_ADDR` به جای دیگری اشاره می‌کند. `systemctl status throne` و `Throne --print-connection` را بررسی کنید. |
| `thronectl tun on`: `needs_privileges` | Throne دسترسی‌های لازم برای TUN را ندارد. `Throne --check` را اجرا کنید و [دسترسی‌ها در Linux](@/headless/installation.fa.md#linux-privileges) را ببینید. |
| `thronectl proxy on`: `system_proxy_unsupported` | Throne بدون رابط گرافیکی پروکسی سیستمی ندارد. برنامه‌های دیگر را روی ورودی mixed تنظیم کنید، یا از TUN استفاده کنید. |
| `tun_conflict`: `the Tun address 172.19.0.1 is already used by the network interface br-…` | یک شبکهٔ Docker (یا شبکهٔ دیگری) از محدودهٔ TUN برنامهٔ Throne استفاده می‌کند. TUN را با `thronectl settings set tun_ipv4_cidr=172.29.0.1/24` به یک محدودهٔ آزاد ببرید (هر محدوده‌ای که هیچ رابط شبکه‌ای روی رایانه از آن استفاده نکند)، سپس دوباره `thronectl tun on` را اجرا کنید. یا به آن شبکهٔ Docker زیرشبکهٔ دیگری بدهید. |
| `tun_conflict`: `port 5533 on 127.0.0.1 (the core's DNS server, dns_in_port) is in use` | برنامهٔ دیگری پورت DNS را در اختیار دارد. `thronectl settings set dns_in_port=PORT` را با یک پورت آزاد اجرا کنید، سپس دوباره `thronectl tun on` را. |
| `tun_conflict` با نام یک Throne دیگر | Throne دیگری روی رایانه TUN را اجرا می‌کند، برای مثال یک Throne دسکتاپ. در هر زمان فقط یک Throne می‌تواند TUN را اجرا کند. |
| نمایه‌ها رد می‌شوند: `kill_switch_inactive` | کیل‌سوییچ روشن است اما نمی‌تواند کار کند. `kill_switch_error` در `thronectl --json status` و خط گزارش `[Kill switch] Not active (<code>)` دلیل را می‌گویند: `privilege`، `unsupported`، `config` یا `overridden`. `thronectl settings set kill_switch=false` آن را خاموش می‌کند. [کیل‌سوییچ](@/advanced/kill_switch.fa.md) را ببینید. |
| `degraded: resume_suppressed` | نمایه‌ای که دوباره اجرا شد، در سه شروع پیاپی باعث توقف Throne یا هسته‌اش شد. نمایه را درست کنید، سپس آن را با `thronectl connect <id>` اجرا کنید. |
| `degraded: core_gave_up` | هسته پشت سر هم شکست می‌خورد. Throne [روشن می‌ماند](@/headless/recovery.fa.md#protection) و هر 5 دقیقه دوباره امتحان می‌کند. خطی در گزارش که دست کشیدن از هسته را اعلام می‌کند، با آخرین خطای هسته پایان می‌یابد. |
| `degraded: vpn_challenge_pending` یا `vpn_auth_failed` | یک نمایهٔ VPN به ورود به حسابی نیاز دارد که Throne بدون رابط گرافیکی نمی‌تواند انجامش دهد، یا اطلاعات ورود ذخیره‌شدهٔ آن رد شده است. برای کدهای یک‌بارمصرف، به نمایه یک [حساب OTP](@/advanced/vpn_profiles.fa.md#otp-manager) بدهید، یا اطلاعات ورود را در یک Throne دسکتاپ درست کنید و آن‌ها را با یک [پشتیبان](@/headless/thronectl.fa.md#from-desktop) منتقل کنید. |
| `previous_crash: true` | آخرین اجرا به‌درستی پایان نیافت. گزارش آن `config/logs/crashed-<time>.log` در پوشهٔ داده‌ها است. |
| Docker: پورت منتشرشدهٔ 2080 پاسخ نمی‌دهد | ورودی روی `127.0.0.1` گوش می‌دهد. `thronectl settings set inbound_address=0.0.0.0` را اجرا کنید و نمایه را دوباره اجرا کنید. |
| Docker: کانتینر پس از `thronectl shutdown` برمی‌گردد | `restart: unless-stopped` آن را پس از هر خروج دوباره شروع می‌کند. آن را با `docker compose stop` متوقف کنید. |
| macOS: Throne هر 10 ثانیه شروع می‌شود و خارج می‌شود | یک خطای پیکربندی که launchd دوباره امتحانش می‌کند. `/Library/Logs/Throne/throne.log` را بخوانید. |
| Windows: سرویس بی‌درنگ متوقف می‌شود | `sc.exe query Throne` کد خروج Throne را به‌صورت `SERVICE_EXIT_CODE` نشان می‌دهد. گزارش در `C:\ProgramData\Throne\config\logs` است. کد 78 اغلب به معنای مشکلی در [پوشهٔ داده‌ها](@/headless/installation.fa.md#windows-data-folder) است. |
| کیل‌سوییچ یا TUN دسترسی شما را قطع کرده است | Throne را یک بار با `--no-resume --no-kill-switch` شروع کنید. [بازیابی دسترسی](@/headless/recovery.fa.md#recovery) را ببینید. |

## آنچه باید در گزارش باگ بیاورید {#reporting}

اگر مشکل باقی ماند، [یک باگ گزارش دهید](@/help/bug_reports.fa.md) و این موارد را بیاورید:

- خروجی `Throne --check`،
- خروجی `Throne --health`،
- نحوهٔ اجرای Throne: بسته یا ایمیج و نسخهٔ آن، و مدیر سرویس،
- گزارش (log)، از شروع تا بروز مشکل، و اگر می‌توانید مشکل را بازتولید کنید، با `--debug`. برای کرش، `config/logs/crashed-<time>.log` را هم بیاورید.

نشانی سرورها، URLهای اشتراک و کلیدها را از آنچه منتشر می‌کنید حذف کنید. هرگز `api.key` را منتشر نکنید.
