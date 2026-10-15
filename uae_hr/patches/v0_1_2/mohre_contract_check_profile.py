"""0.1.2: the seeded MOHRE Employment Contract type gets its own check profile (contract salary fields).

Seeds are insert-only, so sites installed before 0.1.2 keep an empty profile; set it there, and on
the documents of that type, unless the site already chose another profile.
"""

import frappe

NAME = "MOHRE Employment Contract"


def execute():
	if not frappe.db.exists("UAE Document Type", NAME):
		return
	if frappe.db.get_value("UAE Document Type", NAME, "check_profile"):
		return
	frappe.db.set_value("UAE Document Type", NAME, "check_profile", NAME, update_modified=False)
	frappe.db.set_value(
		"UAE Employee Document",
		{"document_type": NAME, "check_profile": ("in", ("", None))},
		"check_profile",
		NAME,
		update_modified=False,
	)
