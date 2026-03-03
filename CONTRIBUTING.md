# Contributing to /contribute

Thank you for your interest in contributing to this plugin. This project follows its own workflow — you can use `/contribute analyze` on this repo to get started.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub CLI](https://cli.github.com/) (`gh`) — authenticated
- Git — configured with `user.name` and `user.email`

## Development Setup

```bash
# Fork and clone
gh repo fork LuciferDono/contribute --clone
cd contribute

# Verify plugin structure
ls .claude-plugin/plugin.json
ls commands/
ls agents/
ls skills/contribute/SKILL.md
```

No build step is required. The plugin is pure Markdown.

## What to Contribute

- **Bug fixes:** Incorrect phase logic, broken gh commands, scoring errors
- **Phase improvements:** Better heuristics, missing edge cases, clearer instructions
- **New quality signals:** Additional checks for the test gate
- **Documentation:** Typos, unclear instructions, missing examples
- **Agent improvements:** Better prompts for issue-scout and deep-reviewer

## Commit Format

Use imperative mood, present tense:

```
fix: correct Rule 6 assignee check command
feat: add complexity scoring to discover phase
docs: update test gate example in README
```

Prefix with `fix:`, `feat:`, `docs:`, `refactor:`, or `chore:`.

## Pull Request Expectations

1. **One concern per PR.** Do not bundle unrelated changes.
2. **Match existing style.** All content is Markdown — match heading levels, list formatting, and code block conventions from surrounding files.
3. **Test your changes.** Install the plugin locally and verify the affected phase works:
   ```bash
   claude plugin add ./contribute
   ```
4. **No AI attribution.** Per Rule 2, commits must be sole-authored. Do not add Co-Authored-By trailers.

## File Organization

| Directory | Contents | Format |
|-----------|----------|--------|
| `.claude-plugin/` | Plugin manifest | JSON |
| `commands/` | Slash command definitions | Markdown with YAML frontmatter |
| `agents/` | Subagent definitions | Markdown with YAML frontmatter |
| `skills/contribute/` | Core skill + phase references | Markdown |
| `skills/contribute/references/` | 11 phase reference files | Markdown |

## Reporting Issues

Use the [issue templates](https://github.com/LuciferDono/contribute/issues/new/choose) to report bugs or request features.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
