# Phase 11: Cleanup

**Purpose:** Cleanly abandon or complete a contribution workflow —
removing state files, local branches, remote branches, and optionally
closing open PRs.

**Entry point:** `/contribute cleanup`

**Prerequisite:** Must be inside a git repository. No other prerequisites
— cleanup should work even when previous phases left broken state.

---

## Invocation Modes

```
/contribute cleanup              — interactive cleanup with prompts
/contribute cleanup --dry-run    — show what would be removed, touch nothing
/contribute cleanup --full       — remove everything without asking per-item
                                   (still requires one upfront confirmation)
```

---

## Step 1: Audit Current State

Read everything before touching anything. Run all of the following:

```bash
# State files
ls -la .claude/contribute-*.md 2>/dev/null

# Current branch
git branch --show-current

# All contribution-related local branches
git branch | grep -E "^[[:space:]]*(feat|fix|bugfix|patch|chore|docs|refactor)/"

# Remote branches on origin matching local contribution branches
git branch -r | grep origin/ \
  | grep -E "(feat|fix|bugfix|patch|chore|docs|refactor)/"

# Open PRs from this fork
gh pr list --author "@me" --state open \
  --json number,title,headRefName,url 2>/dev/null

# Stashes from sync operations
git stash list | grep "sync-stash"
```

Present the full inventory to the user before proceeding:

```
============================================
  CONTRIBUTION CLEANUP AUDIT
============================================

State Files:
  [ ] .claude/contribute-conventions.md   (found / not found)
  [ ] .claude/contribute-test-report.md   (found / not found)
  [ ] .claude/contribute-discover.md      (found / not found)
  [ ] .claude/contribute-release-notes.md (found / not found)
  [ ] .claude/contribute-pr-body.md       (found / not found)

Local Branches:
  [ ] branch-name  (current / not current)

Remote Branches (origin):
  [ ] origin/branch-name

Open PRs:
  [ ] #N — PR title (branch-name) URL

Sync Stashes:
  [ ] stash@{N}: sync-stash-HASH

============================================
```

If `--dry-run` was specified, stop here and display the audit. Do not
proceed to any removal step.

---

## Step 2: Determine Cleanup Scope

If `--full` was specified, skip per-item questions and ask once:

> "I will remove all items listed above. This cannot be undone for
> remote branches and closed PRs. Proceed?"

Otherwise, ask about each category individually in Steps 3-7. The user
can include or exclude any category.

---

## Step 3: Handle Open PRs

For each open PR found:

**If the PR shows engagement** (has maintainer reviews, positive
comments, or approval), surface this:
> "PR #N has [N reviews / N comments / was approved]. Are you sure
> you want to close it?"

**Options — ask the user:**
- **Close** — close the PR with an explanatory comment
- **Draft** — convert to draft (preserves work, signals not ready)
- **Leave open** — skip this PR entirely

For close, draft a closing comment before posting:
> "Closing this PR — [reason: abandoning / switching approach /
> duplicate / resolved differently]. Thanks for any feedback received."

Show the draft. Ask permission before posting and closing — two
separate permission gates:
```bash
# Post closing comment (ask permission)
gh pr comment <NUMBER> --repo <OWNER/REPO> --body "<COMMENT>"

# Close the PR (ask permission, separately)
gh pr close <NUMBER> --repo <OWNER/REPO>
```

For draft conversion:
```bash
gh pr ready <NUMBER> --repo <OWNER/REPO> --undo
```

---

## Step 4: Remove Remote Branches

For each remote branch on `origin` associated with this contribution:

> "Remove remote branch `origin/branch-name`? This deletes it from
> your fork on GitHub. Proceed?"

```bash
git push origin --delete <BRANCH_NAME>
```

If the PR for this branch was still open and was not closed in Step 3,
warn:
> "This remote branch has an open PR (#N). Deleting the branch will
> not close the PR automatically. Close the PR first (Step 3) or
> accept that it will remain open with a deleted source branch."

If the push returns "remote ref does not exist" (branch already deleted
by GitHub auto-delete after merge), treat as success — not a failure.

---

## Step 5: Remove Local Branches

For each local contribution branch:

**If the branch is currently checked out**, switch to the default branch
first. Read the default branch from `.claude/contribute-conventions.md`
if it exists, otherwise detect:
```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \
  | sed 's@refs/remotes/origin/@@'
```

Ask permission:
> "I need to switch to `<DEFAULT_BRANCH>` before deleting the current
> branch. Proceed?"
```bash
git checkout <DEFAULT_BRANCH>
```

**If the branch has unmerged commits**, warn explicitly:
```bash
git log --oneline <DEFAULT_BRANCH>..<BRANCH_NAME> | wc -l
```
> "Branch `branch-name` has N commits not merged into any upstream
> branch. Deleting it will lose this work permanently (recoverable
> via `git reflog` for 30 days). Proceed?"

```bash
# Safe delete (fails if unmerged — good default)
git branch -d <BRANCH_NAME>
```

If safe delete fails due to unmerged commits AND user explicitly
confirmed after the warning above:
```bash
git branch -D <BRANCH_NAME>
```

Never use `-D` without surfacing the unmerged commit warning first.

---

## Step 6: Clear State Files

Ask about each state file individually (unless `--full` mode):

> "Remove `.claude/contribute-conventions.md`? This clears all
> persisted contribution context. Proceed?"

```bash
rm .claude/contribute-conventions.md
rm .claude/contribute-test-report.md
rm .claude/contribute-discover.md
rm .claude/contribute-release-notes.md
rm .claude/contribute-pr-body.md
```

Remove files one at a time. If the user wants to keep a specific file
(e.g., conventions for a new contribution to the same repo), skip it.

If `.claude/` directory is now empty after removal:
```bash
rmdir .claude 2>/dev/null || true
```

If `.claude/` still contains non-contribute files (e.g., user-created
files), leave the directory intact.

---

## Step 7: Clear Sync Stashes

Only target stashes named `sync-stash-*` created by phase-sync. Do not
touch user-created stashes.

For each matching stash entry:

Show the stash contents first:
```bash
git stash show stash@{N} --stat
```

> "Drop stash@{N} (sync-stash from commit HASH, N files)? Proceed?"

```bash
git stash drop stash@{N}
```

Drop from highest index to lowest to avoid index shifting issues.

---

## Step 8: Verification

After all removals, run a final audit to confirm clean state:

```bash
ls .claude/contribute-*.md 2>/dev/null \
  && echo "State files remain" || echo "State files: clean"

git branch | grep -E "(feat|fix|bugfix|patch|chore|docs|refactor)/" \
  && echo "Local branches remain" || echo "Local branches: clean"

git branch -r | grep origin/ \
  | grep -E "(feat|fix|bugfix|patch|chore|docs|refactor)/" \
  && echo "Remote branches remain" || echo "Remote branches: clean"

gh pr list --author "@me" --state open \
  --json number,title 2>/dev/null
```

Present the final state:

```
============================================
  CLEANUP COMPLETE
============================================

  State files:      removed / N remaining
  Local branches:   removed / N remaining
  Remote branches:  removed / N remaining
  PRs:              closed  / N left open (intentional)
  Stashes:          dropped / N remaining

  Ready for next contribution.
  Run /contribute discover to find a new issue.
============================================
```

---

## Edge Cases

**Merged PR, branch already deleted by GitHub:**
GitHub auto-deletes branches after merge if the repo has that setting.
`git push origin --delete` will return "remote ref not found" — treat
as success, not failure.

**No `.claude/` directory exists:**
The user may be running cleanup on a machine that never ran contribute,
or after a manual cleanup. Skip all state file steps gracefully — do
not error.

**Currently in detached HEAD state:**
Before any branch operations, check:
```bash
git symbolic-ref --short HEAD 2>/dev/null || echo "detached"
```
If detached, inform the user and skip branch deletion until they
checkout a named branch.

**Multiple contributions in the same repo:**
The state files are not namespaced by contribution. If the user has run
multiple contributions in the same repo (unusual but possible), warn:
> "The state files in `.claude/` may cover multiple contributions.
> Removing them will clear context for all of them."

**Upstream fork relationship broken:**
If `gh repo view --json isFork` returns false or errors, the repo may
have been de-forked or the user is in a non-fork clone. Skip all remote
operations that depend on fork status and inform the user.

**Branch naming does not match grep patterns:**
The branch grep pattern (`feat|fix|bugfix|patch|chore|docs|refactor`)
may miss branches with non-standard names. If `.claude/contribute-conventions.md`
exists and contains the branch name, also include that branch in the
audit regardless of naming pattern.
