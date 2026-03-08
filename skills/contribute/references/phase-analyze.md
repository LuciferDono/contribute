# Phase 2: Analyze

**Purpose:** Build a complete mental model of the repository, the issue, and the optimal contribution strategy before touching any code.

**Entry point:** `/contribute analyze URL`

**Prerequisite:** An issue or repository URL must be provided. If invoked without a URL, halt and ask the user for one before proceeding.

## Step 1: Read Contribution Rules

Fetch and read all of the following in parallel:

- CONTRIBUTING.md or CONTRIBUTING.rst or equivalent
- CODE_OF_CONDUCT.md
- .github/PULL_REQUEST_TEMPLATE.md (or .github/PULL_REQUEST_TEMPLATE/ directory)
- .github/ISSUE_TEMPLATE/ directory
- .editorconfig
- Linter configs: .pylintrc, .flake8, setup.cfg, ruff.toml, .clang-format, .clang-tidy, .eslintrc, eslint.config.js, prettier config, .golangci-lint.yml, clippy.toml, .rubocop.yml, phpstan.neon, .swiftlint.yml, detekt.yml, .editorconfig (ktlint reads from this), .credo.exs, .hlint.yaml, analysis_options.yaml, shellcheck directives, .hadolint.yaml, .solhint.json, buf.yaml
- Formatter configs: pyproject.toml (tool.black/ruff section), rustfmt.toml, .prettierrc, biome.json, gofmt/goimports, .editorconfig, scalafmt.conf, .ormolu, ocamlformat, fantomas config
- Build system files: Makefile, CMakeLists.txt, meson.build, setup.py, setup.cfg, pyproject.toml, package.json, Cargo.toml, go.mod, build.gradle, build.gradle.kts, pom.xml, build.sbt, mix.exs, Gemfile, pubspec.yaml, *.sln, *.csproj, Package.swift, Dockerfile, docker-compose.yml, helm/Chart.yaml, Justfile, Taskfile.yml, BUILD (Bazel), WORKSPACE (Bazel), flake.nix, shell.nix, dune-project / dune (OCaml), *.nimble (Nim), v.mod (Vlang), Project.toml (Julia), *.rockspec (Lua)
- .github/workflows/ — CI expectations

**Branch naming convention:** If CONTRIBUTING.md does not document a branch naming convention, infer it from recent PRs:
```bash
gh pr list --repo <OWNER/REPO> --limit 10 --json headRefName --jq '.[].headRefName'
```

**Persist to disk:** Write the synthesized conventions summary to `.claude/contribute-conventions.md` in the working directory so it survives across slash command invocations:
```bash
mkdir -p .claude
# Write conventions summary to .claude/contribute-conventions.md
```
All subsequent phases read this file on startup. Overwrite it each time analyze runs.

## Step 2: Understand the Codebase

Perform a structured exploration:

1. **Project structure:** Read the top-level directory listing. Identify source directories, test directories, documentation, configuration files.
2. **Architecture:** Read key entry points. Understand the module or package organization.
3. **Build system:** Identify how to build the project, install dependencies, and run tests. Installing dependencies is a write operation (modifies site-packages or node_modules). Ask permission:
   > "I need to install project dependencies to verify the build. This
   > will run [exact command]. Proceed?"
   ```bash
   # Detect from build files and run the appropriate command:
   # Python:     pip install -e ".[dev]" && python -m pytest --co -q
   # Node:       npm ci && npm test -- --listTests
   # Rust:       cargo build && cargo test -- --list
   # Go:         go build ./... && go test ./... -list '.*'
   # Java:       mvn compile -q && mvn test -pl . -Dtest=none
   # Ruby:       bundle install && bundle exec rake -T test
   # Elixir:     mix deps.get && mix compile
   # C#:         dotnet restore && dotnet build
   # Swift:      swift build
   # Dart:       dart pub get && dart test --reporter=compact
   # Helm:       helm dependency build && helm lint .
   ```
   If commands fail, diagnose the error (missing deps, wrong Python version, missing system libraries, etc.), attempt to fix, and retry. If unresolvable after two attempts, document the blocker in the brief under Risks as a blocker-level risk.
4. **Test framework:** Identify the test runner, test directory structure, test naming conventions, and how to run a single test.
5. **Dependencies:** Read dependency files to understand what libraries are available.

## Step 3: Analyze the Specific Issue

**GATE CHECK (Rule 6):** Before any deep analysis, verify the issue is not taken:

```bash
gh issue view <NUMBER> --repo <OWNER/REPO> --json assignees,closedByPullRequests,comments
gh search prs --repo <OWNER/REPO> --state=open "<NUMBER>"
```

If taken, STOP immediately, inform the user, and suggest pivoting. Do not waste time on deep analysis of taken issues.

Then:

1. **Read the full issue thread:** The opening post, every comment, every linked reference. After reading, extract three things before moving on:
   - **Core ask:** One sentence stating what the issue needs.
   - **Maintainer signals:** Any preferences, constraints, or direction from maintainer comments.
   - **Prior attempts:** Any previously attempted solutions (linked PRs, patches in comments, "I tried X but...").

2. **Trace relevant code paths:** Starting from the issue description, identify the exact functions, classes, and files involved. Read them. Understand the data flow.

3. **Identify files to modify:** List every file that will need changes, and what kind of change (new code, modified logic, new tests, updated docs).

4. **Check for related work:** Search for open and closed PRs that reference the issue. Use the bare issue number to catch all link styles (fixes, closes, resolves, refs):
   ```bash
   gh search prs --repo <OWNER/REPO> "#<NUMBER>" --state=open
   gh search prs --repo <OWNER/REPO> "#<NUMBER>" --state=closed
   ```

## Step 4: Present the Contribution Brief

Present a structured brief:

```
## Contribution Brief

**Issue:** #number — Issue Title
**Repo:** owner/repo (stars, language)
**Issue Summary:** 2-3 sentences explaining what the issue asks for and why
**Core Ask:** one sentence from Step 3.1
**Maintainer Signals:** any preferences or constraints from comments
**Prior Attempts:** any previously attempted solutions

### Upstream Conventions
- Branch naming: convention (source: CONTRIBUTING.md / inferred from PRs)
- Commit format: convention
- Test framework: framework, test location pattern
- Linter: tools, enforced in CI or not
- PR template: Yes/No, requirements

### Files to Modify
1. path/to/file — what changes and why
2. tests/path/to/test — what tests to add
3. docs/path — if documentation needs updating

### Environment Setup
1. Fork and clone command
2. Virtual environment or dependency install command
3. Build command
4. Test command
5. Lint command

### Recommended Approach
Detailed description of the implementation strategy — what to change, in what order,
and why this approach is preferred over alternatives. Include edge cases to watch for.

### Risks and Open Questions
- Any ambiguity that might need maintainer clarification
- Any potential breaking changes or backwards-compatibility concerns
- Any dependency on other issues or PRs
- Any environment setup blockers from Step 2

**Any blocker-level risk must be resolved before transitioning to work phase.** Flag each
risk as BLOCKER (must resolve first) or FLAG (proceed with awareness). If a BLOCKER exists,
recommend a resolution path: ask maintainer for clarification, wait for a dependency, or
choose an alternative approach.
```

## Step 5: User Confirms

Ask: "Does this approach look right? Should I proceed to work, or do you want me to dig deeper into any part?"

If the user confirms and no BLOCKER risks remain unresolved, transition to work. If they want changes, revise the brief.
