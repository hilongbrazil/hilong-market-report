#!/usr/bin/env python3
"""Gera o PDF do Hilong Market Report (sempre em inglês) a partir de data/news.json.

Uso:
  python3 scripts/build_pdf.py --out /caminho/Hilong-Market-Report-AAAA-MM-DD.pdf
      [--date AAAA-MM-DD]      data da edição (padrão: data de updated_at)
      [--days 7]               janela de notícias incluídas no relatório
      [--base-ref HEAD]        ref do git usada para marcar o que é novo (NEW)
      [--edition "Daily edition"]
      [--message "..."]        mensagem positiva do dia (padrão: escolhida pela data)

Requer o Playwright com Chromium (já instalado no ambiente da rotina).
"""
import argparse
import datetime as dt
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://marketreport.hilongbrazil.com"

ONSHORE = ["Carmo Energy", "PetroReconcavo", "Brava Energia", "Origem Energia", "Mandacaru Energia",
           "Seacrest Petróleo", "PetroVictory", "Alvopetro", "Enauta", "Vipetro"]
OFFSHORE = ["Petrobras", "Equinor", "Perenco", "PRIO", "TotalEnergies"]
SUPPLIERS = ["SLB", "Baker Hughes", "Weatherford", "Tenaris", "Confab", "Apolo Tubulars", "Jereh", "Kerui"]

CATEGORY = {"resultados": "Results", "producao": "Production", "perfuracao": "Drilling",
            "investimentos": "Investment", "contratos": "Contracts", "regulatorio": "Regulation",
            "exploracao": "Exploration", "mercado": "Market", "fusoes": "M&A", "outros": "Other"}
ENVIRONMENT = {"onshore": "Onshore", "offshore": "Offshore", "geral": "General"}
COUNTRY = {"BR": "Brazil", "AR": "Argentina", "CO": "Colombia", "GY": "Guyana", "SR": "Suriname",
           "PE": "Peru", "EC": "Ecuador", "BO": "Bolivia", "VE": "Venezuela", "CL": "Chile",
           "UY": "Uruguay", "PY": "Paraguay", "TT": "Trinidad and Tobago"}
COUNTRY_ORDER = ["AR", "CO", "GY", "SR", "PE", "EC", "BO", "VE", "CL", "UY", "PY", "TT"]
RELEVANCE = {5: "Direct interest", 4: "High", 3: "Medium", 2: "Regional", 1: "Context"}

MESSAGES = [
    "Have a safe and productive day. Good decisions start with good information.",
    "Wishing you a steady day: one well, one contract, one good conversation at a time.",
    "May today bring clear data, fair weather on location and a full order book.",
    "A good day to you and the whole crew. Safety first, results right behind.",
    "Have a great day. The market rewards those who show up prepared.",
    "Wishing you energy for the day ahead and good news by the end of it.",
    "Here's to a day of smooth operations and no surprises downhole.",
    "Have an excellent day. Every opportunity in this report started as a single line of news.",
    "Wishing you a confident day: the rigs are turning and so is the market.",
    "A calm, focused and successful day to you and the team.",
    "May your day be as reliable as a well-run rig. Enjoy it.",
    "Have a bright day. Patience and preparation still beat luck in this business.",
    "Wishing you a day of good meetings, safe work and deals that move forward.",
    "Start strong, stay safe, finish proud. Have a wonderful day.",
]

CSS = r"""
@page { size: A4; margin: 15mm 0 17mm 0; }
@page :first { margin-top: 0; }
:root {
  --paper: #EDF1F1; --sheet: #FFFFFF; --ink: #13262B; --muted: #55686E; --line: #CFD9DA;
  --petrol: #0C4650; --petrol-deep: #082F36; --br: #0E7C66; --sa: #B36B00; --signal: #F2B705;
  --soft: #F4F7F7;
}
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; color: var(--ink); background: #fff;
  font-family: "Inter", "Helvetica Neue", Arial, sans-serif; font-size: 9.4pt; line-height: 1.45; }
a { color: inherit; text-decoration: none; }
.pad { padding-left: 15mm; padding-right: 15mm; }

/* Masthead */
.mast { background: var(--petrol-deep); color: #fff; padding: 9mm 15mm 7mm; position: relative; overflow: hidden; }
.mast::after { content: ""; position: absolute; right: -38mm; top: -52mm; width: 150mm; height: 150mm; border-radius: 50%;
  border: 22mm solid rgba(255,255,255,.035); }
.mast::before { content: ""; position: absolute; right: 12mm; bottom: -64mm; width: 96mm; height: 96mm; border-radius: 50%;
  border: 12mm solid rgba(242,183,5,.07); }
.brandrow { display: flex; justify-content: space-between; align-items: center; font-size: 8.2pt; letter-spacing: .14em;
  text-transform: uppercase; font-weight: 600; position: relative; z-index: 1; }
.brandrow .brand b { font-weight: 800; }
.brandrow .brand span { opacity: .7; font-weight: 500; margin-left: 2.2mm; }
.edition { border: .8pt solid rgba(255,255,255,.45); border-radius: 20mm; padding: 1.1mm 3.6mm; font-size: 7.4pt; }
.mast h1 { font-family: "Inter Display", "Inter", sans-serif; font-weight: 800; font-size: 52pt; line-height: .92;
  letter-spacing: -.035em; margin: 8mm 0 3.4mm; position: relative; z-index: 1; }
.mast h1 i { font-style: normal; color: var(--signal); }
.mast .sub { margin: 0; max-width: 118mm; font-size: 10.6pt; line-height: 1.4; color: rgba(255,255,255,.86); position: relative; z-index: 1; }
.dateline { margin-top: 5.5mm; padding-top: 3mm; border-top: .8pt solid rgba(255,255,255,.22); display: flex;
  justify-content: space-between; font-size: 8.8pt; color: rgba(255,255,255,.86); position: relative; z-index: 1; }
.dateline b { color: #fff; font-weight: 600; }

/* KPI row */
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin: 0 15mm; border-bottom: .8pt solid var(--line); }
.kpi { padding: 4.2mm 4mm 3.6mm 0; border-right: .8pt solid var(--line); }
.kpi + .kpi { padding-left: 5mm; }
.kpi:last-child { border-right: 0; }
.kpi .label { font-size: 7.6pt; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
.kpi .value { font-family: "Inter Display", "Inter", sans-serif; font-size: 24pt; font-weight: 700; line-height: 1.05;
  letter-spacing: -.02em; margin-top: 1mm; }
.kpi .note { font-size: 8pt; color: var(--muted); margin-top: .6mm; }

/* Section headings */
.sec { margin-top: 6.5mm; }
.sec.first { margin-top: 5.5mm; }
.sec-h { display: flex; align-items: baseline; justify-content: space-between; border-bottom: 1.6pt solid var(--ink);
  padding-bottom: 1.8mm; margin-bottom: 1mm; break-after: avoid; }
.sec-h h2 { font-family: "Inter Display", "Inter", sans-serif; font-size: 17pt; font-weight: 800; letter-spacing: -.02em; margin: 0; }
.sec-h .hint { font-size: 7.8pt; color: var(--muted); }
.page-break { break-before: page; margin-top: 0; }
.group-h { display: flex; align-items: center; gap: 2.4mm; margin: 6.4mm 0 0; padding: 1.6mm 3mm; background: var(--soft);
  border-left: 2.4pt solid var(--petrol); font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
  color: var(--petrol-deep); break-after: avoid; }
.group-h .count { margin-left: auto; font-weight: 500; letter-spacing: 0; text-transform: none; color: var(--muted); }

/* Relevance meter */
.rel { display: inline-flex; align-items: center; gap: 1.6mm; font-size: 7.4pt; color: var(--muted); white-space: nowrap; }
.rel .pips { display: inline-flex; gap: .7mm; }
.rel .pips span { width: 2.3mm; height: 2.3mm; border-radius: .5mm; background: #DCE4E5; }
.rel .pips span.on { background: var(--petrol); }
.new { display: inline-block; font-size: 6.4pt; font-weight: 800; letter-spacing: .09em; color: var(--petrol-deep);
  background: var(--signal); border-radius: .8mm; padding: .3mm 1.5mm; vertical-align: 1.2pt; margin-left: 1.6mm; }
.dot { display: inline-block; width: 2mm; height: 2mm; border-radius: 50%; margin-right: 1.3mm; vertical-align: .2pt; }
.dot.BR { background: var(--br); } .dot.SA { background: var(--sa); }

/* Top stories */
.top { list-style: none; margin: 0; padding: 0; }
.top li { display: grid; grid-template-columns: 10mm 1fr 21mm; column-gap: 2mm; align-items: start; padding: 2.05mm 0;
  border-bottom: .6pt solid var(--line); break-inside: avoid; }
.top .n { font-family: "Inter Display", "Inter", sans-serif; font-size: 16pt; font-weight: 300; line-height: 1; color: var(--petrol);
  letter-spacing: -.03em; }
.top .t { font-size: 10.2pt; font-weight: 650; line-height: 1.26; }
.top .m { font-size: 7.8pt; color: var(--muted); margin-top: .6mm; }
.top .m b { color: var(--ink); font-weight: 600; }
.top .r { text-align: right; padding-top: .6mm; }
.top .r .lvl { display: block; font-size: 7.2pt; color: var(--muted); margin-top: .7mm; }
.src { color: var(--petrol); font-weight: 600; border-bottom: .6pt solid rgba(12,70,80,.35); }

/* Full report stories */
.story { display: grid; grid-template-columns: 31mm 1fr; column-gap: 5mm; padding: 4mm 0 3.6mm; border-bottom: .6pt solid var(--line);
  break-inside: avoid; }
.story .rail .date { font-size: 7.8pt; color: var(--muted); letter-spacing: .04em; text-transform: uppercase; font-weight: 600; }
.story .rail .op { font-size: 9.6pt; font-weight: 700; line-height: 1.22; margin-top: .9mm; }
.story .rail .rel { margin-top: 1.8mm; }
.story h3 { font-size: 11pt; font-weight: 700; line-height: 1.27; margin: 0 0 1.3mm; letter-spacing: -.005em; }
.story p { margin: 0; color: #2A3C41; }
.story .tags { margin-top: 1.9mm; font-size: 7.8pt; color: var(--muted); display: flex; flex-wrap: wrap; gap: 1.2mm 2.2mm; align-items: center; }
.tag { border: .6pt solid var(--line); border-radius: .9mm; padding: .2mm 1.7mm; color: var(--ink); background: #fff; }
.story .tags .src { margin-left: auto; }
.pay { font-style: italic; }

/* Coverage */
.cov { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; margin-top: 4mm; align-items: start; }
.cov h4 { margin: 0 0 1.4mm; font-size: 8.2pt; letter-spacing: .1em; text-transform: uppercase; color: var(--petrol-deep); }
.cov table { width: 100%; border-collapse: collapse; font-size: 8.6pt; }
.cov td:first-child { white-space: nowrap; }
.cov td { padding: 1.35mm 0; border-bottom: .6pt solid var(--line); vertical-align: middle; }
.cov td.c { width: 6mm; text-align: right; font-weight: 700; }
.cov td.b { width: 12mm; padding: 0 1.6mm; }
.cov td.nn { width: 9mm; text-align: right; white-space: nowrap; }
.cov .bar { display: block; height: 2.1mm; border-radius: 0 1mm 1mm 0; background: var(--petrol); }
.cov tr.zero td { color: #8A999D; } .cov tr.zero td.c { font-weight: 500; }
.cov .nn { font-size: 7.2pt; color: var(--muted); font-weight: 500; }
.nonews { margin-top: 5mm; padding: 3.4mm 4mm; background: var(--soft); border-radius: 1.4mm; font-size: 8.8pt; break-inside: avoid; }
.nonews b { display: block; font-size: 7.8pt; letter-spacing: .1em; text-transform: uppercase; color: var(--petrol-deep); margin-bottom: .8mm; }

/* Sign-off */
.sign { margin: 9mm 15mm 0; background: var(--petrol-deep); color: #fff; border-radius: 2.4mm; padding: 6.5mm 7mm; display: grid;
  grid-template-columns: 23mm 1fr; column-gap: 6mm; align-items: center; break-inside: avoid; position: relative; overflow: hidden; }
.sign::after { content: ""; position: absolute; right: -22mm; top: -26mm; width: 74mm; height: 74mm; border-radius: 50%;
  border: 10mm solid rgba(242,183,5,.08); }
.avatar { width: 23mm; height: 23mm; border-radius: 50%; background: var(--signal); color: var(--petrol-deep); display: flex;
  align-items: center; justify-content: center; font-family: "Inter Display", "Inter", sans-serif; font-weight: 800; font-size: 19pt;
  overflow: hidden; border: 1.2pt solid rgba(255,255,255,.7); }
.avatar img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 18%; }
.sign .msg { font-family: "Inter Display", "Inter", sans-serif; font-size: 13.4pt; font-weight: 600; line-height: 1.3; letter-spacing: -.01em;
  position: relative; z-index: 1; }
.sign .who { margin-top: 2.6mm; font-size: 8.8pt; color: rgba(255,255,255,.8); position: relative; z-index: 1; }
.sign .who b { color: #fff; }
.sign .who a { color: var(--signal); font-weight: 600; }
.method { margin: 5mm 15mm 0; font-size: 7.6pt; color: var(--muted); line-height: 1.5; }
"""


def fetch_data_uri(url):
    """Baixa a imagem do apresentador e devolve um data URI; None se não conseguir (o PDF usa o monograma)."""
    if not url:
        return None
    try:
        import base64
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "hilong-market-report"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            kind = resp.headers.get_content_type() or "image/png"
        if not kind.startswith("image/") or len(data) > 8_000_000:
            return None
        return f"data:{kind};base64,{base64.b64encode(data).decode()}"
    except Exception:  # noqa: BLE001
        return None


def local_data_uri():
    """Usa assets/li-marcitao.(png|jpg|jpeg|webp) quando o arquivo existir no repositório."""
    import base64
    for ext, kind in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"), ("webp", "image/webp")):
        f = ROOT / "assets" / f"li-marcitao.{ext}"
        if f.exists():
            return f"data:{kind};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return None


def esc(text):
    return html.escape(str(text), quote=True)


def fmt_date(iso, long=False):
    d = dt.date.fromisoformat(iso)
    if long:
        return f"{d:%A}, {d.day} {d:%B %Y}"
    return f"{d.day} {d:%b %Y}"


def op_name(item):
    return "Sector" if item["operator"] == "Setor" else item["operator"]


def rank_key(item):
    return (-item["relevance"], item["region"] != "BR", -dt.date.fromisoformat(item["date"]).toordinal())


def rel_html(score, label=True):
    pips = "".join(f'<span class="{"on" if i < score else ""}"></span>' for i in range(5))
    text = f"{score}/5" if label else ""
    return f'<span class="rel"><span class="pips">{pips}</span>{text}</span>'


def story_html(item, new_ids):
    new = '<span class="new">NEW</span>' if item["id"] in new_ids else ""
    place = COUNTRY.get(item["country"], item["country"])
    pay = ' <span class="pay">(subscription required)</span>' if item.get("access") == "paywall" else ""
    return f"""
<article class="story">
  <div class="rail">
    <div class="date">{esc(fmt_date(item["date"]))}</div>
    <div class="op">{esc(op_name(item))}</div>
    {rel_html(item["relevance"])}
  </div>
  <div>
    <h3>{esc(item["title_en"])}{new}</h3>
    <p>{esc(item["summary_en"])}</p>
    <div class="tags">
      <span><span class="dot {item["region"]}"></span>{esc(place)}</span>
      <span class="tag">{esc(CATEGORY.get(item["category"], item["category"]))}</span>
      <span class="tag">{esc(ENVIRONMENT.get(item["environment"], item["environment"]))}</span>
      <span class="src-wrap" style="margin-left:auto">Source: <a class="src" href="{esc(item["url"])}">{esc(item["source"])}</a>{pay}</span>
    </div>
  </div>
</article>"""


def group_html(title, items, new_ids):
    if not items:
        return ""
    items = sorted(items, key=rank_key)
    n = len(items)
    body = "".join(story_html(i, new_ids) for i in items)
    return f'<div class="group-h">{esc(title)}<span class="count">{n} {"story" if n == 1 else "stories"}</span></div>{body}'


def coverage_html(title, names, counts, new_counts, scale):
    rows = []
    for name in names:
        c = counts.get(name, 0)
        nn = new_counts.get(name, 0)
        width = f"{100 * c / scale:.0f}%" if c else "0"
        note = f"{nn} new" if nn else ""
        bar = f'<span class="bar" style="width:{width}"></span>' if c else ""
        rows.append(f'<tr class="{"" if c else "zero"}"><td>{esc(name)}</td><td class="b">{bar}</td>'
                    f'<td class="c">{c if c else "–"}</td><td class="nn">{note}</td></tr>')
    return f"<div><h4>{esc(title)}</h4><table>{''.join(rows)}</table></div>"


def build_html(args):
    news = json.loads((ROOT / "data" / "news.json").read_text(encoding="utf-8"))
    run = json.loads((ROOT / "data" / "run.json").read_text(encoding="utf-8"))
    updated = dt.datetime.fromisoformat(news["updated_at"])
    report_date = args.date or updated.date().isoformat()
    start = (dt.date.fromisoformat(report_date) - dt.timedelta(days=args.days)).isoformat()
    items = [i for i in news["items"] if start <= i["date"] <= report_date]

    new_ids = set()
    if args.base_ref:
        res = subprocess.run(["git", "-C", str(ROOT), "show", f"{args.base_ref}:data/news.json"],
                             capture_output=True, text=True)
        if res.returncode == 0:
            old = {i["id"] for i in json.loads(res.stdout)["items"]}
            new_ids = {i["id"] for i in items if i["id"] not in old}
    new_items = [i for i in items if i["id"] in new_ids]

    br = [i for i in items if i["region"] == "BR"]
    sa = [i for i in items if i["region"] == "SA"]
    br_new = sum(1 for i in new_items if i["region"] == "BR")
    sa_new = sum(1 for i in new_items if i["region"] == "SA")

    # Masthead and KPIs
    avatar = "LM"
    try:
        av = json.loads((ROOT / "assets" / "avatar.json").read_text(encoding="utf-8"))
        uri = local_data_uri() or fetch_data_uri(av.get("image"))
        if uri:
            avatar = f'<img src="{uri}" alt="">'
    except Exception:  # noqa: BLE001
        pass
    message = args.message or MESSAGES[dt.date.fromisoformat(report_date).toordinal() % len(MESSAGES)]

    kpis = [
        ("New stories", len(new_items), f"added in this edition" if new_ids else "no new stories marked"),
        ("Brazil", len(br), f"{br_new} new" if new_ids else "stories in the report"),
        ("South America", len(sa), f"{sa_new} new" if new_ids else "stories in the report"),
        ("Searches run", run.get("searches", 0), "sites, social networks and YouTube"),
    ]
    kpi_html = "".join(f'<div class="kpi"><div class="label">{esc(a)}</div><div class="value">{b}</div>'
                       f'<div class="note">{esc(c)}</div></div>' for a, b, c in kpis)

    # Top 10
    top = sorted(items, key=rank_key)[:10]
    top_html = ""
    for n, i in enumerate(top, 1):
        new = '<span class="new">NEW</span>' if i["id"] in new_ids else ""
        pay = " (subscription required)" if i.get("access") == "paywall" else ""
        top_html += f"""
<li>
  <div class="n">{n:02d}</div>
  <div>
    <div class="t">{esc(i["title_en"])}{new}</div>
    <div class="m"><span class="dot {i["region"]}"></span><b>{esc(op_name(i))}</b> · {esc(COUNTRY.get(i["country"], i["country"]))} ·
      {esc(fmt_date(i["date"]))} · {esc(CATEGORY.get(i["category"], ""))} · <a class="src" href="{esc(i["url"])}">{esc(i["source"])}</a>{pay}</div>
  </div>
  <div class="r">{rel_html(i["relevance"], label=False)}<span class="lvl">{esc(RELEVANCE[i["relevance"]])}</span></div>
</li>"""

    # Full report: Brazil
    def pick(names):
        return [i for i in br if i["operator"] in names]
    listed = set(ONSHORE + OFFSHORE + SUPPLIERS)
    brazil_html = (
        group_html("Onshore operators", pick(ONSHORE), new_ids)
        + group_html("Offshore operators", pick(OFFSHORE), new_ids)
        + group_html("Suppliers", pick(SUPPLIERS), new_ids)
        + group_html("Sector, regulation and other companies", [i for i in br if i["operator"] not in listed], new_ids)
    )
    # Full report: South America
    codes = COUNTRY_ORDER + sorted({i["country"] for i in sa} - set(COUNTRY_ORDER))
    sa_html = "".join(group_html(COUNTRY.get(c, c), [i for i in sa if i["country"] == c], new_ids) for c in codes)

    # Coverage
    counts, new_counts = {}, {}
    for i in items:
        counts[i["operator"]] = counts.get(i["operator"], 0) + 1
        if i["id"] in new_ids:
            new_counts[i["operator"]] = new_counts.get(i["operator"], 0) + 1
    scale = max([counts.get(n, 0) for n in listed] + [1])
    cov_html = (coverage_html("Onshore operators", ONSHORE, counts, new_counts, scale)
                + coverage_html("Offshore operators", OFFSHORE, counts, new_counts, scale)
                + coverage_html("Suppliers", SUPPLIERS, counts, new_counts, scale))
    missing = [n for n in ONSHORE + OFFSHORE + SUPPLIERS if not counts.get(n)]
    extra = (" Enauta is now part of Brava Energia: news on its Atlanta and Papa-Terra fields is counted under Brava."
             if "Enauta" in missing and counts.get("Brava Energia") else "")
    nonews = (f'<div class="nonews"><b>No confirmed news in this window</b>{esc(", ".join(missing))}.{esc(extra)}</div>'
              if missing else "")

    window = f"{fmt_date(start)} to {fmt_date(report_date)}"
    body = f"""
<header class="mast">
  <div class="brandrow"><span class="brand"><b>Hilong</b> Brasil<span>Oil &amp; gas intelligence</span></span><span class="edition">{esc(args.edition)}</span></div>
  <h1>Market Report<i>.</i></h1>
  <p class="sub">Oil and gas news from Brazil and South America, ranked by what matters most to drilling, workover and tubular services.</p>
  <div class="dateline"><span><b>{esc(fmt_date(report_date, long=True))}</b></span><span>Stories from {esc(window)} · updated {updated:%H:%M} Brasília time</span></div>
</header>
<section class="kpis">{kpi_html}</section>

<section class="sec first pad">
  <div class="sec-h"><h2>Top stories</h2><span class="hint">Highest relevance first · Brazil before South America · newest first</span></div>
  <ol class="top">{top_html}</ol>
</section>

<section class="sec pad page-break">
  <div class="sec-h"><h2>Brazil</h2><span class="hint">{len(br)} stories · full report</span></div>
  {brazil_html}
</section>

<section class="sec pad page-break">
  <div class="sec-h"><h2>South America</h2><span class="hint">{len(sa)} stories · full report</span></div>
  {sa_html}
</section>

<section class="sec pad" style="break-inside: avoid">
  <div class="sec-h"><h2>Coverage by company</h2><span class="hint">Priority list · stories in this report</span></div>
  <div class="cov">{cov_html}</div>
  {nonews}
</section>

<section class="sign">
  <div class="avatar">{avatar}</div>
  <div>
    <div class="msg">{esc(message)}</div>
    <div class="who"><b>Li Marcitão</b> · Market news agent, Hilong Brasil · <a href="{SITE}">marketreport.hilongbrazil.com</a></div>
  </div>
</section>
<p class="method">Relevance runs from 5 (direct interest to Hilong in Brazil: land drilling and workover rigs, OCTG, sucker rods, downhole tools and the onshore operators on the priority list) to 1 (general market context). Every story carries a confirmed publication date and a public source link; titles and summaries are written for this report.</p>
"""
    doc = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Hilong Market Report {report_date}</title>'
           f"<style>{CSS}</style></head><body>{body}</body></html>")
    footer = (
        '<div style="width:100%;padding:0 15mm;font-family:Inter,Helvetica,Arial,sans-serif;font-size:7pt;color:#55686E;'
        'display:flex;justify-content:space-between;align-items:center;-webkit-print-color-adjust:exact;">'
        f'<span><b style="color:#13262B">Hilong Brasil</b> · Market Report · {esc(fmt_date(report_date))}</span>'
        '<span>marketreport.hilongbrazil.com</span>'
        '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>'
    )
    return doc, footer, report_date, len(items)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--date")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--base-ref", default="HEAD")
    ap.add_argument("--edition", default="Daily edition")
    ap.add_argument("--message")
    ap.add_argument("--html", help="também grava o HTML intermediário neste caminho")
    args = ap.parse_args()

    doc, footer, report_date, n = build_html(args)
    if args.html:
        Path(args.html).write_text(doc, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(doc, wait_until="load", timeout=30000)
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:  # noqa: BLE001
            pass
        page.evaluate("document.fonts.ready")
        page.pdf(path=args.out, prefer_css_page_size=True, print_background=True, display_header_footer=True,
                 header_template="<span></span>", footer_template=footer)
        browser.close()
    print(f"OK: {args.out} ({n} stories, edition {report_date})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
