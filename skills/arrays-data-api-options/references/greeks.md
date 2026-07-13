# Options Greeks

`GET /api/v1/options/greeks`

Historical daily, in-house-computed option Greeks (delta, gamma, theta, vega) and implied volatility for a single option contract over a date range — one row per trading day, ordered by date ascending. Greeks come from a Cox-Ross-Rubinstein binomial tree; IV is reverse-solved from the contract's daily close. This is Arrays' own calculation (independent of any third-party Greeks), backed by ~12 years of history including delisted underlyings.

**Daily historical, not real-time** — latest date tracks the upstream daily kline sync (≈ T-1). For a same-snapshot view of every contract on an underlying (OHLCV + Greeks together), use `/api/v1/options/chain`.

**IMPORTANT — requires a specific `options_ticker`**: Like kline, this takes an OCC-format contract ticker, not an underlying symbol. To go from an underlying (e.g. "AAPL Greeks"), first call `/api/v1/options/contracts` with the underlying `symbol` to find the contract, then pass its `options_ticker` here.

**Greeks may be null on some days**: The 5 computed fields (`implied_volatility`, `delta`, `gamma`, `theta`, `vega`) can be null (the API omits the key) when the model can't solve them — see the `status` table. The other fields (`date`, `time_open`, `time_close`, `spot_price`, `option_close`, `risk_free_rate`, `dividend_yield`, `dte`) are always present. Guard with `.get()` before reading any Greek.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `options_ticker` | string | yes | OCC-format contract ticker, e.g. `O:AAPL260615P00300000`. Format: `O:` + underlying + `YYMMDD` (expiry) + `C`/`P` + 8-digit strike×1000 |
| `start_date` | string | yes | Inclusive start (`YYYY-MM-DD`) |
| `end_date` | string | yes | Inclusive end (`YYYY-MM-DD`). Must be ≥ `start_date` |

## Response

```json
{
  "success": true,
  "data": [
    {
      "options_ticker": "O:AAPL260615P00300000",
      "underlying_symbol": "AAPL",
      "date": "2026-06-01",
      "time_open": 1780320600,
      "time_close": 1780344000,
      "implied_volatility": 0.2504,
      "delta": -0.3185,
      "gamma": 0.0123,
      "theta": -0.0456,
      "vega": 0.1789,
      "spot_price": 290.55,
      "option_close": 11.20,
      "risk_free_rate": 0.0369,
      "dividend_yield": 0.0042,
      "dte": 14,
      "status": "ok"
    }
  ],
  "request_id": "..."
}
```

**Each item in the `data` array (OptionsGreeksData):**

| Field | Type | Description |
|-------|------|-------------|
| `options_ticker` | string | OCC-format ticker |
| `underlying_symbol` | string | Underlying stock ticker |
| `date` | string | Trading day (`YYYY-MM-DD`) |
| `time_open` | integer | Regular-session open for `date` (Unix seconds; 09:30 ET) |
| `time_close` | integer | Regular-session close for `date` (Unix seconds; 16:00 ET) |
| `implied_volatility` | number | Annualized IV, decimal (`0.25` = 25%). Nullable |
| `delta` | number | ∂price/∂spot per $1 underlying move. Calls ≈ 0…1, puts ≈ −1…0. Nullable |
| `gamma` | number | ∂delta/∂spot per $1 underlying move. Nullable |
| `theta` | number | Time decay, $ change per calendar day (usually negative). Nullable |
| `vega` | number | $ change per +1 percentage point (1%) of IV. Nullable |
| `spot_price` | number | Input. Underlying close that day ($) |
| `option_close` | number | Input. Option daily close ($), used as the market price to solve IV |
| `risk_free_rate` | number | Input. Risk-free rate, decimal (`0.0369` = 3.69%); treasury tenor picked by DTE |
| `dividend_yield` | number | Input. Continuous dividend yield, decimal; `0` when unavailable |
| `dte` | integer | Days to expiration (calendar days from `date` to expiry) |
| `status` | string | Computation quality flag — see below |

**`status` values** — when several apply, only the highest-priority one is reported (high → low):

| Value | Meaning | Greeks/IV present? |
|-------|---------|--------------------|
| `iv_failed` | IV solve did not converge (usually stale data / option close below intrinsic) | null |
| `pricing_failed` | IV solved, but a later pricing/Vega step errored | IV present; 4 Greeks null |
| `low_precision_short_dte` | DTE = 1; binomial precision is low one day to expiry | present |
| `r_fallback` | No treasury rate on the exact date; used nearest within ±7 days | present |
| `q_default` | Dividend yield not found; `q = 0` used as input | present |
| `ok` | Computed cleanly with all inputs present | present |

Any status other than `ok` flags one imperfection of that row; the row is still usable except where Greeks are null.

**Index options not supported** — `greeks` requires a stock/ETF underlying (it needs the underlying spot to compute). Index underlyings (e.g. `SPX`, `NDX`, `RUT`, `VIX`, `XSP`, `DJX`) are rejected with `INVALID_PARAMETER: stock symbol not found`. The same applies to any ticker whose underlying isn't a known stock/ETF.

The response returns a flat `data` array (no pagination), plus `request_id`.

---
