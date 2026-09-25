+++
title = "sing-box vs Xray"
description = "Which core runs your profiles, how the Xray VLESS Preference works, and how to fix Reality errors with newer Xray servers."
weight = 10
toc = true
+++

Throne's core is built on sing-box, and it also contains Xray. Most profiles run on sing-box. Some VLESS profiles and all Xray custom configs run on Xray. This page explains how Throne chooses the core, how to change that choice for VLESS links, and how to fix Reality connection errors.

## Two cores in one {#two-cores}

sing-box always runs. It handles the local proxy port, TUN mode, routing rules and DNS. Xray runs as a helper inside the same core. It starts only when the running profile needs it, for example when the profile, a hop of its chain or the outbound of a routing rule runs on Xray. sing-box hands that traffic to Xray over an internal local connection, so TUN mode, routing profiles and DNS settings work the same with both cores.

These profiles run on Xray:

| `Type` column | Where it comes from |
| --- | --- |
| `VLESS (Xray)` | `vless://` links, depending on the [Xray VLESS Preference](#vless-preference); VLESS outbounds in Xray JSON; the `VLESS (Xray)` type in the profile editor. |
| `Custom Xray … Outbound` | The `Custom (Xray outbound)` type; other outbounds in imported Xray JSON. |
| `Custom Xray Config` | The `Custom (Xray config)` type; imported lists of complete Xray configs. |

All other profiles, including `VLESS`, run on sing-box.

Some VLESS features exist only in Xray. A `vless://` link that uses one of them is always imported as `VLESS (Xray)`, whatever the preference is set to:

- the XHTTP transport (`type=xhttp`) and its `extra` settings,
- VLESS encryption (an `encryption` value other than `none`),
- Finalmask,
- a TCP (`raw`) transport with an HTTP header together with TLS.

Xray messages appear in the same `Logs` tab. Their detail level is set in `Settings` → `Basic Settings` → `Logging` → `Xray Log level`.

## Choose the core for VLESS links {#vless-preference}

`Settings` → `Basic Settings` → `Core` → `Xray VLESS Preference` decides which core a `vless://` link gets when you import it:

| Option | Links imported as `VLESS (Xray)` |
| --- | --- |
| `XHTTP Only` | Only links that need an Xray-only feature (see the list above). Reality links stay on sing-box. |
| `XHTTP And Reality` (default) | The links above, plus every Reality link. |
| `All VLESS` | Every `vless://` link. |

All other `vless://` links become `VLESS` profiles that run on sing-box.

The preference applies only to `vless://` links:

- **Clash / Mihomo YAML:** a VLESS entry gets Xray only when it uses XHTTP or VLESS encryption. Reality entries stay on sing-box.
- **Xray JSON:** every VLESS outbound becomes `VLESS (Xray)`.
- **sing-box JSON:** VLESS outbounds stay on sing-box.
- **Profile editor:** you choose `VLESS` or `VLESS (Xray)` in the `Type` list yourself.

{% alert_info() %}
`XHTTP And Reality` became the default in 1.2.0, when `All VLESS` was also added. Updating Throne keeps your saved value. If you have used Throne since before 1.2.0, you may still have `XHTTP Only`.
{% end %}

### After you change the preference {#after-change}

The preference affects only profiles that you import after the change. Existing profiles keep their core. To move them to the other core:

- **Subscription group:** update the subscription (`Groups` → `Update subscription`, or right-click the group tab → `Update subscription`). Throne replaces the affected profiles with new ones of the other type, so their old test results are gone.
- **Profile added from a link:** add the link again, then delete the old profile.
- **Profile you created by hand:** its type cannot be changed. Create a new profile with the other type.

If `Keep working profiles` is on in the group's `Advanced` subscription settings, old working profiles can stay next to the new ones. Delete them yourself.

### Which core does a profile use? {#which-core}

Look at the `Type` column of the profile list. `VLESS` runs on sing-box. `VLESS (Xray)`, `Custom Xray … Outbound` and `Custom Xray Config` run on Xray.

To also see the security layer, such as Reality, in that column, turn on `Settings` → `Basic Settings` → `Style` → `Show Config Security`. For `VLESS (Xray)` and `Custom (Xray outbound)` profiles, and for chains, the right-click menu also has `Share` → `Export Xray config`.

## Reality errors with newer Xray servers {#reality}

Newer Xray servers reject the Reality client of sing-box. The profile then does not connect, and the log shows `reality verification failed` ([#1780](https://github.com/throneproj/Throne/issues/1780)).

- Xray 26.7.11 to 26.7.28 accept only clients that report a recent Xray version.
- Xray 26.9.9 and newer require a newer key exchange (X25519MLKEM768) that the Reality client of sing-box does not offer.

The fix is to run the profile on Xray:

1. Open `Settings` → `Basic Settings` → `Core`.
2. Set `Xray VLESS Preference` to `XHTTP And Reality` or `All VLESS`.
3. Click `OK`.
4. Update the subscription, or add the link again (see [After you change the preference](#after-change)).
5. Check that the `Type` column now shows `VLESS (Xray)`.

This does not help for Reality entries from a Clash / Mihomo YAML subscription, because they always stay on sing-box. If your provider also offers the subscription as a list of links, use that format.

If you run an Xray server from 26.7.11 to 26.7.28 yourself, you can also add `"minClientVer": "0.0.0"` to the `realitySettings` of its VLESS inbound. This lets older clients connect. It does not help with Xray 26.9.9 and newer.

## Xray in chains {#xray-in-chains}

A chain can mix sing-box and Xray profiles, with two limits:

- All Xray hops must be next to each other. Traffic can switch from sing-box to Xray and back only once: sing-box hops, then Xray hops, then sing-box hops. Otherwise the profile does not start, and the log shows "Too many core transitions".
- A `Custom (Xray config)` profile must be the top hop, and it cannot share a chain with other Xray hops, because a chain can use only one Xray instance.

Group front and landing proxies, and WARP, count as hops too. See [Proxy Chains & Custom Configs](@/advanced/chains.md#chains).

## Xray geo files {#geo-files}

A `Custom (Xray config)` profile can have its own `routing` rules with `geoip:` or `geosite:` values. For these, Xray needs the files `geoip.dat` and `geosite.dat`. Other profiles and Throne's routing profiles do not use these files; they use rule-sets.

When the files are missing, Throne shows "Geo asset files required" and offers to download them. Click `Yes`, wait for "Geo assets installed", then start the profile again.

The download addresses are in `Settings` → `Basic Settings` → `Miscellaneous` → `Xray Geo Assets`, in the fields `GeoIP Asset URL` and `GeoSite Asset URL`. Their lists offer the addresses of four sources: Loyalsoldier (global and China, the default), Chocolate4U (Iran), runetfreedom (Russia) and v2fly. Take both files from the same source. Each `Download` button downloads that file again and replaces the old one.

If a rule names a category that the file does not contain, Throne shows "Geo asset missing category". Choose a source that has this category, then click `Download` for that file.

## Android {#android}

- The same setting is in `Settings` → `Core` → `Xray VLESS preference`, with `XHTTP only`, `XHTTP and Reality` (default) and `All VLESS`. It also applies only when you import, so update the subscription after you change it.
- The profile types are `VLESS` and `VLESS (Xray)`, and the limits for Xray in chains are the same.
