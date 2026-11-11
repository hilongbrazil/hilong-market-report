#!/usr/bin/env python3
"""Valida data/news.json antes de cada commit. Uso: python3 scripts/validate.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGIONS = {"BR", "SA"}
COUNTRIES = {"BR", "AR", "CO", "GY", "SR", "PE", "EC", "BO", "VE", "CL", "UY", "PY", "TT"}
CATEGORIES = {
    "resultados", "producao", "perfuracao", "investimentos", "contratos",
    "regulatorio", "exploracao", "mercado", "fusoes", "outros",
}
VIA = {"site", "linkedin", "x", "youtube"}
REQUIRED = [
    "id", "date", "region", "country", "operator", "category",
    "title_pt", "title_en", "summary_pt", "summary_en", "source", "url", "via",
]
MAX_SUMMARY = 320


def main() -> int:
    path = ROOT / "data" / "news.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERRO: news.json inválido: {exc}")
        return 1

    errors = []
    if not isinstance(data.get("updated_at"), str):
        errors.append("updated_at ausente")
    items = data.get("items")
    if not isinstance(items, list):
        print("ERRO: 'items' deve ser uma lista")
        return 1

    ids, urls = set(), set()
    for i, it in enumerate(items):
        tag = f"item {i} ({it.get('id', '?')})"
        for key in REQUIRED:
            if not isinstance(it.get(key), str) or not it[key].strip():
                errors.append(f"{tag}: campo '{key}' vazio ou ausente")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", it.get("date", "")):
            errors.append(f"{tag}: data fora do formato AAAA-MM-DD")
        if it.get("region") not in REGIONS:
            errors.append(f"{tag}: region deve ser BR ou SA")
        if it.get("country") not in COUNTRIES:
            errors.append(f"{tag}: country desconhecido")
        if (it.get("region") == "BR") != (it.get("country") == "BR"):
            errors.append(f"{tag}: region e country não combinam")
        if it.get("category") not in CATEGORIES:
            errors.append(f"{tag}: category desconhecida")
        if it.get("via") not in VIA:
            errors.append(f"{tag}: via deve ser site, linkedin, x ou youtube")
        if not re.match(r"^https?://", it.get("url", "")):
            errors.append(f"{tag}: url deve começar com http(s)://")
        for key in ("summary_pt", "summary_en"):
            if len(it.get(key, "")) > MAX_SUMMARY:
                errors.append(f"{tag}: {key} passa de {MAX_SUMMARY} caracteres")
        if it.get("id") in ids:
            errors.append(f"{tag}: id duplicado")
        if it.get("url") in urls:
            errors.append(f"{tag}: url duplicada")
        ids.add(it.get("id"))
        urls.add(it.get("url"))

    if errors:
        print("ERROS:")
        for e in errors:
            print(" -", e)
        return 1
    br = sum(1 for it in items if it["region"] == "BR")
    print(f"OK: {len(items)} notícias ({br} Brasil, {len(items) - br} América do Sul)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
