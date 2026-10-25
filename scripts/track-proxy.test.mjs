// node scripts/track-proxy.test.mjs — the two Pages Functions behind the app CRM's tracked links (functions/r/[token].js,
// functions/o/[token].js). Each is driven with a fake `fetch` standing in for the app's crm-track function: the answer passes
// through unchanged (the 302's Location, the GIF), the reader's User-Agent goes along, and any failure still lands the reader on
// the home page (a click) or shows the GIF (an open). No network. Every token here is invented.
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const click = await import(pathToFileURL(path.join(ROOT, "functions", "r", "[token].js")).href);
const open = await import(pathToFileURL(path.join(ROOT, "functions", "o", "[token].js")).href);
const TRACK = "https://oakqmoisxqzxosmhjfzz.supabase.co/functions/v1/crm-track";
const UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148";
const GIF43 = Uint8Array.from([71, 73, 70, 56, 57, 97, 1, 0, 1, 0, 128, 0, 0, 255, 255, 255, 0, 0, 0, 33, 249, 4, 1, 0, 0, 0, 0, 44, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 2, 68, 1, 0, 59]);
let n = 0;
const eq = (a, b, why) => { assert.deepEqual(a, b, why); n++; };

const calls = [];
const stub = (answer) => { globalThis.fetch = async (url, init) => { calls.push({ url: String(url), init }); return typeof answer === "function" ? answer(url, init) : answer; }; };
const req = (p, method = "GET", ua = UA) => new Request(`https://paykicker.com.au${p}`, { method, headers: ua ? { "user-agent": ua } : {} });

// a click: crm-track's 302 passed on
stub(new Response(null, { status: 302, headers: { Location: "https://paykicker.com.au/accountants?utm_content=e1", "Cache-Control": "no-store, private" } }));
let r = await click.onRequest({ request: req("/r/tok987AAAAAAAAAAAAAAAAAAA1"), params: { token: "tok987AAAAAAAAAAAAAAAAAAA1" } });
eq([r.status, r.headers.get("location"), r.headers.get("cache-control")], [302, "https://paykicker.com.au/accountants?utm_content=e1", "no-store, private"], "a click: crm-track's 302 and its Location, unchanged");
eq([calls.at(-1).url, calls.at(-1).init.redirect, calls.at(-1).init.method, calls.at(-1).init.headers["user-agent"]], [`${TRACK}?t=tok987AAAAAAAAAAAAAAAAAAA1&k=click`, "manual", "GET", UA],
  "asked of crm-track with the token, k=click, redirect manual (the 302 is read, not followed), the reader's User-Agent");
r = await click.onRequest({ request: req("/r/x", "HEAD"), params: { token: "a/../b?c=d&k=open" } });
eq([calls.at(-1).url, calls.at(-1).init.method], [`${TRACK}?t=a%2F..%2Fb%3Fc%3Dd%26k%3Dopen&k=click`, "HEAD"], "the token is encoded (it cannot add a parameter); HEAD stays HEAD");

// a click that fails: home
for (const [why, answer] of [["crm-track down", () => { throw new Error("network"); }], ["a 500", new Response("x", { status: 500 })], ["a 302 to a non-https place", new Response(null, { status: 302, headers: { Location: "javascript:alert(1)" } })],
  ["a 200", new Response("ok", { status: 200 })]]) {
  stub(answer);
  r = await click.onRequest({ request: req("/r/tok"), params: { token: "tok" } });
  eq([r.status, r.headers.get("location")], [302, "https://paykicker.com.au/"], `${why}: the reader still lands on the home page`);
}

// an open: the GIF passed on
stub(new Response(GIF43, { status: 200, headers: { "Content-Type": "image/gif" } }));
r = await open.onRequest({ request: req("/o/tok987AAAAAAAAAAAAAAAAAAA9.gif"), params: { token: "tok987AAAAAAAAAAAAAAAAAAA9.gif" } });
let body = new Uint8Array(await r.arrayBuffer());
eq([r.status, r.headers.get("content-type"), body.length, /no-store/.test(r.headers.get("cache-control"))], [200, "image/gif", 43, true], "an open: the 43-byte GIF, never cached");
eq(calls.at(-1).url, `${TRACK}?t=tok987AAAAAAAAAAAAAAAAAAA9&k=open`, "the .gif comes off the token; k=open");
for (const [why, answer] of [["crm-track down", () => { throw new Error("network"); }], ["a 500", new Response("x", { status: 500 })], ["not a GIF", new Response("<html>", { status: 200, headers: { "Content-Type": "text/html" } })]]) {
  stub(answer);
  r = await open.onRequest({ request: req("/o/tok.gif"), params: { token: "tok.gif" } });
  body = new Uint8Array(await r.arrayBuffer());
  eq([r.status, r.headers.get("content-type"), body.length], [200, "image/gif", 43], `${why}: still the GIF (never a broken picture in an email)`);
}
stub(new Response(GIF43, { status: 200, headers: { "Content-Type": "image/gif" } }));
r = await open.onRequest({ request: req("/o/tok.gif", "HEAD"), params: { token: "tok.gif" } });
eq([r.status, (await r.arrayBuffer()).byteLength, calls.at(-1).init.method], [200, 0, "HEAD"], "HEAD: no body, passed on as HEAD (crm-track does not count it)");

console.log(`track-proxy: ${n} passed`);
