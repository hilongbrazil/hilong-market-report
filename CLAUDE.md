# Hilong Market Report

Site estático publicado em https://marketreport.hilongbrazil.com (Netlify, deploy automático a cada push na branch `main`).

- `index.html`: página de notícias. `live.html`: painel ao vivo (indicadores e atividade do agente).
- `assets/site.css` e `assets/site.js`: estilo e código das duas páginas.
- `data/news.json`: as notícias.
- `data/run.json`: registro da última varredura (alimenta o painel ao vivo).
- A rotina diária altera somente `data/news.json`, `data/run.json` e `data/archive/`.
- `data/archive/AAAA-MM.json`: notícias com mais de 60 dias, movidas para cá.
- `scripts/validate.py`: valida o `news.json` e o `run.json`. Rodar antes de todo commit.
- `scripts/build_pdf.py`: gera o relatório completo em PDF e o corpo do e-mail diário, sempre em inglês (seção 6).

## Rotina diária de atualização

Objetivo: registrar as principais notícias do mercado de óleo e gás no Brasil e na América do Sul publicadas desde a última atualização (`updated_at`), com foco no que interessa a uma empresa de serviços e equipamentos de petróleo (sondas de perfuração e workover, OCTG, hastes de bombeio, ferramentas de fundo de poço).

**Prioridade: o mercado brasileiro vem sempre primeiro.** Pesquisar todas as empresas da lista prioritária abaixo, na ordem em que aparecem (onshore, depois offshore, depois fornecedores), antes de passar para a América do Sul.

### 1. Pesquisar

Usar WebSearch (e WebFetch para confirmar data, números e se o link abre). Fazer uma busca separada por empresa; uma busca genérica não cobre tudo. Cada execução passa pelos canais: sites, LinkedIn, Instagram, YouTube e X.

**Lista prioritária (Brasil)**

Onshore:
1. Carmo Energy
2. PetroReconcavo
3. Brava Energia
4. Origem Energia
5. Mandacaru Energia
6. Seacrest Petróleo
7. PetroVictory
8. Alvopetro
9. Enauta (hoje parte da Brava Energia; pesquisar também pelos ativos Atlanta e Papa-Terra)
10. Vipetro

Offshore:
11. Petrobras
12. Equinor
13. Perenco
14. PRIO
15. TotalEnergies

Fornecedores:
16. SLB
17. Baker Hughes
18. Weatherford
19. Tenaris
20. Confab (Tenaris Confab)
21. Apolo Tubulars
22. Jereh
23. Kerui

**Complementos no Brasil:** ANP (leilões, oferta permanente, regulação), Eneva, Petroborn, Shell, onshore do Nordeste (Sergipe, Bahia, Rio Grande do Norte, Alagoas) e contratos de sondas terrestres de perfuração e workover (Braserv, San Antonio Internacional e outras).

**América do Sul (depois do Brasil):** Argentina (YPF, Vista, Pan American Energy, Pluspetrol, Vaca Muerta), Colômbia (Ecopetrol), Guiana e Suriname (ExxonMobil, Staatsolie, TotalEnergies), Peru (Petroperú, Perupetro), Equador (Petroecuador), Bolívia (YPFB), Venezuela (PDVSA) e demais países quando houver fato relevante. Incluir também os fornecedores da lista quando a notícia for sobre a região.

**Sites de referência:** eixos, Brasil Energia / PetróleoHoje, TN Petróleo, PetroNotícias, Agência Petrobras, sites de RI das companhias, Reuters, BNamericas, OilNOW, Ámbito, Rigzone, Offshore Engineer.

**LinkedIn, Instagram e X:** para cada empresa da lista prioritária, buscar as publicações recentes do perfil oficial (por exemplo, "Carmo Energy LinkedIn", "PetroReconcavo Instagram"). Incluir somente publicação oficial da empresa, com data visível e link público que abre sem login. Marcar `via` como `linkedin`, `instagram` ou `x` e `source` com o nome da empresa. Não tentar fazer login nem contornar bloqueios. Se houver um conector de dados de redes sociais disponível na sessão, usar o conector.

**YouTube:** buscar vídeos publicados desde a última atualização nos canais oficiais das empresas e dos veículos do setor (webcasts de resultados, anúncios de projetos, entrevistas de executivos). Registrar apenas o que o título e a descrição do vídeo afirmam; não atribuir ao vídeo nada que não esteja escrito na página. Marcar `via` como `youtube` e `source` com o nome do canal.

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

Antes de alterar qualquer arquivo, logo depois do `git pull`, anotar o hash do commit atual (`git rev-parse --short HEAD`). Ele é o `--base-ref` da seção 6 e serve para marcar as notícias novas.

1. Inserir os itens novos em `data/news.json` e atualizar `updated_at` com data e hora de Brasília (formato ISO, `-03:00`).
2. Mover itens com mais de 60 dias para `data/archive/AAAA-MM.json` (mesmo formato de lista).
3. Regravar `data/run.json` com o registro desta varredura, mantendo o campo `schedule` como está:
   - `run_at`: data e hora de Brasília (ISO, `-03:00`);
   - `searches`: número de buscas feitas; `new_items`: notícias novas gravadas;
   - `terms`: nomes das empresas, países e temas efetivamente pesquisados (de 15 a 40 nomes curtos);
   - `queries`: lista das buscas realmente feitas nesta execução, na ordem (até 60), cada uma com `q` (o texto da busca), `ch` (`site`, `linkedin`, `instagram`, `youtube` ou `x`) e `found` (quantas notícias novas saíram dessa busca; pode ser 0).
   Registrar só o que foi de fato pesquisado: o painel ao vivo reproduz essa lista para o leitor.
4. Rodar `python3 scripts/validate.py`. Corrigir até passar.
5. Commit na `main` com a mensagem `Atualiza notícias AAAA-MM-DD (N novas)` e push.
6. Não alterar `index.html`, `live.html`, `assets/` nem outros arquivos nesta rotina.

### 6. PDF e e-mail diário

Todo dia, depois do push (mesmo que nenhuma notícia tenha entrado), gerar o relatório em PDF e enviar o e-mail. O relatório completo vai sempre em PDF e sempre em inglês.

1. Gerar o PDF e o corpo do e-mail em uma pasta fora do repositório (a pasta de rascunho da sessão):

   ```
   python3 scripts/build_pdf.py \
     --out <pasta>/Hilong-Market-Report-AAAA-MM-DD.pdf \
     --base-ref <hash anotado no início> \
     --email-html <pasta>/email.html --email-text <pasta>/email.txt
   ```

   - O PDF traz a capa com os números do dia, as 10 principais, o relatório completo dos últimos 7 dias (Brasil por grupo de empresas, América do Sul por país), a cobertura das 23 empresas da lista prioritária e a assinatura do Li Marcitão com a mensagem positiva do dia.
   - `email.html` e `email.txt` trazem as 10 principais na mesma ordem do PDF (nota maior primeiro, Brasil antes da América do Sul, mais recente antes) e a mesma assinatura.
   - `--message "..."` troca a mensagem positiva do dia (uma frase curta, em inglês, redação própria). Sem o parâmetro, o script escolhe uma pela data.
   - `--alert "..."` põe um aviso na primeira linha do e-mail. Usar quando o push falhar (por exemplo, `--alert "Push failed: the page was not updated today."`).
   - `--days N` muda a janela do relatório (padrão: 7 dias).
2. Conferir o resultado: o comando termina com `OK:` e o PDF existe e tem mais de uma página.
3. Enviar um único e-mail pelo conector do Gmail, aos destinatários definidos na tarefa agendada:
   - assunto: `Hilong Market Report - AAAA-MM-DD`;
   - `htmlBody`: o conteúdo de `email.html`, sem alterações; `body`: o conteúdo de `email.txt`;
   - anexo: o PDF, com `filename` `Hilong-Market-Report-AAAA-MM-DD.pdf`, `mimeType` `application/pdf` e `content` na forma de referência de arquivo `sha256:<sha256 do arquivo>:<caminho absoluto>` (obter o hash com `sha256sum`).
4. Se o anexo for recusado, gerar de novo com `--alert "The PDF could not be attached today; the full report is on the page."` e enviar o e-mail sem anexo. Se o envio falhar, não tentar outro caminho: registrar no resumo final.
5. Não fazer commit do PDF nem dos arquivos do e-mail. Não alterar o `scripts/build_pdf.py` nesta rotina.

### 7. Resumo final

Encerrar com um resumo curto **em inglês**: quantidade de notícias novas por região, os títulos (em inglês) das três a cinco mais relevantes, em ordem de relevância e com o Brasil primeiro, e o link https://marketreport.hilongbrazil.com. Dizer também se o e-mail foi enviado e se o PDF foi anexado. Se o push falhar ou nenhuma notícia entrar, dizer isso claramente na primeira linha.
