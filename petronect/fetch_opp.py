"""Li Marcitão — baixa uma oportunidade da Petronect e separa as especificações técnicas.
Uso: python3 -I fetch_opp.py <numero> <pasta_saida>
Gera em <pasta_saida>: opp.json (registro da Petronect), raw/ (anexos originais), extracted/ (zips abertos),
specs/ (somente especificações técnicas a anexar), ppu/ (a planilha de preços, PPU, quando houver) e manifest.json
(resumo do que foi feito; "has_ppu" e "ppu" dizem se há PPU e quais arquivos foram separados)."""
import hashlib, json, os, re, subprocess, sys, zipfile, unicodedata

LIST_URL = "https://www.petronect.com.br/sap/opu/odata/SAP/YPCON_GET_XML_SRV/getXMLSet('01')?$format=json"
ATT_URL = "https://www.petronect.com.br/sap/opu/odata/SAP/YPCON_PUB_ATTACHMENT_DOWNLOAD_SRV/attachmentSet('{}')/$value"
SPEC = re.compile(r"((^|[^a-z0-9])et([^a-z]|$)|documentacao[ _-]tecnica|especifica|folha[ _-]?de[ _-]?dados|^fd[-_]|[^a-z]fd[-_]|data[ _-]?sheet|datasheet|desenho|drawing|"
                  r"memorial[ _-]descritivo|requisitos?[ _-]tecnicos?|anexo[ _-]tecnico|technical|spec|norma[ _-]tecnica|"
                  r"escopo|termo[ _-]de[ _-]referencia|lista[ _-]de[ _-]materiais|caracteristicas)", re.I)
NOT_SPEC = re.compile(r"(minuta|contrato|planilha[ _-]de[ _-]precos|ppu|proposta[ _-]comercial|declarac|modelo[ _-]de|"
                      r"instrumento[ _-]convocatorio|edital|condicoes[ _-]gerais|sms|seguranca|garantia|criterio|"
                      r"habilitac|anticorrup|integridade|cadastro|procuracao|\.xml$)", re.I)
PPU = re.compile(r"((^|[^a-z])ppu([^a-z]|$)|planilha[ _-]de[ _-]precos|planilha[ _-]de[ _-]precos[ _-]unitarios|planilha[ _-]de[ _-]quantidades)", re.I)
PPU_EXT = {".xls", ".xlsx", ".xlsm", ".xlsb", ".ods", ".csv", ".pdf"}
KEEP_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".dwg", ".dxf", ".jpg", ".png", ".tif", ".tiff"}


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def curl(url, out):
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "-o", out, "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    return r.stdout.strip()


def safe(name):
    return re.sub(r'[\\/:*?"<>|]+', "_", name).strip() or "file"


def main(num, out):
    os.makedirs(out, exist_ok=True)
    for d in ("raw", "extracted", "specs", "ppu"):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    lst = os.path.join(out, "_list.json")
    code = curl(LIST_URL, lst)
    if code != "200":
        sys.exit(f"ERRO: lista Petronect respondeu {code}")
    tab = json.loads(json.load(open(lst, encoding="utf-8"))["d"]["EvXml"])["TAB"]
    opp = next((o for o in tab if str(o.get("OPPORT_NUM")) == str(num)), None)
    man = {"num": num, "found": bool(opp), "attachments": [], "specs": [], "generated_spec": None}
    if not opp:
        json.dump(man, open(os.path.join(out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
        print(json.dumps(man, ensure_ascii=False))
        sys.exit(2)  # saiu da lista: encerrada ou cancelada
    json.dump(opp, open(os.path.join(out, "opp.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    man.update(end_date=opp.get("END_DATE"), end_hour=opp.get("END_HOUR"), title=opp.get("DESC_OBJ_CONTRAT"))

    for a in opp.get("ANEXOS") or []:
        name = safe(a.get("DESCRIPTION") or a.get("PHIO_OBJID"))
        dst = os.path.join(out, "raw", name)
        code = curl(ATT_URL.format(a["PHIO_OBJID"]), dst)
        ok = code == "200" and os.path.getsize(dst) > 0
        man["attachments"].append({"name": name, "http": code, "bytes": os.path.getsize(dst) if os.path.exists(dst) else 0})
        if not ok:
            continue
        if name.lower().endswith(".zip") and zipfile.is_zipfile(dst):
            zdir = os.path.join(out, "extracted", os.path.splitext(name)[0])
            with zipfile.ZipFile(dst) as z:
                for m in z.infolist():
                    if m.is_dir():
                        continue
                    fn = m.filename
                    if not (m.flag_bits & 0x800):  # nomes em CP437 dentro de zips do Windows
                        try:
                            raw = fn.encode("cp437")
                        except UnicodeEncodeError:
                            raw = None  # nome já decodificado (campo Unicode do zip): usar como está
                        if raw is not None:
                            try:
                                fn = raw.decode("utf-8")
                            except UnicodeDecodeError:
                                fn = raw.decode("cp850", "replace")
                    parts = [safe(p) for p in fn.split("/") if p not in ("", ".", "..")]
                    if not parts:
                        continue
                    tgt = os.path.join(zdir, *parts)
                    os.makedirs(os.path.dirname(tgt), exist_ok=True)
                    with z.open(m) as src, open(tgt, "wb") as f:
                        f.write(src.read())

    # candidatos: arquivos soltos + extraídos; nested zips também são abertos uma vez
    cands = []
    for root, _, files in os.walk(out):
        if os.path.basename(root) in ("specs", "ppu") or "/specs" in root or "/ppu" in root:
            continue
        for f in files:
            p = os.path.join(root, f)
            if p.endswith(("_list.json", "opp.json", "manifest.json")):
                continue
            cands.append(p)
    seen = set()
    for p in sorted(cands):
        rel = norm(os.path.relpath(p, out))
        ext = os.path.splitext(p)[1].lower()
        if ext not in KEEP_EXT:
            continue
        if SPEC.search(rel) and not NOT_SPEC.search(os.path.basename(rel)):
            key = None
            if ext == ".pdf":  # mesmo documento repetido para itens diferentes: anexa uma vez
                t = subprocess.run(["pdftotext", p, "-"], capture_output=True).stdout
                key = hashlib.sha256(t).hexdigest() if t.strip() else None
            if key is None:
                key = hashlib.sha256(open(p, "rb").read()).hexdigest()
            if key in seen:
                man.setdefault("duplicates", []).append(os.path.relpath(p, out)); continue
            seen.add(key)
            dst = os.path.join(out, "specs", safe(os.path.basename(p)))
            i = 1
            while os.path.exists(dst):
                b, e = os.path.splitext(safe(os.path.basename(p)))
                dst = os.path.join(out, "specs", f"{b} ({i}){e}"); i += 1
            with open(p, "rb") as s, open(dst, "wb") as d:
                d.write(s.read())
            man["specs"].append({"file": os.path.basename(dst), "from": os.path.relpath(p, out), "bytes": os.path.getsize(dst)})

    # PPU: planilha de preços. Prefere a que vem solta nos anexos; usa a de dentro de um zip só se não houver solta.
    ppus = [p for p in sorted(cands) if os.path.splitext(p)[1].lower() in PPU_EXT and PPU.search(norm(os.path.basename(p)))]
    top = [p for p in ppus if os.path.relpath(p, out).startswith("raw" + os.sep)]
    pick, seen_ppu = [], set()
    for p in (top or ppus):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h in seen_ppu:
            continue
        seen_ppu.add(h); pick.append(p)
    pick = sorted(pick, key=lambda p: (not p.lower().endswith((".xlsx", ".xls", ".xlsm")), p))[:2]
    man["ppu"] = []
    for p in pick:
        dst = os.path.join(out, "ppu", safe(os.path.basename(p)))
        with open(p, "rb") as s_, open(dst, "wb") as d_:
            d_.write(s_.read())
        man["ppu"].append({"file": os.path.basename(dst), "from": os.path.relpath(p, out), "bytes": os.path.getsize(dst)})
    man["has_ppu"] = bool(man["ppu"])

    man["all_files"] = sorted(os.path.relpath(p, out) for p in cands)
    json.dump(man, open(os.path.join(out, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: man[k] for k in ("num", "found", "title", "end_date", "end_hour", "attachments", "specs", "has_ppu", "ppu")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
