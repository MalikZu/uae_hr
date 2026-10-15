# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

"""Documents expiring in the next N days, and those already past expiry, for the PRO's renewal list."""

import frappe
from frappe import _
from frappe.utils import add_days, cint, date_diff, getdate, today


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120,
		},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
		{
			"label": _("Document Type"),
			"fieldname": "document_type",
			"fieldtype": "Link",
			"options": "UAE Document Type",
			"width": 150,
		},
		{"label": _("Document Number"), "fieldname": "document_number", "fieldtype": "Data", "width": 150},
		{"label": _("Expiry Date"), "fieldname": "expiry_date", "fieldtype": "Date", "width": 110},
		{"label": _("Days Left"), "fieldname": "days_left", "fieldtype": "Int", "width": 90},
		{"label": _("State"), "fieldname": "state", "fieldtype": "Data", "width": 90},
		{
			"label": _("Document"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "UAE Employee Document",
			"width": 150,
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 140,
		},
	]


def get_data(filters):
	days = cint(filters.days) if filters.days not in (None, "") else 90
	horizon = add_days(today(), days)
	conditions = {
		"status": ("in", ("Current", "Expired")),
		"expiry_date": ("<=", horizon),
		"employee": ("is", "set"),
	}
	for field in ("company", "document_type", "employee"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	rows = frappe.get_all(
		"UAE Employee Document",
		filters=conditions,
		fields=[
			"name",
			"employee",
			"employee_name",
			"document_type",
			"document_number",
			"expiry_date",
			"company",
		],
		order_by="expiry_date asc",
	)
	active = (
		set(frappe.get_all("Employee", filters={"status": "Active"}, pluck="name"))
		if not filters.include_inactive
		else None
	)
	out = []
	for r in rows:
		if active is not None and r.employee not in active:
			continue
		r.days_left = date_diff(r.expiry_date, today())
		if r.days_left < 0 and not cint(filters.get("include_overdue", 1)):
			continue
		r.state = _("Overdue") if r.days_left < 0 else _("Due")
		out.append(r)
	return out
