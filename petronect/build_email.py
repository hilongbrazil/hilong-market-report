"""Builds the Hilong Petrobras-opportunity email (HTML + plain text) from a data dict.
Mirrors the Figma template 'Hilong – Petrobras Opportunity Email Template' (file jtgMaB26vle6i51mMs7JHP)."""
import json, html, sys

NAVY, ORANGE, INK, MUTED, LINE, TILE, BG, AMBER = "#0B2545", "#E8711A", "#1F2A37", "#5A6B7F", "#E2E8F0", "#EEF2F7", "#F3F5F8", "#FFF4E8"
FONT = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
e = html.escape

# classificação (valores gravados no banco) -> rótulos EN / ZH
TIPO = {"servico": ("Service", "服务"), "produto": ("Product", "产品"), "ambos": ("Service + Product", "服务 + 产品")}
AMB = {"onshore": ("Onshore", "陆上"), "offshore": ("Offshore", "海上"), "ambos": ("Onshore + Offshore", "陆上 + 海上")}
T = {  # títulos das seções
    "en": {"sum": "EXECUTIVE SUMMARY", "view": "HILONG VIEW", "scope": "SCOPE", "desc": "DESCRIPTION", "qty": "QTY", "dest": "DESTINATION",
           "req": "KEY TECHNICAL REQUIREMENTS", "com": "COMMERCIAL & QUALIFICATION", "att": "ATTACHED DOCUMENTS",
           "type": "TYPE", "env": "ENVIRONMENT", "ppu": "PPU (PRICE SHEET)", "yes": "Attached", "no": "Not in tender",
           "ppu_yes": "PPU attached: filling in and submitting the PPU is mandatory for the proposal.",
           "ppu_no": "No PPU in this tender: prices must be entered directly in the Petronect system."},
    "zh": {"sum": "执行摘要", "view": "海隆观点", "scope": "采购范围", "desc": "描述", "qty": "数量", "dest": "交付地点",
           "req": "主要技术要求", "com": "商务及资质要求", "att": "附件",
           "type": "类型", "env": "作业环境", "ppu": "PPU（报价单）", "yes": "已附", "no": "招标文件中无",
           "ppu_yes": "已附 PPU：投标时必须填写并提交该 PPU。",
           "ppu_no": "本招标无 PPU：价格必须直接在 Petronect 系统中填报。"},
}


def chips(d, lang):
    """Etiquetas de classificação: tipo, ambiente e PPU."""
    i = 0 if lang == "en" else 1
    t = T[lang]
    vals = []
    if d.get("tipo") in TIPO: vals.append((t["type"], TIPO[d["tipo"]][i]))
    if d.get("ambiente") in AMB: vals.append((t["env"], AMB[d["ambiente"]][i]))
    if "ppu" in d: vals.append((t["ppu"], t["yes"] if d["ppu"] else t["no"]))
    if not vals:
        return ""
    cells = "".join(
        f'<td style="padding:0 6px 6px 0;"><span style="display:inline-block;border:1px solid {LINE};border-radius:14px;padding:5px 11px;font-family:{FONT};font-size:11px;color:{INK};">'
        f'<b style="color:{MUTED};font-size:9.5px;letter-spacing:.6px;">{e(l)}</b>&nbsp; <b style="color:{NAVY};">{e(v)}</b></span></td>' for l, v in vals)
    note = ""
    if "ppu" in d:
        note = (f'<tr><td style="padding-bottom:14px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
                f'<td style="background:{AMBER};border-left:3px solid {ORANGE};border-radius:6px;padding:9px 12px;font-family:{FONT};font-size:12px;line-height:17px;font-weight:600;color:{INK};">'
                f'{e(t["ppu_yes"] if d["ppu"] else t["ppu_no"])}</td></tr></table></td></tr>')
    return f'<tr><td style="padding-bottom:12px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>{cells}</tr></table></td></tr>' + note


def section_title(t):
    return (f'<tr><td style="padding:26px 0 12px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td width="4" style="background:{ORANGE};border-radius:2px;font-size:0;line-height:0;">&nbsp;</td>'
            f'<td style="padding-left:10px;font-family:{FONT};font-size:12px;font-weight:700;letter-spacing:1px;color:{NAVY};">{e(t)}</td>'
            f'</tr></table></td></tr>')


def bullets(items):
    rows = "".join(
        f'<tr><td valign="top" width="16" style="font-family:{FONT};font-size:13px;line-height:20px;color:{ORANGE};font-weight:700;">&bull;</td>'
        f'<td style="font-family:{FONT};font-size:13px;line-height:20px;color:{INK};padding-bottom:7px;">{e(i)}</td></tr>' for i in items)
    return f'<tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table></td></tr>'


def subhead(t):
    return f'<tr><td style="font-family:{FONT};font-size:12.5px;line-height:18px;font-weight:600;color:{NAVY};padding:4px 0 8px 0;">{e(t)}</td></tr>'


def approval_block(d):
    url = d.get("approval_url")
    if not url:
        return ""
    return (f'<tr><td style="background:{AMBER};border-bottom:1px solid #F6D9B8;padding:16px 32px;">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td valign="middle" style="font-family:{FONT};">'
            f'<div style="font-size:9.5px;font-weight:700;letter-spacing:.8px;color:{ORANGE};">ADMIN APPROVAL REQUIRED</div>'
            f'<div style="font-size:12.5px;line-height:18px;color:{INK};padding-top:3px;">Approve to register this opportunity in the Corporate &amp; Strategic pipeline.</div></td>'
            f'<td align="right" valign="middle" style="padding-left:12px;white-space:nowrap;">'
            f'<a href="{e(url)}" style="display:inline-block;background:{NAVY};color:#FFFFFF;text-decoration:none;font-family:{FONT};font-size:12px;font-weight:700;letter-spacing:.4px;padding:11px 18px;border-radius:6px;">Approve or reject &rarr;</a>'
            f'</td></tr></table></td></tr>')


def body(c, d, lang):
    """Corpo de um idioma. c = textos do idioma (EN = o próprio d; ZH = d['zh']); d = dados comuns."""
    t = T[lang]
    tiles = "".join(
        f'<td width="25%" valign="top" style="padding:0 {4 if i < 3 else 0}px 0 {4 if i else 0}px;">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:{TILE};border-radius:8px;padding:13px 12px;">'
        f'<div style="font-family:{FONT};font-size:9px;font-weight:600;letter-spacing:.8px;color:{MUTED};">{e(l)}</div>'
        f'<div style="font-family:{FONT};font-size:15px;line-height:20px;font-weight:700;color:{NAVY};padding-top:3px;">{e(v)}</div>'
        f'<div style="font-family:{FONT};font-size:10.5px;line-height:14px;color:{MUTED};padding-top:3px;">{e(s)}</div>'
        f'</td></tr></table></td>' for i, (l, v, s) in enumerate(c["facts"]))
    scope_rows = "".join(
        f'<tr style="background:{TILE if n % 2 else "#FFFFFF"};">'
        f'<td valign="top" style="padding:11px 0 11px 12px;font-family:{FONT};font-size:12.5px;font-weight:700;color:{NAVY};">{e(r[0])}</td>'
        f'<td valign="top" style="padding:11px 10px;font-family:{FONT};font-size:12.5px;line-height:18px;color:{INK};">{e(r[1])}</td>'
        f'<td valign="top" style="padding:11px 10px;font-family:{FONT};font-size:12.5px;color:{INK};">{e(r[2])}</td>'
        f'<td valign="top" style="padding:11px 12px 11px 0;font-family:{FONT};font-size:12.5px;line-height:18px;color:{INK};">{e(r[3])}</td></tr>'
        for n, r in enumerate(c["scope"]))
    th = lambda x, w, pl="10px", pr="10px": f'<td width="{w}" style="padding:9px {pr} 9px {pl};font-family:{FONT};font-size:10px;font-weight:700;letter-spacing:.6px;color:#FFFFFF;">{e(x)}</td>'
    req = "".join(subhead(b["title"]) + bullets(b["items"]) for b in c["requirements"])
    atts = "".join(
        f'<tr><td style="padding-bottom:8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;"><tr>'
        f'<td width="34" style="padding:10px 0 10px 12px;"><span style="display:inline-block;background:{NAVY};color:#fff;border-radius:4px;padding:4px 6px;font-family:{FONT};font-size:9px;font-weight:700;letter-spacing:.5px;">{e((n.rsplit(".",1)[-1] if "." in n else "FILE").upper()[:4])}</span></td>'
        f'<td style="padding:10px 12px;"><div style="font-family:{FONT};font-size:12px;line-height:16px;font-weight:600;color:{INK};">{e(n)}</div>'
        f'<div style="font-family:{FONT};font-size:11px;line-height:15px;color:{MUTED};">{e(desc)}</div></td></tr></table></td></tr>'
        for n, desc in c["attachments"])
    return f"""<tr><td style="padding:26px 32px 30px 32px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
    {chips(d, lang)}
    <tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{tiles}</tr></table></td></tr>
    {section_title(t['sum'])}
    <tr><td style="font-family:{FONT};font-size:13.5px;line-height:21px;color:{INK};">{e(c['summary'])}</td></tr>
    <tr><td style="padding-top:12px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td style="background:{AMBER};border-left:3px solid {ORANGE};border-radius:8px;padding:12px 14px;">
        <div style="font-family:{FONT};font-size:9.5px;font-weight:700;letter-spacing:.8px;color:{ORANGE};">{e(t['view'])}</div>
        <div style="font-family:{FONT};font-size:13px;line-height:20px;font-weight:500;color:{INK};padding-top:4px;">{e(c['hilong_view'])}</div>
      </td></tr></table></td></tr>
    {section_title(t['scope'])}
    <tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;border-collapse:separate;overflow:hidden;">
      <tr style="background:{NAVY};">{th('#', 30, '12px', '0')}{th(t['desc'], '')}{th(t['qty'], 44)}{th(t['dest'], 140, '10px', '12px')}</tr>
      {scope_rows}
    </table></td></tr>
    {section_title(t['req'])}
    {req}
    {section_title(t['com'])}
    {bullets(c['commercial'])}
    {section_title(t['att'])}
    {atts}
    <tr><td style="font-family:{FONT};font-size:11.5px;line-height:17px;color:{MUTED};padding-top:2px;">{e(c['package_note'])}</td></tr>
  </table>
</td></tr>"""


def build(d):
    zh = d.get("zh")
    zh_part = ""
    if zh:
        zh_part = (f'<tr><td style="background:{NAVY};padding:14px 32px;font-family:{FONT};">'
                   f'<div style="font-size:16px;font-weight:700;color:#FFFFFF;">中文版 &nbsp;&middot;&nbsp; 机会 {e(d["number"])}</div>'
                   f'<div style="font-size:12.5px;line-height:18px;color:#D1DEED;padding-top:4px;">{e(zh["tagline"])}</div>'
                   f'<div style="font-size:11px;color:#FFD9B8;padding-top:4px;">{e(zh.get("deadline_pill", ""))}</div></td></tr>'
                   + body(zh, d, "zh"))
    foot_zh = f'<div style="font-family:{FONT};font-size:10.5px;line-height:15px;color:{MUTED};padding-top:4px;">{e(zh["footer_note"])}</div>' if zh else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{e(d['subject'])}</title></head>
<body style="margin:0;padding:0;background:{BG};">
<div style="display:none;max-height:0;overflow:hidden;">{e(d['preheader'])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border:1px solid {LINE};border-radius:10px;overflow:hidden;">
<!-- Header -->
<tr><td style="background:{NAVY};padding:28px 32px;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
    <td width="22" height="22" align="center" style="background:{ORANGE};border-radius:6px;font-family:{FONT};font-size:13px;font-weight:800;color:#FFFFFF;">H</td>
    <td style="padding-left:8px;font-family:{FONT};font-size:10.5px;font-weight:600;letter-spacing:1px;color:#B8C9DE;">HILONG BRAZIL &nbsp;&middot;&nbsp; PETROBRAS OPPORTUNITY{' &nbsp;&middot;&nbsp; EN / 中文' if zh else ''}</td>
  </tr></table>
  <div style="font-family:{FONT};font-size:26px;line-height:32px;font-weight:700;color:#FFFFFF;padding-top:12px;">Opportunity {e(d['number'])}</div>
  <div style="font-family:{FONT};font-size:14px;line-height:20px;color:#D1DEED;padding-top:6px;">{e(d['tagline'])}</div>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;"><tr>
    <td style="background:{ORANGE};border-radius:20px;padding:6px 14px;font-family:{FONT};font-size:10.5px;font-weight:700;letter-spacing:.6px;color:#FFFFFF;">{e(d['deadline_pill'])}</td>
  </tr></table>
</td></tr>
{approval_block(d)}
<!-- English -->
{body(d, d, "en")}
<!-- Chinese -->
{zh_part}
<!-- Footer -->
<tr><td style="background:{BG};padding:22px 32px;">
  <div style="font-family:{FONT};font-size:14px;line-height:18px;font-weight:700;color:{NAVY};">Li Marcitao</div>
  <div style="font-family:{FONT};font-size:11.5px;line-height:16px;color:{MUTED};padding-top:4px;">Market &amp; Tender Intelligence &middot; works for Li Kewei and Marcio Vianna &middot; Hilong Brazil</div>
  <div style="border-top:1px solid {LINE};margin-top:10px;padding-top:8px;font-family:{FONT};font-size:10.5px;line-height:15px;color:{MUTED};">{e(d['footer_note'])}</div>
  {foot_zh}
</td></tr>
</table>
</td></tr></table>
</body></html>"""


def text_part(c, d, lang):
    t = T[lang]; i = 0 if lang == "en" else 1
    out = []
    cl = []
    if d.get("tipo") in TIPO: cl.append(f"{t['type']}: {TIPO[d['tipo']][i]}")
    if d.get("ambiente") in AMB: cl.append(f"{t['env']}: {AMB[d['ambiente']][i]}")
    if "ppu" in d: cl.append(f"{t['ppu']}: {t['yes'] if d['ppu'] else t['no']}")
    if cl: out += [" | ".join(cl), ""]
    if "ppu" in d: out += [t["ppu_yes"] if d["ppu"] else t["ppu_no"], ""]
    out += [" | ".join(f"{l}: {v} ({s})" for l, v, s in c["facts"]), "", t["sum"], c["summary"], "", t["view"], c["hilong_view"], "", t["scope"]]
    out += [f"{r[0]}. {r[1]} | {t['qty']} {r[2]} | {r[3]}" for r in c["scope"]]
    out += ["", t["req"]]
    for b in c["requirements"]:
        out += [b["title"]] + [f"- {x}" for x in b["items"]]
    out += ["", t["com"]] + [f"- {x}" for x in c["commercial"]]
    out += ["", t["att"]] + [f"- {n} ({x})" for n, x in c["attachments"]]
    out += ["", c["package_note"]]
    return out


def text_version(d):
    out = [f"PETROBRAS OPPORTUNITY {d['number']}", d["tagline"], d["deadline_pill"], ""]
    if d.get("approval_url"): out += ["ADMIN APPROVAL REQUIRED – approve or reject: " + d["approval_url"], ""]
    out += text_part(d, d, "en")
    if d.get("zh"):
        z = d["zh"]
        out += ["", "=" * 40, f"中文版 · 机会 {d['number']}", z["tagline"], z.get("deadline_pill", ""), ""] + text_part(z, d, "zh")
    out += ["", "Li Marcitao", "Market & Tender Intelligence · works for Li Kewei and Marcio Vianna · Hilong Brazil", d["footer_note"]]
    if d.get("zh"): out.append(d["zh"]["footer_note"])
    return "\n".join(out)


if __name__ == "__main__":
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    open(sys.argv[2], "w", encoding="utf-8").write(build(d))
    open(sys.argv[3], "w", encoding="utf-8").write(text_version(d))
    print("ok")
