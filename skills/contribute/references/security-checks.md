# Security Checks Reference

This file is loaded by Stage 3 of the test phase. It contains the
complete security checklist organized by language.

NOTE: This file documents ANTI-PATTERNS to flag during code review.
None of these patterns should be used — they are what to look for and
reject.

---

## Dependency Audit Commands

| Language | Command |
|---|---|
| Python | `pip audit` / `safety check` |
| JavaScript/TypeScript | `npm audit` / `yarn audit` / `pnpm audit` |
| Rust | `cargo audit` |
| Go | `govulncheck ./...` |
| Java (Maven) | `mvn org.owasp:dependency-check-maven:check` |
| Java (Gradle) | `./gradlew dependencyCheckAnalyze` |
| Ruby | `bundler-audit check` |
| PHP | `composer audit` |
| C#/.NET | `dotnet list package --vulnerable` |
| Elixir | `mix deps.audit` / `mix hex.audit` |
| Swift | Check advisories manually (no built-in audit) |
| Dart | `dart pub outdated` (check for known CVEs manually) |
| Scala | `sbt dependencyCheck` if OWASP plugin configured |

---

## Universal Checks (All Languages)

- Hardcoded secrets: API keys, tokens, passwords, private keys,
  connection strings, cloud credentials (AWS, GCP, Azure)
- Injection: SQL (string concatenation in queries), command (unsanitized
  input to shell), path traversal, XSS, SSRF, template injection, LDAP
  injection, XML external entities
- Input validation: all external input must be validated and sanitized
- Auth/authz: changes to auth logic flagged for extra scrutiny

---

## Per-Language Anti-Patterns to Flag

### Python
- Unsafe deserialization from untrusted sources
- Dynamic code execution with untrusted data
- Shell invocation with unsanitized user input
- YAML loading without safe loader

### JavaScript / TypeScript
- Dynamic code execution with user data
- Unsanitized input passed to shell commands
- Prototype pollution
- ReDoS on user-provided input
- Unsafe raw HTML injection in React

### Rust
- Unjustified unsafe blocks
- FFI boundary issues
- Unchecked unwrap on user-controlled paths

### Go
- Unsanitized input to command execution
- Template engine misuse (text vs html)
- Unchecked error returns
- Race conditions (test with -race)

### C / C++
- Buffer overflows via unsafe string functions
- Memory safety: use-after-free, double-free, leaks
- Integer overflow on user-controlled arithmetic
- Format string vulnerabilities
- Run with sanitizers if project supports it

### Java / Kotlin
- Unsafe deserialization
- SQL injection via string concatenation
- XXE in XML parsers
- Insecure random for security contexts

### Ruby
- Mass assignment without strong parameters
- Dynamic dispatch with user input
- Template injection
- URL-based file open with user input

### PHP
- Dangerous shell functions with user input
- File inclusion with user-controlled paths
- Unsafe deserialization
- SQL via string interpolation

### Solidity
- Reentrancy
- Integer overflow (pre-0.8.0)
- Unchecked external calls
- Missing access control
- tx.origin misuse

### Shell
- Unquoted variables
- Variable expansion injection
- Insecure temp file creation

### Swift
- Force unwrapping on external data
- Insecure network configuration
- Hardcoded credentials

### C# / .NET
- Unsafe deserialization
- SQL via string concatenation
- XXE in XML parsers
- Path traversal via user input

### Elixir
- Atom exhaustion from user input
- Unsafe template rendering
- Raw query interpolation

### Haskell
- Unsafe IO in pure contexts (unsafePerformIO misuse)
- Unchecked external process execution
- Template Haskell with untrusted input

### Dart / Flutter
- Insecure HTTP connections
- WebView injection
- Hardcoded credentials
