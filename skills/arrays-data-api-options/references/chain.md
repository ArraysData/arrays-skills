# Options Chain

`GET /api/v1/options/chain`

Snapshot of an entire option chain for one underlying — every (non-expired) contract with its daily OHLCV, Greeks, implied volatility, open interest, break-even, and fair market value, plus the underlying's price. Use this to scan a whole chain at once; for a single contract's time series use `kline` (OHLCV) or `greeks`.

**Previous-day snapshot, not real-time** — `daily_data` reflects the last completed trading session and the underlying is delayed. Expired contracts are excluded.

**Index options not supported** — like `greeks`, `chain` requires a stock/ETF underlying. Index underlyings (e.g. `SPX`, `NDX`, `RUT`, `VIX`, `XSP`, `DJX`) are rejected with `INVALID_PARAMETER: stock symbol not found`.

**`option_ticker` takes NO `O:` prefix**: Unlike `kline`/`greeks` (which use `options_ticker` *with* the `O:` prefix), the chain `option_ticker` param is the bare OCC symbol, e.g. `AAPL260612C00120000`. Contract `details.symbol` in the response is also returned without the prefix.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Underlying ticker, uppercase (e.g. `AAPL`, `SPY`) |
| `limit` | int | yes | Results per page. Use ≤ 250 — values above 250 currently error; page with `cursor` for more |
| `option_ticker` | string | no | Single bare OCC symbol, **no `O:` prefix** (e.g. `AAPL260612C00120000`) |
| `contract_type` | string | no | `call` or `put` |
| `min_strike_price` | number | no | Min strike filter |
| `max_strike_price` | number | no | Max strike filter |
| `start_expiration_date` | int | no | Min expiration, Unix seconds |
| `end_expiration_date` | int | no | Max expiration, Unix seconds |
| `cursor` | string | no | Pagination cursor |

## Response

The `data` array holds a single object whose `results` array carries the contracts. Pagination is on the top-level `pagination` envelope (`cursor` is mirrored inside `data[0]`).

```json
{
  "success": true,
  "data": [
    {
      "results": [
        {
          "break_even_price": 295.525,
          "daily_data": {
            "open": 171.996, "high": 176.811, "low": 169.771, "close": 175.525,
            "previous_close": 172.94, "change": 2.585, "change_percent": 1.495,
            "last_updated": 1781150400000000000
          },
          "details": {
            "symbol": "AAPL260612C00120000",
            "contract_type": "call", "exercise_style": "american",
            "expiration_date": "2026-06-12", "strike_price": 120,
            "shares_per_contract": 100
          },
          "greeks": { "delta": 0.69, "gamma": 0.03, "theta": -0.12, "vega": 0.18 },
          "implied_volatility": 0.245,
          "open_interest": 3,
          "underlying_asset": {
            "symbol": "AAPL", "price": 296.31, "change_to_break_even": -0.785,
            "timeframe": "DELAYED", "last_updated": 1781252728879698899
          },
          "fmv": 175.525
        }
      ],
      "cursor": "..."
    }
  ],
  "pagination": { "limit": 0, "cursor": "...", "has_more": true },
  "request_id": "..."
}
```

**Each item in `data[0].results` (OptionsChainContract):**

| Field | Type | Description |
|-------|------|-------------|
| `break_even_price` | number | Underlying price at which the position breaks even |
| `implied_volatility` | number | Annualized IV, decimal; `0` when unavailable |
| `open_interest` | integer | Open contracts; omitted/`0` when unavailable |
| `fmv` | number | Fair market value of the contract |
| `daily_data` | object | Latest session OHLCV — see below |
| `details` | object | Contract specification — see below |
| `greeks` | object | `delta`, `gamma`, `theta`, `vega`; all `0` when unavailable |
| `underlying_asset` | object | Underlying price snapshot — see below |

**`daily_data` fields:** `open`, `high`, `low`, `close`, `previous_close`, `change`, `change_percent` (numbers), `last_updated` (integer, Unix **nanoseconds**).

**`details` fields:** `symbol` (bare OCC, no `O:`), `contract_type` (`call`/`put`), `exercise_style`, `expiration_date` (`YYYY-MM-DD`), `strike_price` (number), `shares_per_contract` (integer).

**`underlying_asset` fields:** `symbol`, `price`, `change_to_break_even` (numbers), `timeframe` (string, e.g. `DELAYED`), `last_updated` (integer, Unix **nanoseconds**).

Greeks, IV, and open interest may be `0` on illiquid or far-from-the-money contracts. For pagination, check top-level `pagination.has_more`; if `true`, pass `pagination.cursor` as `cursor` in the next request.

---
