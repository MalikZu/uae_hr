import frappe

from uae_hr.tests.utils import MAINLAND, UAETestCase, make_company, make_employee, reset_warnings, warnings


def letter(employee, letter_type, **kw):
	return frappe.get_doc(
		{"doctype": "UAE HR Letter", "employee": employee, "letter_type": letter_type, **kw}
	)


class TestHRLetter(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def setUp(self):
		super().setUp()
		reset_warnings()
		self.emp = make_employee(date_of_joining="2021-04-01")

	def test_experience_certificate_needs_the_dl_13_11_facts(self):
		"""DL 13(11): start, end, total service, job, last wage, reason."""
		self.assertRaises(frappe.ValidationError, letter(self.emp.name, "Experience Certificate").insert)
		doc = letter(
			self.emp.name,
			"Experience Certificate",
			service_end_date="2026-03-31",
			job_title="Site Engineer",
			last_wage=9000,
			termination_reason="Contract ended",
		).insert()
		self.assertEqual(str(doc.service_start_date), "2021-04-01")
		self.assertEqual(doc.total_service, "4 years, 11 months, 30 days")

	def test_experience_certificate_fills_from_employee(self):
		self.emp.db_set({"relieving_date": "2026-01-31", "reason_for_leaving": "Resigned"})
		doc = letter(self.emp.name, "Experience Certificate", job_title="Foreman", last_wage=4000).insert()
		self.assertEqual(str(doc.service_end_date), "2026-01-31")
		self.assertEqual(doc.termination_reason, "Resigned")

	def test_submitted_letter_is_frozen(self):
		doc = letter(self.emp.name, "Salary Certificate", addressed_to="To whom it may concern").insert()
		doc.submit()
		doc.addressed_to = "Changed"
		self.assertRaises(frappe.ValidationError, doc.save)

	def test_warning_time_limits(self):
		"""CR 24(4): charge within 30 days of detection, penalty within 60 days of the investigation."""
		letter(
			self.emp.name,
			"Warning",
			violation="Invented violation",
			violation_detected_on="2026-01-01",
			charged_on="2026-03-01",
			investigation_closed_on="2026-03-05",
			issue_date="2026-06-01",
		).insert()
		self.assertIn("charge_late", warnings())
		self.assertIn("penalty_late", warnings())

	def test_warning_in_time(self):
		letter(
			self.emp.name,
			"Warning",
			violation="Invented violation",
			violation_detected_on="2026-01-01",
			charged_on="2026-01-10",
			investigation_closed_on="2026-01-20",
			issue_date="2026-02-01",
		).insert()
		self.assertEqual(warnings(), [])

	def test_warning_needs_its_dates(self):
		self.assertRaises(frappe.ValidationError, letter(self.emp.name, "Warning", violation="x").insert)
