(function () {
  "use strict";

  var T = {
    pt: {
      focus: "Foco Hilong", supplier: "Fornecedor", focusHint: "= interesse direto da Hilong (sondas, workover, operadoras onshore)",
      meet: "Conheça o Li Marcitão", aiNote: "Li Marcitão é um personagem virtual gerado por IA.", close: "Fechar",
      navNews: "Notícias", navLive: "Painel ao vivo", openLive: "Abrir o painel ao vivo", topT: "Destaques da semana",
      sub: "Notícias de óleo e gás das operadoras e empresas do setor no Brasil e na América do Sul.",
      updated: "Atualizado em",
      all: "Todas", BR: "Brasil", SA: "América do Sul",
      operator: "Empresa", allOps: "Todas as empresas",
      category: "Assunto", allCats: "Todos os assuntos", allEnvs: "Todos os ambientes",
      search: "Buscar", searchPh: "Buscar por palavra",
      source: "Fonte", read: "abrir o original", paywall: "exige assinatura",
      emptyT: "Nenhuma notícia com esses filtros", emptyP: "Tente outra empresa, outro assunto ou outra palavra.", clear: "Limpar filtros",
      errT: "Não foi possível carregar as notícias", errP: "Verifique a conexão e recarregue a página.", reload: "Recarregar",
      foot: "Os resumos são elaborados pela Hilong Brasil a partir das fontes indicadas. Abra o link de cada notícia para ver o original.",
      sector: "Setor",
      latest: "Últimas", pause: "Pausar", resume: "Retomar", clockTz: "Brasília",
      spotT: "Em destaque", prev: "Anterior", next: "Próxima",
      kpiT: "Indicadores",
      kStories: "notícias no período", kCompanies: "empresas citadas", kCountries: "países", kSources: "fontes consultadas",
      topics: "Assuntos mais frequentes", companies: "Empresas mais citadas", countriesT: "Países",
      envT: "Ambiente", perDay: "Notícias por dia", channels: "Canais de origem",
      agentT: "Agente de pesquisa", lastScan: "Última varredura", nextScan: "Próxima varredura em",
      ago: "há {t}", searchesL: "buscas na última varredura", newL: "notícias novas encontradas",
      feedT: "Atividade do agente", replayOf: "Reprodução das buscas feitas na varredura de {d}",
      scanDone: "Varredura concluída: {n} buscas, {m} notícias novas",
      coverT: "Empresas e temas cobertos na última varredura",
      liveFoot: "O relógio e a contagem regressiva são em tempo real. As buscas exibidas são a reprodução da última varredura feita pelo agente; os dados da página se atualizam sozinhos quando uma nova varredura termina.",
      noData: "Sem notícias neste recorte.", story1: "notícia", storyN: "notícias", newShort: "nova(s)",
      envs: { onshore: "Onshore", offshore: "Offshore", geral: "Geral" },
      chs: { site: "Sites", linkedin: "LinkedIn", instagram: "Instagram", youtube: "YouTube", x: "X" },
      chShort: { site: "Web", linkedin: "LinkedIn", instagram: "Instagram", youtube: "YouTube", x: "X" },
      cats: { resultados: "Resultados", producao: "Produção", perfuracao: "Perfuração", investimentos: "Investimentos", contratos: "Contratos e licitações", regulatorio: "Regulatório", exploracao: "Exploração", mercado: "Mercado", fusoes: "Fusões e aquisições", outros: "Outros" },
      countries: { BR: "Brasil", AR: "Argentina", CO: "Colômbia", GY: "Guiana", SR: "Suriname", PE: "Peru", EC: "Equador", BO: "Bolívia", VE: "Venezuela", CL: "Chile", UY: "Uruguai", PY: "Paraguai", TT: "Trinidad e Tobago" }
    },
    en: {
      focus: "Hilong focus", supplier: "Supplier", focusHint: "= direct interest for Hilong (rigs, workover, onshore operators)",
      meet: "Meet Li Marcitão", aiNote: "Li Marcitão is an AI-generated virtual character.", close: "Close",
      navNews: "News", navLive: "Live panel", openLive: "Open the live panel", topT: "Top stories this week",
      sub: "Oil and gas news from operators and industry companies in Brazil and South America.",
      updated: "Updated on",
      all: "All", BR: "Brazil", SA: "South America",
      operator: "Company", allOps: "All companies",
      category: "Topic", allCats: "All topics", allEnvs: "All environments",
      search: "Search", searchPh: "Search by keyword",
      source: "Source", read: "open the original", paywall: "subscription required",
      emptyT: "No stories match these filters", emptyP: "Try another company, topic or keyword.", clear: "Clear filters",
      errT: "The news could not be loaded", errP: "Check your connection and reload the page.", reload: "Reload",
      foot: "Summaries are written by Hilong Brasil from the sources shown. Open each story's link to see the original.",
      sector: "Industry",
      latest: "Latest", pause: "Pause", resume: "Resume", clockTz: "Brasília",
      spotT: "In focus", prev: "Previous", next: "Next",
      kpiT: "Indicators",
      kStories: "stories in the period", kCompanies: "companies mentioned", kCountries: "countries", kSources: "sources consulted",
      topics: "Most frequent topics", companies: "Most mentioned companies", countriesT: "Countries",
      envT: "Environment", perDay: "Stories per day", channels: "Source channels",
      agentT: "Research agent", lastScan: "Latest scan", nextScan: "Next scan in",
      ago: "{t} ago", searchesL: "searches in the latest scan", newL: "new stories found",
      feedT: "Agent activity", replayOf: "Replay of the searches run in the scan on {d}",
      scanDone: "Scan complete: {n} searches, {m} new stories",
      coverT: "Companies and topics covered in the latest scan",
      liveFoot: "The clock and the countdown are real time. The searches shown are a replay of the agent's latest scan; the page data refreshes by itself when a new scan finishes.",
      noData: "No stories in this view.", story1: "story", storyN: "stories", newShort: "new",
      envs: { onshore: "Onshore", offshore: "Offshore", geral: "General" },
      chs: { site: "Websites", linkedin: "LinkedIn", instagram: "Instagram", youtube: "YouTube", x: "X" },
      chShort: { site: "Web", linkedin: "LinkedIn", instagram: "Instagram", youtube: "YouTube", x: "X" },
      cats: { resultados: "Results", producao: "Production", perfuracao: "Drilling", investimentos: "Investment", contratos: "Contracts and tenders", regulatorio: "Regulation", exploracao: "Exploration", mercado: "Market", fusoes: "M&A", outros: "Other" },
      countries: { BR: "Brazil", AR: "Argentina", CO: "Colombia", GY: "Guyana", SR: "Suriname", PE: "Peru", EC: "Ecuador", BO: "Bolivia", VE: "Venezuela", CL: "Chile", UY: "Uruguay", PY: "Paraguay", TT: "Trinidad and Tobago" }
    }
  };

  var ENV_ORDER = ["onshore", "offshore", "geral"];
  var SUPPLIERS = ["SLB", "Baker Hughes", "Weatherford", "Tenaris", "Confab", "Apolo Tubulars", "Jereh", "Kerui"];
  var ENV_COLOR = { onshore: "var(--env-onshore)", offshore: "var(--env-offshore)", geral: "var(--env-geral)" };
  var CH_ORDER = ["site", "linkedin", "instagram", "youtube", "x"];
  var SCOPES = ["all", "BR", "SA"];
  var PAGE = document.body.getAttribute("data-page");
  var NEWS_URL = "index.html";

  var state = { lang: "en", region: "all", op: "", cat: "", env: "", q: "" };
  var data = { updated_at: null, items: [] };
  var run = null;
  var failed = false;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  try {
    var saved = localStorage.getItem("mr_lang_v2");
    if (saved === "pt" || saved === "en") state.lang = saved;
  } catch (e) { /* storage unavailable */ }

  function $(id) { return document.getElementById(id); }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function t() { return T[state.lang]; }
  function locale() { return state.lang === "pt" ? "pt-BR" : "en-GB"; }
  function parseDay(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function isoDay(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function opName(o) { return o === "Setor" ? t().sector : o; }
  function envOf(it) { return ENV_ORDER.indexOf(it.environment) > -1 ? it.environment : "geral"; }
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function safeUrl(u) { return /^https?:\/\//i.test(u || "") ? u : "#"; }
  function title(it) { return it["title_" + state.lang] || it.title_en || it.title_pt; }
  function summary(it) { return it["summary_" + state.lang] || it.summary_en || it.summary_pt; }
  function rel(it) { return typeof it.relevance === "number" ? it.relevance : 1; }
  function byRank(a, b) { return rel(b) - rel(a) || (a.region === b.region ? 0 : a.region === "BR" ? -1 : 1) || (a.date < b.date ? 1 : a.date > b.date ? -1 : 0); }
  function byDateDesc(a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : byRank(a, b); }
  function topStories(n) {
    if (!data.items.length) return [];
    var last = data.items.reduce(function (m, it) { return it.date > m ? it.date : m; }, "0000-00-00");
    var from = parseDay(last); from.setDate(from.getDate() - 6);
    var cut = isoDay(from);
    return data.items.filter(function (it) { return it.date >= cut; }).sort(byRank).slice(0, n);
  }
  function ext(a, url) { a.href = safeUrl(url); a.target = "_blank"; a.rel = "noopener noreferrer"; return a; }
  function newsLink(key, value) { return NEWS_URL + "?" + key + "=" + encodeURIComponent(value); }
  function fmtStamp(iso, opts) {
    var o = opts || { day: "numeric", month: "long", year: "numeric", hour: "2-digit", minute: "2-digit" };
    o.timeZone = "America/Sao_Paulo";
    return new Intl.DateTimeFormat(locale(), o).format(new Date(iso));
  }

  function chip(cls, text) { return el("span", "chip " + cls, text); }
  function isFocus(it) { return rel(it) === 5; }
  function tagsFor(it) {
    var L = t(), tags = el("div", "tags");
    tags.appendChild(el("span", "op", opName(it.operator)));
    tags.appendChild(chip("ct", L.countries[it.country] || it.country));
    if (SUPPLIERS.indexOf(it.operator) > -1) tags.appendChild(chip("dot supplier", L.supplier));
    if (envOf(it) !== "geral") tags.appendChild(chip("dot " + envOf(it), L.envs[envOf(it)]));
    tags.appendChild(chip("cat", L.cats[it.category] || it.category));
    if (isFocus(it)) tags.appendChild(chip("dot focus", L.focus));
    return tags;
  }
  function sourceLine(it) {
    var L = t(), src = el("p", "src");
    var via = { linkedin: "LinkedIn", instagram: "Instagram", x: "X", youtube: "YouTube" }[it.via];
    src.appendChild(document.createTextNode(L.source + ": " + it.source + (via ? " (" + via + ")" : "") + ", "));
    src.appendChild(ext(el("a", null, L.read), it.url));
    if (it.access === "paywall") src.appendChild(el("span", "lock", "(" + L.paywall + ")"));
    return src;
  }

  /* ---------- Shared chrome ---------- */

  function renderCommon() {
    var L = t();
    document.documentElement.lang = state.lang === "pt" ? "pt-BR" : "en";
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n]"), function (n) {
      n.textContent = L[n.getAttribute("data-i18n")];
    });
    Array.prototype.forEach.call(document.querySelectorAll(".lang button"), function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === state.lang));
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll(".lang button"), function (b) {
    b.addEventListener("click", function () {
      state.lang = b.getAttribute("data-lang");
      try { localStorage.setItem("mr_lang_v2", state.lang); } catch (e) { /* ignore */ }
      renderAll();
    });
  });

  /* ---------- News page ---------- */

  function matches(it, skipRegion) {
    if (!skipRegion && state.region !== "all" && it.region !== state.region) return false;
    if (state.op && it.operator !== state.op) return false;
    if (state.cat && it.category !== state.cat) return false;
    if (state.env && envOf(it) !== state.env) return false;
    if (state.q) {
      var hay = norm([it.title_pt, it.title_en, it.summary_pt, it.summary_en, it.operator, it.source].join(" "));
      if (hay.indexOf(norm(state.q)) === -1) return false;
    }
    return true;
  }
  function readParams() {
    var p = new URLSearchParams(location.search);
    if (p.get("region") === "BR" || p.get("region") === "SA") state.region = p.get("region");
    state.op = p.get("op") || ""; state.cat = p.get("cat") || ""; state.env = p.get("env") || ""; state.q = p.get("q") || "";
  }
  function writeParams() {
    var p = new URLSearchParams();
    if (state.region !== "all") p.set("region", state.region);
    if (state.op) p.set("op", state.op);
    if (state.cat) p.set("cat", state.cat);
    if (state.env) p.set("env", state.env);
    if (state.q) p.set("q", state.q);
    var s = p.toString();
    try { history.replaceState(null, "", location.pathname + (s ? "?" + s : "")); } catch (e) { /* file preview */ }
  }
  function fillSelect(sel, first, keys, labelFn, value) {
    sel.textContent = "";
    var o0 = el("option", null, first); o0.value = ""; sel.appendChild(o0);
    keys.forEach(function (k) { var o = el("option", null, labelFn(k)); o.value = k; sel.appendChild(o); });
    sel.value = value;
    if (sel.value !== value) sel.value = "";
  }
  function regionCounts() {
    var btns = $("regionSeg").querySelectorAll("button");
    ["all", "BR", "SA"].forEach(function (r, i) {
      var n = data.items.filter(function (it) { return matches(it, true) && (r === "all" || it.region === r); }).length;
      if (btns[i]) btns[i].querySelector(".n").textContent = String(n);
    });
  }
  function renderNewsChrome() {
    var L = t();
    $("q").placeholder = L.searchPh;
    if ($("q").value !== state.q) $("q").value = state.q;
    var seg = $("regionSeg"); seg.textContent = "";
    ["all", "BR", "SA"].forEach(function (r) {
      var b = el("button"); b.type = "button";
      b.setAttribute("aria-pressed", String(state.region === r));
      b.appendChild(document.createTextNode(L[r]));
      b.appendChild(el("span", "n", "0"));
      b.addEventListener("click", function () { state.region = r; renderNews(); });
      seg.appendChild(b);
    });
    regionCounts();
    var ops = {}, cats = {}, envs = {};
    data.items.forEach(function (it) { ops[it.operator] = 1; cats[it.category] = 1; envs[envOf(it)] = 1; });
    fillSelect($("opSel"), L.allOps, Object.keys(ops).sort(function (a, b) {
      if (a === "Setor") return 1; if (b === "Setor") return -1; return a.localeCompare(b);
    }), opName, state.op);
    fillSelect($("catSel"), L.allCats, Object.keys(cats).sort(function (a, b) {
      return (L.cats[a] || a).localeCompare(L.cats[b] || b);
    }), function (c) { return L.cats[c] || c; }, state.cat);
    fillSelect($("envSel"), L.allEnvs, ENV_ORDER.filter(function (e) { return envs[e]; }), function (e) { return L.envs[e]; }, state.env);
    var lg = $("legend"); lg.textContent = "";
    var a = el("span", "br"); a.appendChild(el("i")); a.appendChild(document.createTextNode(L.BR)); lg.appendChild(a);
    var s = el("span", "sa"); s.appendChild(el("i")); s.appendChild(document.createTextNode(L.SA)); lg.appendChild(s);
    lg.appendChild(chip("dot onshore", L.envs.onshore)); lg.appendChild(chip("dot offshore", L.envs.offshore));
    lg.appendChild(chip("dot supplier", L.supplier)); lg.appendChild(chip("dot focus", L.focus));
    lg.appendChild(el("span", "hint", L.focusHint));
    var ed = $("edition"); ed.textContent = "";
    if (data.updated_at) {
      ed.appendChild(document.createTextNode(L.updated + " "));
      ed.appendChild(el("strong", null, fmtStamp(data.updated_at)));
    }
  }
  function stateBox(titleText, text, btn, fn) {
    var box = el("div", "state");
    box.appendChild(el("h2", null, titleText));
    box.appendChild(el("p", null, text));
    var b = el("button", null, btn); b.type = "button"; b.addEventListener("click", fn);
    box.appendChild(b);
    return box;
  }
  function renderLog() {
    var L = t(), log = $("log"); log.textContent = "";
    if (failed) { log.appendChild(stateBox(L.errT, L.errP, L.reload, function () { location.reload(); })); return; }
    var list = data.items.filter(function (it) { return matches(it, false); }).sort(byDateDesc);
    if (!list.length) {
      log.appendChild(stateBox(L.emptyT, L.emptyP, L.clear, function () {
        state.region = "all"; state.op = ""; state.cat = ""; state.env = ""; state.q = ""; renderNews();
      }));
      return;
    }
    var monFmt = new Intl.DateTimeFormat(locale(), { month: "short" });
    var wkFmt = new Intl.DateTimeFormat(locale(), { weekday: "long" });
    var current = null, track = null;
    list.forEach(function (it) {
      if (it.date !== current) {
        current = it.date;
        var day = el("section", "day"), lab = el("div", "day-label"), inner = el("div", "inner"), dt = parseDay(it.date);
        inner.appendChild(el("span", "d", dt.getDate() + " " + monFmt.format(dt).replace(".", "")));
        inner.appendChild(el("span", "w", wkFmt.format(dt)));
        lab.appendChild(inner);
        track = el("div", "track");
        day.appendChild(lab); day.appendChild(track);
        log.appendChild(day);
      }
      var art = el("article", "item");
      art.setAttribute("data-region", it.region);
      if (isFocus(it)) art.classList.add("focus");
      art.appendChild(tagsFor(it));
      var h = el("h2"); h.appendChild(ext(el("a", null, title(it)), it.url)); art.appendChild(h);
      art.appendChild(el("p", null, summary(it)));
      art.appendChild(sourceLine(it));
      track.appendChild(art);
    });
  }
  function renderTop() {
    var box = $("top"), ol = $("topList"); ol.textContent = "";
    var filtered = state.region !== "all" || state.op || state.cat || state.env || state.q;
    var list = filtered || failed ? [] : topStories(5);
    box.hidden = !list.length;
    list.forEach(function (it, i) {
      var li = el("li", i === 0 ? "lead" : null); li.setAttribute("data-region", it.region);
      li.appendChild(tagsFor(it));
      li.appendChild(ext(el("a", "t", title(it)), it.url));
      if (i === 0) { li.appendChild(el("p", "sum", summary(it))); li.appendChild(sourceLine(it)); }
      ol.appendChild(li);
    });
  }
  function renderNews() { renderNewsChrome(); renderTop(); renderLog(); writeParams(); }
  function bindNews() {
    $("opSel").addEventListener("change", function (e) { state.op = e.target.value; renderNews(); });
    $("catSel").addEventListener("change", function (e) { state.cat = e.target.value; renderNews(); });
    $("envSel").addEventListener("change", function (e) { state.env = e.target.value; renderNews(); });
    $("q").addEventListener("input", function (e) { state.q = e.target.value.trim(); regionCounts(); renderTop(); renderLog(); writeParams(); });
  }

  /* ---------- Live panel ---------- */

  var live = { scope: "all", auto: !reduce, rot: null, spotT: null, spotIdx: 0, radT: null, radIdx: 0, feedT: null, feedGen: 0 };

  function scoped() { return data.items.filter(function (it) { return live.scope === "all" || it.region === live.scope; }); }
  function countBy(list, fn) {
    var m = {};
    list.forEach(function (it) { var k = fn(it); if (k) m[k] = (m[k] || 0) + 1; });
    return Object.keys(m).map(function (k) { return { k: k, n: m[k] }; }).sort(function (a, b) { return b.n - a.n || a.k.localeCompare(b.k); });
  }
  function grow(fn) { requestAnimationFrame(function () { requestAnimationFrame(fn); }); }
  function countUp(node, to) {
    var from = parseInt(node.textContent, 10) || 0;
    if (reduce || from === to) { node.textContent = String(to); return; }
    var t0 = null;
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / 600);
      node.textContent = String(Math.round(from + (to - from) * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function tiles(list) {
    var L = t(), box = $("tiles");
    var vals = [
      [list.length, L.kStories, "hero"],
      [countBy(list, function (it) { return it.operator === "Setor" ? "" : it.operator; }).length, L.kCompanies, ""],
      [countBy(list, function (it) { return it.country; }).length, L.kCountries, ""],
      [countBy(list, function (it) { return it.source; }).length, L.kSources, ""]
    ];
    if (!box.children.length) {
      vals.forEach(function (v) {
        var d = el("div", "tile" + (v[2] ? " " + v[2] : ""));
        d.appendChild(el("span", "v", "0")); d.appendChild(el("span", "l"));
        box.appendChild(d);
      });
    }
    vals.forEach(function (v, i) {
      countUp(box.children[i].querySelector(".v"), v[0]);
      box.children[i].querySelector(".l").textContent = v[1];
    });
  }
  function bars(box, rows, labelFn, hrefFn) {
    box.textContent = "";
    if (!rows.length) { box.appendChild(el("p", "none", t().noData)); return; }
    var max = Math.max.apply(null, rows.map(function (r) { return r.n; })) || 1;
    rows.forEach(function (r) {
      var row = el(hrefFn ? "a" : "div", "row");
      if (hrefFn) row.href = hrefFn(r.k);
      var label = labelFn(r.k);
      row.appendChild(el("span", "name", label));
      var trk = el("span", "trk"), fill = el("span", "fill");
      trk.appendChild(fill); row.appendChild(trk);
      row.appendChild(el("span", "num", String(r.n)));
      row.title = label + ": " + r.n;
      box.appendChild(row);
      grow(function () { fill.style.width = (r.n ? Math.max(4, Math.round(r.n / max * 100)) : 0) + "%"; });
    });
  }
  function envBar(list) {
    var L = t(), box = $("cEnv"); box.textContent = "";
    if (!list.length) { box.appendChild(el("p", "none", L.noData)); return; }
    var counts = {}; ENV_ORDER.forEach(function (e) { counts[e] = 0; });
    list.forEach(function (it) { counts[envOf(it)]++; });
    var bar = el("div", "seg-bar"), legend = el("div", "legend-d");
    ENV_ORDER.forEach(function (e) {
      if (!counts[e]) return;
      var share = Math.round(counts[e] / list.length * 100);
      var b = el("a", null, share >= 12 ? share + "%" : "");
      b.href = newsLink("env", e); b.style.background = ENV_COLOR[e]; b.style.flexGrow = "0.0001";
      var label = L.envs[e] + ": " + counts[e] + " (" + share + "%)";
      b.title = label; b.setAttribute("aria-label", label);
      bar.appendChild(b);
      grow(function () { b.style.flexGrow = String(counts[e]); });
      var li = el("span"), sw = el("i"); sw.style.background = ENV_COLOR[e];
      li.appendChild(sw); li.appendChild(document.createTextNode(L.envs[e] + " " + counts[e]));
      legend.appendChild(li);
    });
    box.appendChild(bar); box.appendChild(legend);
  }
  function showTip(x, y, value, label) {
    var tip = $("tip"); tip.textContent = "";
    tip.appendChild(el("b", null, value)); tip.appendChild(document.createTextNode(label));
    tip.style.display = "block";
    var w = tip.offsetWidth;
    tip.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, x - w / 2)) + "px";
    tip.style.top = Math.max(8, y - 40) + "px";
  }
  function hideTip() { $("tip").style.display = "none"; }
  function dayCols(list) {
    var L = t(), box = $("cDays"); box.textContent = "";
    if (!data.items.length) { box.appendChild(el("p", "none", L.noData)); return; }
    var last = data.items.reduce(function (m, it) { return it.date > m ? it.date : m; }, "0000-00-00");
    var end = parseDay(last), days = [], N = 14;
    for (var i = N - 1; i >= 0; i--) { var d = new Date(end); d.setDate(end.getDate() - i); days.push(d); }
    var per = {}; list.forEach(function (it) { per[it.date] = (per[it.date] || 0) + 1; });
    var max = 0; days.forEach(function (d) { max = Math.max(max, per[isoDay(d)] || 0); });
    var fmt = new Intl.DateTimeFormat(locale(), { day: "numeric", month: "short" });
    var wrap = el("div", "days"), labelled = false;
    days.forEach(function (d) {
      var n = per[isoDay(d)] || 0, b = el("button"); b.type = "button";
      b.setAttribute("aria-label", fmt.format(d) + ": " + n + " " + (n === 1 ? L.story1 : L.storyN));
      if (n && n === max && !labelled) { b.appendChild(el("span", "top-n", String(n))); labelled = true; }
      var col = el("span", "col" + (n ? "" : " zero")); b.appendChild(col);
      b.addEventListener("pointermove", function (ev) { showTip(ev.clientX, ev.clientY, String(n), fmt.format(d)); });
      b.addEventListener("pointerleave", hideTip);
      b.addEventListener("focus", function () { var r = b.getBoundingClientRect(); showTip(r.left + r.width / 2, r.top, String(n), fmt.format(d)); });
      b.addEventListener("blur", hideTip);
      wrap.appendChild(b);
      grow(function () { col.style.height = (n ? Math.max(4, Math.round(n / max * 52)) : 2) + "px"; });
    });
    var axis = el("div", "days-axis");
    axis.appendChild(el("span", null, fmt.format(days[0])));
    axis.appendChild(el("span", null, fmt.format(days[N - 1])));
    box.appendChild(wrap); box.appendChild(axis);
  }

  function renderScope() {
    var L = t(), seg = $("scopeSeg"); seg.textContent = "";
    SCOPES.forEach(function (s) {
      var b = el("button", null, L[s]); b.type = "button";
      b.setAttribute("aria-pressed", String(live.scope === s));
      b.addEventListener("click", function () { live.scope = s; clearInterval(live.rot); renderScope(); renderKpis(); });
      seg.appendChild(b);
    });
    $("pauseBtn").textContent = live.auto ? L.pause : L.resume;
    document.body.classList.toggle("auto", live.auto);
    document.body.classList.toggle("paused", !live.auto);
  }
  function renderKpis() {
    var L = t(), list = scoped();
    tiles(list);
    bars($("cTopics"), countBy(list, function (it) { return it.category; }).slice(0, 6), function (k) { return L.cats[k] || k; }, function (k) { return newsLink("cat", k); });
    bars($("cCompanies"), countBy(list, function (it) { return it.operator === "Setor" ? "" : it.operator; }).slice(0, 6), function (k) { return k; }, function (k) { return newsLink("op", k); });
    bars($("cCountries"), countBy(list, function (it) { return it.country; }).slice(0, 6), function (k) { return L.countries[k] || k; }, null);
    envBar(list); dayCols(list);
    var ch = {}; list.forEach(function (it) { ch[it.via] = (ch[it.via] || 0) + 1; });
    bars($("cChannels"), CH_ORDER.map(function (c) { return { k: c, n: ch[c] || 0 }; }), function (k) { return L.chs[k]; }, null);
  }
  function renderTicker() {
    var box = $("ticker"); box.textContent = "";
    var list = data.items.slice().sort(byDateDesc).slice(0, 12);
    if (!list.length) return;
    for (var pass = 0; pass < 2; pass++) {
      list.forEach(function (it) {
        var s = el("span"); if (pass) s.setAttribute("aria-hidden", "true");
        s.appendChild(el("b", null, opName(it.operator)));
        s.appendChild(document.createTextNode(title(it)));
        box.appendChild(s);
      });
    }
    box.style.animationDuration = Math.max(40, list.length * 7) + "s";
  }

  /* Spotlight: one story at a time */
  function spotList() { return topStories(10); }
  function renderSpot() {
    var list = spotList(), box = $("spotBody"); box.textContent = "";
    if (!list.length) { box.appendChild(el("p", "none", t().noData)); return; }
    live.spotIdx = (live.spotIdx + list.length) % list.length;
    var it = list[live.spotIdx];
    $("spot").setAttribute("data-region", it.region);
    var inner = el("div", "spot-in");
    inner.appendChild(tagsFor(it));
    var h = el("h3"); h.appendChild(ext(el("a", null, title(it)), it.url)); inner.appendChild(h);
    inner.appendChild(el("p", null, summary(it)));
    inner.appendChild(sourceLine(it));
    box.appendChild(inner);
    $("spotCount").textContent = (live.spotIdx + 1) + " / " + list.length;
    var bar = $("spotBar"); bar.classList.remove("run"); void bar.offsetWidth;
    if (live.auto) bar.classList.add("run");
  }
  function spotStep(d) { live.spotIdx += d; renderSpot(); }
  function spotTimer() {
    clearInterval(live.spotT);
    if (live.auto) live.spotT = setInterval(function () { spotStep(1); }, 8000);
  }

  /* Agent: status, replay of the latest scan, coverage */
  function nextRun(now) {
    if (!run) return null;
    if (run.schedule && run.schedule.type === "interval" && run.schedule.minutes && run.run_at) {
      var step = run.schedule.minutes * 60000, n = new Date(run.run_at).getTime() + step;
      while (n <= now) n += step;
      return n;
    }
    if (run.schedule && (run.schedule.type === "weekdays" || run.schedule.type === "daily") && /^\d\d:\d\d$/.test(run.schedule.time || "")) {
      var everyDay = run.schedule.type === "daily";
      var hh = +run.schedule.time.slice(0, 2), mm = +run.schedule.time.slice(3, 5);
      var sp = new Date(now - 3 * 3600000); /* Brasília is UTC-3, no daylight saving */
      for (var d = 0; d < 8; d++) {
        var cand = Date.UTC(sp.getUTCFullYear(), sp.getUTCMonth(), sp.getUTCDate() + d, hh + 3, mm);
        var wd = new Date(cand - 3 * 3600000).getUTCDay();
        if (cand > now && (everyDay || (wd >= 1 && wd <= 5))) return cand;
      }
    }
    return null;
  }
  function dur(ms) {
    var s = Math.max(0, Math.floor(ms / 1000)), h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
    return ("0" + h).slice(-2) + ":" + ("0" + m).slice(-2) + ":" + ("0" + x).slice(-2);
  }
  function agoText(ms) {
    var m = Math.max(0, Math.floor(ms / 60000)), h = Math.floor(m / 60), d = Math.floor(h / 24);
    var txt = d ? d + " d " + (h % 24) + " h" : h ? h + " h " + (m % 60) + " min" : m + " min";
    return t().ago.replace("{t}", txt);
  }
  function tick() {
    var L = t(), now = Date.now();
    var c = $("clock"); c.textContent = "";
    c.appendChild(document.createTextNode(new Intl.DateTimeFormat(locale(), { day: "numeric", month: "short", year: "numeric", timeZone: "America/Sao_Paulo" }).format(now)));
    c.appendChild(el("b", null, new Intl.DateTimeFormat(locale(), { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false, timeZone: "America/Sao_Paulo" }).format(now)));
    c.appendChild(document.createTextNode(" " + L.clockTz));
    if (!run) return;
    if (run.run_at) {
      $("lastV").textContent = fmtStamp(run.run_at, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
      $("lastS").textContent = agoText(now - new Date(run.run_at).getTime());
    }
    var n = nextRun(now);
    $("nextV").textContent = n ? dur(n - now) : "--:--:--";
    $("nextS").textContent = n ? fmtStamp(n, { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) : "";
  }
  function renderAgent() {
    var L = t(), box = $("agent");
    if (!run) { box.hidden = true; return; }
    box.hidden = false;
    countUp($("searchV"), run.searches || 0);
    countUp($("newV"), run.new_items || 0);
    $("replayLine").textContent = run.run_at ? L.replayOf.replace("{d}", fmtStamp(run.run_at, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })) : "";
    var ul = $("chips"); ul.textContent = "";
    (run.terms || []).forEach(function (term) { ul.appendChild(el("li", null, term)); });
    radarStep(0); startFeed(); tick();
  }
  function radarStep(i) {
    var lis = $("chips").children; if (!lis.length) return;
    live.radIdx = i % lis.length;
    for (var k = 0; k < lis.length; k++) lis[k].classList.toggle("on", k === live.radIdx && live.auto);
  }
  function feedLine(q) {
    var L = t(), li = el("li");
    li.appendChild(el("span", "ch", L.chShort[q.ch] || "Web"));
    li.appendChild(el("span", "q"));
    li.appendChild(el("span", "res"));
    return li;
  }
  function feedResult(li, q) {
    var res = li.querySelector(".res"), n = q.found || 0;
    res.textContent = n ? "+" + n + " " + t().newShort : "0";
    res.classList.toggle("hit", n > 0);
  }
  function startFeed() {
    var L = t(), feed = $("feed"), qs = (run && run.queries) || [];
    clearTimeout(live.feedT); live.feedGen++;
    var gen = live.feedGen;
    feed.textContent = "";
    if (!qs.length) return;
    var doneText = L.scanDone.replace("{n}", run.searches || qs.length).replace("{m}", run.new_items || 0);
    function trim() { while (feed.children.length > 9) feed.removeChild(feed.firstChild); }
    if (!live.auto) {
      qs.slice(-8).forEach(function (q) { var li = feedLine(q); li.querySelector(".q").textContent = q.q; feedResult(li, q); feed.appendChild(li); });
      feed.appendChild(el("li", "done", doneText));
      return;
    }
    var i = 0;
    function nextQuery() {
      if (gen !== live.feedGen) return;
      if (i >= qs.length) {
        feed.appendChild(el("li", "done", doneText)); trim();
        live.feedT = setTimeout(function () { if (gen === live.feedGen) { feed.textContent = ""; i = 0; nextQuery(); } }, 5000);
        return;
      }
      var q = qs[i++], li = feedLine(q), span = li.querySelector(".q"), c = 0;
      feed.appendChild(li); trim(); span.classList.add("typing");
      (function type() {
        if (gen !== live.feedGen) return;
        c += 2; span.textContent = q.q.slice(0, c);
        if (c < q.q.length) { live.feedT = setTimeout(type, 28); return; }
        live.feedT = setTimeout(function () {
          if (gen !== live.feedGen) return;
          span.classList.remove("typing"); feedResult(li, q);
          live.feedT = setTimeout(nextQuery, 650);
        }, 550);
      })();
    }
    nextQuery();
  }

  function setAuto(on) {
    live.auto = on;
    clearInterval(live.rot); clearInterval(live.radT);
    if (on) {
      live.rot = setInterval(function () {
        live.scope = SCOPES[(SCOPES.indexOf(live.scope) + 1) % SCOPES.length];
        renderScope(); renderKpis();
      }, 7000);
      live.radT = setInterval(function () { radarStep(live.radIdx + 1); }, 1300);
    }
    spotTimer(); renderScope(); radarStep(live.radIdx);
    if (run) startFeed();
    renderSpot();
  }
  function renderLive() { renderScope(); renderTicker(); renderKpis(); renderSpot(); renderAgent(); tick(); }
  function bindLive() {
    $("pauseBtn").addEventListener("click", function () { setAuto(!live.auto); });
    $("spotPrev").addEventListener("click", function () { spotStep(-1); spotTimer(); });
    $("spotNext").addEventListener("click", function () { spotStep(1); spotTimer(); });
    setInterval(tick, 1000);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { clearInterval(live.rot); clearInterval(live.radT); clearInterval(live.spotT); }
      else if (live.auto) setAuto(true);
    });
    /* pick up a new scan without reloading the page */
    setInterval(function () {
      if (window.__NEWS__) return;
      Promise.all([getJson("data/news.json"), getJson("data/run.json").catch(function () { return null; })]).then(function (r) {
        var changed = r[0].updated_at !== data.updated_at || (r[1] && run && r[1].run_at !== run.run_at);
        if (!changed) return;
        data = { updated_at: r[0].updated_at || null, items: Array.isArray(r[0].items) ? r[0].items : [] };
        if (r[1]) run = r[1];
        renderLive();
      }).catch(function () { /* keep showing what we have */ });
    }, 300000);
  }

  /* ---------- Li Marcitão, the presenter ---------- */

  var avatar = null, avLang = "en";
  function avatarText() {
    if (!avatar) return;
    var L = t();
    $("liLabel").textContent = L.meet;
    $("liBtn").setAttribute("aria-label", L.meet);
    $("liNote").textContent = L.aiNote;
    $("liClose").textContent = L.close;
  }
  function avatarPlay(lang) {
    avLang = lang;
    var v = $("liVideo"), src = avatar.videos[lang];
    Array.prototype.forEach.call(document.querySelectorAll(".li-langs button"), function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-v") === lang));
    });
    $("liCaption").textContent = (avatar.captions || {})[lang] || "";
    $("liCaption").lang = lang === "zh" ? "zh-CN" : "en";
    if (v.getAttribute("src") !== src) v.setAttribute("src", src);
    v.currentTime = 0;
    var p = v.play(); if (p && p.catch) p.catch(function () { /* the person can press play */ });
  }
  function buildAvatar(cfg) {
    if (!cfg || !cfg.image || !cfg.videos || !/^https?:|^assets\//.test(cfg.image)) return;
    avatar = cfg;
    var btn = el("button", "li-btn"); btn.type = "button"; btn.id = "liBtn";
    var img = el("img"); img.src = cfg.image; img.alt = ""; img.width = 64; img.height = 64;
    btn.appendChild(img); btn.appendChild(el("span", null)).id = "liLabel";
    var dlg = el("dialog", "li-dlg"); dlg.id = "liDlg"; dlg.setAttribute("aria-labelledby", "liName");
    var head = el("div", "li-head");
    head.appendChild(el("h2", null, "Li Marcitão")).id = "liName";
    var close = el("button", "li-close"); close.type = "button"; close.id = "liClose"; head.appendChild(close);
    dlg.appendChild(head);
    var v = el("video"); v.id = "liVideo"; v.controls = true; v.playsInline = true; v.preload = "none"; v.poster = cfg.image;
    dlg.appendChild(v);
    var langs = el("div", "li-langs"); langs.setAttribute("role", "group");
    [["en", "English"], ["zh", "中文"]].forEach(function (p) {
      if (!cfg.videos[p[0]]) return;
      var b = el("button", null, p[1]); b.type = "button"; b.setAttribute("data-v", p[0]);
      b.addEventListener("click", function () { avatarPlay(p[0]); });
      langs.appendChild(b);
    });
    dlg.appendChild(langs);
    dlg.appendChild(el("p", "li-caption")).id = "liCaption";
    dlg.appendChild(el("p", "li-note")).id = "liNote";
    document.body.appendChild(btn); document.body.appendChild(dlg);
    function shut() { v.pause(); if (dlg.open) dlg.close(); }
    btn.addEventListener("click", function () {
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
      avatarPlay(cfg.videos[avLang] ? avLang : "en");
    });
    close.addEventListener("click", shut);
    dlg.addEventListener("click", function (e) { if (e.target === dlg) shut(); });
    dlg.addEventListener("close", function () { v.pause(); });
    avatarText();
  }

  /* ---------- Boot ---------- */

  function renderAll() {
    renderCommon(); avatarText();
    if (PAGE === "news") renderNews();
    if (PAGE === "live") { renderLive(); }
  }
  function getJson(path) {
    return fetch(path + "?t=" + Date.now(), { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error(r.status); return r.json();
    });
  }
  function start(payload, runPayload) {
    data = { updated_at: payload.updated_at || null, items: Array.isArray(payload.items) ? payload.items : [] };
    run = runPayload || null;
    renderAll();
    if (PAGE === "live") setAuto(live.auto);
  }

  if (PAGE === "news") { readParams(); bindNews(); }
  if (PAGE === "live") { bindLive(); }
  renderCommon();
  if (PAGE === "live") tick();

  if (window.__AVATAR__) buildAvatar(window.__AVATAR__);
  else getJson("assets/avatar.json").then(buildAvatar).catch(function () { /* no presenter configured */ });

  if (window.__NEWS__) {
    start(window.__NEWS__, window.__RUN__ || null);
  } else {
    Promise.all([getJson("data/news.json"), getJson("data/run.json").catch(function () { return null; })])
      .then(function (r) { start(r[0], r[1]); })
      .catch(function () { failed = true; renderAll(); });
  }
})();
