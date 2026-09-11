#!/usr/bin/env python3
# PROJECT:     SNOOPY-RF-FUSION (web reference)
# CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
# DESCRIPTION: A neutered, web-based reference fusion server for the SNOOPY passive-RF approach. Devices
#              running a passive Wi-Fi/BLE survey (the SNOOPY sensor, not a browser, browsers cannot
#              scan RF) POST their observations here; the server merges them across devices into one
#              coherent picture and serves a live web VIEW of it. Report-level fusion only: dedup
#              emitters by MAC, coarse RSSI-weighted position, aggregate Remote ID, public vendor
#              lookup. The high-value stages (precise RSSI-SLAM, cooperative/non-cooperative
#              correlation, the drone-maker signature list) are empty extension points (see pipeline/).
#              Standard library only; no keys, no model, no proprietary DSP.
#
# USAGE:       python3 server.py                 # http://127.0.0.1:8080 (localhost)
#              python3 server.py --demo          # synthesize device reports so it runs solo
#              python3 server.py --host 0.0.0.0 --cert c.pem --key k.pem   # HTTPS for real devices

import argparse
import json
import math
import os
import ssl
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from pipeline import fuse, locate, delta

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
REPORT_TTL_S = 12.0                             # a device report older than this drops out

_lock = threading.Lock()
_reports = {}                                   # node_id -> report dict (+ rx monotonic)


def ingest(report):
    """Store the latest survey report for a device."""
    nid = str(report.get("node_id", "anon"))
    with _lock:
        r = dict(report)
        r["node_id"] = nid
        r["rx"] = time.monotonic()
        _reports[nid] = r


def picture():
    """Fuse the currently-active device reports into a picture for the UI."""
    now = time.monotonic()
    with _lock:
        active = [r for r in _reports.values() if now - r["rx"] <= REPORT_TTL_S]
    fused = fuse.fuse(active)
    fused["stages"] = {
        "merge": "report-level dedup + coarse RSSI position (reference)",
        "vendor": "public OUI lookup (sample table)",
        "precise_locate": ("wired" if locate.available() else "extension point - not in this repo"),
        "coop_correlation": ("wired" if delta.available() else "extension point - not in this repo"),
        "drone_maker_list": "extension point - not in this repo",
    }
    return fused


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _static(self, name, ctype):
        path = os.path.join(WEB_DIR, name)
        if not os.path.isfile(path):
            return self._send(404, "not found", "text/plain")
        with open(path, "rb") as f:
            self._send(200, f.read(), ctype)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._static("index.html", "text/html; charset=utf-8")
        if self.path == "/app.js":
            return self._static("app.js", "text/javascript")
        if self.path == "/style.css":
            return self._static("style.css", "text/css")
        if self.path == "/api/picture":
            return self._send(200, json.dumps(picture()))
        return self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/observe":
            return self._send(404, "not found", "text/plain")
        try:
            n = int(self.headers.get("Content-Length", 0))
            ingest(json.loads(self.rfile.read(n) or b"{}"))
            self._send(200, json.dumps({"ok": True}))
        except Exception as e:
            self._send(400, json.dumps({"ok": False, "error": str(e)}))

    def log_message(self, *_):
        pass


def _demo_thread():
    """Synthesize device reports: virtual survey nodes hearing a fixed set of Wi-Fi/BLE emitters plus
    one moving Remote ID drone. RSSI falls off with distance (free-space-ish); each node reports the
    emitters it 'hears'. Pure geometry, no RNG."""
    n = 5
    ring = [(70 * math.cos(2 * math.pi * i / n), 70 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    # Fixed emitters: (bssid, band, ssid, x, y, dev_type, is_drone_sig)
    emitters = [
        ("d0:03:4b:11:22:33", "wifi", "Cafe-WiFi", 10, 20, "AP", False),
        ("ac:bc:32:aa:bb:cc", "ble", "", -30, 10, "BLE tag", False),
        ("60:60:1f:de:ad:01", "ble", "", 25, -15, "controller", True),   # drone-signature emitter
        ("3c:5a:b4:44:55:66", "wifi", "Home-2G", -20, -40, "AP", False),
    ]
    step = 0
    while True:
        dx, dy = 40 * math.cos(step / 12.0), 40 * math.sin(step / 12.0)   # RID drone position
        for i, (nx, ny) in enumerate(ring):
            seen = []
            for bssid, band, ssid, ex, ey, dev, sig in emitters:
                d = max(1.0, math.hypot(ex - nx, ey - ny))
                rssi = -40 - 20 * math.log10(d)               # simple path loss
                if rssi > -95:
                    seen.append({"bssid": bssid, "band": band, "ssid": ssid,
                                 "rssi": round(rssi, 1), "dev_type": dev, "is_drone_sig": sig})
            # The RID drone broadcasts its own GPS, so every node that hears it reports the same pos.
            rid = [{"uasid": "DRONE-RID-001", "x": dx, "y": dy}] if math.hypot(dx - nx, dy - ny) < 120 else []
            ingest({"node_id": f"snoopy-{i}", "x": nx, "y": ny, "emitters": seen, "rid": rid})
        step += 1
        time.sleep(0.5)


def main():
    ap = argparse.ArgumentParser(description="SNOOPY RF fusion web reference server.")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="127.0.0.1", help="bind address (0.0.0.0 for LAN devices)")
    ap.add_argument("--cert", help="TLS certificate (PEM); enables HTTPS")
    ap.add_argument("--key", help="TLS private key (PEM)")
    ap.add_argument("--demo", action="store_true", help="synthesize device reports")
    args = ap.parse_args()
    if args.demo:
        threading.Thread(target=_demo_thread, daemon=True).start()
        print("demo: 5 synthetic SNOOPY survey nodes reporting emitters + one Remote ID drone")
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    scheme = "http"
    if args.cert and args.key:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=args.cert, keyfile=args.key)
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        scheme = "https"
    print(f"SNOOPY RF fusion reference on {scheme}://{args.host}:{args.port}/  "
          f"(precise locate + coop correlation + drone-maker list are empty extension points)")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
