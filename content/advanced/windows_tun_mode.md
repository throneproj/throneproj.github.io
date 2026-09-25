+++
title = "Windows DNS Leak Protection"
description = "How Strict Route stops DNS leaks in TUN mode on Windows, and what to do when you cannot use it."
weight = 60
toc = true
aliases = ["/advanced/windows-tun-mode/"]
+++

In TUN mode, Windows can still send DNS queries through your normal network adapter instead of the tunnel. Your internet provider can then see which sites you look up. This is a DNS leak. This page explains how Throne prevents it, how to check that the protection is on, and what to do when you cannot use it.

The page is about [TUN mode](@/guides/tun_mode.md) only. `Strict Route` has no effect in `System Proxy` mode, where apps that ignore the proxy connect and look up names on their own.

## Strict Route {#strict-route}

Windows can send the same DNS query to the DNS servers of all network adapters at the same time. Even if Windows then uses the answer from the tunnel, the query has already left through your normal adapter, outside the tunnel.

`Strict Route` stops this. While TUN mode runs, Throne adds Windows firewall filters that:

- block DNS queries (port 53) on every network adapter except the tunnel, so Windows gets its answers from Throne;
- block IPv6 connections of other apps when `Tun Enable IPv6` is off, so nothing leaks over IPv6.

ThroneCore itself is not blocked. The filters disappear when TUN mode stops or Throne exits. They can also block programs that must reach a DNS server or use IPv6 outside the tunnel.

`Strict Route` is on by default on Windows 10 and 11 since Throne 1.2.1. When it is on, you do not need the registry fallback below.

### Check that it is on {#check}

1. Open `Settings` → `Tun Settings`.
2. Make sure `Strict Route` is ticked.
3. Press `OK`.
4. If `Tun Mode` is on, turn it off and on again. Throne reminds you with "Restart Tun to take effect".

### When it is off {#when-off}

`Strict Route` can be off in these cases:

- **Windows 7, 8 or 8.1.** `Strict Route` does not work on Windows older than Windows 10, so Throne leaves it off.
- **You turned it off after an error.** If Windows cannot set up the filters, the profile does not start and Throne shows "Strict routing unavailable". The message suggests turning `Strict Route` off, which also removes the protection. If you can fix the cause, turn it back on.
- **You started with Throne 1.2.0.** That version had `Strict Route` off by default, and updates keep your saved settings. Tick it now.

If you cannot use `Strict Route`, use the registry fallback below.

## Registry fallback {#registry-fallback}

Without `Strict Route`, you can turn off the Windows feature that sends DNS queries to all adapters at the same time. Its Group Policy name is `Turn off smart multi-homed name resolution`. This is weaker than `Strict Route`: it changes how Windows chooses DNS servers, but it blocks nothing. The policy exists on Windows 8 and later, so Windows 7 has neither protection.

### With Group Policy (Pro, Enterprise, Education) {#group-policy}

1. In the Start menu, search for `Edit group policy` and open it.
2. Go to `Computer Configuration` → `Administrative Templates` → `Network` → `DNS Client`.
3. Double-click `Turn off smart multi-homed name resolution`.
4. Select `Enabled` and press `OK`.
5. Restart Windows.

{% alert_warning() %}
Select `Enabled`, not `Disabled`. Enabling this policy is what turns the feature off. If you followed older instructions and selected `Disabled`, change it to `Enabled`.
{% end %}

### With the registry (Windows Home) {#windows-home}

Windows Home has no Group Policy editor. This command sets the same policy in the registry:

```text
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v DisableSmartNameResolution /t REG_DWORD /d 1 /f
```

1. Copy the command above.
2. In the Start menu, search for `cmd`.
3. Right-click `Command Prompt` and choose `Run as administrator`.
4. Paste the command and press `Enter`.
5. Restart Windows.

To undo it, run this command the same way, then restart Windows:

```text
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v DisableSmartNameResolution /f
```

If you used Group Policy, set the policy back to `Not Configured` instead.

## Browsers {#browsers}

### Encrypted DNS {#encrypted-dns}

Browsers can use their own encrypted DNS (DNS over HTTPS), and Windows 11 can use it for a network adapter. These lookups do not use port 53, so `Strict Route` does not block them, and they do not use Throne's DNS settings. A leak test then shows the servers of that DNS provider.

If you want every lookup to go through Throne's DNS, turn off the secure DNS option in the privacy or security settings of your browser. Also turn off DNS over HTTPS for your network adapter in Windows Settings.

### QUIC {#quic}

Turning off QUIC does not fix DNS leaks. It helps with a different problem. Many sites, such as Google and YouTube, use QUIC (HTTP/3 over UDP), and some proxy servers carry UDP badly or not at all. If these sites load slowly or fail through the tunnel while other sites work, turn off QUIC in the browser so that it uses TCP.

In Chrome:

1. Open `chrome://flags/`.
2. Search for `QUIC`.
3. Set `Experimental QUIC protocol` to `Disabled`.
4. Press `Relaunch`.

## Still leaking? {#still-leaking}

- **Check your routing.** Some results are expected. For example, domains that your rules send direct are looked up with `Direct DNS` on purpose, and that is usually the DNS server of your internet provider. [DNS leak tests](@/guides/dns.md#leak-tests) lists the expected results.
- **Check security software.** Some antivirus and firewall products filter or redirect DNS themselves. Test with them paused, or add an exception for Throne.
- **Check other VPN apps.** Disconnect other VPN clients while you use TUN mode. They can change DNS settings and firewall rules too.
