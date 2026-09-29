---
name: compare-versions
description: "List all Vercel deployment URLs in a comparison table."
user_invocable: true
---

# Compare Versions

Run: `vercel ls 2>&1`

Parse the output and display ALL deployments as a clean markdown table with:
- Version number (V1, V2, V3... based on age, oldest first)
- Age
- Status
- Full deployment URL (as a clickable link)

Format:
```
| Version | Age | Status | URL |
|---------|-----|--------|-----|
| V1      | 5d  | Ready  | https://... |
| V2      | 4d  | Ready  | https://... |
```

Only show deployments with status "Ready".
