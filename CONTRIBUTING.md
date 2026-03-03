# Contributing to /contribute

## Quick Start

1. Fork and clone:
   ```bash
   gh repo fork LuciferDono/contribute --clone
   cd contribute
   ```

2. Install the plugin locally to test changes:
   ```bash
   claude plugin add ./
   ```

3. Make your changes on a feature branch:
   ```bash
   git checkout -b feat/your-change
   ```

4. Test by running any `/contribute` phase and verifying the
   instructions are coherent, commands are correct, and permission
   gates fire properly.

5. Open a PR against `master`.

## What You Can Contribute

- **Phase improvements** — Better instructions, edge case handling,
  clearer wording in `skills/contribute/references/phase-*.md`
- **New language support** — The test phase matrix covers Python,
  C/C++, and JS/TS. Adding Go, Rust, Java, etc. means extending
  the matrix and adding language-specific checks to `phase-test.md`
- **Agent tuning** — Improving prompts in `agents/deep-reviewer.md`
  and `agents/issue-scout.md` for better output quality
- **Bug reports** — If a phase gives bad instructions, file an issue
  with the phase name and what went wrong

## File Structure

| Directory | What goes here |
|-----------|----------------|
| `skills/contribute/references/` | Phase instruction files (one per phase) |
| `skills/contribute/SKILL.md` | Core rules and routing — keep under 200 lines |
| `agents/` | Subagent definitions (frontmatter + prompt) |
| `commands/` | Entry point command definition |
| `.claude-plugin/` | Plugin manifest only |

## Conventions

- **Commit format:** Imperative mood, descriptive
  (`Add Rust support to test phase matrix`,
  `Fix branch detection in sync phase`)
- **Branch naming:** `feat/`, `fix/`, `docs/` prefixes
- **Markdown style:** 72-char line wraps, ATX headings (`#` not
  underlines), fenced code blocks with language tags
- **No executable code:** This is a pure-markdown plugin. All "code"
  is instructional — commands that the AI model interprets and runs.
  Do not add scripts, build systems, or compiled artifacts.
- **Test your changes:** Install the plugin locally, run the phase
  you modified, and verify the behavior end-to-end before opening
  a PR.

## Pull Requests

- One logical change per PR
- Reference an issue if one exists
- Keep SKILL.md changes separate from phase reference changes
- If adding a new phase, also update the routing table in SKILL.md
  and the command router in `commands/contribute.md`

## Reporting Issues

Use the [issue templates](https://github.com/LuciferDono/contribute/issues/new/choose).
Include:

- Which phase misbehaved
- What the AI did vs what it should have done
- The repo/issue you were working on (if applicable)

## License

By contributing, you agree that your contributions will be licensed
under the [MIT License](LICENSE).
