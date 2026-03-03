# Phase 10: Sync

**Purpose:** Keep fork in sync with upstream, handle divergence and
conflicts.

**Entry point:** `/contribute sync`

**Prerequisite:** Must be inside a git repository. If not, halt and
inform the user.

---

## Step 1: Verify Fork and Configure Upstream

Confirm this is actually a fork:
```bash
gh repo view --json isFork --jq '.isFork'
```
If `false`, halt:
> "This repository is not a fork. Sync requires an upstream to sync
> from."

Check for upstream remote:
```bash
git remote -v
```

If no upstream remote exists, detect the parent repo and add it:
```bash
gh repo view --json parent \
  --jq '.parent.owner.login + "/" + .parent.name'

git remote add upstream https://github.com/<OWNER>/<REPO>.git
```

Fetch upstream:
```bash
git fetch upstream
```

Detect the upstream default branch (locale-independent):
```bash
gh repo view <OWNER>/<REPO> --json defaultBranchRef \
  --jq '.defaultBranchRef.name'
```
Store as `<DEFAULT_BRANCH>`. Write to `.claude/contribute-conventions.md`
if not already present.

---

## Step 2: Detect Divergence

Compare current branch with upstream default:
```bash
git rev-list --left-right --count HEAD...upstream/<DEFAULT_BRANCH>
```

Report:
> "Your branch is N commits ahead and M commits behind
> upstream/<DEFAULT_BRANCH>."

If already up to date (0 ahead, 0 behind), inform the user and stop.

---

## Step 3: Check Working Tree

Before any sync operation, verify the working tree is clean:
```bash
git status --porcelain
```

If uncommitted changes exist, offer to stash:
> "You have uncommitted changes. I can stash them before syncing and
> restore them after. Proceed with stash?"
```bash
git stash push -m "sync-stash-$(git rev-parse --short HEAD)"
```

Record stash name to restore after Step 6.

---

## Step 4: Select Sync Strategy

**If the current branch is the fork's default branch**, rebase and merge
are both wrong. Use fast-forward reset to track upstream exactly.

First check if the fork's default branch has local-only commits:
```bash
git rev-list --count upstream/<DEFAULT_BRANCH>..HEAD
```
If ahead by N commits, warn explicitly:
> "Your fork's default branch has N local commits not in upstream.
> Resetting will discard these commits from the branch (recoverable
> via `git reflog` for 30 days). Proceed?"

After user approves:
```bash
git reset --hard upstream/<DEFAULT_BRANCH>
git push origin <DEFAULT_BRANCH> --force-with-lease
```
Skip to Step 7 after this.

**If on a feature branch**, ask:
- **Rebase** — linear history, recommended for unshared branches
- **Merge** — preserves history, safer for branches others have pulled

Check whether the branch exists on remote:
```bash
git branch -r | grep "origin/<BRANCH_NAME>"
```
If it exists on remote, warn regardless of strategy chosen:
> "This branch has been pushed. Rebase will require a force-push —
> only safe if no one else has pulled it."

---

## Step 5: Execute Sync

Only after explicit user approval:

**Rebase:**
```bash
git rebase upstream/<DEFAULT_BRANCH>
```

**Merge:**
```bash
git merge upstream/<DEFAULT_BRANCH>
```

---

## Step 6: Handle Conflicts

If conflicts arise, list all conflicted files:
```bash
git diff --name-only --diff-filter=U
```

For each conflict, read the file and present both sides with context.
Help the user resolve interactively. After resolving each file:
```bash
git add <RESOLVED_FILE>
```

For rebase, after resolving each round:
```bash
git rebase --continue
```
Rebase may surface new conflicts at each replayed commit — repeat this
loop until `git rebase --continue` completes without new conflicts.

For merge, after resolving all files:
```bash
git commit
```

If stash was created in Step 3, restore it now:
```bash
git stash pop
```
If stash pop causes conflicts, handle them the same way.

---

## Step 7: Verify

Run the project's test suite. Read the test command from
`.claude/contribute-conventions.md`. If not present, attempt to detect
it from the project (check `Makefile`, `package.json`, `pyproject.toml`).
If detection fails, inform the user:
> "Could not determine test command automatically. Please run tests
> manually before pushing."

If tests fail, diagnose whether the failure is from upstream changes or
a conflict resolution mistake, and offer to fix.

---

## Step 8: Push

**After rebase** (force-push required):
> "Rebase rewrites history. I need to force-push to update the remote
> branch. This is safe if no one else has pulled this branch. Proceed?"
```bash
git push --force-with-lease origin <BRANCH>
```

**After merge** (normal push):
> "Ready to push to origin/<BRANCH>. Proceed?"
```bash
git push origin <BRANCH>
```

Never use `--force`. `--force-with-lease` refuses if the remote has
commits not present locally, protecting against overwriting others' work.
