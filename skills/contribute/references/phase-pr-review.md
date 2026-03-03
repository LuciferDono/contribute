# Phase 7: PR Review

**Purpose:** Review someone else's PR on an upstream repo — read code,
analyze quality, draft constructive feedback.

**Entry point:** `/contribute pr-review <URL>`

**Prerequisite:** A PR URL must be provided. If not, halt and ask for it.

---

## Step 1: Parse URL and Fetch PR Context

Extract owner, repo, and PR number from the URL:
```bash
gh pr view <URL> \
  --json number,title,body,files,additions,deletions,commits, \
reviews,comments,headRefName,baseRefName,statusCheckRollup, \
state,headRefOid,baseRepository
```

If `state` is `merged` or `closed`, inform the user:
> "This PR is already merged/closed. Analysis will proceed for
> reference, but comments cannot be posted."

Fetch diff and CI status in the same batch:
```bash
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>
gh pr checks <PR_NUMBER> --repo <OWNER/REPO>
```

Store `headRefOid` — it is required for line comments in Step 7.

---

## Step 2: Understand Context

Read the linked issue to understand intent:
```bash
# Extract issue number from PR body ("Fixes #N", "Closes #N", etc.)
gh issue view <ISSUE_NUMBER> --repo <OWNER/REPO> \
  --json title,body,comments,labels
```

Read all existing reviews and comments before drafting — do not
duplicate feedback already given.

---

## Step 3: Establish Style Conventions

Check in order, use the first that succeeds:

1. Read `.claude/contribute-conventions.md` if it exists (in-workflow use)
2. Read linter/formatter configs from the repo root
3. If neither exists, sample recent merged PRs to infer conventions:
```bash
   gh pr list --repo <OWNER/REPO> --state merged --limit 5 \
     --json number,headRefName
   gh pr diff <RECENT_PR_NUMBER> --repo <OWNER/REPO>
```

---

## Step 4: Code Review Analysis

Review the diff against five dimensions:

1. **Correctness:** Does the change do what the issue asks? Logic errors,
   off-by-one bugs, missed edge cases?
2. **Style:** Does it match the conventions established in Step 3?
3. **Tests:** Happy path, edge cases, and error paths covered? Any missing?
4. **Security:** Injection, unsafe deserialization, hardcoded secrets,
   unvalidated input?
5. **Performance:** Unnecessary allocations, quadratic loops, blocking
   calls in async paths?

---

## Step 5: Draft Review Comments

For each issue found:
- **File:** path/to/file
- **Line:** line number or range
- **Severity:** BLOCKER / WARNING / SUGGESTION
  - **BLOCKER** — must fix before merge
  - **WARNING** — should fix, but won't hard-block if author disagrees
  - **SUGGESTION** — take it or leave it, improvement only
- **Comment:** what the problem is and what to do about it

Overall verdict:
- **Approve** — no BLOCKERs, code is ready
- **Request changes** — one or more BLOCKERs present
- **Comment only** — WARNINGs or SUGGESTIONs only, no hard objection

---

## Step 6: Present to User

Show the aggregate first:
> "Review complete: N blockers, N warnings, N suggestions.
> Verdict: [Approve / Request changes / Comment only]"

Then show the full draft — every line comment and the overall summary.

Ask: "Here is the review I'd post. Should I submit it, or do you want
to modify anything?"

Do NOT post anything without explicit user approval (Rule 1).

---

## Step 7: Post Review

Only after explicit user approval. If the PR is merged or closed, halt
— do not attempt to post.

**Post line comments first** (additive, recoverable on failure):
```bash
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments \
  -f body="<COMMENT>" \
  -f path="<FILE>" \
  -F line=<LINE> \
  -f commit_id="<HEAD_REF_OID>"
```

If any line comment fails, report which ones failed and offer to retry
before proceeding. Do not post the overall verdict until all line
comments have succeeded or the user explicitly chooses to skip failures.

**Then post the overall verdict:**
```bash
# Approve
gh pr review <PR_NUMBER> --repo <OWNER/REPO> --approve \
  --body "<OVERALL_COMMENT>"

# Request changes
gh pr review <PR_NUMBER> --repo <OWNER/REPO> --request-changes \
  --body "<OVERALL_COMMENT>"

# Comment only
gh pr review <PR_NUMBER> --repo <OWNER/REPO> --comment \
  --body "<OVERALL_COMMENT>"
```
