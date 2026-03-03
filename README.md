# contribute

A Claude Code plugin for full-lifecycle open-source contributions. Find issues, analyze repos, write code, validate with industrial-grade testing, submit PRs, and respond to review feedback.

## Installation

```bash
claude plugin add LuciferDono/contribute
```

## Usage

```
/contribute discover          # Find issues to contribute to
/contribute analyze URL       # Deep-dive into a repo and issue
/contribute work              # Write code and prepare changes
/contribute test              # Industrial-grade validation (85% gate)
/contribute submit            # Push and open PR
/contribute review            # Monitor PR, respond to feedback
/contribute pr-review URL     # Review someone else's PR
/contribute release           # Create GitHub releases
/contribute triage URL        # Triage upstream issues
/contribute sync              # Keep fork in sync with upstream
/contribute cleanup           # Clean up contribution state
/contribute                   # Auto-detect phase from context
```

## Requirements

- **Claude Code** (primary target)
- **GitHub CLI** (`gh`) -- authenticated and configured
- **Git** -- configured with user.name and user.email

## Plugin Components

| Component | File | Purpose |
|---|---|---|
| Skill | `skills/contribute/SKILL.md` | Core rules, phase routing, state file schema |
| Command | `commands/contribute.md` | `/contribute` entry point with auto-detection |
| Agent | `agents/deep-reviewer.md` | AI deep review for test phase Stage 5 |
| Agent | `agents/issue-scout.md` | Parallel issue discovery with Rule 6 verification |

## Phases

### Core Workflow

1. **Discover** -- Search GitHub for issues matching your skills and interests. The `issue-scout` agent runs parallel searches, applies Rule 6 (verify not taken), and scores quality signals.

2. **Analyze** -- Clone the repo, read contribution guidelines, trace relevant code paths, and produce a structured contribution brief with files to modify, environment setup, and recommended approach.

3. **Work** -- Implement the change in one of three modes:
   - `do` -- AI writes everything, you review and approve
   - `guide` -- AI walks you through each step, you execute
   - `adaptive` -- AI handles boilerplate, you handle logic

4. **Test** -- Five-stage validation:
   - Stage 1: Upstream test suite (zero regressions)
   - Stage 2: Static analysis and code quality
   - Stage 3: Security audit
   - Stage 4: Functional verification
   - Stage 5: AI deep review via `deep-reviewer` agent
   - Score must reach 85% with zero BLOCKERs to unlock submit.

5. **Submit** -- Rebase, push to fork, draft PR following upstream conventions, open after user approval.

6. **Review** -- Check CI status, handle maintainer feedback, iterate on changes, respond to comments.

### Standalone Phases

- **PR Review** -- Review someone else's open PR with structured feedback across correctness, style, tests, security, and performance.
- **Release** -- Create GitHub releases with proper tags, changelogs, and release notes.
- **Triage** -- Reproduce bugs, categorize issues, check for duplicates, draft response comments.
- **Sync** -- Keep fork in sync with upstream via rebase or merge, handle conflicts.
- **Cleanup** -- Remove state files, local/remote branches, close stale PRs. Supports `--dry-run` and `--full` flags.

## State Files

All contribution state is persisted in `.claude/` in the working directory. This enables context to survive across sessions and slash command invocations.

### `.claude/contribute-conventions.md`

Written by: **analyze**
Read by: **work, test, submit, review, pr-review, sync, cleanup**

Schema (structured YAML header followed by freeform markdown):

```yaml
repo: owner/repo
issue: 123
issue_title: "Issue title"
default_branch: main
upstream_remote: upstream
branch_name: feat/issue-123-description
mode: do | guide | adaptive
pr_number: 456                    # written by submit
status: analyzing | working | testing | submitted | reviewing | merged | abandoned
test_report_timestamp: 1709510400 # unix timestamp, written by test
```

Below the YAML header: full conventions summary including branch naming, commit format, test framework, linter configuration, PR template requirements, and the recommended implementation approach.

### `.claude/contribute-test-report.md`

Written by: **test**
Read by: **submit**

Contains the scored test report with per-check PASS/WARN/FAIL/SKIP status, blocker count, and overall score. Submit refuses to proceed if this file is missing, the score is below 85%, or any BLOCKER exists.

### `.claude/contribute-discover.md`

Written by: **discover**
Read by: **analyze** (optional)

Contains search criteria, the full issue shortlist with URLs, complexity ratings, and quality scores. Preserves context if the session ends before the user selects an issue.

### `.claude/contribute-release-notes.md`

Written by: **release**
Read by: **release** (for `gh release create --notes-file`)

Draft release notes written to disk to avoid shell escaping issues with multiline content.

### `.claude/contribute-pr-body.md`

Written by: **submit**
Read by: **submit** (for `gh pr create --body-file`)

PR body written to disk to avoid shell escaping issues with multiline content.

## Cross-Tool Compatibility

This plugin is built for **Claude Code** but the skill content is tool-agnostic markdown. Other AI coding tools (Cursor, Antigravity, etc.) can use the skill by reading `skills/contribute/SKILL.md` and the reference files in `skills/contribute/references/`.

**What works everywhere:**
- All phase instructions (pure markdown directives)
- Core rules (read/write permissions, upstream conventions, operating modes)
- State file schema (standard markdown files in `.claude/`)
- GitHub CLI commands (tool-agnostic)

**Claude Code specific:**
- `/contribute` slash command (requires Claude Code command system)
- `deep-reviewer` and `issue-scout` agents (require Claude Code Task tool)
- Auto-detection logic in `commands/contribute.md`

Tools without agent support can run the deep review and issue search inline instead of in separate agents.

## Core Rules

1. **Read is free, write requires permission** -- Never modify state without explicit user approval.
2. **No Co-Authored-By** -- Every commit appears as sole-authored by the logged-in user. Zero exceptions.
3. **Three operating modes** -- do, guide, or adaptive. Persisted for the duration of the contribution.
4. **Respect upstream conventions** -- Match the project's style exactly.
5. **Opus only for subagents** -- Both agents use Claude Opus.
6. **Verify issue is not taken** -- Check assignees, open PRs, comment claims, and linked PRs before recommending any issue.

## License

MIT
