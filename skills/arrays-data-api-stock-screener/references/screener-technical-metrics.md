# Technical metrics screener

`GET /api/v1/stocks/screener/technical-metrics`

Covers US-listed stocks and ETFs (`symbol_type`) across NYSE, NASDAQ, NYSE American, NYSE Arca, and Cboe BZX (XNYS/XNAS/XASE/ARCX/BATS), with no size/liquidity floor — rankings include illiquid names. Filter with a `DOLLAR_VOLUME` range (works for both); for stocks you can also use `MARKET_CAP` (via `financial-metrics`). Each call filters only the queried metric.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `snapshot` | integer | yes | Snapshot time (Unix seconds, used directly for querying) |
| `metric_type` | string | yes | Technical metric to filter by (see list below) |
| `range_min` | float64 | no | Min value filter — returns stocks with value ≥ `range_min` |
| `range_max` | float64 | no | Max value filter — returns stocks with value ≤ `range_max` |
| `order_by` | string | no | Sort by metric value: `ASC` or `DESC` (default `DESC`) |
| `symbol_type` | string | no | Asset type filter: `stock` (CS/ADRC) or `etf`. Default `stock`. |

**Technical metric types:**

- **Price change**: `PRICE_CHANGE_1D`, `PRICE_CHANGE_1W`, `PRICE_CHANGE_1M`, `PRICE_CHANGE_3M`, `PRICE_CHANGE_6M`, `PRICE_CHANGE_YTD`, `PRICE_CHANGE_1Y`, `PRICE_CHANGE_3Y`, `PRICE_CHANGE_5Y`
- **Volume**: `SHARES_VOLUME`, `DOLLAR_VOLUME`, `AVERAGE_DAILY_DOLLAR_VOLUME`
- **Simple MA**: `MA_5`, `MA_10`, `MA_20`, `MA_60`, `MA_120`, `MA_200`
- **Exponential MA**: `EMA_5`, `EMA_10`, `EMA_20`, `EMA_60`, `EMA_120`, `EMA_200`
- **Momentum**: `RSI_14`
- **MACD components**: `MACD_DIF`, `MACD_DEA`, `MACD_HIST`
- **Bollinger components**: `BOLLINGER_UPPER`, `BOLLINGER_MID`, `BOLLINGER_LOWER`
- **Other**: `VWAP_DAY`, `BETA`, `VOLATILITY_20`, `VOLATILITY_60`, `VOLATILITY_90`

## Response

```json
{
  "success": true,
  "data": [
    {
      "symbol": "TFII",
      "snapshot_time": 1777060800,
      "date": "2026-04-24",
      "metric": "RSI_14",
      "value": 79.614817
    }
  ],
  "request_id": "..."
}
```

**Each item in `data`:**

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `snapshot_time` | int64 | Snapshot time (Unix seconds, UTC) |
| `date` | string | Snapshot date (`YYYY-MM-DD`) |
| `metric` | string | Metric type that was queried (echoes `metric_type`) |
| `value` | float64 | Metric value for this stock |
