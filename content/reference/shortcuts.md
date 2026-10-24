+++
title = "Keyboard Shortcuts & Tray"
description = "Keyboard shortcuts of Throne desktop, the command palette, how to change shortcuts, global hotkeys, and what the tray icon and its menu do."
weight = 20
toc = true
+++

This page lists the keyboard shortcuts of Throne desktop, the global hotkeys you can set, and what the tray icon does. It also explains the command palette, which finds commands and settings by name. Shortcuts work while the Throne window is active. Global hotkeys work in every app, also when the Throne window is hidden.

**macOS:** `Ctrl` on this page means `Cmd` on a Mac, and `Alt` means `Option`. For example, `Ctrl+Shift+S` is `Cmd+Shift+S`. On a Mac laptop keyboard, `Del` is `Fn+Delete`.

## Main window {#main-window}

The toolbar buttons `Program`, `Settings`, `Groups`, `Routing` and `Tools` open the menus of the main window. The `Settings` and `Routing` menus have no shortcuts. Since 1.4.0, right-click a routing profile at the bottom of the `Routing` menu to open it in the routing profile editor without making it active; see [Routing profiles](@/guides/routing.md#profiles).

Since 1.4.0, a new installation starts in Simple mode, which hides some of the items on this page, for example `Resolve Domain for group`, `Export config` and `Reset Traffic`. See [Simple and Advanced mode](@/get_started/configuration.md#interface-mode).

The column "Can change" shows whether you can set another shortcut in `Settings` → `Integration Settings` (`Hotkey Settings` before 1.4.0). See [Change a shortcut](#change-shortcuts).

### Program menu {#program-menu}

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Hide window` | `Ctrl+H` (macOS: also `Cmd+W`) | Yes |
| `New profile` | `Ctrl+N` | Yes |
| `Add profile from clipboard` | `Ctrl+V` | No |
| `Add profile from File(s)` | `Ctrl+O` | Yes |
| `Scan QR Code` | `Ctrl+Shift+Q` | Yes |

You can also drop files, images with a QR code, or links on the window to import them.

The `Program` menu also has `Check For Update` and, since 1.4.0, `About`. `About` shows the versions of Throne, sing-box, Xray-core, Qt and Go. Before 1.4.0, `Check For Update` was in the `Tools` menu.

### Groups menu {#groups-menu}

The group actions work on the group of the open tab.

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Url Test Group` | `Ctrl+Shift+G` | Yes |
| `Speedtest Group` | `Ctrl+Alt+P` | Yes |
| `Resolve Domain for group` | `Ctrl+Shift+I` | Yes |
| `Clear Group test result` | `Ctrl+Shift+C` | Yes |
| `Update subscription` | `Ctrl+U` | Yes |
| `Clean up` → `Remove Duplicates` | `Ctrl+Shift+D` | Yes |
| `Clean up` → `Remove Unavailable` | `Ctrl+Shift+R` | Yes |
| `Clean up` → `Remove Invalid` | `Ctrl+Alt+I` | Yes |
| `Stop Testing` | `Ctrl+.` | Yes |

`Stop Testing` appears in the menu only while a test is running. Since 1.4.0, the remove actions, together with `Remove Insecure Configs`, are in the `Clean up` submenu.

Right-click a group tab to open that group and its menu. The tab menu has `Add new Group`, `Edit selected Group`, `Delete selected Group`, `Update subscription`, `Url Test selected Group` and `Speed Test selected Group`. Drag a tab to change the order of the groups.

### Tools menu {#tools-menu}

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Search Settings` | `Ctrl+K` | Yes |
| `Speedtest Current` | `F6` | Yes |

`Search Settings` opens the [command palette](#command-palette) (since 1.4.0). `Speedtest Current` works only while a profile is running.

### Status bar {#status-bar}

- Click the running profile on the left of the status bar to run a URL test of it.
- Click `Mixed: …` in the middle of the status bar to open `Basic Settings`.

## Command palette {#command-palette}

Since 1.4.0, the command palette finds menu commands and settings by name. To open it, press `Ctrl+K` in the main window, or click `Tools` → `Search Settings`. It opens in a window of its own, `Search Settings`.

- Without a query, it lists the commands of the menus `Program`, `Settings`, `Groups`, `Routing`, `Tools` and `Server`, which is the menu of the profile list. The `Routing` group also lists your routing profiles. Only the commands that the menus show at the moment are listed.
- Type one or more words to search. An entry matches when it contains all the words, in its name or in the path that follows it, for example `Basic Settings › Common › Inbound Settings`. The results are grouped under `Commands` and `Settings`. In a translated interface, English words also find many entries.
- Start the query with `>` to search only commands, or with `@` to search only settings. `@` alone lists all settings.
- Move with the arrow keys, `Tab`, `Page Up` and `Page Down`. Press `Enter` or double-click an entry to run it. `Esc` closes the palette.

A command runs as if you chose it in its menu. Its shortcut is shown on the right, and a command that is on or off, such as `Start with system`, shows a switch. Commands that are not available at the moment are greyed out.

A setting opens its settings window on the right tab, puts the cursor in the setting and outlines it for a moment. The palette finds the settings of `Basic Settings`, `Routing Settings`, `Tun Settings`, `Preset Settings` and `Integration Settings`. After you run an entry, the palette closes.

In Simple mode, a search also finds the settings that Simple mode hides, under "Settings in Advanced mode". Choosing one switches Throne to Advanced mode and then opens the setting. Menu commands that Simple mode hides are not listed. See [Simple and Advanced mode](@/get_started/configuration.md#interface-mode).

Only one of these windows can be open at a time: the settings windows, `Manage Groups`, `OTP Manager`, `Traffic Stats` and `About`. While one of them is open, the palette greys out the entries that would open another one and adds `close "<window>" first` to their path. The palette stays open, and these entries work again as soon as you close that window. The entries of the open window itself still work.

## Profile list {#profile-list}

Right-click the profile list to open its menu. It has the same four "add" actions as the `Program` menu, plus these:

| Action | Shortcut | Can change |
| --- | --- | --- |
| `Start` | `Enter` | No |
| `Stop` | `Ctrl+S` | No |
| `Share` → `Export config` | `Ctrl+E` | Yes |
| `Share` → `Copy links of selected` | `Ctrl+C` | No |
| `Share` → `Copy links of selected (Deep Links)` | `Ctrl+Alt+C` | No |
| `Delete` | `Del` | No |
| `Select All` | `Ctrl+A` | No |
| `Clone` | `Ctrl+D` | Yes |
| `Url Test Selected` | `Ctrl+Shift+S` | Yes |
| `Speedtest Selected` | `Ctrl+Shift+P` | Yes |
| `Reset Traffic` | `Ctrl+R` | Yes |

Since 1.4.0, `Export config` opens a window with the generated sing-box config and, for profiles that use Xray, the Xray config on its own tab. `Copy` copies the config of the open tab. Before 1.4.0, the item was `Export Sing-box config`, and some profiles also had `Export Xray config`.

Other keys and mouse actions in the list:

| Key or action | What it does |
| --- | --- |
| Double-click a profile | Opens the profile editor. |
| `Esc` | Clears the selection. |
| Drag a row | Moves the profile. This does not work while a filter is active. |
| Click a column header | Sorts by that column. Click it again to sort in the other direction. An arrow next to the column name shows the sorted column and the direction. |
| `Ctrl+F` | Shows or hides the filter row. Hiding it clears the filters. |
| `Up` on the first row | Moves to the filter row, if it is open. |
| `Down` in the filter row | Moves back to the list. |
| `Esc` in the filter row | Closes the filter row. |

### Actions without a default shortcut {#no-default}

You can give a shortcut to these actions, which have none by default: `QR Code and link`, `Copy Test Result`, `Resolve Selected Domain`, `Resolve Selected Out IP`, `Clear Test Result`, `Resolve out IP for group`, `Update all subscriptions`, `Remove Insecure Configs`, `IP Scanner` and `Refresh Column Widths`.

## Change a shortcut {#change-shortcuts}

1. Open `Settings` → `Integration Settings` (Advanced mode only, see [Simple and Advanced mode](@/get_started/configuration.md#interface-mode)).
2. Open the `Shortcuts` tab. It lists every action whose shortcut you can change.
3. Click the field next to an action and press the new key combination. To remove a shortcut, click the field and press `Backspace`.
4. Click `OK`.

The shortcuts marked "No" in the tables above cannot be changed, and `Ctrl+F` cannot be changed either. Since 1.4.0, the window marks a key combination that another action or a global hotkey already uses, names the conflict next to the buttons, and does not save until you change one of them.

## Global hotkeys {#global-hotkeys}

Global hotkeys work in any app, even when the Throne window is hidden. All of them are empty by default.

1. Open `Settings` → `Integration Settings`.
2. On the `Global Hotkeys` tab (`Global` before 1.4.0), click the field of a hotkey.
3. Press the key combination.
4. Click `OK`.

| Hotkey | What it does |
| --- | --- |
| `Trigger main window` | Shows the main window, or hides it if it is active. This is the same as clicking the tray icon. Since 1.4.0, it also works on macOS. |
| `Show groups` | Opens the `Manage Groups` window. |
| `Show routes` | Opens `Routing Settings`. |
| `Proxy mode` | Opens the `Operation Mode` menu (`System Proxy`, `Tun Mode`) at the mouse pointer. |
| `Toggle System Proxy` | Turns `System Proxy` on or off. |
| `Start/Stop Profile` | Stops the running profile, or starts the last profile when none runs (since 1.4.0). |
| `Toggle Tun Mode` | Turns `Tun Mode` on or off (since 1.4.0). |

- A global hotkey is one key combination. It needs `Ctrl`, `Alt` or `Meta` (`Cmd` on macOS), unless it is a function key such as `F9`, so that it does not block typing in other apps.
- If another program or a system shortcut already uses a key combination, that hotkey does not work. After you click `OK`, Throne lists the hotkeys it could not register, and the log shows "Global hotkey not registered" with the reason. Choose a different combination.
- Global hotkeys are paused while the `Integration Settings` window is open.
- **Linux:** since 1.4.0, global hotkeys work in X11 sessions and in KDE Plasma Wayland sessions. On KDE Plasma, they also appear in the system settings for shortcuts, under `Throne`. In other Wayland sessions they are not available, and the `Global Hotkeys` tab says "Global hotkeys are not supported in this desktop session."

To control Throne from a macro pad, a Stream Deck or a script, you can also use [thronectl](@/advanced/api.md#example-hotkey).

## Tray icon {#tray}

Throne shows an icon in the system tray. On macOS, the icon is in the menu bar. The icon changes when a profile is running and when `System Proxy` or `Tun Mode` is on. Since 1.4.0, it also shows when a profile is starting or stopping. Hover over it to see the running profile and its location. The tooltip also shows the mode when one is on, and the active routing profile when it is not `Default`.

- **Windows and Linux:** click the icon to show the window, or to hide it if it is active. Right-click the icon to open the tray menu.
- **macOS:** click the icon to open the tray menu.

Closing the window does not quit Throne. The window hides, and Throne keeps running in the tray. To quit, choose `Exit` in the tray menu or in the `Program` menu.

**macOS:** while the window is hidden, Throne has no icon in the Dock. Since 1.4.0, if you keep Throne in the Dock, click its Dock icon to show the window, also when it is minimized. Opening Throne again from Finder does the same.

**Linux:** GNOME shows tray icons only when the AppIndicator extension is installed ([#1623](https://github.com/throneproj/Throne/issues/1623)). Without a tray icon, you can still bring back a hidden window: start Throne again, and the running Throne shows its window.

### Tray menu {#tray-menu}

| Item | What it does |
| --- | --- |
| `Show Window` | Shows the main window. |
| `Connect` / `Disconnect` | Starts a profile when none runs, or stops the running one (since 1.4.0). It starts the profile that is selected in the list. With nothing selected, it starts the last profile, else the first profile of the open group. While a profile starts or stops, the item reads `Connecting` or `Disconnecting` and cannot be clicked. |
| `Start with system` | Starts Throne when you log in. |
| `Remember last profile` | At the next start, Throne starts the last running profile again and turns `System Proxy` and `Tun Mode` back on if they were on. |
| `Allow other devices to connect` | Opens the local proxy port to other devices on your network. See [LAN sharing](@/guides/proxy_modes.md#lan-sharing). |
| `Select Profile` | Opens a small list of your groups. Choose a group, then a profile to start it, or type to search all profiles. The running profile has a check mark. The `Stop: <name>` button stops it. |
| `Select Routing` | Lists your routing profiles. Choosing one makes it active and restarts the running profile. |
| `OTP Codes` | Lists your OTP profiles. Click one to copy its current code. Hidden in Simple mode. |
| `Operation Mode` → `System Proxy`, `Tun Mode` | Turns system proxy or TUN mode on or off. |
| `Restart Core` | Restarts the core. |
| `Restart Program` | Restarts Throne. |
| `Exit` | Quits Throne. |

`Start with system` works differently on each system:

- **Windows:** Throne adds a Task Scheduler task. The window opens at login unless `Hide dashboard at startup` is on. Each time Throne starts, it sets the task to the rights of the running Throne: if Throne runs as administrator, the task also starts it as administrator, unless `Always Start as Standard User` is on.
- **Linux:** Throne adds `Throne.desktop` to `~/.config/autostart` with the option `-tray`, so it starts in the tray.
- **macOS:** Throne adds a login item. The window opens at login unless `Hide dashboard at startup` is on.

If Throne cannot change the autostart entry, it shows "Could not update the autostart entry:" with the reason (since 1.3.2).

### Tray settings {#tray-settings}

These settings are in `Settings` → `Basic Settings` → `Style`.

| Setting | Default | What it does |
| --- | --- | --- |
| `Hide dashboard at startup` | Off | Throne starts with only the tray icon, and the window stays hidden. The command-line option `-tray` does the same. |
| `Disable tray` | Off | Removes the tray icon. Closing the window then quits Throne. |

{% alert_warning() %}
Do not turn on `Disable tray` together with `Hide dashboard at startup` or `-tray`. Throne would then start with no window and no tray icon. If this happens, start Throne again: the running Throne shows its window.
{% end %}
