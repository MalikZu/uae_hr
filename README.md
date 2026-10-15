# UAE HR

A [Frappe HR](https://github.com/frappe/hrms) app that makes HR records follow UAE private-sector labour law:
Federal Decree-Law No. 33 of 2021 and its implementing regulation, Cabinet Resolution No. 1 of 2022.

> **Not legal advice.** UAE HR encodes the law as published in English by the Ministry of Human Resources and
> Emiratisation (MOHRE). The Arabic text prevails where the two differ (DL 66), and the Cabinet may change any
> period, percentage or value in the law (DL 70(7)). The software can be wrong, and so can its reading of the law.
> Check anything that matters with a qualified adviser. You use it at your own risk (see the GPL-3.0 licence,
> sections 15 and 16).

Status: **v0.1, early.** Built and tested on Frappe 16 / ERPNext 16 / HRMS 16. Not yet used in production.

## What it does

**Employee records**
- UAE fields on Employee, all prefixed `uae_`: nationality, name as on passport and in Arabic, UID, work-permit
  type (the 12 types of CR 6(1)), skill category, visa designation, MOHRE person code, probation in months,
  second contract language (DL 66), accommodation (DL 13(4)), death-entitlements nominee (DL 15(2)), bank / IBAN /
  salary card, and a table of company property issued to the worker.
- Who sponsors the visa and how the worker is engaged: **UAE Establishment** (the visa sponsor, often not the ERP
  company), visa emirate, engagement type (salaried, visa only, daily wage on another sponsor's visa, absconded,
  left with the visa still active, not salaried) and payment method (WPS bank account or salary card, cash, on
  hold, not paid by us).
- **UAE Employee Document**: one record per passport, visa, Emirates ID, work permit, contract, insurance and so on,
  with a private scan. **Verify** (HR Manager) makes it current, supersedes the previous one of that type and
  copies its values to the Employee (passport number and dates, Emirates ID, visa and permit expiry). Those
  Employee fields become read-only: they are only ever set from a verified document. A verified document is locked;
  an HR Manager can **Reopen** it to correct a mistake and verify it again. Renewals that keep their number (an
  Emirates ID does) are recorded as a new document with the new expiry date. The MOHRE contract document carries
  the contract salary, and a Salary Structure Assignment below it is warned.
- Expiry reminders as standard Frappe Notifications to the **UAE PRO** role (HR Manager in copy), with lead times
  per document type, plus an **Expiring Documents** report for the next 90 days and anything overdue.
- **UAE HR Letter**: a submittable register of salary certificates, experience certificates, warnings, NOCs. Print
  formats are left to you, on your letterhead.
- Salary components **Basic, Housing, Transport, Other** that read amounts from the Salary Structure Assignment, so
  one salary structure fits everyone and the basic wage stays separate (gratuity is calculated on it, DL 51(5)). An
  empty base is filled with their sum.
- The Exit tab lists issued items not yet returned, and leaving with items still out is warned.

**Checks, each with its article**

| Rule | Source | Behaviour |
|---|---|---|
| Probation at most 6 months | DL 9(1) | blocks save |
| Probation only once per employer | DL 9(2) | warns when a re-hired worker gets probation again |
| Employer gives 14 days' written notice to end probation | DL 9(1) | shown on the Employee during probation |
| Notice between 30 and 90 days | DL 43(1) | blocks save |
| Contract contents | CR 10(1) | **Contract Readiness** lists what is missing before the MOHRE contract is made |
| Worker file kept 2 years after the end of service | DL 13(1) | blocks deleting documents and letters of a worker who left |
| Official documents are not withheld | DL 13(2) | an official document cannot be an "issued item"; documents are scans only |
| Free experience certificate with start, end, service, job, last wage, reason | DL 13(11) | required on the letter |
| Nominee is a family member (spouse, son, daughter) | DL 15(2), DL 1 | blocks other relations |
| Charge within 30 days, penalty within 60 days of the investigation | CR 24(4) | warns on a warning letter |
| Basic wage separate from allowances | DL 1, DL 51(5) | warns when allowances have no basic |
| Emirates ID format and check digit, IBAN checksum and bank code, same birth date and passport across documents, one visa designation | (data quality) | warnings |

Every legal number is a field in **UAE HR Settings**, defaulting to the law, with the article in its description
(`uae_hr/law.py` is the single source). A company may make a value more generous to workers (DL 65(1)); making it
less favourable needs the amending resolution named in the settings.

**Jurisdiction.** Per company: mainland (MOHRE) and free zones under the federal law are covered. DIFC and ADGM have
their own employment laws, so the checks switch off there. A company that is not listed is covered only if its
country is the UAE.

**Arabic** translations ship for every label and message (`uae_hr/translations/ar.csv`). They are machine-drafted
and need a native speaker's review; corrections are very welcome.

## Install

```bash
cd frappe-bench
bench get-app erpnext --branch version-16
bench get-app hrms --branch version-16
bench get-app https://github.com/MalikZu/uae_hr --branch main
bench --site <site> install-app uae_hr
```

Then, in **UAE HR Settings**: list your companies (jurisdiction, emirate, MOHRE establishment ID, WPS agent bank) and
check the reminder days. Check **UAE Bank** (3-digit IBAN code, SWIFT) and add the 9-digit WPS routing codes from
your WPS agent. Add the establishments that sponsor your workers' visas to **UAE Establishment**. Give your PRO the
**UAE PRO** role.

Uninstalling removes the app's doctypes, fields, permission rows, notifications, report and workspace, and gives the
standard Employee passport fields their normal behaviour back. As with any Frappe app, the data columns of the
removed fields stay in the database until `bench trim-tables`, and the four salary components stay because salary
structures may use them.

## Moving from spreadsheets

```bash
bench --site <site> execute uae_hr.importer.make_template --args "['/tmp/uae_hr_import.xlsx']"
# fill it in, then:
bench --site <site> execute uae_hr.importer.check --args "['/tmp/uae_hr_import.xlsx']"
bench --site <site> execute uae_hr.importer.split --args "['/tmp/uae_hr_import.xlsx', '/tmp/uae_hr_import']"
```

`check` runs every check on the workbook and writes nothing; it lists errors and warnings and saves them next to
the file. `split` writes one file per sheet for Frappe's standard **Data Import**. Imported documents arrive
unverified: select them in the list and use **Actions > Verify**.

## Not covered yet

Hiring and the visa process, leave policies, end-of-service gratuity, and the WPS salary file are not part of this
version.

HRMS ships three UAE gratuity rules written for the 1980 law; they reduce gratuity on resignation, which the 2021
law does not. Do not use them for final settlements.

The cited rules are in [docs/law.md](docs/law.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Law changes need the article and the source.

## Licence

GNU General Public License v3.0. See [LICENSE](LICENSE).
