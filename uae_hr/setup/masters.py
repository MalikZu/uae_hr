"""Seed data. Inserted only when missing and never overwritten, so a site's own edits survive migrate."""

import frappe

# CR 6(1): the 12 work-permit types, named as in the article. Descriptions only where the article gives one. CR 6(2): the Minister may add more, so this is a master, not a Select.
PERMIT_TYPES = [
	("Work Permit", "CR 6(1)(a)", "Recruiting a worker from outside the State", 0),
	("Transfer Work Permit", "CR 6(1)(b)", "", 0),
	("Family-Sponsored Resident Permit", "CR 6(1)(c)", "Residents sponsored by their families", 0),
	("Temporary Work Permit", "CR 6(1)(d)", "", 0),
	("Mission Permit", "CR 6(1)(e)", "", 0),
	("Part-Time Work Permit", "CR 6(1)(f)", "May work for more than one employer with a Ministry permit", 0),
	(
		"Juvenile Permit",
		"CR 6(1)(g)",
		"A person who has reached 15 years of age but is not over 18 years",
		15,
	),
	(
		"Student Training and Employment Permit",
		"CR 6(1)(h)",
		"A student already in the State, from 15 years of age",
		15,
	),
	("UAE and GCC National Permit", "CR 6(1)(i)", "", 0),
	("Golden Visa Holder Permit", "CR 6(1)(j)", "", 0),
	("National Trainee Permit", "CR 6(1)(k)", "", 0),
	("Freelance Permit", "CR 6(1)(l)", "", 0),
]

# (name, check profile, has expiry, {document field: employee field}, required for every permit type)
DOCUMENT_TYPES = [
	(
		"Passport",
		"Passport",
		1,
		{
			"document_number": "passport_number",
			"expiry_date": "valid_upto",
			"issue_date": "date_of_issue",
			"place_of_issue": "place_of_issue",
		},
		True,
	),
	("Entry Permit", "Entry Permit", 1, {}, False),
	("Residence Visa", "Residence Visa", 1, {"expiry_date": "uae_residency_expiry"}, False),
	(
		"Emirates ID",
		"Emirates ID",
		1,
		{"document_number": "uae_emirates_id", "expiry_date": "uae_emirates_id_expiry"},
		False,
	),
	("Work Permit", "Work Permit", 1, {"expiry_date": "uae_work_permit_expiry"}, True),
	("MOHRE Employment Contract", "", 1, {}, False),
	("Health Insurance", "", 1, {}, False),
	("Degree Certificate", "", 0, {}, False),
	("Visa Cancellation", "", 0, {}, False),
	("Sponsor Visa", "", 1, {}, False),
	("Sponsor Emirates ID", "", 1, {}, False),
	("Marriage Certificate", "", 0, {}, False),
	("NOC", "", 0, {}, False),
	("Driving Licence", "", 1, {}, False),
	("Site Access Pass", "", 1, {}, False),
	("Safety Certificate", "", 1, {}, False),
	("NDA", "", 0, {}, False),
]

ISSUED_ITEM_TYPES = [
	"SIM Card",
	"Laptop",
	"Mobile Phone",
	"PPE",
	"Vehicle",
	"Fuel Card",
	"Access Card",
	"Tools",
]


def seed_masters():
	for name, ref, description, min_age in PERMIT_TYPES:
		_insert(
			"UAE Permit Type",
			name,
			{
				"permit_type_name": name,
				"legal_reference": ref,
				"description": description,
				"min_age": min_age,
			},
		)
	permit_rows = [{"permit_type": p[0]} for p in PERMIT_TYPES]
	for name, profile, has_expiry, mapping, all_permits in DOCUMENT_TYPES:
		_insert(
			"UAE Document Type",
			name,
			{
				"document_type_name": name,
				"check_profile": profile,
				"has_expiry": has_expiry,
				"field_map": [{"document_field": k, "employee_field": v} for k, v in mapping.items()],
				"required_for_permit_types": permit_rows if all_permits else [],
			},
		)
	for name in ISSUED_ITEM_TYPES:
		_insert("UAE Issued Item Type", name, {"item_type_name": name})


def _insert(doctype, name, values):
	if frappe.db.exists(doctype, name):
		return
	doc = frappe.get_doc({"doctype": doctype, **values})
	doc.flags.ignore_permissions = True
	doc.insert()


def seed_settings():
	"""Write the law defaults into the single the first time, and any parameter added by a new version."""
	from uae_hr.law import PARAMS

	missing = {}
	stored = dict(frappe.db.sql("select field, value from tabSingles where doctype = 'UAE HR Settings'"))
	for p in PARAMS:
		if stored.get(p.fieldname) in (None, ""):
			missing[p.fieldname] = p.default
	for field, default in (("default_reminder_days", "60,30,7"), ("copy_hr_manager", 1)):
		if field not in stored:
			missing[field] = default
	if missing:
		for field, value in missing.items():
			frappe.db.set_single_value("UAE HR Settings", field, value)
