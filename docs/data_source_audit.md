# Data Source Audit — Phase 2 Research Memo

**Status:** Research only. No data was collected, downloaded, or fabricated. No code
was changed. Nothing was staged, committed, or pushed.

**Scope:** Investigate a practical, legally compliant data strategy for an
earnings-call language research project. This memo compares candidate sources,
documents known limitations, proposes a minimal dataset schema, recommends a small
legal pilot sample, and lists open questions.

**Conventions used in this memo:**

- **[VERIFIED]** — confirmed against a primary source (provider documentation,
  terms page, or SEC website) on 2026-10-13.
- **[UNVERIFIED]** — reported second-hand or not confirmed against provider terms;
  must be re-checked before any integration.
- **[ASSUMPTION]** — our own design judgement, not a claim about a provider.

> Nothing in this memo is legal advice. Any licensing or redistribution decision
> must be confirmed against the provider's current terms and, where relevant, with
> counsel.

---

## 1. Why SEC filings are not a transcript source by themselves

A common misconception is that SEC filings contain full earnings-call transcripts.
They usually do not.

- **[VERIFIED]** The SEC's EDGAR system exposes free REST APIs on `data.sec.gov`
  (company submissions and extracted XBRL), plus full-text search of electronically
  filed documents since 2001. Access is governed by a Fair Access policy: **no more
  than 10 requests per second**, a descriptive `User-Agent` is required, and
  excessive/unclassified automated crawling may be blocked. Source: SEC.gov
  "Developer Resources" (last updated 2025-03-10).
- **[VERIFIED]** Earnings are typically disclosed in a **Form 8-K, Item 2.02**
  ("Results of Operations and Financial Condition"), where the attached press
  release is usually **Exhibit 99.1**. The 8-K is often accompanied by a
  same-day press release and a webcast, but the **prepared-remarks/PDF and full
  verbatim transcript are frequently posted to the company's investor-relations
  site rather than filed with the SEC**.
- **[VERIFIED]** Transcripts *are* occasionally filed as an 8-K exhibit
  (a documented example: a 2006 Form 8-K filing an earnings-call transcript as
  Exhibit 99.1), but this is company-by-company and **not systematic**.

**Implication:** EDGAR is a reliable, free, timestamped source for the **earnings
release, filing time, and XBRL financials** — but it is **not** a reliable
standalone source of full call transcripts. A transcript source must be chosen
separately.

---

## 2. Transcript sources

### 2.1 Commercial/academic aggregators

| Source | Access model | Notes | Evidence |
|---|---|---|---|
| **LSEG (Refinitiv) StreetEvents / Company Transcripts** | Paid subscription; some access via university LSEG Workspace terminals | Large global coverage; widely used in academic research | **[VERIFIED]** LSEG Data Catalogue "Company Transcripts" page describes transcript/summary coverage across major indices |
| **S&P Capital IQ Transcripts** | Paid; often delivered through **WRDS** at subscribing universities | Historical conference-call transcripts, ~8,000 public companies | **[VERIFIED]** WRDS "Capital IQ Transcripts" page |
| **Bloomberg / AlphaSense / FactSet CallStreet** | Paid enterprise | Rich metadata, speaker separation | **[UNVERIFIED]** (not fetched) |
| **S&P Global Transcripts (via WRDS)** | Subscription through WRDS | Combines transcripts with earnings/guidance datasets | **[VERIFIED]** WRDS data-announcement page |
| **ROIC.ai** | Free tier advertised for transcripts | Independent provider; free-tier limits unconfirmed | **[UNVERIFIED]** — search result claims "free tier"; terms not verified |
| **Financial Modeling Prep (FMP)** | Paid API, some free endpoints | Public "earnings call transcripts" API product | **[VERIFIED]** FMP markets an earnings-call-transcripts dataset; **[UNVERIFIED]** free-tier entitlement |
| **Finnhub** | Free + paid API | Estimates/actuals/EPS surprises; filings API | **[VERIFIED]** Finnhub docs list filings and EPS-surprise endpoints; **[UNVERIFIED]** free-tier limits |

### 2.2 Free web sources (use with care)

| Source | Access model | Notes | Evidence |
|---|---|---|---|
| **The Motley Fool** | Free public web archive | US-centric, selected companies; ToS reported to **prohibit scraping** | **[UNVERIFIED]** — third-party scraper repos cite the Fool's Terms of Use prohibiting scraping; we did **not** fetch the ToS directly |
| **Seeking Alpha** | Free browsing + Premium; **no public API** | ToS restrict scraping/redistribution | **[VERIFIED]** Seeking Alpha states transcripts are published roughly **6 hours after the call ends**; ToS/redistribution restrictions **[UNVERIFIED]** (not fetched directly) |
| **Company investor-relations sites** | Free | Often post prepared remarks immediately and the full transcript/PDF later | **[VERIFIED]** Microsoft IR states prepared remarks are posted after the call "until the complete transcript is available"; Meta IR lists a call-transcript PDF |
| **Kaggle mirrors (e.g., scraped Motley Fool transcripts)** | Free download | Derivative of a scraped source; license often "Unknown" | **[VERIFIED]** Kaggle "Scraped Motley Fool Earnings Call Transcripts" dataset page lists **License: Unknown** |
| **Strux** (academic transcript dataset) | Academic dataset | Reported ~11,950 transcripts sourced from Motley Fool | **[UNVERIFIED]** — project page only; provenance/licensing not confirmed |

**Caution:** free web archives (Motley Fool, Seeking Alpha) are attractive for cost
but commonly restrict automated collection and redistribution in their terms.
Scraping them may breach ToS even though the pages are publicly readable. A
legal decision here is a **prerequisite**, not a detail.

### 2.3 Licensing: public availability is not permission

Public availability of a transcript — on a company investor-relations website or
any other public page — does **not** automatically grant permission for automated
collection, local storage, use in derived data, or redistribution. Public
*readability* is a separate question from *permitted use*, and this memo draws **no
legal conclusion** about either.

Before any collection, the following terms must be checked for the chosen source.
This checklist is our own **[ASSUMPTION]**; the answers are source-specific and
currently **unknown/unverified**:

- Whether the site's **Terms of Use** permit automated retrieval, and whether
  `robots.txt` disallows the relevant paths.
- Whether **local storage** of full transcript text is permitted (and for how long).
- Whether **derived data** (e.g., sentiment/uncertainty scores, embeddings) may be
  computed and retained.
- Whether **redistribution** or publication of the text or of derived features is
  allowed, together with any attribution requirements.
- Any **rate limits, crawl policies, or sanctioned access paths** (for example an
  official API or a data-use agreement) — none of which is verified in this memo.
- Whether access depends on a **paid license** whose scope differs from the public
  website.

Until these questions are answered for a specific source, no transcript collection
should be assumed permissible.

---

## 3. Market and benchmark price sources

Requirements for this project: **daily** OHLCV (adjusted for splits/dividends),
long history, and a benchmark series suitable for abnormal-return models.

| Source | Free tier | History | Key constraints | Evidence |
|---|---|---|---|---|
| **SEC EDGAR (XBRL)** | Free | 2001+ filings | Filings/financials only, **not prices** | **[VERIFIED]** SEC Developer Resources |
| **Alpha Vantage** | **25 requests/day**; unlimited for verified open-source/educational projects | Long daily history | Realtime/15-min US data is **premium-only** (exchange-licensed); adjusted for splits + cash dividends | **[VERIFIED]** Alpha Vantage support page (2026-10-13) |
| **Tiingo** | Advertised free tier (limits vary) | 30+ years EOD for US equities | Hourly/daily request buckets; pricing page body did not render for us | **[UNVERIFIED]** — pricing page fetch returned empty body; figures seen only in third-party snippets |
| **Polygon.io / "Massive"** | Advertised free tier (~5 calls/min, ~2 years history) | Short on free tier | Brand/branding confusion in search results; must confirm the canonical domain before integrating | **[UNVERIFIED]** — verify at integration time |
| **Nasdaq Data Link** | Mixed (some free tables, most premium) | Varies | Legacy Quandl platform; ZEEH earnings-estimate history is a paid feed | **[UNVERIFIED]** for price tables; **[VERIFIED]** ZEEH estimate feed exists |
| **Stooq** | Free CSV, no key | Decades of daily data | Licensing/ToS unclear; no SLA | **[UNVERIFIED]** — third-party description only |
| **Yahoo Finance (via `yfinance`)** | Free (unofficial wrapper) | Long daily history | **Unofficial**, ToS/rate-limit risk; not licensed for redistribution | **[UNVERIFIED]** — widely used but not an official API |
| **CRSP (via WRDS)** | Institutional subscription | 1920s+ | **Survivorship-bias-free** with delisting returns — the research gold standard | **[VERIFIED]** WRDS/CRSP and CRSP-Compustat linking tables require subscription |
| **Kenneth R. French Data Library** | **Free** | Market and factor series, long history | Benchmark/factor returns (Rm-Rf, SMB, HML, etc.) | **[VERIFIED]** Dartmouth Data Library homepage |

**Implication:** for a genuinely publishable event study, **CRSP (point-in-time,
delisting-aware)** is the correct market-data source, accessed through a university
WRDS subscription. For a cheap pilot, Alpha Vantage (very low free daily quota) or
another free EOD feed is workable, with the explicit caveat that survivorship bias
and unlicensed redistribution must be managed.

**Adjusted prices and how they will be used.** Returns will be computed from
**adjusted** prices so that splits and cash dividends do not create artificial
jumps (an unadjusted price series would show a large spurious drop on every
dividend ex-date and a false jump on every split). Adjustments matter directly for
return windows that straddle an ex-date. Some vendors expose **adjusted close
only** while returning raw intraday OHLC — we must **not** assume every source
supplies adjusted open/high/low/close. Confirmed specifics here are limited to
**[VERIFIED]** Alpha Vantage (adjusted for splits and cash dividends, with a raw
option on many endpoints); adjustment behavior for Tiingo, Stooq, and
Polygon/"Massive" remains **[UNVERIFIED]** and must be checked before use. The
schema (§7) therefore records the adjustment status per price row rather than
assuming it.

---

## 4. Timestamps and look-ahead avoidance

Look-ahead bias is the central integrity risk: a transcript must only be treated
as known **after it became publicly available**, not on the call date.

What timestamps are actually obtainable:

- **[VERIFIED]** EDGAR provides filing/acceptance timestamps for 8-Ks and other
  filings (and full-text search with date filters). This gives a defensible time
  for the **earnings release**, which is usually the same day as the call.
- **[VERIFIED]** Transcript vendors publish with a delay (Seeking Alpha states
  ~6 hours after the call ends; company IR sites post prepared remarks immediately
  and the full transcript later). So a transcript's **publication time can be
  *after* the market close on the call day**.
- **[UNVERIFIED]** Most free transcript archives do **not** expose a precise,
  machine-readable "published-at" timestamp; the article date may be day-granular.
- **[ASSUMPTION]** WRDS/IBES-style datasets typically carry an event-date field;
  whether a **first-availability timestamp** exists must be confirmed for the
  chosen vendor.

**Three distinct times must not be conflated:**

- `transcript_published_at` — the moment the source made the transcript publicly
  available (may be day-granular or unknown).
- `decision_timestamp` — the moment the strategy is modeled as acting on the
  signal; it must be **at or after** `transcript_published_at`.
- `first_eligible_execution_price` — the first price a strategy could realistically
  trade at **on or after** `decision_timestamp`. It must never predate public
  availability.

(`filing_datetime` from EDGAR still anchors the earnings-release time separately.)

**Conservative convention** — a research-integrity rule, **[ASSUMPTION]**, not a
provider fact:

| Publication timing | `decision_timestamp` | First eligible execution |
|---|---|---|
| Before market open on a trading day | That day's open | That day's open (or later) |
| During market hours | First moment at/after publication | Next trading day's open |
| After market close | Next trading day's open | Next trading day's open |
| Date only (no time) | End of that date | Next trading day's open |
| Time unknown / ambiguous | End of that date | Next trading day's open |

Rationale: a fill at a price that predates public availability is not executable
and would bias results; where timing is uncertain, the convention deliberately
delays execution. Verify programmatically that every feature's availability time
precedes the start of its return window.

---

## 5. Earnings-surprise sources

Earnings surprise (actual vs consensus estimate) is a required control variable.

- **[VERIFIED]** **I/B/E/S** (via WRDS) is the standard academic source of
  consensus estimates and actuals; requires subscription.
- **[VERIFIED]** **Finnhub** documents EPS-surprise and estimate endpoints;
  **[UNVERIFIED]** free-tier access to historical estimates.
- **[VERIFIED]** **FMP** markets earnings-surprise APIs.
- **[VERIFIED]** **Nasdaq Data Link ZEEH** ("North American Consensus Earnings
  Estimate History") is a paid feed.
- **[ASSUMPTION]** For a free pilot, actual EPS can be taken from a company press
  release (EDGAR 8-K Exhibit 99.1) while consensus estimates would come from a
  provider; the **estimate** side is the harder, more licensing-sensitive piece.

---

## 6. Comparison summary (verified vs. assumed)

| Need | Best compliant option | Cheap/pilot option | Confidence |
|---|---|---|---|
| Earnings release + filing time | EDGAR (free) | EDGAR (free) | **[VERIFIED]** |
| Full call transcript | LSEG / Capital IQ / S&P Global via WRDS | Company IR PDFs, or a licensed aggregator | Vendor access **[VERIFIED]**; free alternatives **[UNVERIFIED]** |
| Daily prices (research-grade) | CRSP via WRDS | Alpha Vantage (25/day free), other EOD feed | CRSP **[VERIFIED]**; free tiers **[VERIFIED]** for Alpha Vantage |
| Delisting/survivorship handling | CRSP | Not available for free | **[VERIFIED]** |
| Benchmark/factor returns | Ken French Data Library (free) / CRSP | Ken French Data Library | **[VERIFIED]** |
| Earnings surprise | I/B/E/S via WRDS | FMP/Finnhub free endpoints | Estimate side **[UNVERIFIED]** for free tiers |

---

## 7. Proposed minimal dataset schema

A deliberately small, joinable relational schema (SQLite-ready). Timestamps are
explicit and every foreign key is stated so point-in-time joins are auditable.

```
companies
  company_id           PK   internal surrogate
  cik                  SEC Central Index Key (EDGAR join key, zero-padded)
  ticker               as-of ticker (may change over time)
  permno               CRSP identifier (nullable until WRDS access)
  name                 company name as filed
  sector               GICS/industry (source noted; nullable in pilot)

earnings_events
  event_id             PK
  company_id           FK -> companies
  fiscal_period        e.g. "2024Q3"
  call_date            date of the earnings call
  filing_accession     EDGAR accession number of the earnings 8-K
  filing_datetime      precise EDGAR acceptance timestamp (UTC)
  release_datetime     when the earnings release became public (UTC)
  source               provenance label (e.g. "edgar:8-K:2.02")

transcripts
  transcript_id        PK
  event_id             FK -> earnings_events
  source               provider/archive name
  source_url            canonical URL
  published_at         best available publication timestamp (UTC); may be day-granular
  published_at_precision  {timestamp, date, unknown}
  license_note          terms under which this transcript may be used
  raw_path              path under data/raw/ (git-ignored)
  text_sha256           content hash for dedup/integrity

transcript_sections
  section_id           PK
  transcript_id        FK -> transcripts
  section_type         {prepared_remarks, qa, operator, other}
  speaker_role         {ceo, cfo, analyst, operator, other} (nullable)
  speaker_name         nullable
  seq                  ordinal position within the transcript
  text                 section text

earnings_surprises
  surprise_id          PK
  event_id             FK -> earnings_events
  estimate_eps         consensus EPS (source noted)
  actual_eps           reported EPS
  surprise             actual - estimate (and/or standardized surprise / SUE)
  estimate_source      e.g. "ibes", "fmp", "none"
  estimate_as_of       timestamp the estimate is valid as of (point-in-time)

prices_daily
  price_id             PK
  security_id          company_id or permno
  date                 trading date
  open/high/low/close  as provided by source (state adjusted vs. raw)
  adj_close            adjusted close, if the source supplies it
  volume
  adjustment           {none, split, split_dividend, unknown} + method note
  source               provenance label

returns
  return_id              PK
  event_id               FK -> earnings_events
  window_label           e.g. "+1", "+5", "[0,+60]" (naming only)
  window_start           window start (>= decision_timestamp)
  window_end             window end
  method                 abnormal-return method (see §7.1)
  benchmark              e.g. "market_adjusted", "market_model", "ff3"
  raw_return             cumulative raw (adjusted-price) return over the window
  expected_return        benchmark expectation (nullable for market-adjusted)
  abnormal_return        raw minus expected
  signal_available_at    transcript publication time used for this row
  decision_timestamp     time the strategy acts (>= signal_available_at)
  execution_convention   how the entry price was chosen (e.g. "next_open")
  entry_price            first eligible execution price (>= decision_timestamp)
```

**Design notes**

- Everything downstream joins through `event_id` so each analysis row carries its
  own timestamps.
- The `returns` table separates the **signal availability time**
  (`signal_available_at`), the **decision time** (`decision_timestamp`), the
  **execution convention and price** (`execution_convention`,
  `entry_price`), and the **return window** (`window_start`, `window_end`). This
  makes the look-ahead decision auditable per row instead of hidden.
- `published_at` + `published_at_precision` make the transcript's availability
  timing explicit, including when it is only day-granular.
- `license_note` and `source` on `transcripts` keep provenance and redistribution
  constraints attached to the data itself.
- `adjustment` on `prices_daily` prevents silently mixing adjusted and raw series.
- Raw text lives under the git-ignored `data/raw/`; only hashes/structured rows
  would ever be tracked.

### 7.1 Abnormal-return methodology (methodological choices, not provider facts)

Three candidate methods, in increasing data and estimation requirements. All are
**[ASSUMPTION]** methodological choices; none is a verified provider claim.

1. **Market-adjusted returns.** `abnormal = raw_return − benchmark_return`, where
   the benchmark is a broad market series (e.g. the Ken French market factor).
   Needs only the security's adjusted returns and one benchmark series; no
   estimation window and no fitted parameters. Recommended as the **pilot
   baseline** for its transparency.
2. **Market model.** Estimate `r_i = alpha_i + beta_i · r_m + e_i` on a pre-event
   estimation window, then take the event-window residual as the abnormal return.
   Requires an estimation-window length and end date and a market index; adds
   estimation risk.
3. **Factor-adjusted returns.** Extend the model to multiple factors (e.g.
   Fama-French 3- or 5-factor, optionally momentum). Requires the factor series
   and the same estimation decisions; more robust to known risk exposures but
   needs more data per event.

**Recommendation (methodological):** start the pilot with **market-adjusted
returns**, and treat the market model and factor-adjusted returns as specification
checks once samples are large enough to estimate them reliably. The additional
estimation decisions required for the alternatives — estimation-window length and
end date, benchmark/index choice, factor set, and whether betas are pooled or
estimated per firm — are **not** provider facts and must be pre-specified.

---

## 8. Recommended starting sample (not collected yet)

To exercise the **entire workflow** legally with minimal licensing exposure:

- **Companies:** a small, fixed set of large, high-coverage US issuers with
  reliable IR pages (e.g., 5–10 firms across 2–3 sectors). Concrete names to be
  chosen only after confirming the transcript source's terms.
- **Period:** a recent 4–8 quarter window (keeps transcript count small and stays
  within free-tier price quotas).
- **Transcripts:** from a source whose terms permit the intended use. If using a
  free web archive, confirm ToS **first**; otherwise prefer company IR PDFs, which
  are the least licensing-encumbered free option.
- **Prices:** Alpha Vantage free tier (25 requests/day) is enough for a handful of
  tickers over a few quarters if requests are budgeted; benchmark from the
  Ken French Data Library (free).
- **Goal:** produce a tiny end-to-end artifact — event table → transcript sections
  → features → abnormal returns — to validate the pipeline and the timestamp
  handling, **not** to produce research findings.

**Pilot limitations (explicit).** A small convenience sample can validate that the
pipeline runs end-to-end and that timestamps are handled correctly; it **cannot**
establish a reliable trading edge. With few firms and a few quarters, estimates are
noisy, industry/regime heterogeneity cannot be identified, and any apparent result
is easily an artifact of one period or a handful of names. Stronger conclusions
require a much larger point-in-time universe, **pre-specified hypotheses**
registered before analysis, genuine **out-of-sample** (walk-forward) evaluation,
and **corrections or controls for multiple testing**. None of these is possible
with the pilot sample, and none is claimed here.

---

## 9. Risk register

| Risk | Description | Mitigation |
|---|---|---|
| **Licensing** | Transcript vendors restrict use/derivation; free archives restrict scraping | Confirm ToS before collection; prefer IR PDFs; keep `license_note` on every transcript |
| **Redistribution** | Scraped/licensed text cannot be committed or shared | Raw text stays in git-ignored `data/raw/`; commit only hashes/schemas |
| **Rate limits** | EDGAR 10 req/s; Alpha Vantage 25 req/day; others vary | Throttle + cache; budget requests; never assume a quota is unchanged |
| **Survivorship bias** | Free price feeds often omit delisted firms | Document the limitation; reserve CRSP/WRDS for research-grade runs |
| **Timestamp alignment** | Transcript publication time may post-date the call (and the close) | `max(published_at, next open)` rule; conservative next-day fallback |
| **Data quality** | Transcript formatting, speaker labels, OCR errors; free price gaps | Validate/schema-check on ingest; store content hashes; log provenance |
| **Overstated claims** | Treating EDGAR as a transcript source, or assuming free tiers | Facts labeled [VERIFIED]/[UNVERIFIED] throughout this memo |

---

## 10. Recommended approach

1. **Resolve the licensing question first.** Choose one transcript source and
   confirm its terms permit this research use. Company IR PDFs or a licensed
   aggregator are lower-risk than scraping free archives.
2. **Use EDGAR** (free, timestamped) for earnings releases, filing times, and as
   a fallback for the occasional filed transcript.
3. **Pilot with free/low-cost market data** (Alpha Vantage free tier) plus the
   **Ken French** benchmark library; plan a **CRSP/WRDS** upgrade for any
   research-grade, survivorship-aware analysis.
4. **Encode timestamps from day one** using the schema in §7 and the
   `max(published_at, next open)` rule.
5. **Keep the sample tiny** and validate the end-to-end workflow before scaling.

---

## 11. Unresolved questions

1. Which transcript source can we legally use for automated collection and
   internal research? (Needs a terms review — the single biggest blocker.)
2. Does the chosen transcript source expose a **machine-readable publication
   timestamp**, or only a date?
3. Can we obtain **point-in-time consensus estimates** (for earnings surprise)
   free, or is a WRDS/IBES subscription required?
4. What are the current, exact free-tier limits for Tiingo, Polygon/"Massive",
   Finnhub, and FMP? (Several pages did not render; figures are second-hand.)
5. Do we have access to a **WRDS subscription** (CRSP, Compustat, I/B/E/S,
   Capital IQ Transcripts) through an institution? This changes the plan materially.
6. What is the acceptable **redistribution boundary** — is storing raw transcript
   text locally (git-ignored) sufficient, or must even derived features be
   restricted?
7. How should ticker/CIK/PERMNO changes over time be reconciled for point-in-time
   universes?

---

## 12. Sources consulted (accessed 2026-10-13)

- SEC.gov — "Developer Resources" (Fair Access, `data.sec.gov` APIs, 10 req/s cap).
- SEC.gov — EDGAR full-text search and example Form 8-K filing a transcript as
  Exhibit 99.1.
- Alpha Vantage — Customer Support (free tier: 25 requests/day; premium realtime;
  split/dividend-adjusted data).
- Seeking Alpha — "Transcripts" page (≈6-hour publication delay) and Terms of Use.
- The Motley Fool — earnings-call-transcripts archive page (scraping restriction
  reported second-hand; ToS not fetched).
- Kaggle — "Scraped Motley Fool Earnings Call Transcripts" (License: Unknown).
- WRDS — "Capital IQ Transcripts" and S&P Global transcripts announcements;
  Fama-French factor data vendor page.
- LSEG — Company Transcripts data catalogue page.
- Ken French Data Library — Dartmouth.
- Finnhub, Financial Modeling Prep, Nasdaq Data Link (ZEEH) — earnings-surprise and
  estimate product pages.
- Microsoft and Meta investor-relations event pages (transcript availability
  behavior).

> Details marked **[UNVERIFIED]** above must be re-checked against provider terms
> at integration time; this memo deliberately does not assert unconfirmed prices,
> quotas, or endpoints.
