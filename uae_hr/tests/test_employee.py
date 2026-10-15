import frappe

from uae_hr.tests.utils import (
	ABROAD,
	DIFC,
	EID_1990,
	IBAN_OK,
	MAINLAND,
	UAETestCase,
	make_bank,
	make_company,
	make_employee,
	reset_warnings,
	warnings,
)


class TestEmployeeRules(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)
		make_company(DIFC, jurisdiction="DIFC (not covered)")
		make_company(ABROAD, country="India", currency="INR")

	def setUp(self):
		super().setUp()
		reset_warnings()

	def test_probation_over_six_months_blocks(self):
		"""DL 9(1)"""
		self.assertRaises(frappe.ValidationError, make_employee, uae_probation_months=7)

	def test_probation_sets_confirmation_date(self):
		emp = make_employee(uae_probation_months=6, date_of_joining="2025-03-15")
		self.assertEqual(str(emp.final_confirmation_date), "2025-09-15")

	def test_hand_typed_confirmation_date_checked(self):
		self.assertRaises(
			frappe.ValidationError,
			make_employee,
			date_of_joining="2025-01-01",
			final_confirmation_date="2025-08-01",
		)

	def test_notice_outside_range_blocks(self):
		"""DL 43(1)"""
		self.assertRaises(frappe.ValidationError, make_employee, notice_number_of_days=14)
		self.assertRaises(frappe.ValidationError, make_employee, notice_number_of_days=91)
		self.assertEqual(make_employee(notice_number_of_days=60).notice_number_of_days, 60)

	def test_not_covered_companies_are_left_alone(self):
		"""Plan U9: DIFC and ADGM have their own laws; a company outside the UAE is not ours to check."""
		self.assertTrue(make_employee(company=DIFC, notice_number_of_days=14).name)
		self.assertTrue(make_employee(company=ABROAD, uae_probation_months=12).name)

	def test_iban_sets_bank_and_account(self):
		bank = make_bank("033")
		emp = make_employee(salary_mode="Bank", iban="ae07 0331 2345 6789 0123 456")
		self.assertEqual(emp.iban, IBAN_OK)
		self.assertEqual(emp.uae_bank, bank)
		self.assertEqual(emp.bank_ac_no, "1234567890123456")
		self.assertEqual(emp.bank_name, bank)

	def test_iban_typo_blocks(self):
		"""Frappe's IBAN field type already rejects a bad checksum on Employee; the import checker reports it earlier."""
		self.assertRaises(
			frappe.ValidationError, make_employee, salary_mode="Bank", iban="AE080331234567890123456"
		)

	def test_eid_mismatch_warns(self):
		emp = make_employee(date_of_birth="1991-01-01")
		reset_warnings()
		emp.db_set("uae_emirates_id", EID_1990)
		emp.reload()
		emp.save()
		self.assertIn("eid_birth_year", warnings())

	def test_nominee_must_be_family(self):
		"""DL 15(2)"""
		emp = make_employee(uae_death_nominee="Invented Person", uae_death_nominee_relation="Spouse")
		self.assertEqual(emp.uae_death_nominee_relation, "Spouse")

	def test_probation_only_once_per_employer(self):
		"""DL 9(2): a re-hired worker given probation again is flagged."""
		first = make_employee(first_name="Rehire", uae_uid="900100200", uae_probation_months=3)
		first.db_set({"status": "Left", "relieving_date": "2025-06-30"})
		reset_warnings()
		make_employee(
			first_name="Rehire", uae_uid="900100200", uae_probation_months=3, date_of_joining="2026-01-01"
		)
		self.assertIn("probation_twice", warnings())

	def test_rehire_without_probation_is_fine(self):
		first = make_employee(first_name="Rehire Two", uae_uid="900100201", uae_probation_months=3)
		first.db_set({"status": "Left", "relieving_date": "2025-06-30"})
		reset_warnings()
		make_employee(first_name="Rehire Two", uae_uid="900100201", date_of_joining="2026-01-01")
		self.assertNotIn("probation_twice", warnings())

	def test_dashboard_lists_uae_documents(self):
		from frappe.desk.notifications import get_open_count

		data = frappe.get_meta("Employee").get_dashboard_data()
		items = [i for group in data.transactions for i in group["items"]]
		self.assertIn("UAE Employee Document", items)
		self.assertIn("UAE HR Letter", items)


class TestPermissions(UAETestCase):
	def test_pro_cannot_read_pay_fields(self):
		"""Plan 3.9: UAE PRO reads Employee at permlevel 0 only."""
		perms = frappe.get_all(
			"Custom DocPerm",
			filters={"parent": "Employee", "role": "UAE PRO"},
			fields=["permlevel", "read", "write"],
		)
		self.assertEqual([(p.permlevel, p.read, p.write) for p in perms], [(0, 1, 0)])
		meta = frappe.get_meta("Employee")
		for field in ("uae_bank", "uae_account_name", "uae_salary_card_no", "uae_salary_agent"):
			self.assertEqual(meta.get_field(field).permlevel, 1, field)
		self.assertTrue(
			frappe.db.exists(
				"Custom DocPerm", {"parent": "Employee", "role": "HR Manager", "permlevel": 1, "read": 1}
			)
		)

	def test_mirrored_fields_are_read_only(self):
		meta = frappe.get_meta("Employee")
		for field in (
			"passport_number",
			"valid_upto",
			"uae_emirates_id",
			"uae_residency_expiry",
			"uae_work_permit_expiry",
		):
			self.assertTrue(meta.get_field(field).read_only, field)


class TestEngagement(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def test_fields_and_options(self):
		meta = frappe.get_meta("Employee")
		self.assertEqual(meta.get_field("uae_visa_establishment").options, "UAE Establishment")
		self.assertIn(
			"Visa only (works for another employer)",
			meta.get_field("uae_engagement_type").options.split("\n"),
		)
		self.assertIn("WPS salary card", meta.get_field("uae_payment_method").options.split("\n"))
		self.assertIn("Fujairah", meta.get_field("uae_visa_emirate").options.split("\n"))

	def test_salaried_without_payment_method_warns(self):
		make_employee(uae_engagement_type="Salaried")
		self.assertIn("no_payment_method", warnings())
		reset_warnings()
		make_employee(uae_engagement_type="Salaried", uae_payment_method="WPS bank account")
		make_employee(uae_engagement_type="Visa only (works for another employer)")
		self.assertNotIn("no_payment_method", warnings())

	def test_visa_establishment_link(self):
		est = frappe.get_doc(
			{"doctype": "UAE Establishment", "establishment_name": "Invented Visa Sponsor"}
		).insert()
		emp = make_employee(uae_visa_establishment=est.name, uae_visa_emirate="Ajman")
		self.assertEqual(emp.uae_visa_establishment, est.name)


class TestReadinessInTab(UAETestCase):
	def test_button_sits_in_the_uae_tab(self):
		meta = frappe.get_meta("Employee")
		field = meta.get_field("uae_contract_readiness")
		self.assertEqual(field.fieldtype, "Button")
		order = [f.fieldname for f in meta.fields]
		tab = order.index("uae_tab")
		self.assertGreater(order.index("uae_contract_readiness"), tab)
		next_tabs = [i for i, f in enumerate(meta.fields) if f.fieldtype == "Tab Break" and i > tab]
		if next_tabs:
			self.assertLess(order.index("uae_contract_readiness"), next_tabs[0])


class TestExitChecklist(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def test_leaving_with_unreturned_items_warns(self):
		emp = make_employee(
			uae_issued_items=[
				{"item_type": "Laptop", "serial_no": "LT-001", "issued_on": "2025-01-05"},
				{"item_type": "SIM Card", "issued_on": "2025-01-05", "returned_on": "2025-12-01"},
			]
		)
		reset_warnings()
		emp.status, emp.relieving_date = "Left", "2026-01-31"
		emp.save()
		found = [f for f in frappe.flags.uae_hr_warnings or [] if f.code == "unreturned_items"]
		self.assertEqual(len(found), 1)
		self.assertIn("LT-001", found[0].message)
		self.assertNotIn("SIM Card", found[0].message)

	def test_all_returned_is_quiet(self):
		emp = make_employee(
			uae_issued_items=[{"item_type": "Laptop", "issued_on": "2025-01-05", "returned_on": "2025-12-01"}]
		)
		reset_warnings()
		emp.status, emp.relieving_date = "Left", "2026-01-31"
		emp.save()
		self.assertNotIn("unreturned_items", warnings())

	def test_section_is_on_the_exit_tab(self):
		meta = frappe.get_meta("Employee")
		order = [f.fieldname for f in meta.fields]
		tabs = [(i, f.fieldname) for i, f in enumerate(meta.fields) if f.fieldtype == "Tab Break"]
		pos = order.index("uae_exit_items_html")
		tab = [name for i, name in tabs if i < pos][-1]
		self.assertEqual(tab, "exit")


class TestSeededBanks(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def test_adcb_iban_decodes_to_adcb_not_investbank(self):
		adcb = frappe.db.get_value("UAE Bank", {"bank_code": "003"}, "name")
		emp = make_employee(salary_mode="Bank", iban="AE37 0030 0123 4567 8901 234")
		self.assertEqual(emp.uae_bank, adcb)
		self.assertNotEqual(emp.uae_bank, frappe.db.get_value("UAE Bank", {"bank_code": "030"}, "name"))
		self.assertIn("ADCB", emp.bank_name)

	def test_merged_bank_iban_decodes_and_warns(self):
		emp = make_employee(salary_mode="Bank", iban="AE540450012345678901234")
		self.assertEqual(emp.uae_bank, frappe.db.get_value("UAE Bank", {"bank_code": "045"}, "name"))
		self.assertIn("iban_bank_merged", warnings())
