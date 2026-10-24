+++
title = "بررسی سلامت و گزارش‌ها"
description = "بررسی کنید که آیا یک رایانه می‌تواند Throne بدون رابط گرافیکی را اجرا کند، وضعیت Throne در حال اجرا را از خودش بپرسید، وضعیت systemd آن را بخوانید و گزارش‌هایش را پیدا کنید."
weight = 40
toc = true
+++

Throne بدون رابط گرافیکی دو بررسی داخلی دارد: `Throne --check` پیش از نخستین اجرا یا وقتی چیزی کار نمی‌کند، و `Throne --health` برای Throne در حال اجرا. همچنین وضعیت خود را به systemd اعلام می‌کند و گزارش (log) می‌نویسد.

## Throne --check {#check}

`Throne --check` به شما می‌گوید که آیا این رایانه می‌تواند Throne بدون رابط گرافیکی را با پیکربندی فعلی اجرا کند. آن را با کاربر Throne و با همان گزینه‌ها و متغیرهایی که Throne با آن‌ها شروع می‌شود اجرا کنید. این فرمان هیچ چیزی را تغییر نمی‌دهد: هیچ فایلی نمی‌سازد، هیچ قفلی نمی‌گیرد، پایگاه‌داده را فقط‌خواندنی باز می‌کند و در کنار یک Throne در حال اجرا هم اجرا می‌شود.

برای هر مورد یک خط چاپ می‌کند، و هر جا راه‌حلی وجود داشته باشد، خطوط `fix:` را هم:

```text
$ sudo /opt/Throne/Throne --check
[INFO] build: Throne <version>, Qt 6.x, Debian GNU/Linux 12 (bookworm) x86_64, kernel 6.1.0-28-amd64, euid 0, ruid 0
[INFO] data dir /var/lib/throne (root default): does not exist yet; the first start creates it
[ OK ] instance: none (no data dir yet)
...
[INFO] API key: /var/lib/throne/config/api.key is created on the first start
[ OK ] port 127.0.0.1:9095 (the Throne API, the headless default): free
[ OK ] port 127.0.0.1:2080 (the mixed proxy, inbound_port): free
...
result: 0 failed, 0 warnings
```

این فرمان این موارد را پوشش می‌دهد: بیلد، پوشهٔ داده‌ها، نمونهٔ در حال اجرا، تنظیمات، TLS، هسته، TUN، کیل‌سوییچ، کلید API، پورت‌ها (API، ورودی mixed، پورت DNS، و Clash API و sing-box API وقتی روشن باشند)، Throneهای بدون رابط گرافیکی دیگر و مالکان TUN روی رایانه، مدیر سرویس و حالت راه‌اندازی دوباره، و [شناسهٔ دستگاه](@/headless/_index.fa.md#device-id).

فقط چیزی که به‌طور کلی مانع کار کردن Throne شود `[FAIL]` است، و در این صورت فرمان با کد 1 خارج می‌شود. نبود دسترسی‌های لازم برای TUN یا کیل‌سوییچ `[WARN]` است، همراه با فرمان‌های `setcap` یا `chmod u+s` برای رفع آن، یا در کانتینر همراه با `--cap-add NET_ADMIN` و `--device /dev/net/tun`.

## Throne --health {#health}

`Throne --health` از طریق سوکت نمونه (instance)، از Throne در حال اجرا می‌پرسد و یک خط JSON چاپ می‌کند. آن را با کاربر Throne و برای همان پوشهٔ داده‌ها اجرا کنید:

```bash
$ sudo /opt/Throne/Throne --health
{"api":"listening","core_restarts":0,"degraded":null,"headless_dialogs":0,"ok":true,"previous_crash":false,"previous_exit":{"at":1760700000,"code":75,"reason":"restart requested"},"ready":true,"state":"running","stuck_s":0}
```

وقتی Throne سالم باشد، با کد 0 خارج می‌شود. برای کدهای دیگر، [کدهای خروج](@/headless/command_line.fa.md#exit-codes) را ببینید.

| فیلد | معنی |
| --- | --- |
| `ok` | Throne کار می‌کند: شروع شده است، هسته متصل است، هیچ چیزی گیر نکرده است، Throne از هسته دست نکشیده است، و کیل‌سوییچ خاموش است یا کار می‌کند. کیل‌سوییچی که با پیکربندی فعلی نمی‌تواند کار کند، یا `--no-kill-switch` آن را خاموش کرده است، این مقدار را `true` نگه می‌دارد، چون راه‌اندازی دوباره نمی‌تواند آن را درست کند. این مقدار هرگز به یک سرور راه‌دور یا به نمایهٔ در حال اجرا بستگی ندارد، بنابراین راه‌اندازی دوبارهٔ Throne در زمانی که این مقدار `false` است، هنگام از کار افتادن یک سرور به چرخهٔ بی‌پایان نمی‌افتد. |
| `ready` | Throne شروع به کار را تمام کرده است. |
| `state` | `idle`، `connecting`، `running`، `stopping`، یا `starting` تا وقتی Throne شروع به کار کند. |
| `degraded` | `null`، یا دلیل اینکه Throne نمی‌تواند با پیکربندی فعلی کار کند. جدول زیر را ببینید. |
| `stuck_s` | چند ثانیه است که یک نمایه، فراتر از 90 ثانیهٔ نخست، در حال اتصال است، یا فراتر از 45 ثانیهٔ نخست، در حال توقف است؛ در غیر این صورت 0. تا وقتی بیشتر از 0 است، `ok` برابر `false` است. |
| `core_restarts` | تعداد دفعاتی که هسته دوباره راه‌اندازی شده است. |
| `headless_dialogs` | پرسش‌هایی که چون پنجره‌ای وجود ندارد نادیده گرفته شده‌اند. این مقدار باید 0 بماند. گزارش آن‌ها را در خطوط `HEADLESS-DIALOG` نام می‌برد. |
| `previous_crash` | اجرای قبلی به‌درستی پایان نیافته است: کرش، `kill -9` یا قطع برق. |
| `previous_exit` | اینکه اجرای قبلی چگونه پایان یافت، به‌صورت `{code, reason, at}` (`at` بر حسب ثانیه از 1970)، یا `null`. پس از اینکه مدیر سرویس Throne را دوباره شروع کرد (کدهای 75، 70، 71)، دلیل در اینجا باقی می‌ماند. |
| `api` | شنوندهٔ API: `off`، `listening`، `key_invalid`، `failed`، `retrying` (تا 30 ثانیه برای نشانی‌اش صبر می‌کند) یا `address_missing` (نشانی‌اش از همهٔ رابط‌های شبکه حذف شده است). |

در نخستین لحظه‌های شروع، این خط فقط `ok`، `ready`، `state` و `headless_dialogs` را دارد.

مقدارهای `degraded`. وقتی چند مورد صدق کنند، Throne نخستین مورد را به این ترتیب گزارش می‌کند:

| مقدار | معنی |
| --- | --- |
| `core_gave_up` | هسته پشت سر هم شکست خورد و Throne از آن دست کشید. Throne برای مدیر سرویس با کد 70 خارج می‌شود، یا پس از سه شروع پیاپی از این دست، [روشن می‌ماند](@/headless/recovery.fa.md#protection) و هر 5 دقیقه هسته را دوباره امتحان می‌کند. |
| `core_unavailable` | پردازهٔ هسته در حال اجرا نیست. |
| `kill_switch_failed` | کیل‌سوییچ روشن است اما شکست خورده است. نمایه‌ها رد می‌شوند. [کیل‌سوییچ](@/advanced/kill_switch.fa.md) را ببینید. |
| `api_unavailable` | API روشن است اما گوش نمی‌دهد، برای مثال چون برنامهٔ دیگری پورت آن را در اختیار دارد یا فایل کلیدش قابل استفاده نیست. `ok` همچنان `true` می‌ماند. |
| `tun_unavailable` | TUN وقتی Throne آخرین بار متوقف شد روشن بود، و Throne اکنون نمی‌تواند آن را روشن کند: دسترسی‌های لازم را ندارد، یا چیز دیگری TUN را در اختیار دارد ([تداخل TUN](@/headless/_index.fa.md#beside-desktop)). Throne نمایه را بدون TUN اجرا نکرد. `thronectl tun off` این وضعیت را پاک می‌کند؛ سپس نمایه را با `thronectl connect` اجرا کنید. |
| `resume_suppressed` | Throne آخرین نمایه را دوباره اجرا نکرد، چون در هر یک از سه بار آخری که این کار را کرد، Throne یا هسته‌اش در کمتر از یک دقیقه متوقف شد. نمایه را با `thronectl connect` اجرا کنید؛ وقتی یک دقیقه اجرا شد، این وضعیت پاک می‌شود. |
| `vpn_auth_failed` | سرور یک نمایهٔ VPN اطلاعات ورود ذخیره‌شدهٔ آن را رد کرد. وقتی نمایه متوقف شود، این وضعیت پاک می‌شود. |
| `vpn_challenge_pending` | سرور یک نمایهٔ VPN چیزی می‌خواهد که Throne خودش نمی‌تواند به آن پاسخ دهد، مانند ورود به حساب از طریق وب. Throne وقتی مهلت پرسش تمام شود، حداکثر پس از 5 دقیقه، آن را لغو می‌کند. |

[مشخصات API](https://github.com/throneproj/Throne-api/blob/main/spec/api.md#headless-throne) این مقدارها را با جزئیات توضیح می‌دهد.

ایمیج Docker از `Throne --health` برای بررسی سلامت استفاده می‌کند. یک اسکریپت پایش (monitoring) که اطلاعات بیشتری می‌خواهد، می‌تواند خط `HEALTH` را به سوکت `config/.instance` در پوشهٔ داده‌ها بفرستد:

```bash
echo HEALTH | sudo socat -t 3 - UNIX-CONNECT:/var/lib/throne/config/.instance
```

پاسخ، `mode`، `pid`، `uptime_s`، `version`، `tun_running`، بلوک کامل `api` و فیلدهای `thronectl status` را هم دارد. اگر مسیر پوشهٔ داده‌ها 100 بایت یا بیشتر باشد، یا فایل‌سیستم آن سوکت نداشته باشد، سوکت به `headless-<hash>` منتقل می‌شود: برای root در `/run/throne` (در macOS، `/var/run/throne`) و برای کاربران دیگر در `/tmp/throne-<uid>`. در Windows، از `--health` استفاده کنید.

## systemd: آمادگی، وضعیت و watchdog {#systemd}

یونیت عرضه‌شده از نوع `Type=notify` است. Throne از پردازهٔ اصلی خود این موارد را به systemd اعلام می‌کند:

- **`READY=1`** وقتی پوشهٔ داده‌ها را در اختیار گرفته است، پایگاه‌داده باز است، API گوش می‌دهد (یا شکست خورده است)، هسته متصل است، وضعیت کیل‌سوییچ مشخص شده است و نمایه‌ای که دوباره اجرا می‌شود در راه است. این معمولاً کمتر از 20 ثانیه طول می‌کشد. تا آن زمان Throne مهلت شروع را تمدید می‌کند، بنابراین `TimeoutStartSec=90` فقط شروعی را که گیر کرده است پایان می‌دهد. پس از سه شروع بدون هستهٔ کارا، به هر حال آمادگی را اعلام می‌کند.
- **`STATUS=`** که `systemctl status` آن را نشان می‌دهد: `Starting`، `Starting core`، `Core restarting 2/5`، `Idle`، `Connecting <profile>`، `Connected <profile>` (با ` (Tun)` وقتی TUN روشن است)، `Stopping <profile>`، `Degraded: <reason>`، `Stopping` و `Restarting`.
- **`WATCHDOG=1`** هر 20 ثانیه، تا وقتی حلقهٔ اصلی‌اش در حال اجراست (یک‌سوم `WatchdogSec=60`). اگر حلقهٔ اصلی گیر کند، systemd سیگنال `SIGABRT` را می‌فرستد و Throne را دوباره شروع می‌کند.
- **`STOPPING=1`** وقتی خروج را آغاز می‌کند، یا `RELOADING=1` پیش از اینکه در همان پردازه دوباره راه‌اندازی شود (`--restart-mode exec`).

Throne همچنین، با یا بدون systemd، پیشرفت کار خودش را زیر نظر دارد: نمایه‌ای که 180 ثانیه در حال اتصال یا 90 ثانیه در حال توقف باشد باعث می‌شود Throne با کد 71 خارج شود، و هسته‌ای که 60 ثانیه قابل استفاده نبوده باشد باعث می‌شود با کد 70 خارج شود. سپس مدیر سرویس آن را دوباره شروع می‌کند.

`KillMode=mixed` الزامی است. با آن، systemd سیگنال `SIGTERM` را فقط به Throne می‌فرستد، و Throne هسته و کیل‌سوییچ را به‌ترتیب متوقف می‌کند و سپس خارج می‌شود، معمولاً در چند ثانیه (`TimeoutStopSec=45`). `SIGTERM` یا `SIGINT` دوم هسته را بی‌درنگ می‌بندد (kill). از `systemctl kill` استفاده نکنید: این فرمان مستقیماً به هسته و برنامهٔ کمکی کیل‌سوییچ سیگنال می‌فرستد.

## گزارش‌ها {#logs}

Throne گزارش خود را در خروجی خطای استاندارد (standard error) و در `config/logs/throne.log` درون پوشهٔ داده‌ها می‌نویسد. محل خواندن آن:

| نحوهٔ اجرای Throne | گزارش |
| --- | --- |
| یونیت سیستمی systemd | `journalctl -u throne -f` |
| یونیت کاربری systemd | `journalctl --user -u throne -f` |
| Docker | `docker compose logs -f throne` |
| LaunchDaemon در macOS | `/Library/Logs/Throne/throne.log` |
| سرویس Windows | `C:\ProgramData\Throne\config\logs\throne.log` (سرویس خروجی خطای استاندارد ندارد) |

`thronectl logs` گزارش را از طریق API می‌خواند، از هر دستگاهی که اجازهٔ فرستادن [درخواست‌های مدیریتی](@/headless/thronectl.fa.md#admin-requests) را دارد: `thronectl logs -n 500` آخرین 500 خط را چاپ می‌کند، و `thronectl logs -f` پس از آن خطوط جدید را هم چاپ می‌کند، حتی وقتی Throne دوباره راه‌اندازی می‌شود. این‌ها همان خطوطی هستند که پنجرهٔ گزارش برنامهٔ دسکتاپ نشان می‌دهد، همراه با خروجی هسته؛ Throne جدیدترین 5000 خط را در حافظه نگه می‌دارد. صفحهٔ `Logs` در [رابط وب](@/headless/web.fa.md) همین خطوط را در مرورگر نشان می‌دهد.

Throne بدون رابط گرافیکی گزارش‌ها را به زبان انگلیسی می‌نویسد. `--debug` خطوط debug را اضافه می‌کند. `--log-format` قالب خروجی خطای استاندارد را تعیین می‌کند:

| قالب | خطوط |
| --- | --- |
| `auto` | وقتی خروجی خطای استاندارد به journal در systemd می‌رود `journal`، در غیر این صورت `plain` |
| `journal` | هر خط با یک اولویت syslog مانند `<4>` شروع می‌شود که journald آن را به اولویت پیام تبدیل می‌کند. journald زمان را اضافه می‌کند. |
| `plain` | هر خط با زمان محلی شروع می‌شود. |

خطوطی که ارزش جست‌وجو دارند:

- `EXIT <code>: <reason>`: چرا Throne خارج شد. [کدهای خروج](@/headless/command_line.fa.md#exit-codes) را ببینید.
- `Ready <n> ms after launch`: شروع به کار تمام شده است.
- `[API] Listening on …`: جایی که API گوش می‌دهد.
- `[Resume] …`: اینکه آیا آخرین نمایه دوباره اجرا شد یا نه.
- `[Kill switch] Not active (<code>): …`: چرا کیل‌سوییچ کار نمی‌کند.
- `[Watchdog] …`: بررسی‌های خود Throne روی پیشرفت کارش.
- `HEADLESS-DIALOG`: پرسشی که کسی نتوانست به آن پاسخ دهد.

وقتی یک اجرا به‌درستی پایان نیابد، گزارش آن با نام `config/logs/crashed-<time>.log` نگه داشته می‌شود و گزارش‌های کرش به `config/crashes/` می‌روند.
