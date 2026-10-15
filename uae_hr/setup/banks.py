"""UAE banks: IBAN bank code, name and SWIFT, seeded insert-only by bank code.

Only codes verified against a primary source go here (the bank's own published IBAN / SWIFT
details, or the UAE Central Bank). Name the source on each row. WPS routing codes are not seeded:
they come from each company's WPS agent.

A site's own edits are never overwritten: a code that already exists, or a bank name that already
exists, is skipped.
"""

import frappe

# (IBAN bank code, bank name, short name, SWIFT / BIC, source)
BANKS: list[tuple[str, str, str, str, str]] = []


def seed_banks(banks=None):
	for code, name, short_name, swift, _source in BANKS if banks is None else banks:
		if frappe.db.exists("UAE Bank", {"bank_code": code}) or frappe.db.exists("UAE Bank", name):
			continue
		doc = frappe.get_doc(
			{
				"doctype": "UAE Bank",
				"bank_name": name,
				"short_name": short_name,
				"bank_code": code,
				"swift_code": swift,
			}
		)
		doc.flags.ignore_permissions = True
		doc.insert()
