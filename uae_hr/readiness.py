"""Contract readiness: what CR 10(1) says an employment contract must contain, checked against the record.

Run before the MOHRE contract is prepared. It lists gaps; it never blocks, because the contract is
made in MOHRE's system, not here.
"""

import frappe
from frappe import _

CR10 = "CR 10(1)"


def _item(label, ok, citation=CR10, hint=None, manual=False):
	return {"item": label, "ok": bool(ok), "citation": citation, "hint": hint or "", "manual": manual}


@frappe.whitelist()
def get_contract_readiness(employee):
	emp = frappe.get_doc("Employee", employee)
	emp.check_permission("read")
	items = []

	address = frappe.db.exists(
		"Dynamic Link", {"link_doctype": "Company", "link_name": emp.company, "parenttype": "Address"}
	)
	items.append(
		_item(
			_("Employer name and address"),
			emp.company and address,
			hint=_("Add an Address linked to the company"),
		)
	)
	items.append(_item(_("Worker name"), emp.employee_name))
	items.append(_item(_("Nationality"), emp.uae_nationality))
	items.append(_item(_("Date of birth"), emp.date_of_birth))
	identity = frappe.db.exists(
		"UAE Employee Document",
		{"employee": emp.name, "status": "Current", "check_profile": ("in", ("Passport", "Emirates ID"))},
	)
	items.append(_item(_("Proof of identity (verified passport or Emirates ID)"), identity))
	items.append(_item(_("Qualification"), emp.get("education"), hint=_("Add a row under Education")))
	items.append(_item(_("Job (visa designation)"), emp.uae_visa_designation or emp.designation))
	items.append(_item(_("Commencement date"), emp.date_of_joining))
	items.append(_item(_("Workplace (branch)"), emp.branch, hint=_("Set the Branch the worker reports to")))
	items.append(_item(_("Working hours (default shift)"), emp.get("default_shift")))
	holiday_list = emp.holiday_list or frappe.get_cached_value("Company", emp.company, "default_holiday_list")
	items.append(_item(_("Rest days (holiday list)"), holiday_list))
	items.append(
		_item(
			_("Contract term (end date)"),
			emp.contract_end_date,
			citation="CR 10(1), DL 8(3)",
			hint=_("Contracts are fixed-term"),
		)
	)
	items.append(
		_item(
			_("Wage, with allowances"),
			_has_pay(emp.name),
			hint=_("Submit a Salary Structure Assignment with the basic wage"),
		)
	)
	items.append(
		_item(_("Annual leave entitlement"), _has_leave_policy(emp.name), hint=_("Assign a Leave Policy"))
	)
	items.append(_item(_("Notice period"), emp.notice_number_of_days, citation="CR 10(1), DL 43"))
	items.append(
		_item(_("Second contract language beside Arabic"), emp.uae_contract_language, citation="DL 66")
	)
	items.append(
		_item(
			_("Termination procedures"),
			True,
			manual=True,
			hint=_("Stated in the contract text; check it by hand"),
		)
	)

	for dt in _required_documents(emp):
		have = frappe.db.exists(
			"UAE Employee Document", {"employee": emp.name, "document_type": dt, "status": "Current"}
		)
		items.append(
			_item(
				_("Document: {0}").format(_(dt)),
				have,
				citation=_("Permit type {0}").format(emp.uae_permit_type),
			)
		)

	missing = [i for i in items if not i["ok"]]
	return {"employee": emp.name, "ready": not missing, "missing": len(missing), "items": items}


def _has_pay(employee):
	return frappe.db.exists(
		"Salary Structure Assignment", {"employee": employee, "docstatus": 1, "uae_basic": (">", 0)}
	)


def _has_leave_policy(employee):
	return frappe.db.exists("Leave Policy Assignment", {"employee": employee, "docstatus": 1})


def _required_documents(emp):
	if not emp.uae_permit_type:
		return []
	return frappe.get_all(
		"UAE Document Type Permit",
		filters={"permit_type": emp.uae_permit_type, "parenttype": "UAE Document Type"},
		pluck="parent",
		distinct=True,
		order_by="parent",
	)
