// paykicker.com.au/r/<token> — a click on a link in one of PayKicker's sales emails (the app repo's pass 987, 26 Oct 2026).
//
// The app's CRM rewrites each link in a sales email it sends to https://paykicker.com.au/r/<token>. This Pages Function hands the
// request to the app's `crm-track` edge function, which logs the click against the email it came from and answers a 302 to the
// page the link was really for (the address stored with the token, never one from the request). This file passes that answer on
// unchanged, with the reader's User-Agent (so link scanners can be told apart). No secret here: crm-track is public by design —
// a token only ever leads to its own stored page. If anything fails, the reader still lands on the home page.
const TRACK = "https://oakqmoisxqzxosmhjfzz.supabase.co/functions/v1/crm-track";
const HOME = "https://paykicker.com.au/";
const TIMEOUT_MS = 5000;

const home = () => new Response(null, { status: 302, headers: { Location: HOME, "Cache-Control": "no-store, private", "Referrer-Policy": "no-referrer" } });

export async function onRequest({ request, params }) {
  const method = request.method === "HEAD" ? "HEAD" : "GET";
  const token = String(params.token ?? "");
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(`${TRACK}?t=${encodeURIComponent(token)}&k=click`, {
      method, redirect: "manual", signal: ctrl.signal,
      headers: { "user-agent": request.headers.get("user-agent") ?? "" },
    });
    const location = res.headers.get("location");
    if (res.status < 300 || res.status > 399 || !location || !/^https:\/\//.test(location)) return home();
    return new Response(null, { status: res.status, headers: { Location: location, "Cache-Control": res.headers.get("cache-control") ?? "no-store, private", "Referrer-Policy": "no-referrer" } });
  } catch {
    return home();
  } finally {
    clearTimeout(timer);
  }
}
