# Phase 7: Debug

**Purpose:** Diagnose and fix failures after a PR has been submitted.
Handles CI failures and maintainer-reported bugs. Focused on parsing
logs, mapping errors to changed code, and applying targeted fixes.

**Entry point:** `/contribute debug`

**Prerequisite:** A PR must exist for the current branch. Read
`.claude/contribute-conventions.md` for repo, branch, issue, and mode.
If the conventions file is missing or no PR exists, stop and direct the
user to the appropriate earlier phase.

---

## Step 1: Identify the Failure Source

Two auto-detected paths (check CI first, then maintainer feedback):

**Path A: CI Failure**
```bash
gh run list --repo <OWNER/REPO> --branch <BRANCH> \
  --limit 1 --json databaseId,conclusion,name
```
If `conclusion` is `"failure"`, fetch the failed logs:
```bash
gh run view <RUN_ID> --repo <OWNER/REPO> --log-failed
```
Extract: which job/step failed, error message, test name, exit code.

**Path B: Maintainer Comment / Changes Requested**
```bash
gh pr view <PR_NUMBER> --repo <OWNER/REPO> \
  --json reviews,comments,reviewDecision
```
Extract from reviews where `state` is `CHANGES_REQUESTED`: what they
want changed, specific files/lines, whether bug/style/design.

If both CI failed AND changes are requested, handle CI first.

---

## Step 2: Map Failure to Changed Code

Get the diff against the default branch:
```bash
git diff <DEFAULT_BRANCH>...HEAD
```

- **For test failures:** trace the failing test to the function it
  exercises, then check if that function was modified in the diff.
- **For CI tool failures** (linter, type checker, formatter): the tool
  output contains file paths and line numbers directly.
- **For reviewer comments:** match referenced files/lines to the diff.

Present a structured diagnosis:
```
## Diagnosis

Source: CI failure / Reviewer comment
Failure: <what failed>
File: <path>:<line>
Cause: <brief explanation>
Suggested fix: <one-sentence description>
```

Wait for user acknowledgment before applying any fix.

---

## Step 3: Apply Fix

Read the operating mode from `.claude/contribute-conventions.md`:
- **do:** Apply fix directly, show diff, ask permission before writing
  (Rule 1).
- **guide:** Explain fix step by step with exact code snippets, user
  applies.
- **adaptive:** Apply mechanical fixes directly, consult user on logic
  changes.

Multiple failures: fix one at a time, present each diagnosis
individually.

---

## Step 4: Re-validate and Push

1. Direct the user to run `/contribute test` — the 85% gate and
   zero-BLOCKER requirement still apply. Never skip testing, even for
   trivial fixes.
2. Push with force-with-lease (ask permission per Rule 1):
```bash
git push origin <BRANCH> --force-with-lease
```
3. Update the status in `.claude/contribute-conventions.md` back to
   `submitted`.
4. Suggest: "Fix pushed. Run `/contribute review` to check CI results
   and maintainer response."
