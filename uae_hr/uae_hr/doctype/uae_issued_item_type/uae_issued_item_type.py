# Copyright (c) 2026, UAE HR contributors
# License: GNU General Public License v3. See LICENSE

import frappe
from frappe.model.document import Document

from uae_hr import checks
from uae_hr.utils import apply_findings


class UAEIssuedItemType(Document):
	def validate(self):
		# DL 13(2): official documents are never "issued" to or held from the worker
		apply_findings(checks.check_issued_item_type(self.item_type_name))
