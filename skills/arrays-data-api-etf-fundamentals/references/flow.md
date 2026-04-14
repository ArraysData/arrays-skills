# ETF Flow

`GET /api/v1/etf/flow`

Retrieve ETF in/outflow data. Includes daily close, net flow in shares, volume, and FOMC day indicator.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `tickers` | string | yes | Comma-separated ETF symbols (e.g., SPY,QQQ,IWM) |
| `start_time` | integer | no | Start time (Unix timestamp in seconds) |
| `end_time` | integer | no | End time (Unix timestamp in seconds) |

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | ETF symbol |
| `date` | string | Flow date (YYYY-MM-DD) |
| `close` | string | Daily closing price |
| `net_flow_in_shares` | integer | Net flow in number of shares |
| `volume` | integer | Daily trading volume |
| `net_flow` | string | Net fund flow amount in USD (positive = inflow, negative = outflow) |
| `expiration_cycle` | string | Options expiration cycle (e.g., "weekly") |
| `is_fomc` | boolean | Whether the date is an FOMC meeting day |
