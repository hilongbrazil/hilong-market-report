// Hilong Market Report · porteiro no servidor (Netlify Edge Function), igual ao do Centro (hilong.hilongbrazil.com).
// Antes de entregar qualquer página ou arquivo, confere a sessão do Supabase guardada no cookie "hl-auth"
// (o mesmo login do Centro, compartilhado em .hilongbrazil.com). Sem sessão válida: vai para a área restrita.
// Exceção: /reports/ (PDFs dos últimos 3 dias) fica aberto, porque o Resend busca os arquivos por endereço para anexar ao e-mail.
import type { Context } from "https://edge.netlify.com";

const SUPABASE_URL = "https://wmekochxazvxcghykcgg.supabase.co";
const ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndtZWtvY2h4YXp2eGNnaHlrY2dnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgwNDI4MzUsImV4cCI6MjEwMzYxODgzNX0.jtbf1YjazW25IYOZZyvT3zfuCprMHMZyJ8HE_Ges_H8";
const LOGIN = "https://hilongbrazil.com/#acesso";

// tokens já conferidos nesta instância (evita perguntar ao Supabase a cada arquivo)
const ok = new Map<string, number>();

function readSession(req: Request): string | null {
  const raw = req.headers.get("cookie") || "";
  const jar: Record<string, string> = {};
  for (const part of raw.split(/;\s*/)) {
    const i = part.indexOf("=");
    if (i > 0) jar[part.slice(0, i)] = part.slice(i + 1);
  }
  const n = parseInt(jar["hl-auth.n"] || "0", 10);
  if (!n) return null;
  let s = "";
  for (let i = 0; i < n; i++) {
    const p = jar[`hl-auth.${i}`];
    if (p == null) return null;
    s += decodeURIComponent(p);
  }
  try {
    const j = JSON.parse(s);
    return j.access_token || (j.currentSession && j.currentSession.access_token) || null;
  } catch {
    return null;
  }
}

function expOf(token: string): number {
  try {
    const p = JSON.parse(atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
    return (p.exp || 0) * 1000;
  } catch {
    return 0;
  }
}

// Só entra quem tem o Market News no perfil do Centro (hl_perfis.reports contém "mkt") ou é admin.
// Com login mas sem o Market News no perfil: volta para o Centro de Operações.
const CENTRO = "https://hilong.hilongbrazil.com/";
const denied = new Map<string, number>();

export default async (req: Request, context: Context) => {
  if (new URL(req.url).pathname.startsWith("/reports/")) return context.next();
  const token = readSession(req);
  if (token) {
    const now = Date.now();
    const cached = ok.get(token);
    if (cached && cached > now) return context.next();
    const no = denied.get(token);
    if (no && no > now) return Response.redirect(CENTRO, 302);
    const exp = expOf(token);
    if (exp > now) {
      let r: Response | null = null;
      try {
        r = await fetch(`${SUPABASE_URL}/rest/v1/rpc/hl_meu_acesso`, {
          method: "POST",
          headers: { apikey: ANON_KEY, Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
          body: "{}",
        });
      } catch {
        r = null;
      }
      if (r && r.ok) {
        let a: { perfil?: string; reports?: string[] } | null = null;
        try { a = await r.json(); } catch { a = null; }
        const until = Math.min(exp, now + 5 * 60 * 1000);
        if (a && (a.perfil === "admin" || (Array.isArray(a.reports) && a.reports.includes("mkt")))) {
          ok.set(token, until);
          if (ok.size > 500) ok.clear();
          return context.next();
        }
        denied.set(token, until);
        if (denied.size > 500) denied.clear();
        return Response.redirect(CENTRO, 302);
      }
    }
  }
  return Response.redirect(LOGIN, 302);
};
