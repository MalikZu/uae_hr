"""Salary Structure Assignment: total of the UAE components, base, and checks against the contract."""

import frappe
from frappe.utils import flt

from uae_hr import checks
from uae_hr.utils import apply_findings, is_covered

PARTS = ("uae_basic", "uae_housing", "uae_transport", "uae_other")
CONTRACT_PROFILE = "MOHRE Employment Contract"


def validate_assignment(doc, method=None):
	parts = [flt(doc.get(f)) for f in PARTS]
	doc.uae_total = sum(parts)
	# an app on top may add components and set base itself, so only fill an empty base
	if doc.uae_total and not flt(doc.base):
		doc.base = doc.uae_total
	if not is_covered(doc.company) or not doc.uae_total:
		return
	findings = checks.check_pay_split(*parts)
	contract = current_contract(doc.employee)
	if contract:
		findings += checks.check_pay_vs_contract(
			parts[0], doc.uae_total, contract.contract_basic, contract.contract_total, contract.name
		)
	apply_findings(findings)


def current_contract(employee):
	if not employee:
		return None
	rows = frappe.get_all(
		"UAE Employee Document",
		filters={"employee": employee, "check_profile": CONTRACT_PROFILE, "status": "Current"},
		fields=["name", "contract_basic", "contract_total"],
		order_by="verified_on desc",
		limit=1,
	)
	return rows[0] if rows else None
