"""PayKicker Sales sync (Square into MYOB and Xero): two how-to guides and one anonymised case study
(TR, 26 Oct 2026: "Do guides ... can we do a case study without real ... name and figures?").

Rendered by scripts/cfmeu/build_guides.py (it owns the page shell), so a run of that script rewrites these pages too.

Every PayKicker claim here was checked against the app (C:\\buildpays origin/main 9a9fa822, 26 Oct 2026):
  _shared/square/day.js          the day's lines (GST / GST-free sales, surcharges with GST, tips and gift cards no tax) and
                                 the checks (lines = orders, GST = Square's, tenders = orders + tips; a failed day never posts)
  _shared/square/refundTax.js    a refund on the day it was made, carrying the tax of the lines it refunds (pass 939)
  _shared/square/payout.js       a payout = one spend money of what Square kept (fees on the fees tax code, Capital / held on
                                 no tax) + a transfer from Square clearing to the bank; fees on the shop's job
  _shared/square/autosetup.js    "Set it up for me": the account names (Square Sales, Square Fees ...) and their tax roles
  _shared/square/postingStart.js when a shop starts posting: Not yet / From today / From a date I choose
  fixtures/country/au/golden/au-{myob,xero}-square-{day,payout}.json   the accounts and tax codes as they post
  app/src/help/guides.js         the set-up steps (Connect MYOB, Connect Square, Before posting, Set it up for me, payouts bank
                                 and the start date)
Prices are the site's own (/integrations, /pricing): free up to 60 orders a month across every shop, $9.99 up to 500,
$29.99 unlimited, inc GST, monthly, any number of shops.

Every general accounting rule carries the official page it came from, read on CHECKED (ATO, Square AU, MYOB AU, Xero).
Where a rule could not be confirmed it is left out or handed to the reader's accountant.

The case study: the figures are the owner's (TR, 26 Oct 2026), rounded, and the business is not named. Never add a figure,
a place, a trade, a product or a quote to it.
"""
import json

CHECKED = "26 October 2026"
CHECKED_ISO = "2026-10-26"
PUBLISHED = "2026-10-26"
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg>'

ALL = {
    "myob": ("/guides/square-to-myob", "How to get Square sales into MYOB"),
    "fees": ("/guides/square-fees-gst-myob-xero", "Square fees, tips, surcharges and GST in MYOB and Xero"),
    "case": ("/guides/square-myob-retailer-case-study", "Case study: a Melbourne retailer with two shops on Square and MYOB"),
    "gst": ("/guides/mixed-gst-invoices", "Invoices with GST and GST-free items"),
    "sync": ("/integrations#square-myob", "Square sales sync: what it posts"),
    "delivery": ("/delivery-payouts", "Uber Eats and DoorDash payouts"),
}

SIGNUP_MYOB = "https://app.paykicker.com.au/signup?for=square&amp;via=myob"
SIGNUP_ANY = "https://app.paykicker.com.au/signup?for=square"

PRICE = ("Free up to 60 orders a month across all your shops, then $9.99 a month up to 500 orders and $29.99 a month for "
         "unlimited orders, GST included, any number of shops, billed monthly.")

INDEP = ("PayKicker is independent software and is not affiliated with or endorsed by Square, MYOB or Xero. Square is a trademark "
         "of Block, Inc., MYOB is a trademark of MYOB Technology Pty Ltd and Xero is a trademark of Xero Limited. This page is general "
         "information, not tax advice: check your own GST treatment with your accountant.")

# The official pages behind the general rules (read on CHECKED).
SRC = {
    "myob_square": ("MYOB: Connect your Square account to MYOB", "https://www.myob.com/au/support/myob-business/inventory/connect-your-square-account-to-myob"),
    "myob_codes": ("MYOB: Tax codes", "https://www.myob.com/au/support/myob-business/accounting/financial-control/accounts-list/gst-codes"),
    "sq_fees": ("Square AU: Learn about Square's fees", "https://squareup.com/help/au/en/article/5068-learn-about-square-s-fees"),
    "ato_vouchers": ("ATO: GST and vouchers", "https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/in-detail/rules-for-specific-transactions/gst-and-vouchers"),
    "ato_surcharge": ("ATO: GSTR 2014/2, GST treatment of credit card surcharges", "https://www.ato.gov.au/law/view/document?docid=GST%2FGSTR20142%2FNAT%2FATO%2F00001"),
    "ato_tips": ("ATO: GST issues register, restaurant tips", "https://www.ato.gov.au/law/view/document?docid=GII%2FGSTIITH9%2FNAT%2FATO%2F00001"),
    "ato_adjust": ("ATO: When to make adjustments", "https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/completing-your-bas-for-gst/making-adjustments-on-your-activity-statements/when-to-make-adjustments"),
    "ato_credit": ("ATO: When you can claim a GST credit", "https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/claiming-gst-credits/when-you-can-claim-a-gst-credit"),
    "xero_types": ("Xero Developer: Australian tax types", "https://developer.xero.com/documentation/api/accounting/types"),
}


def link(key):
    path, text = ALL[key]
    return f'<a href="{path}">{text}</a>'


def related(*keys):
    return " &middot; ".join(link(k) for k in keys)


def ext(key):
    t, u = SRC[key]
    return f'<a href="{u}" rel="noopener">{t}</a>'


def sources(items):
    """The sources section at the bottom of a guide: [(key, what it supports), ...]."""
    lis = "\n".join(f"        <li>{ext(k)}: {why}</li>" for k, why in items)
    return (f"      <h2>Sources</h2>\n      <p class=\"src\">Read {CHECKED}. The general rules on this page come from these official pages; how PayKicker posts each piece comes from the app itself.</p>\n"
            f"      <ul>\n{lis}\n      </ul>")


def table(head, rows, total=None):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "\n".join("        <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    if total:
        body += "\n        <tr>" + "".join(f"<td><b>{c}</b></td>" if c else "<td></td>" for c in total) + "</tr>"
    return f'      <div class="tbl-wrap"><table class="tbl fold">\n        <thead><tr>{th}</tr></thead>\n        <tbody>\n{body}\n        </tbody>\n      </table></div>'


def ld_page(path, headline, desc, faq, faq_ld):
    art = {
        "@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc,
        "url": "https://paykicker.com.au" + path, "datePublished": PUBLISHED, "dateModified": CHECKED_ISO, "inLanguage": "en-AU",
        "articleSection": "Guides",
        "author": {"@id": "https://paykicker.com.au/#organization"}, "publisher": {"@id": "https://paykicker.com.au/#organization"},
        "mainEntityOfPage": "https://paykicker.com.au" + path,
        "about": {"@type": "SoftwareApplication", "name": "PayKicker Square sales sync", "url": "https://paykicker.com.au/integrations#square-myob",
                  "applicationCategory": "BusinessApplication", "operatingSystem": "Web"},
    }
    crumbs = [("PayKicker", "/"), ("Guides", "/guides/"), (headline, path)]
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://paykicker.com.au" + u} for i, (n, u) in enumerate(crumbs)]}
    out = ['<script type="application/ld+json">\n' + json.dumps(art, indent=2, ensure_ascii=False) + "\n</script>",
           '<script type="application/ld+json">\n' + json.dumps(bc, indent=2, ensure_ascii=False) + "\n</script>"]
    if faq:
        out.append(faq_ld(faq))
    return "\n".join(out)


def cta(h2, lead, href, rel, price=True):
    tail = f" {PRICE} Uber Eats and DoorDash payouts are included at no extra charge." if price else ""
    return f'''      <h2>{h2}</h2>
      <p>{lead}{tail}</p>
      <div class="cta-act"><a class="btn go big" href="{href}" rel="noopener">Start free</a><a href="/integrations#square-myob">What it posts and prices</a></div>
      <p class="related">Related: {rel}</p>
      <p class="indep">{INDEP}</p>'''


# What PayKicker does, said once so every page says it the same way.
PK_CHECK = ("Before a day posts, PayKicker checks it against Square: the lines must add up to Square's own order totals, the GST must equal "
            "Square's GST, and the payments must equal what the orders asked for. Every day is matched to Square's own totals to the cent. "
            "A day that does not add up is held with the reason and never posted.")


def build(h):
    page, section, head_section, faq_ld, faq_html = h["page"], h["section"], h["head_section"], h["faq_ld"], h["faq_html"]
    built = []

    def emit(key, title, og, desc, lede, extra, sections, faq, src_items, try_block, toc=None):
        path = ALL[key][0]
        body = head_section("Guides", ALL[key][1] if key != "case" else CASE_H1, lede, toc, extra)
        for sid, inner in sections:
            body += section("", "", sid, inner)
        if faq:
            body += section("", "", "faq", "      <h2>Questions</h2>\n" + faq_html(faq))
        if src_items:
            body += section("", "", "sources", sources(src_items))
        body += section("", "", "try", try_block)
        page(path, title, og, desc, ld_page(path, og, desc, faq, faq_ld), body)
        built.append((path, og))

    written = f'  <p class="note">Written {CHECKED}.</p>\n'

    # ------------------------------------------------------------------ Guide 1: Square sales into MYOB
    myob_faq = [
        ("Can Square connect to MYOB?",
         "Yes, through an app. MYOB's own help connects Square through a partner app rather than a built-in feed. PayKicker is one way: it posts each Square shop's day into MYOB every night, with each payout and Square's fees."),
        ("How do I record Square sales in MYOB by hand?",
         "Once a day for each shop: one tax-inclusive entry with GST sales on the GST code, GST-free sales on FRE, card surcharges on their own income account, tips and gift cards sold on N-T to liability accounts, and refunds as negative lines. The card total goes into a Square clearing account and the cash into your cash account. When Square pays out, its fees come out of the clearing account and the deposit is a transfer to your bank."),
        ("Where do Square's fees go in MYOB?",
         "On an expense account such as Square Fees, on the GST code, when Square pays out. Square takes its fees before it transfers the money, so the deposit is the card takings less the fees. Square gives you a monthly tax invoice for its fees in the Square Dashboard."),
        ("Can each shop have its own job in MYOB?",
         "Yes. PayKicker posts each shop's day as its own sales invoice with every line on that shop's job, and puts the shop's Square fees on the same job, so each shop has its own figures in MYOB."),
        ("What if some days are already in MYOB?",
         "Tell PayKicker when you set up. If another app or a bookkeeper has been entering your Square sales, it looks in MYOB for the last day already there, and you choose the first day it posts. A day or payout already in MYOB is never posted again."),
        ("How much does it cost?",
         "Free up to 60 orders a month across all your shops, $9.99 a month up to 500 orders and $29.99 a month for unlimited orders, GST included, any number of shops, billed monthly."),
    ]
    myob_toc = [("", "why", "Why MYOB needs a link"), ("", "manual", "The manual way"), ("", "wrong", "What goes wrong"),
                ("", "auto", "The automatic way"), ("", "setup", "Set up in minutes"), ("", "price", "What it costs"),
                ("", "faq", "Questions"), ("", "sources", "Sources")]
    emit("myob",
         "How to Get Square Sales into MYOB: by Hand or Every Night Automatically | PayKicker",
         "How to get Square sales into MYOB",
         "How to record Square sales in MYOB: the daily sales entry, a Square clearing account and the payouts by hand, what goes wrong with fees, refunds, tips, GST and two shops, and how to post every day automatically.",
         "Square knows every sale. MYOB needs to know them too, in a shape your BAS and your bank reconciliation can use: sales by GST code, the card money Square is holding, the cash, and what Square kept when it paid you. Here is how to do it by hand, where it usually goes wrong, and how to have it posted every night.",
         written,
         [("why", '''      <h2>Why MYOB needs a link to Square</h2>
      <p>Square keeps your sales and MYOB keeps your books, and nothing moves between them unless something connects them. MYOB's own help connects Square through a partner app rather than a built-in feed. If your Square account isn't connected to MYOB, someone has to enter every day's takings from Square's reports.</p>
      <p>The sales are only half of it. Square takes its processing fees out before it transfers your money, so the deposit that reaches the bank is the card takings less the fees, and it lands later than the sale. MYOB needs both sides, the day's sales and the payout, or the bank never reconciles.</p>'''),
          ("manual", '''      <h2>The manual way: a daily entry, a clearing account and the payouts</h2>
      <ol>
        <li><b>Set up the accounts once.</b> A bank-type account for the card money Square is holding (often called Square Balance or Square clearing), an income account for sales and one for card surcharges, liability accounts for tips owed to staff and for gift cards sold, and an expense account for Square's fees. Two shops? A job for each.</li>
        <li><b>Each day, open Square's sales summary for each shop.</b> You need the sales with GST, the GST-free sales, surcharges, tips, gift cards sold and redeemed, refunds, and how it was paid: card, cash, gift card.</li>
        <li><b>Enter one tax-inclusive entry for the day.</b> One way is a sales invoice to a customer called Square, one per shop: GST sales on the GST code, GST-free sales on FRE, surcharges on their income account, tips and gift cards sold on N-T to their liability accounts, refunds and gift cards redeemed as negative lines, every line on the shop's job.</li>
        <li><b>Record how it was paid.</b> The card total into the Square clearing account, the cash into your cash account.</li>
        <li><b>When Square pays out, settle it.</b> Square's fees come out of the clearing account to the fees account, on the GST code; the deposit is a transfer from the clearing account to your bank.</li>
        <li><b>Check the clearing account.</b> It should hold only card takings Square has not paid out yet. If it drifts, a day or a payout is missing or wrong.</li>
      </ol>'''),
          ("wrong", f'''      <h2>What goes wrong</h2>
      <ul>
        <li><b>Fees.</b> Entering the bank deposit as the day's sales understates your sales and loses the fees, and the GST on them. Square charges its fees on the whole of each transaction, GST and tip included, and takes them out before it pays you, so the deposit is never the sales figure.</li>
        <li><b>Refunds.</b> A refund belongs to the day it was given, carrying the GST of what was refunded. The ATO treats a refund for a returned sale as an adjustment in the period you become aware of it, so last week's figures stay as they were. Putting every refund on the GST code overstates the GST credit when the item was GST-free.</li>
        <li><b>Tips.</b> Entered as sales, they inflate your income and your GST. The ATO's view is that a voluntary tip passed on to staff is not part of the price of the sale, so it belongs in a liability until it is paid out to staff.</li>
        <li><b>GST.</b> One sales line on the GST code for a day that included GST-free items overstates the GST you owe. Square records the tax on each item; the entry needs the GST and GST-free totals apart. (The same split for supplier bills: {link("gst")}.)</li>
        <li><b>Gift cards.</b> Selling a gift card is not a sale for GST: the ATO treats a card that can be spent on a range of goods as a face value voucher, with the GST on the sale when it is spent. Counting it as income when sold, and again when spent, counts the same sale twice.</li>
        <li><b>Two shops.</b> One combined entry loses which shop earned what and which shop's fees were paid. An entry per shop, each on its own job, keeps each shop's figures.</li>
      </ul>
      <p>The {link("fees")} guide works through an example day line by line.</p>'''),
          ("auto", f'''      <h2>The automatic way, with PayKicker</h2>
      <p>PayKicker reads each Square shop's day every night and posts it into MYOB as one tax-inclusive sales invoice per shop, with the payments, every line on the shop's job. MYOB stays your books; PayKicker only reads from Square and never moves money.</p>
      <ul>
        <li><b>Checked before it posts.</b> {PK_CHECK}</li>
        <li><b>Each piece on its own account.</b> GST sales on GST and GST-free sales on FRE, card surcharges on their own income account, tips and gift cards sold on N-T to their own liability accounts, gift cards redeemed off the gift card liability, and discounts on their own line if your file keeps a discounts account.</li>
        <li><b>Refunds on the day they were given</b>, carrying the GST of the items refunded.</li>
        <li><b>Card into Square clearing, cash into your cash account.</b></li>
        <li><b>Each Square payout settled.</b> What Square kept goes in as one spend money out of Square clearing: its fees on your fees account with their GST, and a Square Capital repayment or funds held on their own accounts with no GST. The payout is a transfer to your bank. The fees go on the shop's job too.</li>
        <li><b>Nothing posts twice.</b> PayKicker looks for each entry in MYOB before it writes it, so a retry never doubles, and a day already in MYOB (typed in, or posted by another app) is never posted again.</li>
        <li><b>Sales by category, if you want it.</b> Send a Square category, such as food or drinks, to its own income account; the invoice total and GST do not change.</li>
        <li><b>Uber Eats and DoorDash too.</b> Each weekly payout posts with the commission, fees, refunds, tips and GST on their own lines: {link("delivery")}.</li>
      </ul>'''),
          ("setup", '''      <h2>Set up in minutes</h2>
      <ol>
        <li><b>Start free and connect MYOB.</b> Sign up with MYOB and connect your MYOB file.</li>
        <li><b>Connect Square.</b> Sign in to Square and press Allow. PayKicker only reads from Square.</li>
        <li><b>Say whether anything posted your Square sales before.</b> If another app or a bookkeeper did, PayKicker looks in MYOB for the last day already there, so nothing is posted twice.</li>
        <li><b>Press Set it up for me on each shop.</b> PayKicker finds the Square accounts in your MYOB file, or makes the missing ones after asking, and finds the shop's customer and job. Your bookkeeper can change any account.</li>
        <li><b>Pick the bank Square pays into, and when posting starts.</b> PayKicker suggests the bank account from Square. For the start, pick <em>Not yet</em> (it reads every day so you can check first, and posts nothing), <em>From today</em>, or <em>From a date I choose</em>. Then switch the shop on.</li>
      </ol>'''),
          ("price", f'''      <h2>What it costs</h2>
      <p>{PRICE} Orders are counted across every connected shop. Uber Eats and DoorDash payouts are included at no extra charge. <a href="/pricing#square">Every plan on one page</a>.</p>''')],
         myob_faq,
         [("myob_square", "MYOB connects Square through a partner app"),
          ("sq_fees", "Square deducts its fees before each transfer, from the total of each transaction including tax and tip"),
          ("ato_adjust", "a refund for a returned sale is an adjustment"),
          ("ato_tips", "a voluntary tip passed on to staff is not part of the price"),
          ("ato_vouchers", "gift cards as face value vouchers, GST when redeemed"),
          ("myob_codes", "the GST, FRE and N-T codes")],
         cta("Post your Square days into MYOB every night", "Connect MYOB and Square, press Set it up for me on each shop, and start free: up to 60 orders a month cost nothing.", SIGNUP_MYOB,
             related("fees", "case", "sync", "delivery"), price=False),
         myob_toc)

    # ------------------------------------------------------------------ Guide 2: fees, tips, surcharges and GST
    pieces = table(["What", "Where it goes", "GST", "MYOB code", "Xero tax rate"], [
        ["Sales of taxable items", "Sales (income)", "1/11 of the GST-inclusive price", "GST", "GST on Income"],
        ["GST-free sales", "Sales (income)", "None", "FRE", "GST Free Income"],
        ["Card surcharges", "Card surcharges (income)", "Follows the sale it is charged on", "GST on a taxable sale", "GST on Income on a taxable sale"],
        ["Tips", "Tips owed to staff (liability)", "None on a voluntary tip passed on to staff", "N-T", "BAS Excluded"],
        ["Gift cards sold", "Gift cards (liability)", "None when sold", "N-T", "BAS Excluded"],
        ["Gift cards redeemed", "Off the gift card liability; what was bought is a sale", "On the sale, when the card is spent", "N-T", "BAS Excluded"],
        ["Refunds", "Off sales, on the day given", "Reduces GST by the tax of what was refunded", "GST or FRE", "GST on Income or GST Free Income"],
        ["Square's fees", "Fees (expense)", "A GST credit, with Square's tax invoice", "GST", "GST on Expenses"],
        ["Square Capital repayments, funds held", "A loan or holding account", "None", "N-T", "BAS Excluded"],
        ["The payout", "A transfer from Square clearing to your bank", "None", "Transfer", "Transfer"],
    ])
    ex_day = table(["Example: what happened in Square", "Amount inc GST", "GST in it"], [
        ["Sales of taxable items", "$1,320.00", "$120.00"],
        ["GST-free sales", "$180.00", "$0.00"],
        ["Card surcharges", "$11.00", "$1.00"],
        ["Tips", "$40.00", "$0.00"],
        ["Gift cards sold", "$100.00", "$0.00"],
        ["Refund of a taxable sale", "&minus;$22.00", "&minus;$2.00"],
        ["Paid for with gift cards (the goods are in the sales above)", "$50.00", "$0.00"],
    ])
    ex_inv = table(["Example: line on the day's invoice", "Account", "MYOB", "Xero", "Amount"], [
        ["Sales (GST)", "Square Sales", "GST", "GST on Income", "$1,320.00"],
        ["Sales (GST-free)", "Square Sales", "FRE", "GST Free Income", "$180.00"],
        ["Card surcharges", "Square Card Surcharges", "GST", "GST on Income", "$11.00"],
        ["Tips", "Square Tips (liability)", "N-T", "BAS Excluded", "$40.00"],
        ["Gift cards sold", "Square Gift Cards (liability)", "N-T", "BAS Excluded", "$100.00"],
        ["Refunds (GST)", "Square Sales", "GST", "GST on Income", "&minus;$22.00"],
        ["Gift cards redeemed", "Square Gift Cards (liability)", "N-T", "BAS Excluded", "&minus;$50.00"],
    ], total=["Invoice total", "", "", "", "$1,579.00"])
    ex_pay = table(["Example: the payout", "From and to", "MYOB", "Xero", "Amount"], [
        ["Square fees (spend money)", "Square Fees, out of Square Balance", "GST", "GST on Expenses", "$22.00"],
        ["The payout (transfer)", "Square Balance to your bank", "None (a transfer)", "None (a transfer)", "$1,328.00"],
    ])
    fees_faq = [
        ("Is there GST on Square's fees?",
         "Square gives you a monthly GST tax invoice for its processing fees in the Square Dashboard, on its Tax invoices page. If you are registered for GST, that invoice supports the GST credit on the fees; the ATO requires a tax invoice to claim a credit on a purchase over $82.50. Check the claim with your accountant."),
        ("Do I charge GST on tips?",
         "Not on a voluntary tip that is passed on to your staff: the ATO's view is that it is not part of the price of the sale, as long as you keep records showing it went to staff. A tip the business keeps is part of the price and carries GST. PayKicker posts tips with no GST to a tips liability account."),
        ("Is a card surcharge subject to GST?",
         "It follows the sale. The ATO treats a merchant's card surcharge as part of the price of what was sold, so a surcharge on a taxable sale carries GST and a surcharge on a GST-free sale does not."),
        ("When is GST paid on a gift card?",
         "When it is spent, not when it is sold. The ATO treats a gift card that can be spent on a range of goods as a face value voucher: selling it for its face value is not a taxable sale, and GST is accounted for when it is redeemed for taxable goods. Until then it is a liability."),
        ("Which day does a refund belong to?",
         "The day it was given. The ATO treats a refund for a returned sale as an adjustment, generally reported in the period you become aware of it, so last week's figures stay as they were and the refund reduces this period's GST by the tax on what was refunded."),
        ("Why doesn't my Square payout match my sales?",
         "Because the payout is the card takings less Square's fees, and less any Square Capital repayment or funds Square holds, paid after the sale. Cash takings and gift card redemptions never pass through it."),
    ]
    fees_toc = [("", "pieces", "Where each piece belongs"), ("", "rules", "The rules behind it"), ("", "example", "An example day"),
                ("", "books", "MYOB and Xero"), ("", "pk", "How PayKicker posts it"), ("", "faq", "Questions"), ("", "sources", "Sources")]
    emit("fees",
         "Square Fees, Tips, Surcharges and GST in MYOB and Xero | PayKicker",
         "Square fees, tips, surcharges and GST in MYOB and Xero",
         "Where each part of a Square day belongs in MYOB or Xero: sales, GST, GST-free sales, tips, card surcharges, gift cards, refunds, Square's fees and the payout, with an example day and the tax code for each.",
         "A Square day is more than its sales. Tips, card surcharges, gift cards, refunds and Square's fees each have their own place in the books and their own GST treatment, and the payout that reaches your bank is none of them on its own. Here is where each piece goes in MYOB and Xero, with an example day worked through.",
         written,
         [("pieces", "      <h2>Where each piece belongs</h2>\n      <p>One line per piece of a Square day, the account it belongs on, its GST, and the code MYOB and Xero use for it. The rules behind each are set out below the table.</p>\n" + pieces),
          ("rules", '''      <h2>The rules behind it</h2>
      <h3>Tips</h3>
      <p>The ATO's view is that a voluntary tip passed on to staff is not part of the price of the sale, so there is no GST on it, as long as you keep records showing the tips went to staff. A tip the business keeps, or a fixed amount charged as a service charge, is part of the price. Until tips are paid out they are money you owe your staff, which is why they sit in a liability account. How they reach your staff through payroll is a question for your accountant.</p>
      <h3>Card surcharges</h3>
      <p>The ATO treats a merchant's card surcharge as part of the price of what was sold. Its GST follows that sale: a surcharge on a taxable sale is taxable, a surcharge on a GST-free sale is GST-free. Keeping surcharges on their own income account shows what they bring in against what Square charges you.</p>
      <h3>Gift cards</h3>
      <p>A gift card that can be spent on a range of your goods is what the ATO calls a face value voucher. Selling one for its face value is not a taxable sale, so there is no GST when it is sold; GST is accounted for when the card is spent on taxable goods. Until then the card is a liability. If cards expire unused, ask your accountant: the ATO has a rule for that too.</p>
      <h3>Refunds</h3>
      <p>A refund for a returned sale is what the ATO calls an adjustment, generally reported in the period you become aware of it. So a refund belongs to the day it was given, not to the day of the original sale, and it reduces GST by the tax on what was refunded: none for a GST-free item.</p>
      <h3>Square's fees</h3>
      <p>Square charges its processing fees on the whole of each transaction, GST and tip included, takes them out before it transfers your money, and gives you a monthly GST tax invoice for them in the Square Dashboard under Account &amp; Settings &gt; Tax invoices. If you are registered for GST, the GST on the fees is a credit, and the ATO requires a tax invoice to claim a credit on a purchase over $82.50; Square's monthly invoice is that record. Check the claim with your accountant.</p>
      <h3>The payout</h3>
      <p>A payout is not income. It is money moving from the card balance Square holds for you to your bank, after Square has kept its fees and anything else it deducts, such as a Square Capital repayment. In the books it is a transfer out of a Square clearing account, and that account's balance is the card money Square has not paid out yet.</p>'''),
          ("example", "      <h2>An example day</h2>\n      <p>Made-up figures for one shop's day, labelled Example throughout. Not a real business.</p>\n" + ex_day +
           "\n      <p>Paid: $1,350.00 by card (after the $22.00 refund went back to a card), $229.00 in cash and $50.00 with gift cards.</p>\n"
           "      <h3>The day's sales entry</h3>\n      <p>One tax-inclusive invoice for the shop's day, every line on the shop's job:</p>\n" + ex_inv +
           "\n      <p>Paid by two payments: $1,350.00 of card into Square Balance (the Square clearing account) and $229.00 of cash into your cash account. The $50.00 spent with gift cards is not a payment: it comes off the gift card liability, and what was bought is already in the sales. GST on the day: $120.00 + $1.00 &minus; $2.00 = $119.00.</p>\n"
           "      <h3>When Square pays out</h3>\n      <p>Square pays out the $1,350.00 of card takings less $22.00 of fees, $2.00 of which is GST:</p>\n" + ex_pay +
           "\n      <p>Square Balance takes $1,350.00 in and $22.00 and $1,328.00 out, so it is back to nothing, and the $1,328.00 matches the line on your bank statement. The $119.00 of GST on sales and the $2.00 credit on the fees are this shop's Square side only; your BAS also has every other sale and purchase.</p>"),
          ("books", f'''      <h2>MYOB and Xero: the same entries in each one's words</h2>
      <h3>In MYOB</h3>
      <p>The day is a tax-inclusive sales invoice to a customer for the shop, each line on the shop's job. Card and cash are customer payments into Square clearing (a Bank account) and your cash account. The payout is a spend money for what Square kept and a transfer money to your bank. MYOB's codes are GST, FRE (GST-free) and N-T (not reportable on the BAS).</p>
      <h3>In Xero</h3>
      <p>The day is a tax-inclusive sales invoice for the shop, each line on the shop's option in your jobs tracking category. Card and cash are payments into Square clearing (a BANK account) and your cash account. The payout is a spend money for what Square kept and a bank transfer to your bank. Xero's tax rates are GST on Income, GST Free Income, GST on Expenses, GST Free Expenses and BAS Excluded.</p>
      <p>The detail of what each file needs, the permissions and the accounts, is on {link("sync")}.</p>'''),
          ("pk", f'''      <h2>How PayKicker posts each one</h2>
      <p>PayKicker posts the shape above into MYOB or Xero every night, one shop at a time. Press Set it up for me and it finds or makes the accounts with these names: Square Sales, Square Discounts, Square Card Surcharges, Square Tips, Square Gift Cards, Square Balance, Square Cash Clearing and Square Fees, plus the ones only a payout needs, such as Square Loan Repayments and Square Held Funds. It never makes an account whose name already exists.</p>
      <ul>
        <li><b>Sales</b> on the GST code or the GST-free code, as Square recorded the tax on each item. A discount is already off each line; if your file keeps a discounts account, the sales post before discount and the discount as its own line.</li>
        <li><b>Card surcharges</b> on their own income account, on the GST code, with the GST Square recorded on them. If much of what you surcharge is GST-free, ask your accountant how the surcharge should be split.</li>
        <li><b>Tips</b> with no GST to the tips liability account.</li>
        <li><b>Gift cards sold</b> to the gift card liability with no GST; <b>gift cards redeemed</b> come off it.</li>
        <li><b>Refunds</b> on the day they were given, carrying the tax of the items refunded.</li>
        <li><b>Cash rounding</b> on its own GST-free line, so cash days add up.</li>
        <li><b>Each payout</b>: Square's fees on Square Fees with their GST; a Square Capital repayment or funds held on their own accounts with no GST; the payout as a transfer to your bank. The fees go on the shop's job.</li>
      </ul>
      <p>{PK_CHECK} At the month's end there is a GST summary of the Square side: the GST on sales and on Square's fees.</p>''')],
         fees_faq,
         [("ato_tips", "voluntary tips passed on to staff are not consideration; tips kept by the business are"),
          ("ato_surcharge", "a merchant's card surcharge is part of the price of the sale and follows its GST treatment"),
          ("ato_vouchers", "face value vouchers: no GST when sold for face value, GST when redeemed; unredeemed vouchers"),
          ("ato_adjust", "a refund for a returned sale is an adjustment event"),
          ("sq_fees", "fees deducted before each transfer, from the total including tax and tip; monthly GST invoices under Account &amp; Settings &gt; Tax invoices"),
          ("ato_credit", "a tax invoice is needed to claim a GST credit on a purchase over $82.50"),
          ("myob_codes", "MYOB's GST, FRE and N-T codes"),
          ("xero_types", "Xero's Australian tax rates: GST on Income, GST Free Income, GST on Expenses, GST Free Expenses, BAS Excluded")],
         cta("Have every piece posted for you", "Connect MYOB or Xero and Square, and each shop's day posts in this shape every night.", SIGNUP_ANY,
             related("myob", "case", "gst", "sync")),
         fees_toc)

    # ------------------------------------------------------------------ Case study (anonymised; TR's figures, rounded)
    case_tiles = '''  <div class="tiles">
    <div class="tile"><b>200<small>a day</small></b><span class="cap">Around 200 orders a day across both shops</span></div>
    <div class="tile"><b>3,000</b><span class="cap">Close to 3,000 orders in its first two weeks</span></div>
    <div class="tile"><b>2<small>shops</small></b><span class="cap">Each shop on its own job in MYOB</span></div>
    <div class="tile"><b>Nightly</b><span class="cap">Posting to MYOB automatically since mid-October 2026</span></div>
  </div>
''' + written
    emit("case",
         "Case Study: a Melbourne Retailer With Two Shops on Square and MYOB | PayKicker",
         "Case study: a Melbourne retailer with two shops on Square and MYOB",
         "A Melbourne retailer with two shops on Square and MYOB went from entering daily takings by hand to posting automatically every night: around 200 orders a day, each shop on its own job, every Square payout settled with its fees.",
         "Two shops on Square, one MYOB file, and every day's takings entered from Square's reports by hand. Since mid-October 2026 each shop's day has posted into MYOB automatically every night.",
         case_tiles,
         [("before", f'''      <h2>Before: daily takings by hand</h2>
      <p>The business is a Melbourne retailer with two shops, both on Square, with its books in MYOB. Each day's takings were entered into MYOB from Square's reports by hand.</p>
      <p>With two shops, that is two entries for every day traded, and then each Square payout, less Square's fees, to match against the bank. The {link("myob")} guide sets out that job step by step.</p>'''),
          ("now", '''      <h2>Now: every night, automatically</h2>
      <p>The business connected Square and its MYOB file to PayKicker, with each shop set up on its own job. Since mid-October 2026 PayKicker has posted each shop's day into MYOB automatically every night.</p>
      <ul>
        <li><b>Around 200 orders a day</b> across both shops, and close to 3,000 orders in its first two weeks.</li>
        <li><b>Each shop on its own job in MYOB</b>, so each shop's sales sit apart in the same file.</li>
        <li><b>Every Square payout settled</b>, with Square's fees on their own account and the payout as a transfer to the bank.</li>
        <li><b>Each day checked against Square before it posts</b>: the lines must add up to Square's own order totals and the GST must equal Square's, or the day is held with the reason instead of posted.</li>
      </ul>'''),
          ("how", f'''      <h2>What posts each night</h2>
      <p>For each shop, one tax-inclusive sales invoice for the day, every piece of the day on its own account and every line on the shop's job; and for each Square payout, Square's fees on their own account and the payout to the bank. The {link("fees")} guide shows those lines on an example day.</p>
      <p class="note-dim">Figures rounded; the business asked not to be named.</p>''')],
         None,
         None,
         cta("Your shops, posted the same way", "Connect MYOB and Square and press Set it up for me on each shop.", SIGNUP_MYOB,
             related("myob", "fees", "sync")))

    return built


CASE_H1 = "A Melbourne retailer with two shops, on Square and MYOB"


def guide_cards():
    """The /guides/ index cards for the Square guides and the case study."""
    cards = [
        ("myob", "1", "sales invoice per shop per day", "Why MYOB needs a link to Square, the daily entry and the payouts by hand, what goes wrong with fees, refunds, tips and two shops, and how to post every night.", "Read the guide"),
        ("fees", "1/11", "of a GST-inclusive price is the GST", "Sales, GST, tips, card surcharges, gift cards, refunds, Square's fees and the payout: where each one belongs in MYOB and Xero, with an example day.", "Read the guide"),
        ("case", "2", "shops, posted into MYOB every night", "A Melbourne retailer with two shops on Square and MYOB: from daily takings by hand to posting automatically every night, each shop on its own job.", "Read the case study"),
    ]
    out = []
    for k, big, small, p, go in cards:
        path, title = ALL[k]
        out.append(f'''    <a class="gcard" href="{path}">
      <div class="big"><span class="fig">{big}</span><small>{small}</small></div>
      <h2>{title}</h2>
      <p>{p}</p>
      <p class="when">Written {CHECKED}.</p>
      <span class="go">{go} {ARROW}</span>
    </a>''')
    return "  <div class=\"gcards\">\n" + "\n".join(out) + "\n  </div>"


SITEMAP = [ALL[k][0] for k in ("myob", "fees", "case")]
