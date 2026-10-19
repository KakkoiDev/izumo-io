# Vendored test-core tools

Copied unchanged from [KakkoiDev/test-core](https://github.com/KakkoiDev/test-core) at commit
`9906fb6b1c5a2bce138d6293b70afb60fe91fb1f` (branch `feat/recipes`). MIT licence: [LICENSE](LICENSE).
Standard library only; nothing is downloaded at test time.

- `scenarios.py`: every `### Scenario: <title>` in SCENARIOS.md has one e2e test named after its title, and with
  `--junit` that test ran and passed.
- `e2e_coverage.py`: every control in `website/pages/` and `website/templates/` is used by an e2e step, and no test
  uses a control that no longer exists.
- `flaky_lint.py`: no fixed sleeps, timers used as waits, focused tests, `networkidle` or real hosts in tests.

Update by copying the three files again from a newer test-core commit and changing the commit above.
