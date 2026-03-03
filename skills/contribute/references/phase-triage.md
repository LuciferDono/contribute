# Phase 9: Triage

**Purpose:** Help triage issues on upstream repos — reproduce, categorize,
gather context, draft responses.

**Entry point:** `/contribute triage <URL>`

**Prerequisite:** An issue URL must be provided. If not, halt and ask.

---

## Step 1: Parse URL and Read Issue

Parse owner, repo, and issue number from the URL:
```bash
gh issue view <URL> --json number,repository,title,body,comments, \
  labels,assignees,state,createdAt,updatedAt,author
```

Read every comment and linked reference. Note the reporter's environment,
reproduction steps, and expected vs. actual behavior.

---

## Step 2: Categorize and Surface

Classify the issue as one of:
- **Bug** — something broken, has reproduction steps or error output
- **Feature request** — asks for new functionality
- **Question** — asks for help or clarification
- **Duplicate** — same as an existing issue (confirmed in Step 4)
- **Invalid** — user error, misconfiguration, or out of scope

State the classification explicitly before proceeding:
> "I'm classifying this as: **[Category]** — [one sentence reasoning]"

This classification drives Step 6. If the user disagrees, correct it
before continuing.

---

## Step 3: Reproduce (Bugs Only)

Skip this step for non-bug categories.

**Determine the latest version:**
```bash
gh release list --repo <OWNER/REPO> --limit 1 --json tagName
```
If no releases exist:
```bash
gh api repos/<OWNER/REPO>/commits/HEAD --jq '.sha[0:7]'
```
Compare against the reporter's stated version.

**Follow reproduction steps exactly.** If the environment required
cannot be set up (GUI app, hardware dependency, OS-specific), document
the requirements and mark as:
> "Unable to verify — reproduction requires [environment] not available
> in this context."

If reproduction succeeds:
- Confirm the bug reproduces on version X
- Attempt to trace the code path to the offending function or line
- Note any environment differences from the reporter's

If reproduction fails:
- Note the version and environment where it did not reproduce
- Check if it was fixed between the reporter's version and latest

---

## Step 4: Check for Duplicates

Extract 2-3 distinctive keywords from the issue title, plus the error
string or function name if present. Run two searches:
```bash
gh search issues --repo <OWNER/REPO> --state open "<TITLE_KEYWORDS>"
gh search issues --repo <OWNER/REPO> --state closed "<TITLE_KEYWORDS>"
gh search issues --repo <OWNER/REPO> --state closed "<ERROR_STRING>"
```

If a duplicate is found, record the issue number and whether the
original is resolved, still open, or partially addressed.

---

## Step 5: Suggest Labels

Fetch the repo's label taxonomy:
```bash
gh label list --repo <OWNER/REPO> --limit 50
```

Suggest 1-3 labels matching the issue's category and affected area.
If the user has triage permissions and approves, apply them — this is
a separate permission gate from the comment in Step 7:

> "I'd like to apply these labels: [labels]. Proceed?"
```bash
gh issue edit <NUMBER> --repo <OWNER/REPO> --add-label "<LABEL>"
```

If the user does not have triage permissions, include the label
suggestion in the draft comment instead.

---

## Step 6: Draft Response

Tailor to the category identified in Step 2:

**Bug:**
- Confirm or deny reproduction (with version and environment)
- Provide a workaround if one exists
- Identify fix location (file, function) if root cause was found
- Suggest severity: critical / major / minor

**Feature request:**
- Assess feasibility based on codebase architecture
- Check alignment with project roadmap (read milestones and
  recent discussions)
- Note similar existing features

**Question:**
- Answer directly, or point to relevant documentation
- If docs are lacking, note as a potential docs contribution

**Duplicate:**
> "This appears to be a duplicate of #X. [brief explanation]
> Closing in favor of the original."

**Invalid:**
- Explain politely why this is out of scope or not a bug
- Point to the appropriate resource (docs, support forum, other repo)
- Suggest closing

---

## Step 7: Present and Post

Show the complete triage summary: category, reproduction result,
duplicate finding (if any), suggested labels, and draft response.

Ask:
> "Here is my triage and draft response. Should I post it, or do
> you want to modify anything?"

Only after explicit user approval:
```bash
gh issue comment <NUMBER> --repo <OWNER/REPO> --body "<RESPONSE>"
```
