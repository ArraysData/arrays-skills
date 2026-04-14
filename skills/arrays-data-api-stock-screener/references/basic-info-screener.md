# Basic-info screener endpoints

`GET /api/v1/stocks/screener/basic-info/{sub}`

Each takes a single required parameter:

| Endpoint | Param | Values |
|----------|-------|--------|
| `screener/basic-info/country` | `country` | ISO alpha-2 codes: `US`, `CN`, `JP`, `GB`, `DE`, etc. |
| `screener/basic-info/exchange` | `exchange` | `AMEX`, `NASDAQ`, `NYSE` |
| `screener/basic-info/sector` | `sector` | Same GICS sectors as company screener |
| `screener/basic-info/industry` | `industry` | e.g. `Semiconductors`, `Banks Regional`, `Software Application` |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `type` | string | Screener dimension used: `sector`, `industry`, `country`, or `exchange` |
| `value` | string | The value that was matched (e.g. `Technology`, `US`, `NASDAQ`) |
