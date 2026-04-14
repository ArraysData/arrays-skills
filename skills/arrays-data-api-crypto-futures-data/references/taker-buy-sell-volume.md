# Taker Buy Sell Volume

`GET /api/v1/crypto/taker-buy-sell-volume`

**CRITICAL**: `buy_vol` and `sell_vol` are in **base asset quantity** (e.g., ETH for ETHUSDT), NOT USD. To get USD volume, multiply by the token price from the `crypto/kline` endpoint.

**WARNING — DO NOT use this endpoint for "futures trading volume" queries.** This endpoint only provides taker buy/sell breakdown (in base asset, not USD). For total futures trading volume, you MUST use the `crypto/futures/ohlcv` endpoint instead — it returns `volume_traded` directly in **quote currency (USDT)** with no conversion needed. Call it like this:
```python
resp = requests.get(f"{base}/api/v1/crypto/futures/ohlcv",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end, "interval": "1d", "limit": 5},
    headers={"X-API-Key": key})
body = resp.json()
# Data is reverse chronological — use data[-1] for the target date
target = [d for d in body["data"] if d["time_period_start"].startswith("2025-09-06")]
volume_usd = target[0]["volume_traded"] if target else body["data"][-1]["volume_traded"]
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
