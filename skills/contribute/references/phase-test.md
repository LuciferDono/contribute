# Phase 4: Test

**Purpose:** Rigorous validation that ensures the contribution meets
professional standards before submission. Acts as a hard gate — submit will
not proceed without a passing report from this phase.

**Entry point:** `/contribute test`

**Prerequisite:** The work phase must have been completed with at least one
commit. If not, stop and direct the user to run `/contribute work` first.

**HARD GATE:** Submit MUST check for `.claude/contribute-test-report.md`.
If the file does not exist, or the score is below 85%, or any BLOCKER is
present, submit MUST refuse and direct the user back to work.

---

## Stage 0: Local Execution (Mandatory)

**This stage cannot be skipped. No AI review substitutes for actually
running the software.**

The Kubernetes incident proved this: AI-reviewed code that was never
executed locally will get rejected by experienced maintainers. This stage
requires real execution with real output.

**Step 1: Build the project from scratch.**

Use the exact build command from `.claude/contribute-conventions.md`. If
the project has no documented build command, detect from build files:

| Build file | Command |
|---|---|
| Makefile | `make` |
| CMakeLists.txt | `cmake -B build && cmake --build build` |
| package.json | `npm ci && npm run build` (or `yarn install --frozen-lockfile && yarn build`) |
| Cargo.toml | `cargo build` |
| go.mod | `go build ./...` |
| build.gradle / build.gradle.kts | `./gradlew build` |
| pom.xml | `mvn compile` |
| setup.py / pyproject.toml | `pip install -e ".[dev]"` |
| Gemfile | `bundle install` |
| mix.exs | `mix deps.get && mix compile` |
| pubspec.yaml | `dart pub get` or `flutter pub get` |
| *.sln / *.csproj | `dotnet build` |
| Dockerfile | `docker build .` |
| helm/Chart.yaml | `helm template .` or `helm lint .` |

**The build must succeed.** If it fails, this is a BLOCKER. Fix before
proceeding. Do not rationalize build failures away.

**Step 2: Run the project's full test suite.**

Not a subset. Not "the tests related to your change." The full suite.
Capture the complete terminal output.

**Step 3: If the project has benchmarks, integration tests, or end-to-end
tests that your change affects, run those too.**

Examples:
- Kubernetes VPA: run the benchmark (`go run ./benchmark/...`)
- React libraries: run Storybook or Playwright e2e
- CLI tools: run the actual CLI with sample inputs
- APIs: start the server, hit the endpoints
- Helm charts: `helm install --dry-run` or `helm template` and verify output

**Step 4: Capture and persist output.**

Save the raw terminal output to `.claude/contribute-local-execution.log`.
Include: the exact commands run, full stdout/stderr, exit codes. This is
evidence that the code was actually executed.

**Pass criteria:**
- Build succeeds (exit code 0)
- All tests pass (or only pre-existing failures from baseline)
- No runtime errors, crashes, or panics in the output
- Benchmarks/e2e pass if applicable

**A Stage 0 failure is an automatic BLOCKER and automatic overall FAIL
regardless of score.** Do not proceed to Stage 1. Do not generate a
partial report. Fix the issue first, then re-run `/contribute test`.

---

## Stage 1: Upstream Test Suite

**Reuse from Stage 0:** If Stage 0 already ran the full test suite
successfully, you may reuse that output for Stage 1's pass/fail
classification instead of running the suite again. Only run the
baseline stash comparison if Stage 0 did not already capture it.
For large projects this avoids a redundant 30+ minute test run.

**Establish baseline first:** If no test baseline exists in
`.claude/contribute-conventions.md`, stash current changes, run the full
test suite to capture which tests pass on the unmodified branch, record
the results, then unstash. This baseline is required to distinguish
regressions from pre-existing failures.

**Run:**
- The project's complete test suite using the exact command from
  `.claude/contribute-conventions.md`
- Capture full output including pass/fail counts and test names

**Pass criteria:**
- Zero regressions — every test passing before your changes must still pass
- All new tests you added must pass
- Coverage must not decrease if the project tracks it

**Failure classification:**
- **(a) Regression** — test passed before, fails now — counts against score
- **(b) Pre-existing** — was already failing on the clean branch — does not count
- **(c) Flaky** — non-deterministic, fails intermittently — run 3 times to confirm

Only (a) counts against the score.

---

## Stage 2: Static Analysis and Code Quality

Run every applicable tool based on the project's language and existing
configuration. Determine applicability from `.claude/contribute-conventions.md`.

**Auto-detection:** If the conventions file does not specify tools, detect
from config files and lockfiles in the repo. Always prefer the project's
own config over defaults. If a tool is not installed, attempt to install
it in a project-local scope (venv, node_modules, etc.) — ask permission
first per Rule 1.

---

### Python
- **Linting:** `ruff check` / `flake8` / `pylint` — whichever the project uses
- **Type checking:** `mypy` / `pyright` / `pytype` — with project config
- **Formatting:** `ruff format --check` / `black --check` / `isort --check` / `autopep8 --diff`
- **Complexity:** `radon cc -s -a` on changed files — flag any function above 10
- **Dead code:** `vulture` on changed files
- **Import sorting:** `isort --check-only --diff`
- **Docstring:** `pydocstyle` if project enforces it
- **Package:** `twine check dist/*` if building distributions

### JavaScript / TypeScript
- **Linting:** `eslint` with project config (check for flat config vs legacy)
- **Type checking:** `tsc --noEmit` (TS projects)
- **Formatting:** `prettier --check` / `dprint check` / `biome check`
- **Bundling:** `webpack --mode production` / `vite build` / `rollup -c` — verify bundle builds
- **Package validation:** `npm pack --dry-run` / `publint` if it's a library

### Rust
- **Linting:** `cargo clippy -- -D warnings`
- **Formatting:** `cargo fmt -- --check`
- **Build:** `cargo build` and `cargo build --release`
- **Tests:** `cargo test` (includes doc tests and integration tests)
- **Docs:** `cargo doc --no-deps` — must build without warnings
- **Unsafe audit:** `cargo geiger` if available — flag new unsafe blocks
- **Dependency audit:** `cargo audit`
- **MSRV check:** `cargo msrv verify` if project declares minimum supported Rust version

### Go
- **Linting:** `golangci-lint run` (or individual: `go vet ./...`, `staticcheck ./...`)
- **Formatting:** `gofmt -d .` / `goimports -d .` — zero diff required
- **Build:** `go build ./...`
- **Tests:** `go test ./...` with `-race` flag for race detection
- **Vulnerability:** `govulncheck ./...`
- **Module tidy:** `go mod tidy` — verify no diff after running

### Java
- **Build + test:** `mvn verify` / `./gradlew build` / `ant build`
- **Linting:** `checkstyle` / `spotbugs` / `pmd` — whichever is configured
- **Formatting:** `google-java-format --dry-run` / `spotless` plugin
- **Static analysis:** `errorprone` if configured in build
- **Dependency:** `mvn dependency:analyze` / `./gradlew dependencyInsight`

### Kotlin
- **Build + test:** `./gradlew build` / `mvn verify`
- **Linting:** `ktlint` / `detekt`
- **Formatting:** `ktlint` (check-only by default; reports violations without modifying files)

### C / C++
- **Linting:** `clang-tidy` with project config
- **Static analysis:** `cppcheck` / `scan-build` (Clang static analyzer)
- **Formatting:** `clang-format --dry-run --Werror`
- **Build warnings:** Rebuild with `-Wall -Wextra -Wpedantic` — zero new warnings
- **Sanitizers:** If project supports: `-fsanitize=address,undefined` run tests with ASan/UBSan
- **Memory:** Valgrind if available and project supports it

### C# / .NET
- **Build:** `dotnet build --warnaserror`
- **Test:** `dotnet test`
- **Linting:** `dotnet format --verify-no-changes` / Roslyn analyzers
- **Static analysis:** `dotnet build /p:TreatWarningsAsErrors=true` with Roslyn analyzers / SonarQube if configured
- **Package:** `dotnet pack --no-build` if it's a NuGet library

### Swift
- **Build:** `swift build` / `xcodebuild build`
- **Test:** `swift test` / `xcodebuild test`
- **Linting:** `swiftlint`
- **Formatting:** `swiftformat --lint`

### Objective-C
- **Build:** `xcodebuild build`
- **Test:** `xcodebuild test`
- **Linting:** `oclint` / Xcode analyzer
- **Static analysis:** `scan-build xcodebuild`

### Ruby
- **Linting:** `rubocop`
- **Type checking:** `sorbet tc` / `steep check` if project uses types
- **Test:** `bundle exec rake test` / `bundle exec rspec`
- **Security:** `bundler-audit check` / `brakeman` (Rails)
- **Formatting:** `rubocop` (check-only by default; reports violations without modifying files)

### PHP
- **Linting:** `phpstan analyse` / `psalm` / `phpcs`
- **Formatting:** `php-cs-fixer fix --dry-run --diff`
- **Test:** `./vendor/bin/phpunit`
- **Security:** `composer audit`
- **Compatibility:** `phpcompatibility` if project specifies PHP version range

### Perl
- **Linting:** `perlcritic`
- **Test:** `prove -r t/` / `make test`
- **Formatting:** `perltidy -st file.pl | diff - file.pl` (perltidy has no check flag; compare output to detect drift)

### Scala
- **Build + test:** `sbt compile test` / `mill compile`
- **Linting:** `scalafix` / `wartremover`
- **Formatting:** `scalafmt --check`

### Clojure
- **Build + test:** `lein test` / `clojure -M:test`
- **Linting:** `clj-kondo --lint src`
- **Formatting:** `cljfmt check`

### Elixir
- **Build:** `mix compile --warnings-as-errors`
- **Test:** `mix test`
- **Linting:** `mix credo --strict`
- **Formatting:** `mix format --check-formatted`
- **Type checking:** `mix dialyzer` if configured
- **Security:** `mix deps.audit` / `mix sobelow` (Phoenix)

### Haskell
- **Build + test:** `cabal build && cabal test` / `stack build && stack test`
- **Linting:** `hlint`
- **Formatting:** `ormolu --check` / `fourmolu --check` / `stylish-haskell`

### OCaml
- **Build + test:** `dune build && dune test`
- **Formatting:** `ocamlformat --check`
- **Linting:** Review compiler warnings (OCaml compiler is strict by default)

### F#
- **Build + test:** `dotnet build && dotnet test`
- **Linting:** `fantomas --check`

### Dart / Flutter
- **Linting:** `dart analyze` / `flutter analyze`
- **Formatting:** `dart format --set-exit-if-changed .`
- **Test:** `dart test` / `flutter test`
- **Build:** `flutter build` (if applicable)
- **Pub:** `dart pub publish --dry-run` if it's a package

### R
- **Check:** `R CMD check .` (the canonical R package validation)
- **Linting:** `lintr::lint_package()`
- **Test:** `testthat::test_local()`
- **Documentation:** `roxygen2::roxygenise()` — verify no warnings

### Julia
- **Test:** `julia -e 'using Pkg; Pkg.test()'`
- **Linting:** `JuliaFormatter` format check
- **Build:** Verify package precompiles without errors

### Lua
- **Linting:** `luacheck`
- **Test:** `busted` / `luaunit`
- **Formatting:** `stylua --check`

### Zig
- **Build:** `zig build`
- **Test:** `zig build test`
- **Formatting:** `zig fmt --check .`

### Nim
- **Build + test:** `nimble build && nimble test`
- **Linting:** `nim check <file>` / compiler warnings

### V (Vlang)
- **Build + test:** `v . && v test .`
- **Formatting:** `v fmt --verify .`

### Shell / Bash
- **Linting:** `shellcheck` on all `.sh` files in the diff
- **Formatting:** `shfmt -d` if project uses shfmt
- **Test:** `bats` if project uses BATS test framework
- **Portability:** Check shebang lines, POSIX compliance if required

### PowerShell
- **Linting:** `Invoke-ScriptAnalyzer`
- **Test:** `Invoke-Pester`

### Terraform / HCL
- **Validate:** `terraform validate`
- **Formatting:** `terraform fmt -check`
- **Linting:** `tflint`
- **Security:** `tfsec` / `checkov` / `trivy config`
- **Plan:** `terraform plan` (if credentials available, otherwise skip)

### Docker
- **Linting:** `hadolint` on all Dockerfiles in the diff
- **Build:** `docker build .` — must succeed
- **Security:** `trivy image` / `grype` on built image
- **Best practices:** No `latest` tags in FROM, no `apt-get` without cleanup,
  multi-stage builds where appropriate

### Kubernetes / Helm
- **Helm lint:** `helm lint .`
- **Helm template:** `helm template . > /dev/null` — must render without errors
- **Kubeval/kubeconform:** Validate generated YAML against K8s schemas
- **Security:** `kube-score` / `kubesec` / `trivy config`
- **Dry run:** `helm install --dry-run --debug` if cluster access available

### Ansible
- **Linting:** `ansible-lint`
- **Syntax:** `ansible-playbook --syntax-check`

### Solidity (Blockchain)
- **Build:** `forge build` / `npx hardhat compile` / `truffle compile`
- **Test:** `forge test` / `npx hardhat test` / `truffle test`
- **Linting:** `solhint` / `ethlint`
- **Security:** `slither` / `mythril analyze` — any critical finding is BLOCKER
- **Gas:** `forge test --gas-report` — flag significant gas regressions

### Protobuf / gRPC
- **Linting:** `buf lint`
- **Breaking changes:** `buf breaking --against .git#branch=main`
- **Build:** `buf generate` — verify generated code compiles

### GraphQL
- **Validation:** `graphql-inspector validate`
- **Breaking changes:** `graphql-inspector diff`
- **Linting:** `graphql-schema-linter`

### WASM (WebAssembly)
- **Build:** Use the host language toolchain (Rust: `cargo build --target wasm32-unknown-unknown`, Go: `GOOS=js GOARCH=wasm go build`)
- **Test:** Host language tests + `wasm-pack test` for Rust/wasm-pack projects

### Android (Kotlin/Java)
- **Build:** `./gradlew assembleDebug`
- **Test:** `./gradlew testDebugUnitTest`
- **Lint:** `./gradlew lint` — Android lint
- **Instrumented:** `./gradlew connectedAndroidTest` if emulator available

### iOS (Swift/ObjC)
- **Build:** `xcodebuild build -scheme <SCHEME> -destination 'platform=iOS Simulator,...'`
- **Test:** `xcodebuild test -scheme <SCHEME> -destination 'platform=iOS Simulator,...'`
- **Lint:** `swiftlint`

### React Native
- **Build:** `npx react-native build-android --mode=debug` / iOS equivalent
- **Test:** `jest` / `detox test` for e2e
- **Lint:** `eslint` + project config
- **Type check:** `tsc --noEmit`

### Flutter (cross-platform)
- **Build:** `flutter build apk --debug` / `flutter build ios --debug --no-codesign`
- **Test:** `flutter test`
- **Analyze:** `flutter analyze`
- **Integration:** `flutter test integration_test/` if present

### Bazel
- **Build:** `bazel build //...`
- **Test:** `bazel test //...`
- **Query:** `bazel query 'deps(//your:target)'` to verify dependency graph

### CMake (standalone)
- **Configure:** `cmake -B build -DCMAKE_BUILD_TYPE=Release`
- **Build:** `cmake --build build`
- **Test:** `ctest --test-dir build`

### Meson
- **Configure:** `meson setup build`
- **Build:** `ninja -C build`
- **Test:** `meson test -C build`

### LaTeX / Documentation
- **Build:** `latexmk -pdf` / `pdflatex`
- **Linting:** `chktex` / `lacheck`
- **Spell check:** `aspell` / `hunspell` on changed .tex files

---

### Universal Checks (All Languages)

These apply regardless of language:

- **Trailing whitespace:** No trailing whitespace in changed lines
- **File endings:** Consistent line endings (LF vs CRLF) matching project
- **Large files:** No files > 1MB added without justification
- **Binary files:** No accidental binary files committed
- **Merge markers:** No `<<<<<<<`, `=======`, `>>>>>>>` in any file
- **TODO/FIXME:** Flag any new TODO/FIXME/HACK/XXX comments in the diff —
  not a blocker, but note for the user to decide if intentional
- **License headers:** If the project uses them, verify changed files have them

---

### Tool Detection Heuristic

If `.claude/contribute-conventions.md` does not specify which tools to run,
detect from these files. **Priority order** (highest to lowest):

| Priority | Config file | Tools to run |
|---|---|---|
| 1 (highest) | `.github/workflows/ci.yml` | Parse the CI config to extract the exact linting/test commands the project runs in CI — mirror them locally. **CI is the source of truth.** |
| 2 | `.pre-commit-config.yaml` | Run `pre-commit run --all-files` — captures everything the project enforces locally |
| 3 | `Makefile` with `lint`/`check`/`test` targets | Run `make lint`, `make check`, `make test` |
| 4 | `tox.ini` | `tox -e lint` or equivalent env |
| 5 | `nox.py` / `noxfile.py` | `nox -s lint` or equivalent |
| 6 | `justfile` | `just lint`, `just test`, `just check` |
| 7 (lowest) | `Taskfile.yml` | `task lint`, `task test` |

**Rule:** If a CI workflow exists, always run what CI runs first. Then
supplement with pre-commit or Makefile targets for any checks CI does
not cover. This prevents "passes locally, fails in CI."

---

### CodeRabbit AI Review

Check if CodeRabbit is configured in the repo (does not require admin):
```bash
gh api repos/<OWNER>/<REPO>/contents/.coderabbit.yaml \
  --jq '.name' 2>/dev/null && echo "active" || echo "not configured"
```
If active, launch the `coderabbit:code-review` skill. If not configured,
mark as SKIP — do not fail.

---

## Stage 3: Security

**Any security finding rated BLOCKER is an automatic overall FAIL
regardless of score. Do not proceed to submit.**

Refer to `security-checks.md` (in this references directory) for the
complete language-specific security checklist. The checklist covers:
secret detection, dependency auditing (per-language commands), input
validation, injection risks (SQL, command, path traversal, XSS, SSRF,
XXE), auth/authz review, and language-specific anti-patterns for all
languages listed in that file (Python, JS/TS, Rust, Go, C/C++, Java,
Kotlin, Ruby, PHP, Solidity, Shell, Swift, C#/.NET, Elixir, Haskell,
and Dart/Flutter).

### Key rules:
- **Secret detection:** Any hardcoded key, token, password, or credential
  in changed files is an automatic BLOCKER.
- **Dependency audit:** Run the appropriate language tool. Flag only
  vulnerabilities your changes introduced or are affected by.
- **Input validation:** All functions accepting external input must
  validate and sanitize before use.
- **Auth/authz changes:** Any modification to authentication or
  authorization logic must be flagged for extra scrutiny.

---

## Stage 4: Functional Verification

- **Clean build:** Run the project's clean command if one exists (`make
  clean`, `npm run clean`, `cargo clean`, etc.). If no clean target exists,
  do NOT delete directories manually — skip the clean step. Then rebuild
  from scratch. Must succeed.
- **Edge cases:** For each function changed or added, verify behavior with:
  null/None, empty strings, empty collections, boundary values (0, -1,
  MAX_INT, empty file, single element). Run as ad-hoc scripts — do not
  permanently add to the test suite unless they reveal a real bug.
  These are exploratory — ask permission before writing any new files.
- **Error handling:** Error paths must produce meaningful messages, not
  crash, and not leak resources (files, connections, locks).
- **Integration:** Imports resolve, APIs match, types are compatible across
  the codebase.

---

## Stage 5: AI Deep Review

**If Task tool is available:** Launch an Opus subagent with model `opus`.

**If Task tool is unavailable:** Perform the review inline in the current
context. Do not skip this stage.

The reviewer acts as a demanding senior open-source maintainer. Provide:
the full diff, the issue description, and the contribution brief from
`.claude/contribute-conventions.md`.

Review against:
1. **CORRECTNESS** — Does this solve the issue? Any missed edge cases?
2. **EFFICIENCY** — Appropriate algorithm? No unnecessary complexity?
3. **READABILITY** — Understandable in 6 months without context?
4. **MAINTAINABILITY** — Follows existing patterns?
5. **COMPLETENESS** — Tests adequate? Docs updated?
6. **PUSHBACK RISK** — What would a strict maintainer object to?

Each finding rated: **BLOCKER**, **WARNING**, or **SUGGESTION**.
Only BLOCKERs and WARNINGs count against the score.
Any BLOCKER is an automatic overall FAIL.

---

## Scoring and Report

After all stages complete, write to `.claude/contribute-test-report.md`
then display:

```
============================================
  CONTRIBUTION TEST REPORT
============================================

Stage 0 — Local Execution
  [PASS/FAIL]  Build succeeded
  [PASS/FAIL]  Test suite passed
  [PASS/FAIL]  Benchmarks/e2e (if applicable)

Stage 1 — Upstream Tests
  [PASS/FAIL]  N/total passed (N regressions)
  [PASS/FAIL]  N new tests
  [PASS/FAIL]  Coverage: X%

Stage 2 — Code Quality
  [PASS/FAIL/SKIP]  Linter
  [PASS/FAIL/SKIP]  Type checker
  [PASS/FAIL/SKIP]  Formatter
  [PASS/FAIL/SKIP]  Complexity
  [PASS/FAIL/SKIP]  Dead code
  [PASS/FAIL/SKIP]  CodeRabbit

Stage 3 — Security
  [PASS/FAIL]  Dependency audit
  [PASS/FAIL]  Secret detection     <- BLOCKER if failed
  [PASS/FAIL]  Input validation
  [PASS/FAIL]  Injection scan
  [PASS/FAIL/SKIP]  Memory safety (C/C++/Rust only)

Stage 4 — Functional
  [PASS/FAIL]  Clean build
  [PASS/FAIL]  Edge cases
  [PASS/FAIL]  Error handling
  [PASS/FAIL]  Integration

Stage 5 — AI Deep Review
  [PASS/WARN/FAIL]  Correctness
  [PASS/WARN/FAIL]  Efficiency
  [PASS/WARN/FAIL]  Readability
  [PASS/WARN/FAIL]  Maintainability
  [PASS/WARN/FAIL]  Completeness
  [PASS/WARN/FAIL]  Pushback risk

--------------------------------------------
  TOTALS
--------------------------------------------
  Passed:   N
  Warnings: N  (0.5 pts each)
  Failed:   N  (0 pts each)
  Skipped:  N  (not counted)
  Blockers: N  <- any blocker = automatic FAIL

  Score:  X% (earned/possible x 100)
  Status: PASS / FAIL
  (Threshold: 85% with zero BLOCKERs)
============================================
```

**Scoring rules:**
- PASS = 1 point earned / 1 possible
- WARN = 0.5 earned / 1 possible
- FAIL = 0 earned / 1 possible
- SKIP = not counted
- Score = (earned / possible) x 100
- **PASS requires: score >= 85% AND zero BLOCKERs**
- **Stage 0 failure = automatic BLOCKER = automatic overall FAIL.** Do not generate a partial report.
- FAIL lists all failures and warnings, directs user to `/contribute work`

---

## Test Applicability Matrix

**Core rule:** If a project has a tool configured, run it. If not, SKIP
that check — do not fail. The matrix below shows common applicability
but is not exhaustive. Always defer to what the project actually uses.

| Check | Py | C/C++ | JS/TS | Rust | Go | Java | Kotlin | C# | Swift | Ruby | PHP | Elixir | Haskell | Dart | Scala | Shell | Solidity | Terraform | Docker | K8s/Helm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Local execution | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Upstream tests | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Linting | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Type checking | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Opt | Opt | Opt | Yes | Yes | Yes | No | Yes | No | No | No |
| Formatting | Yes | Yes | Yes | Yes | Yes | Opt | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Opt | Yes | Yes | No | No |
| Dependency audit | Yes | Opt | Yes | Yes | Yes | Yes | Yes | Yes | Opt | Yes | Yes | Yes | Opt | Opt | Opt | No | No | No | No | No |
| Secret detection | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Memory safety | No | Yes | No | Yes | No | No | No | No | No | No | No | No | No | No | No | No | No | No | No | No |
| Security scan | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Opt | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Clean build | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | N/A | Yes | Yes | Yes | Yes |
| Edge cases | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | No | No |
| AI Deep Review | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

**Opt** = Only if the project has it configured. Do not install or enforce.
**N/A** = Not applicable for this language/ecosystem.
