# Privacy Policy

**Plugin:** /contribute
**Last updated:** 2026-03-03

## Data Collection

This plugin collects **no user data**. It does not transmit, store, or process any personal information, telemetry, analytics, or usage metrics.

## What the Plugin Does

- Reads and writes files **locally** in your working directory (`.claude/` state files)
- Interacts with **GitHub's public API** via the GitHub CLI (`gh`) using your existing authenticated session
- All GitHub operations (searching issues, reading repos, opening PRs) use **your own GitHub credentials** managed by the GitHub CLI — the plugin has no separate authentication

## Third-Party Services

- **GitHub API:** Accessed through your locally authenticated `gh` CLI. The plugin does not proxy, intercept, or store any API responses beyond local state files.
- **No other services** are contacted.

## Local State Files

The plugin persists contribution context in `.claude/` within your working directory:

| File | Purpose |
|------|---------|
| `contribute-conventions.md` | Repo conventions and contribution approach |
| `contribute-test-report.md` | Test results and scores |
| `contribute-discover.md` | Issue search results |
| `contribute-release-notes.md` | Draft release notes |
| `contribute-pr-body.md` | PR body content |

These files are **local only**, listed in `.gitignore`, and never transmitted anywhere. Run `/contribute cleanup` to remove them.

## Contact

For privacy questions, open an issue at [github.com/LuciferDono/contribute](https://github.com/LuciferDono/contribute/issues).
