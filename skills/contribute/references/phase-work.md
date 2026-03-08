# Phase 3: Work

**Purpose:** Implement the contribution — write code, write tests, validate
locally, and prepare a clean changeset for review.

**Entry point:** `/contribute work`

**Prerequisite:** The analyze phase must have been completed and
`.claude/contribute-conventions.md` must exist. If not, stop and tell the
user to run `/contribute analyze` first.

---

## Step 1: Load Context

Read `.claude/contribute-conventions.md` to restore conventions, branch
naming, test commands, lint commands, and the recommended approach from
the analyze phase.

## Step 2: Select Operating Mode

Check `.claude/contribute-conventions.md` for a previously set mode. If
found, proceed in that mode without asking. If not set, ask once:

"Which mode for this contribution?"
- **do** — I implement everything, you review and approve
- **guide** — I walk you through each step, you execute
- **adaptive** — I handle mechanical parts, guide you on logic

Persist the chosen mode to `.claude/contribute-conventions.md`.

## Step 3: Set Up Local Environment

Each of the following is a write operation. State what will happen and ask
permission before executing each one.

**1. Fork the repo** (skip if already forked):

> "I need to fork owner/repo to your GitHub account, creating
> USERNAME/repo. Proceed?"
```bash
gh repo fork <OWNER/REPO> --clone
```

**2. Configure upstream remote** (if not present):
```bash
git remote get-url upstream 2>/dev/null || \
  git remote add upstream https://github.com/<OWNER/REPO>.git
```

**3. Create branch** following the naming convention from
`.claude/contribute-conventions.md`:

> "I will fetch upstream and create branch `name` from the latest
> upstream/<DEFAULT_BRANCH>. Proceed?"
```bash
git fetch upstream && git checkout -b <BRANCH_NAME> upstream/<DEFAULT_BRANCH>
```
Read `<DEFAULT_BRANCH>` from `.claude/contribute-conventions.md`.

**4. Install dependencies and verify baseline:**

Run the project's install command, then the full test suite on the clean
branch before any changes. If tests fail on the clean branch, surface the
failures to the user:

> "The test suite has N failures on the unmodified branch. This may be
> pre-existing. Proceed anyway, or investigate first?"

Do not silently block. Let the user decide.

## Step 4: Implement the Change

Follow the recommended approach from `.claude/contribute-conventions.md`.
Execute in this order regardless of mode:

1. **Read** every file listed in the contribution brief's "Files to Modify"
   section before writing anything.
2. **Write a failing test first.** For bug fixes: reproduce the bug in a
   test. For features: define expected behavior in tests. Run the test to
   confirm it fails for the right reason.
3. **Implement the fix or feature** to make the failing test pass.
4. **Format** using the project's formatter.
5. **Verify** the test now passes.

Constraints throughout:
- Match upstream code style exactly.
- Write minimal, focused changes. Do not refactor adjacent code, fix
  unrelated issues, or add unrequested features.
- Meet the project's test coverage requirements. If none are specified,
  add tests for all new or changed behavior regardless.

## Step 5: Validate

Run all three in sequence. Fix any failure before proceeding — do not
present a broken changeset.

1. **Full test suite** — all tests must pass (excluding pre-existing
   failures documented in Step 3)
2. **Linter and formatter** — zero new warnings
3. **Functional verification** — programmatically reproduce the original
   issue scenario or invoke the new feature path. Confirm the behavior
   matches what the issue asked for.

## Step 6: Present Changeset

Run `git diff HEAD --stat` first, then `git diff HEAD` for the full diff.
For diffs exceeding 200 changed lines, show the stat summary and offer the
full diff per file on request.

For each changed file, explain:
- What changed and why
- Any decision points where another approach was considered
- Any edge cases handled or intentionally deferred, with reasoning
- Anything that might surprise a reviewer

## Step 7: Commit

If the user requests changes to the diff, return to Step 4, implement,
re-run Step 5, and re-present.

Only after explicit approval:

1. Stage only relevant files — never `git add -A` or `git add .`:
```bash
   git add <file1> <file2> ...
```
2. Commit using the upstream commit message format from
   `.claude/contribute-conventions.md`.
3. Verify sole authorship (Rule 2) — the commit must have exactly one
   author (the logged-in user) and no AI-attribution trailers:
```bash
   git log -1 --format="%an <%ae>%n%(trailers:key=Co-authored-by)"
```
   If any Co-Authored-By or AI trailer is present, do NOT amend
   automatically. Present the violation to the user:

   > "The commit contains an AI trailer: [trailer text]. I need to amend
   > the commit to remove it. Amending rewrites the commit hash.
   > [If already pushed: This branch was already pushed — a force-push
   > will be required after amending.] Proceed?"

   Only after approval:
```bash
   git commit --amend --reset-author
```
   If the branch was already pushed, follow with the force-push flow
   (`--force-with-lease`, with explicit permission).

### Commit Message Humanization

AI-generated commit messages are a top signal maintainers look for.
Follow these rules to write messages that read like a real developer:

**Style rules:**
- Lowercase first word unless it's a proper noun or conventional prefix
- Short subject line (50 chars max), no period at the end
- Match the project's existing commit style exactly — check `git log --oneline -20`
- If the project uses conventional commits (`feat:`, `fix:`, `chore:`),
  use them. If not, don't.

**What to avoid:**
- Overly descriptive subjects: `fix: resolve edge case in label selector matching for VPA benchmark recommender component` — too AI
- Perfect grammar in every message — real devs write `fix label mismatch in benchmark` not `Fix: Correct label selector mismatch in VPA benchmark`
- Bullet-point bodies — real devs rarely write multi-bullet commit bodies for small changes
- Words that signal AI: "enhance", "enhancement", "streamline", "leverage", "utilize", "comprehensive", "robust", "seamless", "implement" (as a fancy synonym for "add")

**Good examples:**
- `fix helm label mismatch in benchmark`
- `add retry logic for flaky API calls`
- `update deps, fix breaking change in v3`
- `wip: rough draft of config parser` (if project allows WIP commits)

**Bad examples (too AI):**
- `Fix: Update Helm chart label selectors to match benchmark expectations`
- `Enhancement: Implement comprehensive retry mechanism for API calls`
- `Refactor: Streamline configuration parsing for improved maintainability`

**Multi-commit contributions:** If your change spans multiple commits,
the first commit message matters most — it often becomes the PR title.
Keep it punchy and specific.

Ask permission before committing:
> "Ready to commit with message: `message here`. Proceed?"
