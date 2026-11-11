# Hilong Market Report

Site estático publicado em https://marketreport.hilongbrazil.com (Netlify, deploy automático a cada push na branch `main`).

- `index.html`: a página (HTML, CSS e JS em um arquivo só, sem dependências).
- `data/news.json`: as notícias.
- `data/run.json`: registro da última varredura (alimenta o painel "Market pulse" da página).
- A rotina diária altera somente `data/news.json`, `data/run.json` e `data/archive/`.
- `data/archive/AAAA-MM.json`: notícias com mais de 60 dias, movidas para cá.
- `scripts/validate.py`: valida o `news.json` e o `run.json`. Rodar antes de todo commit.

## Rotina diária de atualização

Objetivo: registrar as principais notícias de óleo e gás das operadoras e demais empresas do setor no Brasil e na América do Sul publicadas desde a última atualização (`updated_at`), com foco no que interessa a uma empresa de serviços e equipamentos de petróleo (sondas de perfuração e workover, OCTG, hastes de bombeio, ferramentas de fundo de poço).

### 1. Pesquisar

Usar WebSearch (e WebFetch quando precisar confirmar data ou números). Fazer buscas separadas por empresa e por país; uma busca genérica não cobre tudo. Cada execução deve passar pelas quatro frentes abaixo: sites, LinkedIn, YouTube e X.

**Operadoras no Brasil:** Petrobras, PRIO, Brava Energia, PetroReconcavo, Eneva, Carmo Energy, Seacrest, Origem Energia, Petroborn, PetroVictory, Alvopetro, Equinor, Shell, TotalEnergies, ANP (leilões, oferta permanente, regulação) e onshore do Nordeste (Sergipe, Bahia, Rio Grande do Norte, Alagoas).

**Operadoras na América do Sul:** Argentina (YPF, Vista, Pan American Energy, Pluspetrol, Vaca Muerta), Colômbia (Ecopetrol), Guiana e Suriname (ExxonMobil, Staatsolie, TotalEnergies), Peru (Petroperú, Perupetro), Equador (Petroecuador), Bolívia (YPFB), Venezuela (PDVSA) e demais países quando houver fato relevante.

**Demais empresas (serviços, sondas e equipamentos), quando a notícia for sobre Brasil ou América do Sul:** SLB, Halliburton, Baker Hughes, Weatherford, NOV, Tenaris, Vallourec, TechnipFMC, Subsea7, Foresea, Constellation, Ocyan, Valaris, Seadrill, Transocean, Noble, Nabors, Helmerich & Payne, San Antonio Internacional, Braserv, e contratos de sondas terrestres de perfuração e workover. No campo `operator`, usar o nome da empresa.

**Sites de referência:** eixos, Brasil Energia / PetróleoHoje, TN Petróleo, PetroNotícias, Agência Petrobras, sites de RI das companhias, Reuters, BNamericas, OilNOW, Ámbito, Rigzone, Offshore Engineer.

**LinkedIn:** para cada empresa das listas acima, buscar as publicações recentes da página oficial (por exemplo, "Petrobras LinkedIn" mais o assunto ou o mês). Incluir somente publicação oficial da empresa, com data visível e link público que abre sem login. Marcar `via` como `linkedin` e `source` com o nome da empresa. Não tentar fazer login nem contornar bloqueios. Se houver um conector de dados do LinkedIn disponível na sessão, usar o conector para ler as publicações das páginas das empresas.

**YouTube:** buscar vídeos publicados desde a última atualização nos canais oficiais das empresas e dos veículos do setor (webcasts de resultados, anúncios de projetos, entrevistas de executivos). Registrar apenas o que o título e a descrição do vídeo afirmam; não atribuir ao vídeo nada que não esteja escrito na página. Marcar `via` como `youtube` e `source` com o nome do canal.

**X:** publicações oficiais das empresas que aparecerem em resultados públicos de busca. Marcar `via` como `x`.

### 2. Selecionar

- Prioridade: perfuração e sondas, campanhas de workover, contratos e licitações, produção, investimentos (capex), descobertas, leilões, fusões e aquisições, resultados trimestrais, mudanças regulatórias.
- Deixar de fora: recomendações de ações, opinião sem fato novo, política sem efeito direto no setor, conteúdo patrocinado.
- Só entra notícia com data de publicação confirmada e link que abre. Na dúvida sobre a data ou sobre um número, não incluir.
- Não repetir: conferir `url` e assunto contra o que já está em `news.json`.
- Meta: de 5 a 15 notícias novas por dia, equilibrando Brasil e América do Sul. Se não houver nada relevante, não inventar: registrar zero.

### 3. Escrever

Cada item segue este formato:

```json
{
  "id": "AAAA-MM-DD-slug-curto",
  "date": "AAAA-MM-DD",
  "region": "BR ou SA",
  "country": "BR, AR, CO, GY, SR, PE, EC, BO, VE, CL, UY, PY ou TT",
  "operator": "Nome da operadora, ou Setor quando for geral",
  "category": "resultados | producao | perfuracao | investimentos | contratos | regulatorio | exploracao | mercado | fusoes | outros",
  "environment": "onshore | offshore | geral",
  "title_pt": "...", "title_en": "...",
  "summary_pt": "...", "summary_en": "...",
  "source": "Nome do veículo",
  "url": "https://...",
  "via": "site | linkedin | x | youtube"
}
```

- `date` é a data de publicação da matéria.
- `environment`: `onshore` quando a notícia trata de ativos ou operações em terra (inclui não convencional, como Vaca Muerta), `offshore` quando trata de ativos no mar, `geral` quando cobre os dois ou é corporativa (resultados, mercado, regulação ampla).
- Título e resumo são redação própria, nunca cópia do texto da fonte. Resumo com uma ou duas frases (até 320 caracteres), só com fatos e números que constam na fonte.
- Inglês e português do Brasil com o mesmo conteúdo. O inglês é o idioma padrão da página: `title_en` e `summary_en` nunca podem ficar vazios.
- Usar sempre o mesmo nome para a mesma operadora (conferir os já usados no arquivo).

### 4. Gravar e publicar

1. Inserir os itens novos em `data/news.json` e atualizar `updated_at` com data e hora de Brasília (formato ISO, `-03:00`).
2. Mover itens com mais de 60 dias para `data/archive/AAAA-MM.json` (mesmo formato de lista).
3. Regravar `data/run.json` com o registro desta varredura: `run_at` (data e hora de Brasília, ISO), `searches` (número de buscas feitas), `new_items` (notícias novas gravadas) e `terms` (lista com os nomes das empresas, países e temas efetivamente pesquisados nesta execução, de 15 a 40 nomes curtos). Registrar só o que foi de fato pesquisado.
4. Rodar `python3 scripts/validate.py`. Corrigir até passar.
5. Commit na `main` com a mensagem `Atualiza notícias AAAA-MM-DD (N novas)` e push.
6. Não alterar `index.html` nem outros arquivos nesta rotina.

### 5. Resumo final

Encerrar com um resumo curto **em inglês**, que é o texto enviado por e-mail: quantidade de notícias novas por região, os títulos (em inglês) das três a cinco mais importantes e o link https://marketreport.hilongbrazil.com. Se o push falhar ou nenhuma notícia entrar, dizer isso claramente na primeira linha.
