# Phase 6: Review

**Purpose:** Monitor the PR after submission, respond to maintainer
feedback, and iterate until the PR is merged or closed.

**Entry point:** `/contribute review`

**Prerequisite:** A PR must exist for the current branch. If not, stop
and direct the user to run `/contribute submit` first.

---

## Step 1: Resolve PR Identity

Read `.claude/contribute-conventions.md` for the stored PR number and
repo. If not present, detect from the current branch:
```bash
gh pr list \
  --head <USERNAME>:<BRANCH> \
  --repo <OWNER/REPO> \
  --json number,url,state \
  --jq '.[0]'
```

If no PR is found, report the exact state (not found, closed, merged)
and suggest the appropriate next step. Do not proceed with placeholder
values.

---

## Step 2: Check PR Status
```bash
gh pr view <PR_NUMBER> --repo <OWNER/REPO> \
  --json state,reviews,comments,statusCheckRollup,mergeable

gh pr checks <PR_NUMBER> --repo <OWNER/REPO>
```

Present a structured summary:
- **CI:** passing / failing / running
- **Mergeability:** clean / conflicting / unknown
- **Review status:** approved / changes requested / pending
- **Open comments:** count and authors

If `mergeable: CONFLICTING`, flag immediately:
> "Your branch has conflicts with upstream. Rebase is required before
> this can be merged."
Offer to run the rebase flow from phase-submit Step 1.

---

## Step 3: Handle PR State

**If changes are requested:**
1. Read every review comment in full. Summarize what the maintainer wants,
   grouped by theme (not one bullet per comment).
2. Present the summary with a recommended response for each point.
3. If the user agrees, transition to `/contribute work` to implement.
4. After changes are made, run `/contribute test` — the 85% gate and
   zero-BLOCKER requirement still apply.
5. Push updates — branch already exists on remote, so use:
```bash
   git push origin <BRANCH_NAME> --force-with-lease
```
   Ask permission before pushing: "Ready to force-push updated branch
   to your fork. This will update the open PR. Proceed?"

**If approved and not yet merged:**
First check if the user has merge permissions on the upstream repo:
```bash
gh api repos/<OWNER>/<REPO> --jq '.permissions.push'
```
If `false` or null, inform the user:
> "You don't have merge permissions on this repo. The maintainer will
> merge your PR. Nothing more to do — check back later."

If the user has merge permissions, check the repo's merge strategy from
`.claude/contribute-conventions.md` (squash / merge commit / rebase).
Provide the exact command and ask permission before executing:
```bash
gh pr merge <PR_NUMBER> --repo <OWNER/REPO> \
  --squash   # or --merge or --rebase
```
This is a write operation on the upstream repo — always ask permission.

**If merged:**
Congratulate the user. Then offer cleanup:
> "Your contribution has been merged. Should I delete the local and
> remote branch?"
```bash
git branch -d <BRANCH_NAME>
git push origin --delete <BRANCH_NAME>
```
Write the outcome to `.claude/contribute-conventions.md`:
`status: merged, merged_at: <DATE>, pr: <URL>`

**If closed without merge:**
Surface the closing reason (from PR comments or close event). Ask the
user if they want to address the feedback and re-open, or abandon.

**If CI fails:**
```bash
gh run list --repo <OWNER/REPO> --branch <BRANCH> \
  --limit 1 --json databaseId,conclusion

gh run view <RUN_ID> --repo <OWNER/REPO> --log-failed
```
Classify the failure:
- **(a) Related to changes** — transition to `/contribute work` to fix
- **(b) Pre-existing or flaky** — draft a PR comment explaining the
  unrelated failure (see Step 4)

---

## Step 4: Respond to Comments

If responding to multiple comments, draft all responses together and
post as a single consolidated comment — not one command per comment.
This is standard contributor etiquette.

Draft every response before posting. Show the full draft to the user.
Ask permission before posting:
> "Ready to post this response to the PR. Proceed?"
```bash
gh pr comment <PR_NUMBER> --repo <OWNER/REPO> --body "<RESPONSE>"
```

Tone rules:
- Professional, concise, constructive
- Never argue — if you disagree, explain reasoning once and defer
- Acknowledge feedback explicitly before responding to it
- Thank reviewers for substantive feedback
