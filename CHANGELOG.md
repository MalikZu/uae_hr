# Changelog

Each entry names the article behind the change. Versions follow semantic versioning.

## 0.1.0 (unreleased)

First version: records, documents, reminders, pay components and checks for workers already employed.

- Employee fields prefixed `uae_`; work-permit types seeded from CR 6(1) (12 types).
- UAE Employee Document with verify, supersede and mirror to Employee; scans always private.
- Expiry reminders to role UAE PRO; Expiring Documents report.
- UAE HR Letter register; experience certificate content per DL 13(11); disciplinary time limits per CR 24(4).
- Salary components Basic / Housing / Transport / Other read from the Salary Structure Assignment (DL 1, DL 51(5)).
- Checks: probation at most 6 months and once per employer (DL 9(1)-(2)); notice 30 to 90 days (DL 43(1));
  contract readiness (CR 10(1)); worker file kept 2 years (DL 13(1)); official documents not withheld (DL 13(2));
  death nominee from the worker's family (DL 15(2), DL 1).
- UAE HR Settings: 60 law parameters with citations, defaulting to the law; less favourable values need an
  amendment reference (DL 65(1), DL 70(7)).
- Per-company jurisdiction: DIFC and ADGM not covered.
- Arabic translations for every string (machine-drafted, review pending).
- Excel import template, checker and Data Import split.
