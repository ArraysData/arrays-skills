# Financial metrics screener

`GET /api/v1/stocks/screener/financial-metrics`

Covers US-listed stocks on NYSE, NASDAQ, and NYSE American (XNYS/XNAS/XASE), with no size/liquidity floor — rankings include microcaps and illiquid names. Add a `MARKET_CAP` range filter (size) or a `DOLLAR_VOLUME` screen via `technical-metrics` (liquidity); each call filters only the queried metric.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `snapshot` | integer | yes | Snapshot time (Unix seconds, used directly for querying) |
| `metric_type` | string | yes | Financial metric to filter by (see list below) |
| `range_min` | float64 | no | Min value filter — returns stocks with value ≥ `range_min` |
| `range_max` | float64 | no | Max value filter — returns stocks with value ≤ `range_max` |
| `order_by` | string | no | Sort by metric value: `ASC` or `DESC` (default `DESC`) |

**Financial metric types:**

- **PIT balance-sheet ratios (MRQ)**: `CURRENT_RATIO_MRQ`, `QUICK_RATIO_MRQ`, `DEBT_TO_ASSETS_MRQ`, `DEBT_TO_EQUITY_MRQ`, `NET_WORKING_CAPITAL_MRQ`
- **TTM base metrics**: `REVENUE_TTM`, `NET_INCOME_TTM`, `EPS_TTM`
- **TTM profitability**: `ROA_TTM`, `ROE_TTM`, `ROIC_TTM`
- **MRQ margins**: `GROSS_MARGIN_MRQ`, `OPERATING_MARGIN_MRQ`, `NET_MARGIN_MRQ`, `FCF_MARGIN_MRQ`
- **Other**: `RD_TO_SALES_TTM`
- **Revenue growth**: `REVENUE_GROWTH_QOQ`, `REVENUE_GROWTH_YOY_QUARTERLY`, `REVENUE_GROWTH_YOY_TTM`, `REVENUE_GROWTH_YOY_ANNUAL`
- **EPS growth**: `EPS_GROWTH_QOQ`, `EPS_GROWTH_YOY_QUARTERLY`, `EPS_GROWTH_YOY_TTM`, `EPS_GROWTH_YOY_ANNUAL`
- **FCF growth**: `FCF_GROWTH_QOQ`, `FCF_GROWTH_YOY_QUARTERLY`, `FCF_GROWTH_YOY_TTM`, `FCF_GROWTH_YOY_ANNUAL`
- **Price-derived valuation**: `MARKET_CAP`, `PE_RATIO`, `PS_RATIO`, `PB_RATIO`, `DIVIDEND_YIELD`, `ENTERPRISE_VALUE`, `EV_EBITDA_RATIO`

## Response

```json
{
  "success": true,
  "data": [
    {
      "symbol": "NVDA",
      "snapshot_time": 1777060800,
      "date": "2026-04-24",
      "metric": "MARKET_CAP",
      "value": 5062002467464.28
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
