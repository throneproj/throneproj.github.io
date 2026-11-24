+++
title = "Keyboard Shortcuts & Tray"
description = "Keyboard shortcuts, Search Settings, global hotkeys and the tray icon of Throne desktop."
weight = 20
toc = true
+++

Shortcuts work while the Throne window is active. **macOS:** `Ctrl` means `Cmd` and `Alt` means `Option`, so `Ctrl+Shift+S` is `Cmd+Shift+S`. On a Mac laptop keyboard, `Del` is `Fn+Delete`.

## Main window {#main-window}

The `Settings` and `Routing` menus have no default shortcuts. The "Can change" column shows whether you can set another shortcut, see [Change a shortcut](#change-shortcuts).

In the status bar, click the running profile to URL-test it, or `Mixed: …` to open `Basic Settings`.

### Program menu {#program-menu}

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Hide window` | `Ctrl+H` (macOS: also `Cmd+W`) | Yes |
| `New profile` | `Ctrl+N` | Yes |
| `Paste from clipboard` | `Ctrl+V` | No |
| `Import from file` | `Ctrl+O` | Yes |
| `Scan QR code` | `Ctrl+Shift+Q` | Yes |

You can also drop files, QR code images or links on the window to import them.

### Groups menu {#groups-menu}

Group actions work on the group of the open tab.

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Update subscription` | `Ctrl+U` | Yes |
| `Test` → `URL test` | `Ctrl+Shift+G` | Yes |
| `Test` → `Speed test` | `Ctrl+Alt+P` | Yes |
| `Test` → `Resolve domains` | `Ctrl+Shift+I` | Yes |
| `Test` → `Stop testing` | `Ctrl+.` | Yes |
| `Test` → `Clear results` | `Ctrl+Shift+C` | Yes |

`Stop testing` works only while a test is running. Right-click a group tab for the group's menu; drag tabs to reorder the groups.

### Tools menu {#tools-menu}

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Search Settings` | `Ctrl+K` | Yes |
| `Speed test current connection` | `F6` | Yes |

`Search Settings` opens the [Search Settings](#command-palette) window. `Speed test current connection` works only while a profile is running.

## Search Settings {#command-palette}

`Search Settings` finds menu commands and settings by name. Press `Ctrl+K` in the main window, or click `Tools` → `Search Settings`.

- Type one or more words. An entry matches when its name or path, such as `Basic Settings › Connection › Local Proxy`, contains all of them. In a translated interface, English words also find many entries.
- Start with `>` to search only commands, or with `@` to search only settings. `@` alone lists all settings.
- Press `Enter` or double-click an entry to run it. `Esc` closes the window.

It finds the settings of `Basic Settings`, `Routing Settings`, `Tun Settings`, `Preset Settings` and `Integration Settings`, and the commands that the menus show at the moment, including the profile list menu and your routing profiles.

Only one of these windows can be open at a time: a settings window, `Manage Groups`, `OTP Manager`, `Traffic Statistics` and `About`. While one is open, `Search Settings` greys out entries that would open another one.

## Profile list {#profile-list}

Right-click a profile for its menu. Right-click an empty area of the list for `New profile`, `Paste from clipboard`, `Import from file`, `Scan QR code`, `Add subscription` and `Select all`.

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Start` | `Enter` | No |
| `Stop` | `Ctrl+S` | Yes |
| `Test` → `URL test` | `Ctrl+Shift+S` | Yes |
| `Test` → `Speed test` | `Ctrl+Shift+P` | Yes |
| `Share` → `Copy link` | `Ctrl+C` | No |
| `Share` → `Copy deep link` | `Ctrl+Alt+C` | No |
| `Share` → `Export config` | `Ctrl+E` | Yes |
| `Clone` | `Ctrl+D` | Yes |
| `Pin to top` / `Unpin` ([pinning](@/guides/testing.md#pin)) | – | Yes |
| `Reset traffic` | `Ctrl+R` | Yes |
| `Delete` | `Del` | No |
| `Select all` | `Ctrl+A` | No |

Other keys and mouse actions in the list:

| Key or action | What it does |
| --- | --- |
| Double-click a profile | Opens the profile editor. |
| `Esc` | Clears the selection. In the filter row, closes the filter row. |
| Drag a row | Moves the profile. This does not work while a filter is active. |
| `Ctrl+F` | Shows or hides the filter row. Hiding it clears the filters. |
| `Up` on the first row, `Down` in the filter row | Moves between the list and the filter row. |

### Actions without a default shortcut {#no-default}

Most other menu items have no default shortcut but can get one, for example `Edit`, `Pin to top`, `Add subscription`, `Service check`, `Exit IP`, `Copy test result`, the `Clean up` commands, `Manage groups`, the settings windows, the windows of the `Tools` menu, the `Exit through` choices, `Block ads`, `Route lookup`, `Toggle WARP`, `Restart core` and `Refresh column widths`.

## Change a shortcut {#change-shortcuts}

1. Open `Settings` → `Integration Settings` → `Shortcuts`. Each action is listed with its menu path, such as `Groups › Test › URL test`.
2. Click the field next to an action and press the new key combination. `Backspace` removes the shortcut.
3. Click `OK`.

Shortcuts marked "No" above, and `Ctrl+F`, cannot be changed. If another action or a global hotkey already uses the combination, the window names the conflict and does not save until you change one of them.

## Global hotkeys {#global-hotkeys}

Global hotkeys work in any app, even when the Throne window is hidden. All of them are empty by default.

1. Open `Settings` → `Integration Settings` → `Global Hotkeys`.
2. Click the field of a hotkey and press the key combination.
3. Click `OK`.

| Hotkey | What it does |
| --- | --- |
| `Trigger main window` | Shows the main window, or hides it if it is active, like a click on the tray icon. |
| `Manage groups` | Opens `Manage Groups`. |
| `Open Routing Settings` | Opens `Routing Settings`. |
| `Proxy mode` | Opens the `Proxy mode` menu (`System proxy`, `Tun mode`) at the mouse pointer. |
| `Toggle system proxy` | Turns `System proxy` on or off. |
| `Start/Stop Profile` | Stops the running profile, or starts the last profile when none runs. |
| `Toggle Tun mode` | Turns `Tun mode` on or off. |

- A hotkey needs `Ctrl`, `Alt` or `Meta` (`Cmd` on macOS), unless it is a function key such as `F9`.
- A combination that another program or the system already uses does not work. After you click `OK`, Throne lists the hotkeys it could not register.
- Global hotkeys are paused while `Integration Settings` is open.
- **Linux:** global hotkeys work in X11 and KDE Plasma Wayland sessions (on KDE Plasma they also appear in the system shortcut settings, under `Throne`), but not in other Wayland sessions.

To control Throne from a macro pad, a Stream Deck or a script, use [thronectl](@/advanced/api.md#example-hotkey).

## Tray icon {#tray}

Throne shows an icon in the system tray (on macOS, in the menu bar). The icon changes while a profile runs and when `System proxy` or `Tun mode` is on. Hover over it to see the running profile and mode.

- **Windows and Linux:** click the icon to show or hide the window. Right-click it for the tray menu.
- **macOS:** click the icon for the tray menu.

Closing the window does not quit Throne: it keeps running in the tray. To quit, choose `Quit` in the tray menu or the `Program` menu.

**macOS:** while the window is hidden, Throne has no Dock icon. If you keep Throne in the Dock, click its Dock icon to show the window, or open Throne again from Finder.

**Linux:** GNOME shows tray icons only with the AppIndicator extension ([#1623](https://github.com/throneproj/Throne/issues/1623)). Without a tray icon, start Throne again to bring back its hidden window.

### Tray menu {#tray-menu}

The first line of the tray menu shows the connected profile. Its `Program` submenu has `Start with system`, `Remember last profile` and `Allow other devices to connect`, as in the `Program` menu of the main window.

| Item | What it does |
| --- | --- |
| `Connect` / `Disconnect` | Stops the running profile, or starts the profile selected in the list, else the last profile, else the first profile of the open group. |
| `Profile: <name>` | Starts a profile chosen by group, or found by typing its name. Reads `Select profile` when there is no profile to show. |
| `Routing: <name>` | Makes a routing profile active and restarts the running profile. |
| `System proxy`, `Tun mode` | Turn these modes on or off, as in the main window. |
| `OTP codes` | Click an OTP entry to copy its current code. |
| `Show window` | Shows the main window. |
| `Program` → `Remember last profile` | At the next start, Throne starts the profile that was running when it quit, and turns `System proxy` and `Tun mode` back on if they were on. A profile you stopped yourself is not remembered. |
| `Program` → `Allow other devices to connect` | Opens the local proxy port to your network, see [LAN sharing](@/guides/proxy_modes.md#lan-sharing). |
| `Restart` → `Restart core`, `Restart program` | Restarts the core, or Throne itself. |
| `Quit` | Quits Throne. |

`Start with system` starts Throne when you log in. It adds a Task Scheduler task on Windows, a login item on macOS, and `Throne.desktop` with the option `-tray` to `~/.config/autostart` on Linux. On Windows and macOS, the window opens at login unless `Hide main window at startup` is on. On Windows, the task starts Throne as a standard user, also when the core has [administrator rights](@/guides/tun_mode.md#privileges-windows). It starts Throne as administrator only after the `Restart as administrator` fallback, unless `Always start as standard user` is on.

### Tray settings {#tray-settings}

In `Settings` → `Basic Settings` → `General` → `Window`:

| Setting | Default | What it does |
| --- | --- | --- |
| `Hide main window at startup` | Off | Throne starts with only the tray icon, like the command-line option `-tray`. |
| `Disable tray` | Off | Removes the tray icon. Closing the window then quits Throne. |

{% alert_warning() %}
Do not turn on `Disable tray` together with `Hide main window at startup` or `-tray`: Throne would start with no window and no tray icon. If this happens, start Throne again, and the running Throne shows its window.
{% end %}
