# KPI

`GET /api/v1/stocks/company/kpi`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase |
| `fiscal_year` | int | yes | Fiscal year (e.g. `2024`) |
| `fiscal_quarter` | string | yes | `Q1`, `Q2`, `Q3`, `Q4`, or `FY` (for annual) |

**IMPORTANT**: KPI metric names vary by company. A metric value of `0` or `null` may indicate a name mismatch, not actual zero. When searching for a specific KPI:
- First retrieve all metrics without filtering, then match by partial case-insensitive string matching on the `name` field.
- **When looking for revenue**, prioritize metrics ending with `_revenue` (e.g., `sams_club_revenue`, `linkedin_revenue`) over metrics containing "sales" (which may match growth rates like `comparable_sales_growth`). Match `_revenue` first, then fall back to broader matching.
- For segment revenue (e.g., Home Depot's "Building Materials"), look for the closest matching metric name.

**KPI metric name matching**: When searching for a category's total revenue (e.g., "building materials revenue"), **always prefer the metric with `total_` prefix** (e.g., `total_building_materials_revenue`) over the base name (e.g., `building_materials_revenue`). The base-name metric is often a sub-component that may be zero, while the `total_` variant is the correct aggregate. Pattern:
```python
# Find the right metric — prefer total_ prefix
target = "building_materials"
best = None
for m in all_metrics:
    name = m["name"].lower()
    if f"total_{target}_revenue" == name:
        best = m
        break  # exact total match — done
    if target in name and "revenue" in name and not best:
        best = m  # fallback
print(best["value"] if best else "API_ERROR: metric not found")
```

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `period_type` | string | Period type (`annual`, `quarterly`) |
| `period_id` | string | Unique period identifier |
| `calendar_end_date` | string | Report date (`YYYY-MM-DD`) |
| `calendar_year` | int32 | Calendar year |
| `calendar_quarter` | string | Calendar quarter (`Q1`-`Q4`) |
| `fiscal_year` | int32 | Fiscal year |
| `fiscal_quarter` | string | Fiscal quarter (`Q1`-`Q4`) |
| `metrics` | array | KPI metrics as array of `{name, value}` pairs (e.g. `[{"name": "total_building_materials_revenue", "value": 123456}]`) |
