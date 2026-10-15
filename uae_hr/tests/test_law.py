"""The law registry, the settings it generates, and the rule for changing a legal value."""

import json
import os

import frappe
from frappe.tests import UnitTestCase

from uae_hr import law
from uae_hr.tests.utils import UAETestCase

APP = frappe.get_app_path("uae_hr")


class TestRegistry(UnitTestCase):
	def test_every_parameter_is_cited(self):
		for p in law.PARAMS:
			self.assertRegex(p.citation, r"^(DL|CR) \d+", p.fieldname)
			self.assertGreater(p.default, 0, p.fieldname)
			self.assertIn(p.section, law.SECTIONS, p.fieldname)

	def test_quotes_are_verbatim_from_the_law_text(self):
		path = os.path.join(APP, "..", "docs", "law.md")
		if not os.path.exists(path):
			self.skipTest("docs/law.md not shipped with this install")
		text = open(path).read()
		for p in law.PARAMS:
			if p.quote:
				for piece in p.quote.split(" … "):
					self.assertIn(piece, text, p.fieldname)

	def test_settings_doctype_matches_registry(self):
		path = os.path.join(APP, "uae_hr", "doctype", "uae_hr_settings", "uae_hr_settings.json")
		fields = {f["fieldname"]: f for f in json.load(open(path))["fields"]}
		for p in law.PARAMS:
			self.assertIn(p.fieldname, fields, "run dev/gen_doctypes.py")
			self.assertEqual(fields[p.fieldname]["default"], str(p.default), p.fieldname)
			self.assertIn(p.citation, fields[p.fieldname]["description"], p.fieldname)

	def test_direction(self):
		probation = law.BY_FIELDNAME["probation_max_months"]
		self.assertFalse(law.less_favourable(probation, 3))
		self.assertTrue(law.less_favourable(probation, 9))
		notice_min = law.BY_FIELDNAME["notice_min_days"]
		self.assertTrue(law.less_favourable(notice_min, 45))
		self.assertFalse(law.less_favourable(notice_min, 30))


class TestSettings(UAETestCase):
	def test_defaults_are_the_law(self):
		for p in law.PARAMS:
			self.assertEqual(law.get_param(p.fieldname), p.default, p.fieldname)

	def test_more_generous_is_allowed(self):
		s = frappe.get_single("UAE HR Settings")
		s.probation_max_months = 3
		s.annual_leave_days = 35
		s.save()
		self.assertEqual(law.get_param("probation_max_months"), 3)

	def test_less_generous_needs_a_reference(self):
		s = frappe.get_single("UAE HR Settings")
		s.probation_max_months = 9
		s.amendment_reference = ""
		self.assertRaises(frappe.ValidationError, s.save)
		s = frappe.get_single("UAE HR Settings")
		s.probation_max_months = 9
		s.amendment_reference = "Cabinet Resolution No. 99 of 2027 (invented, for the test)"
		s.save()
		self.assertEqual(law.get_param("probation_max_months"), 9)

	def test_zero_rejected(self):
		s = frappe.get_single("UAE HR Settings")
		s.notice_min_days = -1
		self.assertRaises(frappe.ValidationError, s.save)


class TestTranslations(UnitTestCase):
	def test_every_string_has_arabic(self):
		"""DL 66: Arabic is the language of record, so no label ships without it."""
		import importlib.util

		path = os.path.join(APP, "..", "dev", "extract_messages.py")
		if not os.path.exists(path):
			self.skipTest("dev/ not shipped with this install")
		spec = importlib.util.spec_from_file_location("extract_messages", path)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		missing = sorted(mod.collect() - set(mod.existing()))
		self.assertEqual(missing, [], "run python3 dev/build_translations.py")
