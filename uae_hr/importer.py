"""Excel import for HR teams starting from spreadsheets (plan 3.10).

    bench --site <site> execute uae_hr.importer.make_template --args "['/path/uae_hr_import.xlsx']"
    bench --site <site> execute uae_hr.importer.check --args "['/path/uae_hr_import.xlsx']"
    bench --site <site> execute uae_hr.importer.split --args "['/path/uae_hr_import.xlsx', '/path/out']"

`check` runs every legal and consistency check on the workbook without writing anything and returns
the list of problems (and prints it). `split` writes one file per sheet in the layout Frappe's
standard Data Import expects; import them in the order Employees, Documents, Issued Items, Salary.
Documents arrive Unverified: verify them from the list view (select, Actions > Verify).
"""

import datetime

import frappe
from frappe import _
from frappe.utils import getdate

from uae_hr import checks
from uae_hr.law import get_param

SHEETS = {
	"Employees": {
		"doctype": "Employee",
		"key": "name",
		"columns": [
			("name", "ID"),
			("employee_name", "Full Name (reference only)"),
			("date_of_birth", "Date of Birth"),
			("uae_nationality", "Nationality"),
			("uae_name_as_passport", "Name as on Passport"),
			("uae_name_arabic", "Name in Arabic"),
			("uae_passport_country", "Passport Issuing Country"),
			("uae_uid", "UID Number"),
			("uae_permit_type", "Work Permit Type"),
			("uae_skill_category", "Skill Category"),
			("uae_visa_designation", "Visa Designation"),
			("uae_person_code", "MOHRE Person Code"),
			("uae_probation_months", "Probation (months)"),
			("notice_number_of_days", "Notice (days)"),
			("uae_contract_language", "Second Contract Language"),
			("uae_accommodation", "Accommodation"),
			("uae_death_nominee", "Nominee"),
			("uae_death_nominee_relation", "Nominee Relation"),
			("salary_mode", "Salary Mode"),
			("iban", "IBAN"),
			("uae_bank", "Bank"),
			("uae_account_name", "Account Name"),
			("uae_salary_card_no", "Salary Card Number"),
			("uae_salary_agent", "Salary Card Agent"),
		],
	},
	"Documents": {
		"doctype": "UAE Employee Document",
		"columns": [
			("employee", "Employee"),
			("document_type", "Document Type"),
			("document_number", "Document Number"),
			("issue_date", "Issue Date"),
			("expiry_date", "Expiry Date"),
			("issuing_country", "Issuing Country"),
			("issuing_emirate", "Issuing Emirate"),
			("place_of_issue", "Place of Issue"),
			("name_on_document", "Name on Document"),
			("date_of_birth", "Date of Birth"),
			("passport_number", "Passport Number on Document"),
			("designation_on_document", "Designation on Document"),
			("sponsor_name", "Sponsor Name"),
			("notes", "Notes"),
		],
	},
	"Issued Items": {
		"doctype": "Employee",
		"child": "uae_issued_items",
		"columns": [
			("name", "ID"),
			("item_type", "Item Type (Issued Items)"),
			("description", "Description (Issued Items)"),
			("serial_no", "Serial / Asset No (Issued Items)"),
			("mobile_number", "Mobile Number (Issued Items)"),
			("issued_on", "Issued On (Issued Items)"),
			("returned_on", "Returned On (Issued Items)"),
		],
	},
	"Salary": {
		"doctype": "Salary Structure Assignment",
		"columns": [
			("employee", "Employee"),
			("salary_structure", "Salary Structure"),
			("from_date", "From Date"),
			("company", "Company"),
			("currency", "Currency"),
			("uae_basic", "Basic Wage"),
			("uae_housing", "Housing Allowance"),
			("uae_transport", "Transport Allowance"),
			("uae_other", "Other Allowance"),
		],
	},
}

LINKS = {
	"uae_nationality": "Country",
	"uae_passport_country": "Country",
	"issuing_country": "Country",
	"uae_permit_type": "UAE Permit Type",
	"uae_skill_category": "UAE Skill Category",
	"uae_bank": "UAE Bank",
	"uae_salary_agent": "UAE Bank",
	"uae_contract_language": "Language",
	"document_type": "UAE Document Type",
	"item_type": "UAE Issued Item Type",
	"salary_structure": "Salary Structure",
	"company": "Company",
	"currency": "Currency",
}
DATES = {"date_of_birth", "issue_date", "expiry_date", "issued_on", "returned_on", "from_date"}

README = [
	"UAE HR import workbook",
	"",
	"Fill one row per record. Row 1 holds the field labels Frappe's Data Import reads; do not rename them.",
	"Employees: one row per existing employee, ID = the Employee ID in the ERP. Empty cells are left unchanged.",
	"Documents: one row per document (passport, Emirates ID, visa, work permit ...). They import as Unverified.",
	"Issued Items: one row per item; repeat the ID for several items of the same employee.",
	"Salary: one row per employee with the monthly basic and allowances.",
	"Dates as YYYY-MM-DD. Run the checker before importing:",
	"  bench --site <site> execute uae_hr.importer.check --args \"['<this file>']\"",
	"Not legal advice: the checks follow the published law text; see docs/law.md.",
]


def make_template(path):
	from openpyxl import Workbook
	from openpyxl.styles import Font

	wb = Workbook()
	ws = wb.active
	ws.title = "README"
	for line in README:
		ws.append([line])
	for sheet, spec in SHEETS.items():
		ws = wb.create_sheet(sheet)
		ws.append([label for _f, label in spec["columns"]])
		for cell in ws[1]:
			cell.font = Font(bold=True)
		for i, _c in enumerate(spec["columns"], start=1):
			ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = 22
	wb.save(path)
	return path


def read(path):
	"""{sheet: [ {fieldname: value, '_row': n} ]}, matching headers by label or fieldname."""
	from openpyxl import load_workbook

	wb = load_workbook(path, data_only=True)
	out = {}
	for sheet, spec in SHEETS.items():
		if sheet not in wb.sheetnames:
			out[sheet] = []
			continue
		ws = wb[sheet]
		header = [str(c.value).strip() if c.value is not None else "" for c in ws[1]]
		by_label = {label: f for f, label in spec["columns"]} | {f: f for f, _l in spec["columns"]}
		fields = [by_label.get(h) for h in header]
		rows = []
		for n, values in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
			if not any(v not in (None, "") for v in values):
				continue
			row = {"_row": n}
			for field, value in zip(fields, values, strict=False):
				if field:
					row[field] = value.strip() if isinstance(value, str) else value
			rows.append(row)
		out[sheet] = rows
	return out


class Report:
	def __init__(self):
		self.items = []

	def add(self, sheet, row, level, message, field=None):
		self.items.append(
			{"sheet": sheet, "row": row, "field": field or "", "level": level, "message": message}
		)

	def findings(self, sheet, row, findings, field=None):
		for f in findings:
			self.add(sheet, row, "error" if f.level == checks.BLOCK else "warning", f.text(), field)


def _date(value):
	if value in (None, ""):
		return None
	if isinstance(value, datetime.datetime):
		return value.date()
	if isinstance(value, datetime.date):
		return value
	try:
		return getdate(value)
	except Exception:
		return "invalid"


def check(path, write_report=True):
	data = read(path)
	rep = Report()
	employees = {r.get("name"): r for r in data["Employees"] if r.get("name")}
	_check_common(data, rep)
	_check_employees(data["Employees"], rep)
	_check_documents(data["Documents"], employees, rep)
	_check_items(data["Issued Items"], rep)
	_check_salary(data["Salary"], rep)
	errors = sum(1 for i in rep.items if i["level"] == "error")
	result = {"errors": errors, "warnings": len(rep.items) - errors, "items": rep.items}
	for i in rep.items:
		print(f"{i['level'].upper():8} {i['sheet']} row {i['row']} {i['field']}: {i['message']}")
	print(_("{0} errors, {1} warnings").format(result["errors"], result["warnings"]))
	if write_report and rep.items:
		result["report"] = _write_report(path, rep.items)
	return result


def _check_common(data, rep):
	for sheet, rows in data.items():
		for r in rows:
			for field, value in r.items():
				if field == "_row" or value in (None, ""):
					continue
				if field in DATES and _date(value) == "invalid":
					rep.add(
						sheet,
						r["_row"],
						"error",
						_("{0} is not a date (use YYYY-MM-DD)").format(value),
						field,
					)
				doctype = LINKS.get(field)
				if doctype and not frappe.db.exists(doctype, value):
					rep.add(
						sheet,
						r["_row"],
						"error",
						_("{0} {1} does not exist").format(_(doctype), value),
						field,
					)
			emp_field = "name" if sheet in ("Employees", "Issued Items") else "employee"
			emp = r.get(emp_field)
			if not emp:
				rep.add(sheet, r["_row"], "error", _("Employee ID is missing"), emp_field)
			elif not frappe.db.exists("Employee", emp):
				rep.add(sheet, r["_row"], "error", _("Employee {0} does not exist").format(emp), emp_field)


def _check_employees(rows, rep):
	max_months = get_param("probation_max_months")
	for r in rows:
		n = r["_row"]
		company = frappe.db.get_value("Employee", r.get("name"), "company") if r.get("name") else None
		joining = frappe.db.get_value("Employee", r.get("name"), "date_of_joining") if r.get("name") else None
		rep.findings(
			"Employees",
			n,
			checks.check_probation(_int(r.get("uae_probation_months")), max_months, joining),
			"uae_probation_months",
		)
		rep.findings(
			"Employees",
			n,
			checks.check_notice(
				_int(r.get("notice_number_of_days")),
				get_param("notice_min_days"),
				get_param("notice_max_days"),
			),
			"notice_number_of_days",
		)
		rep.findings("Employees", n, checks.check_iban(r.get("iban")), "iban")
		parts = checks.uae_iban_parts(r.get("iban") or "")
		if parts and r.get("uae_bank"):
			bank = frappe.db.get_value("UAE Bank", {"bank_code": parts[0]}, "name")
			if bank and bank != r["uae_bank"]:
				rep.add(
					"Employees",
					n,
					"warning",
					_("The IBAN belongs to {0}, not {1}").format(bank, r["uae_bank"]),
					"uae_bank",
				)
		rep.findings(
			"Employees", n, checks.check_person_code(_str(r.get("uae_person_code"))), "uae_person_code"
		)
		if not r.get("uae_person_code"):
			rep.add(
				"Employees",
				n,
				"warning",
				_("MOHRE person code is empty; WPS payroll needs it"),
				"uae_person_code",
			)
		rep.findings(
			"Employees",
			n,
			checks.check_nominee(r.get("uae_death_nominee"), r.get("uae_death_nominee_relation")),
			"uae_death_nominee_relation",
		)
		if r.get("uae_accommodation") and r["uae_accommodation"] not in ("Provided", "Allowance in wage"):
			rep.add(
				"Employees",
				n,
				"error",
				_("Accommodation is Provided or Allowance in wage"),
				"uae_accommodation",
			)
		if company and r.get("salary_mode") == "Bank" and not r.get("iban"):
			rep.add("Employees", n, "warning", _("Salary mode is Bank but there is no IBAN"), "iban")


def _check_documents(rows, employees, rep):
	seen = {}
	by_emp = {}
	for r in rows:
		by_emp.setdefault(r.get("employee"), []).append(r)
	for r in rows:
		n = r["_row"]
		dtype = r.get("document_type")
		if not dtype or not frappe.db.exists("UAE Document Type", dtype):
			continue
		profile, has_expiry = frappe.db.get_value("UAE Document Type", dtype, ["check_profile", "has_expiry"])
		issue, expiry = _date(r.get("issue_date")), _date(r.get("expiry_date"))
		if has_expiry and not expiry:
			rep.add("Documents", n, "error", _("{0} needs an expiry date").format(dtype), "expiry_date")
		if issue not in (None, "invalid") and expiry not in (None, "invalid") and expiry <= issue:
			rep.add("Documents", n, "error", _("The expiry date must be after the issue date"), "expiry_date")
		if expiry not in (None, "invalid") and expiry < getdate():
			rep.add("Documents", n, "warning", _("Already expired on {0}").format(expiry), "expiry_date")
		key = (r.get("employee"), dtype, _str(r.get("document_number")))
		if key[2] and key in seen:
			rep.add(
				"Documents", n, "error", _("Same document as row {0}").format(seen[key]), "document_number"
			)
		seen[key] = n
		emp_dob = _date((employees.get(r.get("employee")) or {}).get("date_of_birth")) or (
			frappe.db.get_value("Employee", r.get("employee"), "date_of_birth") if r.get("employee") else None
		)
		doc_dob = _date(r.get("date_of_birth"))
		if profile == "Emirates ID":
			rep.findings(
				"Documents",
				n,
				checks.check_emirates_id(_str(r.get("document_number")), doc_dob or emp_dob),
				"document_number",
			)
		if (
			doc_dob not in (None, "invalid")
			and emp_dob not in (None, "invalid")
			and getdate(doc_dob) != getdate(emp_dob)
		):
			rep.add(
				"Documents",
				n,
				"warning",
				_("Date of birth {0} differs from the employee's {1}").format(doc_dob, emp_dob),
				"date_of_birth",
			)
		siblings = by_emp.get(r.get("employee"), [])
		if profile in ("Entry Permit", "Residence Visa") and r.get("passport_number"):
			passports = {
				_str(s.get("document_number")).upper()
				for s in siblings
				if _profile(s.get("document_type")) == "Passport" and s.get("document_number")
			}
			if passports and _str(r["passport_number"]).upper() not in passports:
				rep.add(
					"Documents",
					n,
					"warning",
					_("Passport {0} on the visa is not the passport in this workbook ({1})").format(
						r["passport_number"], ", ".join(sorted(passports))
					),
					"passport_number",
				)
		if profile in ("Work Permit", "Residence Visa", "Emirates ID") and r.get("designation_on_document"):
			others = {
				_str(s.get("designation_on_document")).lower()
				for s in siblings
				if s is not r
				and _profile(s.get("document_type")) in ("Work Permit", "Residence Visa", "Emirates ID")
				and s.get("designation_on_document")
			}
			if others and _str(r["designation_on_document"]).lower() not in others:
				rep.add(
					"Documents",
					n,
					"warning",
					_("Designation differs from the employee's other permit documents"),
					"designation_on_document",
				)


def _check_items(rows, rep):
	for r in rows:
		if r.get("item_type"):
			rep.findings(
				"Issued Items", r["_row"], checks.check_issued_item_type(r["item_type"]), "item_type"
			)


def _check_salary(rows, rep):
	for r in rows:
		parts = [_float(r.get(f)) for f in ("uae_basic", "uae_housing", "uae_transport", "uae_other")]
		rep.findings("Salary", r["_row"], checks.check_pay_split(*parts), "uae_basic")
		if not parts[0]:
			rep.add("Salary", r["_row"], "error", _("Basic wage is empty"), "uae_basic")


def split(path, out_dir):
	"""One workbook per sheet, headed with the labels Data Import maps to fields."""
	import os

	from openpyxl import Workbook

	data = read(path)
	os.makedirs(out_dir, exist_ok=True)
	written = []
	for sheet, spec in SHEETS.items():
		rows = data.get(sheet) or []
		if not rows:
			continue
		cols = [
			(f, label)
			for f, label in spec["columns"]
			if any(r.get(f) not in (None, "") for r in rows) or f in ("name", "employee")
		]
		if sheet == "Employees":
			cols = [c for c in cols if c[0] != "employee_name"]
		wb = Workbook()
		ws = wb.active
		ws.append([label for _f, label in cols])
		for r in rows:
			ws.append([r.get(f) for f, _l in cols])
		target = os.path.join(out_dir, f"{sheet.lower().replace(' ', '_')}.xlsx")
		wb.save(target)
		written.append(
			{
				"sheet": sheet,
				"doctype": spec["doctype"],
				"file": target,
				"import_type": "Update Existing Records"
				if spec["doctype"] == "Employee"
				else "Insert New Records",
			}
		)
	return written


def _write_report(path, items):
	from openpyxl import Workbook

	wb = Workbook()
	ws = wb.active
	ws.title = "Check"
	ws.append(["Level", "Sheet", "Row", "Field", "Message"])
	for i in items:
		ws.append([i["level"], i["sheet"], i["row"], i["field"], i["message"]])
	target = path.rsplit(".", 1)[0] + "-check.xlsx"
	wb.save(target)
	return target


def _profile(dtype):
	return (
		frappe.get_cached_value("UAE Document Type", dtype, "check_profile")
		if dtype and frappe.db.exists("UAE Document Type", dtype)
		else None
	)


def _int(v):
	try:
		return int(v) if v not in (None, "") else None
	except TypeError, ValueError:
		return None


def _float(v):
	try:
		return float(v) if v not in (None, "") else 0.0
	except TypeError, ValueError:
		return 0.0


def _str(v):
	if v is None:
		return ""
	if isinstance(v, float) and v.is_integer():
		v = int(v)
	return str(v).strip()
