# Li Marcitão — oportunidades Petronect

Scripts usados pelas tarefas agendadas do Li Marcitão (não fazem parte do site do Market Report).

- `fetch_opp.py <numero> <pasta>` — baixa a oportunidade da Petronect (lista pública `getXMLSet('01')`), todos os anexos, abre os .zip e copia para `<pasta>/specs/` só as especificações técnicas (sem duplicatas). Sai com código 2 se a oportunidade não está mais na lista.
- `build_email.py data.json out.html out.txt` — e-mail final da oportunidade, sempre em inglês, no template Hilong (Figma jtgMaB26vle6i51mMs7JHP).
- `build_digest.py data.json out.html out.txt` — e-mail-resumo diário de aprovação (português).
- `build_map.py map.json mapa.png` — mapa do Brasil com os locais de entrega numerados e a legenda com nome resumido (usa `br_states.json`). Publicado em `reports/petronect/AAAA-MM-DD/mapa.png` (pasta aberta no Netlify) e usado no resumo diário (`map_url`). Mapas com mais de 7 dias são apagados.
- `s3post.py upload.json` — envia um arquivo ao armazenamento do Resend (`create-file-upload`); upload.json = {"url","file","fields"}.

Fila de aprovação e pipeline: banco do artefato "Centro de Operações Integradas" (slug aef33fcc-3e8b-44ec-bbb7-f8c756a03b1b), coleções `approvals` e `pipeline`.
