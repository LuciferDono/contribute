# Phase 8: Release

**Purpose:** Create GitHub releases with proper tags, changelogs, and
release notes.

**Entry point:** `/contribute release`

**Prerequisite:** Must be in a repository with push access (own project
or maintainer role). If in a fork without upstream push access, halt and
inform the user.

---

## Step 1: Determine Version

Fetch existing tags and recent releases:
```bash
git tag --sort=-v:refname | head -20
gh release list --repo <OWNER/REPO> --limit 5
```

If no tags exist, suggest `v0.1.0` as the initial release and skip to
Step 2 with no bump analysis needed.

If tags exist, analyze commits since the last tag and recommend a bump:
- **patch** (x.y.Z): bug fixes only, no new features
- **minor** (x.Y.0): new features, no breaking changes
- **major** (X.0.0): breaking changes present

Present the recommendation and let the user confirm or override.

---

## Step 2: Generate Changelog

Verify working tree is clean before proceeding:
```bash
git status --porcelain
```
If anything is uncommitted, halt:
> "Working tree has uncommitted changes. Commit or stash before
> creating a release."

Parse commits since the last tag:
```bash
git log <LAST_TAG>..HEAD --format="%h %s (%an)"
```
For initial releases with no prior tag:
```bash
git log --format="%h %s (%an)"
```

**If the project uses conventional commits**, group by type:
- **Breaking Changes** — `!` suffix or `BREAKING CHANGE` footer
- **Features** — `feat:`
- **Bug Fixes** — `fix:`
- **Documentation** — `docs:`
- **Refactoring** — `refactor:`
- **Other** — everything else

**If not conventional commits**, group by file area touched or present
as a flat chronological list — do not force conventional categories onto
non-conforming commit messages.

Include PR numbers where present in commit messages:
```bash
git log <LAST_TAG>..HEAD --format="%h %s (%an)" | grep -oE '#[0-9]+'
```
If PR numbers are not embedded in commit messages, omit rather than
making expensive API calls to look them up.

---

## Step 3: Draft Release Notes

Check the format of previous releases before drafting:
```bash
gh release view <LAST_TAG> --repo <OWNER/REPO> --json body --jq '.body'
```

Match that format. If no prior releases exist, use:
- Version number and date
- Highlights (2-3 sentences on the most important changes)
- Breaking changes with migration notes (if any)
- Full categorized changelog from Step 2

Write the draft to file:
```bash
# Write to .claude/contribute-release-notes.md
```
This file is used in Step 6 to avoid shell escaping issues with
multiline content.

Check if previous releases were published as drafts first:
```bash
gh release list --repo <OWNER/REPO> --limit 5 --json isDraft
```
If the project uses draft releases, prepare to use `--draft` flag in
Step 6.

---

## Step 4: Present Draft to User

Show the complete release notes. Ask:
> "Here are the release notes for vX.Y.Z. Should I proceed, or do
> you want to modify anything?"

---

## Step 5: Create Tag

Only after user approves. Confirm which remote is the release target —
read from `.claude/contribute-conventions.md` or ask if ambiguous
(common when `origin` is a fork and `upstream` is the canonical repo).
```bash
git tag -a v<VERSION> -m "Release v<VERSION>"
```

---

## Step 6: Push Tag and Create Release

Two separate permission gates — tag push and release creation are both
publicly visible.

Ask permission to push the tag:
> "Ready to push tag v<VERSION> to <REMOTE>. This will be publicly
> visible. Proceed?"
```bash
git push <REMOTE> v<VERSION>
```

Ask permission to create the release:
> "Ready to create the GitHub release for v<VERSION>. Proceed?"
```bash
gh release create v<VERSION> \
  --repo <OWNER/REPO> \
  --title "v<VERSION>" \
  --notes-file .claude/contribute-release-notes.md \
  [--draft]   # if project uses draft releases
```

If created as draft, inform the user:
> "Draft release created. Review it at the URL below, then publish
> when ready."

---

## Step 7: Verify

Confirm the release object exists:
```bash
gh release view v<VERSION> --repo <OWNER/REPO> \
  --json tagName,publishedAt,url,isDraft
```

Verify the tag points to the correct commit:
```bash
git rev-list -n 1 v<VERSION>
git rev-parse HEAD
```

If these do not match, warn the user:
> "Tag v<VERSION> does not point to the current HEAD. The release may
> have been created at the wrong commit."

Display the release URL. If draft, remind the user to publish it.
