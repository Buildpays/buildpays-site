// GA4 bootstrap — was an inline <script> on every page. Moved to a file so the site's
// Content-Security-Policy can drop 'unsafe-inline' for scripts (security audit A24, 7 Sep 2026).
// The async gtag.js tag stays in each page's <head>; it drains this queue whenever it loads.
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag("js", new Date());
gtag("config", "G-4DGX8VDBNH");
