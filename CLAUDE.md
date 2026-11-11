# Hilong Market Report

Site estático publicado em https://marketreport.hilongbrazil.com (Netlify, deploy automático a cada push na branch `main`).

- `index.html`: a página (HTML, CSS e JS em um arquivo só, sem dependências).
- `data/news.json`: as notícias. É o único arquivo que a rotina diária altera.
- `data/archive/AAAA-MM.json`: notícias com mais de 60 dias, movidas para cá.
- `scripts/validate.py`: valida o `news.json`. Rodar antes de todo commit.

## Rotina diária de atualização

Objetivo: registrar as principais notícias de óleo e gás das operadoras do Brasil e da América do Sul publicadas desde a última atualização (`updated_at`), com foco no que interessa a uma empresa de serviços e equipamentos de petróleo (sondas de perfuração e workover, OCTG, hastes de bombeio, ferramentas de fundo de poço).

### 1. Pesquisar

Usar WebSearch (e WebFetch quando precisar confirmar data ou números). Fazer buscas separadas por operadora e por país; uma busca genérica não cobre tudo.

**Brasil:** Petrobras, PRIO, Brava Energia, PetroReconcavo, Eneva, Carmo Energy, Seacrest, Origem Energia, Petroborn, PetroVictory, Alvopetro, Equinor, Shell, TotalEnergies, ANP (leilões, oferta permanente, regulação) e onshore do Nordeste (Sergipe, Bahia, Rio Grande do Norte, Alagoas).

**América do Sul:** Argentina (YPF, Vista, Pan American Energy, Pluspetrol, Vaca Muerta), Colômbia (Ecopetrol), Guiana e Suriname (ExxonMobil, Staatsolie, TotalEnergies), Peru (Petroperú, Perupetro), Equador (Petroecuador), Bolívia (YPFB), Venezuela (PDVSA) e demais países quando houver fato relevante.

**Veículos de referência:** eixos, Brasil Energia / PetróleoHoje, TN Petróleo, PetroNotícias, Agência Petrobras, sites de RI das companhias, Reuters, BNamericas, OilNOW, Ámbito, Rigzone, Offshore Engineer.

**LinkedIn e X:** incluir apenas o que aparecer em resultados públicos de busca (publicações oficiais das operadoras). Marcar `via` como `linkedin` ou `x`. Não tentar fazer login.

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
  "title_pt": "...", "title_en": "...",
  "summary_pt": "...", "summary_en": "...",
  "source": "Nome do veículo",
  "url": "https://...",
  "via": "site | linkedin | x"
}
```

- `date` é a data de publicação da matéria.
- Título e resumo são redação própria, nunca cópia do texto da fonte. Resumo com uma ou duas frases (até 320 caracteres), só com fatos e números que constam na fonte.
- Português do Brasil e inglês com o mesmo conteúdo.
- Usar sempre o mesmo nome para a mesma operadora (conferir os já usados no arquivo).

### 4. Gravar e publicar

1. Inserir os itens novos em `data/news.json` e atualizar `updated_at` com data e hora de Brasília (formato ISO, `-03:00`).
2. Mover itens com mais de 60 dias para `data/archive/AAAA-MM.json` (mesmo formato de lista).
3. Rodar `python3 scripts/validate.py`. Corrigir até passar.
4. Commit na `main` com a mensagem `Atualiza notícias AAAA-MM-DD (N novas)` e push.
5. Não alterar `index.html` nem outros arquivos nesta rotina.

### 5. Resumo final

Encerrar com um resumo curto em português, que é o texto enviado por e-mail: quantidade de notícias novas por região, os títulos das três a cinco mais importantes e o link https://marketreport.hilongbrazil.com. Se o push falhar ou nenhuma notícia entrar, dizer isso claramente na primeira linha.
