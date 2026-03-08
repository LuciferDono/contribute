# Phase 5: Submit

**Purpose:** Push the contribution to the user's fork and open a pull
request against the upstream repository.

**Entry point:** `/contribute submit`

**Prerequisite:** Read `.claude/contribute-test-report.md`. If the file
does not exist, the score is below 85%, or any BLOCKER is present, refuse:

> "Cannot submit — test phase has not passed. Run `/contribute test`
> first and address all failures."

---

## Step 1: Pre-flight Checks

**1. Determine the upstream default branch:**

Read from `.claude/contribute-conventions.md`. If not recorded, detect:
```bash
gh repo view <OWNER/REPO> --json defaultBranchRef \
  --jq '.defaultBranchRef.name'
```

**2. Rebase on latest upstream:**

Ask permission: "I need to rebase your branch on the latest
`upstream/<DEFAULT_BRANCH>`. This will rewrite your local commits.
Proceed?"
```bash
git fetch upstream
git rebase upstream/<DEFAULT_BRANCH>
```

If conflicts arise, present each conflict with full context. Ask
permission before editing any conflicted file. After resolving all
conflicts, run `git rebase --continue`. Once complete, re-run the project's
full test suite to verify nothing broke. If tests fail, direct the user
back to `/contribute work`.

**3. Verify branch is clean:**

No uncommitted changes, no untracked files that should be committed:
```bash
git status
```

**4. Re-confirm test report:**

Re-read `.claude/contribute-test-report.md`. Verify the report is not
stale — compare the report's timestamp against the most recent commit:
```bash
git log -1 --format="%ct"
```
If the most recent commit is newer than the test report, warn:
> "The test report was generated before your latest commit. Strongly
> recommend re-running `/contribute test` before submitting."

If the rebase introduced conflicts that required resolution, strongly
suggest re-running `/contribute test` before proceeding.

---

## Step 2: Push to Fork

Check if the branch already exists on the remote:
```bash
git ls-remote --heads origin <BRANCH_NAME>
```

If the branch does not exist on remote, ask permission:
> "Ready to push branch `branch-name` to your fork USERNAME/repo.
> This will be publicly visible. Proceed?"
```bash
git push origin <BRANCH_NAME>
```

If the branch already exists on remote (re-submission after fixes), ask
permission:
> "Branch `branch-name` already exists on your fork. I need to
> force-push to update it. Proceed?"
```bash
git push origin <BRANCH_NAME> --force-with-lease
```

Never use `--force`. `--force-with-lease` refuses if the remote has
commits not present locally.

---

## Step 3: Draft the Pull Request

Read `.claude/contribute-conventions.md` for upstream PR conventions,
required labels, and whether draft PRs are expected.

**Title:** Follow the project's format. Mirror conventional commit style
if the project uses it. Keep under 70 characters.

**Body:** Use the repo's PR template if one exists. If not, write a
body that reads like a real contributor wrote it:

- **Summary:** 2-3 sentences on what this PR does and why
- **Fixes:** `Fixes #NUMBER`
- **Changes:** One bullet per logical change
- **Testing:** Brief note on how you tested. Pull key facts from
  `.claude/contribute-test-report.md` but do not dump the full report.
- **Notes for Reviewers:** Anything needing special attention, open
  questions, or decisions that could have gone another way

### PR Body Humanization

**Check contributor history first:**
```bash
gh pr list --repo <OWNER/REPO> --author @me --state all --limit 5
```
If `gh auth status` is not authenticated or the command returns an error,
skip this check and use the standard (established contributor) body
format. Do not apply first-PR rules unless the history confirms it.

If this is the user's **first PR to this repo**, tone down the body:
- Shorter is better. 5-10 lines max, not 30.
- Don't use markdown headers (##) unless the PR template requires them.
- Don't add checkboxes unless the template has them.
- Don't include a test matrix or coverage report.
- Write like you're explaining to a coworker, not writing documentation.

**Good first-time PR body:**
```
Fixes #1234

The benchmark was failing because the helm chart sets labels
differently from what main.go expects. Updated values-benchmark.yaml
to include the right labels.

Tested locally — full benchmark suite passes now.
```

**Bad first-time PR body (too polished):**
```
## Summary
This PR resolves the label mismatch between the Helm chart deployment
and the benchmark runner expectations.

## Changes
- Updated `values-benchmark.yaml` to include correct label selectors
- Modified `configure-vpa.sh` to use Helm values instead of kubectl
- Updated `full-benchmark.sh` prerequisites

## Testing
- All 47 benchmark tests passing
- Zero regressions from baseline
- Full test suite: 142/142 passed
```

**For established contributors** (5+ merged PRs in the repo), a more
detailed body is acceptable and expected.

**Words to avoid in PR descriptions:** "enhance", "enhancement",
"streamline", "leverage", "utilize", "comprehensive", "robust",
"seamless", "implement" (as a fancy synonym for "add").
Use plain language: "fix", "add", "change", "update", "remove".

**Labels:** If the contribution guide specifies required labels for this
PR type, include them via `--label`. Do not guess labels not mentioned
in the guide.

**Draft flag:** If `.claude/contribute-conventions.md` indicates the
project expects draft PRs, add `--draft` to the create command.

---

## Step 4: Present Draft to User

Show the complete PR: title, body, source branch, target branch, labels,
and draft status. Ask:

> "Here is the PR draft. Should I open it, or do you want to
> modify anything?"

---

## Step 5: Open the PR

Only after explicit user approval. Write the PR body to a temp file to
avoid shell escaping issues with multiline content:
```bash
# Write PR body to .claude/contribute-pr-body.md first, then:
gh pr create \
  --repo <OWNER/REPO> \
  --title "<TITLE>" \
  --body-file .claude/contribute-pr-body.md \
  --head <USERNAME>:<BRANCH> \
  --base <DEFAULT_BRANCH> \
  [--label <LABEL>] \
  [--draft]
```

---

## Step 6: Post-submission

**1.** Display the PR URL immediately.

**2.** Run one immediate CI status check:
```bash
gh pr checks <PR_NUMBER> --repo <OWNER/REPO>
```
Report the initial status. If CI is still running, do not poll — tell
the user:
> "CI is running. Run `/contribute review` to check status and respond
> to any feedback once results are in."

**3.** If CI has already failed at time of check, analyze the failure
output and suggest fixes. Offer to transition back to `/contribute work`.

**4.** If CI passes immediately, inform the user the PR is ready for
maintainer review.
