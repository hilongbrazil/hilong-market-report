# Li Marcitao — oportunidades Petronect

Scripts usados pelas tarefas agendadas do Li Marcitao (não fazem parte do site do Market Report).

- `fetch_opp.py <numero> <pasta>` — baixa a oportunidade da Petronect (lista pública `getXMLSet('01')`), todos os anexos, abre os .zip e copia para `<pasta>/specs/` só as especificações técnicas (sem duplicatas). Sai com código 2 se a oportunidade não está mais na lista.
- `build_email.py data.json out.html out.txt` — e-mail final da oportunidade, sempre em inglês, no template Hilong (Figma jtgMaB26vle6i51mMs7JHP).
- `build_digest.py data.json out.html out.txt` — e-mail-resumo diário de aprovação (português).
- `build_map.py map.json mapa.png` — mapa do Brasil com os locais de entrega numerados e a legenda com nome resumido (usa `br_states.json`). Não é mais usado no e-mail (o mapa fica na aba Mapa do Centro); o dicionário PLACES continua sendo a referência de coordenadas.
- `s3post.py upload.json` — envia um arquivo ao armazenamento do Resend (`create-file-upload`); upload.json = {"url","file","fields"}.

- `lm_db.py fila|salvar` — lê e grava a fila de oportunidades no Centro de Operações público (Supabase Hilong Operation, funções `hl_lm_fila` e `hl_lm_salvar`, ver `supabase/05_li_marcitao.sql` no repositório hilong-center). Precisa da variável `LM_KEY`.

Fila de aprovação, pipeline e mapa: hilong.hilongbrazil.com → Corporate and Strategic (abas Aprovação Petronect e Mapa). Aprovação direta: https://hilong.hilongbrazil.com/#aprovacao

## Aprovação por resposta de e-mail (16/11/2026)

- O e-mail-resumo numera as oportunidades (`n` = 1, 2, 3… em cada item de `opps`, na ordem do prazo) e sai com `replyTo` = `hilongbrazil@gmail.com`.
- A varredura grava em cada oportunidade `ref_resumo` = `"AAAA-MM-DD#n"` (data do resumo e número no resumo).
- O Marcio responde, por exemplo, "aprovo 1 e 3, recuso 2", "aprovo todas" ou "ok, de acordo" (= aprovar todas daquele resumo). Também vale o número Petronect.
- A tarefa de hora em hora lê no Gmail hilongbrazil as respostas novas (só de `marcio.vianna@hilonggroup.com`, assunto com "Petronect"), registra cada decisão com `lm_db.py decidir <num> aprovar|recusar`, marca a conversa com o marcador `LM-processado` e confirma por e-mail o que aplicou. Resposta ambígua não é aplicada: ele recebe um aviso.
- `decidir` só muda oportunidades pendentes. A aprovação pelo Centro continua valendo; o Centro mostra "por resposta de e-mail" nas decididas assim.
- Banco: `supabase/07_aprovacao_email.sql` (repositório hilong-center): `hl_lm_decidir`, colunas `ref_resumo` e `decidido_via`.

## Classificação, PPU e lista da China (19/11/2026)

- Cada oportunidade selecionada leva `tipo` (servico|produto|ambos), `ambiente` (onshore|offshore|ambos) e `tem_ppu` / `ppu_arquivos`.
- `python3 -I ppu_check.py lista.json <num> [<num> ...]` → `{num: {tem_ppu, arquivos}}`: confere os nomes dos anexos e, se preciso, o conteúdo dos zips. `fetch_opp.py` separa a PPU em `ppu/` (`manifest.json`: `has_ppu`, `ppu`).
- Regra da Petrobras: com PPU, a PPU é obrigatória na proposta; sem PPU, o preço vai direto no sistema Petronect. `build_email.py` escreve essa frase a partir de `ppu` (true/false).
- `build_email.py`: e-mail final em inglês e, se houver o objeto `zh`, em chinês no mesmo e-mail; campos comuns `tipo`, `ambiente`, `ppu`.
- `build_digest.py`: o resumo do Marcio mostra tipo, ambiente e PPU (`tipo`, `ambiente`, `ppu` em cada opp).
- Lista da China: `lm_db.py links pedidos.json` cria os tokens dos botões (`[{num, email, pessoa, acao}]`; `email` `"*"` = botão geral, registrado como "China"); `python3 build_china.py china.json email.html email.txt lista.xlsx` monta o e-mail (imprime o assunto) e o Excel. Página dos botões: https://hilongbrazil.com/interesse/?t=<token> (pede confirmação; não pede nome).
- Cliques: `lm_db.py interesses` (ainda não avisados) e `lm_db.py avisados <id> ...`. Só cliques "interesse" da China geram aviso (Marcio e Li Kewei); "sem_interesse" não avisa, só tira a oportunidade da lista.
- Banco: `supabase/08_classificacao_china.sql` (hilong-center).

## Cadeia e times (desde 24/11/2026)

- Cada oportunidade tem `cadeia`: `upstream` (até a cabeça do poço e a plataforma, com submarino, sísmica, embarcações de apoio e facilities de produção), `midstream` (dutos e integridade, processamento de gás, compressão, terminais, píeres e tancagem) ou `downstream` (refino, termelétricas, fertilizantes, catalisadores e químicos de processo). Na dúvida, vale onde o serviço é executado ou o material é entregue.
- A lista diária é dividida primeiro por tipo: **Serviços → Marketing** (chenjuqing, tandunxiang) e **Produtos → Trade** (songguangqiang, lilianwei, zhuzhiming, wangbeichen), sempre com Marcio Vianna e Li Kewei em cópia. Serviço + produto vai nas duas. Dentro de cada lista: Upstream, Midstream, Downstream.
- `build_china.py` recebe `"team": "marketing" | "trade"` e `cadeia` em cada item. Os botões usam links com `email` = `marketing` ou `trade`.
- "Interested": a tarefa de hora em hora envia ao time os documentos técnicos e a PPU (`build_email.py`) e grava `docs_mkt_em` / `docs_trade_em`. "Not interested": sai da lista daquele time (`descartada_mkt` / `descartada_trade`).
- A aprovação do Marcio no Centro continua valendo só para o pipeline.
