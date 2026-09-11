// PROJECT:     SNOOPY-RF-FUSION (web reference)
// CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
// DESCRIPTION: Live viewer. Polls /api/picture and draws the fused RF picture (survey nodes, merged
//   emitters at their coarse RSSI-weighted positions, and Remote ID drones at their exact positions),
//   plus an emitter table and summary counts. No external libraries.

const $ = (id) => document.getElementById(id);
const cv = $("map"), g = cv.getContext("2d");
const W = cv.width, H = cv.height, SCALE = 2.6;
const toPx = (x, y) => [W / 2 + x * SCALE, H / 2 - y * SCALE];   // +Y up

const COL = { node: "#6fd3ff", wifi: "#8fd0ff", ble: "#67c7b0", drone: "#ff5d5d", rid: "#ffb020" };

function draw(pic) {
  g.clearRect(0, 0, W, H);
  g.strokeStyle = "#1e2a33";
  for (let r = 20; r <= 80; r += 20) { g.beginPath(); g.arc(W / 2, H / 2, r * SCALE, 0, 7); g.stroke(); }
  // survey nodes
  for (const nd of pic.nodes || []) {
    const [x, y] = toPx(nd.x, nd.y);
    g.fillStyle = COL.node; g.beginPath(); g.arc(x, y, 4, 0, 7); g.fill();
    g.fillStyle = "#7f97a5"; g.font = "10px system-ui"; g.fillText(nd.node_id, x + 6, y - 6);
  }
  // emitters at their coarse positions
  for (const e of pic.emitters || []) {
    if (!e.est) continue;
    const [x, y] = toPx(e.est.x, e.est.y);
    g.fillStyle = e.is_drone_sig ? COL.drone : (e.band === "wifi" ? COL.wifi : COL.ble);
    g.beginPath(); g.arc(x, y, e.is_drone_sig ? 6 : 4, 0, 7); g.fill();
  }
  // Remote ID drones (exact position) as amber diamonds
  for (const t of pic.rid || []) {
    if (t.x === null || t.x === undefined) continue;
    const [x, y] = toPx(t.x, t.y);
    g.fillStyle = COL.rid; g.beginPath();
    g.moveTo(x, y - 8); g.lineTo(x + 8, y); g.lineTo(x, y + 8); g.lineTo(x - 8, y); g.closePath(); g.fill();
    g.fillStyle = "#0d1418"; g.font = "9px system-ui"; g.fillText("RID", x - 8, y + 3);
  }
}

function table(pic) {
  const rows = (pic.emitters || []).slice().sort((a, b) => (b.best_rssi || -999) - (a.best_rssi || -999));
  $("tbl").querySelector("tbody").innerHTML = rows.map((e) => `
    <tr class="${e.is_drone_sig ? "flag" : ""}">
      <td class="mac">${e.bssid}</td><td>${e.band}</td><td>${e.vendor}</td>
      <td>${e.ssid || e.dev_type}</td><td>${e.best_rssi ?? ""}</td><td>${e.n_nodes}</td>
      <td>${e.is_drone_sig ? "drone-sig" : ""}</td></tr>`).join("");
}

async function poll() {
  try {
    const pic = await (await fetch("/api/picture")).json();
    draw(pic); table(pic);
    const s = pic.summary || {};
    $("summary").textContent =
      `${s.emitters || 0} emitters (${s.wifi || 0} wifi / ${s.ble || 0} ble), ${s.drone_flagged || 0} drone-flagged, ${s.remote_id || 0} Remote ID, ${s.multi_node || 0} multi-node`;
    const st = pic.stages || {};
    $("stages").textContent =
      `merge: ${st.merge} | precise locate: ${st.precise_locate} | coop correlation: ${st.coop_correlation}`;
  } catch (e) { /* server not up */ }
}
setInterval(poll, 500);
poll();
