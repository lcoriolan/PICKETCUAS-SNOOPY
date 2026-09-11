# SNOOPY-RF-FUSION

A web-based reference fusion server for the SNOOPY passive-RF approach: **many devices report what
they hear on the air; one server merges them into a coherent Wi-Fi/BLE picture.** Each device runs a
passive survey and streams its observations; the server dedups emitters across devices, places them,
aggregates drone Remote ID, and serves a live view of the whole scene.

Note: a **browser cannot passively scan Wi-Fi/BLE** (there is no web API for it), so the *sensing* is
done by SNOOPY survey devices; this page is the *view*, and any client can feed it by POSTing the
documented observation JSON to `/observe`.

This repository is a **reference skeleton**: it ships the plain, textbook fusion that runs end to
end and leaves the high-value stages as clearly marked, empty extension points. The production PICKET
engine is not here.

## What you get here

Runnable today: point several survey devices (or `--demo`) at one server and get a live, merged RF
picture. The server:

- **Merges emitters across devices** by MAC, so one radio seen by five devices is one contact, with
  who heard it and how strongly.
- **Places each emitter** at a coarse RSSI-weighted centroid of the devices that heard it.
- **Aggregates drone Remote ID** by UAS id, a cooperative drone broadcasts its own GPS, so its
  position is exact.
- **Types the vendor** from the MAC's OUI (public lookup), and passes through each device's
  drone-signature flag.
- Serves a **live map + table** (`/api/picture`) and takes reports at `/observe`. `--demo` synthesizes
  survey nodes and a moving Remote ID drone so it runs with no hardware.

## What our secret sauce adds

Fill the empty hooks with the production engine and the picture gets precise and decisive:

- **Precise non-cooperative localization** (`pipeline/locate.py`). The reference gives a coarse
  RSSI centroid; production turns many RSSI readings, as devices move, into a tight position with an
  uncertainty (RSSI-SLAM).
- **Cooperative vs non-cooperative correlation** (`pipeline/delta.py`). Correlating decoded Remote ID
  against heard/drone-signature emitters to call a track **COOPERATIVE** (broadcasting Remote ID) or
  **NON-COOPERATIVE** (a silent drone, the real threat).
- **Drone-maker signature list** (`pipeline/oui.py`, `is_drone_maker`). The curated OUI/pattern set
  that flags drone radios on the RF alone.

**Want to see the rest?** The full capability behind these hooks can be shown running, the same as
with the ATAK plugins. Open an issue on this repository (a "capability demo request").

## What's held back

The reference runs the whole merge end to end, but the pieces that make SNOOPY precise and decisive
stay private. Each is a documented, empty hook, described at the capability level, never how:

- **Precise RSSI localization (RSSI-SLAM)** (`pipeline/locate.py`), what tightens the coarse centroid
  into a real position estimate with uncertainty.
- **The cooperative/non-cooperative correlator** (`pipeline/delta.py`), the engine that fuses
  Remote ID with heard drones into a verdict.
- **The curated drone-maker signature list** (`pipeline/oui.py`), the judgement of which radios are
  drones from the RF alone.

None of the code, lists, or keys for these are in this repository; where each attaches, the file says so.

## Run it

```bash
python3 server.py --demo        # synthesize survey nodes + a Remote ID drone
# open http://127.0.0.1:8080/
```

Real survey devices over the network need **HTTPS** (serve with `--cert`/`--key`; a self-signed cert
is fine on a LAN). Devices POST observation JSON to `/observe`; the page shows the fused picture.

This server is part of the **PICKET SNOOPY** repository; it is the server side for the SNOOPY ATAK
plugin's survey reports. See the repository root README for the plugin and the rest of the PICKET
family.

## License

Source-available under the **PolyForm Noncommercial License 1.0.0** (see `LICENSE`) for
noncommercial use; commercial or operational deployment requires a separate license.
