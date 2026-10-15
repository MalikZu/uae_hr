"""Fingerprint of everything uae_hr writes, to prove a second `bench migrate` is a no-op.

	bench --site <site> execute uae_hr.setup.snapshot.fingerprint

Used by dev/check-migrate-noop.sh and CI: migrate, fingerprint, migrate, fingerprint, compare.
"""

import hashlib
import json

import frappe


def fingerprint(dump=None):
	out = {}
	for dt, filters in (
		("Custom Field", {"module": "UAE HR"}),
		("Property Setter", {"module": "UAE HR"}),
		("Notification", {"module": "UAE HR"}),
		("Custom DocPerm", {"parent": "Employee"}),
		("UAE Document Type", {}),
		("UAE Permit Type", {}),
		("UAE Issued Item Type", {}),
		("Salary Component", {}),
		("Role", {"name": "UAE PRO"}),
		("DocType", {"module": "UAE HR"}),
		("Report", {"module": "UAE HR"}),
		("Workspace", {"module": "UAE HR"}),
	):
		out[dt] = sorted(
			[r.name, str(r.modified)]
			for r in frappe.get_all(dt, filters=filters, fields=["name", "modified"])
		)
	out["Singles"] = sorted(
		map(list, frappe.db.sql("select field, value from tabSingles where doctype='UAE HR Settings'"))
	)
	out["columns"] = sorted(
		map(
			list,
			frappe.db.sql(
				"select table_name, column_name, column_type from information_schema.columns where table_schema=database() "
				"and (table_name like 'tabUAE %%' or column_name like 'uae\\_%%')"
			),
		)
	)
	blob = json.dumps(out, sort_keys=True, default=str)
	if dump:
		with open(dump, "w") as fh:
			fh.write(blob)
	digest = hashlib.sha256(blob.encode()).hexdigest()
	print(digest, json.dumps({k: len(v) for k, v in out.items()}))
	return digest
