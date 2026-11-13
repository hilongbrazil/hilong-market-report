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

export default async (req: Request, context: Context) => {
  if (new URL(req.url).pathname.startsWith("/reports/")) return context.next();
  const token = readSession(req);
  if (token) {
    const now = Date.now();
    const cached = ok.get(token);
    if (cached && cached > now) return context.next();
    const exp = expOf(token);
    if (exp > now) {
      const r = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
        headers: { apikey: ANON_KEY, Authorization: `Bearer ${token}` },
      });
      if (r.ok) {
        ok.set(token, Math.min(exp, now + 5 * 60 * 1000));
        if (ok.size > 500) ok.clear();
        return context.next();
      }
    }
  }
  return Response.redirect(LOGIN, 302);
};

