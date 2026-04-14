# Options Kline

`GET /api/v1/options/kline`

Get historical K-line data for options contracts. Provides OHLCV metrics, VWAP, and trade count across specified time intervals.

**IMPORTANT — Two-step workflow for underlying symbol queries**: This endpoint requires a specific `options_ticker` (OCC format). When the user asks for options data by underlying symbol (e.g. "AAPL options OHLCV"), first call `/api/v1/options/contracts` with the underlying `symbol` to discover available contracts, then use the `options_ticker` from the result here.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Underlying symbol (e.g. `SPY`, `AAPL`) |
| `options_ticker` | string | yes | OCC-format options ticker (e.g. `O:SPY260620C00570000`) |
| `interval` | string | yes | Time interval: `1min`, `5min`, `15min`, `30min`, `1h`, `1d`, `1w`, `1m` |
| `start_time` | int | yes | Start time (Unix seconds) |
| `end_time` | int | yes | End time (Unix seconds) |
| `limit` | int | no | Max data points (default 500, max 10000) |
| `session` | string | no | Trading session: `RTH` (regular hours 9:30–16:15 ET) or `ETH` (default, all hours). Uppercase only. |

## Response

```json
{
  "success": true,
  "data": [
    {
      "options_ticker": "O:AAPL260410C00200000",
      "underlying_symbol": "AAPL",
      "time_open": 1775534400,
      "time_close": 1775620800,
      "price_open": 49.5,
      "price_close": 51.7,
      "price_low": 49.1,
      "price_high": 51.7,
      "trades_count": 4,
      "volume_traded": 65,
      "vwap": 50.053846
    }
  ],
  "request_id": "..."
}
```

**Each item in `data` (OptionsKlineData):**

| Field | Type | Description |
|-------|------|-------------|
| `options_ticker` | string | OCC-format ticker (e.g. `O:AAPL260410C00200000`) |
| `underlying_symbol` | string | Underlying stock ticker |
| `time_open` | integer | K-line open time (Unix seconds) |
| `time_close` | integer | K-line close time (Unix seconds) |
| `price_open` | number | Opening price |
| `price_close` | number | Closing price |
| `price_low` | number | Lowest price |
| `price_high` | number | Highest price |
| `trades_count` | integer | Number of trades |
| `volume_traded` | number | Trading volume (number of contracts) |
| `vwap` | number | Volume-weighted average price |

---
