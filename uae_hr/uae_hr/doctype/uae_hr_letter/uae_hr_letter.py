# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

"""Register of letters issued to employees. Submittable, so a letter cannot change after issue.

Print formats are deliberately not part of this app: each company ships its own on its letterhead.
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today

from uae_hr import checks
from uae_hr.law import get_param
from uae_hr.utils import apply_findings


class UAEHRLetter(Document):
	def before_validate(self):
		if self.letter_type == "Experience Certificate":
			self.fill_experience_defaults()

	def validate(self):
		findings = []
		if self.letter_type == "Experience Certificate":
			if self.service_start_date and self.service_end_date:
				self.total_service = checks.format_service(self.service_start_date, self.service_end_date)
			missing = [
				label
				for field, label in (
					("service_start_date", _("start of service")),
					("service_end_date", _("end of service")),
					("job_title", _("job title")),
					("last_wage", _("last wage")),
					("termination_reason", _("reason for end of service")),
				)
				if not self.get(field)
			]
			if missing:
				frappe.throw(
					_("An experience certificate must state the {0} (DL 13(11))").format(", ".join(missing))
				)
		if self.letter_type == "Warning":
			missing = [
				label
				for field, label in (
					("violation", _("violation")),
					("violation_detected_on", _("date the violation was detected")),
					("charged_on", _("date of the written charge")),
					("investigation_closed_on", _("date the investigation closed")),
				)
				if not self.get(field)
			]
			if missing:
				frappe.throw(
					_("A disciplinary warning needs the {0} (CR 24(3)-(4))").format(", ".join(missing))
				)
			findings += checks.check_warning_timing(
				self.violation_detected_on,
				self.charged_on,
				self.investigation_closed_on,
				self.issue_date,
				get_param("warning_charge_days"),
				get_param("warning_penalty_days"),
			)
		apply_findings(findings, title=_("Disciplinary time limits"))

	def fill_experience_defaults(self):
		emp = (
			frappe.db.get_value(
				"Employee",
				self.employee,
				["date_of_joining", "relieving_date", "designation", "reason_for_leaving"],
				as_dict=True,
			)
			or {}
		)
		self.service_start_date = self.service_start_date or emp.get("date_of_joining")
		self.service_end_date = self.service_end_date or emp.get("relieving_date")
		self.job_title = self.job_title or emp.get("designation")
		self.termination_reason = self.termination_reason or emp.get("reason_for_leaving")
		if not self.last_wage:
			self.last_wage = last_wage(self.employee, self.service_end_date or today())

	def on_trash(self):
		status, relieving_date = frappe.db.get_value("Employee", self.employee, ["status", "relieving_date"])
		apply_findings(
			checks.check_retention(status, relieving_date, get_param("file_retention_years"), today())
		)


def last_wage(employee, on_date):
	"""Monthly wage on the latest submitted assignment: the UAE components if used, else the base."""
	ssa = frappe.get_all(
		"Salary Structure Assignment",
		filters={"employee": employee, "docstatus": 1, "from_date": ("<=", on_date)},
		fields=["base", "uae_total"],
		order_by="from_date desc",
		limit=1,
	)
	if not ssa:
		return None
	return ssa[0].uae_total or ssa[0].base
