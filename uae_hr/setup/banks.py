"""UAE banks seeded from uae_banks.csv: IBAN bank code, name, SWIFT, WPS routing code.

Insert-only by IBAN bank code: a code or a bank name already on the site is skipped, so a
company's own edits are never overwritten. Merged banks are kept, disabled, so old IBANs still
decode. Where the data comes from and how each row was checked: docs/banks.md.
"""

import csv
import os

import frappe

DATA = os.path.join(os.path.dirname(__file__), "uae_banks.csv")


def load_banks():
	with open(DATA, newline="", encoding="utf-8") as fh:
		return list(csv.DictReader(fh))


def seed_banks(banks=None):
	for row in load_banks() if banks is None else banks:
		code, name = row["bank_code"], row["bank_name"]
		if frappe.db.exists("UAE Bank", {"bank_code": code}) or frappe.db.exists("UAE Bank", name):
			continue
		doc = frappe.get_doc(
			{
				"doctype": "UAE Bank",
				"bank_name": name,
				"short_name": row.get("short_name") or "",
				"bank_code": code,
				"swift_code": row.get("swift_code") or "",
				"wps_routing_code": row.get("wps_routing_code") or "",
				"enabled": int(row.get("enabled", 1)),
				"notes": row.get("notes") or "",
			}
		)
		doc.flags.ignore_permissions = True
		doc.insert()
