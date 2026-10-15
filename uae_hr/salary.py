"""Salary Structure Assignment: total of the UAE components and the basic-wage check."""

from frappe import _
from frappe.utils import flt

from uae_hr import checks
from uae_hr.utils import apply_findings, is_covered


def validate_assignment(doc, method=None):
	parts = [flt(doc.get(f)) for f in ("uae_basic", "uae_housing", "uae_transport", "uae_other")]
	doc.uae_total = sum(parts)
	if not is_covered(doc.company) or not doc.uae_total:
		return
	findings = checks.check_pay_split(*parts)
	if flt(doc.base) and flt(doc.base) != flt(doc.uae_basic) and flt(doc.base) != doc.uae_total:
		findings.append(
			checks.Finding(
				checks.WARN,
				"base_mismatch",
				_("Base {0} is neither the basic wage nor the total of the UAE components ({1})").format(
					doc.base, doc.uae_total
				),
			)
		)
	apply_findings(findings)
