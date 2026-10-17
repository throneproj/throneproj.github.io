+++
title = "Устранение неполадок"
description = "Типичные проблемы с headless Throne — от юнита, который не запускается, до конфликтов TUN и отклонённых запросов к API, — и что указать в отчёте об ошибке."
weight = 60
toc = true
+++

Начните с `Throne --check` и `Throne --health`, запущенных от имени пользователя Throne и с тем же `--data-dir` (см. [Проверки состояния и логи](@/headless/monitoring.ru.md)), и прочитайте последние строки лога. Строка `EXIT <code>: <reason>` сообщает, почему Throne завершился; каждый код объясняется в разделе [Коды завершения](@/headless/command_line.ru.md#exit-codes).

## Типичные проблемы {#symptoms}

| Симптом | Причина и решение |
| --- | --- |
| Юнит сразу завершается с ошибкой, а в логе есть `refusing to run as root with /var/lib/throne` | Другие пользователи могут записывать в каталог данных. Выполните `sudo chmod go-w /var/lib/throne /var/lib/throne/config`. |
| Код завершения 3: `… is in use by …` | Каталог данных занят другим Throne: приложением для компьютера, пользовательским юнитом или второй службой. Остановите другой экземпляр. |
| Приложение для компьютера сообщает `Throne is running in the background` и завершается | Headless Throne (обычно пользовательский юнит) использует каталог данных приложения для компьютера. Выполните `systemctl --user stop throne` или управляйте им через `thronectl`. См. [Работа рядом с Throne для компьютера](@/headless/_index.ru.md#beside-desktop). |
| `degraded: api_unavailable`, а в логе есть `[API] Not listening on 127.0.0.1:9095` | Порт 9095 занят другой программой. Throne пробует снова каждые 30 секунд. Другой порт можно выбрать с помощью `--api-listen PORT`. |
| `--print-connection`: `The API key is not in a file` | Настройки каталога данных включили API с собственным ключом, как это делает приложение для компьютера. Используйте этот ключ как `THRONE_KEY` (в приложении для компьютера: `Integration Settings` → `Throne API` → `Copy for scripts`) или запустите Throne с `--api-key-file`. |
| `--health` или `--print-connection`: `No headless Throne answered` | Запустите команду от имени пользователя Throne, с тем же `--data-dir`. Для системного юнита используйте `sudo`. |
| Windows: `[Instance] Not talking to … access denied` | Канал службы доступен только администраторам и SYSTEM. Выполните команду из командной строки с правами администратора, с `--data-dir C:\ProgramData\Throne`. |
| thronectl: `Throne closed the connection without a response` | Неверный ключ, или ваш адрес отклоняется на 60 секунд после 5 неудачных попыток, например из-за другого клиента со старым ключом. Проверьте `THRONE_KEY_FILE` и подождите минуту. |
| thronectl: `forbidden` | [Административный запрос](@/headless/thronectl.ru.md#admin-requests) с другого устройства. Запустите Throne с `--api-admin-lan` или выполните команду на устройстве, где работает Throne. |
| thronectl: нет подключения | Throne не запущен, или `THRONE_ADDR` указывает на другой адрес. Проверьте `systemctl status throne` и `Throne --print-connection`. |
| `thronectl tun on`: `needs_privileges` | Throne не хватает прав для TUN. Выполните `Throne --check` и см. [Права в Linux](@/headless/installation.ru.md#linux-privileges). |
| `thronectl proxy on`: `system_proxy_unsupported` | В headless Throne нет системного прокси. Направьте другие программы на смешанный порт или используйте TUN. |
| `tun_conflict`: `the Tun address 172.19.0.1 is already used by the network interface br-…` | Сеть Docker (или другая сеть) использует диапазон TUN Throne. Перенесите TUN в свободный диапазон командой `thronectl settings set tun_ipv4_cidr=172.29.0.1/24` (подойдёт любой диапазон, который не использует ни один сетевой интерфейс на компьютере), затем снова выполните `thronectl tun on`. Или задайте этой сети Docker другую подсеть. |
| `tun_conflict`: `port 5533 on 127.0.0.1 (the core's DNS server, dns_in_port) is in use` | DNS-порт занят другой программой. Выполните `thronectl settings set dns_in_port=PORT` со свободным портом, затем снова `thronectl tun on`. |
| `tun_conflict` с упоминанием другого Throne | TUN использует другой Throne на компьютере, например Throne для компьютера. TUN может одновременно использовать только один Throne. |
| Профили отклоняются: `kill_switch_inactive` | Kill switch включён, но не может работать. Причину сообщают `kill_switch_error` в `thronectl --json status` и строка лога `[Kill switch] Not active (<code>)`: `privilege`, `unsupported`, `config` или `overridden`. Выключить его можно командой `thronectl settings set kill_switch=false`. См. [Kill Switch](@/advanced/kill_switch.ru.md). |
| `degraded: resume_suppressed` | Возобновляемый профиль приводил к остановке Throne или его ядра при трёх запусках подряд. Исправьте профиль, затем запустите его командой `thronectl connect <id>`. |
| `degraded: core_gave_up` | Ядро постоянно падает. Throne [остаётся запущенным](@/headless/recovery.ru.md#protection) и пробует снова каждые 5 минут. Строка лога о прекращении попыток заканчивается последней ошибкой ядра. |
| `degraded: vpn_challenge_pending` или `vpn_auth_failed` | VPN-профилю нужен вход, который headless Throne не может выполнить, или его сохранённые учётные данные отклонены. Добавьте профилю [запись OTP](@/advanced/vpn_profiles.ru.md#otp-manager) для одноразовых кодов или исправьте учётные данные в Throne для компьютера и перенесите их с помощью [резервной копии](@/headless/thronectl.ru.md#from-desktop). |
| `previous_crash: true` | Последний запуск завершился некорректно. Его лог — `config/logs/crashed-<time>.log` в каталоге данных. |
| Docker: опубликованный порт 2080 не отвечает | Входящее подключение слушает `127.0.0.1`. Выполните `thronectl settings set inbound_address=0.0.0.0` и снова запустите профиль. |
| Docker: контейнер снова запускается после `thronectl shutdown` | `restart: unless-stopped` запускает его после каждого завершения. Остановите его командой `docker compose stop`. |
| macOS: Throne запускается каждые 10 секунд и завершается | Ошибка конфигурации, при которой launchd повторяет запуск. Прочитайте `/Library/Logs/Throne/throne.log`. |
| Windows: служба сразу останавливается | `sc.exe query Throne` показывает код завершения Throne как `SERVICE_EXIT_CODE`. Лог находится в `C:\ProgramData\Throne\config\logs`. Код 78 часто означает проблему с [папкой данных](@/headless/installation.ru.md#windows-data-folder). |
| Вы потеряли доступ из-за kill switch или TUN | Запустите Throne один раз с `--no-resume --no-kill-switch`. См. [Восстановление доступа](@/headless/recovery.ru.md#recovery). |

## Что указать в отчёте об ошибке {#reporting}

Если проблема не исчезает, [сообщите об ошибке](@/help/bug_reports.ru.md) и укажите:

- вывод `Throne --check`,
- вывод `Throne --health`,
- как работает Throne: пакет или образ и его версию, а также менеджер служб,
- лог от запуска до появления проблемы, с `--debug`, если можете воспроизвести проблему. При сбое также приложите `config/logs/crashed-<time>.log`.

Удалите адреса серверов, URL подписок и ключи из того, что публикуете. Никогда не публикуйте `api.key`.
