// paykicker.com.au/o/<token>.gif — the 1×1 picture at the end of one of PayKicker's sales emails (the app repo's pass 987,
// 26 Oct 2026). When a mail app shows the email's pictures it fetches this one, and the app's `crm-track` edge function logs an
// open against that email (once per email per hour; opens are approximate — some mail apps fetch every picture on arrival).
// This Pages Function hands the request on with the reader's User-Agent and passes crm-track's answer (a 43-byte transparent GIF,
// never cached) back unchanged. No secret here. If anything fails, it still answers the GIF, so an email never shows a broken
// picture.
const TRACK = "https://oakqmoisxqzxosmhjfzz.supabase.co/functions/v1/crm-track";
const TIMEOUT_MS = 5000;
const GIF = Uint8Array.from([71, 73, 70, 56, 57, 97, 1, 0, 1, 0, 128, 0, 0, 255, 255, 255, 0, 0, 0, 33, 249, 4, 1, 0, 0, 0, 0,
  44, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 2, 68, 1, 0, 59]);
const NO_STORE = "no-store, no-cache, must-revalidate, max-age=0, private";

const gif = (method, body = GIF) => new Response(method === "HEAD" ? null : body, {
  status: 200,
  headers: { "Content-Type": "image/gif", "Content-Length": String(body.byteLength), "Cache-Control": NO_STORE, Pragma: "no-cache", Expires: "0", "X-Content-Type-Options": "nosniff" },
});

export async function onRequest({ request, params }) {
  const method = request.method === "HEAD" ? "HEAD" : "GET";
  const token = String(params.token ?? "").replace(/\.gif$/i, "");
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(`${TRACK}?t=${encodeURIComponent(token)}&k=open`, {
      method, redirect: "manual", signal: ctrl.signal,
      headers: { "user-agent": request.headers.get("user-agent") ?? "" },
    });
    if (res.status !== 200 || !/^image\/gif\b/i.test(res.headers.get("content-type") ?? "")) return gif(method);
    if (method === "HEAD") return gif(method);
    const body = new Uint8Array(await res.arrayBuffer());
    return gif(method, body.byteLength > 0 && body.byteLength <= 1024 ? body : GIF);
  } catch {
    return gif(method);
  } finally {
    clearTimeout(timer);
  }
}
