+++
title = "Расширенная настройка TUN в Windows"
description = "Снижение риска утечки DNS при использовании TUN-режима в Windows через системные политики и настройки браузера."
weight = 1

[extra]
+++

В этой статье показано, как уменьшить риск утечки DNS при использовании TUN-режима в Windows.

Утечка DNS может раскрыть реальные цели ваших подключений и сетевую активность, привести к потере приватности, облегчить анализ трафика провайдером и даже сделать прокси-правила менее эффективными.

## 1. Отключите Smart Multi-Homed Name Resolution в Windows

В среде с виртуальным сетевым адаптером возможны утечки DNS. При наличии нескольких сетевых интерфейсов Windows может использовать для DNS-запросов тот, который отвечает быстрее, из-за чего виртуальный адаптер обходится.

Рекомендуется отключить эту политику:

Если у вас нет редактора групповых политик (часто в Windows Home), можно применить настройку вручную через командную строку с правами администратора:

1. Скопируйте команду:

`reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v DisableSmartNameResolution /t REG_DWORD /d 1 /f`

2. Откройте меню «Пуск» и найдите `CMD`.
3. Найдите «Командная строка», нажмите правой кнопкой и выберите «Запуск от имени администратора».
4. Вставьте команду в окно и нажмите `Enter`.
5. После выполнения перезагрузите систему.

![Выполнение команды в CMD с правами администратора в Windows Home](/images/windows-tun-dns-leak/step1-home-edition-cmd.png)

![Отключение Smart Multi-Homed Name Resolution, шаг 1](/images/windows-tun-dns-leak/step1-disable-smart-multi-homed.png)

![Отключение Smart Multi-Homed Name Resolution, шаг 2](/images/windows-tun-dns-leak/step2-group-policy.png)

![Отключение Smart Multi-Homed Name Resolution, шаг 3](/images/windows-tun-dns-leak/step3-policy-disabled.png)

## 2. Отключите QUIC в браузере

На примере Chrome введите в адресной строке:

`chrome://flags/`

Найдите `QUIC` и установите значение `Disabled`.

![Отключение QUIC в браузере](/images/windows-tun-dns-leak/step4-disable-quic.png)
