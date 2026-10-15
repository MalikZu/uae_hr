"""Idempotent site setup, run after install and after every migrate.

Every step compares before it writes, so a second `bench migrate` changes nothing.
"""

import frappe


def run_setup():
	from uae_hr.setup.banks import seed_banks
	from uae_hr.setup.custom_fields import make_custom_fields, make_property_setters
	from uae_hr.setup.masters import seed_masters, seed_settings
	from uae_hr.setup.notifications import sync_notifications
	from uae_hr.setup.roles import make_docperms, make_roles
	from uae_hr.setup.salary import seed_components

	make_roles()
	make_custom_fields()
	make_property_setters()
	make_docperms()
	seed_settings()
	seed_masters()
	seed_components()
	seed_banks()
	sync_notifications()
	frappe.db.commit()
