---
name: arrays-skill-creator
description: Step-by-step guide for creating new Arrays data API skills. Use when the user wants to create a new skill, write skill documentation, or add a new API domain to the skills library.
---


# Arrays Skill Creator

A step-by-step guide for creating a new Arrays data API skill. Follow every section in order.

> **Scope**: This guide covers `arrays-data-api-*` skills that call Arrays' own REST API (`data-tools.prd.space.id`). Skills wrapping external third-party APIs (e.g. Polymarket) are **not** covered here.

## Workflow

1. First check if the new endpoint belongs to an existing domain (the top-level folders under the `skills/` directory).
2. If you find a match, go to "## 4. Reference file format" directly to generate the reference markdown file. Then read the current SKILL.md file of the chosen domain and "## 3. SKILL.md format" below, and update the frontmatter, endpoint list, and python examples accordingly.
3. If the new endpoint doesn't fit into any of the existing domains, suggest a new one and pause for user confirmation. Once the user confirms or gives a new suggestion, create the new domain with the instructions below.

## Prerequisites

Before starting, set up the environment variables for API access:

```bash
export ARRAYS_API_BASE_URL=https://data-tools.prd.space.id
export ARRAYS_API_KEY=2f21e762-fa1c-4eb8-a8ce-ec8c1e138812
```

You will need these to call endpoints directly for verifying parameters and running python examples.

## 1. Choose a domain name

**Naming convention**: `arrays-data-api-{domain-name}`

| Domain slug | Skill directory name |
|---|---|
| `crypto-futures-data` | `arrays-data-api-crypto-futures-data` |
| `equity-fundamentals` | `arrays-data-api-equity-fundamentals` |
| `spot-market-price-and-volume` | `arrays-data-api-spot-market-price-and-volume` |
| `options` | `arrays-data-api-options` |
| `crypto-exchange-flow` | `arrays-data-api-crypto-exchange-flow` |

## 2. Directory structure

```
skills/
  arrays-data-api-{domain-name}/
    SKILL.md                      # Main skill file
    references/
      {endpoint-slug-1}.md        # One file per endpoint
      {endpoint-slug-2}.md
```

- Every endpoint MUST have a matching `references/{file-slug}.md`.
- No other files needed.

## 3. SKILL.md format

Use `references/skill-template.md` as a starting point. The required sections in order:

### 3.1 Frontmatter

```yaml
---
name: arrays-data-api-{domain-name}
description: Calls Arrays REST APIs for {domain} — {data types}. Use when the user asks about {trigger phrases}.
---
```

- `name` MUST match the directory name.
- `description`: Two parts: what it does + when to use. Pack with keywords for routing.

**Good example**:
```yaml
description: Calls Arrays REST APIs for crypto derivatives data — funding rates, open interest, long-short ratios, and taker buy/sell volume. Use when the user asks about perpetual futures, funding costs, leveraged positions, derivatives market sentiment, or futures data for any cryptocurrency.
```

### 3.2 Title

```markdown
# Arrays Data API — {Human-Readable Domain Name}
```

Followed by a one-line summary (no heading).

### 3.3 Base URL and auth

Copy this exactly into every skill:

```markdown
## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.
```

### 3.4 Important notes

Use heading `## Important notes`. Add domain-specific gotchas as bullet points (e.g., data ordering, timezone, funding rate settlement times, fiscal quarter mapping).

### 3.5 Endpoints table

```markdown
## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `{path-segment}` | `{file-slug}` | {Short description} |
```

- `Path` is relative to the domain prefix. Do NOT include the full URL.
- `File` maps to `references/{file-slug}.md`.
- `Description` — keep it short.

Follow with:

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

### 3.6 Python example

To populate this section, first come up with one use case based on the description of this skill, and then generate python code for it. Make sure you are able to successfully run the python example.

Key rules:
- Read `base` and `key` from `os.environ`
- Check `body["success"]` before reading `body["data"]`

## 4. Reference file format

Use `references/reference-template.md` as a starting point. Each file documents one endpoint:

1. `# {Name}` + `` `GET /api/v1/{asset-class}/{path}` ``
2. Parameters table: Param | Type | Required | Description
3. Response JSON example
4. Response fields table: Field | Type | Description
5. End with `---`


