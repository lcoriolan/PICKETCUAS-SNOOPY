# PROJECT:     SNOOPY-RF-FUSION (web reference)
# CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
# DESCRIPTION: The RF fusion pipeline, laid out so the architecture is legible and each advanced
#              capability has a clearly marked slot. Reporting devices (SNOOPY sensors) stream passive
#              RF survey observations; this server merges them across devices into one coherent
#              Wi-Fi/BLE picture. The reference ships the plain, textbook stages that run end to end;
#              the high-value stages are empty extension points.
#
#   Stage flow (see server.py):
#     observations -> merge (dedup emitters across devices) -> [classify/flag] -> position -> picture
#
#   Implemented here (plain, public):
#     - fuse.py : merge emitters by MAC across devices; coarse RSSI-weighted position; aggregate Remote ID
#     - oui.py  : MAC vendor lookup from a small sample table (public IEEE OUI idea)
#   Extension points here (empty on purpose):
#     - locate.py : precise multi-node RSSI localization (RSSI-SLAM) plugs in here
#     - delta.py  : cooperative-vs-non-cooperative correlation (acoustic + Remote ID) plugs in here
#     - oui.is_drone_maker : the curated drone-maker signature list plugs in here
