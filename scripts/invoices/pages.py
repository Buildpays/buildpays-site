"""PayKicker Invoices: the comparison pages and how-to guides (TR, 9 Oct 2026: "How do I get AI search results ...
to point to our product?" — yes to comparison pages, guides and FAQ markup; "make sure to mention we automatically detect
GST and Non GST items in an invoice to split them automatically").

Rendered by scripts/cfmeu/build_guides.py (it owns the page shell), so a run of that script rewrites these pages too.
Every PayKicker claim here was checked against the app (supabase/functions/_shared/bills/: taxCode.js gstSplitLines +
accountForTax for the GST split, approval.js for paths/limits/delegation, remoteBills.js for duplicates in Xero/MYOB,
exportBill.js for tracking/jobs per line). Every competitor fact carries the public page it came from, read on CHECKED.
Re-check them before changing a figure; their prices change.
"""
import json

CHECKED = "9 October 2026"
CHECKED_ISO = "2026-10-09"
PUBLISHED = "2026-10-09"
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg>'

TRIAL = '''      <h2>Try it on your own bills</h2>
      <p>Connect Xero or MYOB, forward a few real supplier invoices and watch them arrive read, coded and split. 14 days and 8 invoices free, no card to start. After that it is $9.99 a month up to 20 invoices, $29.99 up to 100, $69.99 up to 400 and $149 up to 2,000, GST included, for the band each month lands in.</p>
      <div class="cta-act"><a class="spray" href="https://app.paykicker.com.au/signup">Start free trial</a><a href="/invoices">How it works and prices</a></div>
      <p class="related">Related: {related}</p>
      <p class="indep">{indep}</p>'''

INDEP = ("PayKicker is independent software and is not affiliated with or endorsed by Xero or MYOB. "
         "Xero is a trademark of Xero Limited and MYOB is a trademark of MYOB Technology Pty Ltd. This page is general information, not tax advice.")
INDEP_CMP = ("{them} {is_are} a trademark of {owner}; PayKicker is not affiliated with or endorsed by {them_short}, Xero or MYOB. "
             "Details about {them_short} come from its own public pages, read on " + CHECKED + "; prices and features change, so check theirs before you decide. "
             "Prices on this page are in Australian dollars. Tell us at operations@paykicker.com.au if something here is out of date and we will fix it.")

PK = "PayKicker"


def link(path, text):
    return f'<a href="{path}">{text}</a>'


ALL = {
    "dext": ("/compare/dext-alternative", "PayKicker vs Dext"),
    "hubdoc": ("/compare/hubdoc-alternative", "PayKicker vs Hubdoc"),
    "approvalmax": ("/compare/approvalmax-alternative", "PayKicker vs ApprovalMax"),
    "xero": ("/guides/supplier-invoice-approval-xero", "Supplier invoice approval in Xero"),
    "myob": ("/guides/supplier-invoice-approval-myob", "Supplier invoice approval in MYOB"),
    "gst": ("/guides/mixed-gst-invoices", "Invoices with GST and GST-free items"),
}


def related(*keys):
    return " &middot; ".join(link(*ALL[k]) for k in keys)


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "\n".join("        <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'      <div class="tbl"><table>\n        <thead><tr>{th}</tr></thead>\n        <tbody>\n{body}\n        </tbody>\n      </table></div>'


def src(items):
    return '      <p class="src">Sources, read ' + CHECKED + ": " + "; ".join(f'<a href="{u}" rel="noopener">{t}</a>' for t, u in items) + ".</p>"


def ld_page(path, kind, headline, desc, crumbs, faq, faq_ld):
    art = {
        "@context": "https://schema.org", "@type": kind, "headline": headline, "description": desc,
        "url": "https://paykicker.com.au" + path, "datePublished": PUBLISHED, "dateModified": CHECKED_ISO, "inLanguage": "en-AU",
        "author": {"@id": "https://paykicker.com.au/#organization"}, "publisher": {"@id": "https://paykicker.com.au/#organization"},
        "mainEntityOfPage": "https://paykicker.com.au" + path,
        "about": {"@id": "https://paykicker.com.au/invoices#software"},
    }
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://paykicker.com.au" + u} for i, (n, u) in enumerate(crumbs + [(headline, path)])]}
    out = ['<script type="application/ld+json">\n' + json.dumps(art, indent=2, ensure_ascii=False) + "\n</script>",
           '<script type="application/ld+json">\n' + json.dumps(bc, indent=2, ensure_ascii=False) + "\n</script>"]
    if faq:
        out.append(faq_ld(faq))
    return "\n".join(out)


# What PayKicker does — one place, so every page says it the same way.
GST_SPLIT = ("When an invoice mixes GST and GST-free items, PayKicker detects it from the GST printed and splits the bill into a taxable line "
             "and a GST-free line that add up to the invoice, each on the right tax code, and on the matching account when your chart keeps "
             "&ldquo;with GST&rdquo; and &ldquo;GST-free&rdquo; pairs. Nobody works the split out by hand.")


def build(h):
    page, section, head_section, faq_ld, faq_html, NL = h["page"], h["section"], h["head_section"], h["faq_ld"], h["faq_html"], h["NL"]
    built = []

    def emit(key, kind, name, h1, title, og, desc, lede, sections, faq, crumbs, rel, indep, toc=None):
        path = ALL[key][0]
        body = head_section(name, h1, lede, toc, f'  <p class="note">Written {CHECKED}.</p>{NL}')
        letters = "BCDEFGH"
        i = 0
        for sname, sid, inner in sections:
            body += section(letters[i], sname, sid, inner)
            i += 1
        if faq:
            body += section(letters[i], "Questions", "faq", "      <h2>Questions</h2>" + NL + faq_html(faq))
            i += 1
        body += section(letters[i], "Try it", "try", TRIAL.format(related=rel, indep=indep))
        page(path, title, og, desc, ld_page(path, kind, og, desc, crumbs, faq, faq_ld), body)
        built.append((path, og))

    INV = [("PayKicker", "/"), ("Invoices", "/invoices")]
    GUIDES = [("PayKicker", "/"), ("Guides", "/guides/")]

    # ------------------------------------------------------------------ Dext
    dext_rows = [
        ["Price for 20 invoices a month", "$9.99 a month, GST included", "Business plan $42 a month + GST, billed monthly (up to 250 documents, 5 users)"],
        ["Price for 100 invoices a month", "$29.99 a month, GST included", "Business plan $42 a month + GST, billed monthly"],
        ["Users", "As many as you need", "5 on the Business plan"],
        ["Line items read from the invoice", "Every invoice, included", "5 free credits, then an add-on from $28.50 a month or $0.70 a document"],
        ["Invoices with GST and GST-free items", "Detected and split onto the right tax codes automatically", "You can split a document into line items yourself, each with its own tax rate"],
        ["Approvals", "Paths by job: levels in order, any one or all at each level, approver limits, delegation for set dates", "Included: up to 5 stages, conditions such as supplier, category and project, an amount threshold per stage"],
        ["Xero", "Yes", "Yes"],
        ["MYOB", "MYOB Business and AccountRight", "AccountRight Live, and a separate MYOB Essentials connection"],
        ["Jobs", "Xero tracking or MYOB jobs on each line, learned per supplier", "Xero tracking categories; projects as an approval condition"],
        ["Duplicates", "Checked in PayKicker and against bills already in Xero or MYOB", "Built-in duplicate detection"],
        ["Receipts, expense claims, bank and supplier statements", "Not covered: PayKicker reads supplier bills and credit notes", "Covered (statement extraction is an add-on)"],
        ["Free trial", "14 days or 8 invoices, no card", "14 days, no card"],
    ]
    dext_faq = [
        ("Is PayKicker cheaper than Dext?", "For up to 100 supplier invoices a month, yes: $9.99 or $29.99 a month with GST included, against Dext's Business plan at $42 a month plus GST billed monthly, read on " + CHECKED + ". Dext's plan covers up to 250 documents and more document types, so at higher volumes compare the band your month would land in."),
        ("Does PayKicker split invoices with GST and GST-free items?", "Yes, automatically. When the GST on an invoice is neither 10% of the amount before GST nor nil, PayKicker splits it into a taxable line and a GST-free line, each on the right tax code, before anyone codes it."),
        ("Does PayKicker work with MYOB like Dext does?", "Yes. PayKicker connects to MYOB Business and AccountRight, and to Xero. Suppliers, accounts, jobs and tax codes come from your file, and approved bills go back as bills ready to pay."),
        ("Can I switch from Dext to PayKicker?", "Yes. Connect Xero or MYOB to PayKicker and send new bills to your PayKicker invoices address; what Dext already published stays in your books. PayKicker learns your coding from the bills you approve in it."),
    ]
    emit("dext", "Article", "Compare", "PayKicker vs Dext for supplier invoices",
         "PayKicker vs Dext: Supplier Invoices into Xero or MYOB | PayKicker", "PayKicker vs Dext",
         "PayKicker vs Dext for Australian businesses on Xero or MYOB: price, line items, invoices with GST and GST-free items, approvals and jobs, side by side.",
         "Both read supplier invoices and send them to Xero or MYOB. Dext covers more kinds of document; PayKicker is built around supplier bills and getting them approved, includes line items in every band and splits invoices with GST and GST-free items for you. Here is the honest side by side, with Dext's figures from its own pages.",
         [("Side by side", "side", "      <h2>Side by side</h2>" + NL + table(["", PK, "Dext"], dext_rows) + NL +
           src([("Dext AU pricing", "https://dext.com/au/business/pricing"), ("Dext approvals", "https://help.dext.com/en/articles/219981-how-to-set-up-costs-and-sales-approval-workflows-in-dext"),
                ("Dext line items", "https://help.dext.com/en/articles/416723-using-line-items"), ("Dext on the Xero App Store", "https://apps.xero.com/au/app/dext"),
                ("Dext and MYOB AccountRight", "https://help.dext.com/en/articles/209194-how-to-connect-with-myob-accountright-live")])),
          ("GST", "gst", "      <h2>Invoices with GST and GST-free items</h2>" + NL +
           "      <p>A supermarket order, a café supplier, a hardware run with some exempt items: the invoice shows one GST figure that is not 10% of the whole bill. Coded as one line, it either claims too much GST or too little.</p>" + NL +
           f"      <p>{GST_SPLIT}</p>" + NL +
           "      <p>In Dext you can split the document into line items and give each its own tax rate; the lines must add up to the total before it publishes. Automatic line-item extraction is a paid add-on after five free credits.</p>"),
          ("Which one", "which", "      <h2>Which one fits</h2>" + NL +
           "      <ul>" + NL +
           "        <li><b>Pick Dext</b> if you also want receipts and staff expense claims, bank or supplier statements read, or you are a practice running many client files.</li>" + NL +
           "        <li><b>Pick PayKicker</b> if your job is supplier bills: read with their lines, coded to account, job and tax code, approved by the right person within their limit, and posted to Xero or MYOB, for a price that follows how many you had that month.</li>" + NL +
           "      </ul>")],
         dext_faq, INV, related("hubdoc", "approvalmax", "gst"),
         INDEP_CMP.format(them="Dext", is_are="is", owner="its owner", them_short="Dext"))

    # ------------------------------------------------------------------ Hubdoc
    hub_rows = [
        ["Who makes it", "PayKicker, Melbourne", "Xero"],
        ["Cost", "From $9.99 a month, GST included", "Included with some Xero plans; check yours"],
        ["Xero", "Yes", "Yes"],
        ["MYOB", "MYOB Business and AccountRight", "No (Xero and QuickBooks Online)"],
        ["Line items read from the invoice", "Every invoice", "Not extracted automatically; entered by hand or saved in supplier rules"],
        ["Invoices with GST and GST-free items", "Detected and split onto the right tax codes automatically", "Adjusted by hand with a calculator tool that makes extra lines"],
        ["Approvals", "Paths by job: levels in order, any one or all, approver limits, delegation", "None found in Hubdoc's help; Xero's own single approve step"],
        ["Jobs", "Xero tracking or MYOB jobs on each line, learned per supplier", "Shares Xero tracking categories"],
        ["Duplicates", "Checked in PayKicker and against bills already in Xero or MYOB", "Flagged when date, supplier and total match"],
        ["Email-in", "Your own invoices address", "Yes"],
    ]
    hub_faq = [
        ("Is Hubdoc free with Xero in Australia?", "Xero's Australian plans page says Hubdoc is included in its Ignite, Grow, Comprehensive and Ultimate plans when connected to your Xero subscription. Xero's current pricing page instead lists its own Smart document capture in Grow and above, so check what your plan includes."),
        ("Does Hubdoc work with MYOB?", "Not that we could find: Hubdoc's pricing page and Xero App Store listing name Xero and QuickBooks Online. PayKicker works with MYOB Business, AccountRight and Xero."),
        ("Does Hubdoc have invoice approvals?", "We found no approval workflow in Hubdoc's help. Xero itself has one approve step for bills. PayKicker adds approval paths by job, with limits and delegation, before the bill reaches Xero or MYOB."),
        ("How does PayKicker handle an invoice with GST-free items?", "It spots it from the GST printed and splits the bill into a taxable line and a GST-free line, each on the right tax code, so the GST you claim matches the invoice."),
    ]
    emit("hubdoc", "Article", "Compare", "PayKicker vs Hubdoc for supplier invoices",
         "PayKicker vs Hubdoc: Supplier Invoices, Approvals and MYOB | PayKicker", "PayKicker vs Hubdoc",
         "PayKicker vs Hubdoc for Australian businesses: MYOB as well as Xero, line items, invoices with GST and GST-free items split automatically, and approvals by job.",
         "Hubdoc is Xero's document capture app and comes with some Xero plans, so the first question is what you need beyond getting the PDF into Xero. If someone has to approve bills, you use MYOB, or your invoices carry lines with different GST, here is how the two compare.",
         [("Side by side", "side", "      <h2>Side by side</h2>" + NL + table(["", PK, "Hubdoc"], hub_rows) + NL +
           src([("Xero AU plans", "https://www.xero.com/au/campaign/new-plans-ab/overview"), ("Xero AU pricing", "https://www.xero.com/au/pricing-plans/"),
                ("Hubdoc on the Xero App Store", "https://apps.xero.com/au/app/hubdoc"), ("Hubdoc pricing", "https://www.hubdoc.com/pricing"),
                ("Hubdoc data extraction", "https://support.hubdoc.com/hc/en-us/articles/16660084462477")])),
          ("GST", "gst", "      <h2>Invoices with GST and GST-free items</h2>" + NL +
           "      <p>Hubdoc's help says it does not extract line items automatically, and for grocery-style bills where some items are taxed and others are not, you adjust the bill with its calculator tool.</p>" + NL +
           f"      <p>{GST_SPLIT}</p>"),
          ("Which one", "which", "      <h2>Which one fits</h2>" + NL +
           "      <ul>" + NL +
           "        <li><b>Hubdoc is enough</b> if you are on Xero, it comes with your plan, one person codes every bill and nobody else needs to approve them.</li>" + NL +
           "        <li><b>Pick PayKicker</b> if bills need approving before they are paid, you code to jobs, you run MYOB, or your suppliers send invoices that mix GST and GST-free items.</li>" + NL +
           "      </ul>")],
         hub_faq, INV, related("dext", "approvalmax", "gst"),
         INDEP_CMP.format(them="Hubdoc", is_are="is", owner="Xero Limited", them_short="Hubdoc"))

    # ------------------------------------------------------------------ ApprovalMax
    am_rows = [
        ["What it is", "Supplier invoices read, coded, approved and posted", "Approval workflows for bills, purchase orders and more"],
        ["Price for 100 invoices a month", "$29.99 a month, GST included, reading included", "Standard plan, Small: $83 a month + tax billed monthly ($69.20 annually), 100 approved documents"],
        ["Users", "As many as you need", "Unlimited users and approvers"],
        ["Xero", "Yes", "Yes"],
        ["MYOB", "MYOB Business and AccountRight", "No (Xero, QuickBooks Online, Oracle NetSuite)"],
        ["Reads the invoice", "Yes, two readers on every figure, line items included", "ApprovalMax Capture, included in plans; check it covers your region"],
        ["Approval rules", "Paths by job: levels in order, any one or all, approver limits", "Approval matrix by amount, requester, supplier, tracking category, account, item and tax"],
        ["Purchase orders, batch payments, budgets", "No", "Yes, on Advanced and Premium plans"],
        ["Free trial", "14 days or 8 invoices, no card", "14 days, no card"],
    ]
    am_faq = [
        ("Does ApprovalMax work with MYOB?", "Not that we could find: ApprovalMax lists Xero, QuickBooks Online and Oracle NetSuite. PayKicker works with MYOB Business, AccountRight and Xero."),
        ("Is PayKicker cheaper than ApprovalMax?", "For supplier invoices, yes: 100 invoices a month is $29.99 with GST included, reading and coding included. ApprovalMax's Standard plan for 100 approved documents was $83 a month plus tax billed monthly when we read it on " + CHECKED + ". ApprovalMax also covers purchase orders and, on higher plans, batch payments and budgets."),
        ("Does PayKicker have approval limits?", "Yes. Each approver can have a limit. Above it, the bill goes on to someone whose limit covers it. Paths are set per job, in levels signed in order, with any one or all of the people at a level, and approvers can hand their approvals to someone else for set dates."),
        ("Does PayKicker code the GST for me?", "Yes. Each line gets the tax code your account uses, and an invoice with GST and GST-free items is split into a taxable line and a GST-free line automatically."),
    ]
    emit("approvalmax", "Article", "Compare", "PayKicker vs ApprovalMax for supplier invoice approval",
         "PayKicker vs ApprovalMax: Invoice Approval for Xero and MYOB | PayKicker", "PayKicker vs ApprovalMax",
         "PayKicker vs ApprovalMax for Australian businesses: invoice reading and approval in one, MYOB as well as Xero, approval limits by job, and price per month.",
         "ApprovalMax is an approval engine: purchase orders, bills, payments and budgets, for finance teams on Xero, QuickBooks Online or NetSuite. PayKicker does one job end to end: it reads the supplier invoice, codes it, splits GST and GST-free items, gets it approved by the right person and posts it to Xero or MYOB.",
         [("Side by side", "side", "      <h2>Side by side</h2>" + NL + table(["", PK, "ApprovalMax"], am_rows) + NL +
           src([("ApprovalMax for Xero pricing (AUD)", "https://approvalmax.com/pricing/approvalmax-for-xero"), ("ApprovalMax pricing", "https://www.approvalmax.com/pricing"),
                ("ApprovalMax approval matrix", "https://support.approvalmax.com/en/articles/413469-how-to-set-up-an-approval-matrix"), ("ApprovalMax on the Xero App Store", "https://apps.xero.com/au/app/approvalmax")])),
          ("Which one", "which", "      <h2>Which one fits</h2>" + NL +
           "      <ul>" + NL +
           "        <li><b>Pick ApprovalMax</b> if you raise purchase orders, approve batch payments, check spend against budgets, or run QuickBooks Online or NetSuite.</li>" + NL +
           "        <li><b>Pick PayKicker</b> if you want supplier bills read, coded and approved in one place, you run MYOB, or you want the price to follow how many invoices you had that month.</li>" + NL +
           "      </ul>" + NL +
           f"      <p>{GST_SPLIT}</p>")],
         am_faq, INV, related("dext", "hubdoc", "xero"),
         INDEP_CMP.format(them="ApprovalMax", is_are="is", owner="its owner", them_short="ApprovalMax"))

    # ------------------------------------------------------------------ Guide: Xero approval
    xero_steps = '''      <ol class="steps">
        <li><b>Decide who approves what.</b> Write down, for each job or cost centre, who must sign a bill and in what order: a site manager, then a project manager, then a director. Decide whether one person at a level is enough or everyone must sign.</li>
        <li><b>Set limits.</b> Give each approver a dollar limit. A $400 timber bill should not wait for a director; a $40,000 concrete bill should.</li>
        <li><b>Plan for leave.</b> Name who signs when an approver is away, and for which dates, so bills do not sit in someone's inbox.</li>
        <li><b>Code before approving.</b> The approver should see the account, the job and the tax code, so they approve what will land in the books, not just the total.</li>
        <li><b>Keep the clerk off their own bills.</b> The person who entered a bill should not be the one who approves it.</li>
        <li><b>Only approved bills reach Xero as bills to pay.</b> Anything else waits, with the reason it is waiting.</li>
      </ol>'''
    xero_faq = [
        ("Does Xero have bill approval?", "Yes, one step. A user with the Draft sales and purchases role can create a bill and submit it for approval; a user with a purchases role can approve it. Xero's help describes no approval levels or dollar limits for bills."),
        ("How do I code bills to jobs in Xero?", "With tracking categories (four in total, two active at once) on each line, or with Xero Projects, where different lines of one bill can go to different projects. Projects comes with Xero's Ultimate plans."),
        ("Can one Xero bill have GST and GST-free lines?", "Yes. Xero applies tax rates to each line, so a mixed bill is two or more lines: GST on Expenses for the taxable part, GST Free Expenses for the rest. PayKicker makes that split automatically when the invoice mixes the two."),
        ("How do I add approval limits to Xero?", "Xero has no amount-based approval for bills in its help, so the limits sit in an app in front of Xero. In PayKicker each approver has a limit; above it the bill goes on to someone whose limit covers it, and only then is it posted to Xero."),
    ]
    emit("xero", "Article", "Guides", "How to set up supplier invoice approval in Xero",
         "Supplier Invoice Approval in Xero: Levels, Limits and Jobs | PayKicker", "Supplier invoice approval in Xero",
         "What Xero's own bill approval does, where it stops, and how to set up approval levels, dollar limits and job coding for supplier invoices in Xero.",
         "Xero has one approve step for bills. That is enough for a business where one person checks everything. Once bills need a site manager and a director, or a dollar limit, or have to be coded to jobs before anyone signs, you need a process in front of Xero. This guide sets one out.",
         [("In Xero", "native", "      <h2>What Xero does on its own</h2>" + NL +
           "      <p>A bill in Xero moves from Draft to Awaiting Approval to Awaiting Payment. Users with the <b>Draft sales and purchases</b> role can create bills and submit them, but not approve them; users with a purchases role can approve. That is one approver, one step, with no amount limit described in Xero's help.</p>" + NL +
           "      <p>For job costing, Xero gives you <b>tracking categories</b> on each line (up to four, two active at a time) or <b>Xero Projects</b>, which lets different lines of one bill go to different projects and comes with the Ultimate plans.</p>" + NL +
           src([("Xero user roles", "https://central.xero.com/0/article/Invoice-Only-user-role"), ("Xero tracking categories", "https://central.xero.com/0/article/Set-up-tracking-categories"),
                ("Xero Projects expenses", "https://central.xero.com/0/article/Add-an-expense-to-a-project"), ("Xero tax on each line", "https://central.xero.com/0/article/Choose-the-right-tax-treatment-on-transactions"), ("Xero AU pricing", "https://www.xero.com/au/pricing-plans/")])),
          ("Set it up", "steps", "      <h2>Six decisions for an approval process</h2>" + NL + xero_steps),
          ("In PayKicker", "pk", "      <h2>How PayKicker runs it in front of Xero</h2>" + NL +
           "      <p>Bills arrive at your own invoices address or as a PDF. PayKicker reads them twice, matches the supplier in Xero by ABN and name, codes each line to the account, tracking option and tax code you used for that supplier before, and checks for duplicates, including bills already in Xero.</p>" + NL +
           f"      <p>{GST_SPLIT}</p>" + NL +
           "      <p>Each job has an approval path: named levels signed in order, any one or all of the people at a level, each approver's limit, and delegation for set dates. The person who entered a bill is never asked to approve it. When the path is done, the bill goes to Xero as a bill awaiting payment, with the job on each line.</p>")],
         xero_faq, GUIDES, related("myob", "gst", "approvalmax"), INDEP)

    # ------------------------------------------------------------------ Guide: MYOB approval
    myob_faq = [
        ("Does MYOB have bill approval?", "We found no approval step in MYOB's help for entering bills in MYOB Business. A bill is entered and saved, ready to pay, so any approval happens before it is entered: by email, on paper, or in an app in front of MYOB."),
        ("How do I code a bill to a job in MYOB?", "Each line of a bill can carry a job number. PayKicker sends the job on each line, taken from how that supplier's bills were coded before or from what the invoice says."),
        ("Can one MYOB bill have GST and FRE lines?", "Yes. The tax code is set on each line, so a mixed invoice is one line on GST and one on FRE. PayKicker detects a mixed invoice and makes the two lines automatically."),
        ("Which MYOB versions does PayKicker work with?", "MYOB Business and AccountRight. Your suppliers, accounts, jobs and tax codes come from your MYOB file, and approved bills go back as bills ready to pay."),
    ]
    emit("myob", "Article", "Guides", "How to set up supplier invoice approval in MYOB",
         "Supplier Invoice Approval in MYOB: an Approval Process Before Bills | PayKicker", "Supplier invoice approval in MYOB",
         "MYOB has no bill approval step. How to approve supplier invoices before they are entered in MYOB Business or AccountRight, with jobs, limits and GST codes.",
         "MYOB's help describes entering and saving a bill ready to pay, with no approval step in between. So the approval has to happen before the bill reaches MYOB. Most offices do it by email or by initialling a printout. This guide sets out a process that holds up, and how to stop keying the same bill twice.",
         [("In MYOB", "native", "      <h2>What MYOB does on its own</h2>" + NL +
           "      <p>MYOB's help for entering a bill describes the supplier, the lines, an optional job number on each line, and the tax code on each line (GST, FRE and so on). It describes no approval step. That leaves three common workarounds: an approver signs the paper or PDF before it is keyed; bills are emailed to the approver and keyed once they reply; or a spreadsheet tracks who has signed what. All three mean the bill is typed after the decision, and the approver never sees how it was coded.</p>" + NL +
           src([("MYOB: enter a bill", "https://www.myob.com/au/support/myob-business/purchases/entering-purchases/enter-a-bill-quote-or-order"),
                ("MYOB Community: bill approval", "https://community.myob.com/discussions/sales_and_purchases/supplier-invoicesbills---is-there-an-option-for-approval/890799")])),
          ("Set it up", "steps", "      <h2>An approval process for MYOB</h2>" + NL +
           '''      <ol class="steps">
        <li><b>One inbox for bills.</b> Ask suppliers to send invoices to one address, so nothing sits in a site manager's personal email.</li>
        <li><b>Code before approval.</b> Account, job and tax code go on before anyone signs, so the approver sees what MYOB will get.</li>
        <li><b>Paths by job, with limits.</b> Decide who signs for each job, in what order, and up to what amount.</li>
        <li><b>Cover for leave.</b> Name a stand-in for set dates.</li>
        <li><b>Key it once.</b> The approved bill goes to MYOB as it was approved, with the supplier's invoice number, and a second copy of the same invoice is caught before it is keyed again.</li>
      </ol>'''),
          ("In PayKicker", "pk", "      <h2>How PayKicker does it with MYOB</h2>" + NL +
           "      <p>PayKicker reads each invoice, finds the supplier in your MYOB file by ABN and name, codes each line to the account, job and tax code you used for that supplier before, and checks for duplicates, including bills already keyed into MYOB.</p>" + NL +
           f"      <p>{GST_SPLIT}</p>" + NL +
           "      <p>The bill then follows the job's approval path, with each approver's limit and delegation for set dates. Once approved it goes to MYOB as a bill ready to pay, with the job and tax code on each line.</p>")],
         myob_faq, GUIDES, related("xero", "gst", "dext"), INDEP)

    # ------------------------------------------------------------------ Guide: mixed GST
    ex = table(["", "Amount"], [
        ["Subtotal before GST (all items)", "$187.40"],
        ["GST printed on the invoice", "$6.20"],
        ["Total", "$193.60"],
        ["<b>Taxable items before GST</b> = GST &times; 10", "<b>$62.00</b> on GST (MYOB) or GST on Expenses (Xero)"],
        ["<b>GST-free items</b> = subtotal &minus; taxable", "<b>$125.40</b> on FRE (MYOB) or GST Free Expenses (Xero)"],
    ])
    gst_faq = [
        ("How do I enter an invoice with GST and GST-free items in Xero?", "As two or more lines on one bill: the taxable part on GST on Expenses and the rest on GST Free Expenses. Xero works out tax line by line. When the invoice shows one GST total, the taxable part before GST is the GST times 10 and the GST-free part is the rest of the subtotal."),
        ("How do I enter it in MYOB?", "The same way: one line on the GST code and one on FRE, each with its own account and job if you keep separate accounts. MYOB sets the tax code on each line."),
        ("What must a tax invoice with GST-free items show?", "The ATO says a tax invoice that includes taxable and non-taxable items must clearly show which items are taxable, and also show each taxable sale, the amount of GST and the total to pay."),
        ("Does PayKicker split mixed GST invoices automatically?", "Yes. When the GST on an invoice is neither 10% of the amount before GST nor nil, PayKicker splits it into a taxable line and a GST-free line that add up to the invoice, each on the right tax code, and on your with-GST and GST-free accounts if your chart keeps pairs."),
    ]
    emit("gst", "Article", "Guides", "Invoices with GST and GST-free items: how to code them in Xero and MYOB",
         "Mixed GST Invoices: Coding GST and GST-Free Items in Xero and MYOB | PayKicker", "Invoices with GST and GST-free items",
         "How to code a supplier invoice that mixes GST and GST-free items in Xero or MYOB, with the GST times 10 split worked through, and how PayKicker does it automatically.",
         "A supermarket order, a food wholesaler, a pharmacy: some items carry GST and some do not, and the invoice shows one GST total. Coded as one line, the bill either claims GST you did not pay or misses GST you did. Here is how to split it, and how PayKicker does the split for you.",
         [("The rule", "rule", "      <h2>What the invoice has to show</h2>" + NL +
           "      <p>The ATO says a tax invoice that includes taxable and non-taxable items must clearly show which items are taxable; items are non-taxable if they are GST-free or input-taxed. It must also show each taxable sale, the amount of GST and the total. Suppliers often mark the taxable items with a symbol and print one GST figure at the bottom.</p>" + NL +
           src([("ATO: tax invoices (updated 18 September 2026)", "https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/tax-invoices")])),
          ("The split", "split", "      <h2>Splitting it by hand</h2>" + NL +
           "      <p>GST is 10% of the price of the taxable items, so the GST printed, times 10, is the taxable part before GST. The rest of the subtotal is GST-free. A worked example:</p>" + NL + ex + NL +
           "      <p>Enter the bill as two lines that add up to the subtotal: the taxable part on your GST purchase code and the GST-free part on the GST-free code. Both Xero and MYOB set the tax code on each line. If your chart keeps separate accounts, such as &ldquo;Groceries with GST&rdquo; and &ldquo;Groceries GST-free&rdquo;, each line goes to its own account. A cent of difference can come from the supplier rounding each item; the invoice's own GST figure is the one to match.</p>" + NL +
           src([("Xero: tax on each line", "https://central.xero.com/0/article/Choose-the-right-tax-treatment-on-transactions"), ("MYOB: enter a bill", "https://www.myob.com/au/support/myob-business/purchases/entering-purchases/enter-a-bill-quote-or-order")])),
          ("In PayKicker", "pk", "      <h2>How PayKicker does it automatically</h2>" + NL +
           f"      <p>{GST_SPLIT}</p>" + NL +
           "      <p>The check runs on every invoice it reads: when the GST is 10% of the amount before GST the bill takes your GST code, when it is nil it takes the GST-free code, and anything in between is split. Whoever approves the bill sees both lines, their accounts and their tax codes before it goes to Xero or MYOB.</p>")],
         gst_faq, GUIDES, related("xero", "myob", "dext"), INDEP)

    return built


def guide_cards():
    """The /guides/ index cards for the invoice guides."""
    cards = [
        ("gst", "&times;10", "the GST printed, times ten, is the taxable part", "The GST times 10 split worked through, what the ATO says the invoice must show, and how to enter the two lines in Xero or MYOB."),
        ("xero", "1", "approve step in Xero's own bills", "What Xero's Draft, Awaiting Approval and Awaiting Payment do, where they stop, and six decisions for approval levels, limits and job coding."),
        ("myob", "1&times;", "keyed once, after it is approved", "MYOB saves a bill ready to pay. How to approve supplier invoices before they reach MYOB, with jobs, limits and GST codes."),
    ]
    out = []
    for k, big, small, p in cards:
        path, title = ALL[k]
        out.append(f'''    <a class="gcard chalk" href="{path}">
      <div class="big">{big}<small>{small}</small></div>
      <h2>{title}</h2>
      <p>{p}</p>
      <p class="when">Written {CHECKED}.</p>
      <span class="go">Read the guide {ARROW}</span>
    </a>''')
    return "  <div class=\"gcards\">\n" + "\n".join(out) + "\n  </div>"


SITEMAP = [ALL[k][0] for k in ("dext", "hubdoc", "approvalmax", "xero", "myob", "gst")]
