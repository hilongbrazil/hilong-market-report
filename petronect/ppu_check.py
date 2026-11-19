"""Li Marcitao — diz se cada oportunidade tem PPU (planilha de preços) nos anexos, sem baixar o pacote inteiro.
Uso: python3 -I ppu_check.py <lista.json da Petronect> <numero> [<numero> ...]
Olha os nomes dos anexos; quando não acha PPU e há .zip, baixa só os .zip e lê os nomes de dentro.
Imprime um JSON {numero: {"tem_ppu": true/false, "arquivos": [...]}}."""
import io, json, os, re, subprocess, sys, tempfile, unicodedata, zipfile

ATT_URL = "https://www.petronect.com.br/sap/opu/odata/SAP/YPCON_PUB_ATTACHMENT_DOWNLOAD_SRV/attachmentSet('{}')/$value"
PPU = re.compile(r"((^|[^a-z])ppu([^a-z]|$)|planilha[ _-]de[ _-]precos|planilha[ _-]de[ _-]quantidades)", re.I)
EXT = (".xls", ".xlsx", ".xlsm", ".xlsb", ".ods", ".csv", ".pdf")


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def zip_names(objid):
    with tempfile.NamedTemporaryFile(suffix=".zip") as f:
        r = subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "-o", f.name, "-w", "%{http_code}", ATT_URL.format(objid)],
                           capture_output=True, text=True)
        if r.stdout.strip() != "200" or not zipfile.is_zipfile(f.name):
            return []
        with zipfile.ZipFile(f.name) as z:
            return [n for n in z.namelist() if not n.endswith("/")]


def check(o):
    found = []
    zips = []
    for a in o.get("ANEXOS") or []:
        n = a.get("DESCRIPTION") or ""
        if norm(n).endswith(EXT) and PPU.search(norm(n)):
            found.append(n)
        elif norm(n).endswith(".zip"):
            zips.append(a)
    if not found:
        for a in zips:
            for n in zip_names(a["PHIO_OBJID"]):
                b = os.path.basename(n)
                if norm(b).endswith(EXT) and PPU.search(norm(b)):
                    found.append(f"{a.get('DESCRIPTION')} > {b}")
    return {"tem_ppu": bool(found), "arquivos": found}


if __name__ == "__main__":
    tab = json.loads(json.load(open(sys.argv[1], encoding="utf-8"))["d"]["EvXml"])["TAB"]
    by = {str(o["OPPORT_NUM"]): o for o in tab}
    print(json.dumps({n: (check(by[n]) if n in by else {"erro": "fora da lista"}) for n in sys.argv[2:]}, ensure_ascii=False, indent=1))
