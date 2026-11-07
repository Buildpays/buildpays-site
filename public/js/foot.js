// The footer on a phone (TR, 8 Nov 2026: "Footer on phone is taking up soo much space"): the three link columns start
// closed and open on a tap. On a wider screen they are always open and the toggle is not a control (css .f-col summary).
// The query is watched, so a tablet turned wide opens them (a closed column would otherwise stay shut with no control).
const narrow = matchMedia("(max-width:640px)");
const foldFooter = () => { for (const d of document.querySelectorAll("details.f-col")) d.open = !narrow.matches; };
foldFooter();
narrow.addEventListener("change", foldFooter);
