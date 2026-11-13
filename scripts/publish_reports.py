#!/usr/bin/env python3
"""Guarda os PDFs do dia em reports/AAAA-MM-DD/ (para o Resend buscar e anexar) e apaga os dias antigos.

Uso:
  python3 scripts/publish_reports.py --date AAAA-MM-DD arquivo1.pdf [arquivo2.pdf ...] [--keep 3]

- Copia cada PDF para reports/<data>/<nome do arquivo>.
- Mantém só as pastas dos últimos --keep dias (padrão: 3) e apaga as mais antigas.
- Imprime o endereço público de cada PDF (site no Netlify), para usar como anexo por URL.
Depois: git add -A reports && commit && push; esperar a publicação no Netlify antes de enviar o e-mail.
"""
import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports"
SITE = "https://marketreportnews.netlify.app"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--keep", type=int, default=3)
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    day = dt.date.fromisoformat(a.date)
    dest = BASE / day.isoformat()
    dest.mkdir(parents=True, exist_ok=True)
    for f in a.files:
        src = Path(f)
        if src.suffix.lower() != ".pdf" or not src.is_file():
            sys.exit(f"não é um PDF: {f}")
        shutil.copyfile(src, dest / src.name)
        print(f"URL: {SITE}/reports/{day.isoformat()}/{src.name}")
    oldest = day - dt.timedelta(days=a.keep - 1)
    for d in sorted(BASE.iterdir()):
        try:
            when = dt.date.fromisoformat(d.name)
        except ValueError:
            continue
        if d.is_dir() and when < oldest:
            shutil.rmtree(d)
            print(f"removido: reports/{d.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
