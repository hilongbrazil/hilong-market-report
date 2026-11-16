"""E-mail-resumo diário de aprovação (PT) — Li Marcitão. Uso: python3 build_digest.py data.json out.html out.txt"""
import json, html, sys

NAVY, ORANGE, INK, MUTED, LINE, TILE, BG, AMBER = "#0B2545", "#E8711A", "#1F2A37", "#5A6B7F", "#E2E8F0", "#EEF2F7", "#F3F5F8", "#FFF4E8"
FONT = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
e = html.escape
FIT = {"alta": ("#E7F6EC", "#1E7B3C", "ADERÊNCIA ALTA"), "média": ("#FFF4E8", "#B45309", "ADERÊNCIA MÉDIA")}


def card(o):
    bg, fg, lbl = FIT.get(o["fit"], FIT["média"])
    return f'''<tr><td style="padding:0 0 12px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;">
<tr><td style="padding:14px 16px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td style="font-family:{FONT};font-size:11px;font-weight:700;letter-spacing:.6px;color:{MUTED};">{e(o["num"])} &nbsp;&middot;&nbsp; {e(o["line"])}</td>
    <td align="right"><span style="background:{bg};color:{fg};border-radius:12px;padding:3px 9px;font-family:{FONT};font-size:9.5px;font-weight:700;letter-spacing:.5px;">{lbl}</span></td>
  </tr></table>
  <div style="font-family:{FONT};font-size:15px;line-height:21px;font-weight:700;color:{NAVY};padding-top:6px;">{e(o["title"])}</div>
  <div style="font-family:{FONT};font-size:13px;line-height:20px;color:{INK};padding-top:6px;">{e(o["summary"])}</div>
  <div style="font-family:{FONT};font-size:12.5px;line-height:19px;color:{INK};padding-top:8px;"><span style="color:{ORANGE};font-weight:700;">Visão Hilong:</span> {e(o["view"])}</div>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:10px;"><tr>
    <td style="background:{TILE};border-radius:6px;padding:6px 10px;font-family:{FONT};font-size:11.5px;font-weight:600;color:{NAVY};">Prazo da proposta: {e(o["deadline"])}</td>
  </tr></table>
</td></tr></table></td></tr>'''


def build(d):
    cards = "".join(card(o) for o in d["opps"])
    url = e(d["approval_url"])
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{e(d['subject'])}</title></head>
<body style="margin:0;padding:0;background:{BG};">
<div style="display:none;max-height:0;overflow:hidden;">{e(d['preheader'])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border:1px solid {LINE};border-radius:10px;overflow:hidden;">
<tr><td style="background:{NAVY};padding:26px 32px;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
    <td width="22" height="22" align="center" style="background:{ORANGE};border-radius:6px;font-family:{FONT};font-size:13px;font-weight:800;color:#FFFFFF;">H</td>
    <td style="padding-left:8px;font-family:{FONT};font-size:10.5px;font-weight:600;letter-spacing:1px;color:#B8C9DE;">HILONG BRAZIL &nbsp;&middot;&nbsp; PETRONECT</td>
  </tr></table>
  <div style="font-family:{FONT};font-size:24px;line-height:30px;font-weight:700;color:#FFFFFF;padding-top:12px;">{e(d['headline'])}</div>
  <div style="font-family:{FONT};font-size:13.5px;line-height:20px;color:#D1DEED;padding-top:6px;">{e(d['tagline'])}</div>
</td></tr>
<tr><td style="background:{AMBER};border-bottom:1px solid #F6D9B8;padding:16px 32px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td valign="middle" style="font-family:{FONT};font-size:12.5px;line-height:18px;color:{INK};">Marque uma ou várias. As aprovadas entram no Corporate &amp; Strategic como <b>Nova</b> e recebem o e-mail completo em inglês.</td>
    <td align="right" valign="middle" style="padding-left:12px;white-space:nowrap;"><a href="{url}" style="display:inline-block;background:{NAVY};color:#FFFFFF;text-decoration:none;font-family:{FONT};font-size:12px;font-weight:700;padding:11px 18px;border-radius:6px;">Aprovar ou recusar &rarr;</a></td>
  </tr></table>
</td></tr>
<tr><td style="padding:22px 32px 12px 32px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{cards}</table></td></tr>
<tr><td style="padding:0 32px 24px 32px;font-family:{FONT};font-size:11.5px;line-height:17px;color:{MUTED};">{e(d['note'])}</td></tr>
<tr><td style="background:{BG};padding:20px 32px;">
  <div style="font-family:{FONT};font-size:14px;font-weight:700;color:{NAVY};">Li Marcit&atilde;o</div>
  <div style="font-family:{FONT};font-size:11.5px;line-height:16px;color:{MUTED};padding-top:4px;">Inteligência de mercado e licitações &middot; trabalha para Li Kewei e Marcio Vianna &middot; Hilong Brazil</div>
</td></tr>
</table></td></tr></table></body></html>"""


def text(d):
    out = [d["headline"], d["tagline"], "", "Aprovar ou recusar: " + d["approval_url"], ""]
    for o in d["opps"]:
        out += [f'{o["num"]} · {o["line"]} · aderência {o["fit"]}', o["title"], o["summary"],
                "Visão Hilong: " + o["view"], "Prazo da proposta: " + o["deadline"], ""]
    out += [d["note"], "", "Li Marcitão — Hilong Brazil"]
    return "\n".join(out)


if __name__ == "__main__":
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    open(sys.argv[2], "w", encoding="utf-8").write(build(d))
    open(sys.argv[3], "w", encoding="utf-8").write(text(d))
