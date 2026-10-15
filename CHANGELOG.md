# Changelog

Each entry names the article behind the change. Versions follow semantic versioning.

## 0.1.2 (2026-10-16)

Fixes and additions from the first HR test.

- A verified UAE Employee Document is locked (identity, dates, names, birth date, passport number, contract pay and
  every mirrored field), so the Employee mirror cannot drift. **Reopen** (HR Manager) puts it back to Unverified;
  the mirror keeps its values until it is verified again. A reopened older document cannot take over from a newer
  one when re-verified.
- Renewals: the duplicate check refuses only an Unverified or Current record with the same number **and** expiry
  date, so a renewal that keeps its number (an Emirates ID) can be recorded. The message links the existing record.
- New master **UAE Establishment** (the visa sponsor) and Employee fields `uae_visa_establishment`,
  `uae_visa_emirate`, `uae_engagement_type`, `uae_payment_method`; a salaried worker with no payment method is
  warned (CR 16(1)(b)).
- MOHRE contract salary (`contract_basic`, `contract_housing`, `contract_transport`, `contract_other`,
  `contract_total`) on the MOHRE Employment Contract document, with its own check profile; a patch sets the profile
  on earlier sites.
- Salary Structure Assignment: an empty base becomes the sum of the four parts (a set base is kept); pay below the
  Current MOHRE contract is warned (DL 22(1)). The "base is neither basic nor total" warning is removed.
- Contract Readiness also from a button inside the Employee UAE tab.
- Exit tab lists unreturned issued items; setting the status to Left with items out is warned.
- UAE Bank list seeded with 51 banks (IBAN code, SWIFT, WPS routing code where the sources agree), insert-only;
  merged banks kept disabled so old IBANs decode, and warned on an Employee. Sources: docs/banks.md.
- Import workbook and checker cover the new fields.

## 0.1.1 (2026-10-15)

Fixes found while building a company layer on 0.1.0.

- UAE Employee Document allows Data Import, so the Documents sheet from the Excel split can be imported;
  System Manager, HR Manager and HR User get the import right, as on Employee.
- Tests no longer assume out-of-the-box reminder days: the reminder and notification tests set them in setUp,
  so the suite passes on a site where document types have their own reminder days.

## 0.1.0 (2026-10-15)

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
