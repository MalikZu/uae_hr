"""Fields on standard doctypes. All prefixed `uae_` and owned by module UAE HR, so uninstall removes
exactly these and leaves the standard HRMS fields alone."""

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

MODULE = "UAE HR"
# salary-related fields: hidden from UAE PRO, who reads Employee at permlevel 0 only (plan 3.9)
PAY = 1

# Employee fields that are copies of a verified UAE Employee Document (plan 3.2)
MIRRORED_STANDARD_FIELDS = ("passport_number", "valid_upto", "date_of_issue", "place_of_issue")
MIRROR_NOTE = "Set by verifying a UAE Employee Document. Not typed by hand"


def get_custom_fields():
	def cf(fieldname, fieldtype, label=None, **kw):
		d = dict(fieldname=fieldname, fieldtype=fieldtype, module=MODULE)
		if label:
			d["label"] = label
		d.update(kw)
		return d

	employee = [
		cf("uae_tab", "Tab Break", "UAE", insert_after="old_parent"),
		cf("uae_identity_sb", "Section Break", "Identity"),
		cf("uae_nationality", "Link", "Nationality", options="Country", in_standard_filter=1),
		cf("uae_name_as_passport", "Data", "Name as on Passport"),
		cf(
			"uae_name_arabic",
			"Data",
			"Name in Arabic",
			description="For Arabic certificates and government letters",
		),
		cf("uae_passport_country", "Link", "Passport Issuing Country", options="Country"),
		cf("uae_identity_cb", "Column Break"),
		cf("uae_uid", "Data", "UID Number", description="ICP unified number. Permanent for the person"),
		cf("uae_emirates_id", "Data", "Emirates ID", read_only=1, description=MIRROR_NOTE),
		cf("uae_emirates_id_expiry", "Date", "Emirates ID Expiry", read_only=1, description=MIRROR_NOTE),
		cf("uae_permit_sb", "Section Break", "Work Permit"),
		cf("uae_permit_type", "Link", "Work Permit Type", options="UAE Permit Type", in_standard_filter=1),
		cf("uae_skill_category", "Link", "Skill Category", options="UAE Skill Category"),
		cf(
			"uae_visa_designation",
			"Data",
			"Visa Designation",
			description="MOHRE occupation exactly as on the work permit. The internal job title stays in Designation",
		),
		cf(
			"uae_person_code",
			"Data",
			"MOHRE Person Code",
			length=14,
			description="14 digits, from the work permit. Needed for WPS",
		),
		cf("uae_permit_cb", "Column Break"),
		cf("uae_residency_expiry", "Date", "Residence Visa Expiry", read_only=1, description=MIRROR_NOTE),
		cf("uae_work_permit_expiry", "Date", "Work Permit Expiry", read_only=1, description=MIRROR_NOTE),
		cf("uae_contract_sb", "Section Break", "Contract"),
		cf(
			"uae_probation_months",
			"Int",
			"Probation (months)",
			non_negative=1,
			description="At most 6 months (DL 9(1)), and only once per employer (DL 9(2)). Sets the Final Confirmation Date. "
			"To end it early the employer gives at least 14 days' written notice (DL 9(1))",
		),
		cf(
			"uae_contract_language",
			"Link",
			"Second Contract Language",
			options="Language",
			description="The contract is in Arabic plus a language the worker understands; the Arabic prevails (DL 66)",
		),
		cf("uae_contract_cb", "Column Break"),
		cf(
			"uae_accommodation",
			"Select",
			"Accommodation",
			options="\nProvided\nAllowance in wage",
			description="The employer provides accommodation or pays an allowance for it (DL 13(4))",
		),
		cf(
			"uae_nominee_sb",
			"Section Break",
			"Death Entitlements Nominee",
			collapsible=1,
			description="The worker may name in writing a family member to receive their rights on death (DL 15(2))",
		),
		cf("uae_death_nominee", "Data", "Nominee"),
		cf("uae_nominee_cb", "Column Break"),
		cf(
			"uae_death_nominee_relation",
			"Select",
			"Nominee Relation",
			options="\nSpouse\nSon\nDaughter",
			description="DL 1: the worker's family is the spouse, sons and daughters",
		),
		cf("uae_pay_sb", "Section Break", "Salary Payment (UAE)"),
		cf(
			"uae_bank",
			"Link",
			"Bank",
			options="UAE Bank",
			permlevel=PAY,
			description="Set from the IBAN when it is entered",
		),
		cf(
			"uae_account_name",
			"Data",
			"Account Name",
			permlevel=PAY,
			description="Name exactly as on the bank account",
		),
		cf("uae_pay_cb", "Column Break"),
		cf(
			"uae_salary_card_no",
			"Data",
			"Salary Card Number",
			permlevel=PAY,
			description="For workers paid by card through a WPS agent, with no IBAN",
		),
		cf("uae_salary_agent", "Link", "Salary Card Agent", options="UAE Bank", permlevel=PAY),
		cf("uae_items_sb", "Section Break", "Issued Items"),
		cf(
			"uae_issued_items",
			"Table",
			"Issued Items",
			options="UAE Issued Item",
			description="Company property in the worker's hands. Official documents are never listed here (DL 13(2))",
		),
	]
	prev = None
	for d in employee:
		if prev and "insert_after" not in d:
			d["insert_after"] = prev
		prev = d["fieldname"]

	ssa = [
		cf(
			"uae_pay_sb",
			"Section Break",
			"UAE Pay Components",
			insert_after="company",
			description="Monthly amounts. Salary structures read them in formulas as uae_basic, uae_housing, uae_transport, uae_other",
		),
		cf(
			"uae_basic",
			"Currency",
			"Basic Wage",
			options="currency",
			insert_after="uae_pay_sb",
			description="Gratuity, overtime and end-of-service leave pay use the basic wage (DL 1, DL 51(5))",
		),
		cf("uae_housing", "Currency", "Housing Allowance", options="currency", insert_after="uae_basic"),
		cf("uae_pay_cb", "Column Break", insert_after="uae_housing"),
		cf("uae_transport", "Currency", "Transport Allowance", options="currency", insert_after="uae_pay_cb"),
		cf("uae_other", "Currency", "Other Allowance", options="currency", insert_after="uae_transport"),
		cf("uae_total", "Currency", "Total Wage", options="currency", read_only=1, insert_after="uae_other"),
	]
	education = [
		cf("uae_attested", "Check", "Attested", insert_after="maj_opt_subj", in_list_view=1, columns=1),
		cf("uae_attested_on", "Date", "Attested On", insert_after="uae_attested", depends_on="uae_attested"),
	]
	return {"Employee": employee, "Salary Structure Assignment": ssa, "Employee Education": education}


def get_property_setters():
	out = []
	for field in MIRRORED_STANDARD_FIELDS:
		out.append(("Employee", field, "read_only", "1", "Check"))
		out.append(("Employee", field, "description", MIRROR_NOTE + " (Passport)", "Small Text"))
	return out


def make_custom_fields():
	create_custom_fields(get_custom_fields(), ignore_validate=True)


def make_property_setters():
	import frappe

	for dt, field, prop, value, ptype in get_property_setters():
		name = frappe.db.get_value(
			"Property Setter",
			{"doc_type": dt, "field_name": field, "property": prop},
			["name", "value", "module"],
			as_dict=True,
		)
		if name and name.value == value and name.module == MODULE:
			continue
		if name:
			frappe.db.set_value("Property Setter", name.name, {"value": value, "module": MODULE})
			continue
		ps = frappe.get_doc(
			{
				"doctype": "Property Setter",
				"doctype_or_field": "DocField",
				"doc_type": dt,
				"field_name": field,
				"property": prop,
				"value": value,
				"property_type": ptype,
				"module": MODULE,
			}
		)
		ps.flags.ignore_permissions = True
		ps.insert()
		frappe.clear_cache(doctype=dt)
