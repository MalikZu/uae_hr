"""Employee hooks: the legal checks that run on save, IBAN handling and the Connections tab."""

import frappe
from frappe import _

from uae_hr import checks
from uae_hr.law import get_param
from uae_hr.utils import apply_findings, is_covered

IDENTITY_FIELDS = ("uae_uid", "uae_emirates_id", "passport_number", "uae_person_code")


def validate(doc, method=None):
	findings = []
	sync_bank(doc, findings)
	if not is_covered(doc.company):
		apply_findings(findings)
		return

	max_months = get_param("probation_max_months")
	if doc.uae_probation_months and doc.uae_probation_months > 0 and doc.date_of_joining:
		# the months are the source; the HRMS confirmation date follows them
		doc.final_confirmation_date = checks.probation_end(
			doc.date_of_joining, min(doc.uae_probation_months, max_months)
		)
	findings += checks.check_probation(
		doc.uae_probation_months, max_months, doc.date_of_joining, doc.final_confirmation_date
	)
	findings += checks.check_notice(
		doc.notice_number_of_days, get_param("notice_min_days"), get_param("notice_max_days")
	)
	findings += checks.check_emirates_id(doc.uae_emirates_id, doc.date_of_birth)
	findings += checks.check_person_code(doc.uae_person_code)
	findings += checks.check_nominee(doc.uae_death_nominee, doc.uae_death_nominee_relation)
	findings += check_probation_once(doc)
	findings += checks.check_engagement(doc.uae_engagement_type, doc.uae_payment_method)
	if doc.status == "Left" and (doc.is_new() or doc.has_value_changed("status")):
		findings += checks.check_unreturned_items(doc.get("uae_issued_items") or [])
	apply_findings(findings)


def sync_bank(doc, findings):
	"""IBAN -> UAE Bank and account number. HRMS checks the IBAN format; this adds the checksum and bank code."""
	if doc.iban:
		doc.iban = checks.normalize_iban(doc.iban)
		findings += checks.check_iban(doc.iban)
		parts = checks.uae_iban_parts(doc.iban)
		if parts and checks.iban_checksum_ok(doc.iban):
			bank_code, account = parts
			bank = frappe.db.get_value("UAE Bank", {"bank_code": bank_code}, "name")
			if bank and not frappe.db.get_value("UAE Bank", bank, "enabled"):
				# merged banks are kept, disabled, so an old IBAN still decodes
				findings.append(
					checks.Finding(
						checks.WARN,
						"iban_bank_merged",
						_(
							"The IBAN is from {0}, which no longer operates under that name. Ask the worker for the current IBAN"
						).format(bank),
					)
				)
			if bank and not doc.uae_bank:
				doc.uae_bank = bank
			elif bank and doc.uae_bank != bank:
				findings.append(
					checks.Finding(
						checks.WARN,
						"iban_bank",
						_("The IBAN belongs to {0}, but the bank is set to {1}").format(bank, doc.uae_bank),
					)
				)
			elif not bank:
				findings.append(
					checks.Finding(
						checks.WARN,
						"iban_bank_unknown",
						_("No UAE Bank has IBAN bank code {0}. Add it to the UAE Bank list").format(
							bank_code
						),
					)
				)
			if not doc.bank_ac_no:
				doc.bank_ac_no = account
			elif doc.bank_ac_no.lstrip("0") != account.lstrip("0"):
				findings.append(
					checks.Finding(
						checks.WARN,
						"iban_account",
						_("Bank account number {0} is not the account inside the IBAN ({1})").format(
							doc.bank_ac_no, account
						),
					)
				)
	if doc.uae_bank:
		doc.bank_name = frappe.get_cached_value("UAE Bank", doc.uae_bank, "bank_name")


def check_probation_once(doc):
	"""DL 9(2): a worker may be put on probation only once by the same employer.

	A re-hire is a second Employee record of the same person in the same company. Only warns: the
	person match relies on identity numbers that may be missing or typed differently.
	"""
	if not (doc.uae_probation_months or 0) > 0:
		return []
	if not doc.is_new() and not doc.has_value_changed("uae_probation_months"):
		return []
	ors = {f: doc.get(f) for f in IDENTITY_FIELDS if doc.get(f)}
	if not ors:
		return []
	earlier = frappe.get_all(
		"Employee",
		filters={"company": doc.company, "name": ("!=", doc.name or "")},
		or_filters=ors,
		fields=["name", "employee_name", "uae_probation_months", "final_confirmation_date"],
	)
	had_probation = [e for e in earlier if (e.uae_probation_months or 0) > 0 or e.final_confirmation_date]
	if not had_probation:
		return []
	return [
		checks.Finding(
			checks.WARN,
			"probation_twice",
			_(
				"{0} was already employed by this company with a probation period ({1}). A worker may be put on probation only once by the same employer"
			).format(doc.employee_name or doc.first_name, ", ".join(e.name for e in had_probation)),
			"DL 9(2)",
		)
	]


def get_dashboard_data(data):
	data.setdefault("transactions", []).append(
		{"label": _("UAE Documents and Letters"), "items": ["UAE Employee Document", "UAE HR Letter"]}
	)
	data.setdefault("non_standard_fieldnames", {})
	return data


@frappe.whitelist()
def get_form_context(employee):
	"""What the Employee form shows: coverage and the probation hint."""
	doc = frappe.get_doc("Employee", employee)
	doc.check_permission("read")
	covered = is_covered(doc.company)
	return {
		"covered": covered,
		"probation_employer_notice_days": get_param("probation_employer_notice_days"),
		"probation_max_months": get_param("probation_max_months"),
	}
