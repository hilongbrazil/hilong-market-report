"""Li Marcitão — acesso ao banco do Centro de Operações (Supabase Hilong Operation) pelas funções do agente.
Uso:
  LM_KEY=<chave> python3 lm_db.py fila                 -> imprime a fila (JSON) de hl_bd_oportunidades
  LM_KEY=<chave> python3 lm_db.py salvar dados.json    -> grava/atualiza uma oportunidade (ou uma lista delas)
Campos aceitos em salvar: num (obrigatório), objeto (obrigatório se for nova), cliente, resumo (nome curto em inglês),
linha, sumario, visao, aderencia (alta|média), prazo ("DD/MM/AAAA HH:MM"), end_date (AAAA-MM-DD), end_hour,
locais ([{"nome","uf","lat","lon"}]), email_enviado, email_enviado_em, resend_id, drive_url, encerrada,
mudanca_prazo ({"from","to","detected_at"}), obs_pipeline (observação no pipeline do Corporate and Strategic).
O status (pending/approved/rejected) só muda pelo Centro."""
import json, os, subprocess, sys

URL = "https://wmekochxazvxcghykcgg.supabase.co/rest/v1/rpc/"
ANON = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndtZWtvY2h4YXp2eGNnaHlrY2dnIiwicm9sZSI6ImFub24iLCJp"
        "YXQiOjE3ODgwNDI4MzUsImV4cCI6MjEwMzYxODgzNX0.jtbf1YjazW25IYOZZyvT3zfuCprMHMZyJ8HE_Ges_H8")   # chave pública (a mesma do site)


def call(fn, body):
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-w", "\n%{http_code}", "-X", "POST", URL + fn,
                        "-H", "apikey: " + ANON, "-H", "Authorization: Bearer " + ANON,
                        "-H", "Content-Type: application/json", "--data-binary", "@-"],
                       input=json.dumps(body), capture_output=True, text=True)
    out, _, code = r.stdout.rpartition("\n")
    if r.returncode or not code.startswith("2"):
        sys.exit(f"ERRO {fn}: HTTP {code or r.returncode} {out[:300]} {r.stderr[:200]}")
    return json.loads(out) if out.strip() else None


def main():
    key = os.environ.get("LM_KEY")
    if not key:
        sys.exit("ERRO: defina LM_KEY")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fila":
        print(json.dumps(call("hl_lm_fila", {"p_chave": key}), ensure_ascii=False, indent=1))
    elif cmd == "salvar":
        data = json.load(open(sys.argv[2], encoding="utf-8"))
        for item in (data if isinstance(data, list) else [data]):
            print("ok", call("hl_lm_salvar", {"p_chave": key, "p": item}))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
