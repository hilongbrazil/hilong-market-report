#!/usr/bin/env python3
"""Gera o PDF do Hilong Market Report a partir de data/news.json, em inglês (padrão) ou em chinês (--lang zh).

Uso:
  python3 scripts/build_pdf.py --out /caminho/Hilong-Market-Report-AAAA-MM-DD.pdf
      [--lang en|zh]           idioma do PDF (zh usa title_zh/summary_zh e a fonte Noto Sans CJK)
      [--date AAAA-MM-DD|today] data da edição (padrão: data de updated_at; "today" = hoje em Brasília)
      [--kind daily|weekly]    edição: diária (padrão, janela de 15 dias) ou semanal (janela de 7 dias, termina no dia da edição)
      [--days 15]              janela do relatório, em dias corridos, contando o dia da edição (semanal: 7)
      [--base-ref HEAD|auto]   ref do git anterior à varredura: garante que as notícias recém-incluídas entrem
                               no relatório mesmo com data de publicação fora da janela. "auto" = último commit
                               que gravou data/reports.json (o envio anterior), usado pela tarefa das 8h
      [--check-scan]           avisa no e-mail se a varredura do dia ainda não tinha terminado
      [--record]               registra a edição em data/reports.json (só no envio real, uma vez por dia)
      [--message "..."] [--message-zh "..."]  mensagem positiva do dia (padrão: escolhida pela data)
      [--email-html arquivo] [--email-text arquivo]  corpo do e-mail: aviso curto, em inglês e chinês,
                               de que o relatório chegou e qual o período avaliado
      [--email-langs en,zh]    relatórios anexados citados no corpo do e-mail
      [--alert "..."]          aviso na primeira linha do e-mail (ex.: falha no push)
      [--brief arquivo.md] [--analysis arquivo.json]  análise do agente (desligada desde 13/11/2026)

Notícia nova (NEW) é a que ainda não saiu em nenhum relatório registrado em data/reports.json; as novas vêm
primeiro, na seção do topo. O histórico mostra todas as notícias da janela, sem limite de edições.
Requer o Playwright com Chromium (já instalado no ambiente da rotina).
"""
import argparse
import base64
import datetime as dt
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://marketreportnews.hilongbrazil.com"

ONSHORE = ["Carmo Energy", "PetroReconcavo", "Brava Energia", "Origem Energia", "Mandacaru Energia",
           "Seacrest Petróleo", "PetroVictory", "Alvopetro", "Petroborn", "Eneva", "Vipetro"]
OFFSHORE = ["Petrobras", "Equinor", "Perenco", "PRIO", "TotalEnergies", "Transpetro", "ANP"]
SUPPLIERS = ["SLB", "Baker Hughes", "Weatherford", "Tenaris", "Expro", "Confab", "Apolo Tubulars", "Jereh", "Kerui",
             "Inpasa", "TAG"]

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

# ---------- Idioma do PDF (--lang en|zh) ----------
LANG = "en"
ZH_CATEGORY = {"resultados": "业绩", "producao": "产量", "perfuracao": "钻井", "investimentos": "投资", "contratos": "合同",
               "regulatorio": "监管", "exploracao": "勘探", "mercado": "市场", "fusoes": "并购", "outros": "其他"}
ZH_ENVIRONMENT = {"onshore": "陆上", "offshore": "海上", "geral": "综合"}
ZH_COUNTRY = {"BR": "巴西", "AR": "阿根廷", "CO": "哥伦比亚", "GY": "圭亚那", "SR": "苏里南", "PE": "秘鲁", "EC": "厄瓜多尔",
              "BO": "玻利维亚", "VE": "委内瑞拉", "CL": "智利", "UY": "乌拉圭", "PY": "巴拉圭", "TT": "特立尼达和多巴哥"}
ZH_RELEVANCE = {5: "直接相关", 4: "高", 3: "中", 2: "区域", 1: "背景"}
ZH_MESSAGES = [
    "祝您今天安全、高效。好的决策源于好的信息。",
    "祝您今天稳步前行：一口井、一份合同、一次愉快的交流。",
    "愿今天数据清晰、井场天气晴好、订单饱满。",
    "祝您和整个团队今天顺利。安全第一，成果随后。",
    "祝您今天愉快。市场总是青睐有准备的人。",
    "愿您今天精力充沛，收获好消息。",
    "祝今天作业顺利，井下没有意外。",
    "祝您今天顺利。报告中的每一个机会，都始于一条新闻。",
    "祝您今天充满信心：钻机在转，市场也在动。",
    "祝您和团队今天平静、专注、成功。",
    "愿您的一天像一台运转良好的钻机一样可靠。",
    "祝您今天顺心。在这个行业，耐心和准备依然胜过运气。",
    "祝您今天会谈顺利、作业安全、项目推进。",
    "开局有力，安全第一，圆满收官。祝您今天愉快。",
]
TXT = {
    "en": {
        "edition": "Daily Edition", "edition_w": "Weekly Edition", "prep": "Prepared by", "tagline": "Oil &amp; gas intelligence",
        "sub": "Oil and gas news from Brazil and South America, ranked by what matters most to drilling, workover and tubular services.",
        "window": "Stories from {a} to {b} · updated {t} Brasília time",
        "k_new": "New stories", "k_new_y": "first time in a report", "k_new_n": "no new stories today",
        "k_br": "Brazil", "k_sa": "South America", "k_n_new": "{n} new", "k_in": "stories in the report",
        "k_search": "Searches run", "k_search_n": "sites, social networks and YouTube",
        "new_h": "New in this report", "new_hint": "Highest relevance first · Brazil before South America",
        "new_none": "No new stories since the last report. The full {d}-day history follows.",
        "br_h": "Brazil", "sa_h": "South America", "hist_hint": "{n} stories · last {d} days · new first",
        "g_on": "Onshore operators", "g_off": "Offshore operators and ANP", "g_sup": "Suppliers",
        "g_other": "Sector, regulation and other companies",
        "cov_h": "Coverage by company", "cov_hint": "Priority list · stories in the last {d} days",
        "cov_off": "Offshore and ANP", "nonews": "No confirmed news in this window",
        "story1": "story", "storyN": "stories", "new": "NEW", "focus": "Hilong Watch", "supplier": "Supplier",
        "source": "Source:", "pay": "(subscription required)", "n_new": "{n} new", "sector": "Sector",
        "who": "Market news agent, Hilong Brasil",
        "k_today": "New today", "k_today_n": "first time in a report", "k_days": "Last {d} days", "k_days_n": "stories in the report",
        "k_watch": "Hilong Watch", "k_watch_n": "relevance 5", "k_co": "Companies", "k_co_n": "with news in the period",
        "top_h": "Top stories", "cat_h": "Stories by segment", "cocite_h": "Most-cited companies",
        "w_week": "News this week", "w_prev": "{n} the week before", "w_msg": "Message of the week",
        "w_tl": "Week timeline", "w_tl_hint": "Highest-relevance story of each day", "w_none": "No stories recorded",
        "w_theme": "By theme", "w_co": "By company", "w_co_hint": "Companies with the most stories this week",
        "w_next": "Next week", "w_next_hint": "Dates confirmed in this week's stories", "w_period": "Week of {a} to {b}", "seg_on": "Onshore", "seg_off": "Offshore", "seg_sup": "Suppliers", "seg_anp": "ANP", "seg_sa": "South America",
        "doc_title_w": "Hilong Market Report, weekly {d}",
        "method": "Relevance runs from 5 (direct interest to Hilong in Brazil: land drilling and workover rigs, OCTG, sucker rods, downhole tools and the onshore operators on the priority list) to 1 (general market context). Every story carries a confirmed publication date and a public source link; titles and summaries are written for this report. Stories marked HILONG WATCH have relevance 5. Stories marked NEW appear in a report for the first time and are listed first; the report covers the last {d} days.",
        "footer": "Market Report", "page": "Page {p} of {t}", "doc_title": "Hilong Market Report {d}",
    },
    "zh": {
        "edition": "日报", "edition_w": "周报", "prep": "由", "tagline": "油气市场资讯",
        "sub": "巴西及南美洲油气新闻，按与钻井、修井和管材服务的相关程度排序。",
        "window": "收录 {a} 至 {b} 的新闻 · 更新于巴西利亚时间 {t}",
        "k_new": "新消息", "k_new_y": "首次出现在报告中", "k_new_n": "今日无新消息",
        "k_br": "巴西", "k_sa": "南美洲", "k_n_new": "新增 {n} 条", "k_in": "报告中的新闻",
        "k_search": "搜索次数", "k_search_n": "网站、社交媒体和 YouTube",
        "new_h": "本期新消息", "new_hint": "相关度高者在前 · 巴西在南美洲之前",
        "new_none": "自上期报告以来没有新消息。以下为近 {d} 天的完整记录。",
        "br_h": "巴西", "sa_h": "南美洲", "hist_hint": "{n} 条新闻 · 近 {d} 天 · 新消息在前",
        "g_on": "陆上作业者", "g_off": "海上作业者和 ANP", "g_sup": "供应商",
        "g_other": "行业、监管及其他公司",
        "cov_h": "按公司统计", "cov_hint": "重点名单 · 近 {d} 天的新闻",
        "cov_off": "海上和 ANP", "nonews": "本期间内没有已确认的新闻",
        "story1": "条", "storyN": "条", "new": "新", "focus": "海隆关注", "supplier": "供应商",
        "source": "来源：", "pay": "（需订阅）", "n_new": "新增 {n}", "sector": "行业",
        "who": "市场新闻助手，海隆巴西",
        "k_today": "今日新增", "k_today_n": "首次出现在报告中", "k_days": "近 {d} 天", "k_days_n": "报告中的新闻",
        "k_watch": "海隆关注", "k_watch_n": "相关度 5", "k_co": "涉及公司", "k_co_n": "期间有新闻",
        "top_h": "重点新闻", "cat_h": "按板块统计", "cocite_h": "被提及最多的公司",
        "w_week": "本周新闻", "w_prev": "上周 {n} 条", "w_msg": "本周寄语",
        "w_tl": "本周时间线", "w_tl_hint": "每日相关度最高的一条", "w_none": "当日无记录",
        "w_theme": "按主题", "w_co": "按公司", "w_co_hint": "本周新闻最多的公司",
        "w_next": "下周看点", "w_next_hint": "本周新闻中已确认的日期", "w_period": "{a} 至 {b} 当周", "seg_on": "陆上", "seg_off": "海上", "seg_sup": "供应商", "seg_anp": "ANP", "seg_sa": "南美洲",
        "doc_title_w": "海隆市场周报 {d}",
        "method": "相关度从 5（与海隆在巴西的业务直接相关：陆上钻井和修井钻机、OCTG、抽油杆、井下工具以及重点名单中的陆上作业者）到 1（一般市场背景）。每条新闻均有确认的发布日期和公开的来源链接；标题和摘要为本报告撰写。标有“海隆关注”的新闻相关度为 5。标有“新”的新闻首次出现在报告中并排在最前；本报告涵盖近 {d} 天的新闻。",
        "footer": "市场报告", "page": "第 {p} 页，共 {t} 页", "doc_title": "海隆市场报告 {d}",
    },
}


def tr(key, **kw):
    text = TXT[LANG][key]
    return text.format(**kw) if kw else text


def cat_name(k):
    return (ZH_CATEGORY if LANG == "zh" else CATEGORY).get(k, k)


def env_name(k):
    return (ZH_ENVIRONMENT if LANG == "zh" else ENVIRONMENT).get(k, k)


def country_name(k):
    return (ZH_COUNTRY if LANG == "zh" else COUNTRY).get(k, k)


def rel_name(n):
    return (ZH_RELEVANCE if LANG == "zh" else RELEVANCE)[n]


def ttl(it):
    return (it.get("title_zh") if LANG == "zh" else None) or it["title_en"]


def smr(it):
    return (it.get("summary_zh") if LANG == "zh" else None) or it["summary_en"]


def n_stories(n):
    return f"{n} {tr('story1') if n == 1 else tr('storyN')}"


CSS_ZH = """
body, .mast h1, .sec-h h2, .kpi .value, .top .n, .avatar, .sign .msg, .analysis h2 {
  font-family: "Archivo", "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC", "PingFang SC", sans-serif; }
.story h3, .top .t { line-height: 1.38; }
.tag, .group-h, .kpi .label, .cov h4 { letter-spacing: .02em; }
"""

THEME_WEEKLY = """
:root { --petrol: #12915F; --accent: #3DDC97; }
.mast::before { border-color: rgba(61,220,151,.08); }
.sign::after { border-color: rgba(61,220,151,.09); }
"""

CSS = r"""
@page { size: A4; margin: 15mm 0 17mm 0; }
@page :first { margin-top: 0; }
:root {
  --paper: #EDF1F1; --sheet: #FFFFFF; --ink: #07131F; --muted: #55686E; --line: #D6DEE6;
  --petrol: #0E8FC0; --petrol-deep: #07131F; --accent: #58CFFF; --br: #0E7C66; --sa: #B36B00; --signal: #F5A524;
  --soft: #EEF3F7;
}
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; color: var(--ink); background: #fff;
  font-family: "Archivo", "Inter", "Helvetica Neue", Arial, sans-serif; font-size: 9.4pt; line-height: 1.45; }
a { color: inherit; text-decoration: none; }
.pad { padding-left: 15mm; padding-right: 15mm; }

/* Masthead */
.mast { background: var(--petrol-deep); color: #fff; padding: 9mm 15mm 7mm; position: relative; overflow: hidden; }
.mast::after { content: ""; position: absolute; right: -38mm; top: -52mm; width: 150mm; height: 150mm; border-radius: 50%;
  border: 22mm solid rgba(255,255,255,.035); }
.mast::before { content: ""; position: absolute; right: 12mm; bottom: -64mm; width: 96mm; height: 96mm; border-radius: 50%;
  border: 12mm solid rgba(88,207,255,.07); }
.brandrow { display: flex; justify-content: space-between; align-items: center; font-size: 8.2pt; letter-spacing: .14em;
  text-transform: uppercase; font-weight: 600; position: relative; z-index: 1; }
.brandrow .brand b { font-weight: 800; color: var(--accent); }
.brandrow .brand span { opacity: .7; font-weight: 500; margin-left: 2.2mm; }
.edition { border: .8pt solid var(--accent); color: var(--accent); border-radius: 20mm; padding: 1.1mm 3.6mm; font-size: 7.4pt; }
.mast h1 { font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-weight: 800; font-stretch: 72%; font-size: 58pt; line-height: .92;
  letter-spacing: -.01em; margin: 8mm 0 3.4mm; position: relative; z-index: 1; }
.mast h1 i { font-style: normal; color: var(--accent); }
.titlerow { display: flex; justify-content: space-between; align-items: flex-end; gap: 8mm; position: relative; z-index: 1; }
.mast .ed { font-size: 21pt; font-weight: 700; color: var(--accent); margin: 0 0 3.2mm; letter-spacing: -.01em; }
.prep { text-align: center; flex: 0 0 auto; padding-bottom: 1mm; }
.prep .avatar { width: 20mm; height: 20mm; font-size: 15pt; margin: 0 auto 1.8mm; background: #12304A; color: var(--accent); border-color: var(--accent); }
.prep .by { font-size: 7.2pt; letter-spacing: .1em; text-transform: uppercase; color: rgba(255,255,255,.72); }
.prep .by b { display: block; font-size: 8.8pt; letter-spacing: 0; text-transform: none; color: #fff; font-weight: 700; margin-top: .4mm; }
.accent-strip { height: 1.4mm; background: var(--accent); }
.catbar { margin: 5mm 15mm 0; break-inside: avoid; }
.catbar .t { font-size: 7.8pt; letter-spacing: .1em; text-transform: uppercase; font-weight: 700; color: var(--petrol-deep); margin-bottom: 2mm; }
.catbar .bar { display: flex; gap: .7mm; height: 3mm; }
.catbar .bar span { display: block; border-radius: .6mm; }
.catbar .leg { display: flex; flex-wrap: wrap; gap: 1mm 5mm; margin-top: 2mm; font-size: 8pt; color: var(--muted); }
.catbar .leg i { display: inline-block; width: 2.2mm; height: 2.2mm; border-radius: 50%; margin-right: 1.4mm; vertical-align: -.2mm; }
.tl { display: grid; grid-template-columns: 14mm 36mm 1fr; column-gap: 3mm; padding: 1.9mm 0; border-bottom: .6pt solid var(--line); font-size: 9pt; break-inside: avoid; }
.tl .d { font-weight: 700; color: var(--petrol); letter-spacing: .06em; text-transform: uppercase; font-size: 7.8pt; padding-top: .3mm; }
.tl .o { color: var(--muted); font-weight: 600; font-size: 8.2pt; text-transform: uppercase; letter-spacing: .04em; padding-top: .3mm; }
.tl .h { font-weight: 600; line-height: 1.3; }
.tl.none .h { color: #8A999D; font-weight: 400; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin-top: 3mm; }
.tile { background: var(--soft); border-top: 1.4mm solid var(--accent); padding: 3mm 3.4mm; break-inside: avoid; }
.tile b { display: block; font-size: 19pt; font-weight: 700; line-height: 1.05; letter-spacing: -.02em; }
.tile span { font-size: 7.4pt; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
.mast .sub { margin: 0; max-width: 118mm; font-size: 10.6pt; line-height: 1.4; color: rgba(255,255,255,.86); position: relative; z-index: 1; }
.dateline { margin-top: 5.5mm; padding-top: 3mm; border-top: .8pt solid rgba(255,255,255,.22); display: flex;
  justify-content: space-between; font-size: 8.8pt; color: rgba(255,255,255,.86); position: relative; z-index: 1; }
.dateline b { color: #fff; font-weight: 600; }
.cotable { width: 100%; border-collapse: collapse; font-size: 9pt; margin-top: 2mm; }
.cotable td { padding: 1.7mm 1mm; border-bottom: .6pt solid var(--line); vertical-align: top; }
.cotable .cn { font-weight: 700; width: 34mm; }
.cotable .cc { width: 9mm; text-align: center; font-weight: 700; color: var(--petrol); }

/* Agent's analysis (top of page 1) */
.analysis { margin: 6mm 15mm 0; border: .8pt solid var(--line); border-left: 3pt solid var(--signal); border-radius: 1.6mm;
  padding: 4.6mm 6mm 4.4mm; background: var(--soft); break-inside: avoid; }
.analysis .kicker { display: flex; justify-content: space-between; align-items: baseline; font-size: 7.6pt; letter-spacing: .12em;
  text-transform: uppercase; font-weight: 700; color: var(--petrol-deep); }
.analysis .kicker span { font-weight: 500; letter-spacing: 0; text-transform: none; color: var(--muted); }
.analysis h2 { font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-size: 14.6pt; line-height: 1.24; font-weight: 750;
  letter-spacing: -.012em; margin: 2mm 0 2.4mm; }
.analysis ul { margin: 0; padding-left: 4.6mm; }
.analysis li { margin: 0 0 1.5mm; font-size: 9.6pt; line-height: 1.42; color: #22363B; }
.analysis li::marker { color: var(--petrol); }
.analysis .hilong { margin-top: 3mm; padding-top: 2.6mm; border-top: .6pt solid var(--line); font-size: 9.6pt; line-height: 1.42; }
.analysis .hilong b { color: var(--petrol-deep); }

/* KPI row */
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin: 0 15mm; border-bottom: .8pt solid var(--line); }
.kpi { padding: 4.2mm 4mm 3.6mm 0; border-right: .8pt solid var(--line); }
.kpi + .kpi { padding-left: 5mm; }
.kpi:last-child { border-right: 0; }
.kpi .label { font-size: 7.6pt; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
.kpi .value.amber { color: #B87300; }
.kpi .value { font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-size: 24pt; font-weight: 700; line-height: 1.05;
  letter-spacing: -.02em; margin-top: 1mm; }
.kpi .note { font-size: 8pt; color: var(--muted); margin-top: .6mm; }

/* Section headings */
.sec { margin-top: 6.5mm; }
.sec.first { margin-top: 5.5mm; }
.sec-h { display: flex; align-items: baseline; justify-content: space-between; border-bottom: 1.6pt solid var(--ink);
  padding-bottom: 1.8mm; margin-bottom: 1mm; break-after: avoid; }
.sec-h h2 { font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-size: 17pt; font-weight: 800; letter-spacing: -.02em; margin: 0; }
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
.top .n { font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-size: 16pt; font-weight: 300; line-height: 1; color: var(--petrol);
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
.tag { border-radius: 3mm; padding: .25mm 2.2mm; color: var(--muted); background: var(--paper); font-weight: 600; white-space: nowrap; }
.tag.onshore { background: #FBE9E1; color: #A63E12; }
.tag.offshore { background: #E3EEFC; color: #1F5FB0; }
.tag.supplier { background: #ECE7F8; color: #4B3596; }
.focus-tag { display: inline-block; font-size: 6.4pt; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; color: #0A1F24;
  background: var(--signal); border-radius: 3mm; padding: .3mm 2mm; vertical-align: 1.2pt; margin-left: 1.6mm; white-space: nowrap; }
.story.focus { border-left: 2.6pt solid var(--signal); padding-left: 3mm; }
.top li.focus .n { font-weight: 700; }
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
  border: 10mm solid rgba(88,207,255,.08); }
.avatar { width: 23mm; height: 23mm; border-radius: 50%; background: var(--accent); color: var(--petrol-deep); display: flex;
  align-items: center; justify-content: center; font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-weight: 800; font-size: 19pt;
  overflow: hidden; border: 1.2pt solid rgba(255,255,255,.7); }
.avatar img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 18%; }
.sign .msg { font-family: "Archivo", "Inter Display", "Inter", sans-serif; font-size: 13.4pt; font-weight: 600; line-height: 1.3; letter-spacing: -.01em;
  position: relative; z-index: 1; }
.sign .who { margin-top: 2.6mm; font-size: 8.8pt; color: rgba(255,255,255,.8); position: relative; z-index: 1; }
.sign .who b { color: #fff; }
.sign .who a { color: var(--signal); font-weight: 600; }
.method { margin: 5mm 15mm 0; font-size: 7.6pt; color: var(--muted); line-height: 1.5; }
"""


def font_css():
    """Archivo (a fonte do site) embutida no PDF a partir de assets/fonts; sem o arquivo, o PDF usa Inter."""
    f = ROOT / "assets" / "fonts" / "archivo-latin.woff2"
    try:
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
    except Exception:  # noqa: BLE001
        return ""
    return ('@font-face { font-family: "Archivo"; font-style: normal; font-weight: 100 900; font-stretch: 62% 125%; '
            f'src: url(data:font/woff2;base64,{b64}) format("woff2"); }}\n')


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
    if LANG == "zh":
        base = f"{d.year}年{d.month}月{d.day}日"
        return base + " " + "星期" + "一二三四五六日"[d.weekday()] if long else base
    if long:
        return f"{d:%A}, {d.day} {d:%B %Y}"
    return f"{d.day} {d:%b %Y}"


def op_name(item):
    return tr("sector") if item["operator"] == "Setor" else item["operator"]


NEW_IDS = set()      # notícias que ainda não saíram em nenhum relatório; preenchido em build_html
LOG = ROOT / "data" / "reports.json"


def rank_key(item):
    # notícia nova primeiro; depois relevância, Brasil antes da América do Sul e a mais recente antes
    return (item["id"] not in NEW_IDS, -item["relevance"], item["region"] != "BR",
            -dt.date.fromisoformat(item["date"]).toordinal())


def load_log():
    try:
        reports = json.loads(LOG.read_text(encoding="utf-8")).get("reports", [])
        return [r for r in reports if isinstance(r.get("date"), str) and isinstance(r.get("ids"), list)]
    except Exception:  # noqa: BLE001
        return []


def record_report(report_date, ids):
    """Registra a edição em data/reports.json (uma entrada por data; refazer no mesmo dia substitui)."""
    reports = [r for r in load_log() if r["date"] != report_date]
    reports.append({"date": report_date, "ids": sorted(ids)})
    reports.sort(key=lambda r: r["date"])
    LOG.write_text(json.dumps({"reports": reports[-60:]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_analysis(path):
    """Lê a análise do agente (JSON). Devolve None se não houver arquivo; erro claro se o formato estiver errado."""
    if not path:
        return None
    a = json.loads(Path(path).read_text(encoding="utf-8"))
    head = str(a.get("headline", "")).strip()
    points = [str(x).strip() for x in a.get("points", []) if str(x).strip()]
    hilong = str(a.get("hilong", "")).strip()
    if not head or not points:
        raise SystemExit("analysis: 'headline' e ao menos um item em 'points' são obrigatórios")
    if len(points) > 6:
        raise SystemExit("analysis: no máximo 6 itens em 'points'")
    if len(head) > 160 or any(len(x) > 360 for x in points) or len(hilong) > 420:
        raise SystemExit("analysis: texto longo demais (headline até 160, cada ponto até 360, hilong até 420 caracteres)")
    return {"headline": head, "points": points, "hilong": hilong}


def analysis_html(a, n_items, n_new):
    if not a:
        return ""
    pts = "".join(f"<li>{esc(x)}</li>" for x in a["points"])
    hil = f'<div class="hilong"><b>What it means for Hilong:</b> {esc(a["hilong"])}</div>' if a["hilong"] else ""
    basis = f"Based on the {n_items} {'story' if n_items == 1 else 'stories'} in this report ({n_new} new)"
    return (f'<section class="analysis"><div class="kicker">Li Marcitao\'s analysis<span>{esc(basis)}</span></div>'
            f'<h2>{esc(a["headline"])}</h2><ul>{pts}</ul>{hil}</section>')


def brief_md(report_date, items, new_ids):
    """Lista das notícias do relatório, na ordem do PDF, para o agente escrever a análise."""
    lines = [f"# Stories in the report of {report_date}", "",
             f"{len(items)} stories, {len(new_ids)} new. Order: new first, then relevance, Brazil before South America.", ""]
    for n, i in enumerate(sorted(items, key=rank_key), 1):
        flags = (" NEW" if i["id"] in new_ids else "") + (" HILONG-FOCUS" if is_focus(i) else "")
        lines += [f"{n}. [{i['region']}/{i['country']}] {op_name(i)} | {CATEGORY.get(i['category'], i['category'])} | "
                  f"{ENVIRONMENT.get(i.get('environment'), '')} | relevance {i['relevance']} | {i['date']}{flags}",
                  f"   {i['title_en']}", f"   {i['summary_en']}", ""]
    return "\n".join(lines)


def rel_html(score, label=True):
    pips = "".join(f'<span class="{"on" if i < score else ""}"></span>' for i in range(5))
    text = f"{score}/5" if label else ""
    return f'<span class="rel"><span class="pips">{pips}</span>{text}</span>'


def is_focus(item):
    return item.get("relevance") == 5


def focus_tag():
    return f'<span class="focus-tag">{tr("focus")}</span>'


def env_tags(item):
    """Etiquetas coloridas: fornecedor e ambiente (onshore/offshore); "geral" não leva etiqueta."""
    out = ""
    if item["operator"] in SUPPLIERS:
        out += f'<span class="tag supplier">{tr("supplier")}</span>'
    env = item.get("environment")
    if env in ("onshore", "offshore"):
        out += f'<span class="tag {env}">{esc(env_name(env))}</span>'
    return out


def story_html(item, new_ids):
    new = f'<span class="new">{tr("new")}</span>' if item["id"] in new_ids else ""
    focus = focus_tag() if is_focus(item) else ""
    place = country_name(item["country"])
    pay = f' <span class="pay">{tr("pay")}</span>' if item.get("access") == "paywall" else ""
    return f"""
<article class="story{" focus" if focus else ""}">
  <div class="rail">
    <div class="date">{esc(fmt_date(item["date"]))}</div>
    <div class="op">{esc(op_name(item))}</div>
    {rel_html(item["relevance"])}
  </div>
  <div>
    <h3>{esc(ttl(item))}{new}{focus}</h3>
    <p>{esc(smr(item))}</p>
    <div class="tags">
      <span><span class="dot {item["region"]}"></span>{esc(place)}</span>
      {env_tags(item)}
      <span class="tag">{esc(cat_name(item["category"]))}</span>
      <span class="src-wrap" style="margin-left:auto">{tr("source")} <a class="src" href="{esc(item["url"])}">{esc(item["source"])}</a>{pay}</span>
    </div>
  </div>
</article>"""


def group_html(title, items, new_ids):
    if not items:
        return ""
    items = sorted(items, key=rank_key)
    n = len(items)
    body = "".join(story_html(i, new_ids) for i in items)
    return f'<div class="group-h">{esc(title)}<span class="count">{n_stories(n)}</span></div>{body}'


def coverage_html(title, names, counts, new_counts, scale):
    rows = []
    for name in names:
        c = counts.get(name, 0)
        nn = new_counts.get(name, 0)
        width = f"{100 * c / scale:.0f}%" if c else "0"
        note = tr("n_new", n=nn) if nn else ""
        bar = f'<span class="bar" style="width:{width}"></span>' if c else ""
        rows.append(f'<tr class="{"" if c else "zero"}"><td>{esc(name)}</td><td class="b">{bar}</td>'
                    f'<td class="c">{c if c else "–"}</td><td class="nn">{note}</td></tr>')
    return f"<div><h4>{esc(title)}</h4><table>{''.join(rows)}</table></div>"


def email_bodies(start, report_date, alert, attached=("en", "zh"), weekly=False):
    """Corpo do e-mail diário: só avisa que o relatório chegou e o período avaliado (inglês e chinês).

    Usa só estilos inline e atributos de tabela (o conector do Gmail, usado como reserva, remove <style> e class).
    """
    d = lambda iso: dt.date.fromisoformat(iso)
    a, b = d(start), d(report_date)
    en_period = f"{a.day} {a:%B %Y} to {b.day} {b:%B %Y}"
    zh_period = f"{a.year}年{a.month}月{a.day}日至{b.year}年{b.month}月{b.day}日"
    en = (f"Your {'weekly' if weekly else 'daily'} Hilong Market Report has arrived. Period covered: {en_period}. "
          + ("The report is attached in English and in Chinese." if "zh" in attached else "The report is attached."))
    zh = (f"您的海隆市场{'周报' if weekly else '日报'}已送达。报告期间：{zh_period}。"
          + ("附件为英文版和中文版报告。" if "zh" in attached else "附件为报告。"))
    ff = "font-family:Arial,Helvetica,'PingFang SC','Microsoft YaHei',sans-serif"
    alert_html = (f'<p style="{ff};margin:0 0 14px;padding:10px 14px;font-size:14px;color:#13262B;border-left:4px solid #F2B705">'
                  f'{esc(alert)}</p>') if alert else ""
    html_body = (f'<div style="{ff};font-size:15px;line-height:23px;color:#13262B">{alert_html}'
                 f'<p style="margin:0 0 10px">{esc(en)}</p><p style="margin:0 0 18px">{esc(zh)}</p>'
                 f'<p style="margin:0;color:#55686E;font-size:13px">Li Marcitao &middot; Hilong Brasil</p></div>')
    text_body = "\n".join(([alert, ""] if alert else []) + [en, "", zh, "", "Li Marcitao · Hilong Brasil"])
    return html_body, text_body


SEGMENTS = [("seg_on", "#1B9AD6"), ("seg_off", "#2F4B9B"), ("seg_sup", "#7C6FD6"), ("seg_anp", "#E0713F"), ("seg_sa", "#9AA9B5")]


def segment_of(i):
    if i["region"] == "SA":
        return "seg_sa"
    if i["operator"] == "ANP":
        return "seg_anp"
    if i["operator"] in SUPPLIERS:
        return "seg_sup"
    if i.get("environment") == "offshore" or i["operator"] in OFFSHORE:
        return "seg_off"
    return "seg_on"


def catbar_html(items):
    counts = {k: 0 for k, _ in SEGMENTS}
    for i in items:
        counts[segment_of(i)] += 1
    total = sum(counts.values()) or 1
    bar = "".join(f'<span style="width:{100 * counts[k] / total:.1f}%;background:{c}"></span>' for k, c in SEGMENTS if counts[k])
    leg = "".join(f'<span><i style="background:{c}"></i>{esc(tr(k))} {counts[k]}</span>' for k, c in SEGMENTS)
    return f'<section class="catbar"><div class="t">{tr("cat_h")}</div><div class="bar">{bar}</div><div class="leg">{leg}</div></section>'


def top_rows_html(items, new_ids, limit=5):
    rows = ""
    for n, i in enumerate(sorted(items, key=rank_key)[:limit], 1):
        focus = focus_tag() if is_focus(i) else ""
        rows += f"""
<li class="{'focus' if focus else ''}"><div class="n">{n:02d}</div><div><div class="t">{esc(ttl(i))}{focus}</div>
<div class="m"><span class="dot {i["region"]}"></span><b>{esc(op_name(i))}</b> · {esc(country_name(i["country"]))} · {esc(fmt_date(i["date"]))} · {esc(cat_name(i["category"]))}</div></div>
<div class="r">{rel_html(i["relevance"], label=False)}<span class="lvl">{esc(rel_name(i["relevance"]))}</span></div></li>"""
    return f'<ol class="top">{rows}</ol>'


def cocite_html(items, limit=8):
    c = {}
    for i in items:
        if i["operator"] == "Setor":
            continue
        c[op_name(i)] = c.get(op_name(i), 0) + 1
    top = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]
    sep = "、" if LANG == "zh" else " · "
    return sep.join(f"<b>{esc(n)}</b> {k}" for n, k in top)


def load_next_week(path, report_date):
    """Lê o JSON de datas confirmadas para a semana seguinte: [{"date","company","text_en","text_zh"}].
    Só entram datas de D+1 a D+7; devolve [] se não houver arquivo ou itens válidos."""
    if not path:
        return []
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    d0 = dt.date.fromisoformat(report_date)
    out = []
    for e in raw if isinstance(raw, list) else []:
        try:
            d = dt.date.fromisoformat(e["date"])
        except (KeyError, ValueError):
            continue
        if d0 < d <= d0 + dt.timedelta(days=7) and str(e.get("text_en", "")).strip() and str(e.get("text_zh", "")).strip():
            out.append({"date": d, "company": str(e.get("company", "")).strip(),
                        "text": str(e["text_zh" if LANG == "zh" else "text_en"]).strip()})
    return sorted(out, key=lambda e: e["date"])


def next_week_html(events):
    if not events:
        return ""
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] if LANG == "en" else ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    rows = "".join(f'<div class="tl"><div class="d">{names[e["date"].weekday()]} {e["date"].day}</div>'
                   f'<div class="o">{esc(e["company"])}</div><div class="h">{esc(e["text"])}</div></div>' for e in events)
    return (f'<section class="sec pad"><div class="sec-h"><h2>{tr("w_next")}</h2><span class="hint">{tr("w_next_hint")}</span></div>{rows}</section>')


def weekly_sections(items, start, report_date, co_limit=8):
    d0 = dt.date.fromisoformat(start)
    tl = ""
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] if LANG == "en" else ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    for k in range(7):
        day = d0 + dt.timedelta(days=k)
        day_items = sorted([i for i in items if i["date"] == day.isoformat()], key=rank_key)
        if day_items:
            i = day_items[0]
            tl += (f'<div class="tl"><div class="d">{names[day.weekday()]} {day.day}</div><div class="o">{esc(op_name(i))}</div>'
                   f'<div class="h">{esc(ttl(i))}</div></div>')
        else:
            tl += (f'<div class="tl none"><div class="d">{names[day.weekday()]} {day.day}</div><div class="o">–</div>'
                   f'<div class="h">{tr("w_none")}</div></div>')
    cats = {}
    for i in items:
        cats[i["category"]] = cats.get(i["category"], 0) + 1
    tiles = "".join(f'<div class="tile"><b>{n}</b><span>{esc(cat_name(c))}</span></div>'
                    for c, n in sorted(cats.items(), key=lambda kv: (-kv[1], kv[0]))[:4])
    by_co = {}
    for i in items:
        if i["operator"] == "Setor":
            continue
        by_co.setdefault(op_name(i), []).append(i)
    rows = ""
    for name, lst in sorted(by_co.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:co_limit]:
        best = sorted(lst, key=rank_key)[0]
        rows += (f'<tr><td class="cn">{esc(name)}</td><td class="cc">{len(lst)}</td><td>{esc(ttl(best))}</td></tr>')
    return tl, tiles, rows


def build_html(args):
    news = json.loads((ROOT / "data" / "news.json").read_text(encoding="utf-8"))
    run = json.loads((ROOT / "data" / "run.json").read_text(encoding="utf-8"))
    updated = dt.datetime.fromisoformat(news["updated_at"])
    if args.date == "today":
        args.date = dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).date().isoformat()
    report_date = args.date or updated.date().isoformat()
    weekly = args.kind == "weekly"
    if args.days is None:
        args.days = 7 if weekly else 15
    if args.check_scan and not weekly and not args.alert and str(run.get("run_at", ""))[:10] != report_date:
        args.alert = ("Today's 6:00 scan had not finished when this report was sent. "
                      "The stories below are the latest available; anything new will come in tomorrow's report.")
    if args.base_ref == "auto":
        res = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", "data/reports.json"],
                             capture_output=True, text=True)
        args.base_ref = res.stdout.strip() or "HEAD"
    # janela de --days dias corridos, contando o dia do relatório (15 dias: de D-14 a D)
    start = (dt.date.fromisoformat(report_date) - dt.timedelta(days=args.days - 1)).isoformat()
    new_ids = set()
    if args.base_ref:
        res = subprocess.run(["git", "-C", str(ROOT), "show", f"{args.base_ref}:data/news.json"],
                             capture_output=True, text=True)
        if res.returncode == 0:
            old = {i["id"] for i in json.loads(res.stdout)["items"]}
            new_ids = {i["id"] for i in news["items"] if i["id"] not in old}
    # candidatas: as notícias da janela e todas as que entraram nesta edição, mesmo com data de publicação anterior
    candidates = [i for i in news["items"] if start <= i["date"] <= report_date or i["id"] in new_ids]
    # nova = nunca saiu em um relatório anterior (edições com data anterior à deste relatório)
    seen = set()
    for rep in load_log():
        if rep["date"] < report_date:
            seen.update(rep["ids"])
    items = candidates
    new_ids = {i["id"] for i in items if i["id"] not in seen}
    if weekly:  # semanal: só as notícias da semana (D-6 a D), sem controle de "novas"
        items = [i for i in news["items"] if start <= i["date"] <= report_date]
        new_ids = set()
    NEW_IDS.clear()
    NEW_IDS.update(new_ids)
    new_items = sorted([i for i in items if i["id"] in new_ids], key=rank_key)

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
    idx = dt.date.fromisoformat(report_date).toordinal()
    if LANG == "zh":
        message = args.message_zh or ZH_MESSAGES[idx % len(ZH_MESSAGES)]
    else:
        message = args.message or MESSAGES[idx % len(MESSAGES)]

    n_watch = sum(1 for i in items if is_focus(i))
    n_co = len({i["operator"] for i in items})
    if weekly:
        d0 = dt.date.fromisoformat(start)
        prev = [i for i in news["items"] if (d0 - dt.timedelta(days=7)).isoformat() <= i["date"] < start]
        kpis = [(tr("w_week"), len(items), tr("w_prev", n=len(prev))),
                (tr("k_br"), len(br), tr("k_in")), (tr("k_watch"), n_watch, tr("k_watch_n")),
                (tr("k_co"), n_co, tr("k_co_n"))]
    else:
        kpis = [(tr("k_today"), len(new_items), tr("k_today_n") if new_ids else tr("k_new_n")),
                (tr("k_days", d=args.days), len(items), tr("k_days_n")),
                (tr("k_watch"), n_watch, tr("k_watch_n")), (tr("k_co"), n_co, tr("k_co_n"))]
    kpi_html = "".join(f'<div class="kpi"><div class="label">{esc(a)}</div>'
                       f'<div class="value{" amber" if a == tr("k_watch") else ""}">{b}</div>'
                       f'<div class="note">{esc(c)}</div></div>' for a, b, c in kpis)

    # New in this report (all new stories, at the top)
    top_html = ""
    for n, i in enumerate(new_items, 1):
        pay = " " + tr("pay") if i.get("access") == "paywall" else ""
        focus = focus_tag() if is_focus(i) else ""
        top_html += f"""
<li class="{'focus' if focus else ''}">
  <div class="n">{n:02d}</div>
  <div>
    <div class="t">{esc(ttl(i))}{focus}</div>
    <div class="m"><span class="dot {i["region"]}"></span><b>{esc(op_name(i))}</b> · {esc(country_name(i["country"]))} ·
      {esc(fmt_date(i["date"]))} · {esc(cat_name(i["category"]))} · <a class="src" href="{esc(i["url"])}">{esc(i["source"])}</a>{pay}</div>
  </div>
  <div class="r">{rel_html(i["relevance"], label=False)}<span class="lvl">{esc(rel_name(i["relevance"]))}</span></div>
</li>"""

    # Full report: Brazil
    def pick(names):
        return [i for i in br if i["operator"] in names]
    listed = set(ONSHORE + OFFSHORE + SUPPLIERS)
    brazil_html = (
        group_html(tr("g_on"), pick(ONSHORE), new_ids)
        + group_html(tr("g_off"), pick(OFFSHORE), new_ids)
        + group_html(tr("g_sup"), pick(SUPPLIERS), new_ids)
        + group_html(tr("g_other"), [i for i in br if i["operator"] not in listed], new_ids)
    )
    # Full report: South America
    codes = COUNTRY_ORDER + sorted({i["country"] for i in sa} - set(COUNTRY_ORDER))
    sa_html = "".join(group_html(country_name(c), [i for i in sa if i["country"] == c], new_ids) for c in codes)

    # Coverage
    counts, new_counts = {}, {}
    for i in items:
        counts[i["operator"]] = counts.get(i["operator"], 0) + 1
        if i["id"] in new_ids:
            new_counts[i["operator"]] = new_counts.get(i["operator"], 0) + 1
    scale = max([counts.get(n, 0) for n in listed] + [1])
    cov_html = (coverage_html(tr("g_on"), ONSHORE, counts, new_counts, scale)
                + coverage_html(tr("cov_off"), OFFSHORE, counts, new_counts, scale)
                + coverage_html(tr("g_sup"), SUPPLIERS, counts, new_counts, scale))
    missing = [n for n in ONSHORE + OFFSHORE + SUPPLIERS if not counts.get(n)]
    sep = "、" if LANG == "zh" else ", "
    nonews = (f'<div class="nonews"><b>{tr("nonews")}</b>{esc(sep.join(missing))}{"。" if LANG == "zh" else "."}</div>'
              if missing else "")

    # A análise do agente só entra se --analysis for passado (desligada desde 13/11/2026).
    analysis_block = analysis_html(load_analysis(args.analysis), len(items), len(new_items))
    edition = args.edition or tr("edition_w" if weekly else "edition")
    days = args.days
    prep_name = "Li Marcitao"
    prep = (f'<div class="prep"><div class="avatar">{avatar}</div><div class="by">{tr("prep")}'
            f'<b>{prep_name}</b></div></div>' if LANG == "en" else
            f'<div class="prep"><div class="avatar">{avatar}</div><div class="by"><b>{tr("prep")} {prep_name} 编制</b></div></div>')
    if weekly:
        period = tr("w_period", a=fmt_date(start, long=True), b=fmt_date(report_date, long=True))
    else:
        period = tr("window", a=fmt_date(start), b=fmt_date(report_date), t=f"{updated:%H:%M}")
    masthead = f"""
<header class="mast">
  <div class="brandrow"><span class="brand"><b>Hilong</b> Brasil<span>{tr("tagline")}</span></span></div>
  <div class="titlerow"><div><h1>Market Report<i>.</i></h1><div class="ed">{esc(edition)}</div></div>{prep}</div>
  <div class="dateline"><span><b>{esc(fmt_date(report_date, long=True))}</b></span><span>{esc(period)}</span></div>
</header>
<div class="accent-strip"></div>
<section class="kpis">{kpi_html}</section>
"""
    sign = f"""
<section class="sign">
  <div class="avatar">{avatar}</div>
  <div>
    <div class="msg">{esc(message)}</div>
    <div class="who"><b>{"Li Marcitao"}</b> · {tr("who")} · <a href="{SITE}">marketreportnews.hilongbrazil.com</a></div>
  </div>
</section>
"""
    new_section = (f'<ol class="top">{top_html}</ol>' if new_items
                   else f'<p style="margin:4mm 0;color:#55686E">{esc(tr("new_none", d=days))}</p>')
    analysis_block = ""
    if weekly:
        events = load_next_week(args.next_week, report_date)[:4]
        tl, tiles, rows = weekly_sections(items, start, report_date, co_limit=max(3, 8 - 2 * len(events)))
        next_html = next_week_html(events)
        body = f"""{masthead}
<section class="sec first pad"><div class="sec-h"><h2>{tr("top_h")}</h2><span class="hint">{tr("new_hint")}</span></div>
  {top_rows_html(items, new_ids)}</section>
{catbar_html(items)}
<section class="sec pad" style="margin-top:4mm"><div class="sec-h"><h2>{tr("cocite_h")}</h2></div><p style="font-size:9.6pt;margin:2mm 0 0">{cocite_html(items)}</p></section>
<section class="sec pad page-break first"><div class="sec-h"><h2>{tr("w_tl")}</h2><span class="hint">{tr("w_tl_hint")}</span></div>{tl}</section>
<section class="sec pad"><div class="sec-h"><h2>{tr("w_theme")}</h2></div><div class="tiles">{tiles}</div></section>
<section class="sec pad"><div class="sec-h"><h2>{tr("w_co")}</h2><span class="hint">{tr("w_co_hint")}</span></div>
  <table class="cotable">{rows}</table></section>
{next_html}
{sign}
"""
    else:
        cover_top = top_rows_html(new_items, new_ids) if new_items else new_section
        body = f"""{masthead}
<section class="sec first pad">
  <div class="sec-h"><h2>{tr("top_h")}</h2><span class="hint">{tr("new_hint")}</span></div>
  {cover_top}
</section>
{catbar_html(items)}
<section class="sec pad" style="margin-top:4mm"><div class="sec-h"><h2>{tr("cocite_h")}</h2></div><p style="font-size:9.6pt;margin:2mm 0 0">{cocite_html(items)}</p></section>
{sign}

<section class="sec pad page-break first">
  <div class="sec-h"><h2>{tr("new_h")}</h2><span class="hint">{tr("new_hint")}</span></div>
  {new_section}
</section>

<section class="sec pad page-break">
  <div class="sec-h"><h2>{tr("br_h")}</h2><span class="hint">{esc(tr("hist_hint", n=len(br), d=days))}</span></div>
  {brazil_html}
</section>

<section class="sec pad page-break">
  <div class="sec-h"><h2>{tr("sa_h")}</h2><span class="hint">{esc(tr("hist_hint", n=len(sa), d=days))}</span></div>
  {sa_html}
</section>

<section class="sec pad" style="break-inside: avoid">
  <div class="sec-h"><h2>{tr("cov_h")}</h2><span class="hint">{esc(tr("cov_hint", d=days))}</span></div>
  <div class="cov">{cov_html}</div>
  {nonews}
</section>
<p class="method">{esc(tr("method", d=days))}</p>
"""
    html_lang = "zh-CN" if LANG == "zh" else "en"
    css = font_css() + CSS + (THEME_WEEKLY if weekly else "") + (CSS_ZH if LANG == "zh" else "")
    doc = (f'<!DOCTYPE html><html lang="{html_lang}"><head><meta charset="utf-8"><title>{esc(tr("doc_title_w" if weekly else "doc_title", d=report_date))}</title>'
           f"<style>{css}</style></head><body>{body}</body></html>")
    page = tr("page", p='<span class="pageNumber"></span>', t='<span class="totalPages"></span>')
    footer = (
        '<div style="width:100%;padding:0 15mm;font-family:Inter,Helvetica,Arial,\'Noto Sans CJK SC\',sans-serif;font-size:7pt;color:#55686E;'
        'display:flex;justify-content:space-between;align-items:center;-webkit-print-color-adjust:exact;">'
        f'<span><b style="color:#13262B">Hilong Brasil</b> · {tr("footer")} · {esc(fmt_date(report_date))}</span>'
        '<span>marketreportnews.hilongbrazil.com</span>'
        f'<span>{page}</span></div>'
    )
    email = email_bodies(start, report_date, args.alert, attached=tuple(args.email_langs.split(",")), weekly=weekly)
    stats = {"date": report_date, "start": start, "stories": len(items), "new_br": br_new, "new_sa": sa_new,
             "ids": [i["id"] for i in items], "brief": brief_md(report_date, items, new_ids)}
    return doc, footer, stats, email


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="caminho do PDF (sem --out, use --brief para só gravar o briefing)")
    ap.add_argument("--date")
    ap.add_argument("--kind", choices=["daily", "weekly"], default="daily", help="edição diária (padrão) ou semanal")
    ap.add_argument("--days", type=int, default=None)
    ap.add_argument("--base-ref", default="HEAD")
    ap.add_argument("--edition")
    ap.add_argument("--message")
    ap.add_argument("--message-zh", help="mensagem positiva em chinês (com --lang zh)")
    ap.add_argument("--lang", choices=["en", "zh"], default="en", help="idioma do PDF")
    ap.add_argument("--email-langs", default="en,zh", help="relatórios citados no corpo do e-mail")
    ap.add_argument("--html", help="também grava o HTML intermediário neste caminho")
    ap.add_argument("--email-html", help="grava o corpo do e-mail em HTML")
    ap.add_argument("--email-text", help="grava o corpo do e-mail em texto simples")
    ap.add_argument("--alert", help="aviso na primeira linha do e-mail (ex.: falha no push)")
    ap.add_argument("--check-scan", action="store_true",
                    help="avisa no e-mail se data/run.json não for de hoje (varredura não terminou)")
    ap.add_argument("--record", action="store_true",
                    help="registra esta edição em data/reports.json (usar só no envio real, não em testes)")
    ap.add_argument("--brief", help="grava a lista das notícias do relatório (markdown) para o agente escrever a análise")
    ap.add_argument("--next-week", help="JSON com datas confirmadas da semana seguinte (só no semanal; seção omitida se vazio)")
    ap.add_argument("--analysis", help="análise do agente em JSON (headline, points, hilong), no topo do PDF")
    args = ap.parse_args()
    if not args.out and not args.brief:
        ap.error("informe --out (PDF) ou --brief (só o briefing)")

    global LANG
    LANG = args.lang
    doc, footer, stats, email = build_html(args)
    if args.brief:
        Path(args.brief).write_text(stats["brief"], encoding="utf-8")
        if not args.out:
            print(f"OK: briefing {args.brief} ({stats['stories']} stories, edition {stats['date']})")
            return 0
    if args.html:
        Path(args.html).write_text(doc, encoding="utf-8")
    if args.email_html:
        Path(args.email_html).write_text(email[0], encoding="utf-8")
    if args.email_text:
        Path(args.email_text).write_text(email[1], encoding="utf-8")
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
    if args.record and args.kind == "daily":
        record_report(stats["date"], stats["ids"])
    print(f"OK: {args.out} ({stats['stories']} stories, edition {stats['date']}, "
          f"new: {stats['new_br']} Brazil, {stats['new_sa']} South America)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
