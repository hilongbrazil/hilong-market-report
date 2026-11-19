"""Li Marcitão — lista diária de oportunidades Petrobras para a China (inglês e chinês).
Uso: python3 build_china.py china.json email.html email.txt lista.xlsx
china.json = {"date_en": "20 Nov 2026", "date_zh": "2026年11月20日", "link": "https://hilongbrazil.com/interesse/?t=",
              "items": [{num, novo (true nas novas do dia), objeto_en, objeto_zh, resumo_en, resumo_zh, linha (nome em PT),
                         aderencia (alta|média), tipo (servico|produto|ambos), ambiente (onshore|offshore|ambos), ppu (true|false),
                         prazo ("DD/MM/AAAA HH:MM"), end_date, local, status (pending|approved|rejected), tok_int, tok_no}]}
Botões: "Interested / 有兴趣" e "Not interested / 无兴趣" (clicada sem interesse, sai da lista na próxima atualização).
As novas vêm no topo (marcadas NEW / 新); depois, todas as abertas, pelo prazo. Imprime o assunto sugerido."""
import html, json, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

NAVY, ORANGE, INK, MUTED, LINE, TILE, BG, AMBER, GREEN = "#0B2545", "#E8711A", "#1F2A37", "#5A6B7F", "#E2E8F0", "#EEF2F7", "#F3F5F8", "#FFF4E8", "#1E8E5A"
FONT = "Inter,'Segoe UI','Microsoft YaHei',Helvetica,Arial,sans-serif"
e = html.escape
TIPO = {"servico": ("Service", "服务"), "produto": ("Product", "产品"), "ambos": ("Service + Product", "服务 + 产品")}
AMB = {"onshore": ("Onshore", "陆上"), "offshore": ("Offshore", "海上"), "ambos": ("Onshore + Offshore", "陆上 + 海上")}
FIT = {"alta": ("High fit", "高度匹配"), "média": ("Medium fit", "中等匹配")}
ST = {"pending": ("Under review", "审核中"), "approved": ("Hilong pursuing", "海隆参与"), "rejected": ("Hilong not pursuing", "海隆不参与")}
LINES = {
    "Serviços de sonda": ("Rig services", "钻修井服务"), "Elevação artificial": ("Artificial lift", "人工举升"), "Completação": ("Completion", "完井"),
    "OCTG e hastes": ("OCTG & sucker rods", "油套管及抽油杆"), "Facilities": ("Facilities", "地面设施"), "Dutos": ("Pipelines", "管道"),
    "Drill pipe / landing string": ("Drill pipe / landing string", "钻杆 / 坐落管柱"), "Serviços offshore": ("Offshore services", "海上服务"),
    "Ferramentas de poço": ("Downhole tools", "井下工具"), "Cabeça de poço e válvulas": ("Wellhead & valves", "井口及阀门"),
    "Fluidos e serviços de poço": ("Fluids & well services", "钻完井液及井服务"), "Submarino": ("Subsea", "水下设备"),
    "Sísmica e geofísica": ("Seismic & geophysics", "地震及地球物理"), "Refino e downstream": ("Refining & downstream", "炼化及下游"),
    "Embarcações": ("Vessels", "船舶"), "EPC de plataforma": ("Platform EPC", "平台 EPC"),
}


def pair(d, k, i):
    return d.get(k, ("", ""))[i] if k in d else ""


def ppu_txt(o, i):
    if o.get("ppu") is True:
        return ("PPU attached in tender – mandatory", "招标附 PPU – 必须填写")[i]
    if o.get("ppu") is False:
        return ("No PPU – price entered in Petronect", "无 PPU – 价格在 Petronect 填报")[i]
    return ""


def chip(txt, color=NAVY, border=LINE):
    return (f'<span style="display:inline-block;border:1px solid {border};border-radius:12px;padding:2px 8px;margin:0 5px 4px 0;'
            f'font-family:{FONT};font-size:10.5px;font-weight:600;color:{color};">{e(txt)}</span>')


def buttons(o, link, small=False):
    c = "bs" if small else "b"
    out = ""
    if o.get("tok_int"):
        out += f'<a class="{c} bi" href="{e(link + o["tok_int"])}">Interested · 有兴趣</a>'
    if o.get("tok_no"):
        out += f'<a class="{c} bn" href="{e(link + o["tok_no"])}">Not interested · 无兴趣</a>'
    return out


def card(o, link):
    ln = LINES.get(o.get("linha", ""), (o.get("linha", ""), o.get("linha", "")))
    chips = "".join(chip(x) for x in [
        f'{pair(TIPO, o.get("tipo"), 0)} · {pair(TIPO, o.get("tipo"), 1)}' if o.get("tipo") in TIPO else "",
        f'{pair(AMB, o.get("ambiente"), 0)} · {pair(AMB, o.get("ambiente"), 1)}' if o.get("ambiente") in AMB else "",
        f'{pair(FIT, o.get("aderencia"), 0)} · {pair(FIT, o.get("aderencia"), 1)}' if o.get("aderencia") in FIT else "",
    ] if x)
    pp = ppu_txt(o, 0)
    ppu = (f'<div style="margin-top:6px;font-family:{FONT};font-size:11.5px;line-height:16px;font-weight:600;color:{ORANGE if o.get("ppu") else NAVY};">'
           f'{e(pp)} · {e(ppu_txt(o, 1))}</div>') if pp else ""
    return f"""<tr><td style="padding:0 0 12px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-left:4px solid {ORANGE};border-radius:8px;">
<tr><td style="padding:14px 16px;">
  <div style="font-family:{FONT};font-size:11px;font-weight:700;letter-spacing:.5px;color:{MUTED};"><span style="background:{ORANGE};color:#fff;border-radius:4px;padding:2px 6px;margin-right:8px;">NEW · 新</span>{e(o["num"])} · {e(ln[0])} · {e(ln[1])}</div>
  <div style="font-family:{FONT};font-size:15px;line-height:21px;font-weight:700;color:{NAVY};padding-top:8px;">{e(o.get("objeto_en", ""))}</div>
  <div style="font-family:{FONT};font-size:14px;line-height:21px;font-weight:600;color:{NAVY};">{e(o.get("objeto_zh", ""))}</div>
  <div style="padding-top:6px;">{chips}</div>{ppu}
  <div style="font-family:{FONT};font-size:12.5px;line-height:19px;color:{INK};padding-top:8px;">{e(o.get("resumo_en", ""))}</div>
  <div style="font-family:{FONT};font-size:12.5px;line-height:19px;color:{INK};padding-top:4px;">{e(o.get("resumo_zh", ""))}</div>
  <div style="font-family:{FONT};font-size:11.5px;color:{NAVY};font-weight:600;padding-top:8px;">Deadline · 投标截止: {e(o.get("prazo", ""))} BRT{(" &nbsp;·&nbsp; " + e(o["local"])) if o.get("local") else ""}</div>
  <div style="padding-top:10px;">{buttons(o, link)}</div>
</td></tr></table></td></tr>"""


def row(o, n, link):
    st = ST.get(o.get("status"), ("", ""))
    sc = "sa" if o.get("status") == "approved" else ("sr" if o.get("status") == "rejected" else "sp")
    meta = " · ".join(x for x in [pair(TIPO, o.get("tipo"), 0), pair(AMB, o.get("ambiente"), 0), "PPU" if o.get("ppu") else ("No PPU" if o.get("ppu") is False else "")] if x)
    meta_zh = " · ".join(x for x in [pair(TIPO, o.get("tipo"), 1), pair(AMB, o.get("ambiente"), 1), "有 PPU" if o.get("ppu") else ("无 PPU" if o.get("ppu") is False else "")] if x)
    nw = '<br><b class="nw">NEW 新</b>' if o.get("novo") else ""
    pz = o.get("prazo") or ""
    return (f'<tr class="{"z" if n % 2 else ""}"><td class="c1">{e(o["num"])}{nw}</td>'
            f'<td class="c2"><b>{e(o.get("objeto_en", ""))}</b><br>{e(o.get("objeto_zh", ""))}<br><span class="m">{e(meta)} · {e(meta_zh)}</span>'
            f'<br><span class="{sc}">{e(st[0])} · {e(st[1])}</span><div class="bt">{buttons(o, link, True)}</div></td>'
            f'<td class="c3">{e(pz[:10])}<br><span class="m">{e(pz[11:16])}</span></td></tr>')


AVATAR = "https://hilongbrazil.com/assets/img/li-marcitao-petronect-face.jpg"
HERO = "https://hilongbrazil.com/assets/img/li-marcitao-petronect.jpg"

HOW = [
    ("Daily list of Petrobras (Petronect) opportunities within Hilong's scope. It is sent only on days with new opportunities.",
     "本清单每日汇总海隆业务范围内的巴西国家石油公司（Petronect）招标商机，仅在有新商机的日子发送。"),
    ("New opportunities are at the top, marked NEW / 新. Below them, every opportunity still open, ordered by proposal deadline.",
     "新商机列于顶部并标注 NEW / 新；其下为所有仍在招标中的商机，按投标截止时间排序。"),
    ("For each opportunity, click Interested or Not interested and press Confirm on the page that opens. Marcio Vianna and Li Kewei are notified.",
     "请对每个商机点击“有兴趣”或“无兴趣”，并在打开的页面上点击“确认”；系统将通知 Marcio Vianna 和 Li Kewei。"),
    ("Not interested: the opportunity leaves the list. No click: it stays on the list until the deadline. You can change your answer by clicking the other button.",
     "点击“无兴趣”后，该商机将从清单中移除；未点击的商机将保留至截止日期。点击另一个按钮即可更改选择。"),
    ("Status: Under review, Hilong pursuing or Hilong not pursuing. When Hilong Brazil approves an opportunity, you receive the full email with the technical specifications and the PPU.",
     "状态：审核中、海隆参与或海隆不参与。海隆巴西批准后，您将收到包含技术规格和 PPU 的完整邮件。"),
]


def how_rows():
    return "".join(
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:7px;"><tr>'
        f'<td valign="top" width="20" style="font-family:{FONT};font-size:12px;font-weight:700;color:{ORANGE};">{i}.</td>'
        f'<td style="font-family:{FONT};font-size:12px;line-height:18px;color:{INK};">{e(en)}<br><span style="color:{MUTED};">{e(zh)}</span></td></tr></table>'
        for i, (en, zh) in enumerate(HOW, 1))


def build(d):
    items = d["items"]
    new = [o for o in items if o.get("novo")]
    rest = sorted(items, key=lambda o: (o.get("end_date") or "9999", (o.get("prazo") or "")[-5:], o["num"]))
    link = d["link"]
    cards = "".join(card(o, link) for o in sorted(new, key=lambda o: (o.get("aderencia") != "alta", o.get("end_date") or "")))
    rows = "".join(row(o, n, link) for n, o in enumerate(rest))
    sec = lambda en, zh: (f'<tr><td style="padding:22px 0 10px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
                          f'<td width="4" style="background:{ORANGE};border-radius:2px;font-size:0;">&nbsp;</td>'
                          f'<td style="padding-left:10px;font-family:{FONT};font-size:12px;font-weight:700;letter-spacing:1px;color:{NAVY};">{e(en)} · {e(zh)}</td></tr></table></td></tr>')
    how_rows_html = how_rows()
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(d.get("subject", ""))}</title>
<style>
a.b,a.bs{{display:inline-block;text-decoration:none;border-radius:6px;font-family:{FONT};font-weight:700;margin:0 6px 4px 0}}
a.b{{padding:9px 14px;font-size:12px}} a.bs{{padding:5px 9px;font-size:10.5px}}
a.bi{{background:{ORANGE};color:#ffffff;border:1px solid {ORANGE}}} a.bn{{color:{MUTED};border:1px solid {MUTED}}}
td.c1{{padding:9px 8px 9px 10px;font-family:{FONT};font-size:11px;color:{MUTED};white-space:nowrap;vertical-align:top}}
td.c2{{padding:9px 8px;font-family:{FONT};font-size:12px;line-height:17px;color:{INK};vertical-align:top}} td.c2 b{{color:{NAVY}}}
td.c3{{padding:9px 10px 9px 8px;font-family:{FONT};font-size:11.5px;line-height:16px;color:{NAVY};font-weight:600;white-space:nowrap;vertical-align:top}}
tr.z td{{background:{TILE}}} .m{{color:{MUTED};font-size:11px;font-weight:400}} .nw{{color:{ORANGE}}} .bt{{padding-top:5px}}
.sp{{color:{NAVY};font-size:11px;font-weight:600}} .sa{{color:{GREEN};font-size:11px;font-weight:600}} .sr{{color:{MUTED};font-size:11px;font-weight:600}}
</style></head>
<body style="margin:0;padding:0;background:{BG};">
<div style="display:none;max-height:0;overflow:hidden;">{len(new)} new Petrobras opportunities · 新增 {len(new)} 项巴西国家石油公司商机</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="width:640px;max-width:640px;background:#FFFFFF;border:1px solid {LINE};border-radius:10px;overflow:hidden;">
<tr><td style="background:{NAVY};padding:22px 24px 22px 30px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td valign="middle">
  <div style="font-family:{FONT};font-size:10.5px;font-weight:600;letter-spacing:1px;color:#B8C9DE;">HILONG BRAZIL · PETRONECT · EN / 中文</div>
  <div style="font-family:{FONT};font-size:23px;line-height:29px;font-weight:700;color:#FFFFFF;padding-top:10px;">Petrobras opportunities · {e(d["date_en"])}</div>
  <div style="font-family:{FONT};font-size:19px;line-height:27px;font-weight:700;color:#FFFFFF;">巴西国家石油公司商机 · {e(d["date_zh"])}</div>
  <div style="font-family:{FONT};font-size:13px;line-height:19px;color:#D1DEED;padding-top:6px;">{len(new)} new today · {len(items)} open in total<br>今日新增 {len(new)} 项 · 共 {len(items)} 项在招</div>
  </td>
  <td width="168" valign="middle" align="right" style="padding-left:12px;"><img src="{HERO}" width="160" height="160" alt="Li Marcit&atilde;o" style="display:block;width:160px;height:160px;border-radius:10px;border:2px solid #58CFFF;"></td>
</tr></table></td></tr>
<tr><td style="background:{AMBER};padding:16px 30px;font-family:{FONT};font-size:12px;line-height:18px;color:{INK};">
  <div style="font-size:11px;font-weight:700;letter-spacing:.8px;color:{ORANGE};">HOW THIS LIST WORKS · 使用说明</div>
  {how_rows_html}
</td></tr>
<tr><td style="padding:6px 30px 26px 30px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
  {sec("NEW TODAY", "今日新增") + cards if new else ""}
  {sec("ALL OPEN OPPORTUNITIES", "全部在招商机")}
  <tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;border-collapse:separate;overflow:hidden;">
    <tr style="background:{NAVY};"><td style="padding:8px 8px 8px 10px;font-family:{FONT};font-size:10px;font-weight:700;color:#fff;">PETRONECT</td>
    <td style="padding:8px;font-family:{FONT};font-size:10px;font-weight:700;color:#fff;">OPPORTUNITY · 商机</td>
    <td style="padding:8px 10px 8px 8px;font-family:{FONT};font-size:10px;font-weight:700;color:#fff;">DEADLINE · 截止</td></tr>
    {rows}
  </table></td></tr>
</table></td></tr>
<tr><td style="background:{BG};padding:20px 30px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="64" valign="middle"><img src="{AVATAR}" width="56" height="56" alt="Li Marcit&atilde;o" style="display:block;width:56px;height:56px;border-radius:28px;border:2px solid {ORANGE};"></td>
  <td valign="middle" style="padding-left:12px;">
  <div style="font-family:{FONT};font-size:14px;font-weight:700;color:{NAVY};">Li Marcit&atilde;o</div>
  <div style="font-family:{FONT};font-size:11.5px;line-height:16px;color:{MUTED};padding-top:4px;">Market &amp; Tender Intelligence · works for Li Kewei and Marcio Vianna · Hilong Brazil</div>
  </td></tr></table>
</td></tr>
</table></td></tr></table></body></html>"""


def text(d):
    items = d["items"]; new = [o for o in items if o.get("novo")]
    out = [f"Petrobras opportunities · {d['date_en']} / 巴西国家石油公司商机 · {d['date_zh']}",
           f"{len(new)} new today · {len(items)} open / 今日新增 {len(new)} 项 · 共 {len(items)} 项", "", "HOW THIS LIST WORKS · 使用说明"]
    out += [f"{i}. {en}\n   {zh}" for i, (en, zh) in enumerate(HOW, 1)] + [""]
    if new:
        out.append("NEW TODAY · 今日新增")
        for o in new:
            out += [f"* {o['num']} · {o.get('objeto_en','')} / {o.get('objeto_zh','')}",
                    f"  {pair(TIPO, o.get('tipo'), 0)} · {pair(AMB, o.get('ambiente'), 0)} · {ppu_txt(o, 0)} · deadline {o.get('prazo','')} BRT",
                    f"  Interested / 有兴趣: {d['link']}{o.get('tok_int','')}", f"  Not interested / 无兴趣: {d['link']}{o.get('tok_no','')}", ""]
    out.append("ALL OPEN · 全部在招")
    for o in sorted(items, key=lambda o: (o.get("end_date") or "9999", (o.get("prazo") or "")[-5:], o["num"])):
        out.append(f"- {o['num']} · {o.get('objeto_en','')} / {o.get('objeto_zh','')} · {o.get('prazo','')} · {ST.get(o.get('status'),('',''))[0]}")
    out += ["", "Li Marcitão · Hilong Brazil"]
    return "\n".join(out)


def xlsx(d, path):
    wb = Workbook(); ws = wb.active; ws.title = "Opportunities"
    hdr = ["New 新", "Petronect", "Opportunity (EN)", "商机 (中文)", "Line 业务", "Fit 匹配", "Type 类型", "Environment 环境",
           "PPU", "Deadline 截止 (BRT)", "Location 地点", "Status 状态", "Summary (EN)", "摘要 (中文)"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="0B2545"); c.alignment = Alignment(wrap_text=True, vertical="center")
    items = sorted(d["items"], key=lambda o: (not o.get("novo"), o.get("end_date") or "9999", (o.get("prazo") or "")[-5:], o["num"]))
    for o in items:
        ln = LINES.get(o.get("linha", ""), (o.get("linha", ""), ""))
        ws.append(["NEW 新" if o.get("novo") else "", o["num"], o.get("objeto_en", ""), o.get("objeto_zh", ""), f"{ln[0]} {ln[1]}".strip(),
                   " ".join(FIT.get(o.get("aderencia"), ("", ""))).strip(), " ".join(TIPO.get(o.get("tipo"), ("", ""))).strip(),
                   " ".join(AMB.get(o.get("ambiente"), ("", ""))).strip(), f"{ppu_txt(o, 0)} {ppu_txt(o, 1)}".strip(), o.get("prazo", ""),
                   o.get("local", ""), " ".join(ST.get(o.get("status"), ("", ""))).strip(), o.get("resumo_en", ""), o.get("resumo_zh", "")])
    for col, w in zip("ABCDEFGHIJKLMN", [8, 12, 44, 34, 22, 16, 18, 20, 30, 16, 18, 20, 60, 50]):
        ws.column_dimensions[col].width = w
    for r in ws.iter_rows(min_row=2):
        for c in r:
            c.alignment = Alignment(wrap_text=True, vertical="top")
        if r[0].value:
            for c in r:
                c.fill = PatternFill("solid", fgColor="FFF4E8")
    ws.freeze_panes = "C2"; ws.auto_filter.ref = ws.dimensions
    wb.save(path)


if __name__ == "__main__":
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    n = sum(1 for o in d["items"] if o.get("novo"))
    d.setdefault("subject", f"Petrobras opportunities · {d['date_en']} · {n} new / 巴西国家石油公司商机 · 新增 {n} 项")
    h = build(d)
    # tamanho: a fonte vai uma vez no <body> e no <style>, não em cada célula
    h = h.replace(f"font-family:{FONT};", "").replace(f"{{font-family:{FONT};", "{")
    h = h.replace('<body style="margin:0;padding:0;', f'<body style="margin:0;padding:0;font-family:{FONT};', 1)
    h = h.replace("<style>", f"<style>\ntable,td,div,span,a{{font-family:{FONT}}}", 1)
    open(sys.argv[2], "w", encoding="utf-8").write(h)
    open(sys.argv[3], "w", encoding="utf-8").write(text(d))
    xlsx(d, sys.argv[4])
    print("ok", d["subject"])
