# Contributing to UAE HR

Thank you for helping. This app touches other people's payroll and legal obligations, so the bar is a little
higher than usual.

## Law changes

- **Every legal rule needs its article.** Cite it as `DL 9(1)` (Federal Decree-Law No. 33 of 2021) or `CR 24(4)`
  (Cabinet Resolution No. 1 of 2022), and add or update the quote in `docs/law.md`.
- **Numbers live in `uae_hr/law.py`, never in logic.** Add a `LawParam` with its default, citation, a verbatim quote
  and the direction that is more generous to the worker, then run `python3.14 dev/gen_doctypes.py` to regenerate the
  settings doctype. Code reads it with `get_param()`.
- **An amendment is a settings default plus a CHANGELOG line** naming the amending decree or resolution.
- **The Arabic text prevails (DL 66).** If the English is ambiguous, say so in the pull request and quote the Arabic
  if you can. Open questions are listed at the end of `docs/law.md`.
- **Only federal law and its regulations.** DIFC and ADGM have their own laws and are out of scope. Company policies
  that go beyond the law belong in your own app, not here.

## Code

- One test per legal rule. Pure checks go in `uae_hr/checks.py` and are tested without the database in
  `tests/test_checks.py`; behaviour on documents goes in the integration tests.
- Fields on standard doctypes are prefixed `uae_` and carry `module="UAE HR"`, so uninstalling removes exactly them.
- Setup (`uae_hr/setup/`) must be idempotent: a second `bench migrate` changes nothing. `tests/test_setup.py` checks it.
- Every user-facing string goes through `_()` / `__()` and gets an Arabic line: run `python3.14 dev/build_translations.py`
  after adding strings to `dev/ar_source.py`. A test fails if a string has no Arabic.
- Test data is invented. Never commit real names, passport or ID numbers, IBANs or company data.
- Format with `pre-commit` (ruff, eslint, prettier):

```bash
pre-commit install
```

## Running the tests

```bash
bench --site <test site> set-config allow_tests true
bench --site <test site> run-tests --app uae_hr
```

On a blank site the tests complete the setup wizard with an invented UAE company first.

## Reporting a wrong rule

Open an issue with the article number, what the app does, what the law says, and your source (ideally the Arabic
text). Wrong rules are treated as bugs with the highest priority.
