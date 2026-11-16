"""Builds the Hilong Petrobras-opportunity email (HTML + plain text) from a data dict.
Mirrors the Figma template 'Hilong – Petrobras Opportunity Email Template' (file jtgMaB26vle6i51mMs7JHP)."""
import json, html, sys

NAVY, ORANGE, INK, MUTED, LINE, TILE, BG, AMBER = "#0B2545", "#E8711A", "#1F2A37", "#5A6B7F", "#E2E8F0", "#EEF2F7", "#F3F5F8", "#FFF4E8"
FONT = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
e = html.escape


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


def build(d):
    tiles = "".join(
        f'<td width="25%" valign="top" style="padding:0 {4 if i < 3 else 0}px 0 {4 if i else 0}px;">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:{TILE};border-radius:8px;padding:13px 12px;">'
        f'<div style="font-family:{FONT};font-size:9px;font-weight:600;letter-spacing:.8px;color:{MUTED};">{e(l)}</div>'
        f'<div style="font-family:{FONT};font-size:15px;line-height:20px;font-weight:700;color:{NAVY};padding-top:3px;">{e(v)}</div>'
        f'<div style="font-family:{FONT};font-size:10.5px;line-height:14px;color:{MUTED};padding-top:3px;">{e(s)}</div>'
        f'</td></tr></table></td>' for i, (l, v, s) in enumerate(d["facts"]))

    scope_rows = "".join(
        f'<tr style="background:{TILE if n % 2 else "#FFFFFF"};">'
        f'<td valign="top" style="padding:11px 0 11px 12px;font-family:{FONT};font-size:12.5px;font-weight:700;color:{NAVY};">{e(r[0])}</td>'
        f'<td valign="top" style="padding:11px 10px;font-family:{FONT};font-size:12.5px;line-height:18px;color:{INK};">{e(r[1])}</td>'
        f'<td valign="top" style="padding:11px 10px;font-family:{FONT};font-size:12.5px;color:{INK};">{e(r[2])}</td>'
        f'<td valign="top" style="padding:11px 12px 11px 0;font-family:{FONT};font-size:12.5px;line-height:18px;color:{INK};">{e(r[3])}</td></tr>'
        for n, r in enumerate(d["scope"]))
    th = lambda t, w, pl="10px", pr="10px": f'<td width="{w}" style="padding:9px {pr} 9px {pl};font-family:{FONT};font-size:10px;font-weight:700;letter-spacing:.6px;color:#FFFFFF;">{t}</td>'

    req = ""
    for block in d["requirements"]:
        req += subhead(block["title"]) + bullets(block["items"])

    atts = "".join(
        f'<tr><td style="padding-bottom:8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;"><tr>'
        f'<td width="34" style="padding:10px 0 10px 12px;"><span style="display:inline-block;background:{NAVY};color:#fff;border-radius:4px;padding:4px 6px;font-family:{FONT};font-size:9px;font-weight:700;letter-spacing:.5px;">{e((n.rsplit(".",1)[-1] if "." in n else "FILE").upper()[:4])}</span></td>'
        f'<td style="padding:10px 12px;"><div style="font-family:{FONT};font-size:12px;line-height:16px;font-weight:600;color:{INK};">{e(n)}</div>'
        f'<div style="font-family:{FONT};font-size:11px;line-height:15px;color:{MUTED};">{e(desc)}</div></td></tr></table></td></tr>'
        for n, desc in d["attachments"])

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
    <td style="padding-left:8px;font-family:{FONT};font-size:10.5px;font-weight:600;letter-spacing:1px;color:#B8C9DE;">HILONG BRAZIL &nbsp;&middot;&nbsp; PETROBRAS OPPORTUNITY</td>
  </tr></table>
  <div style="font-family:{FONT};font-size:26px;line-height:32px;font-weight:700;color:#FFFFFF;padding-top:12px;">Opportunity {e(d['number'])}</div>
  <div style="font-family:{FONT};font-size:14px;line-height:20px;color:#D1DEED;padding-top:6px;">{e(d['tagline'])}</div>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;"><tr>
    <td style="background:{ORANGE};border-radius:20px;padding:6px 14px;font-family:{FONT};font-size:10.5px;font-weight:700;letter-spacing:.6px;color:#FFFFFF;">{e(d['deadline_pill'])}</td>
  </tr></table>
</td></tr>
<!-- Approval -->
{approval_block(d)}
<!-- Body -->
<tr><td style="padding:26px 32px 30px 32px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{tiles}</tr></table></td></tr>
    {section_title('EXECUTIVE SUMMARY')}
    <tr><td style="font-family:{FONT};font-size:13.5px;line-height:21px;color:{INK};">{e(d['summary'])}</td></tr>
    <tr><td style="padding-top:12px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td style="background:{AMBER};border-left:3px solid {ORANGE};border-radius:8px;padding:12px 14px;">
        <div style="font-family:{FONT};font-size:9.5px;font-weight:700;letter-spacing:.8px;color:{ORANGE};">HILONG VIEW</div>
        <div style="font-family:{FONT};font-size:13px;line-height:20px;font-weight:500;color:{INK};padding-top:4px;">{e(d['hilong_view'])}</div>
      </td></tr></table></td></tr>
    {section_title('SCOPE')}
    <tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;border-collapse:separate;overflow:hidden;">
      <tr style="background:{NAVY};">{th('#', 30, '12px', '0')}{th('DESCRIPTION', '')}{th('QTY', 44)}{th('DESTINATION', 140, '10px', '12px')}</tr>
      {scope_rows}
    </table></td></tr>
    {section_title('KEY TECHNICAL REQUIREMENTS')}
    {req}
    {section_title('COMMERCIAL & QUALIFICATION')}
    {bullets(d['commercial'])}
    {section_title('ATTACHED TECHNICAL SPECIFICATIONS')}
    {atts}
    <tr><td style="font-family:{FONT};font-size:11.5px;line-height:17px;color:{MUTED};padding-top:2px;">{e(d['package_note'])}</td></tr>
  </table>
</td></tr>
<!-- Footer -->
<tr><td style="background:{BG};padding:22px 32px;">
  <div style="font-family:{FONT};font-size:14px;line-height:18px;font-weight:700;color:{NAVY};">Li Marcit&atilde;o</div>
  <div style="font-family:{FONT};font-size:11.5px;line-height:16px;color:{MUTED};padding-top:4px;">Market &amp; Tender Intelligence &middot; works for Li Kewei and Marcio Vianna &middot; Hilong Brazil</div>
  <div style="border-top:1px solid {LINE};margin-top:10px;padding-top:8px;font-family:{FONT};font-size:10.5px;line-height:15px;color:{MUTED};">{e(d['footer_note'])}</div>
</td></tr>
</table>
</td></tr></table>
</body></html>"""


def text_version(d):
    out = [f"PETROBRAS OPPORTUNITY {d['number']}", d["tagline"], d["deadline_pill"], ""]
    if d.get("approval_url"): out += ["ADMIN APPROVAL REQUIRED – approve or reject: " + d["approval_url"], ""]
    out += [" | ".join(f"{l}: {v} ({s})" for l, v, s in d["facts"]), "", "EXECUTIVE SUMMARY", d["summary"], "", "HILONG VIEW", d["hilong_view"], "", "SCOPE"]
    out += [f"{r[0]}. {r[1]} | Qty {r[2]} | {r[3]}" for r in d["scope"]]
    out += ["", "KEY TECHNICAL REQUIREMENTS"]
    for b in d["requirements"]:
        out += [b["title"]] + [f"- {i}" for i in b["items"]]
    out += ["", "COMMERCIAL & QUALIFICATION"] + [f"- {i}" for i in d["commercial"]]
    out += ["", "ATTACHED TECHNICAL SPECIFICATIONS"] + [f"- {n} ({x})" for n, x in d["attachments"]]
    out += ["", d["package_note"], "", "Li Marcitão", "Market & Tender Intelligence · works for Li Kewei and Marcio Vianna · Hilong Brazil", d["footer_note"]]
    return "\n".join(out)


if __name__ == "__main__":
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    open(sys.argv[2], "w", encoding="utf-8").write(build(d))
    open(sys.argv[3], "w", encoding="utf-8").write(text_version(d))
    print("ok")
