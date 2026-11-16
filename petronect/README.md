# Li Marcitão — oportunidades Petronect

Scripts usados pelas tarefas agendadas do Li Marcitão (não fazem parte do site do Market Report).

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
