# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

"""One record per document, so history is kept and expiry notifications can fire on it.

Lifecycle: Unverified -> (Verify) Current -> Superseded when a newer one of the same type is verified,
Expired when the expiry date passes (daily job), Cancelled by hand. Verifying copies the mapped
values onto the Employee; those Employee fields are read-only and never typed by hand.
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, today

from uae_hr import checks
from uae_hr.law import get_param
from uae_hr.utils import apply_findings, has_role, reminder_days_for

VERIFIERS = ("HR Manager",)
LIVE = ("Current", "Expired")


class UAEEmployeeDocument(Document):
	def validate(self):
		if not self.employee and not self.job_applicant:
			frappe.throw(_("Link the document to an Employee or a Job Applicant"))
		dtype = frappe.get_cached_doc("UAE Document Type", self.document_type)
		self.check_profile = dtype.check_profile
		self.has_expiry = dtype.has_expiry
		self.reminder_days = reminder_days_for(self.document_type) if dtype.has_expiry else ""
		if dtype.has_expiry and not self.expiry_date:
			frappe.throw(_("{0} needs an expiry date").format(_(self.document_type)))
		if self.issue_date and self.expiry_date and getdate(self.expiry_date) <= getdate(self.issue_date):
			frappe.throw(_("The expiry date must be after the issue date"))
		if self.document_number:
			self.document_number = self.document_number.strip()
			if self.check_profile == "Emirates ID":
				self.document_number = checks.format_eid(self.document_number) or self.document_number
		self.validate_duplicate()
		findings = []
		if self.check_profile == "Emirates ID":
			findings += checks.check_emirates_id(self.document_number, self.date_of_birth)
		apply_findings(findings)

	def validate_duplicate(self):
		if not (self.employee and self.document_number):
			return
		dup = frappe.db.get_value(
			"UAE Employee Document",
			{
				"employee": self.employee,
				"document_type": self.document_type,
				"document_number": self.document_number,
				"status": ("!=", "Cancelled"),
				"name": ("!=", self.name or ""),
			},
			"name",
		)
		if dup:
			frappe.throw(
				_("{0} {1} is already recorded for this employee in {2}").format(
					_(self.document_type), self.document_number, frappe.bold(dup)
				),
				frappe.DuplicateEntryError,
			)

	def on_update(self):
		self.make_scan_private()

	def make_scan_private(self):
		"""A scan uploaded before the first save is not attached yet, so the File hook missed it."""
		if not self.file:
			return
		name = frappe.db.get_value("File", {"file_url": self.file, "is_private": 0}, "name")
		if not name:
			return
		file = frappe.get_doc("File", name)
		file.is_private = 1
		file.attached_to_doctype, file.attached_to_name, file.attached_to_field = (
			self.doctype,
			self.name,
			"file",
		)
		file.save(ignore_permissions=True)
		self.db_set("file", file.file_url)

	def on_trash(self):
		if not self.employee:
			return
		status, relieving_date = frappe.db.get_value("Employee", self.employee, ["status", "relieving_date"])
		apply_findings(
			checks.check_retention(status, relieving_date, get_param("file_retention_years"), today())
		)

	@frappe.whitelist()
	def verify(self):
		if not has_role(*VERIFIERS):
			frappe.throw(_("Only an HR Manager can verify documents"), frappe.PermissionError)
		if self.status != "Unverified":
			frappe.throw(
				_("Only an unverified document can be verified; this one is {0}").format(_(self.status))
			)
		if not self.employee:
			frappe.throw(_("Link the document to an Employee before verifying it"))
		findings = self.cross_check()
		for old in frappe.get_all(
			"UAE Employee Document",
			filters={
				"employee": self.employee,
				"document_type": self.document_type,
				"status": ("in", LIVE),
				"name": ("!=", self.name),
			},
			pluck="name",
		):
			frappe.db.set_value(
				"UAE Employee Document", old, {"status": "Superseded", "superseded_by": self.name}
			)
		self.status = (
			"Expired" if self.expiry_date and getdate(self.expiry_date) < getdate(today()) else "Current"
		)
		self.verified_by = frappe.session.user
		self.verified_on = now_datetime()
		self.save()
		self.mirror()
		apply_findings(findings, title=_("Verified, with warnings"))
		return [f.text() for f in findings]

	@frappe.whitelist()
	def cancel_document(self, reason=None):
		"""Mark as cancelled (e.g. a cancelled visa). If it was the current one, its mirrors are cleared."""
		self.check_permission("write")
		was_live = self.status in LIVE
		self.status = "Cancelled"
		if reason:
			self.notes = ((self.notes or "") + "\n" + _("Cancelled: {0}").format(reason)).strip()
		self.save()
		if was_live and self.employee:
			self.mirror(clear=True)

	def mirror(self, clear=False):
		values = {}
		meta = frappe.get_meta("Employee")
		for row in frappe.get_cached_doc("UAE Document Type", self.document_type).field_map:
			if not meta.has_field(row.employee_field):
				continue
			values[row.employee_field] = None if clear else self.get(row.document_field)
		if values:
			frappe.db.set_value("Employee", self.employee, values)
			frappe.clear_document_cache("Employee", self.employee)

	def cross_check(self) -> list:
		"""Checks across documents (plan 3.3): same birth date, passport on the visa, one visa designation."""
		emp = frappe.db.get_value(
			"Employee",
			self.employee,
			["date_of_birth", "passport_number", "uae_visa_designation"],
			as_dict=True,
		)
		out = []
		if (
			self.date_of_birth
			and emp.date_of_birth
			and getdate(self.date_of_birth) != getdate(emp.date_of_birth)
		):
			out.append(
				checks.Finding(
					checks.WARN,
					"dob_mismatch",
					_("Date of birth {0} on the {1} differs from the Employee record ({2})").format(
						getdate(self.date_of_birth), _(self.document_type), getdate(emp.date_of_birth)
					),
				)
			)
		if self.check_profile in ("Entry Permit", "Residence Visa") and self.passport_number:
			passport = current_value(self.employee, "Passport", "document_number") or emp.passport_number
			if passport and passport.strip().upper() != self.passport_number.strip().upper():
				out.append(
					checks.Finding(
						checks.WARN,
						"visa_passport",
						_("The {0} carries passport {1}, but the current passport is {2}").format(
							_(self.document_type), self.passport_number, passport
						),
					)
				)
		if (
			self.check_profile in ("Work Permit", "Residence Visa", "Emirates ID")
			and self.designation_on_document
		):
			seen = {
				p: current_value(self.employee, p, "designation_on_document")
				for p in ("Work Permit", "Residence Visa", "Emirates ID")
				if p != self.check_profile
			}
			if emp.uae_visa_designation:
				seen["Employee"] = emp.uae_visa_designation
			differ = {
				k: v
				for k, v in seen.items()
				if v and v.strip().lower() != self.designation_on_document.strip().lower()
			}
			if differ:
				out.append(
					checks.Finding(
						checks.WARN,
						"designation_mismatch",
						_("Designation {0} differs from {1}").format(
							self.designation_on_document, ", ".join(f"{_(k)}: {v}" for k, v in differ.items())
						),
					)
				)
		return out


def current_value(employee, check_profile, field):
	return frappe.db.get_value(
		"UAE Employee Document",
		{"employee": employee, "check_profile": check_profile, "status": ("in", LIVE)},
		field,
		order_by="verified_on desc",
	)


@frappe.whitelist()
def verify_many(names):
	"""List-view bulk action. Returns per-document results instead of stopping at the first error."""
	names = frappe.parse_json(names)
	results = []
	for i, name in enumerate(names):
		savepoint = f"uae_verify_{i}"
		frappe.db.savepoint(savepoint)
		try:
			doc = frappe.get_doc("UAE Employee Document", name)
			frappe.flags.uae_hr_quiet = True
			warnings = doc.verify()
			results.append({"name": name, "ok": True, "warnings": warnings})
		except Exception as e:
			frappe.db.rollback(save_point=savepoint)
			results.append({"name": name, "ok": False, "error": frappe.utils.strip_html(str(e))})
		finally:
			frappe.flags.uae_hr_quiet = False
	return results


def mark_expired():
	"""Daily: Current documents past their expiry date become Expired. Mirrors keep the date."""
	for name in frappe.get_all(
		"UAE Employee Document", filters={"status": "Current", "expiry_date": ("<", today())}, pluck="name"
	):
		frappe.db.set_value("UAE Employee Document", name, "status", "Expired")


def make_files_private(doc, method=None):
	"""File after_insert: scans of official documents are never public. File moves the file on save."""
	if doc.attached_to_doctype == "UAE Employee Document" and not doc.is_private and not doc.is_folder:
		doc.is_private = 1
		doc.save(ignore_permissions=True)
