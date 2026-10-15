"""Invented test data only. Nothing here comes from a real company or person."""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, now_datetime, today

MAINLAND = "UAE HR Test Mainland"
DIFC = "UAE HR Test DIFC"
ABROAD = "UAE HR Test Abroad"

# Luhn-valid Emirates ID for a 1990 birth year
EID_1990 = "784-1990-1234567-6"
IBAN_OK = "AE070331234567890123456"


def make_company(name=MAINLAND, country="United Arab Emirates", currency="AED", jurisdiction=None):
	if not frappe.db.exists("Company", name):
		abbr = "".join(w[0] for w in name.split()) + str(len(name))
		frappe.get_doc(
			{
				"doctype": "Company",
				"company_name": name,
				"abbr": abbr,
				"default_currency": currency,
				"country": country,
				"create_chart_of_accounts_based_on": "Standard Template",
				"chart_of_accounts": "Standard",
			}
		).insert(ignore_permissions=True)
	if jurisdiction:
		settings = frappe.get_single("UAE HR Settings")
		if not any(r.company == name for r in settings.companies):
			settings.append("companies", {"company": name, "jurisdiction": jurisdiction})
			settings.save()
	return name


def make_bank(code="033", name="Test Bank Alpha"):
	if not frappe.db.exists("UAE Bank", name):
		frappe.get_doc(
			{"doctype": "UAE Bank", "bank_name": name, "bank_code": code, "wps_routing_code": "123456789"}
		).insert()
	return name


def make_employee(company=MAINLAND, **kw):
	values = {
		"doctype": "Employee",
		"first_name": kw.pop("first_name", "Test Worker"),
		"gender": "Male",
		"date_of_birth": "1990-05-01",
		"date_of_joining": "2025-01-01",
		"company": company,
		"status": "Active",
	}
	values.update(kw)
	doc = frappe.get_doc(values)
	doc.insert(ignore_permissions=True)
	return doc


def make_document(employee, document_type="Passport", **kw):
	values = {
		"doctype": "UAE Employee Document",
		"employee": employee,
		"document_type": document_type,
		"document_number": kw.pop("document_number", "P" + frappe.generate_hash(length=7).upper()),
		"issue_date": "2024-01-01",
		"expiry_date": add_days(today(), 400),
	}
	values.update(kw)
	return frappe.get_doc(values).insert(ignore_permissions=True)


def use_default_reminders(default="60,30,7"):
	"""Reminder days as on a fresh install: no document type has its own, the settings default applies.

	A site in use sets per-type reminder days, which changes which notifications exist. Tests that
	count lead times call this in setUp so they pass on any site; the test rollback restores the values.
	"""
	from uae_hr.setup.notifications import refresh_reminder_days

	for name in frappe.get_all("UAE Document Type", filters={"reminder_days": ("is", "set")}, pluck="name"):
		frappe.db.set_value("UAE Document Type", name, "reminder_days", None, update_modified=False)
		frappe.clear_document_cache("UAE Document Type", name)
	frappe.db.set_single_value("UAE HR Settings", "default_reminder_days", default)
	refresh_reminder_days()


def warnings():
	return [f.code for f in (frappe.flags.uae_hr_warnings or [])]


def reset_warnings():
	frappe.flags.uae_hr_warnings = []


def before_tests():
	"""Complete the setup wizard on a blank site with an invented UAE company (HRMS does the same for India)."""
	from frappe.desk.page.setup_wizard.setup_wizard import setup_complete

	frappe.clear_cache()
	if not frappe.get_all("Company", limit=1):
		year = now_datetime().year
		setup_complete(
			{
				"currency": "AED",
				"full_name": "Test User",
				"company_name": MAINLAND,
				"timezone": "Asia/Dubai",
				"company_abbr": "UHTM",
				"industry": "Construction",
				"country": "United Arab Emirates",
				"fy_start_date": f"{year}-01-01",
				"fy_end_date": f"{year}-12-31",
				"language": "english",
				"company_tagline": "Testing",
				"email": "test@example.com",
				"password": "test",
				"chart_of_accounts": "Standard",
			}
		)
	frappe.db.commit()  # nosemgrep


class UAETestCase(IntegrationTestCase):
	"""Rolls back after every test, not just every class, so tests cannot leak settings into each other."""

	def setUp(self):
		super().setUp()
		frappe.db.savepoint("uae_hr_test")
		reset_warnings()

	def tearDown(self):
		try:
			frappe.db.rollback(save_point="uae_hr_test")
		except Exception:
			# something released the savepoint (a commit or DDL); fall back to a full rollback
			frappe.db.rollback()
		frappe.clear_cache()
		super().tearDown()
