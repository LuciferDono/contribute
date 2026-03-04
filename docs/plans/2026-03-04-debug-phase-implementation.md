# Debug Phase Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a `debug` phase to the /contribute plugin for post-commit debugging (CI failures + maintainer-reported bugs).

**Architecture:** Single new reference file `phase-debug.md` plus edits to SKILL.md, commands/contribute.md, and README.md. No new agents or state files. Debug sits between review and test in the fix cycle: `review -> debug -> test -> push`.

**Tech Stack:** Pure markdown (Claude Code plugin). GitHub CLI for CI log fetching.

---

### Task 1: Create phase-debug.md

**Files:**
- Create: `skills/contribute/references/phase-debug.md`

**Step 1: Write the phase reference file**

```markdown
# Phase 7: Debug

**Purpose:** Diagnose and fix failures after a PR has been submitted.
Handles CI failures and maintainer-reported bugs. Focused on parsing
logs, mapping errors to changed code, and applying targeted fixes.

**Entry point:** `/contribute debug`

**Prerequisite:** A PR must exist for the current branch. Read
`.claude/contribute-conventions.md` for repo, branch, issue, and
mode. If conventions file is missing or no PR exists, stop and
direct the user to the appropriate earlier phase.

---

## Step 1: Identify the Failure Source

Check CI status first. If CI is passing, check for maintainer
feedback. Auto-detect — do not ask the user which path to take.

### Path A: CI Failure

```bash
# Get the most recent workflow run for this branch
gh run list --repo <OWNER/REPO> --branch <BRANCH> \
  --limit 1 --json databaseId,conclusion,name

# If conclusion is "failure", fetch the failed logs
gh run view <RUN_ID> --repo <OWNER/REPO> --log-failed
```

Extract from the logs:
- Which job and step failed
- The error message or assertion failure
- The test name (if a test failure)
- The exit code

### Path B: Maintainer Comment / Changes Requested

```bash
gh pr view <PR_NUMBER> --repo <OWNER/REPO> \
  --json reviews,comments,reviewDecision
```

Extract from reviews where `state: "CHANGES_REQUESTED"`:
- What the maintainer wants changed
- Specific files or lines referenced
- Whether it is a bug report, style issue, or design concern

If both CI has failed AND changes are requested, handle CI first
(it is more mechanical and may resolve the review concern too).

---

## Step 2: Map Failure to Changed Code

Get the contribution diff:
```bash
git diff <DEFAULT_BRANCH>...HEAD
```

Correlate the failure to specific files and lines in the diff:
- For test failures: trace the failing test to the function it
  exercises, check if that function was modified in the diff
- For CI tool failures (linter, type checker, formatter): the
  tool output includes file paths and line numbers directly
- For reviewer comments: match referenced files/lines to the diff

Present a structured diagnosis before proceeding:

```
## Diagnosis

Source: CI failure / Reviewer comment
Failure: <what failed — test name, linter rule, reviewer quote>
File: <path>:<line>
Cause: <brief explanation of why this broke>
Suggested fix: <one-sentence description of the fix>
```

Wait for user acknowledgment before applying any fix.

---

## Step 3: Apply Fix

Read the operating mode from `.claude/contribute-conventions.md`
and act accordingly:

- **do** — Apply the fix directly. Show the diff of changes made.
  Ask permission before writing files (Rule 1).
- **guide** — Explain the fix step by step. Provide exact code
  snippets. The user applies the changes.
- **adaptive** — Apply mechanical fixes (formatting, imports,
  typos) directly. For logic changes, explain options and let
  the user decide.

If there are multiple failures, fix them one at a time. Present
each diagnosis and fix individually.

---

## Step 4: Re-validate and Push

After all fixes are applied:

1. **Re-run the test gate:**
   Direct the user to run `/contribute test`. The 85% score
   threshold and zero-BLOCKER requirement still apply. Do not
   skip this step even if the fix seems trivial.

2. **Push the fix:**
   The branch already exists on the remote. Use force-with-lease:
   ```bash
   git push origin <BRANCH_NAME> --force-with-lease
   ```
   This is a write operation — ask permission before executing
   (Rule 1): "Ready to force-push the fix to your fork. This
   will update the open PR. Proceed?"

3. **Update status:**
   Write `status: submitted` back to
   `.claude/contribute-conventions.md` (it may have been set to
   `debugging` during the fix cycle).

4. **Suggest next step:**
   "Fix pushed. The PR has been updated. Run `/contribute review`
   to check CI results and maintainer response."
```

**Step 2: Commit**

```bash
git add skills/contribute/references/phase-debug.md
git commit -m "feat: add phase-debug.md reference file"
```

---

### Task 2: Update SKILL.md — routing table and dependency diagram

**Files:**
- Modify: `skills/contribute/SKILL.md:3` (description — 11 phases -> 12)
- Modify: `skills/contribute/SKILL.md:62-74` (phase routing table)
- Modify: `skills/contribute/SKILL.md:78-86` (dependency diagram)
- Modify: `skills/contribute/SKILL.md:99` (state files — add debug to Read By)

**Step 1: Update frontmatter description**

Line 3, change:
```
Provides a full-lifecycle open-source contribution system with 11 phases.
```
to:
```
Provides a full-lifecycle open-source contribution system with 12 phases.
```

Also add `"debug CI failures"` to the trigger phrase list.

**Step 2: Add Debug row to phase routing table**

After the Review row (line 69), insert:

```markdown
| Debug | `/contribute debug` | `references/phase-debug.md` | Diagnose and fix CI failures or reviewer-reported bugs |
```

**Step 3: Update dependency diagram**

Replace the diagram (lines 78-86) with:

```
discover -> analyze -> work -> test -> submit -> review
                                                   |
                                              debug -> test -> submit (force-push)
                                              sync (anytime)
                                              cleanup (anytime)
                                              triage (standalone)
                                              pr-review (standalone)
                                              release (standalone)
```

**Step 4: Update state files table**

In the `contribute-conventions.md` row, add `debug` to the
"Read By" column (alongside work, test, submit, review, etc.).

**Step 5: Commit**

```bash
git add skills/contribute/SKILL.md
git commit -m "feat: add debug phase to SKILL.md routing and diagram"
```

---

### Task 3: Update commands/contribute.md — routing and auto-detection

**Files:**
- Modify: `commands/contribute.md:13` (phase keywords list)
- Modify: `commands/contribute.md:26-38` (routing table)
- Modify: `commands/contribute.md:40-76` (auto-detection)

**Step 1: Add `debug` to phase keywords list**

Line 13, add `debug` to the list:

```markdown
**Phase keywords:** `discover`, `analyze`, `work`, `test`, `submit`, `review`, `debug`, `pr-review`, `triage`, `sync`, `release`, `cleanup`
```

**Step 2: Add debug row to routing table**

After the `review` row (line 33), insert:

```markdown
| `debug` | `references/phase-debug.md` | Requires existing PR with CI failure or review feedback |
```

**Step 3: Add auto-detection for debug**

After item 3 (`status: submitted` -> suggest review), add:

```markdown
3b. **If `.claude/contribute-conventions.md` exists with `status: submitted` and CI has failed:**
    ```bash
    gh run list --repo <OWNER/REPO> --branch <BRANCH> \
      --limit 1 --json conclusion --jq '.[0].conclusion'
    ```
    If conclusion is `failure`:
    Suggest: "CI is failing on your PR. Want to run **debug** to diagnose and fix?"
```

**Step 4: Commit**

```bash
git add commands/contribute.md
git commit -m "feat: add debug keyword to command routing and auto-detection"
```

---

### Task 4: Update README.md — core workflow table and references

**Files:**
- Modify: `README.md:33` (phase count 11 -> 12)
- Modify: `README.md:78-86` (How It Works diagram)
- Modify: `README.md:104-111` (core workflow table)
- Modify: `README.md:180-191` (architecture tree — references count)

**Step 1: Update phase count**

Line 33, change `11-phase workflow` to `12-phase workflow`.

**Step 2: Update How It Works diagram**

Replace lines 78-86 with:

```
/contribute discover ──> analyze ──> work ──> test ──> submit ──> review
                                                                    │
                                                              debug ──> test ──> push
                                                              sync (anytime)
                                                              cleanup (anytime)
                                                              triage (standalone)
                                                              pr-review (standalone)
                                                              release (standalone)
```

**Step 3: Add Debug row to core workflow table**

After row 6 (Review), insert:

```markdown
| 7 | **Debug** | `/contribute debug` | Diagnose CI failures or reviewer-reported bugs. Parse logs, map to changed code, apply targeted fix, re-test. |
```

**Step 4: Update architecture tree**

Change `# 11 phase reference files` to `# 12 phase reference files`
and add `│           ├── phase-debug.md` in alphabetical position.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: add debug phase to README"
```

---

### Task 5: Update CI workflow — add phase-debug.md to validation

**Files:**
- Modify: `.github/workflows/validate.yml:32` (phases array)

**Step 1: Add `debug` to the phases array**

In the "Check all phase files exist" step, add `debug` to
the phases list:

```bash
phases=(
  discover analyze work test submit review debug
  pr-review release triage sync cleanup
)
```

**Step 2: Commit**

```bash
git add .github/workflows/validate.yml
git commit -m "ci: add debug to phase file validation"
```

---

### Task 6: Verify locally

**Step 1: Run the CI validation locally**

```bash
python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"
```

Verify phase-debug.md exists:
```bash
ls skills/contribute/references/phase-debug.md
```

Verify SKILL.md has 12 phases in the routing table:
```bash
grep -c "references/phase-" skills/contribute/SKILL.md
```
Expected: `12`

**Step 2: Push all commits**

```bash
git push origin master
```
