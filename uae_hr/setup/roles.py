import frappe
from frappe.permissions import add_permission, update_permission_property

PRO = "UAE PRO"
# roles that see and edit the salary-related Employee fields (permlevel 1)
PAY_ROLES = ("HR Manager", "HR User", "System Manager")


def make_roles():
	if not frappe.db.exists("Role", PRO):
		frappe.get_doc({"doctype": "Role", "role_name": PRO, "desk_access": 1}).insert(
			ignore_permissions=True
		)


def make_docperms():
	"""UAE PRO reads Employee without the pay fields. add_permission copies the standard rules to
	Custom DocPerm first, so the existing roles keep exactly what they had."""
	_grant("Employee", PRO, 0, read=1, report=1, print=1)
	for role in PAY_ROLES:
		_grant("Employee", role, 1, read=1, write=1)


def _grant(doctype, role, permlevel, **rights):
	if not frappe.db.exists("Role", role):
		return
	existing = frappe.db.get_value(
		"Custom DocPerm", {"parent": doctype, "role": role, "permlevel": permlevel, "if_owner": 0}, "name"
	)
	if not existing:
		add_permission(doctype, role, permlevel)
		existing = frappe.db.get_value(
			"Custom DocPerm", {"parent": doctype, "role": role, "permlevel": permlevel, "if_owner": 0}, "name"
		)
	current = frappe.db.get_value("Custom DocPerm", existing, list(rights), as_dict=True)
	for right, value in rights.items():
		if current.get(right) != value:
			update_permission_property(doctype, role, permlevel, right, value)


def remove_docperms():
	"""Uninstall: drop the rows this app added. The copied standard rows are equal to the standard ones."""
	for name in frappe.get_all("Custom DocPerm", filters={"role": PRO}, pluck="name"):
		frappe.delete_doc("Custom DocPerm", name, ignore_permissions=True, force=True)
	for role in PAY_ROLES:
		for name in frappe.get_all(
			"Custom DocPerm", filters={"parent": "Employee", "role": role, "permlevel": 1}, pluck="name"
		):
			frappe.delete_doc("Custom DocPerm", name, ignore_permissions=True, force=True)
	frappe.clear_cache(doctype="Employee")
