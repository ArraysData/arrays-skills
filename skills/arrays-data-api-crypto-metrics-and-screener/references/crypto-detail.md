# Token detail

`GET /api/v1/crypto/detail`

Get the metadata profile for a token by its symbol — name, category, description, logo, contract addresses per chain, and official URLs.

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (e.g. `BTC`, `ETH`). Cannot be empty. |

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of TokenProfile objects.

Returns token metadata only. For price and volume, use the spot kline endpoints in this skill.

**Each item in `data` (TokenProfile):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol (e.g. `"BTC"`) |
| Name | `name` | string | Full token name (e.g. `"Bitcoin"`) |
| Category | `category` | string | Token category (e.g. `"coin"`) |
| Description | `description` | string | Token description |
| Logo | `logo` | string | URL to the token logo image |
| Contracts | `contracts` | array of object | Contract addresses per chain — each `{ "chain": string, "address": string }` |
| URLs | `urls` | object | Official URLs, each a list of strings (see below) |

**`urls` object:**

| JSON key | Type | Description |
|----------|------|-------------|
| `website` | array of string | Official website URLs |
| `twitter` | array of string | Twitter/X profile URLs |
| `reddit` | array of string | Reddit URLs |
| `explorer` | array of string | Block explorer URLs |
| `technical_doc` | array of string | Whitepaper / technical documentation URLs |
