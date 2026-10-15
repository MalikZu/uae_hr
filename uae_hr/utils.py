import frappe
from frappe import _

from uae_hr.checks import BLOCK, blocks

NOT_COVERED = ("DIFC (not covered)", "ADGM (not covered)")
UAE = "United Arab Emirates"


def company_setup(company):
	if not company:
		return None
	rows = frappe.get_all(
		"UAE Company Setup", filters={"parent": "UAE HR Settings", "company": company}, fields=["*"], limit=1
	)
	return rows[0] if rows else None


def is_covered(company) -> bool:
	"""Whether the federal labour law, and so this app's checks, apply to this company.

	Listed companies follow their jurisdiction (DIFC and ADGM have their own employment laws, plan U9).
	Unlisted companies are covered when their country is the UAE, so a site that also holds a company
	elsewhere is not affected.
	"""
	if not company:
		return False
	row = company_setup(company)
	if row:
		return row.jurisdiction not in NOT_COVERED
	return frappe.get_cached_value("Company", company, "country") == UAE


def parse_days(value) -> list[int]:
	out = []
	for part in (value or "").replace(";", ",").split(","):
		part = part.strip()
		if part.isdigit() and int(part) > 0:
			out.append(int(part))
	return sorted(set(out), reverse=True)


def format_days(days) -> str:
	return ",".join(str(d) for d in sorted(set(days), reverse=True))


def reminder_days_for(document_type) -> str:
	"""The type's own reminder days, else the settings default."""
	own = (
		frappe.get_cached_value("UAE Document Type", document_type, "reminder_days")
		if document_type
		else None
	)
	if parse_days(own):
		return format_days(parse_days(own))
	default = frappe.db.get_single_value("UAE HR Settings", "default_reminder_days") or "60,30,7"
	return format_days(parse_days(default))


def apply_findings(findings, title=None):
	"""Throw on any block finding, show the warnings."""
	if not findings:
		return
	title = title or _("UAE labour law check")
	hard = blocks(findings)
	if hard:
		frappe.throw("<br>".join(f.text() for f in hard), title=title)
	# kept on the request so tests and the import checker can read what was shown
	frappe.flags.uae_hr_warnings = (frappe.flags.uae_hr_warnings or []) + list(findings)
	if frappe.flags.in_import or frappe.flags.in_test or frappe.flags.uae_hr_quiet:
		return
	frappe.msgprint("<br>".join(f.text() for f in findings), title=title, indicator="orange")


def has_role(*roles):
	user_roles = set(frappe.get_roles())
	return "System Manager" in user_roles or bool(user_roles.intersection(roles))
