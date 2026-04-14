# Crypto OHLCV full bar

`GET crypto/ohlcv`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of KlineData items.

**Response fields:** Same KlineData fields as `crypto/kline` (see `crypto-kline.md`).
