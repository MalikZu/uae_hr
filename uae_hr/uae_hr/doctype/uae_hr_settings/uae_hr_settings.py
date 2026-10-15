# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

import frappe
from frappe import _
from frappe.model.document import Document

from uae_hr.law import PARAMS, less_favourable
from uae_hr.utils import parse_days


class UAEHRSettings(Document):
	def validate(self):
		self.validate_law_values()
		seen = set()
		for row in self.companies:
			if row.company in seen:
				frappe.throw(_("Company {0} is listed twice").format(row.company))
			seen.add(row.company)
		if self.default_reminder_days and not parse_days(self.default_reminder_days):
			frappe.throw(_("Default reminder days are whole numbers separated by commas, e.g. 60,30,7"))

	def validate_law_values(self):
		"""More generous than the law is fine (DL 65(1)). Anything else needs the amending resolution named."""
		changed = []
		for p in PARAMS:
			value = self.get(p.fieldname)
			if value in (None, ""):
				self.set(p.fieldname, p.default)
				continue
			if value <= 0:
				frappe.throw(_("{0} must be greater than zero").format(_(p.label)))
			if less_favourable(p, value):
				changed.append(f"{_(p.label)}: {value} ({_('law')}: {p.default}, {p.citation})")
		if changed and not (self.amendment_reference or "").strip():
			frappe.throw(
				_(
					"These values are less favourable to workers than the law, or change a value the law fixes. "
					"Name the resolution that amended them in Amendment Reference:"
				)
				+ "<br>"
				+ "<br>".join(changed),
				title=_("Amendment reference needed"),
			)

	def on_update(self):
		if self.has_value_changed("default_reminder_days") or self.has_value_changed("copy_hr_manager"):
			from uae_hr.setup.notifications import refresh_reminder_days

			refresh_reminder_days()


@frappe.whitelist()
def reset_to_law_defaults():
	frappe.only_for(("HR Manager", "System Manager"))
	doc = frappe.get_single("UAE HR Settings")
	for p in PARAMS:
		doc.set(p.fieldname, p.default)
	doc.save()
	return True
