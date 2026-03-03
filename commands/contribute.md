---
description: Full-lifecycle open-source contribution workflow
argument-hint: [phase] [url-or-args]
model: opus
---

Open-source contribution workflow. Route to the appropriate phase based on the argument provided.

## Argument Parsing

Parse `$ARGUMENTS` to determine the phase and any additional arguments (URLs, flags).

**Phase keywords:** `discover`, `analyze`, `work`, `test`, `submit`, `review`, `pr-review`, `triage`, `sync`, `release`, `cleanup`

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
| `pr-review` | `references/phase-pr-review.md` | Requires PR URL argument |
| `release` | `references/phase-release.md` | Requires push access |
| `triage` | `references/phase-triage.md` | Requires issue URL argument |
| `sync` | `references/phase-sync.md` | Must be inside a git repo |
| `cleanup` | `references/phase-cleanup.md` | Accepts `--dry-run` or `--full` flags |

## Auto-Detection (No Arguments)

If `/contribute` is invoked with no arguments, detect the appropriate phase from context:

1. Check if `.claude/contribute-conventions.md` exists. Read it for current status.

2. **Resume from discover shortlist:**
   If `.claude/contribute-discover.md` exists but `.claude/contribute-conventions.md` does not, the user completed discover but never analyzed.
   Suggest: "You have a discover shortlist from a previous session. Want to **analyze** one of those issues?"

3. **If inside a git repo that is a fork:**
   ```bash
   gh repo view --json isFork --jq '.isFork' 2>/dev/null
   ```

   a. **Uncommitted changes exist** (`git status --porcelain` is non-empty):
      Suggest: "You have uncommitted changes. Want to continue with **work**, or run **test** on what you have?"

   b. **Conventions brief exists but no commits on feature branch** (analyze completed, work not started):
      Check if `.claude/contribute-conventions.md` exists with `status: analyzing` and `git log main..HEAD --oneline` is empty.
      Suggest: "Analysis is ready but no code changes yet. Ready to start **work**?"

   c. **Feature branch with committed changes, no test report:**
      Suggest: "You have commits ready. Want to run **test** to validate before submitting?"

   d. **Feature branch with committed changes AND passing test report:**
      Check if `.claude/contribute-test-report.md` exists and score >= 85%.
      Suggest: "Tests pass. Ready to **submit**?"

   e. **Feature branch, no changes yet (no brief):**
      Suggest: "Branch is clean. Ready to start **work**?"

   f. **Default branch, no contribution state:**
      Suggest: "No active contribution. Want to **discover** an issue or **analyze** a specific one?"

4. **If `.claude/contribute-conventions.md` exists with `status: submitted`:**
   Suggest: "PR is open. Want to check **review** status?"

5. **If not in a git repo or no fork detected:**
   Suggest: "Want to **discover** an issue to contribute to?"

6. **If none of the above match:**
   Present all available phases and ask the user to choose.

Always explain why a phase is suggested and let the user override.
