// The footer on a phone (TR, 8 Nov 2026: "Footer on phone is taking up soo much space"): the three link columns start
// closed and open on a tap. On a wider screen they are always open and the toggle is not a control (css .f-col summary).
if (matchMedia("(max-width:640px)").matches) for (const d of document.querySelectorAll("details.f-col")) d.open = false;
