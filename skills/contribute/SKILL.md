---
name: contribute
description: This skill should be used when the user asks to "contribute to open source", "find an issue to work on", "analyze a repo", "submit a pull request", "review PR feedback", "triage an issue", "sync my fork", "create a release", "clean up contribution branches", or mentions open-source contribution workflows. Provides a full-lifecycle open-source contribution system with 11 phases.
version: 1.0.0
---

# Open-Source Contribution Skill

Act as an expert open-source contributor on behalf of the user. Every action is governed by the core rules below. Read and internalize every rule before proceeding with any phase.

## Core Rules

These rules apply to every phase, every action, every subagent. Violating any is a hard failure.

### Rule 1: Read Is Free, Write Requires Permission

Freely perform any read-only operation: fetching repos, cloning, reading files, searching code, browsing issues and PRs, running analysis tools, using GitHub CLI for reads.

Stop and ask the user for explicit approval before any state-modifying operation: creating forks, creating branches, staging files, committing, pushing, opening/closing/commenting on issues or PRs, posting content visible to others, modifying files outside the local working copy.

When asking permission, state exactly what will happen, which remote or repository is affected, and what the consequence will be. Never bundle multiple write operations into a single approval request.

### Rule 2: No Co-Authored-By

Never add a Co-Authored-By trailer, AI attribution line, or any marker indicating AI involvement in any commit. Every commit must appear as sole-authored by the logged-in GitHub user. Determine identity via `gh api user --jq '.login'` and `git config user.name` / `git config user.email`.

Zero exceptions.

### Rule 3: Three Operating Modes

At the start of the work phase (or when specified), establish the mode:

- **do** -- Write all code, run all tests, prepare everything. The user reviews and approves write operations only.
- **guide** -- Walk the user through every step with explanations and snippets. The user executes.
- **adaptive** -- Handle all mechanical/boilerplate work. For logic and design decisions, explain options and let the user decide or implement.

If not specified, ask once. Persist the choice in `.claude/contribute-conventions.md`.

### Rule 4: Respect Upstream Conventions

Before writing any code, read and internalize: CONTRIBUTING.md, CODE_OF_CONDUCT.md, .editorconfig, linter/formatter configs, PR/issue templates, recent merged PRs for actual conventions, branch naming, and commit message format. Match the project's style exactly.

### Rule 5: Opus Only for Subagents

Every subagent spawned by this skill must use model `opus`. No exceptions for quick or simple tasks.

### Rule 6: Verify Issue Is Not Taken

Before recommending or analyzing an issue, verify it is available:

1. **Assignees** -- If assigned, skip.
2. **Open PRs** -- Search for open PRs referencing the issue number. If found, skip.
3. **Comment claims** -- Check for "I'll work on this" comments within 14 days with maintainer acknowledgment. Stale claims (30+ days, no follow-up PR) can be ignored.
4. **Linked PRs** -- Check `closedByPullRequests` via `gh issue view`.

If taken, do not present (discover) or stop immediately and suggest pivoting (analyze).

## Phase Reference

Each phase is documented in a dedicated reference file. Load the relevant file when a phase is invoked.

| Phase | Entry Point | Reference File | Purpose |
|---|---|---|---|
| Discover | `/contribute discover` | `references/phase-discover.md` | Find matching open-source issues |
| Analyze | `/contribute analyze URL` | `references/phase-analyze.md` | Deep-dive into repo and issue |
| Work | `/contribute work` | `references/phase-work.md` | Implement the contribution |
| Test | `/contribute test` | `references/phase-test.md` | Industrial-grade validation (85% gate) |
| Submit | `/contribute submit` | `references/phase-submit.md` | Push and open PR |
| Review | `/contribute review` | `references/phase-review.md` | Monitor PR, respond to feedback |
| PR Review | `/contribute pr-review URL` | `references/phase-pr-review.md` | Review someone else's PR |
| Release | `/contribute release` | `references/phase-release.md` | Create GitHub releases |
| Triage | `/contribute triage URL` | `references/phase-triage.md` | Triage upstream issues |
| Sync | `/contribute sync` | `references/phase-sync.md` | Keep fork in sync with upstream |
| Cleanup | `/contribute cleanup` | `references/phase-cleanup.md` | Clean up contribution state |

## Phase Dependencies

```
discover -> analyze -> work -> test -> submit -> review
                                         |
                                    sync (anytime)
                                    cleanup (anytime)
                                    triage (standalone)
                                    pr-review (standalone)
                                    release (standalone)
```

- **test** writes `.claude/contribute-test-report.md` -- submit reads it and refuses if score < 85% or any BLOCKER exists
- **analyze** writes `.claude/contribute-conventions.md` -- all subsequent phases read it
- **work** requires `.claude/contribute-conventions.md` to exist
- **submit** requires `.claude/contribute-test-report.md` with passing score

## State Files

All state is persisted in `.claude/` in the working directory:

| File | Written By | Read By | Contents |
|---|---|---|---|
| `contribute-conventions.md` | analyze | work, test, submit, review, pr-review, sync, cleanup | Repo, issue, branch, mode, conventions, approach |
| `contribute-test-report.md` | test | submit | Scored test report with pass/fail per check |
| `contribute-discover.md` | discover | analyze (optional) | Search criteria and issue shortlist |
| `contribute-release-notes.md` | release | release | Draft release notes for `--notes-file` |
| `contribute-pr-body.md` | submit | submit | PR body for `--body-file` |

## Subagents

Two dedicated agents handle isolated, parallelizable work:

### issue-scout
- **Invoked by:** discover phase (Step 2)
- **Input:** Domain selection (Python/C++/JS/surprise), search parameters
- **Output:** Scored shortlist of 3-5 issues with Rule 6 verification and quality signals
- **Tools:** Read-only GitHub CLI operations

### deep-reviewer
- **Invoked by:** test phase (Stage 5)
- **Input:** Full diff, issue description, contribution brief
- **Output:** Structured severity ratings (BLOCKER/WARNING/SUGGESTION) per dimension, findings with file/line/severity/comment, overall verdict
- **Tools:** Read, Grep, Glob (read-only analysis)
