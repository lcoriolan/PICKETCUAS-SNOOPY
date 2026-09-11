# PICKET SNOOPY: Passive RF/ESM Survey Plugin for ATAK

PICKET SNOOPY turns an Android phone running ATAK into a passive, receive-only RF
spectrum-awareness sensor. It listens to the radio environment around you (Wi-Fi,
Bluetooth/BLE, and drone Remote ID beacons), decodes what it can, and places the
results on the ATAK map as contacts. Everything runs on the phone; SNOOPY never
transmits and never injects traffic. It is the RF half of PICKET; the acoustic half
is [PICKET SWARM](https://github.com/lcoriolan/PICKETCUAS-SWARM). In the ATAK plugin
list it appears as **PICKET SNOOPY**.

Glossary: **ATAK** = Android Team Awareness Kit (the situational-awareness app).
**ESM** = Electronic Support Measures (passive RF listening). **RF** = radio
frequency. **Remote ID (RID)** = a beacon many drones are required to broadcast,
carrying the drone's ID and its own GPS position. **OUI** = the manufacturer prefix
of a device's MAC address (used to flag drone-maker radios). **RSSI** = received
signal strength, in dBm. **C-UAS** = counter-unmanned-aircraft systems. **EUD** =
end user device (the phone).

## What it does

- **Passive RF survey**: catalogues the emitters the phone can hear (Wi-Fi access
  points, BLE devices, Remote ID beacons) as map contacts, each labeled by band and,
  where the manufacturer prefix is known, by vendor.
- **Drone Remote ID**: decodes ASTM F3411 Remote ID over the bearers Android exposes.
  Because a cooperative drone broadcasts its own GPS position, SNOOPY draws the
  **exact** direction and range to it, not just a bearing.
- **Non-cooperative bearing**: for radios that do not announce a position, SNOOPY
  offers a coarse, honestly-uncertain estimate from signal strength as the operator
  moves. It is shown as a wide, uncertainty-scaled wedge, never a false-precision line.
- **RF compass bubble**: a heading-up bubble on the panel shows where each contact is
  relative to the way the phone is pointed.
- **Receive-only by doctrine**: SNOOPY only listens. It does not transmit, associate,
  deauthenticate, or interfere with any network. There is no active or offensive mode.
- **Coordinates with the acoustic plugin**: when PICKET SWARM is streaming, SNOOPY
  eases its radios ("gentle mode") so the acoustic clock can stay in sync.
- **SURVEY / SENTRY modes**: SURVEY maps every emitter to build the RF picture; SENTRY
  watches for a new drone-signature emitter appearing near you and alerts on it.
- **Cooperative vs non-cooperative calls**: paired with PICKET SWARM, SNOOPY correlates
  SWARM's acoustic drone detection against decoded Remote ID and labels the track
  COOPERATIVE (it is broadcasting Remote ID) or NON-COOPERATIVE (a drone that is silent).
- **Drone-maker flagging**: emitters whose OUI (MAC manufacturer prefix) belongs to a
  known drone maker (for example DJI) are flagged so drone-adjacent RF stands out.

## Supported ATAK versions

| Release asset | ATAK host |
|---|---|
| `PICKETCUAS-SNOOPY-2.0.0-ATAK5.5.1.apk` | ATAK-CIV 5.5.1.x |
| `PICKETCUAS-SNOOPY-2.0.0-ATAK5.8.apk` | ATAK-CIV 5.8.x |

Same plugin, same version: install the APK that matches your ATAK host (a plugin's
API level must match the ATAK it runs on).

The APK is built and signed by the **TAK Product Center third-party signing service**;
ATAK shows the third-party-signed indicator for such plugins.

## Install: getting SNOOPY onto your device

You do not need a computer, ADB, or a rooted phone. The whole flow happens on the EUD.

### 1. Download the plugin APK
On the phone, open the [**Releases** page](https://github.com/lcoriolan/PICKETCUAS-SNOOPY/releases)
and download the `.apk` asset that matches your ATAK version (see the table above).
If you downloaded it on a computer instead, copy the `.apk` to the phone by any
ordinary transfer: USB/MTP file copy, a cloud drive, email to yourself, or an ATAK
data package.

### 2. Allow installing this one app
Android blocks installs from outside the Play Store until you permit them. When you
open the `.apk`, Android will offer a settings toggle such as **"Allow from this
source"** (the exact wording varies by phone and Android version, under
*Settings to Install unknown apps*). Enable it for the app you are installing from
(your Files app or browser), then continue. You can turn it back off afterward.

### 3. Install the APK
Tap the downloaded `.apk`, review the permissions, and approve the install prompt.
The app installs as **PICKET SNOOPY**. Installing the plugin APK does **not** launch
anything on its own; ATAK loads it.

### 4. Load the plugin in ATAK
1. Open (or restart) **ATAK**.
2. ATAK detects the newly installed plugin and shows a **"Load plugin?"** prompt for
   PICKET SNOOPY. Approve it. (If you miss the prompt, restart ATAK and it appears
   again, or find PICKET SNOOPY under **Plugins** in the ATAK settings.)
3. PICKET SNOOPY appears in the ATAK toolbar / **All Tools** menu.

### 5. Grant the runtime permissions
On first run, Android asks for the permissions SNOOPY needs to hear the radio
environment. Grant all of them or the survey cannot run:
- **Location** (Precise): required by Android for any Wi-Fi/BLE scan and to place
  Remote ID contacts. SNOOPY uses it only to scan and to geo-locate contacts.
- **Nearby devices / Nearby Wi-Fi devices** and **Bluetooth scan/connect**: to see
  Wi-Fi and Bluetooth emitters and Remote ID.
- **Notifications**: for the persistent survey notification (Android shows an active
  foreground service while the survey runs).

### 6. Start the survey
Open the PICKET SNOOPY panel, choose a mode, and start:
- **SURVEY** maps everything it hears.
- **SENTRY** watches for new drone-like emitters and alerts on them.

Contacts populate the map as they are heard. Remote ID drones show an exact wedge and
range; non-cooperative emitters show a benign device marker, or a wide uncertainty
wedge once enough signal-strength history exists.

### Troubleshooting
- **No contacts at all**: confirm Location is set to **Precise** and that Wi-Fi and
  Bluetooth are turned on (Android needs the radios on to scan, even passively).
- **Plugin not listed in ATAK**: restart ATAK; approve the load prompt. Make sure the
  APK matches your ATAK version.
- **Survey stops when the screen locks**: keep the persistent notification enabled; it
  is what keeps the receive-only service alive.

## Known limitations (read before relying on it)

- **Receive-only.** SNOOPY is a passive listener. It cannot make a drone land, jam,
  or take any action against a radio. It is situational awareness, not an effector.
- **Non-cooperative position is coarse.** Only Remote ID gives an exact fix. Everything
  else is a signal-strength estimate and is displayed with its uncertainty.
- **What the phone can hear is the ceiling.** Coverage depends on the phone's radios
  and Android's scan throttling; SNOOPY surfaces what the OS exposes, no more.
- **Legal use is your responsibility.** Passively receiving is broadly permissible in
  many places, but rules vary. Operate within the law and policy for your location.

## Free version vs. production

This is the **free version** and it is useful on its own: a passive RF survey, drone
Remote ID on the map, and OUI vendor typing, open source under Apache-2.0. The production
PICKET stack is a large step up in sensitivity, decode breadth, multi-node localization,
and robustness.

| Capability | Free (this plugin) | Production PICKET |
|---|---|---|
| **Use / license** | Open source, Apache-2.0 (commercial use OK) | Commercial license for the production engine |
| **Passive RF survey** | Yes | Yes, wider bearer and band coverage |
| **Drone Remote ID** | Yes: ASTM F3411 over Android bearers | Yes: expanded decode + fusion correlation |
| **Non-cooperative localization** | Coarse single-phone RSSI estimate | Multi-node localization and tracking |
| **Multi-node / map fusion** | With a PICKET mesh/server | Full networked fusion at scale |

## License

Licensed under the **Apache License 2.0** (see `LICENSE`), free and open for any use, including
commercial. See the Releases page for the signed build.

## RF fusion server

A companion web-based **RF fusion server** lives in [`rf-fusion-server/`](./rf-fusion-server/): point
several SNOOPY devices (or its `--demo`) at one server and it merges their Wi-Fi/BLE survey reports
into a coherent picture, dedup across devices, coarse RSSI position, Remote ID aggregation, vendor
lookup, and a live map. The advanced stages (precise localization, cooperative/non-cooperative
correlation, the drone-maker list) are documented, empty extension points. See its README to run it.

## PICKET family

- [PICKET SWARM](https://github.com/lcoriolan/PICKETCUAS-SWARM): acoustic detection ATAK plugin (classification, bearing, distributed array + CoHear).
- [SWARM-DEVICE-AGNOSTIC](https://github.com/lcoriolan/SWARM-DEVICE-AGNOSTIC): web-based acoustic reference; any browser is a sensor node.
