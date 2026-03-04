---
description: Full-lifecycle open-source contribution workflow
argument-hint: [phase] [url-or-args]
model: opus
---

Open-source contribution workflow. Route to the appropriate phase based on the argument provided.

## Argument Parsing

Parse `$ARGUMENTS` to determine the phase and any additional arguments (URLs, flags).

**Phase keywords:** `discover`, `analyze`, `work`, `test`, `submit`, `review`, `debug`, `pr-review`, `triage`, `sync`, `release`, `cleanup`

**With URL argument:** If a URL is provided after the phase keyword, pass it to that phase.
- `/contribute analyze https://github.com/owner/repo/issues/123` -> analyze phase with URL
- `/contribute pr-review https://github.com/owner/repo/pull/456` -> pr-review phase with URL
- `/contribute triage https://github.com/owner/repo/issues/789` -> triage phase with URL

**With flags:** `/contribute cleanup --dry-run` or `/contribute cleanup --full`

## Phase Routing

If a phase keyword is present, load the contribute skill and the corresponding reference file, then execute that phase:

| Keyword | Reference | Notes |
|---|---|---|
| `discover` | `references/phase-discover.md` | Launch issue-scout agent for parallel search |
| `analyze` | `references/phase-analyze.md` | Requires URL argument |
| `work` | `references/phase-work.md` | Requires prior analyze |
| `test` | `references/phase-test.md` | Launch deep-reviewer agent for Stage 5 |
| `submit` | `references/phase-submit.md` | Requires test score >= 85% |
| `review` | `references/phase-review.md` | Requires existing PR |
| `debug` | `references/phase-debug.md` | Requires existing PR with CI failure or review feedback |
| `pr-review` | `references/phase-pr-review.md` | Requires PR URL argument |
| `release` | `references/phase-release.md` | Requires push access |
| `triage` | `references/phase-triage.md` | Requires issue URL argument |
| `sync` | `references/phase-sync.md` | Must be inside a git repo |
| `cleanup` | `references/phase-cleanup.md` | Accepts `--dry-run` or `--full` flags |

## Auto-Detection (No Arguments)

If `/contribute` is invoked with no arguments, detect the appropriate phase from context:

1. Check if `.claude/contribute-conventions.md` exists. Read it for current status.

2. **If inside a git repo that is a fork:**
   ```bash
   gh repo view --json isFork --jq '.isFork' 2>/dev/null
   ```

   a. **Uncommitted changes exist** (`git status --porcelain` is non-empty):
      Suggest: "You have uncommitted changes. Want to continue with **work**, or run **test** on what you have?"

   b. **Feature branch with committed changes, no test report:**
      Suggest: "You have commits ready. Want to run **test** to validate before submitting?"

   c. **Feature branch with committed changes AND passing test report:**
      Check if `.claude/contribute-test-report.md` exists and score >= 85%.
      Suggest: "Tests pass. Ready to **submit**?"

   d. **Feature branch, no changes yet:**
      Suggest: "Branch is clean. Ready to start **work**?"

   e. **Default branch, no contribution state:**
      Suggest: "No active contribution. Want to **discover** an issue or **analyze** a specific one?"

3. **If `.claude/contribute-conventions.md` exists with `status: submitted`:**
   Check CI status on the PR branch:
   ```bash
   gh run list --repo <OWNER/REPO> --branch <BRANCH> \
     --limit 1 --json conclusion --jq '.[0].conclusion'
   ```
   If conclusion is `failure`:
   Suggest: "CI is failing on your PR. Want to run **debug** to diagnose and fix?"

   If CI is passing:
   Suggest: "PR is open. Want to check **review** status?"

4. **If not in a git repo or no fork detected:**
   Suggest: "Want to **discover** an issue to contribute to?"

5. **If none of the above match:**
   Present all available phases and ask the user to choose.

Always explain why a phase is suggested and let the user override.
