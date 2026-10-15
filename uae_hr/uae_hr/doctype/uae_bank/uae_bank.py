# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

import re

import frappe
from frappe import _
from frappe.model.document import Document


class UAEBank(Document):
	def validate(self):
		if self.bank_code and not re.fullmatch(r"\d{3}", self.bank_code):
			frappe.throw(_("The IBAN bank code is 3 digits"))
		if self.wps_routing_code and not re.fullmatch(r"\d{9}", self.wps_routing_code):
			frappe.throw(_("The WPS routing code is 9 digits"))
		if self.swift_code:
			self.swift_code = self.swift_code.strip().upper()
			if not re.fullmatch(r"[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?", self.swift_code):
				frappe.throw(_("{0} is not a valid SWIFT / BIC code").format(self.swift_code))
