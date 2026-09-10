---
name: arrays-data-api-semiconductor-price
description: Guides the agent to call Arrays REST APIs for semiconductor price data (DRAM spot & contract price, NAND Flash spot & contract price, Memory Card price, DXI index). Use when the user asks about DRAM prices, DDR3/DDR4/DDR5 memory pricing, NAND Flash prices (MLC/SLC), MicroSD card prices, contract/long-term memory pricing, the DXI memory index, or semiconductor component pricing trends.
---

# Arrays Data API — Semiconductor Price

**Domain**: `semiconductor_price`. Spot and contract prices for DRAM and NAND Flash,
Memory Card prices, and the DXI memory index.

> **Data frequency differs by endpoint:**
> - **DRAM spot price → DAILY** (trading days — Mon–Fri, excluding holidays)
> - **DXI index → DAILY** (trading days — Mon–Fri, excluding holidays)
> - **NAND Flash spot price → WEEKLY**
> - **Memory Card price → WEEKLY**
> - **DRAM / NAND Flash contract price → MONTHLY**
>
> A "latest price" query on a weekly/monthly endpoint returns nothing if you only
> look back 1–2 days — widen the window (e.g., 14–21 days for weekly, 30–60 days for monthly) and take the row with the newest 'date'.

## Price type — spot vs contract

- **Spot price** — small-lot, open-market transactions, quoted each trading session;
  more volatile. Endpoints: `dram-spot-price`, `nand-flash-spot-price`, `memory-card-price`.
- **Contract price** — negotiated long-term supply agreements between manufacturers and
  large buyers; monthly cadence, less volatile. Endpoints: `dram-contract-price`,
  `nand-flash-contract-price`.

Spot and contract are distinct series with **different `item` dictionaries** — do not
mix them or substitute one for the other.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

- **Prefix**: `/api/v1/other/semiconductor/`

| Method | Path | File | Frequency | Description |
|--------|------|------|-----------|-------------|
| GET | `dram-spot-price` | `dram-spot-price` | Daily | DRAM spot price (DDR3/DDR4/DDR5, 19 items) |
| GET | `dram-contract-price` | `dram-contract-price` | Monthly | DRAM contract price (DDR2–DDR5 + SO-DIMM/U-DIMM, 19 items) |
| GET | `nand-flash-spot-price` | `nand-flash-spot-price` | Weekly | NAND Flash spot price (MLC/SLC, 9 items) |
| GET | `nand-flash-contract-price` | `nand-flash-contract-price` | Monthly | NAND Flash contract price (MLC/SLC, 9 items) |
| GET | `memory-card-price` | `memory-card-price` | Weekly | Memory Card price (MicroSD, 6 items) |
| GET | `dxi-index` | `dxi-index` | Daily | DXI memory index (no `item`) |

> For detailed parameters, response fields, valid `item` values, and examples for
> a specific endpoint, read `references/<file>.md` in this skill directory. The five
> price endpoints share the same parameter set and `symbol/date/high/low/avg` schema;
> `dxi-index` has no `item` and a different response schema (see its reference).

## Important notes

- **`start_time` / `end_time` are Unix timestamps in seconds** (int), NOT date
  strings — passing `YYYY-MM-DD` returns a `VALIDATION_ERROR`. Compute them with
  `calendar.timegm` (see reference examples); avoid `datetime.timestamp()`, which
  applies the local timezone.
- **Response wrapper is flat**: read `body["data"]` (a list of rows). Always
  check `body["success"]` first.
- **Data ordering**: rows come back **ascending** by `date` (oldest first), so
  `data[-1]` is the latest row — the *opposite* of the macro historical
  endpoints, which are newest-first. Sorting by `date` yourself is still the
  safest way to take "first" / "last" / "latest".
- **`item` is case-sensitive** and must exactly match a valid value — no
  normalization. **Spot and contract use different `item` dictionaries**; see each
  reference file for its list. The live spec enum is authoritative for all five price
  endpoints — if a user names an item not listed, fetch
  `GET {BASE}/docs/output/v1_other_semiconductor_<path>_get.json` → `params[0].enum`
  before saying it doesn't exist.
- All prices are in **USD**. History depth differs by endpoint:
  **DRAM / NAND Flash spot & contract from 2022-01**; **Memory Card from 2024-10**;
  **DXI from 2025-01**.
- When the user says "DRAM"/"NAND"/"memory card" without naming an item, a common
  spot default is `DDR5 16Gb (2Gx8) 4800/5600` / `MLC 64Gb 8GBx8` / `MicroSD 128GB`
  (contract: `DDR4 8Gb 1Gx8` / `NAND 128Gb 16Gx8 MLC`); mention other items are available.

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/v1_other_semiconductor_<path>_get.json`.
