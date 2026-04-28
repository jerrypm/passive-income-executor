## 9 — Stripe Payout Worldwide

### What This Chapter Covers

- Why Medium uses Stripe Express specifically — and what that means for how you connect your bank account
- The exact setup steps, the tax forms you will be asked to complete, and what goes wrong and why
- How currencies, exchange rates, and the $10 minimum threshold interact with your actual cash flow
- What to do if Stripe rejects your bank, and a simple tracking template that doubles as a tax log

---

### Why Stripe Express

Medium does not process payouts itself. The Partner Program uses Stripe Express to handle the entire payment flow — identity verification, tax document collection, bank account management, and fund disbursement.

Stripe Express is a hosted onboarding product Stripe provides specifically for marketplace platforms. When you set up Medium payouts, you are connecting to a Stripe Express account that Medium creates on your behalf. You do not need a separate Stripe account first. If you already have one for another business, it does not matter here — the two are completely separate.

The important consequence of this architecture: when something goes wrong on the Stripe side — a bank rejection, an identity verification flag, a tax form issue — Medium support cannot fix it. Those issues go to Stripe Express support directly, via the dashboard link in your Express account.

The canonical reference for Stripe Express is: https://stripe.com/express

---

### Setup Steps

Have your official ID and bank account details ready before you start. The process can complete instantly or pause for manual identity verification — having everything on hand avoids having to restart.

1. Sign in to Medium with the account enrolled in the Partner Program.
2. Go to **Settings → Payouts**. If you do not see Payouts in the menu, confirm your account is enrolled in the Medium Partner Program first (covered in Chapter 2).
3. Click **Connect to Stripe**.
4. Choose your **country of residence** from the list. This must be a country where Stripe Express is supported. The full list of supported countries was reviewed in Chapter 2. Your payout currency and available bank options depend on this selection, so choose accurately — you cannot easily switch countries later without contacting support.
5. Enter your **legal name** exactly as it appears on your official government-issued ID. Middle names, diacritics, abbreviated names — match the ID. Mismatches here cause identity verification to fail.
6. Enter your **date of birth** and your **tax identification number** appropriate for your country. For US writers this is your SSN or EIN. For non-US writers it may be your national tax ID, personal identification number, or in some countries, a passport number. If your country does not use tax IDs in the traditional sense, Stripe will guide you to the appropriate field.
7. Enter your **bank account details**: account number, routing number or IBAN/SWIFT depending on your country, and confirm the account is in your name and in the country you selected in step 4.
8. Complete **identity verification** if Stripe requests it. This usually means uploading a photo of a government-issued ID — passport, national ID card, or driver's license. Stripe's verification system handles the review.
9. Wait for **verification to complete**. This is often instant for low-complexity cases. For accounts in certain countries or with edge cases in the document review, it can take 1–3 business days. You will receive an email when it is done.

After verification, your Stripe Express dashboard becomes accessible from Medium's Payouts page. That dashboard is where you can check your balance, update your bank account, download tax documents, and reach Stripe support.

---

### Tax Documents By Region

Tax forms are collected during onboarding and sometimes updated annually. What you fill out depends entirely on where you are based.

**US writers** complete a **W-9** during onboarding. If your earnings exceed $600 in a calendar year, you will receive a 1099-NEC reporting that income to the IRS. Keep your own records throughout the year — the 1099 confirms the number but you want a log to verify it.

**Non-US writers** complete a **W-8BEN** during onboarding. The W-8BEN declares your foreign tax status and lets you claim a tax treaty benefit if one exists between your country and the US. Without a treaty, Medium withholds 30% of your earnings before paying you. With a valid treaty claim, that rate drops — often to 0–15%. Look up your country's treaty with the US on the IRS website before completing the form. For Indonesian writers, the US–Indonesia treaty reduces withholding on this income type to 10–15%.

**EU writers**: VAT is not collected by Medium on your Partner Program earnings. Declare income as personal or freelance income per your country's rules. Check whether your Medium earnings, combined with other freelance income, push you past your local VAT registration threshold (typically €10K–€50K depending on the country).

**All other regions**: declare Medium earnings as personal income per your local rules. If your country has a US tax treaty, claim it on your W-8BEN. Export your Medium earnings history regularly rather than relying on platform records alone at tax time.

---

### Currencies And Exchange

Stripe Express defaults to USD payouts globally. Medium pays into your Stripe Express account in USD; Stripe then transfers to your bank. If your bank account is in a local currency, the conversion happens at the bank level on the day of transfer. Bank exchange rates include a 1–3% margin over the interbank rate — sometimes wider.

For writers in stable-currency countries — UK, EU, Australia, Singapore — this is a minor friction. For writers in high-volatility currencies — Argentine peso, Turkish lira, Nigerian naira, Pakistani rupee — converting at the bank's rate on transfer day can erode real value quickly during periods of depreciation.

The workaround: receive into a multi-currency wallet instead of a local-currency bank account. Wise and Revolut both support Stripe Express deposits in most of their operating countries and let you hold balances in USD, converting on your own schedule. This puts the timing of the exchange in your hands. Check the Stripe Express dashboard for what is available in your country before you set this up.

Some countries support native local-currency payout through Stripe Express — check your dashboard after onboarding. If that option exists and your currency is stable, it removes the conversion step entirely.

---

### The $10 Minimum + Rolling 30 Days

Medium only initiates a payout when your accumulated balance crosses $10. If you earn $7.20 in a month, that balance rolls forward and combines with next month's earnings. The threshold applies to your total outstanding balance, not to a single month in isolation.

The "rolling 30 days" calculation works at the story level: for each story, Medium counts member read time from the preceding 30 days at any given point. A story that goes modestly viral does not pay you once and stop — every day it earns based on whoever read it in the previous 30 days. A story from November can still be adding to your January balance if readers keep finding it.

This means you cannot predict a month's payout from what you published that month. You are collecting earnings from a rolling window across all your stories. A story you published six months ago with steady search traffic may be contributing more than your most recent piece — older content compounds quietly. Balances below $10 carry forward indefinitely with no expiration.

---

### Payout Calendar

Medium runs its payout cycle around the 5th of each month — sometimes the 4th, sometimes the 6th or 7th depending on weekends and banking holidays. On that date, Medium instructs Stripe to transfer your accumulated balance.

Funds land in your bank within 5–7 business days after Stripe initiates the transfer. US accounts are often faster — 2–3 business days is common. International transfers to banks in Southeast Asia, South Asia, or Africa typically take the full 5–7 days, with occasional delays beyond that.

The practical consequence: January earnings reach your bank in mid-to-late February at earliest. Medium is a slow-pay channel by design. Do not treat it as income you will see this month — build your cash flow plan around a 4–6 week lag from when you earn to when funds land.

---

### What To Do If Stripe Rejects Your Bank

Bank rejections happen. Stripe Express does not accept all banks in all countries, and some banks actively reject incoming Stripe deposits even if Stripe accepts the account for setup. The rejection usually shows up as a failed transfer notification in your Stripe Express dashboard with a generic error code.

Work through these three fixes in order:

**1. Try a different bank account in your name.** Some banks have standing policies against Stripe payments — often for compliance reasons specific to their charter. If one bank rejects the deposit, another bank in the same country may accept it without any issue. This is the most common fix and requires no contact with anyone — just update the bank account in your Stripe Express dashboard and wait for the next payout cycle.

**2. Use a Stripe-supported fintech wallet.** Wise multi-currency accounts and Revolut both support Stripe Express deposits in most countries where they operate. Your country may have a local equivalent — check Stripe's list of supported banks and financial institutions in the Express documentation. Set up the fintech account, add it in Stripe Express, and the next payout will route there instead. You can then transfer from the fintech wallet to your local bank on your own timeline.

**3. Contact Stripe Express support directly.** In your Stripe Express dashboard, there is a support link specific to Express accounts. Use that, not Medium's general support. Medium support does not have access to your Stripe Express account and cannot resolve bank-side issues. Stripe Express support can review the specific rejection reason and tell you whether it is fixable or whether you need a different bank. Have your account details ready when you reach out.

In markets where Stripe Express support is limited, some countries have very few banks that work reliably with Stripe. Research your local options in writer communities or expat finance forums before you apply — finding this out during setup is far less frustrating than when your first payout fails to arrive.

---

### Tracking Your Earnings

Medium provides an earnings dashboard, but it is not a substitute for your own records. The platform can change its reporting format; you need a log that works for tax purposes and that tells you what is actually driving your income.

A single Google Sheet or Notion page with these columns is enough:

| Month | Gross (USD) | Local-currency value | Stripe / bank fees | Net received | Notes |
|-------|-------------|---------------------|-------------------|--------------|-------|
| Jan 2026 | $41.20 | Rp 670,000 | $1.80 | $39.40 | "SwiftUI tips" drove 60% |

One row per month, updated when the transfer lands. The Notes column is the most underused part — one sentence on which story drove the month is information you will use for content decisions. If January's $41 came almost entirely from a SwiftUI piece you wrote in September, that pattern is worth knowing.

The tax value of this log is straightforward: an independent record to cross-check against Medium's reported earnings and any 1099 or withholding documentation you receive. I have kept a version of this log since 2017. The most useful thing it shows is not the total — it is which content has a long tail and which content dies after a week. That pattern changes how you decide what to write next.

---

Chapter 10 takes everything set up across these nine chapters — the profile, the writing system, the publication relationships, the engagement habits, and the payout infrastructure — and puts it into a concrete 90-day calendar you can follow to turn this setup into ongoing, predictable income.

