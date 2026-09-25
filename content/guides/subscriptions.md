+++
title = "Subscriptions & Groups"
description = "Add and update subscriptions, set group options, User-Agent and HWID, front and landing proxies, and fix update problems."
weight = 10
toc = true
+++

A subscription is a link from your provider that returns a list of servers. Throne keeps each subscription in its own group and can update it for you. This page explains how to add and update subscriptions, which options a group has, and what to do when an update fails.

## Groups and subscriptions {#groups}

Every tab above the profile list is a group. A group has one of two types:

- **Basic.** Holds profiles that you add yourself, for example from links, files, QR codes or `Program` → `New profile`.
- **Subscription.** Also has a `URL`. Throne downloads the profile list from this address and keeps the group in line with it.

You choose the type when you create the group. You cannot change it later.

{% alert_info() %}
An update makes a subscription group match the provider's list. It removes profiles that are not in the list and undoes changes that you made to the others. Keep your own profiles in a Basic group.
{% end %}

## Add a subscription {#add-subscription}

### From the clipboard {#from-clipboard}

1. Copy the subscription address. It starts with `https://` or `http://`.
2. In Throne, press `Ctrl+V`, or choose `Program` → `Add profile from clipboard`.
3. Throne shows the address and asks "How to update?". Choose `Create new subscription group` and click `OK`.

Throne creates a group named after the host name in the address and downloads its profiles right away. The same question appears when the address comes from a file, a QR code or text that you drop on the window. The three choices do this:

| Choice | Result |
| --- | --- |
| `Add profiles to this group` | Downloads the list once and adds the profiles to the current group. Throne does not save the address, so these profiles are never updated. |
| `Create new subscription group` | Creates a subscription group and downloads it. |
| `Import HTTP proxy profile` | Treats the address as an HTTP proxy server and adds it as one profile. |

### Create the group yourself {#create-group}

1. Choose `Groups` → `Add new Group`.
2. Enter a `Name`.
3. Set `Type` to `Subscription`.
4. Paste the address into `URL`.
5. Click `OK`.
6. Right-click the new tab and choose `Update subscription`.

Creating a group does not download it. The group stays empty until the first update in step 6.

`Groups` → `Manage Groups` opens a window with all groups. You can also create groups there with `New group`. Each row shows the type, the number of profiles, the address and the time of the last update. If the provider sends quota information (the `Subscription-UserInfo` header), the row also shows `Used`, `Remain` and `Expire`. Each row has `Edit` and `Remove` buttons, and subscription rows also have `Update Subscription`.

### From a throne:// link {#from-link}

A `throne://addsub/…` link, for example on your provider's website, opens the `Add subscription` window with the name and address. Keep `Auto update` ticked if the group should take part in automatic updates, and click `OK`. Throne then creates the group and downloads it. See [Deep Links](@/advanced/deeplinks.md#addsub).

## Update a subscription {#update}

To update one group, use one of these:

- Right-click the group's tab and choose `Update subscription`.
- Select the tab and press `Ctrl+U`, or choose `Groups` → `Update subscription`.
- Click `Update Subscription` next to the group in `Groups` → `Manage Groups`.

`Groups` → `Update all subscriptions` updates every subscription group, including groups with `Skip automatic update`.

During an update, Throne:

- Downloads the list and compares it with the profiles in the group. Profiles that did not change keep their test results. Changed profiles are updated. New profiles are added, and profiles that are no longer in the list are deleted.
- Puts the profiles in the same order as the provider's list.
- Changes nothing if the response contains no profiles at all. The log then says "No profiles found in the subscription: *group* was left unchanged." This protects your group from an empty or blocked response.
- Gives up if the server sends no data for 10 seconds, or if the response is larger than 64 MB.

With `Settings` → `Basic Settings` → `Subscription` → `Clear servers before updating subscription` (off by default), Throne deletes the profiles of the group before each update, so their test results are lost.

### Change report {#change-report}

Every update writes a report to the `Logs` tab. It starts with `Change of` and the group name. Each line starts with `[+]` (added), `[~]` (updated), `[-]` (deleted) or `[=]` (kept). If nothing changed, the report says `Nothing`.

After you update one group by hand, Throne also shows the report in a window. To turn the window off, untick `Settings` → `Basic Settings` → `Subscription` → `Show the changes window after a manual subscription update`. Automatic updates and `Update all subscriptions` only write to the log.

### The profile you are using {#running-profile}

An update does not stop or delete the profile you are connected to. If the provider removed it, Throne keeps it and lists it in the report under "Still in use, so kept instead of deleted". To let Throne stop and delete such a profile instead, turn on `Settings` → `Basic Settings` → `Subscription` → `Allow stopping the active profile`.

If the provider changed the settings of the running profile, Throne saves the new settings, but the connection keeps the old ones. Start the profile again to use the new settings. A running [auto selector](@/guides/testing.md#auto-selector) restarts by itself when an update replaces profiles that it uses.

## Automatic updates {#auto-update}

Automatic updates are off by default. To turn them on:

1. Open `Settings` → `Basic Settings` → `Subscription`.
2. Next to `Subscription auto update`, tick `Enable`.
3. Set `Interval (minute, invalid if less than 30)`. The default is 30.
4. Click `OK`.

How automatic updates work:

- One interval applies to all groups. Each time it has passed, Throne updates every subscription group except groups with `Skip automatic update`.
- An interval of less than 30 minutes counts as off.
- Throne checks once a minute, and 10 seconds after it starts. An update that became due while Throne was closed runs soon after you open it.
- The `Runtime Stats` tab shows the time left in `Next sub update`.
- The log shows `Auto-update: running subscriptions` each time. Automatic updates never open the changes window.

## Group options {#group-options}

To change a group, right-click its tab and choose `Edit selected Group`, or choose `Groups` → `Edit current Group`.

| Setting | Default | What it does |
| --- | --- | --- |
| `Name` | – | The name on the tab. |
| `Type` | `Basic` | `Basic` or `Subscription`. You cannot change it after the group is created. |
| `Front Proxy` | `None` | A profile that every profile of this group connects through first. See [Front and landing proxy](#front-landing-proxy). |
| `Landing Proxy` | `None` | A profile that traffic leaves through after the group's profile. |
| `Auto Clear Unavailable Profiles` | off | After a URL test of this group's profiles, deletes the profiles that failed, without asking. |
| `URL` | – | The subscription address. Only for subscription groups. |
| `Skip automatic update` | off | Leaves this group out of automatic updates. Manual updates still work. |
| `Advanced` | – | Opens `Advanced Subscription Settings` (since 1.3.1). See [After each update](#after-update) and [User-Agent and HWID](#user-agent-and-hwid). |

If the group has profiles, the window also has `Copy profile share links` and `Copy profile share links (Deep Links)`. They copy the links of all profiles in the group.

## After each update {#after-update}

Since 1.3.1, a subscription group can clean itself up after each update. Open the group options, click `Advanced`, and use the `Update` part. All options are off by default.

| Setting | What it does |
| --- | --- |
| `Keep working profiles` | Profiles whose last test succeeded are kept when the subscription no longer lists them. |
| `Remove duplicate profiles` | Removes profiles that are exact copies of another profile. |
| `Remove insecure profiles` | Removes profiles whose traffic is not properly protected, the same as `Groups` → `Remove Insecure Configs`. |
| `Remove invalid profiles` | Removes profiles that the core rejects. Skipped while the core is unreachable. |
| `Run URL test` | Tests the group's profiles when the update is finished, after any test that is already running. |
| `Remove unavailable profiles` | Needs `Run URL test`. Removes the profiles that failed the test. |
| `Sort by latency` | Needs `Run URL test`. Sorts the group, fastest first. |

The change report lists every profile these options removed. They do not delete the profile you are connected to, unless `Allow stopping the active profile` is on.

## User-Agent and HWID {#user-agent-and-hwid}

When Throne downloads a subscription, it sends a `User-Agent` header that names the app. Some providers send a different list for each app, or refuse apps they do not know. You can change the value:

- For all groups: `Settings` → `Basic Settings` → `Subscription` → `User Agent`. If it is empty, Throne sends `Throne/` and its version, for example `Throne/1.3.1`.
- For one group (since 1.3.1): group options → `Advanced` → `Request` → `User Agent`. If it is empty, the group uses the global value.

Some providers also require a device ID (HWID). Throne sends it only if you turn it on:

- For all groups: tick `Enable sending HWID, device model, and OS version when updating subscription` on the `Subscription` tab. It is off by default. Hover over it to see the values that Throne would send.
- For one group: set `Send HWID` to `Keep Default` (follow the global setting), `On` or `Off`. The `HWID`, `OS`, `OS Version` and `Device Model` fields override the values for this group. You can edit them only while HWID sending is on for the group.

To send other values for all groups, fill in `Custom System Parameters (optional)` on the `Subscription` tab. Use this format, and leave out the values that you do not want to change:

```text
hwid=value,os=value,osVersion=value,model=value
```

Throne sends these values in the headers `x-hwid`, `x-device-os`, `x-ver-os` and `x-device-model`. For what they contain, see [Privacy](@/reference/privacy.md#hwid).

## Front and landing proxy {#front-landing-proxy}

A group can send the traffic of all its profiles through two extra profiles:

**Your device → `Front Proxy` → a profile of this group → `Landing Proxy` → WARP (if enabled) → Internet**

- Use a `Front Proxy` when your device cannot reach the group's servers directly.
- Use a `Landing Proxy` when websites should see the address of the landing proxy instead of the group's servers.

You can choose any saved profile from any group; type in the field to search. Auto selectors are not offered, because they change servers on their own. For chains and the rules for mixing cores, see [Proxy Chains & Custom Configs](@/advanced/chains.md#front-landing).

## Supported formats {#formats}

A subscription can return:

- Share links such as `vless://`, `vmess://`, `trojan://`, `ss://`, `hysteria2://` or `tuic://`, one per line, as plain text or Base64-encoded.
- Clash or Mihomo YAML with a `proxies:` list.
- sing-box JSON: a full config or a list of outbounds. Each supported outbound becomes a profile. A single outbound object becomes one custom outbound profile.
- Xray JSON. The outbounds of a config become profiles. A list of complete Xray configs becomes one `Custom Xray Config` profile per config.
- SIP008 (Shadowsocks JSON), WireGuard and AmneziaWG `.conf` files, OpenVPN `.ovpn` files, AnyConnect XML profiles and AmneziaVPN `vpn://` links.

Whether a `vless://` link becomes a sing-box or an Xray profile depends on `Settings` → `Basic Settings` → `Core` → `Xray VLESS Preference`. Throne applies it when it imports, so update your subscriptions again after you change it. See [sing-box vs Xray](@/advanced/xray.md#vless-preference). The full list of formats is in [Protocols & Import Formats](@/reference/protocols.md#import-formats).

## Problems {#problems}

Open the `Logs` tab first. Each update writes lines that start with `>>>>>>>>` and `<<<<<<<<`, including the error if there is one.

### The provider refuses Throne or sends no profiles {#problem-user-agent}

Some providers only answer apps that they know. The log then shows an error such as status code 403, or "No profiles found in the subscription". Set the group's `User Agent` (group options → `Advanced`) to the value your provider expects. Values that users needed include `ClashMeta`, `sing-box` and `Happ/1.0`.

### The provider requires a device ID {#problem-hwid}

If the provider asks for a device ID or fingerprint, turn on HWID sending: set `Send HWID` to `On` for the group, or turn it on for all groups on the `Subscription` tab.

### "Request with proxy but no profile started." {#problem-no-profile}

Throne sends its own requests, for example subscription updates, through its local proxy port when `Settings` → `Basic Settings` → `Miscellaneous` → `Use proxy` is on. It also does this whenever `System Proxy` is ticked. If no profile is running, there is no proxy and the request fails with this message. Start a profile first, or turn off `Use proxy` and `System Proxy`.

### The subscription address is blocked in your country {#problem-blocked}

1. Start a profile that works.
2. Turn on `Settings` → `Basic Settings` → `Miscellaneous` → `Use proxy`.
3. Update the subscription.

`Use proxy` needs the local proxy port, so it does not work while `Disable Mixed Inbound` is on.

### Happ and v2RayTun "crypt" links {#problem-crypt}

Links that start with `happ://crypt` or `v2raytun://crypt` are encrypted for those apps, and Throne cannot read them. Web pages such as `…/dl/happ-link/…` are not subscriptions either. Ask your provider for a normal subscription address that starts with `https://`.

### Profiles show up as `Custom Xray Config` {#problem-custom-config}

If the subscription returns a list of complete Xray configs, Throne imports each config as one profile of the type `Custom Xray Config` (called `Custom (Xray config)` in the profile editor). It removes the `inbounds` of each config and runs the rest as written. This is by design: such configs can contain load balancers and chains that only work as a whole. A sing-box config, in contrast, is split into one profile per outbound.

For more help, see [Troubleshooting](@/help/troubleshooting.md#subscriptions).

## On Android {#android}

Throne for Android has the same groups, options and update behavior.

- Open `Groups` from the side menu. Use `New group` and `Update all subscriptions` at the top. Each group shows its type, the number of profiles, the last update and, if the provider sends it, the quota ("Used … · … left · expires …").
- The group editor has the same options, written in sentence case: `Front proxy`, `Landing proxy`, `Auto clear unavailable profiles`, `Skip automatic update` and `Advanced`.
- `URL` also accepts a `content://` address, so a subscription can come from a file that another app provides. For a plain `http://` address, the editor warns "Cleartext HTTP traffic is insecure".
- The global options are in `Settings` → `Subscriptions`. If `User agent` is empty, the app sends `Throne/Android/` and its version.
- `Add profile` → `Import from clipboard` with an address asks the same "How to update?" question.
- The changes window appears only after a manual update of one group. Automatic updates only write to the log.

For Android-specific problems, see [Android Troubleshooting](@/android/troubleshooting.md#subscriptions).
