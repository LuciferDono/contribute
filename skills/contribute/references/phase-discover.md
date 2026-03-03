# Phase 1: Discover

**Purpose:** Find open-source issues that match the user's skills, interests, and available time.

**Entry point:** `/contribute discover`

## Step 1: Understand What the User Wants

Ask exactly one question:

"What are you looking for today?"

Present these options:
- **A) I have a specific repo or issue in mind** — Transition directly to analyze phase with the URL they provide.
- **B) Find me something in AI/ML/Data Science (Python)** — Search for Python issues in machine learning, deep learning, data science, NLP, computer vision, and related domains.
- **C) Find me something in systems programming (C/C++)** — Search for C or C++ issues in compilers, runtimes, databases, operating systems, performance-critical libraries, and similar.
- **D) Find me something in frontend** — Search for JavaScript or TypeScript issues in web frameworks, UI libraries, design systems, and browser tooling.
- **E) Surprise me** — Search across all of the above, prioritizing highly-starred repos with active communities.

If the user picks A, take their URL and transition to analyze. For B through E, proceed to Step 2.

## Step 2: Search GitHub for Candidate Issues

Use the GitHub CLI and GitHub MCP plugin to search. Execute multiple searches in parallel to maximize coverage.

**Search strategy — run ALL of these in parallel:**

1. **Label-based search:**
   ```bash
   gh search issues --label="good first issue" --language=<LANG> --sort=updated --limit=20 --state=open
   gh search issues --label="help wanted" --language=<LANG> --sort=updated --limit=20 --state=open
   ```

2. **Activity-based filtering:** Discard any issue that:
   - Has not had activity in the last 90 days
   - Already has an open PR linked to it
   - Is in a repo with fewer than 50 stars
   - Fails Rule 6 (Verify Issue Is Not Taken) — check assignees, open PRs, and recent comment claims:
   ```bash
   gh issue view <NUMBER> --repo <OWNER/REPO> --json assignees,closedByPullRequests,comments
   gh search prs --repo <OWNER/REPO> --state=open "<ISSUE_NUMBER>"
   ```

3. **Quality signals to prioritize:**
   - Repo has a CONTRIBUTING.md
   - Repo has CI configured (GitHub Actions, CircleCI, etc.)
   - Issue has clear reproduction steps or acceptance criteria
   - Maintainer has responded to the issue (indicates they care about it)
   - Repo has had a release in the last 6 months:
   ```bash
   gh release list --repo <OWNER/REPO> --limit=1
   ```

## Step 3: Present and Persist the Shortlist

Present 3 to 5 candidate issues in this exact format. Also write the
shortlist to `.claude/contribute-discover.md` so context survives if the
session ends before the user selects:

```bash
mkdir -p .claude
# Write: search criteria, full shortlist with URLs/complexity/reasoning, timestamp
```

Present:

```
## Issue Shortlist

### 1. [repo-owner/repo-name] — Issue Title
   Stars: X | Language: Y | Last activity: Z days ago
   Link: issue URL
   Labels: label1, label2
   Complexity: Small/Medium/Large (with brief justification)
   Why this is a good pick: reasoning
```

For complexity estimation:
- **Small:** 1-2 files, less than 50 lines, straightforward fix
- **Medium:** 3-5 files, 50-200 lines, requires understanding a subsystem
- **Large:** 5+ files, 200+ lines, requires understanding architecture

## Step 4: User Selects

Ask the user to pick one (by number) or ask for a new search. When they pick, transition to analyze with the issue URL.
