"""Li Marcitão — mapa do Brasil com os locais de entrega das oportunidades do resumo diário.
Uso: python3 build_map.py map.json saida.png
map.json = {"title": "...", "opps": [{"n": 1, "short": "Válvulas API 6A", "fit": "alta"|"média",
            "places": ["Taquipe", "AM", {"name": "Outro lugar", "lat": -10.1, "lon": -37.2}]}]}
"short": até 20 caracteres (ex.: "Workover Araçás", "OCTG, 60 itens").
Cada lugar pode ser: um nome do dicionário PLACES abaixo, a sigla de um estado (usa o centro do estado)
ou um objeto com name/lat/lon. Gera um PNG 1200 px de largura para o e-mail (exibido a 600 px)."""
import json, math, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

NAVY, ORANGE, INK, MUTED, LINE, AMBERTXT = "#0B2545", "#E8711A", "#1F2A37", "#5A6B7F", "#E2E8F0", "#B45309"
HERE = os.path.dirname(os.path.abspath(__file__))

# locais frequentes da Petrobras (lat, lon)
PLACES = {
    "Taquipe": (-12.52, -38.49), "São Sebastião do Passé": (-12.51, -38.49), "Araçás": (-12.20, -38.20),
    "Catu": (-12.35, -38.38), "Candeias": (-12.67, -38.55), "Alagoinhas": (-12.14, -38.42), "Salvador": (-12.97, -38.50),
    "Buracica": (-12.30, -38.30), "Miranga": (-12.40, -38.25), "Entre Rios": (-11.94, -38.08),
    "Carmópolis": (-10.65, -36.99), "Aracaju": (-10.91, -37.07), "Atalaia": (-10.98, -37.05),
    "Mossoró": (-5.19, -37.34), "Alto do Rodrigues": (-5.29, -36.76), "Natal": (-5.79, -35.21), "Guamaré": (-5.11, -36.32),
    "Manaus": (-3.12, -60.02), "Urucu": (-4.86, -65.35), "Coari": (-4.09, -63.14),
    "Macaé": (-22.37, -41.79), "Rio de Janeiro": (-22.90, -43.20), "Campos": (-21.75, -41.32),
    "Vitória": (-20.32, -40.34), "São Mateus": (-18.72, -39.86), "Linhares": (-19.39, -40.07),
    "Santos": (-23.96, -46.33), "São Paulo": (-23.55, -46.63), "Fortaleza": (-3.73, -38.52),
    "Maceió": (-9.67, -35.74), "Recife": (-8.05, -34.88), "Paulínia": (-22.76, -47.15), "Betim": (-19.97, -44.20),
}


def load_states():
    return json.load(open(os.path.join(HERE, "br_states.json")))


def state_center(rings):
    r = max(rings, key=len)
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
        c = x1 * y2 - x2 * y1
        a += c; cx += (x1 + x2) * c; cy += (y1 + y2) * c
    a *= 0.5
    return (cy / (6 * a), cx / (6 * a))


def resolve(p, states):
    if isinstance(p, dict):
        return p["name"], p["lat"], p["lon"]
    if p in PLACES:
        return p, *PLACES[p]
    if p.upper() in states:
        lat, lon = state_center(states[p.upper()])
        return p.upper(), lat, lon
    raise SystemExit(f"local desconhecido: {p} (use sigla de estado ou name/lat/lon)")


def main(src, out):
    d = json.load(open(src, encoding="utf-8"))
    states = load_states()
    # um marcador por local; locais a menos de 1,5 grau viram um só marcador com os números juntos
    from matplotlib.path import Path
    raw = []
    for o in d["opps"]:
        for p in o["places"]:
            name, lat, lon = resolve(p, states)
            raw.append({"n": o["n"], "fit": o.get("fit", "alta"), "lat": lat, "lon": lon})
    groups = []
    for r in raw:
        g = next((g for g in groups if math.hypot(g["lat"] - r["lat"], g["lon"] - r["lon"]) < 1.5), None)
        if g:
            if r["n"] not in g["ns"]:
                g["ns"].append(r["n"])
            g["alta"] = g["alta"] or r["fit"] == "alta"
        else:
            groups.append({"lat": r["lat"], "lon": r["lon"], "ns": [r["n"]], "alta": r["fit"] == "alta"})
    # afasta marcadores que se sobrepõem (caixas em graus) e guarda o ponto real para a linha-guia
    for g in groups:
        g["label"] = " · ".join(str(n) for n in sorted(g["ns"]))
        g["w"], g["h"] = 1.6 + 0.85 * len(g["label"]), 3.2
        g["x0"], g["y0"], g["x"], g["y"] = g["lon"], g["lat"], g["lon"], g["lat"]
    for _ in range(200):
        moved = False
        for i, a in enumerate(groups):
            for b in groups[i + 1:]:
                ox = (a["w"] + b["w"]) / 2 + 0.3 - abs(a["x"] - b["x"])
                oy = (a["h"] + b["h"]) / 2 + 0.3 - abs(a["y"] - b["y"])
                if ox > 0 and oy > 0:
                    moved = True
                    if oy <= ox:
                        sgn = 1 if a["y"] >= b["y"] else -1
                        a["y"] += sgn * oy / 2; b["y"] -= sgn * oy / 2
                    else:
                        sgn = 1 if a["x"] >= b["x"] else -1
                        a["x"] += sgn * ox / 2; b["x"] -= sgn * ox / 2
        if not moved:
            break
    hot = set()
    for uf, rings in states.items():
        for r in rings:
            path = Path(r)
            if any(path.contains_point((x["lon"], x["lat"])) for x in raw):
                hot.add(uf)

    fig = plt.figure(figsize=(12, 8), dpi=100)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.0, 0.01, 0.50, 0.98])
    for uf, rings in states.items():
        for r in rings:
            ax.add_patch(Polygon(r, closed=True, facecolor="#F9DCC4" if uf in hot else "#E4EAF2",
                                 edgecolor="white", linewidth=1.2))
    for g in groups:
        col = ORANGE if g["alta"] else "#F2B263"
        label = g["label"]
        if math.hypot(g["x"] - g["x0"], g["y"] - g["y0"]) > 0.6:
            ax.plot([g["x0"], g["x"]], [g["y0"], g["y"]], color=NAVY, linewidth=1.4, zorder=4)
            ax.scatter(g["x0"], g["y0"], s=40, color=NAVY, zorder=4)
        ax.text(g["x"], g["y"], label, ha="center", va="center", fontsize=19, fontweight="bold", color="white",
                family="DejaVu Sans", zorder=6,
                bbox=dict(boxstyle="round,pad=0.45,rounding_size=0.9", facecolor=col, edgecolor="white", linewidth=2.5))
    ax.set_xlim(-74.2, -34.4); ax.set_ylim(-34.0, 5.5)
    ax.set_aspect("equal"); ax.axis("off")

    lx = fig.add_axes([0.51, 0.0, 0.49, 1.0]); lx.axis("off"); lx.set_xlim(0, 1); lx.set_ylim(0, 1)
    lx.text(0.0, 0.92, d.get("title", "Locais de entrega"), fontsize=27, fontweight="bold", color=NAVY, family="DejaVu Sans")
    n = len(d["opps"])
    step = min(0.14, 0.80 / max(n, 1))
    y = 0.82
    for o in d["opps"]:
        col = ORANGE if o.get("fit", "alta") == "alta" else "#F2B263"
        lx.text(0.04, y, str(o["n"]), ha="center", va="center", fontsize=19, fontweight="bold", color="white", family="DejaVu Sans",
                bbox=dict(boxstyle="circle,pad=0.35", facecolor=col, edgecolor="white", linewidth=2))
        lx.text(0.12, y + 0.016, o["short"], fontsize=min(24, 24 * 19 / max(len(o["short"]), 1)), fontweight="bold", color=INK, va="center", family="DejaVu Sans")
        names = [resolve(p, states)[0] for p in o["places"]]
        lx.text(0.12, y - 0.042, " · ".join(names), fontsize=min(20, 20 * 24 / max(len(" · ".join(names)), 1)), color=MUTED, va="center", family="DejaVu Sans")
        y -= step
    fig.savefig(out, dpi=100, facecolor="white", bbox_inches="tight", pad_inches=0.25)
    print("ok", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
