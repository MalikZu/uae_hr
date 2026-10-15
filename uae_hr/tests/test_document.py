import frappe
from frappe.utils import add_days, getdate, today

from uae_hr.tests.utils import (
	EID_1990,
	MAINLAND,
	UAETestCase,
	make_company,
	make_document,
	make_employee,
	reset_warnings,
	use_default_reminders,
	warnings,
)
from uae_hr.uae_hr.doctype.uae_employee_document.uae_employee_document import mark_expired, verify_many


class TestEmployeeDocument(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def setUp(self):
		super().setUp()
		reset_warnings()
		use_default_reminders()
		self.emp = make_employee()

	def test_verify_mirrors_to_employee(self):
		doc = make_document(
			self.emp.name,
			"Passport",
			document_number="X1234567",
			expiry_date="2031-02-03",
			issue_date="2021-02-04",
			place_of_issue="Testville",
		)
		self.assertEqual(doc.status, "Unverified")
		doc.verify()
		self.assertEqual(doc.status, "Current")
		self.assertEqual(doc.verified_by, frappe.session.user)
		emp = frappe.get_doc("Employee", self.emp.name)
		self.assertEqual(emp.passport_number, "X1234567")
		self.assertEqual(str(emp.valid_upto), "2031-02-03")
		self.assertEqual(str(emp.date_of_issue), "2021-02-04")
		self.assertEqual(emp.place_of_issue, "Testville")

	def test_unverified_document_does_not_mirror(self):
		make_document(self.emp.name, "Passport", document_number="NOTYET1")
		self.assertNotEqual(frappe.db.get_value("Employee", self.emp.name, "passport_number"), "NOTYET1")

	def test_new_document_supersedes_the_old(self):
		old = make_document(
			self.emp.name, "Emirates ID", document_number=EID_1990, date_of_birth="1990-05-01"
		)
		old.verify()
		new = make_document(
			self.emp.name, "Emirates ID", document_number="784199076543210", expiry_date="2032-01-01"
		)
		new.verify()
		old.reload()
		self.assertEqual(old.status, "Superseded")
		self.assertEqual(old.superseded_by, new.name)
		self.assertEqual(new.status, "Current")
		self.assertEqual(new.document_number, "784-1990-7654321-0")
		self.assertEqual(
			frappe.db.get_value("Employee", self.emp.name, "uae_emirates_id"), "784-1990-7654321-0"
		)
		self.assertEqual(
			str(frappe.db.get_value("Employee", self.emp.name, "uae_emirates_id_expiry")), "2032-01-01"
		)

	def test_only_unverified_can_be_verified(self):
		doc = make_document(self.emp.name)
		doc.verify()
		self.assertRaises(frappe.ValidationError, doc.verify)

	def test_only_hr_manager_verifies(self):
		doc = make_document(self.emp.name)
		user = "uae.pro.test@example.com"
		if not frappe.db.exists("User", user):
			frappe.get_doc(
				{"doctype": "User", "email": user, "first_name": "PRO", "roles": [{"role": "UAE PRO"}]}
			).insert(ignore_permissions=True)
		with self.set_user(user):
			self.assertRaises(
				frappe.PermissionError, frappe.get_doc("UAE Employee Document", doc.name).verify
			)

	def test_cancel_clears_mirrors(self):
		doc = make_document(self.emp.name, "Residence Visa", expiry_date="2030-06-30")
		doc.verify()
		self.assertEqual(
			str(frappe.db.get_value("Employee", self.emp.name, "uae_residency_expiry")), "2030-06-30"
		)
		doc.cancel_document("visa cancelled")
		self.assertEqual(doc.status, "Cancelled")
		self.assertIsNone(frappe.db.get_value("Employee", self.emp.name, "uae_residency_expiry"))

	def test_expiry_required_when_type_has_one(self):
		self.assertRaises(frappe.ValidationError, make_document, self.emp.name, "Passport", expiry_date=None)
		self.assertTrue(make_document(self.emp.name, "Degree Certificate", expiry_date=None).name)

	def test_expiry_after_issue(self):
		self.assertRaises(
			frappe.ValidationError,
			make_document,
			self.emp.name,
			issue_date="2026-01-01",
			expiry_date="2025-01-01",
		)

	def test_duplicate_blocked(self):
		make_document(self.emp.name, "Passport", document_number="DUP111")
		self.assertRaises(
			frappe.DuplicateEntryError, make_document, self.emp.name, "Passport", document_number="DUP111"
		)

	def test_needs_employee_or_applicant(self):
		self.assertRaises(frappe.ValidationError, make_document, None)

	def test_retention_blocks_delete(self):
		"""DL 13(1): the file is kept 2 years after the end of service."""
		doc = make_document(self.emp.name)
		self.emp.db_set({"status": "Left", "relieving_date": add_days(today(), -30)})
		self.assertRaises(frappe.ValidationError, frappe.delete_doc, "UAE Employee Document", doc.name)
		self.emp.db_set("relieving_date", add_days(today(), -800))
		frappe.delete_doc("UAE Employee Document", doc.name)
		self.assertFalse(frappe.db.exists("UAE Employee Document", doc.name))

	def test_active_employee_document_can_be_deleted(self):
		doc = make_document(self.emp.name)
		frappe.delete_doc("UAE Employee Document", doc.name)

	def test_mark_expired(self):
		doc = make_document(self.emp.name, issue_date="2020-01-01", expiry_date=add_days(today(), 5))
		doc.verify()
		frappe.db.set_value("UAE Employee Document", doc.name, "expiry_date", add_days(today(), -1))
		mark_expired()
		self.assertEqual(frappe.db.get_value("UAE Employee Document", doc.name, "status"), "Expired")

	def test_cross_checks(self):
		"""Plan 3.3: same birth date, passport number on the visa, one visa designation."""
		make_document(
			self.emp.name, "Passport", document_number="PP0001", date_of_birth="1990-05-01"
		).verify()
		visa = make_document(
			self.emp.name,
			"Residence Visa",
			passport_number="PP0002",
			designation_on_document="Engineer",
			date_of_birth="1989-01-01",
		)
		reset_warnings()
		visa.verify()
		self.assertIn("visa_passport", warnings())
		self.assertIn("dob_mismatch", warnings())
		permit = make_document(self.emp.name, "Work Permit", designation_on_document="Labourer")
		reset_warnings()
		permit.verify()
		self.assertIn("designation_mismatch", warnings())

	def test_matching_documents_raise_nothing(self):
		make_document(
			self.emp.name, "Passport", document_number="PP0100", date_of_birth="1990-05-01"
		).verify()
		visa = make_document(
			self.emp.name, "Residence Visa", passport_number="pp0100", designation_on_document="Engineer"
		)
		reset_warnings()
		visa.verify()
		self.assertEqual(warnings(), [])

	def test_reminder_days_from_type_or_default(self):
		doc = make_document(self.emp.name)
		self.assertEqual(doc.reminder_days, "60,30,7")
		dtype = frappe.get_doc("UAE Document Type", "Passport")
		dtype.reminder_days = "180, 90,30"
		dtype.save()
		self.assertEqual(frappe.db.get_value("UAE Employee Document", doc.name, "reminder_days"), "180,90,30")
		self.assertTrue(frappe.db.exists("Notification", "UAE HR: document expires in 180 days"))

	def test_bulk_verify_reports_each(self):
		ok = make_document(self.emp.name)
		done = make_document(self.emp.name, "Emirates ID", document_number=EID_1990)
		done.verify()
		results = {r["name"]: r for r in verify_many(frappe.as_json([ok.name, done.name]))}
		self.assertTrue(results[ok.name]["ok"])
		self.assertFalse(results[done.name]["ok"])
		self.assertEqual(frappe.db.get_value("UAE Employee Document", ok.name, "status"), "Current")

	def test_scans_are_private(self):
		doc = make_document(self.emp.name)
		f = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": "scan.txt",
				"content": b"invented",
				"attached_to_doctype": doc.doctype,
				"attached_to_name": doc.name,
				"is_private": 0,
			}
		).insert(ignore_permissions=True)
		self.assertTrue(f.is_private)


class TestVerifiedDocumentLock(UAETestCase):
	"""A verified document cannot drift from the Employee mirror: it is locked until reopened."""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def setUp(self):
		super().setUp()
		self.emp = make_employee()

	def test_verified_identity_is_locked(self):
		doc = make_document(self.emp.name, "Passport", document_number="L100", expiry_date="2031-01-01")
		doc.verify()
		doc.reload()
		doc.document_number = "L101"
		self.assertRaises(frappe.ValidationError, doc.save)
		doc.reload()
		doc.expiry_date = "2032-01-01"
		self.assertRaises(frappe.ValidationError, doc.save)

	def test_notes_and_scan_stay_editable(self):
		doc = make_document(self.emp.name)
		doc.verify()
		doc.reload()
		doc.notes = "renewal started"
		doc.save()
		self.assertEqual(doc.notes, "renewal started")

	def test_reopen_then_correct_then_verify(self):
		doc = make_document(self.emp.name, "Passport", document_number="R200", expiry_date="2031-01-01")
		doc.verify()
		doc.reload()
		doc.reopen()
		self.assertEqual((doc.status, doc.verified_by, doc.verified_on), ("Unverified", None, None))
		# mirrors untouched until verified again
		self.assertEqual(frappe.db.get_value("Employee", self.emp.name, "passport_number"), "R200")
		doc.reload()
		doc.document_number = "R201"
		doc.save()
		self.assertEqual(frappe.db.get_value("Employee", self.emp.name, "passport_number"), "R200")
		doc.verify()
		self.assertEqual(frappe.db.get_value("Employee", self.emp.name, "passport_number"), "R201")

	def test_only_hr_manager_reopens(self):
		doc = make_document(self.emp.name)
		doc.verify()
		user = "uae.pro.test@example.com"
		if not frappe.db.exists("User", user):
			frappe.get_doc(
				{"doctype": "User", "email": user, "first_name": "PRO", "roles": [{"role": "UAE PRO"}]}
			).insert(ignore_permissions=True)
		with self.set_user(user):
			self.assertRaises(
				frappe.PermissionError, frappe.get_doc("UAE Employee Document", doc.name).reopen
			)

	def test_reopened_older_document_does_not_take_over(self):
		old = make_document(self.emp.name, "Passport", document_number="O1", expiry_date="2027-01-01")
		old.verify()
		new = make_document(self.emp.name, "Passport", document_number="O2", expiry_date="2035-01-01")
		new.verify()
		old.reload()
		old.reopen()
		old.reload()
		old.place_of_issue = "Corrected"
		old.save()
		old.verify()
		self.assertEqual((old.status, old.superseded_by), ("Superseded", new.name))
		self.assertEqual(frappe.db.get_value("UAE Employee Document", new.name, "status"), "Current")
		self.assertEqual(frappe.db.get_value("Employee", self.emp.name, "passport_number"), "O2")

	def test_lock_list_matches_the_form(self):
		from uae_hr.uae_hr.doctype.uae_employee_document.uae_employee_document import LOCKED_FIELDS

		meta = frappe.get_meta("UAE Employee Document")
		in_form = {f.fieldname for f in meta.fields if f.read_only_depends_on}
		self.assertEqual(in_form, set(LOCKED_FIELDS))


class TestRenewal(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def setUp(self):
		super().setUp()
		self.emp = make_employee()

	def test_renewal_keeps_the_number(self):
		"""An Emirates ID renewal keeps the EID number and gets a new expiry date."""
		old = make_document(self.emp.name, "Emirates ID", document_number=EID_1990, expiry_date="2027-03-01")
		old.verify()
		new = make_document(self.emp.name, "Emirates ID", document_number=EID_1990, expiry_date="2030-03-01")
		new.verify()
		self.assertEqual(frappe.db.get_value("UAE Employee Document", old.name, "status"), "Superseded")
		self.assertEqual(
			str(frappe.db.get_value("Employee", self.emp.name, "uae_emirates_id_expiry")), "2030-03-01"
		)

	def test_same_number_and_expiry_is_a_duplicate_and_says_where(self):
		first = make_document(self.emp.name, "Passport", document_number="D1", expiry_date="2031-05-05")
		with self.assertRaises(frappe.DuplicateEntryError) as ctx:
			make_document(self.emp.name, "Passport", document_number="D1", expiry_date="2031-05-05")
		self.assertIn(first.name, str(ctx.exception))

	def test_cancelled_record_does_not_block(self):
		first = make_document(self.emp.name, "Passport", document_number="D2", expiry_date="2031-05-05")
		first.cancel_document("entered by mistake")
		self.assertTrue(
			make_document(self.emp.name, "Passport", document_number="D2", expiry_date="2031-05-05").name
		)

	def test_no_expiry_type_still_refuses_repeats(self):
		make_document(self.emp.name, "NDA", document_number="N9", expiry_date=None)
		self.assertRaises(
			frappe.DuplicateEntryError,
			make_document,
			self.emp.name,
			"NDA",
			document_number="N9",
			expiry_date=None,
		)


class TestContractSalary(UAETestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		make_company(MAINLAND)

	def test_total_is_computed_and_locked(self):
		emp = make_employee()
		doc = make_document(
			emp.name,
			"MOHRE Employment Contract",
			contract_basic=4000,
			contract_housing=1500,
			contract_transport=300,
			contract_other=200,
		)
		self.assertEqual(doc.check_profile, "MOHRE Employment Contract")
		self.assertEqual(doc.contract_total, 6000)
		doc.verify()
		doc.reload()
		doc.contract_basic = 3000
		self.assertRaises(frappe.ValidationError, doc.save)

	def test_negative_amount_refused(self):
		emp = make_employee()
		self.assertRaises(
			frappe.ValidationError, make_document, emp.name, "MOHRE Employment Contract", contract_basic=-1
		)

	def test_patch_sets_the_profile_on_older_sites(self):
		from uae_hr.patches.v0_1_2.mohre_contract_check_profile import NAME, execute

		emp = make_employee()
		doc = make_document(emp.name, NAME)
		frappe.db.set_value("UAE Document Type", NAME, "check_profile", "")
		frappe.db.set_value("UAE Employee Document", doc.name, "check_profile", "")
		execute()
		self.assertEqual(frappe.db.get_value("UAE Document Type", NAME, "check_profile"), NAME)
		self.assertEqual(frappe.db.get_value("UAE Employee Document", doc.name, "check_profile"), NAME)
