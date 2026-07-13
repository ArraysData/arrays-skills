# Sec Earnings Release

`GET /api/v1/stocks/sec-earnings-release`

Retrieve the SEC earnings release publication date and filing URL for a company's official earnings report, filed with the SEC for a specific fiscal period.

The underlying filing is an **8-K** for US domestic issuers and a **6-K** for foreign private issuers (ADRs). 

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, IBM) |
| `period_type` | string | Yes | `annual` or `quarterly`. `period_type=annual` returns the full-year earnings release as a single row with `quarter` = `YYYY00` (e.g. `202400` = FY2024 annual). This is the same underlying filing (8-K, or 6-K for foreign private issuers) as that fiscal year's Q4. Treat the annual release as the Q4 filing, not a separate event.|
| `fiscal_year` | integer | Yes | Fiscal year (≥ ~2005; e.g., 2024). Older fiscal years return a `NOT_FOUND` error rather than an empty `data` array. |
| `fiscal_quarter` | string | No | Fiscal quarter: `Q1`, `Q2`, `Q3`, `Q4` — required when period_type is `quarterly` |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `quarter` | string | Fiscal period identifier, `YYYYQQ`. Quarterly: `202401` = FY2024 Q1 … `202404` = Q4. Annual (`period_type=annual`): `YYYY00`, e.g. `202400` = FY2024 full year (same filing as that FY's Q4). |
| `release_date` | string | SEC publication date (YYYY-MM-DD) |
| `url` | string | URL to the SEC filing document |

---

## Freshness & live fallback when the SEC filing lags

This endpoint is sourced from **SEC EDGAR 8-K and 6-K filings**. Most 8-K and 6-K filings reach EDGAR the same day as the earnings release and are available in Arrays within minutes, except for two groups — **wire filers** (large caps reporting via Business Wire / GlobeNewswire + a call; 8-K ~1 day later) and **IR-only filers** (notably **Berkshire Hathaway BRK-A/BRK-B**; publish on their IR site 2–3 days before the 8-K). When the user needs the **just-released** results and this endpoint doesn't have them yet, fall back to the public source (IR site / newswire) — as a clearly-labeled, best-effort supplement.

**When to use the fallback** — trigger when ALL hold:
1. The user wants the **most recent** period (latest quarter/year), and
2. `sec-earnings-release` returns `NOT_FOUND` (or a period earlier than the period asked for), and
3. The company has released latest earnings.

**Fallback action (labeled, best-effort):**
- Known IR-only filer → fetch the IR page (Berkshire: `https://www.berkshirehathaway.com/news/news.html` + report links on `https://www.berkshirehathaway.com`).
- Otherwise → `WebSearch` for `"<company> Q<n> FY<year> earnings press release"` (or the company IR/newsroom) and fetch the release.
- Surface it **with explicit provenance**, e.g. *"Published on the company's IR site / newswire on <date>; the official SEC filing is not yet available."* Always include the source URL.

**Known IR-only late filers** (publish on IR site days before the 8-K; validated 2026-06):

| Symbol | IR source | Typical lag vs our data |
|--------|-----------|-------------------------|
| BRK-A | https://www.berkshirehathaway.com (Saturday post) | ~2 days before EDGAR 8-K |
| BRK-B | https://www.berkshirehathaway.com (Saturday post) | ~2 days before EDGAR 8-K |
