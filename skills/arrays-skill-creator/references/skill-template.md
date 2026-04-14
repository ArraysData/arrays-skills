# SKILL.md Template

Use this skeleton to create a new SKILL.md. Refer to the guide in `SKILL.md` for detailed rules on each section.

---

```yaml
---
name: arrays-data-api-{domain-name}
description: {what it does + when to use}
---
```

```markdown
# Arrays Data API — {Domain Human Name}

{One-line summary}

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

<!-- Add domain-specific notes: data ordering, timezone, gotchas, etc. -->

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|

> For detailed parameters, response fields, and examples, read `references/<file>.md` in this skill directory.

## Python example

<!-- Come up with a use case, generate code, and verify it runs successfully. -->
```
