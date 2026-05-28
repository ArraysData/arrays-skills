# Taker Buy Sell Volume

`GET /api/v1/crypto/taker-buy-sell-volume`

**CRITICAL**: `buy_vol` and `sell_vol` are in **base asset quantity** (e.g., ETH for ETHUSDT), NOT USD. To get USD volume, multiply by the token price from `crypto/binance/perp/usdt/kline` (the perp kline endpoint in this same skill).

**WARNING — DO NOT use this endpoint for "futures trading volume" queries.** This endpoint only provides taker buy/sell breakdown (in base asset, not USD). For total futures trading volume, use `crypto/binance/perp/usdt/kline` (also in this skill) — its `volume` field is in **base-asset units** (e.g. ETH for ETHUSDT); multiply by a representative bar price (e.g. `price_close`) to get USDT notional. Call it like this:
```python
resp = requests.get(f"{base}/api/v1/crypto/binance/perp/usdt/kline",
    params={"symbol": "ETH", "start_time": start, "end_time": end, "interval": "1d", "limit": 5},
    headers={"X-API-Key": key})
body = resp.json()
# Binance returns reverse chronological — match by date prefix on time_open (RFC 3339 string)
target = [d for d in body["data"] if d["time_open"].startswith("2025-09-06")]
bar = target[0] if target else body["data"][-1]
volume_usd = bar["volume"] * bar["price_close"]   # base × price = USDT notional
```

```json
{
  "success": true,
  "data": [
    { "buy_vol": 19037814781.55, "sell_vol": 18442110914.54, "buy_sell_ratio": 1.032, "timestamp": 1723507200 }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `buy_vol` | float64 | Taker buy volume in **base asset quantity** (e.g. ETH for ETHUSDT). Multiply by price to get USD. |
| `sell_vol` | float64 | Taker sell volume in **base asset quantity**. Multiply by price to get USD. |
| `buy_sell_ratio` | float64 | Buy/sell volume ratio. >1.0 means more buying pressure. |
| `timestamp` | int64 | Unix timestamp in seconds |
