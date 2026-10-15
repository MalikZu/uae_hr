"""Seeded masters, notifications, pay components, issued items, readiness, report, idempotent setup."""

import frappe
from frappe.utils import add_days, today

from uae_hr.setup import run_setup
from uae_hr.setup.notifications import PREFIX, sync_notifications
from uae_hr.tests.utils import (
	MAINLAND,
	UAETestCase,
	make_company,
	make_document,
	make_employee,
	use_default_reminders,
)


class TestSeeds(UAETestCase):
	def test_twelve_permit_types(self):
		"""CR 6(1) lists 12 work-permit types, (a) to (l)."""
		refs = sorted(
			frappe.get_all(
				"UAE Permit Type", filters={"legal_reference": ("like", "CR 6(1)%")}, pluck="legal_reference"
			)
		)
		self.assertEqual(refs, [f"CR 6(1)({c})" for c in "abcdefghijkl"])
		self.assertEqual(frappe.db.get_value("UAE Permit Type", "Juvenile Permit", "min_age"), 15)

	def test_document_types(self):
		for name in (
			"Passport",
			"Entry Permit",
			"Residence Visa",
			"Emirates ID",
			"Work Permit",
			"Health Insurance",
			"NDA",
		):
			self.assertTrue(frappe.db.exists("UAE Document Type", name), name)
		maps = {
			r.document_field: r.employee_field
			for r in frappe.get_doc("UAE Document Type", "Emirates ID").field_map
		}
		self.assertEqual(
			maps, {"document_number": "uae_emirates_id", "expiry_date": "uae_emirates_id_expiry"}
		)

	def test_pay_components_read_assignment_fields(self):
		for name, field in (
			("Basic", "uae_basic"),
			("Housing Allowance", "uae_housing"),
			("Transport Allowance", "uae_transport"),
			("Other Allowance", "uae_other"),
		):
			self.assertTrue(frappe.db.exists("Salary Component", name), name)
			description, formula = frappe.db.get_value("Salary Component", name, ["description", "formula"])
			if (description or "").startswith(
				"Monthly amount from"
			):  # seeded by us, not pre-existing on the site
				self.assertEqual(formula, field)

	def test_issued_item_cannot_be_an_official_document(self):
		"""DL 13(2)"""
		self.assertRaises(
			frappe.ValidationError,
			frappe.get_doc({"doctype": "UAE Issued Item Type", "item_type_name": "Passport (held)"}).insert,
		)

	def test_setup_is_idempotent(self):
		"""Running the setup again (what every migrate does) writes nothing."""
		run_setup_no_commit()
		before = snapshot()
		run_setup_no_commit()
		self.assertEqual(before, snapshot())


def run_setup_no_commit():
	from uae_hr.setup.custom_fields import make_custom_fields, make_property_setters
	from uae_hr.setup.masters import seed_masters, seed_settings
	from uae_hr.setup.roles import make_docperms, make_roles
	from uae_hr.setup.salary import seed_components

	make_roles()
	make_custom_fields()
	make_property_setters()
	make_docperms()
	seed_settings()
	seed_masters()
	seed_components()
	sync_notifications()


def snapshot():
	out = {}
	for dt, filters in (
		("Custom Field", {"module": "UAE HR"}),
		("Property Setter", {"module": "UAE HR"}),
		("Notification", {"module": "UAE HR"}),
		("Custom DocPerm", {"parent": "Employee"}),
		("UAE Document Type", {}),
		("UAE Permit Type", {}),
		("Salary Component", {}),
	):
		out[dt] = sorted(
			(r.name, str(r.modified))
			for r in frappe.get_all(dt, filters=filters, fields=["name", "modified"])
		)
	out["Singles"] = sorted(
		map(tuple, frappe.db.sql("select field, value from tabSingles where doctype='UAE HR Settings'"))
	)
	return out


class TestNotifications(UAETestCase):
	def setUp(self):
		super().setUp()
		use_default_reminders()

	def test_one_notification_per_lead_time(self):
		names = frappe.get_all(
			"Notification", filters={"name": ("like", PREFIX + "%"), "enabled": 1}, pluck="name"
		)
		self.assertEqual(sorted(names), sorted(PREFIX + f"{d} days" for d in (60, 30, 7)))
		n = frappe.get_doc("Notification", PREFIX + "30 days")
		self.assertEqual(
			(n.event, n.date_changed, n.days_in_advance, n.document_type),
			("Days Before", "expiry_date", 30, "UAE Employee Document"),
		)
		self.assertEqual([r.receiver_by_role for r in n.recipients], ["UAE PRO", "HR Manager"])

	def test_condition_matches_only_its_lead_time(self):
		n = frappe.get_doc("Notification", PREFIX + "30 days")
		ctx = {"doc": frappe._dict(status="Current", reminder_days="60,30,7")}
		self.assertTrue(frappe.safe_eval(n.condition, None, ctx))
		ctx["doc"].reminder_days = "90,60"
		self.assertFalse(frappe.safe_eval(n.condition, None, ctx))
		ctx["doc"].update(status="Superseded", reminder_days="30")
		self.assertFalse(frappe.safe_eval(n.condition, None, ctx))

	def test_unused_lead_time_is_disabled(self):
		s = frappe.get_single("UAE HR Settings")
		s.default_reminder_days = "45"
		s.save()
		self.assertTrue(frappe.db.get_value("Notification", PREFIX + "45 days", "enabled"))
		self.assertFalse(frappe.db.get_value("Notification", PREFIX + "7 days", "enabled"))

	def test_hr_manager_copy_is_optional(self):
		s = frappe.get_single("UAE HR Settings")
		s.copy_hr_manager = 0
		s.save()
		n = frappe.get_doc("Notification", PREFIX + "30 days")
		self.assertEqual([r.receiver_by_role for r in n.recipients], ["UAE PRO"])


class TestReportAndReadiness(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def test_expiring_documents(self):
		from uae_hr.uae_hr.report.expiring_documents.expiring_documents import execute

		emp = make_employee(first_name="Report Person")
		soon = make_document(emp.name, "Passport", expiry_date=add_days(today(), 20), issue_date="2020-01-01")
		later = make_document(
			emp.name, "Emirates ID", document_number="784-1990-1111111-6", expiry_date=add_days(today(), 200)
		)
		late = make_document(
			emp.name, "Residence Visa", expiry_date=add_days(today(), 10), issue_date="2020-01-01"
		)
		unverified = make_document(emp.name, "Work Permit", expiry_date=add_days(today(), 5))
		for d in (soon, later, late):
			d.verify()
		frappe.db.set_value(
			"UAE Employee Document", late.name, {"expiry_date": add_days(today(), -3), "status": "Expired"}
		)
		_cols, rows = execute({"employee": emp.name})
		got = {r.name: (r.state, r.days_left) for r in rows}
		self.assertEqual(got, {late.name: ("Overdue", -3), soon.name: ("Due", 20)})
		self.assertNotIn(unverified.name, got)
		_cols, rows = execute({"employee": emp.name, "include_overdue": 0, "days": 365})
		self.assertEqual({r.name for r in rows}, {soon.name, later.name})

	def test_contract_readiness_lists_gaps(self):
		"""CR 10(1)"""
		from uae_hr.readiness import get_contract_readiness

		emp = make_employee(first_name="Readiness Person", uae_permit_type="Work Permit")
		r = get_contract_readiness(emp.name)
		missing = {i["item"] for i in r["items"] if not i["ok"]}
		self.assertFalse(r["ready"])
		for item in (
			"Nationality",
			"Notice period",
			"Second contract language beside Arabic",
			"Document: Passport",
			"Document: Work Permit",
		):
			self.assertIn(item, missing)
		self.assertNotIn("Date of birth", missing)
		make_document(emp.name, "Passport").verify()
		frappe.db.set_value("Employee", emp.name, {"uae_nationality": "India", "notice_number_of_days": 30})
		missing = {i["item"] for i in get_contract_readiness(emp.name)["items"] if not i["ok"]}
		self.assertNotIn("Nationality", missing)
		self.assertNotIn("Document: Passport", missing)
		self.assertNotIn("Proof of identity (verified passport or Emirates ID)", missing)


class TestSalaryAssignment(UAETestCase):
	def test_components_total_and_formula_context(self):
		"""Plan 3.7: HRMS formulas see the SSA fields by name."""
		from hrms.payroll.utils import get_component_eval_context

		make_company(MAINLAND)
		emp = make_employee()
		ssa = frappe.new_doc("Salary Structure Assignment")
		ssa.update(
			{
				"employee": emp.name,
				"company": MAINLAND,
				"uae_basic": 6000,
				"uae_housing": 2500,
				"uae_transport": 500,
				"uae_other": 0,
			}
		)
		from uae_hr.salary import validate_assignment

		validate_assignment(ssa)
		self.assertEqual(ssa.uae_total, 9000)
		ctx = get_component_eval_context(emp.name, ssa.as_dict())
		self.assertEqual(frappe.safe_eval("uae_basic + uae_housing", None, ctx), 8500)

	def test_allowances_without_basic_warn(self):
		from uae_hr.salary import validate_assignment
		from uae_hr.tests.utils import reset_warnings, warnings

		make_company(MAINLAND)
		reset_warnings()
		validate_assignment(
			frappe._dict(
				company=MAINLAND, uae_basic=0, uae_housing=1000, uae_transport=0, uae_other=0, base=0
			)
		)
		self.assertIn("no_basic", warnings())


class TestPayAgainstContract(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def ssa(self, emp, **amounts):
		from uae_hr.salary import validate_assignment

		doc = frappe.new_doc("Salary Structure Assignment")
		doc.update({"employee": emp, "company": MAINLAND, **amounts})
		validate_assignment(doc)
		return doc

	def test_empty_base_is_the_four_parts(self):
		emp = make_employee()
		self.assertEqual(
			self.ssa(emp.name, uae_basic=5000, uae_housing=2000, uae_transport=500, uae_other=100).base, 7600
		)

	def test_non_zero_base_is_kept(self):
		emp = make_employee()
		self.assertEqual(self.ssa(emp.name, uae_basic=5000, uae_housing=2000, base=8000).base, 8000)

	def test_pay_below_the_contract_warns(self):
		from uae_hr.tests.utils import reset_warnings, warnings

		emp = make_employee()
		make_document(
			emp.name, "MOHRE Employment Contract", contract_basic=5000, contract_housing=2000
		).verify()
		reset_warnings()
		self.ssa(emp.name, uae_basic=4500, uae_housing=2500)
		self.assertIn("basic_below_contract", warnings())
		self.assertNotIn("total_below_contract", warnings())
		reset_warnings()
		self.ssa(emp.name, uae_basic=5000, uae_housing=1500)
		self.assertEqual(warnings(), ["total_below_contract"])
		reset_warnings()
		self.ssa(emp.name, uae_basic=5000, uae_housing=2000)
		self.assertEqual(warnings(), [])

	def test_unverified_contract_is_ignored(self):
		from uae_hr.tests.utils import reset_warnings, warnings

		emp = make_employee()
		make_document(emp.name, "MOHRE Employment Contract", contract_basic=9000)
		reset_warnings()
		self.ssa(emp.name, uae_basic=1000)
		self.assertNotIn("basic_below_contract", warnings())


class TestBankSeed(UAETestCase):
	SAMPLE = (
		("901", "Invented Test Bank One", "ITB1", "TESTAEAA", "invented for the test"),
		("902", "Invented Test Bank Two", "ITB2", "TESTAEBBXXX", "invented for the test"),
	)

	def test_inserts_missing_by_code_and_keeps_edits(self):
		from uae_hr.setup.banks import seed_banks

		frappe.get_doc({"doctype": "UAE Bank", "bank_name": "Site's Own Name", "bank_code": "902"}).insert()
		seed_banks(self.SAMPLE)
		self.assertEqual(frappe.db.get_value("UAE Bank", {"bank_code": "901"}, "swift_code"), "TESTAEAA")
		# code 902 already existed under the site's own name: left alone
		self.assertEqual(
			frappe.get_all("UAE Bank", filters={"bank_code": "902"}, pluck="name"), ["Site's Own Name"]
		)
		before = frappe.db.get_value("UAE Bank", {"bank_code": "901"}, "modified")
		seed_banks(self.SAMPLE)
		self.assertEqual(frappe.db.get_value("UAE Bank", {"bank_code": "901"}, "modified"), before)

	def test_shipped_rows_are_valid_and_sourced(self):
		import re

		from uae_hr.setup.banks import BANKS

		codes = [b[0] for b in BANKS]
		self.assertEqual(len(codes), len(set(codes)))
		for code, name, _short, swift, source in BANKS:
			self.assertRegex(code, r"^\d{3}$", name)
			self.assertRegex(swift, r"^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$", name)
			self.assertTrue(source, name)
