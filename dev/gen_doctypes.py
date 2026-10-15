"""Generate the DocType JSON files from compact definitions.

Run from the repo root: python3 dev/gen_doctypes.py

UAE HR Settings is built from uae_hr/law.py, so every legal number is a setting with its citation
and the two cannot drift. A doctype's `modified` stamp only changes when its definition changes,
so rerunning this is safe and `bench migrate` stays a no-op when nothing changed.
"""

import datetime
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "uae_hr" / "uae_hr" / "doctype"
MODULE = "UAE HR"

spec = importlib.util.spec_from_file_location("law", ROOT / "uae_hr" / "law.py")
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)

EMIRATES = "\nAbu Dhabi\nDubai\nSharjah\nAjman\nUmm Al Quwain\nRas Al Khaimah\nFujairah"
CHECK_PROFILES = "\nPassport\nEntry Permit\nResidence Visa\nEmirates ID\nWork Permit"
DOC_FIELDS = "\n".join(
	[
		"document_number",
		"issue_date",
		"expiry_date",
		"issuing_country",
		"issuing_emirate",
		"place_of_issue",
		"name_on_document",
		"designation_on_document",
		"sponsor_name",
		"date_of_birth",
	]
)


def f(fieldname, fieldtype, label=None, **kw):
	d = {"fieldname": fieldname, "fieldtype": fieldtype}
	if label:
		d["label"] = label
	d.update(kw)
	return d


def perm(role, submit=0, delete=1, create=1, write=1):
	p = {
		"role": role,
		"read": 1,
		"write": write,
		"create": create,
		"delete": delete,
		"email": 1,
		"print": 1,
		"export": 1,
		"report": 1,
		"share": 1,
	}
	if submit:
		p.update(submit=1, cancel=1, amend=1)
	return p


def read_perm(role):
	return {"role": role, "read": 1, "print": 1, "report": 1, "export": 1}


def master_perms(pro_write=False):
	perms = [perm("System Manager"), perm("HR Manager"), read_perm("HR User")]
	perms.append(perm("UAE PRO", delete=0) if pro_write else read_perm("UAE PRO"))
	return perms


def dt(name, fields, **kw):
	d = {
		"doctype": "DocType",
		"name": name,
		"module": MODULE,
		"custom": 0,
		"engine": "InnoDB",
		"owner": "Administrator",
		"fields": fields,
		"field_order": [x["fieldname"] for x in fields],
		"sort_field": "modified",
		"sort_order": "DESC",
		"track_changes": 1,
		"row_format": "Dynamic",
		"permissions": kw.pop("permissions", []),
		"states": [],
	}
	if kw.get("istable"):
		d.update(editable_grid=1, track_changes=0)
	d.update(kw)
	return d


def write(doc):
	folder = BASE / doc["name"].lower().replace(" ", "_")
	folder.mkdir(parents=True, exist_ok=True)
	(folder / "__init__.py").touch()
	path = folder / (folder.name + ".json")
	old = json.loads(path.read_text()) if path.exists() else {}
	stamp = {k: old.get(k) for k in ("creation", "modified", "modified_by")}
	comparable_old = {k: v for k, v in old.items() if k not in stamp}
	if comparable_old != doc:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		stamp = {"creation": old.get("creation") or now, "modified": now, "modified_by": "Administrator"}
	path.write_text(json.dumps({**doc, **stamp}, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
	ctrl = folder / (folder.name + ".py")
	if not ctrl.exists():
		cls = doc["name"].replace(" ", "")
		ctrl.write_text(
			"# Copyright (c) 2026, UAE HR contributors\n# License: GNU General Public License v3. See LICENSE\n\n"
			f"from frappe.model.document import Document\n\n\nclass {cls}(Document):\n\tpass\n"
		)


# ---------------------------------------------------------------- masters
write(
	dt(
		"UAE Permit Type",
		[
			f("permit_type_name", "Data", "Permit Type", reqd=1, unique=1, in_list_view=1),
			f(
				"legal_reference",
				"Data",
				"Legal Reference",
				in_list_view=1,
				description="Article that creates this permit type, e.g. CR 6(1)(a)",
			),
			f("enabled", "Check", "Enabled", default="1"),
			f("cb1", "Column Break"),
			f(
				"min_age",
				"Int",
				"Minimum Age",
				description="Leave 0 when the general minimum applies (CR 7(1): 18)",
			),
			f("max_age", "Int", "Maximum Age", description="0 = no maximum"),
			f("sb1", "Section Break"),
			f("description", "Small Text", "Description"),
		],
		autoname="field:permit_type_name",
		title_field="permit_type_name",
		search_fields="legal_reference",
		permissions=master_perms(),
		naming_rule="By fieldname",
	)
)

write(
	dt(
		"UAE Skill Category",
		[
			f("category_name", "Data", "Skill Category", reqd=1, unique=1, in_list_view=1),
			f("enabled", "Check", "Enabled", default="1"),
			f(
				"description",
				"Small Text",
				"Description",
				description="CR 3 classifies workers by skill, qualification, productivity and salary level, but names no levels: "
				"they are set by a separate Cabinet resolution. Record the categories your establishment uses.",
			),
		],
		autoname="field:category_name",
		permissions=master_perms(),
		naming_rule="By fieldname",
	)
)

write(
	dt(
		"UAE Bank",
		[
			f("bank_name", "Data", "Bank Name", reqd=1, unique=1, in_list_view=1),
			f("short_name", "Data", "Short Name", in_list_view=1),
			f("enabled", "Check", "Enabled", default="1"),
			f("cb1", "Column Break"),
			f(
				"bank_code",
				"Data",
				"IBAN Bank Code",
				length=3,
				unique=1,
				in_list_view=1,
				description="The 3 digits after AE and the check digits in a UAE IBAN (AEkk BBB ...)",
			),
			f("swift_code", "Data", "SWIFT / BIC", length=11),
			f(
				"wps_routing_code",
				"Data",
				"WPS Routing Code",
				length=9,
				description="9-digit routing code used in WPS salary files. Take it from your WPS agent bank",
			),
			f("sb1", "Section Break"),
			f("notes", "Small Text", "Notes"),
		],
		autoname="field:bank_name",
		search_fields="short_name,bank_code",
		permissions=master_perms(),
		naming_rule="By fieldname",
	)
)

write(
	dt(
		"UAE Issued Item Type",
		[
			f("item_type_name", "Data", "Item Type", reqd=1, unique=1, in_list_view=1),
			f("enabled", "Check", "Enabled", default="1"),
			f("description", "Small Text", "Description"),
		],
		autoname="field:item_type_name",
		permissions=master_perms(),
		naming_rule="By fieldname",
	)
)

write(
	dt(
		"UAE Issued Item",
		[
			f(
				"item_type",
				"Link",
				"Item Type",
				options="UAE Issued Item Type",
				reqd=1,
				in_list_view=1,
				columns=2,
			),
			f("description", "Data", "Description", in_list_view=1, columns=2),
			f("serial_no", "Data", "Serial / Asset No", in_list_view=1, columns=2),
			f("mobile_number", "Data", "Mobile Number", options="Phone", description="For SIM cards"),
			f("cb1", "Column Break"),
			f("issued_on", "Date", "Issued On", in_list_view=1, columns=2),
			f("returned_on", "Date", "Returned On", in_list_view=1, columns=2),
			f("undertaking", "Attach", "Signed Undertaking"),
		],
		istable=1,
	)
)

write(
	dt(
		"UAE Document Field Map",
		[
			f(
				"document_field",
				"Select",
				"Document Field",
				options=DOC_FIELDS,
				reqd=1,
				in_list_view=1,
				columns=4,
			),
			f(
				"employee_field",
				"Data",
				"Employee Field",
				reqd=1,
				in_list_view=1,
				columns=4,
				description="Fieldname on Employee that mirrors this value when the document is verified",
			),
		],
		istable=1,
	)
)

write(
	dt(
		"UAE Document Type Permit",
		[
			f("permit_type", "Link", "Permit Type", options="UAE Permit Type", reqd=1, in_list_view=1),
		],
		istable=1,
	)
)

write(
	dt(
		"UAE Document Type",
		[
			f("document_type_name", "Data", "Document Type", reqd=1, unique=1, in_list_view=1),
			f("enabled", "Check", "Enabled", default="1"),
			f(
				"check_profile",
				"Select",
				"Checks",
				options=CHECK_PROFILES,
				description="Which built-in checks run for this type (Emirates ID format, passport number on a visa, ...)",
			),
			f("cb1", "Column Break"),
			f("has_expiry", "Check", "Has Expiry Date", default="1"),
			f(
				"reminder_days",
				"Data",
				"Reminder Days",
				depends_on="has_expiry",
				description="Days before expiry to remind the PRO, comma separated, e.g. 60,30,7. Empty = the default in UAE HR Settings",
			),
			f("sb1", "Section Break", "Mirror to Employee"),
			f(
				"field_map",
				"Table",
				"Field Map",
				options="UAE Document Field Map",
				description="When a document of this type is verified, these Employee fields are set from it. Mirrored fields are never typed by hand",
			),
			f("sb2", "Section Break", "Required For"),
			f(
				"required_for_permit_types",
				"Table MultiSelect",
				"Required for Permit Types",
				options="UAE Document Type Permit",
				description="Listed as missing on the contract readiness check for employees on these permit types",
			),
			f("description", "Small Text", "Description"),
		],
		autoname="field:document_type_name",
		permissions=master_perms(pro_write=True),
		naming_rule="By fieldname",
	)
)

# ---------------------------------------------------------------- employee document
write(
	dt(
		"UAE Employee Document",
		[
			f(
				"employee",
				"Link",
				"Employee",
				options="Employee",
				in_list_view=1,
				in_standard_filter=1,
				search_index=1,
			),
			f(
				"employee_name",
				"Data",
				"Employee Name",
				fetch_from="employee.employee_name",
				read_only=1,
				in_list_view=1,
			),
			f(
				"company",
				"Link",
				"Company",
				options="Company",
				fetch_from="employee.company",
				read_only=1,
				in_standard_filter=1,
			),
			f(
				"job_applicant",
				"Link",
				"Job Applicant",
				options="Job Applicant",
				description="For documents collected before the Employee record exists",
			),
			f("cb1", "Column Break"),
			f(
				"document_type",
				"Link",
				"Document Type",
				options="UAE Document Type",
				reqd=1,
				in_list_view=1,
				in_standard_filter=1,
			),
			f(
				"status",
				"Select",
				"Status",
				options="Unverified\nCurrent\nSuperseded\nExpired\nCancelled",
				default="Unverified",
				read_only=1,
				in_list_view=1,
				in_standard_filter=1,
				no_copy=1,
			),
			f(
				"check_profile",
				"Data",
				"Checks",
				fetch_from="document_type.check_profile",
				read_only=1,
				hidden=1,
			),
			f(
				"has_expiry",
				"Check",
				"Has Expiry Date",
				fetch_from="document_type.has_expiry",
				read_only=1,
				hidden=1,
			),
			f(
				"reminder_days",
				"Data",
				"Reminder Days",
				read_only=1,
				hidden=1,
				no_copy=1,
				description="Copied from the document type (or the settings default); drives the expiry notifications",
			),
			f("details_sb", "Section Break", "Details"),
			f("document_number", "Data", "Document Number", in_list_view=1, search_index=1),
			f("issue_date", "Date", "Issue Date"),
			f(
				"expiry_date",
				"Date",
				"Expiry Date",
				in_list_view=1,
				search_index=1,
				mandatory_depends_on="eval:doc.has_expiry",
			),
			f("cb2", "Column Break"),
			f("issuing_country", "Link", "Issuing Country", options="Country"),
			f("issuing_emirate", "Select", "Issuing Emirate", options=EMIRATES),
			f("place_of_issue", "Data", "Place of Issue"),
			f("holder_sb", "Section Break", "As Printed on the Document"),
			f("name_on_document", "Data", "Name on Document"),
			f("date_of_birth", "Date", "Date of Birth"),
			f(
				"passport_number",
				"Data",
				"Passport Number on Document",
				depends_on="eval:['Entry Permit','Residence Visa'].includes(doc.check_profile)",
				description="Checked against the employee's current passport",
			),
			f("cb3", "Column Break"),
			f(
				"designation_on_document",
				"Data",
				"Designation on Document",
				description="Occupation as printed; must match across work permit, residence visa and Emirates ID",
			),
			f(
				"sponsor_name",
				"Data",
				"Sponsor Name",
				description="For relative permits: the sponsoring family member",
			),
			f("file_sb", "Section Break", "Scan"),
			f(
				"file",
				"Attach",
				"Scan (private)",
				description="Always stored as a private file. The original stays with the worker: DL 13(2) forbids withholding official documents",
			),
			f("verify_sb", "Section Break", "Verification"),
			f("verified_by", "Link", "Verified By", options="User", read_only=1, no_copy=1),
			f("verified_on", "Datetime", "Verified On", read_only=1, no_copy=1),
			f("cb4", "Column Break"),
			f(
				"superseded_by",
				"Link",
				"Superseded By",
				options="UAE Employee Document",
				read_only=1,
				no_copy=1,
			),
			f("notes", "Small Text", "Notes"),
		],
		autoname="UAE-DOC-.YYYY.-.#####",
		title_field="employee_name",
		search_fields="employee_name,document_type,document_number",
		show_title_field_in_link=0,
		naming_rule="Expression (old style)",
		permissions=[
			perm("System Manager"),
			perm("HR Manager"),
			perm("HR User", delete=0),
			perm("UAE PRO", delete=0),
		],
	)
)

# ---------------------------------------------------------------- HR letter
LETTER_TYPES = "Salary Certificate\nSalary Transfer Letter\nSalary Revision\nEmployment Certificate\nExperience Certificate\nWarning\nNOC\nOther"
write(
	dt(
		"UAE HR Letter",
		[
			f(
				"naming_series",
				"Select",
				"Reference Series",
				options="UAE-LTR-.YYYY.-",
				default="UAE-LTR-.YYYY.-",
				reqd=1,
				no_copy=1,
			),
			f(
				"employee",
				"Link",
				"Employee",
				options="Employee",
				reqd=1,
				in_list_view=1,
				in_standard_filter=1,
				search_index=1,
			),
			f(
				"employee_name",
				"Data",
				"Employee Name",
				fetch_from="employee.employee_name",
				read_only=1,
				in_list_view=1,
			),
			f("company", "Link", "Company", options="Company", fetch_from="employee.company", read_only=1),
			f("cb1", "Column Break"),
			f(
				"letter_type",
				"Select",
				"Letter Type",
				options=LETTER_TYPES,
				reqd=1,
				in_list_view=1,
				in_standard_filter=1,
			),
			f("issue_date", "Date", "Issue Date", default="Today", reqd=1, in_list_view=1),
			f(
				"addressed_to",
				"Data",
				"Addressed To",
				description="e.g. To whom it may concern, a bank, an embassy",
			),
			f("issued_by", "Link", "Issued By", options="User", default="__user"),
			f(
				"experience_sb",
				"Section Break",
				"Experience Certificate (DL 13(11))",
				depends_on="eval:doc.letter_type=='Experience Certificate'",
			),
			f(
				"service_start_date",
				"Date",
				"Start of Service",
				mandatory_depends_on="eval:doc.letter_type=='Experience Certificate'",
			),
			f(
				"service_end_date",
				"Date",
				"End of Service",
				mandatory_depends_on="eval:doc.letter_type=='Experience Certificate'",
			),
			f("total_service", "Data", "Total Service", read_only=1),
			f("cb2", "Column Break"),
			f(
				"job_title",
				"Data",
				"Job Title",
				mandatory_depends_on="eval:doc.letter_type=='Experience Certificate'",
			),
			f(
				"last_wage",
				"Currency",
				"Last Wage",
				options="currency",
				mandatory_depends_on="eval:doc.letter_type=='Experience Certificate'",
			),
			f("currency", "Link", "Currency", options="Currency", default="AED"),
			f(
				"termination_reason",
				"Small Text",
				"Reason for End of Service",
				mandatory_depends_on="eval:doc.letter_type=='Experience Certificate'",
				description="DL 13(11): the certificate is free and must not contain anything harmful to the worker",
			),
			f(
				"warning_sb",
				"Section Break",
				"Disciplinary Warning (CR 24)",
				depends_on="eval:doc.letter_type=='Warning'",
			),
			f("violation", "Small Text", "Violation", mandatory_depends_on="eval:doc.letter_type=='Warning'"),
			f(
				"violation_detected_on",
				"Date",
				"Violation Detected On",
				mandatory_depends_on="eval:doc.letter_type=='Warning'",
			),
			f("cb3", "Column Break"),
			f(
				"charged_on",
				"Date",
				"Written Charge Given On",
				mandatory_depends_on="eval:doc.letter_type=='Warning'",
				description="CR 24(3): the worker is told the charge in writing and heard before any penalty",
			),
			f(
				"investigation_closed_on",
				"Date",
				"Investigation Closed On",
				mandatory_depends_on="eval:doc.letter_type=='Warning'",
			),
			f("other_sb", "Section Break"),
			f("remarks", "Small Text", "Remarks"),
			f("signed_copy", "Attach", "Signed Copy", allow_on_submit=1),
			f(
				"amended_from",
				"Link",
				"Amended From",
				options="UAE HR Letter",
				read_only=1,
				no_copy=1,
				print_hide=1,
			),
		],
		is_submittable=1,
		autoname="naming_series:",
		title_field="employee_name",
		search_fields="employee_name,letter_type",
		naming_rule='By "Naming Series" field',
		permissions=[
			perm("System Manager", submit=1),
			perm("HR Manager", submit=1),
			perm("HR User", delete=0),
		],
	)
)

# ---------------------------------------------------------------- settings
write(
	dt(
		"UAE Company Setup",
		[
			f("company", "Link", "Company", options="Company", reqd=1, in_list_view=1, columns=3),
			f(
				"jurisdiction",
				"Select",
				"Jurisdiction",
				reqd=1,
				in_list_view=1,
				columns=3,
				options="Mainland (MOHRE)\nFree zone under the federal law\nDIFC (not covered)\nADGM (not covered)",
				default="Mainland (MOHRE)",
				description="DIFC and ADGM have their own employment laws: the app's checks are switched off for those companies",
			),
			f("emirate", "Select", "Emirate", options=EMIRATES, in_list_view=1, columns=2),
			f("mohre_establishment_id", "Data", "MOHRE Establishment ID", in_list_view=1, columns=2),
			f("cb1", "Column Break"),
			f("wps_agent", "Link", "WPS Agent Bank", options="UAE Bank"),
			f(
				"wps_routing_code",
				"Data",
				"WPS Agent Routing Code",
				fetch_from="wps_agent.wps_routing_code",
				read_only=1,
			),
			f(
				"health_insurance_regulator",
				"Data",
				"Health Insurance Regulator",
				description="Set per emirate, e.g. the emirate's health authority",
			),
			f("pension_fund", "Data", "Pension Fund for UAE Nationals"),
		],
		istable=1,
	)
)

NOTICE = (
	"<div class='alert alert-warning'><b>Not legal advice.</b> UAE HR encodes Federal Decree-Law No. 33 of 2021 and "
	"Cabinet Resolution No. 1 of 2022 as published in English by MOHRE. The Arabic text prevails (DL 66), and the "
	"Cabinet may change any period, percentage or value (DL 70(7)). Check anything that matters with a qualified "
	"adviser. Every value below defaults to the law; you may make it more generous to workers.</div>"
)
settings_fields = [
	f("notice_html", "HTML", options=NOTICE),
	f("companies_sb", "Section Break", "Companies"),
	f(
		"companies",
		"Table",
		"Companies",
		options="UAE Company Setup",
		description="A company not listed here is treated as mainland if its country is United Arab Emirates, and is ignored otherwise",
	),
	f("reminders_sb", "Section Break", "Expiry Reminders"),
	f(
		"default_reminder_days",
		"Data",
		"Default Reminder Days",
		default="60,30,7",
		description="Used for document types with no reminder days of their own",
	),
	f("cb_rem", "Column Break"),
	f(
		"copy_hr_manager",
		"Check",
		"Copy HR Manager",
		default="1",
		description="Reminders go to role UAE PRO; tick to also send them to HR Manager",
	),
	f("law_sb", "Section Break", "Law Parameters"),
	f(
		"amendment_reference",
		"Small Text",
		"Amendment Reference",
		description="Required when a value below is less favourable to workers than the 2022 text, or when a value without a "
		"direction changes: name the resolution that changed it (DL 70(7))",
	),
]
for key, title in law.SECTIONS.items():
	params = [p for p in law.PARAMS if p.section == key]
	settings_fields.append(f(f"law_{key}_sb", "Section Break", title, collapsible=1))
	half = (len(params) + 1) // 2
	for i, p in enumerate(params):
		if i == half:
			settings_fields.append(f(f"law_{key}_cb", "Column Break"))
		settings_fields.append(
			f(
				p.fieldname,
				p.fieldtype,
				p.label,
				default=str(p.default),
				non_negative=1,
				description=law.describe(p)
				+ ("" if p.enforced_in == "0.1" else f" (used from v{p.enforced_in})"),
			)
		)

write(
	dt(
		"UAE HR Settings",
		settings_fields,
		issingle=1,
		permissions=[
			{
				"role": "System Manager",
				"read": 1,
				"write": 1,
				"create": 1,
				"print": 1,
				"email": 1,
				"share": 1,
			},
			{"role": "HR Manager", "read": 1, "write": 1, "create": 1, "print": 1, "email": 1, "share": 1},
			{"role": "HR User", "read": 1},
		],
	)
)

print("doctypes written to", BASE)
