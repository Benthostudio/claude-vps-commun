---
name: ship
description: "Commit, push, and deploy to Vercel. Returns the preview URL."
user_invocable: true
---

# Deploy to Vercel

Run the following steps sequentially:

1. `cd /Users/bentho/claudecode/pro/website-studio-makers`
2. Run `npx next build` to verify the build passes. If the build fails, stop and report the error. Do NOT push broken code.
3. Run `git status` to see what changed.
4. Run `git diff --stat` to see a summary of changes.
5. Run `git add -A`
6. Create a commit with a concise message describing the changes. Always end with:
   ```
   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
   ```
7. Run `git push`
8. Wait 35 seconds for Vercel to deploy.
9. Run `vercel ls 2>&1 | head -6` to get the deployment URL.
10. Report the deployment URL to the user in this format:

```
**Deployed:** <URL>
```

If the deployment status is still "Building", wait 15 more seconds and check again.
