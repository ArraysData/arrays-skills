# Insider Transactions

`GET /api/v1/stocks/insider/transactions`

Returns insider transaction data including officer/director status, SEC filings, transaction codes, and ownership changes.

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | No | Stock symbol (e.g., AAPL, TSLA) |
| `owner_name` | string | No | Filter by insider name (case-insensitive partial match) |
| `transaction_code` | string | No | SEC Form 4 transaction code (single letter, see table below) |
| `start_time` | integer | Yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | Yes | End time (Unix timestamp in seconds) |
| `time_type` | string | Yes | Date field to filter on: `TRANSACTION_DATE`, `FILING_DATE`, or `OBSERVED_AT` |
| `limit` | integer | No | Maximum number of records (1-5000, default 1000) |

#### Transaction codes (SEC Form 4)

**General**

| Code | Description |
|------|-------------|
| `P` | Open market or private purchase of non-derivative or derivative security |
| `S` | Open market or private sale of non-derivative or derivative security |
| `V` | Transaction voluntarily reported earlier than required |

**Rule 16b-3**

| Code | Description |
|------|-------------|
| `A` | Grant, award or other acquisition pursuant to Rule 16b-3(d) |
| `D` | Disposition to the issuer of issuer equity securities pursuant to Rule 16b-3(e) |
| `F` | Payment of exercise price or tax liability by delivering or withholding securities incident to the receipt, exercise or vesting of a security issued in accordance with Rule 16b-3 |
| `I` | Discretionary transaction in accordance with Rule 16b-3(f) resulting in acquisition or disposition of issuer securities |
| `M` | Exercise or conversion of derivative security exempted pursuant to Rule 16b-3 |

**Derivative Securities** (except transactions exempted pursuant to Rule 16b-3)

| Code | Description |
|------|-------------|
| `C` | Conversion of derivative security |
| `E` | Expiration of short derivative position |
| `H` | Expiration (or cancellation) of long derivative position with value received |
| `O` | Exercise of out-of-the-money derivative security |
| `X` | Exercise of in-the-money or at-the-money derivative security |

**Other Section 16(b) Exempt Transaction and Small Acquisition** (except Rule 16b-3 codes above)

| Code | Description |
|------|-------------|
| `G` | Bona fide gift |
| `L` | Small acquisition under Rule 16a-6 |
| `W` | Acquisition or disposition by will or the laws of descent and distribution |
| `Z` | Deposit into or withdrawal from voting trust |

**Other**

| Code | Description |
|------|-------------|
| `J` | Other acquisition or disposition (describe transaction) |
| `K` | Transaction in equity swap or instrument with similar characteristics |
| `U` | Disposition pursuant to a tender of shares in a change of control transaction |

#### Response

```json
{
  "success": true,
  "data": [
    {
      "symbol": "AAPL",
      "tx_id": "e4d80b94-...",
      "owner_name": "COOK TIMOTHY D",
      "transaction_code": "S",
      "amount": "-108136.000000",
      "price": "229.0700",
      "filing_date": "2025-04-17",
      "transaction_date": "2025-04-15",
      ...
    }
  ]
}
```

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `tx_id` | string | Unique transaction ID |
| `owner_name` | string | Insider's name |
| `transaction_code` | string | SEC transaction code (`P` = Purchase, `S` = Sale) |
| `amount` | string | Shares transacted (negative = sale, positive = purchase) |
| `price` | string | Transaction price per share |
| `transactions` | integer | Number of transactions |
| `sector` | string | Company sector |
| `filing_date` | string | SEC filing date |
| `transaction_date` | string | Transaction date |
| `observed_at` | int64 | Observed timestamp (Unix seconds) |
| `is_officer` | boolean | Whether insider is an officer |
| `is_director` | boolean | Whether insider is a director |
| `is_ten_percent_owner` | boolean | Whether insider is a 10%+ owner |
| `security_title` | string | Security name (e.g., "Common Stock") |
| `form_type` | string | SEC form type (e.g., "4") |
| `is_10b51` | boolean | Whether trade is under a 10b5-1 plan |
| `security_ad_code` | string | Acquisition/Disposition code |
| `shares_owned_after` | string | Shares owned after transaction |
| `shares_owned_before` | string | Shares owned before transaction |
| `officer_title` | string | Officer title (empty if not officer) |
| `market_cap` | string | Company market cap at time of trade |
| `is_sp500` | boolean | Whether company is in S&P 500 |
| `stock_price` | string | Stock price at time of trade |
