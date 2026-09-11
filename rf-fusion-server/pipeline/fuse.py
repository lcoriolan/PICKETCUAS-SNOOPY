# PROJECT:     SNOOPY-RF-FUSION (web reference)
# CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
# DESCRIPTION: The plain, public fusion stage. Takes RF survey observations from several devices and
#              merges them into one coherent picture: dedup each emitter by its MAC across devices,
#              keep who heard it and how strongly, estimate a coarse position from signal strength, and
#              aggregate Remote ID tracks. It trusts each device's fields (band, ssid, dev_type,
#              drone-signature flag) verbatim, no proprietary weighting. Coordinates are a local plane
#              in metres; Remote ID contacts carry their own (exact) position.

import math

from . import oui


def _rssi_weight(rssi_dbm):
    """Linear power weight from an RSSI in dBm. Stronger observers pull the estimate toward them."""
    return 10.0 ** (rssi_dbm / 10.0)


def fuse(reports):
    """Merge per-device reports into a fused picture.

    reports: list of {"node_id","x","y","emitters":[...],"rid":[...]} where each emitter is
             {"bssid","band","ssid","rssi","dev_type","is_drone_sig"} and each rid is {"uasid","x","y"}.
    Returns {"emitters":[...], "rid":[...], "summary":{...}, "nodes":[...]}.
    """
    emitters = {}   # bssid -> merged record
    nodes = []
    for r in reports:
        nx, ny, nid = r.get("x", 0.0), r.get("y", 0.0), r.get("node_id", "anon")
        nodes.append({"node_id": nid, "x": nx, "y": ny})
        for e in r.get("emitters", []):
            bssid = e.get("bssid")
            if not bssid:
                continue
            m = emitters.setdefault(bssid, {
                "bssid": bssid, "band": e.get("band", "?"), "ssid": e.get("ssid") or "",
                "dev_type": e.get("dev_type") or "unknown", "is_drone_sig": False, "obs": {},
            })
            if e.get("ssid"):
                m["ssid"] = e["ssid"]
            m["is_drone_sig"] = m["is_drone_sig"] or bool(e.get("is_drone_sig"))
            # keep the strongest RSSI heard per node for this emitter
            rssi = e.get("rssi")
            if rssi is not None:
                prev = m["obs"].get(nid)
                if prev is None or rssi > prev["rssi"]:
                    m["obs"][nid] = {"rssi": rssi, "x": nx, "y": ny}
    # Coarse position per emitter = RSSI-weighted centroid of the nodes that heard it.
    out_em = []
    for m in emitters.values():
        obs = list(m["obs"].values())
        est = None
        if obs:
            wsum = sum(_rssi_weight(o["rssi"]) for o in obs)
            if wsum > 0:
                ex = sum(_rssi_weight(o["rssi"]) * o["x"] for o in obs) / wsum
                ey = sum(_rssi_weight(o["rssi"]) * o["y"] for o in obs) / wsum
                est = {"x": ex, "y": ey}
        best = max((o["rssi"] for o in obs), default=None)
        out_em.append({
            "bssid": m["bssid"], "band": m["band"], "ssid": m["ssid"],
            "vendor": oui.label(m["bssid"]),                 # public vendor lookup (sample table)
            "dev_type": m["dev_type"], "is_drone_sig": m["is_drone_sig"],
            "n_nodes": len(obs), "best_rssi": best, "est": est,
        })
    # Remote ID: merge by uasid, keep the latest exact position.
    rid = {}
    for r in reports:
        for t in r.get("rid", []):
            uid = t.get("uasid")
            if uid:
                rid[uid] = {"uasid": uid, "x": t.get("x"), "y": t.get("y")}
    summary = {
        "emitters": len(out_em),
        "wifi": sum(1 for e in out_em if e["band"] == "wifi"),
        "ble": sum(1 for e in out_em if e["band"] == "ble"),
        "drone_flagged": sum(1 for e in out_em if e["is_drone_sig"]),
        "remote_id": len(rid),
        "multi_node": sum(1 for e in out_em if e["n_nodes"] >= 2),
    }
    return {"emitters": out_em, "rid": list(rid.values()), "summary": summary, "nodes": nodes}
