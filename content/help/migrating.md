+++
title = "Coming from Nekoray / NekoBox"
description = "Where Nekoray and NekoBox features are in Throne, and how to move your servers, subscriptions and settings."
weight = 40
toc = true
+++

Throne continues Nekoray, so most things work the same way, but some features moved or were replaced. This page shows where to find them and how to move your data. For background, see [How is Throne different from Nekoray?](@/help/faq.md#nekoray)

## Where did it go? {#where-did-it-go}

| In Nekoray / NekoBox you used… | In Throne you use… |
| --- | --- |
| The `Server` menu | Right-click the profile list. The menu bar is hidden. |
| The `Preferences` menu | The `Settings` button in the toolbar: `Basic Settings`, `Routing Settings`, `Tun Settings`, `Hotkey Settings` and more. |
| Subscription groups | The same groups, under the `Groups` button. To update one, right-click its tab → `Update subscription`. |
| `Tun Settings` → `Bypass Process Name` (programs that skip the tunnel) | `processName:` rules in the `Direct` box of your routing profile, for example `processName:game.exe`. Or right-click a connection in the `Connections` tab → `Append process "<name>" to` → `Direct`. |
| `Tun Settings` → `Whitelist mode` (only listed programs use the tunnel) | A routing profile with `Default outbound` set to `direct`, and the programs (`processName:…`) or sites in the `Proxy` box. |
| `Tun Settings` → `Bypass CIDR` | `Tun Settings` → `Private Range Bypass` (address ranges that skip the tunnel), or `ip:` rules in the `Direct` box. |
| A routing `Preset` for your country | `Routing` → `Download Profiles` → `China`, `Iran` or `Russia`. |
| `Default Outbound` set to `bypass` or `block` | `Default outbound` set to `direct` or `block` in the routing profile. `block` is available since 1.2.0. |
| Themes such as FlatGray, LightBlue and BlackSoft | `Basic Settings` → `Style` → `Theme`. These themes are back since 1.1.5. |
| `Copy links of selected (Neko Links)` | Standard share links. Throne cannot read `nekoray://` or `sn://` links. |
| `Hijack` (its DNS server and `Redirect Settings`) or `System DNS` in Throne 1.3.1 and older | `Tun Mode`. These features are deprecated in 1.3.1 and will be removed in the next release. |
| NekoBox for Android | Throne for Android 2.0.0. See [below](#from-nekobox-android). |

For per-app routing, turn on `Tun Mode`. Apps that ignore the system proxy never reach Throne, so rules cannot apply to them in system proxy mode. See [Routing](@/guides/routing.md#simple-rules) and [Connections tab](@/guides/routing.md#connections-tab).

## Moving your data {#moving-data}

### From Nekoray {#from-nekoray}

Throne cannot read Nekoray's configuration folder, and it has no import tool for it. Move your data by hand:

1. In Nekoray, copy the URL of each subscription from its group settings.
2. In Throne, copy one subscription URL, press `Ctrl+V` in the main window, and choose `Create new subscription group`. Repeat this for each subscription.
3. For servers that you added by hand, select them in Nekoray and use `Server` → `Share` → `Copy links of selected`. In Throne, press `Ctrl+V` to import them.
4. Set up routing again: download a profile for your country with `Routing` → `Download Profiles`, or add your own rules. See [Routing](@/guides/routing.md).
5. Check the settings that you changed in Nekoray, such as the listen port, DNS servers and hotkeys, and set them again in Throne.

Do not run Nekoray and Throne at the same time with TUN mode or the system proxy on.

### From Throne 1.0.x {#from-1-0}

Throne 1.1.0 moved from Nekoray-style JSON files to a database (`throne.db`) and cannot read the old files. If you update 1.0.x in place, your profiles, groups and settings do not appear in the new version ([#1765](https://github.com/throneproj/Throne/issues/1765)). Keep a copy of the old version's folder, and move your subscriptions, share links and routing profiles by hand as described above. [#1202](https://github.com/throneproj/Throne/issues/1202) lists manual steps and a community script, which is not official.

Since 1.1.3, you can move data between Throne versions and computers with `Basic Settings` → `Backup and Restore`. See [Backup, Updates & Migration](@/guides/backup.md#backup-restore).

### From NekoBox for Android {#from-nekobox-android}

Throne for Android was called NekoBox for Android before. Version 2.0.0 is rebuilt on the desktop core, and it cannot update an older version:

- It is signed with a new key, so you must uninstall the old version first.
- It starts empty and cannot restore old Android backups (the backup files and WebDAV `.zip` files of version 1.6.x and older). It restores only `.thrbackup` files, including backups made with Throne desktop.

Before you uninstall the old version, copy your subscription URLs and the share links of the servers that you added by hand. If you also use Throne desktop, you can restore a desktop backup on the phone instead; see [Backup, Updates & Migration](@/guides/backup.md#desktop-android). Details: [Installation & Upgrade](@/android/installation.md#upgrading).
