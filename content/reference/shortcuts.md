+++
title = "Keyboard Shortcuts & Tray"
description = "Keyboard shortcuts of Throne desktop, how to change them, global hotkeys, and what the tray icon and its menu do."
weight = 20
toc = true
+++

This page lists the keyboard shortcuts of Throne desktop, the global hotkeys you can set, and what the tray icon does. Shortcuts work while the Throne window is active. Global hotkeys work in every app, also when the Throne window is hidden.

**macOS:** `Ctrl` on this page means `Cmd` on a Mac, and `Alt` means `Option`. For example, `Ctrl+Shift+S` is `Cmd+Shift+S`. On a Mac laptop keyboard, `Del` is `Fn+Delete`.

## Main window {#main-window}

The toolbar buttons `Program`, `Settings`, `Groups`, `Routing` and `Tools` open the menus of the main window. The `Settings` and `Routing` menus have no shortcuts.

The column "Can change" shows whether you can set another shortcut in `Settings` → `Hotkey Settings`. See [Change a shortcut](#change-shortcuts).

### Program menu {#program-menu}

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Hide window` | `Ctrl+H` (macOS: also `Cmd+W`) | Yes |
| `New profile` | `Ctrl+N` | Yes |
| `Add profile from clipboard` | `Ctrl+V` | No |
| `Add profile from File(s)` | `Ctrl+O` | Yes |
| `Scan QR Code` | `Ctrl+Shift+Q` | Yes |

You can also drop files, images with a QR code, or links on the window to import them.

### Groups menu {#groups-menu}

The group actions work on the group of the open tab.

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Url Test Group` | `Ctrl+Shift+G` | Yes |
| `Speedtest Group` | `Ctrl+Alt+P` | Yes |
| `Resolve Domain for group` | `Ctrl+Shift+I` | Yes |
| `Clear Group test result` | `Ctrl+Shift+C` | Yes |
| `Update subscription` | `Ctrl+U` | Yes |
| `Remove Duplicates` | `Ctrl+Shift+D` | Yes |
| `Remove Unavailable` | `Ctrl+Shift+R` | Yes |
| `Remove Invalid` | `Ctrl+Alt+I` | Yes |
| `Stop Testing` | `Ctrl+.` | Yes |

`Stop Testing` appears in the menu only while a test is running.

Right-click a group tab to open that group and its menu. The tab menu has `Add new Group`, `Edit selected Group`, `Delete selected Group`, `Update subscription`, `Url Test selected Group` and `Speed Test selected Group`. Drag a tab to change the order of the groups.

### Tools menu {#tools-menu}

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Speedtest Current` | `F6` | Yes |

`Speedtest Current` works only while a profile is running.

### Status bar {#status-bar}

- Click the running profile on the left of the status bar to run a URL test of it.
- Click `Mixed: …` in the middle of the status bar to open `Basic Settings`.

## Profile list {#profile-list}

Right-click the profile list to open its menu. It has the same four "add" actions as the `Program` menu, plus these:

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Start` | `Enter` | No |
| `Stop` | `Ctrl+S` | No |
| `Share` → `Export Sing-box config` | `Ctrl+E` | Yes |
| `Share` → `Copy links of selected` | `Ctrl+C` | No |
| `Share` → `Copy links of selected (Deep Links)` | `Ctrl+Alt+C` | No |
| `Delete` | `Del` | No |
| `Select All` | `Ctrl+A` | No |
| `Clone` | `Ctrl+D` | Yes |
| `Url Test Selected` | `Ctrl+Shift+S` | Yes |
| `Speedtest Selected` | `Ctrl+Shift+P` | Yes |
| `Reset Traffic` | `Ctrl+R` | Yes |

Other keys and mouse actions in the list:

| Key or action | What it does |
| --- | --- |
| Double-click a profile | Opens the profile editor. |
| `Esc` | Clears the selection. |
| Drag a row | Moves the profile. This does not work while a filter is active. |
| Click a column header | Sorts by that column. Click it again to sort in the other direction. |
| `Ctrl+F` | Shows or hides the filter row. Hiding it clears the filters. |
| `Up` on the first row | Moves to the filter row, if it is open. |
| `Down` in the filter row | Moves back to the list. |
| `Esc` in the filter row | Closes the filter row. |

### Actions without a default shortcut {#no-default}

You can give a shortcut to these actions, which have none by default: `QR Code and link`, `Copy Test Result`, `Resolve Selected Domain`, `Resolve Selected Out IP`, `Clear Test Result`, `Resolve out IP for group`, `Update all subscriptions`, `Remove Insecure Configs` and `Refresh Column Widths`.

## Change a shortcut {#change-shortcuts}

1. Open `Settings` → `Hotkey Settings`.
2. Open the `Shortcuts` tab. It lists every action whose shortcut you can change.
3. Click the field next to an action and press the new key combination. To remove a shortcut, click the field and press `Backspace`.
4. Click `OK`.

If two actions have the same shortcut, neither of them works. The shortcuts marked "No" in the tables above cannot be changed, and `Ctrl+F` cannot be changed either.

## Global hotkeys {#global-hotkeys}

Global hotkeys work in any app, even when the Throne window is hidden. All of them are empty by default.

1. Open `Settings` → `Hotkey Settings`.
2. On the `Global` tab, click the field of a hotkey.
3. Press the key combination.
4. Click `OK`.

| Hotkey | What it does |
| --- | --- |
| `Trigger main window` | Shows the main window, or hides it if it is active. This is the same as clicking the tray icon. |
| `Show groups` | Opens the `Manage Groups` window. |
| `Show routes` | Opens `Routing Settings`. |
| `Proxy mode` | Opens the `Operation Mode` menu (`System Proxy`, `Tun Mode`) at the mouse pointer. |
| `Toggle System Proxy` | Turns `System Proxy` on or off. |

- If two global hotkeys use the same keys, Throne registers none of them.
- If another program already uses a key combination, that hotkey does not work. Choose a different one.
- Global hotkeys are paused while the `Hotkey Settings` window is open.
- **macOS:** `Trigger main window` has no effect. Use `Show Window` in the tray menu instead.
- **Linux:** global hotkeys use X11. In a Wayland session they may not work.

## Tray icon {#tray}

Throne shows an icon in the system tray. On macOS, the icon is in the menu bar. The icon changes when a profile is running and when `System Proxy` or `Tun Mode` is on. Hover over it to see the running profile and its location. The tooltip also shows the mode when one is on, and the active routing profile when it is not `Default`.

- **Windows and Linux:** click the icon to show the window, or to hide it if it is active. Right-click the icon to open the tray menu.
- **macOS:** click the icon to open the tray menu.

Closing the window does not quit Throne. The window hides, and Throne keeps running in the tray. To quit, choose `Exit` in the tray menu or in the `Program` menu.

**macOS:** while the window is hidden, Throne has no icon in the Dock.

**Linux:** GNOME shows tray icons only when the AppIndicator extension is installed ([#1623](https://github.com/throneproj/Throne/issues/1623)). Without a tray icon, you can still bring back a hidden window: start Throne again, and the running Throne shows its window.

### Tray menu {#tray-menu}

| Item | What it does |
| --- | --- |
| `Show Window` | Shows the main window. |
| `Start with system` | Starts Throne when you log in. |
| `Remember last profile` | At the next start, Throne starts the last running profile again and turns `System Proxy` and `Tun Mode` back on if they were on. |
| `Allow other devices to connect` | Opens the local proxy port to other devices on your network. See [LAN sharing](@/guides/proxy_modes.md#lan-sharing). |
| `Select Profile` | Opens a small list of your groups. Choose a group, then a profile to start it, or type to search all profiles. The running profile has a check mark. The `Stop: <name>` button stops it. |
| `Select Routing` | Lists your routing profiles. Choosing one makes it active and restarts the running profile. |
| `OTP Codes` | Lists your OTP profiles. Click one to copy its current code. |
| `Operation Mode` → `System Proxy`, `Tun Mode` | Turns system proxy or TUN mode on or off. |
| `Restart Core` | Restarts the core. |
| `Restart Program` | Restarts Throne. |
| `Exit` | Quits Throne. |

`Start with system` works differently on each system:

- **Windows:** Throne adds a Task Scheduler task. The window opens at login unless `Hide dashboard at startup` is on. Each time Throne starts, it sets the task to the rights of the running Throne: if Throne runs as administrator, the task also starts it as administrator, unless `Always Start as Standard User` is on.
- **Linux:** Throne adds `Throne.desktop` to `~/.config/autostart` with the option `-tray`, so it starts in the tray.
- **macOS:** Throne adds a login item. The window opens at login unless `Hide dashboard at startup` is on.

### Tray settings {#tray-settings}

These settings are in `Settings` → `Basic Settings` → `Style`.

| Setting | Default | What it does |
| --- | --- | --- |
| `Hide dashboard at startup` | Off | Throne starts with only the tray icon, and the window stays hidden. The command-line option `-tray` does the same. |
| `Disable tray` | Off | Removes the tray icon. Closing the window then quits Throne. |

{% alert_warning() %}
Do not turn on `Disable tray` together with `Hide dashboard at startup` or `-tray`. Throne would then start with no window and no tray icon. If this happens, start Throne again: the running Throne shows its window.
{% end %}
