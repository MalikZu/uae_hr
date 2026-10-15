"""Basic / Housing / Transport / Other as salary components reading the SSA amounts (plan 3.7).

HRMS puts every Salary Structure Assignment field into the formula context
(hrms.payroll.utils.get_component_eval_context), so one structure with these formulas serves everyone.
"""

import frappe

COMPONENTS = [
	("Basic", "B", "uae_basic"),
	("Housing Allowance", "HA", "uae_housing"),
	("Transport Allowance", "TA", "uae_transport"),
	("Other Allowance", "OA", "uae_other"),
]


def seed_components():
	for name, abbr, field in COMPONENTS:
		if frappe.db.exists("Salary Component", name):
			continue
		if frappe.db.exists("Salary Component", {"salary_component_abbr": abbr}):
			abbr = "UAE_" + abbr
		doc = frappe.get_doc(
			{
				"doctype": "Salary Component",
				"salary_component": name,
				"salary_component_abbr": abbr,
				"type": "Earning",
				"depends_on_payment_days": 1,
				"amount_based_on_formula": 1,
				"formula": field,
				"description": f"Monthly amount from Salary Structure Assignment field {field}",
			}
		)
		doc.flags.ignore_permissions = True
		doc.insert()
