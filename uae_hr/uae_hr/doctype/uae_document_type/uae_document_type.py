# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

import frappe
from frappe import _
from frappe.model.document import Document

from uae_hr.utils import format_days, parse_days, reminder_days_for


class UAEDocumentType(Document):
	def validate(self):
		if self.reminder_days:
			days = parse_days(self.reminder_days)
			if not days:
				frappe.throw(_("Reminder days are whole numbers separated by commas, e.g. 60,30,7"))
			self.reminder_days = format_days(days)
		meta = frappe.get_meta("Employee")
		for row in self.field_map:
			if not meta.has_field(row.employee_field):
				frappe.throw(
					_("Row {0}: Employee has no field {1}").format(row.idx, frappe.bold(row.employee_field))
				)

	def on_update(self):
		if self.has_value_changed("reminder_days") or self.has_value_changed("has_expiry"):
			# the cached copy of this type is still the old one here, so use self
			days = (
				(format_days(parse_days(self.reminder_days)) or reminder_days_for(None))
				if self.has_expiry
				else ""
			)
			frappe.db.set_value(
				"UAE Employee Document",
				{"document_type": self.name},
				"reminder_days",
				days,
				update_modified=False,
			)
			from uae_hr.setup.notifications import sync_notifications

			sync_notifications()
