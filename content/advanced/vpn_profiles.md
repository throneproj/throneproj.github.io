+++
title = "OpenVPN, OpenConnect & Tailscale"
description = "Import and set up OpenVPN, OpenConnect and Tailscale profiles, sign in with one-time codes, and run a work VPN next to your proxy."
weight = 50
toc = true
+++

Throne can connect to OpenVPN servers and to Cisco AnyConnect and compatible VPNs (OpenConnect), and it can join a Tailscale network. The VPN clients are built into the core, so you do not need to install OpenVPN or OpenConnect. This page covers import, the main options, signing in with one-time codes, and running a work VPN next to your proxy.

## OpenVPN {#openvpn}

Import a `.ovpn` file in one of these ways:

- `Program` → `Add profile from File(s)` (`Ctrl+O`).
- Drag the file onto the main window.
- Copy the text of the file and press `Ctrl+V` in the main window.

To create a profile by hand, use `Program` → `New profile` and set `Type` to `OpenVPN`.

What to know about the import:

- Only client profiles for `dev tun` work. TAP profiles (`dev tap`) and server configs are rejected.
- PKCS#12 bundles (`pkcs12`) are not supported. Export the CA, certificate and key as PEM, then paste them into `CA Certificate`, `Client Certificate` and `Client Key`.
- If the file keeps the login in a separate file (`auth-user-pass <file>`), enter `Username` and `Password` in the profile.
- Unknown or unsupported options are listed in the log, in lines that start with `OpenVPN:`. Options that do not apply to Throne, such as `up` and `down` scripts or `persist-tun`, are skipped without a message.
- If the file sends all traffic through the VPN (`redirect-gateway`), Throne turns off `Only route advertised network` for the profile.

The editor also has `Network` (empty means `udp`), `Static Challenge`, `MTU`, `OTP`, `Tunnel DNS`, the TLS files, and `Control Channel Wrap` for `tls-auth` and `tls-crypt` keys. `Advanced` opens more options.

## OpenConnect {#openconnect}

`Flavor` in the profile selects the type of server:

| `Flavor` | Server type |
| --- | --- |
| empty or `anyconnect` | Cisco AnyConnect and compatible servers |
| `gp` | Palo Alto GlobalProtect |
| `fortinet` | Fortinet |
| `f5` | F5 BIG-IP |
| `pulse` | Pulse Connect Secure |
| `nc` | Juniper Network Connect |

Throne imports these formats from a file, the clipboard or a subscription:

- An AnyConnect XML profile. Each server in its `<ServerList>` becomes a profile. Servers that use IPsec (IKEv2) and entries without an address are skipped with a note.
- An `openconnect` command line, for example `openconnect --protocol=gp --user=alice vpn.example.com`.
- A config file with one option per line that includes a `protocol=` line, such as `protocol=fortinet`.

Other main fields are `Username`, `Password`, `Auth Group` (preselects a group, realm or gateway), `Server Path` (the path part of the server URL, needed by some GlobalProtect, F5 and Fortinet portals), `MTU`, `OTP` and the TLS options. `Advanced` holds more, for example a session `Cookie` and a `Software Token`.

## Options for both VPN types {#vpn-options}

| Setting | Default | What it does |
| --- | --- | --- |
| `Only route advertised network` | On | When you start this profile, only traffic to the networks that the VPN server advertises enters the tunnel. Other traffic that reaches the profile is blocked. Routing rules that name this profile are not affected. Turn it off for a VPN that should carry all traffic. |
| `Tunnel DNS` | `Prefer` | How Throne uses the DNS servers that the VPN server sends. `None`: ignore them. `Prefer`: resolve only the names that the server claims (its split-DNS domains) through them. `Strict`: also send every remote DNS query to them, and fail the names they cannot answer. |
| `Username`, `Password` | empty | The login. `{otp}` in these fields becomes a one-time code, see [Use a code with a VPN profile](#bind-otp). |

For a routing-profile endpoint, `Prefer` and `Strict` both resolve only the names that the server claims.

## Signing in {#sign-in}

Throne signs in with the saved `Username` and `Password`. When the server asks for more, a `VPN Authentication` window opens:

- **A question or form**, for example a second password: fill it in and click `Submit`. Some requests show a time limit ("Expires in …").
- **A sign-in page:** the window shows an address and an `Open in Browser` button. Sign in in the browser, then close the window. The connection continues once the server accepts the sign-in.
- **Single sign-on that works only inside a browser** is not supported yet. Use a login with a username and password, or, for OpenConnect, enter a session `Cookie` in the profile's `Advanced` settings.

If the server rejects the saved login, Throne asks for a username and password for this session and offers `Reconnect`. They are not saved in the profile, and Throne forgets them when you stop the profile yourself. It asks up to three times.

The `Runtime Stats` tab at the bottom of the main window lists each VPN connection with its state and a `Details` button.

## OTP Manager {#otp-manager}

Many work VPNs ask for a one-time code from an authenticator app. Since 1.3.0, Throne has its own authenticator: `Tools` → `OTP Manager`.

Add entries:

- `Import` → `Add manually...`: enter a `Name` and the `Secret` (Base32). Change `Type` (`TOTP (time based)` or `HOTP (counter based)`), `Algorithm`, `Digits` (4 to 10, default 6) or `Period (seconds)` (default 30) only if your provider says so. The window shows the current code, so you can compare it with your other authenticator.
- `Import` → `From link or text...`: paste `otpauth://` links, an `otpauth-migration://` link (the export format of Google Authenticator), a JSON export, or just a Base32 secret.
- `Import` → `From clipboard` (or `Ctrl+V` in the window), or `From QR image file...`.
- `Scan QR Code` finds a QR code on your screen.

Use the entries:

- Click an entry to copy its current code.
- Drag entries to change their order.
- `Export` on an entry offers `This one as otpauth:// link and QR`, `All as otpauth-migration:// link and QR` and `All as JSON file...`.
- `Delete` removes an entry. Its secret cannot be recovered.
- The tray menu has `OTP Codes`, a searchable list of all codes. Click a code to copy it.

OTP entries are part of backups (`OTP profiles` in `Settings` → `Basic Settings` → `Backup and Restore`). Keep backup files private.

### Use a code with a VPN profile {#bind-otp}

1. Open the OpenVPN or OpenConnect profile.
2. In `OTP`, choose the entry.
3. If the server expects the code as part of the password, put `{otp}` where the code goes, for example `MyPassword{otp}`. For OpenConnect, `{otp}` also works in the software token and form fields.
4. Click `OK`.

Throne now fills in a fresh code each time it connects. It also answers the server's code prompts by itself: the OpenVPN challenge (enter the challenge text in `Static Challenge` if your server uses a static challenge) and the OpenConnect sign-in forms. If the server rejects a code, Throne tries a new one, up to three times. If the server rejects the whole login, Throne restarts the profile with a new code, up to three times, instead of asking you.

## Split tunnel: a work VPN next to your proxy {#split-tunnel}

Since 1.3.0, a routing profile can start OpenVPN or OpenConnect profiles next to the profile you run. Traffic to the networks that the VPN server advertises goes through the VPN. Everything else follows the routing profile, for example through your proxy.

1. Import or create the VPN profile.
2. Open `Routing` → `Routing Settings` → the `Route` tab.
3. Select the routing profile you use and click `Edit`.
4. Open the `Endpoints` tab. It appears only when you have an OpenVPN or OpenConnect profile, or a chain that ends with one.
5. Choose the VPN profile in the list and click `Add`.
6. Click `OK`, and make sure that this routing profile is the active one (it is ticked at the bottom of the `Routing` menu).
7. Start your normal profile. The VPN starts with it.

Each endpoint adds a rule named `<name> route prefer` to the `Advanced` tab, where `<name>` is the name of the VPN profile. You cannot edit this rule, but you can move it among your own rules: rules above it are checked first. Deleting the rule asks whether to remove the endpoint.

Limits:

- A profile used as an endpoint cannot also be the profile you start, or a hop of it.
- An endpoint can be a chain whose exit (the bottom row of the chain) is an OpenVPN or OpenConnect profile. Tick `Allow routing to inner hops` to get a rule for each OpenVPN or OpenConnect hop inside the chain too.
- Endpoint hops cannot run on Xray, and they cannot be Extra Core or full-config profiles.

For a complete example, see [Recipes](@/guides/recipes.md#corporate-vpn).

## Tailscale {#tailscale}

A Tailscale profile joins your tailnet, so you can reach your Tailscale devices or use one of them as an exit node. Tailscale profiles are available on desktop only.

1. Open `Program` → `New profile`.
2. Set `Type` to `Tailscale`.
3. Fill in the fields below. You create the `Auth key` in the Tailscale admin console.
4. Click `OK` and start the profile.

| Field | Default | What it does |
| --- | --- | --- |
| `State directory` | `$HOME/.tailscale` | Where the login state is stored. |
| `Auth key` | empty | The key used to log in to your tailnet. |
| `Control URL` | `https://controlplane.tailscale.com` | The coordination server. Change it only for a self-hosted control server. |
| `Hostname` | empty | The name of this device in the tailnet. |
| `Accept routes` | off | Use the subnet routes that other devices advertise. |
| `Ephemeral` | off | Register as an ephemeral device, which the tailnet removes after it goes offline. |
| `Exit node` | empty | Send internet traffic through this tailnet device. |
| `Exit node allow lan access` | off | Keep access to your local network while you use an exit node. |
| `Advertise exit node` | off | Offer this computer as an exit node. |
| `Advertise routes` | empty | Subnets to offer to the tailnet, separated by commas. |
| `Global DNS` | off | Let Tailscale's DNS also use the tailnet's global name servers. |

Throne resolves the names of your tailnet devices (under `ts.net`) with Tailscale's DNS. Other names use your normal DNS settings. URL tests and the auto selector skip Tailscale profiles.

## Android {#android}

- OpenVPN and OpenConnect profiles work on Android, with the same import formats. The editor shows fewer options: there is no OTP binding, no `Only route advertised network` and no `Tunnel DNS`.
- There is no OTP Manager and no `VPN Authentication` window. The profile must sign in with its saved username and password. OTP entries from a desktop backup are not restored.
- Routing-profile endpoints (split tunnel) do not run on Android. A routing profile from a desktop backup keeps its endpoints, but Android does not start them.
- Tailscale profiles are not supported.
- On both platforms, the auto selector skips OpenVPN, OpenConnect and Tailscale profiles.
