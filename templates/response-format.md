## Response format

**Standard** (most endpoints):
```json
{ "success": true, "response": [...], "total": 42, "pagination": { "next_cursor": "...", "has_more": true }, "request_id": "..." }
```

**V2** (screener, financial statements, on-chain metrics):
```json
{ "success": true, "data": [...], "request_id": "..." }
```

**Error**:
```json
{ "success": false, "error": { "code": "INVALID_TIMESTAMP", "message": "..." }, "request_id": "..." }
```

Always check `success` before reading `response` or `data`.
