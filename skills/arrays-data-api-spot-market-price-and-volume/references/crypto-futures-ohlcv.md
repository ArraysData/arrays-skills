# Crypto futures OHLCV full bar

`GET crypto/futures/ohlcv`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of KlineData items.

**Response fields:** Same KlineData fields as `crypto/ohlcv` (see `crypto-ohlcv.md`).
