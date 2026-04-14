# Known Issues — Eval Test Cases

Cases that cannot reliably pass due to external data limitations or methodology mismatches.
The structural ceiling with these excluded is approximately **83.3%** (50/60 on the simple-tests subset).

## Unfixable Cases (8)

| Case ID | Reason |
|---------|--------|
| 38 | CPI data not available from the API |
| 57 | Wrong expected answer in the dataset |
| 60 | BLS data revision — expected answer is stale |
| 123 | Analyst count not returned by the API |
| 197 | DeFi Llama API returns HTTP 500 intermittently |
| 213 | Correlation methodology mismatch between expected and computed |
| 239 | Token unlock data range doesn't cover the expected period |
| 265 | Token unlock data range doesn't cover the expected period |

## Stochastic Cases (2)

| Case ID | Reason |
|---------|--------|
| 10 | AMD current ratio — value fluctuates near the pass/fail threshold |
| 598 | Jobless claims — date filter sensitivity causes inconsistent results |

## How to Use

When analyzing eval failures, cross-reference failing case IDs against this list.
If a failure matches a known issue, it should not be counted as a regression.
Flag only **new** failures (cases not in this list) as actionable.
