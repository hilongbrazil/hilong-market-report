# Hilong Market Report

Site estático publicado em https://marketreportnews.hilongbrazil.com (Netlify, deploy automático a cada push na branch `main`).

- `index.html`: página de notícias. `live.html`: painel ao vivo (indicadores e atividade do agente).
- `assets/site.css` e `assets/site.js`: estilo e código das duas páginas.
- `data/news.json`: as notícias.
- `data/run.json`: registro da última varredura (alimenta o painel ao vivo).
- `data/reports.json`: registro das edições do relatório em PDF (quais notícias saíram em cada uma). Gravado pelo `scripts/build_pdf.py --record`.
- A rotina diária altera somente `data/news.json`, `data/run.json`, `data/reports.json` e `data/archive/`.
- `data/archive/AAAA-MM.json`: notícias com mais de 60 dias, movidas para cá.
- `scripts/validate.py`: valida o `news.json` e o `run.json`. Rodar antes de todo commit.
- `scripts/build_pdf.py`: gera o relatório completo em PDF e o corpo do e-mail diário, sempre em inglês (seção 6).

## Rotina diária de atualização

Três tarefas agendadas, todos os dias (horário de Brasília). Nada roda das 22h às 6h.

- **6h00, varredura completa:** seções 1 a 5 (pesquisar, selecionar, escrever, gravar e publicar) e o resumo da seção 7, passando por todas as empresas da lista. Não gera PDF nem envia e-mail.
- **De hora em hora, das 7h às 21h, rodada rápida:** seção 1b, depois as seções 2 a 5. Não gera PDF nem envia e-mail. (Em teste na semana de 12/11/2026.)
- **7h55, relatório:** só a seção 6 (PDF e e-mail), para o e-mail chegar por volta das 8h. Usa o que as varreduras publicaram até ali.

Cada varredura (a completa e cada rodada) regrava o `data/run.json`; o painel ao vivo mostra sempre a última que terminou.

Objetivo: registrar as principais notícias do mercado de óleo e gás no Brasil e na América do Sul publicadas desde a última atualização (`updated_at`), com foco no que interessa a uma empresa de serviços e equipamentos de petróleo (sondas de perfuração e workover, OCTG, hastes de bombeio, ferramentas de fundo de poço).

**Prioridade: o mercado brasileiro vem sempre primeiro.** Pesquisar todas as empresas da lista prioritária abaixo, na ordem em que aparecem (onshore, depois offshore, depois fornecedores), antes de passar para a América do Sul.

### 1. Pesquisar

Usar WebSearch (e WebFetch para confirmar data, números e se o link abre). Fazer uma busca separada por empresa; uma busca genérica não cobre tudo. Cada execução passa pelos canais: sites, LinkedIn, Instagram, YouTube e X.

**Lista prioritária (Brasil)**

Usar nos itens (`operator`) exatamente os nomes desta lista.

Onshore:
1. Carmo Energy
2. PetroReconcavo
3. Brava Energia (inclui os ativos da antiga Enauta: Atlanta e Papa-Terra)
4. Origem Energia
5. Mandacaru Energia
6. Seacrest Petróleo
7. PetroVictory
8. Alvopetro
9. Petroborn
10. Eneva
11. Vipetro

Offshore:
12. Petrobras
13. Equinor
14. Perenco
15. PRIO
16. TotalEnergies
17. Transpetro

Regulador:
18. ANP (leilões, oferta permanente, regulação, boletins de produção)

Fornecedores:
19. SLB
20. Baker Hughes
21. Weatherford
22. Tenaris
23. Expro
24. Confab (Tenaris Confab)
25. Apolo Tubulars
26. Jereh
27. Kerui
28. Inpasa
29. TAG (Transportadora Associada de Gás)

**Sites oficiais: visita obrigatória todo dia.** A varredura das 6h abre, uma a uma, as páginas abaixo (WebFetch) e confere os itens publicados desde a última atualização. Toda notícia nova que passar nos critérios entra, com o link da própria página da empresa (`via` = `site`, `source` = nome da empresa). Quando a página não abre ou não mostra itens, fazer a busca indicada na coluna "Se falhar". Registrar cada visita no `run.json` (campo `sites`, seção 5).

| # | Empresa | Página a abrir | Se falhar ou observação |
|---|---|---|---|
| 1 | Carmo Energy | https://carmoenergy.com/noticias/ | Datas em português; links relativos (carmoenergy.com/noticias/<slug>) |
| 2 | PetroReconcavo | https://ri.petroreconcavo.com.br/ | Não abriu na checagem de 12/11/2026. Buscar "PetroReconcavo fato relevante" e "PetroReconcavo comunicado ao mercado" |
| 3 | Brava Energia | https://bravaenergia.com/noticias/ | Usar a página em português (a em inglês está desatualizada). Fatos relevantes: buscar "Brava Energia fato relevante" (a página de RI só carrega com JavaScript) |
| 4 | Origem Energia | https://www.origemenergia.com/en/press/news/ | Datas no formato MM/DD |
| 5 | Mandacaru Energia | https://mandacaruenergia.com.br/noticias/ | A lista não mostra datas: conferir a data na página da matéria |
| 6 | Seacrest Petróleo | https://seacrestpetroleo.com/news/ | Empresa em liquidação; publica pouco |
| 7 | PetroVictory | https://www.petrovictoryenergy.com/press-releases/ | Reserva: https://www.prnewswire.com/news/petro__victory-energy-corp./ |
| 8 | Alvopetro | https://alvopetro.com/News-Releases | |
| 9 | Petroborn | https://petroborn.com.br/ | O site bloqueia leitura automática. Buscar "Petroborn" |
| 10 | Eneva | https://ri.eneva.com.br/en/information-to-the-market/material-facts-and-notices-to-the-market/ | A lista só carrega com JavaScript. Buscar "Eneva fato relevante" e "Eneva comunicado" |
| 11 | Vipetro | sem site | Buscar "Vipetro" (ANP e imprensa do Espírito Santo) |
| 12 | Petrobras | https://agencia.petrobras.com.br/mais-recentes | |
| 13 | Equinor | https://www.equinor.com.br/noticias | Mostra poucos itens; conferir também https://www.equinor.com/news |
| 14 | Perenco | https://www.perenco.com/news/ | Itens em PDF, com data só dentro do PDF; poucos sobre o Brasil |
| 15 | PRIO | https://ri.prio3.com.br/servicos-aos-investidores/comunicados-e-fatos-relevantes/ | A lista só carrega com JavaScript. Buscar "PRIO fato relevante" e "PRIO comunicado" |
| 16 | TotalEnergies | https://totalenergies.com/brazil | Também https://totalenergies.com.br/imprensa (institucional) |
| 17 | Transpetro | https://transpetro.com.br/en_us/transpetro-institucional/noticias/ | Datas no formato M/D/AA |
| 18 | ANP | https://www.gov.br/anp/pt-br/canais_atendimento/imprensa/noticias-comunicados | |
| 19 | SLB | https://investorcenter.slb.com/news-events/news-releases | Comunicados globais: filtrar o que for do Brasil e da América do Sul |
| 20 | Baker Hughes | https://www.bakerhughes.com/company/newsroom | A página de investidores só mostra "Loading" |
| 21 | Weatherford | https://weatherford.gcs-web.com/news-releases | A página em weatherford.com está desatualizada |
| 22 | Tenaris | https://ir.tenaris.com/press-releases | Notícias comerciais (contratos no Brasil): buscar "Tenaris Brasil" |
| 23 | Expro | https://investors.expro.com/news/Press-Releases/default.aspx | A lista só carrega com JavaScript. Buscar "Expro Brazil" e "Expro press release" |
| 24 | Confab | sem página própria | Sai nas páginas da Tenaris; buscar "Tenaris Confab" |
| 25 | Apolo Tubulars | sem site encontrado | Buscar "Apolo Tubulars" e "Dexxos Apolo" |
| 26 | Jereh | https://www.jereh.com/en/news/press-release | A lista não carrega na leitura automática. Buscar "Jereh Group news" |
| 27 | Kerui | https://www.keruigroup.com/en/h-col-114.html | |
| 28 | Inpasa | https://www.inpasa.com.br/ | Sem página de notícias encontrada. Buscar "Inpasa" |
| 29 | TAG | sem site confirmado | Buscar "TAG Transportadora Associada de Gás" |

Se uma página mudar de endereço ou passar a abrir (ou a falhar) de forma estável, avisar no resumo final; não alterar esta tabela durante a rotina.

**Complementos no Brasil:** Shell, onshore do Nordeste (Sergipe, Bahia, Rio Grande do Norte, Alagoas) e contratos de sondas terrestres de perfuração e workover (Braserv, San Antonio Internacional e outras).

**América do Sul (depois do Brasil):** Argentina (YPF, Vista, Pan American Energy, Pluspetrol, Vaca Muerta), Colômbia (Ecopetrol), Guiana e Suriname (ExxonMobil, Staatsolie, TotalEnergies), Peru (Petroperú, Perupetro), Equador (Petroecuador), Bolívia (YPFB), Venezuela (PDVSA) e demais países quando houver fato relevante. Incluir também os fornecedores da lista quando a notícia for sobre a região.

**Sites de referência:** eixos, Brasil Energia / PetróleoHoje, TN Petróleo, PetroNotícias, Agência Petrobras, sites de RI das companhias, Reuters, BNamericas, OilNOW, Ámbito, Rigzone, Offshore Engineer.

**LinkedIn, Instagram e X:** para cada empresa da lista prioritária, buscar as publicações recentes do perfil oficial (por exemplo, "Carmo Energy LinkedIn", "PetroReconcavo Instagram"). Incluir somente publicação oficial da empresa, com data visível e link público que abre sem login. Marcar `via` como `linkedin`, `instagram` ou `x` e `source` com o nome da empresa. Não tentar fazer login nem contornar bloqueios. Se houver um conector de dados de redes sociais disponível na sessão, usar o conector.

**YouTube:** buscar vídeos publicados desde a última atualização nos canais oficiais das empresas e dos veículos do setor (webcasts de resultados, anúncios de projetos, entrevistas de executivos). Registrar apenas o que o título e a descrição do vídeo afirmam; não atribuir ao vídeo nada que não esteja escrito na página. Marcar `via` como `youtube` e `source` com o nome do canal.

### 1b. Rodada rápida (de hora em hora, das 7h às 21h)

Uma rodada curta, de no máximo 12 buscas, só para pegar o que saiu desde as últimas horas:

1. Sempre: as notícias mais recentes de eixos, PetroNotícias, Agência Petrobras e Click Petróleo e Gás (canal `site`).
2. Um bloco da lista prioritária, conforme a hora da rodada (resto da divisão da hora por 3):
   - resto 0 (9h, 12h, 15h, 18h, 21h): onshore, empresas 1 a 11;
   - resto 1 (7h, 10h, 13h, 16h, 19h): offshore, empresas 12 a 17, e ANP (18);
   - resto 2 (8h, 11h, 14h, 17h, 20h): fornecedores, empresas 19 a 29, e uma busca da América do Sul.
   Agrupar empresas na mesma busca quando fizer sentido, para caber nas 12 buscas.
3. Procurar notícias das últimas 48 horas que ainda não estejam em `news.json` (conferir `url` e assunto). Os critérios de seleção, relevância e escrita são os mesmos das seções 2 a 4.
4. Gravar como na seção 5, com estas diferenças: `terms` pode ter menos de 15 nomes (só o que a rodada pesquisou); se nada novo entrar, não alterar `news.json` e regravar só o `run.json` (com `new_items` 0), para o painel mostrar a rodada; mensagem do commit `Rodada AAAA-MM-DD HHh (N novas)`.

### 2. Selecionar

- Prioridade de assunto: perfuração e sondas, campanhas de workover, contratos e licitações, produção, investimentos (capex), descobertas, leilões, fusões e aquisições, resultados trimestrais, mudanças regulatórias.
- Deixar de fora: recomendações de ações, opinião sem fato novo, política sem efeito direto no setor, conteúdo patrocinado.
- Só entra notícia com data de publicação confirmada e link que abre. Na dúvida sobre a data ou sobre um número, não incluir.
- O link precisa abrir a matéria para qualquer leitor, sem login. Conferir cada link com WebFetch antes de gravar. Se a fonte for fechada para assinantes (por exemplo, Brasil Energia), procurar outra fonte aberta para o mesmo fato; só usar a fonte fechada quando não houver alternativa e, nesse caso, incluir `"access": "paywall"` no item.
- Não repetir: conferir `url` e assunto contra o que já está em `news.json`.
- Meta: de 5 a 15 notícias novas por dia, com maioria do Brasil. Se não houver nada relevante, não inventar: registrar zero.

### 3. Avaliar a relevância

Cada notícia recebe uma nota `relevance` de 1 a 5. A página e o e-mail mostram os destaques nessa ordem (nota maior primeiro; em caso de empate, Brasil antes da América do Sul e a mais recente antes).

- **5:** interesse direto da Hilong no Brasil: contratos, licitações ou campanhas de sondas terrestres de perfuração e workover; compras de OCTG, hastes de bombeio ou ferramentas de poço; operações, aquisições ou planos de poços das operadoras onshore da lista prioritária.
- **4:** produção, perfuração, investimentos ou intervenções em poços das operadoras da lista prioritária no Brasil (onshore ou offshore); movimentos dos fornecedores da lista no Brasil.
- **3:** resultados trimestrais e projeções das operadoras da lista; leilões e regulação da ANP; demais fatos relevantes do setor no Brasil.
- **2:** perfuração, investimentos e contratos na América do Sul.
- **1:** mercado em geral, preços, notícias corporativas da América do Sul sem efeito operacional.

### 4. Escrever

Cada item segue este formato:

```json
{
  "id": "AAAA-MM-DD-slug-curto",
  "date": "AAAA-MM-DD",
  "region": "BR ou SA",
  "country": "BR, AR, CO, GY, SR, PE, EC, BO, VE, CL, UY, PY ou TT",
  "operator": "Nome da empresa, ou Setor quando for geral",
  "category": "resultados | producao | perfuracao | investimentos | contratos | regulatorio | exploracao | mercado | fusoes | outros",
  "environment": "onshore | offshore | geral",
  "relevance": 4,
  "title_pt": "...", "title_en": "...",
  "summary_pt": "...", "summary_en": "...",
  "source": "Nome do veículo",
  "url": "https://...",
  "via": "site | linkedin | instagram | x | youtube",
  "access": "paywall (opcional; só quando a fonte exige assinatura)"
}
```

- `date` é a data de publicação da matéria.
- `environment`: `onshore` quando a notícia trata de ativos ou operações em terra (inclui não convencional, como Vaca Muerta), `offshore` quando trata de ativos no mar, `geral` quando cobre os dois ou é corporativa (resultados, mercado, regulação ampla).
- Título e resumo são redação própria, nunca cópia do texto da fonte. Resumo com uma ou duas frases (até 320 caracteres), só com fatos e números que constam na fonte.
- Inglês e português do Brasil com o mesmo conteúdo. O inglês é o idioma padrão da página: `title_en` e `summary_en` nunca podem ficar vazios.
- Usar sempre o mesmo nome para a mesma empresa (conferir os já usados no arquivo e os nomes da lista prioritária).

### 5. Gravar e publicar

1. Inserir os itens novos em `data/news.json` e atualizar `updated_at` com data e hora de Brasília (formato ISO, `-03:00`).
2. Mover itens com mais de 60 dias para `data/archive/AAAA-MM.json` (mesmo formato de lista).
3. Regravar `data/run.json` com o registro desta varredura, mantendo o campo `schedule` como está:
   - `run_at`: data e hora de Brasília (ISO, `-03:00`);
   - `searches`: número de buscas feitas; `new_items`: notícias novas gravadas;
   - `terms`: nomes das empresas, países e temas efetivamente pesquisados (de 15 a 40 nomes curtos);
   - `queries`: lista das buscas realmente feitas nesta execução, na ordem (até 60), cada uma com `q` (o texto da busca), `ch` (`site`, `linkedin`, `instagram`, `youtube` ou `x`) e `found` (quantas notícias novas saíram dessa busca; pode ser 0). A visita a um site oficial entra como `q` = `Site oficial: <empresa>`, `ch` = `site`;
   - `sites` (obrigatório na varredura das 6h): uma entrada por empresa da tabela de sites oficiais, na ordem, com `name` (nome da empresa), `url` (página aberta, ou vazio se não houver site), `status` (`ok`, `sem_itens`, `bloqueado` ou `sem_site`) e `found` (notícias novas que saíram dela). Nas rodadas de hora em hora, manter o `sites` da varredura das 6h como está.
   Registrar só o que foi de fato pesquisado: o painel ao vivo reproduz essa lista para o leitor.
4. Rodar `python3 scripts/validate.py`. Corrigir até passar.
5. Commit na `main` com a mensagem `Atualiza notícias AAAA-MM-DD (N novas)` e push. Antes do push, fazer `git pull --rebase`. Se der conflito (outra varredura gravou ao mesmo tempo), desfazer o rebase (`git rebase --abort`), voltar para `origin/main` (`git reset --hard origin/main`), inserir de novo só os itens novos desta varredura que ainda não estiverem no arquivo, regravar o `run.json`, validar e enviar outra vez.
6. Não alterar `index.html`, `live.html`, `assets/` nem outros arquivos nesta rotina.

### 6. PDF e e-mail diário

Feita pela tarefa das 7h55, todos os dias (mesmo que nenhuma notícia tenha entrado), depois de `git pull` na `main`. O relatório completo vai sempre em PDF e sempre em inglês.

1. Gerar o PDF e o corpo do e-mail em uma pasta fora do repositório (a pasta de rascunho da sessão):

   ```
   python3 scripts/build_pdf.py \
     --out <pasta>/Hilong-Market-Report-AAAA-MM-DD.pdf \
     --date today --base-ref auto --check-scan --record \
     --email-html <pasta>/email.html --email-text <pasta>/email.txt
   ```

   - `--base-ref auto` compara com o último envio registrado, para que toda notícia gravada desde então entre no relatório. `--check-scan` põe um aviso no e-mail se a varredura das 6h ainda não tiver terminado; o envio acontece assim mesmo.

   - O PDF traz a capa com os números do dia, as 10 principais, o relatório completo dos últimos 7 dias (Brasil por grupo de empresas, América do Sul por país), a cobertura das empresas da lista prioritária e a assinatura do Li Marcitão com a mensagem positiva do dia.
   - **Notícia nova primeiro:** o relatório do dia prioriza o que ainda não saiu em nenhum relatório anterior (marcado NEW); depois vêm as demais por nota, Brasil antes da América do Sul e a mais recente antes.
   - **No máximo dois relatórios por notícia:** a mesma notícia aparece em no máximo duas edições; na terceira ela sai do PDF e do e-mail (continua na página). O controle é o `data/reports.json`, gravado pelo `--record`. Usar `--record` sempre no envio real; ao gerar de novo no mesmo dia (por exemplo com `--alert`), manter o `--record`: a entrada do dia é substituída, não duplicada. Não editar o `data/reports.json` à mão.
   - `email.html` e `email.txt` trazem as 10 principais na mesma ordem do PDF, cada uma com empresa, país, título e resumo, e a mesma assinatura. O corpo do e-mail não leva links (as fontes estão no PDF). O HTML usa só estilos inline, porque o conector do Gmail remove blocos `<style>`, atributos `class` e a propriedade `background`.
   - `--message "..."` troca a mensagem positiva do dia (uma frase curta, em inglês, redação própria). Sem o parâmetro, o script escolhe uma pela data.
   - `--alert "..."` põe um aviso na primeira linha do e-mail. Usar quando o push falhar (por exemplo, `--alert "Push failed: the page was not updated today."`).
   - `--days N` muda a janela do relatório (padrão: 7 dias).
2. Conferir o resultado: o comando termina com `OK:` e o PDF existe e tem mais de uma página.
3. Enviar um único e-mail pelo conector do Gmail, aos destinatários definidos na tarefa agendada:
   - assunto: `Hilong Market Report - AAAA-MM-DD`;
   - `htmlBody`: o conteúdo de `email.html`, sem alterações; `body`: o conteúdo de `email.txt`;
   - anexo: o PDF, com `filename` `Hilong-Market-Report-AAAA-MM-DD.pdf`, `mimeType` `application/pdf` e `content` na forma de referência de arquivo `sha256:<sha256 do arquivo>:<caminho absoluto>` (obter o hash com `sha256sum`).
4. Se o anexo for recusado, gerar de novo com `--alert "The PDF could not be attached today; the full report is on the page."` e enviar o e-mail sem anexo. Se o envio falhar, não tentar outro caminho: registrar no resumo final.
5. Depois do envio, fazer commit e push do `data/reports.json` (mensagem `Registra relatório AAAA-MM-DD`). Não fazer commit do PDF nem dos arquivos do e-mail. Não alterar o `scripts/build_pdf.py` nesta rotina.

### 7. Resumo final

Encerrar com um resumo curto **em inglês**: quantidade de notícias novas por região, os títulos (em inglês) das três a cinco mais relevantes, em ordem de relevância e com o Brasil primeiro, e o link https://marketreportnews.hilongbrazil.com. Dizer também se o e-mail foi enviado e se o PDF foi anexado. Se o push falhar ou nenhuma notícia entrar, dizer isso claramente na primeira linha.
