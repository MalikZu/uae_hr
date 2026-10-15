import frappe


def before_install():
	# doctype permissions name the role, so it has to exist before the doctypes are synced
	from uae_hr.setup.roles import make_roles

	make_roles()


def after_install():
	from uae_hr.setup import run_setup

	run_setup()


def before_migrate():
	before_install()


def after_migrate():
	from uae_hr.setup import run_setup

	run_setup()


def before_uninstall():
	"""Custom fields, property setters, notifications, workspace and reports carry module UAE HR, so
	Frappe deletes them with the module. The permission rows have no module; remove them here."""
	from uae_hr.setup.roles import remove_docperms

	remove_docperms()
	for doctype in ("Workspace Sidebar", "Desktop Icon"):
		if frappe.db.exists("DocType", doctype):
			for name in frappe.get_all(doctype, filters={"app": "uae_hr"}, pluck="name"):
				frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)
