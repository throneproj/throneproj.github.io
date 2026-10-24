+++
title = "Проверки состояния и логи"
description = "Как проверить, может ли компьютер запустить headless Throne, узнать состояние работающего Throne, прочитать его статус в systemd и найти его логи."
weight = 40
toc = true
+++

В headless Throne есть две встроенные проверки: `Throne --check` — перед первым запуском или когда что-то не работает, и `Throne --health` — для работающего Throne. Кроме того, он сообщает своё состояние systemd и пишет лог.

## Throne --check {#check}

`Throne --check` сообщает, может ли этот компьютер запустить headless Throne в текущей настройке. Запускайте эту команду от имени пользователя Throne, с теми же параметрами и переменными, с которыми запускается Throne. Она ничего не меняет: не создаёт файлов, не берёт блокировку, открывает базу данных только для чтения и может работать одновременно с запущенным Throne.

Команда выводит по одной строке на каждый пункт и строки `fix:` там, где есть способ исправления:

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

Она проверяет сборку, каталог данных, работающий экземпляр, настройки, TLS, ядро, TUN, kill switch, ключ API, порты (API, смешанный порт, DNS-порт, а также Clash API и API sing-box, если они включены), другие headless Throne и владельцев TUN на компьютере, менеджер служб и режим перезапуска, а также [идентификатор устройства](@/headless/_index.ru.md#device-id).

`[FAIL]` получает только то, что вообще не даёт Throne работать, и тогда команда завершается с кодом 1. Нехватка прав для TUN или kill switch — это `[WARN]` с командами `setcap` или `chmod u+s` для исправления либо, в контейнере, с `--cap-add NET_ADMIN` и `--device /dev/net/tun`.

## Throne --health {#health}

`Throne --health` обращается к работающему Throne через его сокет экземпляра и выводит одну строку JSON. Запускайте эту команду от имени пользователя Throne и для того же каталога данных:

```bash
$ sudo /opt/Throne/Throne --health
{"api":"listening","core_restarts":0,"degraded":null,"headless_dialogs":0,"ok":true,"previous_crash":false,"previous_exit":{"at":1760700000,"code":75,"reason":"restart requested"},"ready":true,"state":"running","stuck_s":0}
```

Команда завершается с кодом 0, если Throne исправен. Остальные коды см. в разделе [Коды завершения](@/headless/command_line.ru.md#exit-codes).

| Поле | Значение |
| --- | --- |
| `ok` | Throne работает: он запустился, ядро подключено, ничего не зависло, Throne не прекратил попытки запустить ядро, а kill switch выключен или работает. Kill switch, который не может работать в текущей настройке или который выключен параметром `--no-kill-switch`, оставляет значение `true`, потому что перезапуск этого не исправит. Значение никогда не зависит от удалённого сервера или запущенного профиля, поэтому перезапуск Throne при значении `false` не зацикливается во время сбоя на сервере. |
| `ready` | Throne завершил запуск. |
| `state` | `idle`, `connecting`, `running`, `stopping` или `starting`, пока Throne не запустился. |
| `degraded` | `null` или причина, по которой Throne не может работать в текущей настройке. См. таблицу ниже. |
| `stuck_s` | Сколько секунд профиль подключается сверх первых 90 секунд или останавливается сверх первых 45; иначе 0. Пока значение больше 0, `ok` равно `false`. |
| `core_restarts` | Сколько раз перезапускалось ядро. |
| `headless_dialogs` | Вопросы, пропущенные из-за отсутствия окна. Значение должно оставаться равным 0. Лог называет их в строках `HEADLESS-DIALOG`. |
| `previous_crash` | Предыдущий запуск завершился некорректно: сбой, `kill -9` или отключение питания. |
| `previous_exit` | Как завершился предыдущий запуск, в виде `{code, reason, at}` (`at` — в секундах с 1970 года), или `null`. Если менеджер служб перезапустил Throne (коды 75, 70, 71), причина сохраняется именно здесь. |
| `api` | Слушатель API: `off`, `listening`, `key_invalid`, `failed`, `retrying` (ждёт появления своего адреса до 30 секунд) или `address_missing` (его адрес исчез со всех сетевых интерфейсов). |

В первые моменты запуска строка содержит только `ok`, `ready`, `state` и `headless_dialogs`.

Значения `degraded`. Если подходят несколько, Throne сообщает первое в таком порядке:

| Значение | Что означает |
| --- | --- |
| `core_gave_up` | Ядро постоянно падало, и Throne прекратил попытки его запустить. Throne завершается с кодом 70 для менеджера служб или, после трёх таких запусков подряд, [остаётся запущенным](@/headless/recovery.ru.md#protection) и снова пробует запустить ядро каждые 5 минут. |
| `core_unavailable` | Процесс ядра не работает. |
| `kill_switch_failed` | Kill switch включён, но не сработал. Профили отклоняются. См. [Kill Switch](@/advanced/kill_switch.ru.md). |
| `api_unavailable` | API включён, но не слушает, например потому что его порт занят другой программой или его файл ключа нельзя использовать. `ok` остаётся `true`. |
| `tun_unavailable` | TUN был включён, когда Throne в последний раз остановился, а сейчас Throne не может его включить: ему не хватает прав или TUN занят чем-то другим ([конфликт TUN](@/headless/_index.ru.md#beside-desktop)). Throne не стал запускать профиль без TUN. `thronectl tun off` сбрасывает это состояние; затем запустите профиль командой `thronectl connect`. |
| `resume_suppressed` | Throne не возобновил последний профиль, потому что каждый из последних трёх раз, когда он это делал, Throne или его ядро останавливались в течение минуты. Запустите профиль командой `thronectl connect`; когда он проработает минуту, это состояние сбросится. |
| `vpn_auth_failed` | Сервер VPN-профиля отклонил его сохранённые учётные данные. Состояние сбрасывается, когда профиль останавливается. |
| `vpn_challenge_pending` | Сервер VPN-профиля запрашивает то, на что Throne не может ответить сам, например вход через веб. Throne отменяет запрос, когда истекает его срок, — не позже чем через 5 минут. |

Эти значения подробно описаны в [спецификации API](https://github.com/throneproj/Throne-api/blob/main/spec/api.md#headless-throne).

Образ Docker использует `Throne --health` как проверку состояния. Скрипт мониторинга, которому нужно больше данных, может отправить строку `HEALTH` в сокет `config/.instance` в каталоге данных:

```bash
echo HEALTH | sudo socat -t 3 - UNIX-CONNECT:/var/lib/throne/config/.instance
```

Ответ дополнительно содержит `mode`, `pid`, `uptime_s`, `version`, `tun_running`, полный блок `api` и поля `thronectl status`. Если путь к каталогу данных занимает 100 байт или больше либо его файловая система не поддерживает сокеты, сокет переносится в `headless-<hash>` в `/run/throne` (`/var/run/throne` в macOS) для root или в `/tmp/throne-<uid>` для остальных пользователей. В Windows используйте `--health`.

## systemd: готовность, статус и watchdog {#systemd}

Поставляемый юнит имеет тип `Type=notify`. Throne отправляет уведомления systemd из своего главного процесса:

- **`READY=1`** — когда он удерживает каталог данных, база данных открыта, API слушает (или запустить его не удалось), ядро подключено, kill switch пришёл в устойчивое состояние, а возобновляемый профиль запускается. Обычно это занимает меньше 20 секунд. До этого момента Throne продлевает тайм-аут запуска, поэтому `TimeoutStartSec=90` прерывает только зависший запуск. После трёх запусков без работающего ядра он всё равно сообщает о готовности.
- **`STATUS=`**, который показывает `systemctl status`: `Starting`, `Starting core`, `Core restarting 2/5`, `Idle`, `Connecting <profile>`, `Connected <profile>` (с ` (Tun)`, когда TUN включён), `Stopping <profile>`, `Degraded: <reason>`, `Stopping` и `Restarting`.
- **`WATCHDOG=1`** — каждые 20 секунд, пока работает его главный цикл (треть от `WatchdogSec=60`). Если главный цикл зависнет, systemd отправит `SIGABRT` и снова запустит Throne.
- **`STOPPING=1`** — когда он начинает завершаться, или `RELOADING=1` — перед перезапуском на месте (`--restart-mode exec`).

Throne также сам следит за ходом своей работы, с systemd или без него: если профиль подключается 180 секунд или останавливается 90 секунд, Throne завершается с кодом 71, а если ядро непригодно к работе в течение 60 секунд — с кодом 70. Затем менеджер служб снова запускает его.

`KillMode=mixed` обязателен. С ним systemd отправляет `SIGTERM` только самому Throne, а Throne по порядку останавливает ядро и kill switch и завершается, обычно за несколько секунд (`TimeoutStopSec=45`). Повторный `SIGTERM` или `SIGINT` сразу принудительно завершает ядро. Не используйте `systemctl kill`: эта команда отправляет сигналы напрямую ядру и вспомогательной программе kill switch.

## Логи {#logs}

Throne пишет лог в стандартный поток ошибок и в `config/logs/throne.log` в каталоге данных. Где его читать:

| Как работает Throne | Лог |
| --- | --- |
| Системный юнит systemd | `journalctl -u throne -f` |
| Пользовательский юнит systemd | `journalctl --user -u throne -f` |
| Docker | `docker compose logs -f throne` |
| LaunchDaemon в macOS | `/Library/Logs/Throne/throne.log` |
| Служба Windows | `C:\ProgramData\Throne\config\logs\throne.log` (у службы нет стандартного потока ошибок) |

`thronectl logs` читает лог через API с любого устройства, которому разрешено отправлять [административные запросы](@/headless/thronectl.ru.md#admin-requests): `thronectl logs -n 500` выводит последние 500 строк, а `thronectl logs -f` затем продолжает выводить новые, в том числе после перезапусков Throne. Это те же строки, что показывает окно лога в приложении для компьютера, включая вывод ядра; Throne хранит в памяти последние 5000. Страница `Logs` [веб-интерфейса](@/headless/web.ru.md) показывает те же строки в браузере.

Headless Throne пишет лог на английском языке. `--debug` добавляет отладочные строки. `--log-format` задаёт формат стандартного потока ошибок:

| Формат | Строки |
| --- | --- |
| `auto` | `journal`, если стандартный поток ошибок направлен в журнал systemd, иначе `plain` |
| `journal` | Каждая строка начинается с приоритета syslog, например `<4>`, который journald превращает в приоритет сообщения. Время добавляет journald. |
| `plain` | Каждая строка начинается с местного времени. |

Строки, которые стоит искать:

- `EXIT <code>: <reason>`: почему Throne завершился. См. [Коды завершения](@/headless/command_line.ru.md#exit-codes).
- `Ready <n> ms after launch`: запуск завершён.
- `[API] Listening on …`: где слушает API.
- `[Resume] …`: был ли снова запущен последний профиль.
- `[Kill switch] Not active (<code>): …`: почему kill switch не работает.
- `[Watchdog] …`: собственные проверки хода работы Throne.
- `HEADLESS-DIALOG`: вопрос, на который никто не смог ответить.

Если запуск завершился некорректно, его лог сохраняется как `config/logs/crashed-<time>.log`, а отчёты о сбоях попадают в `config/crashes/`.
