# Hilong Market Report

Site estático publicado em https://marketreportnews.hilongbrazil.com (Netlify, deploy automático a cada push na branch `main`).

**Acesso só com login** (o mesmo do Centro, hilong.hilongbrazil.com): `netlify/edge-functions/guard.ts` + `netlify.toml`. A única exceção é `/reports/` (o Resend busca os PDFs por endereço). Não remover nem alterar o porteiro sem combinar com o Marcio.

- `index.html`: página de notícias. `live.html`: painel ao vivo (indicadores e atividade do agente).
- `assets/site.css` e `assets/site.js`: estilo e código das duas páginas.
- `data/news.json`: as notícias.
- `data/run.json`: registro da última varredura (alimenta o painel ao vivo).
- `data/reports.json`: registro das edições do relatório em PDF (quais notícias saíram em cada uma). Gravado pelo `scripts/build_pdf.py --record`.
- A rotina diária altera somente `data/news.json`, `data/run.json`, `data/reports.json`, `data/archive/` e `reports/`.
- `data/archive/AAAA-MM.json`: notícias com mais de 60 dias, movidas para cá.
- `scripts/validate.py`: valida o `news.json` e o `run.json`. Rodar antes de todo commit.
- `reports/AAAA-MM-DD/`: PDFs dos últimos 3 dias, publicados no site para o Resend anexar ao e-mail (`scripts/publish_reports.py`).
- `scripts/build_pdf.py`: gera os relatórios em PDF, em inglês e em chinês (`--lang zh`), e o corpo do e-mail diário (seção 6).

## Rotina diária de atualização

Tarefas agendadas, todos os dias (horário de Brasília). Nada roda depois da rodada das 22h nem antes das 6h.

- **6h00, varredura completa:** seções 1 a 5 (pesquisar, selecionar, escrever, gravar e publicar) e o resumo da seção 7, passando por todas as empresas da lista. Não gera PDF nem envia e-mail.
- **6h40, LinkedIn:** seção 1c, no computador do Marcio (navegador do aplicativo Claude, conta alternativa logada). Só roda com o computador ligado e o aplicativo aberto.
- **12h e 22h, rodada rápida:** seção 1b, depois as seções 2 a 5. Não gera PDF nem envia e-mail. (Até 14/11/2026 eram de hora em hora, das 7h às 21h; reduzidas a pedido do Marcio.)
- **7h55, relatório:** só a seção 6 (dois PDFs, em inglês e em chinês, num único e-mail), para o e-mail chegar por volta das 8h. Usa o que as varreduras publicaram até ali.

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

**Click Petróleo e Gás: visita obrigatória em toda varredura e rodada.** Abrir (WebFetch) as duas categorias e conferir tudo o que saiu desde a última atualização:
- Petróleo e Gás: https://clickpetroleoegas.com.br/category/petroleo-oleo-e-gas/
- Setor Offshore: https://clickpetroleoegas.com.br/category/setor-offshore/

Cada página mostra 12 matérias; na varredura das 6h, se a 12ª ainda for posterior ao `updated_at`, buscar as anteriores com `site:clickpetroleoegas.com.br` e palavras do assunto. O WebFetch costuma recusar o link da matéria copiado da lista: buscar o título exato entre aspas (WebSearch) e abrir o link que a busca devolver. Ficam de fora vagas, concursos, cursos, eventos e matérias de outros setores. Registrar cada categoria no `run.json` como `q` = `Site oficial: Click Petróleo e Gás (categoria ...)`, `ch` = `site`.

**Sites de referência:** eixos, Brasil Energia / PetróleoHoje, TN Petróleo, PetroNotícias, Agência Petrobras, sites de RI das companhias, Reuters, BNamericas, OilNOW, Ámbito, Rigzone, Offshore Engineer.

**LinkedIn, Instagram e X:** para cada empresa da lista prioritária, buscar as publicações recentes do perfil oficial (por exemplo, "Carmo Energy LinkedIn", "PetroReconcavo Instagram"). Incluir somente publicação oficial da empresa, com data visível e link público que abre sem login. Marcar `via` como `linkedin`, `instagram` ou `x` e `source` com o nome da empresa. Não tentar fazer login nem contornar bloqueios. Se houver um conector de dados de redes sociais disponível na sessão, usar o conector. A leitura logada do LinkedIn é feita por uma tarefa separada (seção 1c); a varredura na nuvem não tenta entrar no LinkedIn.

**YouTube:** buscar vídeos publicados desde a última atualização nos canais oficiais das empresas e dos veículos do setor (webcasts de resultados, anúncios de projetos, entrevistas de executivos). Registrar apenas o que o título e a descrição do vídeo afirmam; não atribuir ao vídeo nada que não esteja escrito na página. Marcar `via` como `youtube` e `source` com o nome do canal.

### 1b. Rodada rápida (12h e 22h)

Uma rodada curta, de no máximo 12 buscas, só para pegar o que saiu desde a última varredura ou rodada:

1. Sempre: as notícias mais recentes de eixos, PetroNotícias, Agência Petrobras e as duas categorias do Click Petróleo e Gás, Petróleo e Gás e Setor Offshore (canal `site`; endereços e cuidados na seção 1).
2. Um bloco da lista prioritária, conforme a hora da rodada:
   - 12h: onshore (empresas 1 a 11), offshore (12 a 17) e ANP (18);
   - 22h: fornecedores (19 a 29) e uma busca da América do Sul.
   Agrupar empresas na mesma busca quando fizer sentido, para caber nas 12 buscas.
3. Procurar notícias das últimas 48 horas que ainda não estejam em `news.json` (conferir `url` e assunto). Os critérios de seleção, relevância e escrita são os mesmos das seções 2 a 4.
4. Gravar como na seção 5, com estas diferenças: `terms` pode ter menos de 15 nomes (só o que a rodada pesquisou); se nada novo entrar, não alterar `news.json` e regravar só o `run.json` (com `new_items` 0), para o painel mostrar a rodada; mensagem do commit `Rodada AAAA-MM-DD HHh (N novas)`.

### 1c. LinkedIn (6h40, no computador do Marcio)

Tarefa separada, que roda depois da varredura das 6h e antes do relatório das 7h55. Usa o navegador do aplicativo Claude no computador do Marcio, onde uma conta alternativa do LinkedIn já está logada e segue as páginas abaixo. Se o computador não responder, ou se o LinkedIn pedir login ou verificação, não tentar nada: registrar no resumo final e encerrar sem alterar o repositório.

Para cada página, abrir `https://www.linkedin.com/company/<endereço>/posts/?feedView=all`, esperar carregar, rolar uma vez e ler as publicações (elementos `[data-urn^="urn:li:activity"]`). Só leitura: não curtir, comentar, compartilhar, seguir, deixar de seguir nem enviar mensagem. Abrir uma página por vez, com alguns segundos de intervalo.

| Empresa | Endereço da página |
|---|---|
| Carmo Energy | carmoenergy |
| PetroReconcavo | petroreconcavo |
| Brava Energia | brava-energia |
| Origem Energia | origem-energia |
| Mandacaru Energia | mandacaru-energia |
| Seacrest Petróleo | seacrest-petroleo |
| PetroVictory | petro-victory-energy |
| Alvopetro | alvopetro-s-a-extra%C3%A7%C3%A3o-de-petr%C3%B3leo-e-g%C3%A1s-natural e alvopetro-energy-ltd |
| Petroborn | petroborn-%C3%B3leo-e-g%C3%A1s |
| Eneva | eneva |
| Vipetro | vipetro-petroleo |
| Petrobras | petrobras |
| Equinor | equinor |
| Perenco | perenco |
| PRIO | prio3 |
| TotalEnergies | totalenergies |
| Transpetro | transpetro-petrobras-transporte |
| ANP | agencia-nacional-do-petroleo |
| SLB | slbglobal |
| Baker Hughes | bakerhughes |
| Weatherford | weatherford |
| Tenaris | tenaris |
| Expro | expro |
| Confab | confab-industrial-s-a |
| Apolo Tubulars | tubos-apolo |
| Jereh | jerehgroup |
| Kerui | shandongkerui e kerui-petroleum-brasil |
| Inpasa | inpasa |
| TAG | tag-transportadora-associada-de-gas |

- **Data da publicação:** a página mostra só tempo relativo ("3 d", "2 sem"). A data exata sai do número da publicação: `datetime.fromtimestamp((ID >> 22) / 1000)` em horário de Brasília, onde ID é o número do `urn:li:activity:ID`. Considerar só publicações desde o `updated_at` anterior à varredura das 6h (no máximo 48 horas).
- **O que entra:** só fato novo que passe nos critérios da seção 2 (contratos, perfuração, workover, produção, investimentos, resultados, leilões, aquisições). Ficam de fora vagas, datas comemorativas, institucional, eventos, treinamentos, saúde e segurança e responsabilidade social. Se o mesmo fato já estiver em `news.json` vindo de outra fonte, não repetir.
- **Item:** `via` = `linkedin`, `source` = nome da empresa, `url` = `https://www.linkedin.com/feed/update/urn:li:activity:ID/`. Título e resumo com redação própria, só com o que a publicação afirma.
- **Gravar:** inserir os itens em `data/news.json` e atualizar `updated_at`. No `data/run.json`, não regravar: acrescentar ao que a varredura das 6h deixou uma entrada em `queries` por página lida (`q` = `LinkedIn: <empresa>`, `ch` = `linkedin`, `found` = notícias que saíram dela), somar as páginas em `searches` e as notícias em `new_items`. Validar, commit `LinkedIn AAAA-MM-DD (N novas)`, `git pull --rebase` e push (conflito: item 5 da seção 5).

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
  "title_pt": "...", "title_en": "...", "title_zh": "...",
  "summary_pt": "...", "summary_en": "...", "summary_zh": "...",
  "source": "Nome do veículo",
  "url": "https://...",
  "via": "site | linkedin | instagram | x | youtube",
  "access": "paywall (opcional; só quando a fonte exige assinatura)"
}
```

- `date` é a data de publicação da matéria.
- `environment`: `onshore` quando a notícia trata de ativos ou operações em terra (inclui não convencional, como Vaca Muerta), `offshore` quando trata de ativos no mar, `geral` quando cobre os dois ou é corporativa (resultados, mercado, regulação ampla).
- Título e resumo são redação própria, nunca cópia do texto da fonte. Resumo com uma ou duas frases (até 320 caracteres), só com fatos e números que constam na fonte.
- Inglês, português do Brasil e chinês simplificado com o mesmo conteúdo. O inglês é o idioma padrão da página: `title_en` e `summary_en` nunca podem ficar vazios. `title_zh` e `summary_zh` são obrigatórios (o validador recusa sem eles) e vão para o relatório em PDF enviado à China, então a tradução precisa ser a melhor possível:
  - chinês simplificado, registro de imprensa de negócios, frases naturais (não tradução palavra por palavra);
  - nomes de empresas, campos, blocos, plataformas e poços em letras latinas, como na fonte (Petrobras, Búzios, BM-S-24, P-78); siglas de órgãos também (ANP, Ibama, CADE);
  - termos do setor: 修井 (workover), 钻机 (sonda/rig), 钻井 (perfuração), 完井 (completação), 油管/套管 (OCTG), 抽油杆 (haste de bombeio), 井下工具 (ferramentas de fundo), 盐下 (pré-sal), 陆上/海上 (onshore/offshore), 最终投资决定 (FID), 桶/日 (bpd), 桶油当量/日 (boe/d);
  - números iguais aos da fonte, com as unidades chinesas usuais (万、亿): 26 万桶/日, 36 亿雷亚尔, 79 亿美元;
  - `summary_zh` com até 200 caracteres.
- Usar sempre o mesmo nome para a mesma empresa (conferir os já usados no arquivo e os nomes da lista prioritária).

### 5. Gravar e publicar

1. Inserir os itens novos em `data/news.json` e atualizar `updated_at` com data e hora de Brasília (formato ISO, `-03:00`).
2. Mover itens com mais de 60 dias para `data/archive/AAAA-MM.json` (mesmo formato de lista).
3. Regravar `data/run.json` com o registro desta varredura, mantendo o campo `schedule` como está:
   - `run_at`: data e hora de Brasília (ISO, `-03:00`);
   - `searches`: número de buscas feitas; `new_items`: notícias novas gravadas;
   - `terms`: nomes das empresas, países e temas efetivamente pesquisados (de 15 a 40 nomes curtos);
   - `queries`: lista das buscas realmente feitas nesta execução, na ordem (até 60), cada uma com `q` (o texto da busca), `ch` (`site`, `linkedin`, `instagram`, `youtube` ou `x`) e `found` (quantas notícias novas saíram dessa busca; pode ser 0). A visita a um site oficial entra como `q` = `Site oficial: <empresa>`, `ch` = `site`;
   - `sites` (obrigatório na varredura das 6h): uma entrada por empresa da tabela de sites oficiais, na ordem, com `name` (nome da empresa), `url` (página aberta, ou vazio se não houver site), `status` (`ok`, `sem_itens`, `bloqueado` ou `sem_site`) e `found` (notícias novas que saíram dela). Nas rodadas das 12h e 22h, manter o `sites` da varredura das 6h como está.
   Registrar só o que foi de fato pesquisado: o painel ao vivo reproduz essa lista para o leitor.
4. Rodar `python3 scripts/validate.py`. Corrigir até passar.
5. Commit na `main` com a mensagem `Atualiza notícias AAAA-MM-DD (N novas)` e push. Antes do push, fazer `git pull --rebase`. Se der conflito (outra varredura gravou ao mesmo tempo), desfazer o rebase (`git rebase --abort`), voltar para `origin/main` (`git reset --hard origin/main`), inserir de novo só os itens novos desta varredura que ainda não estiverem no arquivo, regravar o `run.json`, validar e enviar outra vez.
6. Não alterar `index.html`, `live.html`, `assets/` nem outros arquivos nesta rotina.

### 6. PDF e e-mail diário

Feita pela tarefa das 7h55, todos os dias (mesmo que nenhuma notícia tenha entrado), depois de `git pull` na `main`. São dois relatórios em PDF, com as mesmas notícias: um em inglês e outro em chinês simplificado (para a China). Os dois vão no mesmo e-mail.

1. Conferir que todas as notícias da janela têm `title_zh` e `summary_zh` (`python3 scripts/validate.py`). Se faltar alguma, escrever a tradução seguindo as regras da seção 4 e fazer commit antes de gerar os PDFs.

2. Gerar os dois PDFs e o corpo do e-mail em uma pasta fora do repositório (a pasta de rascunho da sessão). Primeiro o inglês, que registra a edição:

   ```
   python3 scripts/build_pdf.py \
     --out <pasta>/Hilong-Market-Report-AAAA-MM-DD.pdf \
     --date today --base-ref auto --check-scan --record \
     --email-html <pasta>/email.html --email-text <pasta>/email.txt
   ```

   Depois o chinês, sem `--record` e antes de qualquer commit (para as mesmas notícias saírem como novas nos dois):

   ```
   python3 scripts/build_pdf.py --lang zh \
     --out <pasta>/Hilong-Market-Report-AAAA-MM-DD-ZH.pdf \
     --date today --base-ref auto
   ```

   - **Janela de 15 dias:** os relatórios trazem todas as notícias dos últimos 15 dias corridos, contando o dia da edição (`--days 15` é o padrão), sem limite de quantas edições a mesma notícia aparece.
   - **Notícias novas no topo:** a primeira seção, "New in this report" / "本期新消息", lista todas as notícias que ainda não saíram em nenhum relatório anterior (marcadas NEW / 新), por relevância, Brasil antes da América do Sul. Depois vem o histórico completo dos 15 dias (Brasil por grupo de empresas, América do Sul por país, novas primeiro em cada grupo), a cobertura das empresas da lista prioritária e a assinatura do Li Marcitão com a mensagem positiva do dia (em chinês no PDF chinês).
   - O controle do que é novo é o `data/reports.json`, gravado pelo `--record` só no PDF em inglês. Não editar o `data/reports.json` à mão. Ao gerar de novo no mesmo dia, manter o `--record`: a entrada do dia é substituída, não duplicada.
   - **Corpo do e-mail:** só o aviso de que o relatório diário chegou e o período avaliado, em inglês e em chinês, e a assinatura do Li Marcitão. Sem lista de notícias e sem links. O HTML usa só estilos inline.
   - `--message "..."` / `--message-zh "..."` trocam a mensagem positiva do dia; sem o parâmetro, o script escolhe uma pela data.
   - `--alert "..."` põe um aviso na primeira linha do e-mail (por exemplo, quando o push falhar). `--check-scan` põe o aviso automaticamente se a varredura das 6h ainda não tiver terminado; o envio acontece assim mesmo.
   - A análise do agente no topo do PDF foi desligada em 13/11/2026: não usar `--brief` nem `--analysis`.

3. Conferir o resultado: os dois comandos terminam com `OK:` e os dois PDFs existem e têm mais de uma página.

4. **Publicar os PDFs no site** (o Resend busca os arquivos por endereço para anexar):

   ```
   python3 scripts/publish_reports.py --date AAAA-MM-DD <pasta>/Hilong-Market-Report-AAAA-MM-DD.pdf <pasta>/Hilong-Market-Report-AAAA-MM-DD-ZH.pdf
   ```

   O script copia os PDFs para `reports/AAAA-MM-DD/`, apaga as pastas com mais de 3 dias e imprime os endereços (`URL: https://marketreportnews.netlify.app/reports/...`). Fazer commit de `reports/` junto com o `data/reports.json` (mensagem `Registra relatório AAAA-MM-DD`), `git pull --rebase` e push. Esperar cerca de 90 segundos para o Netlify publicar.

5. **Enviar um único e-mail pelo Resend** (ferramenta `send-email` do conector Resend), aos destinatários definidos na tarefa agendada:
   - `from`: `noreply@hilongbrazil.com`;
   - assunto: `Hilong Market Report - AAAA-MM-DD`;
   - `html`: o conteúdo de `email.html`, sem alterações; `text`: o conteúdo de `email.txt`;
   - dois anexos por endereço: `{"filename": "Hilong-Market-Report-AAAA-MM-DD.pdf", "url": "<URL do PDF em inglês>", "contentType": "application/pdf"}` e `{"filename": "Hilong-Market-Report-AAAA-MM-DD-ZH.pdf", "url": "<URL do PDF em chinês>", "contentType": "application/pdf"}`;
   - `idempotencyKey`: `hilong-report-AAAA-MM-DD` (evita e-mail duplicado se precisar repetir a chamada).
   Se o Resend falhar (conector indisponível, erro ou os anexos não puderem ser buscados), esperar 60 segundos e tentar uma vez com a mesma `idempotencyKey`.

6. **Reserva: Gmail.** Só se o Resend falhar duas vezes, enviar pelo conector do Gmail (remetente: o Gmail hilongbrazil), com o mesmo assunto, `htmlBody` = `email.html`, `body` = `email.txt` e os dois PDFs anexados como referência de arquivo `sha256:<sha256 do arquivo>:<caminho absoluto>` (`mimeType` `application/pdf`, com os mesmos nomes de arquivo; hash com `sha256sum`). Se os anexos forem recusados, gerar de novo o PDF em inglês (com `--record`) e o corpo do e-mail com `--alert "The PDFs could not be attached today; the reports are on the page."` e enviar sem anexo. Nunca enviar pelos dois caminhos no mesmo dia. Se o Gmail também falhar, não tentar outro caminho: registrar no resumo final.

7. Não fazer commit dos PDFs fora de `reports/` nem dos arquivos do e-mail. Não alterar o `scripts/build_pdf.py` nem o `scripts/publish_reports.py` nesta rotina.

### 7. Resumo final

Encerrar com um resumo curto **em inglês**: quantidade de notícias novas por região, os títulos (em inglês) das três a cinco mais relevantes, em ordem de relevância e com o Brasil primeiro, e o link https://marketreportnews.hilongbrazil.com. Dizer também se o e-mail foi enviado, por qual caminho (Resend ou Gmail de reserva) e se os dois PDFs (inglês e chinês) foram anexados. Se o push falhar ou nenhuma notícia entrar, dizer isso claramente na primeira linha.
