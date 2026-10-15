"""Each legal rule as a pure function, tested without the database."""

from datetime import date

from frappe.tests import UnitTestCase

from uae_hr import checks
from uae_hr.tests.utils import EID_1990, IBAN_OK


def codes(findings):
	return [f.code for f in findings]


class TestEmiratesID(UnitTestCase):
	def test_valid_number_passes(self):
		self.assertEqual(checks.check_emirates_id(EID_1990, date(1990, 5, 1)), [])

	def test_formats_to_dashed_form(self):
		self.assertEqual(checks.format_eid("784199012345676"), EID_1990)
		self.assertIsNone(checks.format_eid("12345"))

	def test_wrong_length_or_prefix(self):
		self.assertEqual(codes(checks.check_emirates_id("784-1990-123-4")), ["eid_format"])
		self.assertEqual(codes(checks.check_emirates_id("785-1990-1234567-6")), ["eid_format"])

	def test_bad_check_digit(self):
		self.assertIn("eid_check_digit", codes(checks.check_emirates_id("784-1990-1234567-5")))

	def test_birth_year_must_match(self):
		self.assertEqual(codes(checks.check_emirates_id(EID_1990, date(1991, 5, 1))), ["eid_birth_year"])

	def test_empty_is_fine(self):
		self.assertEqual(checks.check_emirates_id(None), [])

	def test_only_warns(self):
		self.assertFalse(checks.blocks(checks.check_emirates_id("garbage")))


class TestIBAN(UnitTestCase):
	def test_valid(self):
		self.assertEqual(checks.check_iban(IBAN_OK), [])
		self.assertEqual(checks.check_iban("ae07 0331 2345 6789 0123 456"), [])

	def test_checksum(self):
		self.assertEqual(codes(checks.check_iban("AE080331234567890123456")), ["iban_checksum"])

	def test_uae_length(self):
		self.assertEqual(codes(checks.check_iban("AE07033123456789")), ["iban_format"])

	def test_parts(self):
		self.assertEqual(checks.uae_iban_parts(IBAN_OK), ("033", "1234567890123456"))
		self.assertIsNone(checks.uae_iban_parts("GB82WEST12345698765432"))

	def test_foreign_iban_checked_by_checksum_only(self):
		self.assertEqual(checks.check_iban("GB82WEST12345698765432"), [])


class TestProbation(UnitTestCase):
	"""DL 9(1): probation of at most 6 months from the date work starts."""

	def test_six_months_allowed(self):
		self.assertEqual(checks.check_probation(6, 6), [])

	def test_seven_months_blocks(self):
		f = checks.check_probation(7, 6)
		self.assertEqual(codes(f), ["probation_max"])
		self.assertEqual(f[0].level, checks.BLOCK)
		self.assertEqual(f[0].citation, "DL 9(1)")

	def test_limit_comes_from_caller(self):
		self.assertEqual(checks.check_probation(7, 9), [])

	def test_confirmation_date_beyond_limit_blocks(self):
		self.assertEqual(
			codes(checks.check_probation(None, 6, "2025-01-01", "2025-07-02")), ["probation_end"]
		)
		self.assertEqual(checks.check_probation(None, 6, "2025-01-01", "2025-07-01"), [])

	def test_end_date(self):
		self.assertEqual(checks.probation_end("2025-01-31", 1), date(2025, 2, 28))
		self.assertIsNone(checks.probation_end("2025-01-01", 0))


class TestNotice(UnitTestCase):
	"""DL 43(1): notice of not less than 30 and not more than 90 days."""

	def test_range(self):
		for days in (30, 60, 90):
			self.assertEqual(checks.check_notice(days, 30, 90), [], days)
		for days in (29, 14, 91, 120):
			f = checks.check_notice(days, 30, 90)
			self.assertEqual(codes(f), ["notice_range"], days)
			self.assertEqual(f[0].level, checks.BLOCK)

	def test_unset_is_not_checked(self):
		self.assertEqual(checks.check_notice(None, 30, 90), [])
		self.assertEqual(checks.check_notice(0, 30, 90), [])


class TestRetention(UnitTestCase):
	"""DL 13(1): the worker file is kept at least 2 years after the end of service."""

	def test_active_employee_not_restricted(self):
		self.assertEqual(checks.check_retention("Active", None, 2, "2026-01-01"), [])

	def test_within_two_years_blocks(self):
		self.assertEqual(codes(checks.check_retention("Left", "2025-03-01", 2, "2027-02-28")), ["retention"])

	def test_after_two_years_allowed(self):
		self.assertEqual(checks.check_retention("Left", "2025-03-01", 2, "2027-03-01"), [])

	def test_left_without_date_blocks(self):
		self.assertEqual(codes(checks.check_retention("Left", None, 2, "2030-01-01")), ["retention_no_date"])


class TestWarningTiming(UnitTestCase):
	"""CR 24(4): charge within 30 days of detection, penalty within 60 days of the investigation."""

	def t(self, detected, charged, closed, issued):
		return codes(checks.check_warning_timing(detected, charged, closed, issued, 30, 60))

	def test_in_time(self):
		self.assertEqual(self.t("2026-01-01", "2026-01-31", "2026-02-10", "2026-04-11"), [])

	def test_late_charge(self):
		self.assertEqual(self.t("2026-01-01", "2026-02-01", "2026-02-10", "2026-02-11"), ["charge_late"])

	def test_late_penalty(self):
		self.assertEqual(self.t("2026-01-01", "2026-01-05", "2026-02-10", "2026-04-12"), ["penalty_late"])

	def test_impossible_order_blocks(self):
		self.assertIn("charge_before_detection", self.t("2026-01-10", "2026-01-05", None, None))
		self.assertIn(
			"penalty_before_investigation", self.t("2026-01-01", "2026-01-02", "2026-01-10", "2026-01-09")
		)
		self.assertIn("investigation_before_charge", self.t("2026-01-01", "2026-01-10", "2026-01-05", None))


class TestOtherRules(UnitTestCase):
	def test_service_length(self):
		self.assertEqual(checks.service_length("2020-01-15", "2025-03-10"), (5, 1, 23))
		self.assertEqual(checks.service_length("2020-01-01", "2020-01-01"), (0, 0, 0))

	def test_nominee_must_be_family(self):
		"""DL 15(2) + DL 1: the nominee is a family member, and family is spouse, sons and daughters."""
		self.assertEqual(checks.check_nominee("A", "Spouse"), [])
		self.assertEqual(codes(checks.check_nominee("A", "Brother")), ["nominee_family"])
		self.assertEqual(codes(checks.check_nominee("A", None)), ["nominee_relation"])

	def test_official_documents_are_not_issued_items(self):
		"""DL 13(2): official documents may not be withheld."""
		for name in (
			"Passport",
			"Passport held",
			"Emirates ID",
			"Residence Visa",
			"Labour Card",
			"Work permit",
		):
			self.assertEqual(codes(checks.check_issued_item_type(name)), ["withheld_document"], name)
		for name in ("SIM Card", "Laptop", "Visa Card", "Fuel Card"):
			self.assertEqual(checks.check_issued_item_type(name), [], name)

	def test_basic_wage_required_with_allowances(self):
		"""DL 1 / DL 51(5): basic wage is separate, and gratuity is calculated on it."""
		self.assertEqual(codes(checks.check_pay_split(0, 2000, 500, 0)), ["no_basic"])
		self.assertEqual(checks.check_pay_split(5000, 2000, 500, 0), [])
		self.assertEqual(codes(checks.check_pay_split(5000, -1, 0, 0)), ["negative_pay"])

	def test_person_code(self):
		self.assertEqual(checks.check_person_code("12345678901234"), [])
		self.assertEqual(codes(checks.check_person_code("1234")), ["person_code"])


class TestPayAgainstContract(UnitTestCase):
	def test_below_contract(self):
		self.assertEqual(
			codes(checks.check_pay_vs_contract(4000, 6000, 5000, 6000)), ["basic_below_contract"]
		)
		self.assertEqual(
			codes(checks.check_pay_vs_contract(5000, 5500, 5000, 6000)), ["total_below_contract"]
		)
		self.assertEqual(checks.check_pay_vs_contract(5000, 6000, 5000, 6000), [])
		self.assertEqual(checks.check_pay_vs_contract(5000, 6000, 0, 0), [])

	def test_only_warns(self):
		self.assertFalse(checks.blocks(checks.check_pay_vs_contract(0, 0, 5000, 6000)))


class TestExitClearance(UnitTestCase):
	def test_unreturned(self):
		rows = [
			{"item_type": "Laptop", "serial_no": "X1"},
			{"item_type": "PPE", "returned_on": "2026-01-01"},
			{},
		]
		f = checks.check_unreturned_items(rows)
		self.assertEqual(codes(f), ["unreturned_items"])
		self.assertIn("Laptop X1", f[0].message)
		self.assertEqual(
			checks.check_unreturned_items([{"item_type": "PPE", "returned_on": "2026-01-01"}]), []
		)
