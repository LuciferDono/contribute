# Design: Debug Phase

**Date:** 2026-03-04
**Status:** Approved
**Approach:** Lightweight debug step (Approach A)

## Summary

Add a new `debug` phase to the /contribute plugin that handles
post-commit debugging. Triggered after `review` detects a CI
failure or maintainer-reported bug. Focused on CI log analysis
and targeted fixes — not deep root cause analysis or bisecting.

## Position in Pipeline

```
review -> debug -> test -> submit (force-push)
```

Debug is invoked after review identifies a problem. After fixing,
the user re-runs test (85% gate still applies) and pushes.

## Phase Design: `/contribute debug`

### Entry Point

`/contribute debug`

### Prerequisite

A PR must exist and either CI has failed or a maintainer has
flagged a bug. Reads `.claude/contribute-conventions.md` for
repo/branch/issue context.

### Step 1: Identify the Failure Source

Two entry paths, auto-detected:

1. **CI failure** — Fetch failed run logs:
   ```bash
   gh run list --repo <OWNER/REPO> --branch <BRANCH> \
     --limit 1 --json databaseId,conclusion
   gh run view <RUN_ID> --repo <OWNER/REPO> --log-failed
   ```

2. **Maintainer comment** — Fetch review comments:
   ```bash
   gh pr view <PR_NUMBER> --repo <OWNER/REPO> \
     --json reviews,comments
   ```

Auto-detect: check CI status first. If passing, check for
"changes requested" reviews.

### Step 2: Map Failure to Changed Code

- Get the diff: `git diff <DEFAULT_BRANCH>...HEAD`
- Parse error messages from CI logs or reviewer comments
- Correlate failures to specific files and lines in the diff
- Present a structured diagnosis:
  ```
  ## Diagnosis

  Source: CI / Reviewer comment
  Failure: <what failed>
  File: <path>:<line>
  Cause: <brief explanation>
  Suggested fix: <description>
  ```

### Step 3: Apply Fix

Respect the operating mode from conventions:
- **do** — Apply the fix directly, show the diff
- **guide** — Explain the fix, provide snippets, user applies
- **adaptive** — Apply mechanical fixes, consult on logic

### Step 4: Re-validate and Push

1. Run `/contribute test` — 85% gate still applies
2. If passing, push with `--force-with-lease` (ask permission)
3. Update conventions: `status: debugging -> submitted`

## State

No new state file. Reads `contribute-conventions.md` and
`contribute-test-report.md`. Test phase overwrites its report
on re-run as usual.

## Files to Create

- `skills/contribute/references/phase-debug.md` — Phase reference

## Files to Modify

- `skills/contribute/SKILL.md` — Add Debug row to routing table,
  update dependency diagram, update phase count (11 -> 12)
- `commands/contribute.md` — Add `debug` keyword to routing and
  auto-detection
- `README.md` — Add Debug to core workflow table and phase count

## Design Decisions

- **No new agent** — CI log parsing and diff correlation do not
  need isolated parallel work. The main context handles it.
- **No new state file** — Debug is a transient fix cycle, not a
  persistent artifact. Conventions file tracks status.
- **Auto-detect entry path** — Check CI first, then comments.
  Avoids requiring the user to specify what went wrong.
- **Force-with-lease not force** — Safer push that prevents
  overwriting upstream changes.
