import frappe

from uae_hr.tests.utils import UAETestCase


class TestEstablishment(UAETestCase):
	def test_named_by_establishment_name(self):
		doc = frappe.get_doc(
			{
				"doctype": "UAE Establishment",
				"establishment_name": "Invented Sponsor LLC",
				"mohre_establishment_number": "1234567",
				"emirate": "Sharjah",
			}
		).insert()
		self.assertEqual(doc.name, "Invented Sponsor LLC")
		self.assertRaises(
			frappe.DuplicateEntryError,
			frappe.get_doc(
				{"doctype": "UAE Establishment", "establishment_name": "Invented Sponsor LLC"}
			).insert,
		)

	def test_who_may_write(self):
		perms = {p.role: p for p in frappe.get_meta("UAE Establishment").permissions}
		self.assertTrue(perms["HR Manager"].write)
		for role in ("HR User", "UAE PRO"):
			self.assertTrue(perms[role].read, role)
			self.assertFalse(perms[role].write, role)
