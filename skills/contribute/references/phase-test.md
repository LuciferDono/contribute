# Phase 4: Test

**Purpose:** Industrial-grade validation that ensures the contribution meets
professional standards before submission. Acts as a hard gate — submit will
not proceed without a passing report from this phase.

**Entry point:** `/contribute test`

**Prerequisite:** The work phase must have been completed with at least one
commit. If not, stop and direct the user to run `/contribute work` first.

**HARD GATE:** Submit MUST check for `.claude/contribute-test-report.md`.
If the file does not exist, or the score is below 85%, or any BLOCKER is
present, submit MUST refuse and direct the user back to work.

---

## Stage 1: Upstream Test Suite

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

**Python:**
- Linting: `flake8` / `pylint` / `ruff` — whichever the project uses
- Type checking: `mypy` / `pyright` — with project config
- Formatting: `black --check` / `isort --check`
- Complexity: `radon cc -s -a` on changed files — flag any function above 10
- Dead code: `vulture` on changed files

**C/C++:**
- `clang-tidy` with project config
- `cppcheck` for static analysis
- `clang-format --dry-run` for formatting
- Rebuild with `-Wall -Wextra -Wpedantic` — zero new warnings required

**JavaScript/TypeScript:**
- `eslint` with project config
- `tsc --noEmit` for type checking
- `prettier --check` for formatting

**CodeRabbit AI Review:**
Check if CodeRabbit is configured in the repo (does not require admin):
```bash
gh api repos/<OWNER>/<REPO>/contents/.coderabbit.yaml \
  --jq '.name' 2>/dev/null && echo "active" || echo "not configured"
```
If active, launch the `coderabbit:code-review` skill. If not configured,
mark as SKIP — do not fail.

---

## Stage 3: Security

**All projects:**
- **Dependency audit:** `pip audit` / `npm audit` / `safety check` —
  flag only vulnerabilities your changes introduced or are affected by
- **Secret detection:** Scan all changed files for hardcoded API keys,
  tokens, passwords, private keys, connection strings. Any finding is a
  BLOCKER.
- **Input validation:** Verify all functions accepting external input
  validate and sanitize before use
- **Injection:** SQL injection (string concatenation in queries), command
  injection (`shell=True`), path traversal (unsanitized paths), XSS
  (unescaped content in HTML)

**Any security finding rated BLOCKER is an automatic overall FAIL
regardless of score. Do not proceed to submit.**

**Python specific:**
- Unsafe dynamic code execution with untrusted data, unsafe subprocess
  invocation with shell interpreters
- Unsafe YAML: `yaml.load()` without `SafeLoader`

**C/C++ specific:**
- Buffer overflows: array accesses, unsafe string functions (strcpy,
  sprintf, gets) — flag and recommend safe alternatives
- Memory safety: use-after-free, double-free, leaks, dangling pointers
- Integer overflow on user-controlled arithmetic
- Run with AddressSanitizer/MemorySanitizer if project supports it

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
  [PASS/FAIL]  Memory safety (C/C++ only)

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
- FAIL lists all failures and warnings, directs user to `/contribute work`

---

## Test Applicability Matrix

| Check                | Python | C/C++ | JS/TS |
|---|---|---|---|
| Upstream test suite  | Yes | Yes | Yes |
| Linting              | Yes | Yes | Yes |
| Type checking        | Yes | Yes | Yes |
| Formatting           | Yes | Yes | Yes |
| Complexity analysis  | Yes | Yes | No  |
| Dead code            | Yes | No  | Yes |
| CodeRabbit review    | Yes | Yes | Yes |
| Dependency audit     | Yes | If pkg mgr | Yes |
| Secret detection     | Yes | Yes | Yes |
| Input validation     | Yes | Yes | Yes |
| Injection scan       | Yes | Yes | Yes |
| Buffer overflow      | No  | Yes | No  |
| Memory safety        | No  | Yes | No  |
| Integer overflow     | No  | Yes | No  |
| Unsafe operations    | Yes | Yes | Yes |
| Clean build          | Yes | Yes | Yes |
| Edge cases           | Yes | Yes | Yes |
| Error handling       | Yes | Yes | Yes |
| Integration          | Yes | Yes | Yes |
| AI Deep Review       | Yes | Yes | Yes |
