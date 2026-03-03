# Privacy Policy

**Plugin:** /contribute
**Effective date:** 2026-03-03
**Last updated:** 2026-03-03

---

## 1. Introduction

This Privacy Policy describes how the `/contribute` Claude Code plugin ("the Plugin") handles information when you install, configure, and use it. The Plugin is developed and maintained by LuciferDono ("we", "us", "our").

We are committed to transparency about data practices. This policy explains what data the Plugin accesses, how it is used, where it is stored, and what rights you have.

---

## 2. Information We Do NOT Collect

The Plugin does **not** collect, transmit, store, or process any of the following:

- Personal identifying information (name, email, address, phone number)
- Usage analytics or telemetry
- Crash reports or error logs sent to external services
- Browsing history, cookies, or tracking identifiers
- Advertising identifiers or marketing data
- Financial or payment information
- Biometric data
- Location data
- Device fingerprints or hardware identifiers

**The Plugin has no backend server, no database, no analytics endpoint, and no external data collection mechanism of any kind.**

---

## 3. Information the Plugin Accesses Locally

To function, the Plugin reads and writes files on your local machine within your current working directory. All data remains entirely under your control.

### 3.1 Git Identity

The Plugin reads your locally configured Git identity to ensure commits are attributed correctly:

- `git config user.name`
- `git config user.email`
- `gh api user --jq '.login'` (your GitHub username from your authenticated CLI session)

This information is used **only** to verify commit authorship (Rule 2: sole authorship enforcement). It is never transmitted to any service beyond what Git and GitHub CLI already do as part of normal Git operations.

### 3.2 Local State Files

The Plugin persists contribution context in a `.claude/` directory within your working directory:

| File | Created By | Purpose | Contains |
|------|-----------|---------|----------|
| `contribute-conventions.md` | Analyze phase | Store repo conventions | Branch naming, commit format, test commands, lint commands, recommended approach |
| `contribute-test-report.md` | Test phase | Store validation results | Pass/fail status per check, overall score, timestamps |
| `contribute-discover.md` | Discover phase | Store search results | Issue URLs, quality scores, complexity estimates |
| `contribute-release-notes.md` | Release phase | Store draft notes | Version number, changelog, release highlights |
| `contribute-pr-body.md` | Submit phase | Store PR body | PR title, description, testing summary |

**Important characteristics of these files:**

- They exist **only** on your local filesystem
- They are listed in `.gitignore` and are never committed to any repository
- They are never transmitted to any external service
- They can be inspected at any time (they are plain Markdown)
- They can be deleted at any time via `/contribute cleanup` or manual deletion
- They do not survive beyond the working directory in which they were created

### 3.3 Repository Content

During the Analyze and Work phases, the Plugin reads source code files, configuration files, documentation, and issue/PR content from repositories you are contributing to. This reading occurs:

- Locally, from cloned repositories on your filesystem
- Via the GitHub CLI (`gh`), using your existing authenticated session

No repository content is stored beyond what Git itself stores in your local clone and the state files described in Section 3.2.

---

## 4. Third-Party Services

### 4.1 GitHub API

The Plugin interacts with GitHub's API exclusively through the GitHub CLI (`gh`), which you install and authenticate independently. Operations include:

- Searching for issues and pull requests
- Reading issue and PR content, comments, and metadata
- Creating forks, branches, and pull requests
- Posting comments and reviews
- Creating releases and tags

**All API calls use your existing GitHub CLI credentials.** The Plugin does not:

- Store, cache, or proxy your GitHub authentication token
- Create its own OAuth application or authentication flow
- Access any GitHub data that your authenticated `gh` session cannot already access
- Perform any GitHub operation without your explicit approval (Rule 1)

GitHub's own privacy practices govern how GitHub handles your data. Refer to [GitHub's Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) for details.

### 4.2 Claude AI (Anthropic)

The Plugin runs within Claude Code, which is operated by Anthropic. The Plugin's instructions (Markdown files) are processed by Claude's language model as part of your Claude Code session. Anthropic's data practices govern how conversation content is handled. Refer to [Anthropic's Privacy Policy](https://www.anthropic.com/privacy) for details.

The Plugin itself does not independently transmit any data to Anthropic beyond what Claude Code already processes as part of its normal operation.

### 4.3 No Other Services

The Plugin does not contact, integrate with, or transmit data to any other third-party service, API, analytics platform, advertising network, or data broker.

---

## 5. Data Retention

### 5.1 Local State Files

State files persist in `.claude/` until you remove them. They are not automatically deleted. You can remove them at any time by:

- Running `/contribute cleanup` (interactive removal)
- Running `/contribute cleanup --full` (remove all)
- Manually deleting the `.claude/` directory

### 5.2 Git History

Commits, branches, and pull requests created through the Plugin persist according to Git and GitHub's standard behavior. Deleting these follows standard Git and GitHub procedures (branch deletion, PR closure, etc.).

---

## 6. Data Security

- All local files are protected by your operating system's file permissions
- All GitHub API communication occurs over HTTPS via the GitHub CLI
- No credentials are stored, cached, or managed by the Plugin
- The Plugin does not disable, bypass, or weaken any security controls

---

## 7. Children's Privacy

The Plugin is a software development tool and is not directed at children under 13 (or the applicable age of digital consent in your jurisdiction). We do not knowingly collect information from children.

---

## 8. User Rights and Control

You have complete control over all data the Plugin accesses:

- **Access:** All state files are plain Markdown, readable with any text editor
- **Deletion:** Remove state files via `/contribute cleanup` or manual deletion at any time
- **Restriction:** You can deny any write operation when prompted (Rule 1)
- **Portability:** State files are standard Markdown, portable to any system
- **Revocation:** Uninstall the Plugin at any time via `claude plugin remove LuciferDono/contribute`

No account creation, registration, or opt-in is required to use the Plugin. No data persists after uninstallation beyond what you explicitly committed to Git repositories.

---

## 9. International Users

The Plugin processes all data locally on your machine. No data crosses international boundaries through the Plugin itself. GitHub API calls are subject to GitHub's infrastructure and data handling practices.

---

## 10. Changes to This Policy

If we update this Privacy Policy, we will:

- Update the "Last updated" date at the top of this document
- Include the updated policy in the next Plugin release
- Document the changes in the release notes

We encourage you to review this policy periodically.

---

## 11. Open Source Transparency

This Plugin is open source under the MIT License. You can inspect every file, every instruction, and every command the Plugin issues:

- **Repository:** [github.com/LuciferDono/contribute](https://github.com/LuciferDono/contribute)
- **Skill instructions:** `skills/contribute/SKILL.md` and `skills/contribute/references/`
- **Agent definitions:** `agents/deep-reviewer.md` and `agents/issue-scout.md`
- **Command routing:** `commands/contribute.md`

Nothing is obfuscated, compiled, or hidden. The entire Plugin is plain Markdown.

---

## 12. Contact

For privacy questions, concerns, or requests:

- **GitHub Issues:** [github.com/LuciferDono/contribute/issues](https://github.com/LuciferDono/contribute/issues)
- **Repository:** [github.com/LuciferDono/contribute](https://github.com/LuciferDono/contribute)
