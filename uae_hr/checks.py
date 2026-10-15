"""Pure checks: no database access, so each legal rule is unit-testable on its own.

Every function returns a list of Finding. `block` findings stop a save, `warn` findings are shown
to the user and listed by the import checker. Limits are passed in by the caller (from law.get_param),
never hardcoded here.
"""

import re
from dataclasses import dataclass
from datetime import date

from frappe import _
from frappe.utils import add_months, date_diff, getdate

BLOCK = "block"
WARN = "warn"


@dataclass
class Finding:
	level: str
	code: str
	message: str
	citation: str = ""

	def text(self):
		return f"{self.message} ({self.citation})" if self.citation else self.message


def blocks(findings):
	return [f for f in findings if f.level == BLOCK]


# ---------------------------------------------------------------- Emirates ID


def eid_digits(value: str | None) -> str:
	return re.sub(r"\D", "", value or "")


def format_eid(value: str | None) -> str | None:
	"""784198012345678 -> 784-1980-1234567-8. Returns None when it is not 15 digits."""
	d = eid_digits(value)
	if len(d) != 15:
		return None
	return f"{d[:3]}-{d[3:7]}-{d[7:14]}-{d[14]}"


def luhn_ok(digits: str) -> bool:
	total = 0
	for i, ch in enumerate(reversed(digits)):
		n = int(ch)
		if i % 2 == 1:
			n *= 2
			if n > 9:
				n -= 9
		total += n
	return total % 10 == 0


def check_emirates_id(value: str | None, date_of_birth=None) -> list[Finding]:
	"""Format 784-YYYY-NNNNNNN-C: country code 784, birth year, serial, Luhn check digit."""
	if not value:
		return []
	d = eid_digits(value)
	if len(d) != 15 or not d.startswith("784"):
		return [
			Finding(
				WARN, "eid_format", _("Emirates ID {0} is not in the format 784-YYYY-NNNNNNN-C").format(value)
			)
		]
	out = []
	if not luhn_ok(d):
		out.append(
			Finding(
				WARN, "eid_check_digit", _("Emirates ID {0}: the check digit does not match").format(value)
			)
		)
	if date_of_birth and int(d[3:7]) != getdate(date_of_birth).year:
		out.append(
			Finding(
				WARN,
				"eid_birth_year",
				_("Emirates ID {0}: year {1} does not match the date of birth {2}").format(
					value, d[3:7], getdate(date_of_birth)
				),
			)
		)
	return out


# ---------------------------------------------------------------- IBAN


def normalize_iban(value: str | None) -> str:
	return re.sub(r"\s", "", value or "").upper()


def iban_checksum_ok(iban: str) -> bool:
	"""ISO 13616 mod-97 check."""
	if len(iban) < 5 or not iban.isalnum():
		return False
	rearranged = iban[4:] + iban[:4]
	number = "".join(str(int(ch, 36)) for ch in rearranged)
	return int(number) % 97 == 1


def uae_iban_parts(iban: str) -> tuple[str, str] | None:
	"""AEkk BBB AAAAAAAAAAAAAAAA -> (bank code, 16-digit account). None when not a UAE IBAN."""
	iban = normalize_iban(iban)
	if not re.fullmatch(r"AE\d{21}", iban):
		return None
	return iban[4:7], iban[7:]


def check_iban(value: str | None) -> list[Finding]:
	if not value:
		return []
	iban = normalize_iban(value)
	if iban.startswith("AE") and not re.fullmatch(r"AE\d{21}", iban):
		return [
			Finding(WARN, "iban_format", _("IBAN {0}: a UAE IBAN is AE followed by 21 digits").format(value))
		]
	if not iban_checksum_ok(iban):
		return [
			Finding(
				WARN,
				"iban_checksum",
				_("IBAN {0}: the check digits are wrong, the number has a typo").format(value),
			)
		]
	return []


# ---------------------------------------------------------------- MOHRE person code


def check_person_code(value: str | None) -> list[Finding]:
	if value and not re.fullmatch(r"\d{14}", value.strip()):
		return [Finding(WARN, "person_code", _("MOHRE person code {0} should be 14 digits").format(value))]
	return []


# ---------------------------------------------------------------- probation (DL 9)


def check_probation(months, max_months, date_of_joining=None, final_confirmation_date=None) -> list[Finding]:
	out = []
	if months and months > max_months:
		out.append(
			Finding(
				BLOCK,
				"probation_max",
				_("Probation of {0} months is longer than the legal maximum of {1} months").format(
					months, max_months
				),
				"DL 9(1)",
			)
		)
	if months and months < 0:
		out.append(Finding(BLOCK, "probation_negative", _("Probation cannot be negative")))
	if date_of_joining and final_confirmation_date:
		limit = getdate(add_months(date_of_joining, max_months))
		if getdate(final_confirmation_date) > limit:
			out.append(
				Finding(
					BLOCK,
					"probation_end",
					_("Probation ends on {0}, later than {1} months after joining ({2})").format(
						getdate(final_confirmation_date), max_months, limit
					),
					"DL 9(1)",
				)
			)
	return out


def probation_end(date_of_joining, months) -> date | None:
	"""DL 9(1) counts probation 'from the date of commencement of work'."""
	if not date_of_joining or not months:
		return None
	return getdate(add_months(date_of_joining, months))


# ---------------------------------------------------------------- notice (DL 43)


def check_notice(days, min_days, max_days) -> list[Finding]:
	"""Empty means not set yet (contract readiness lists it). A set value must sit in the legal range."""
	if days in (None, "", 0):
		return []
	if days < min_days or days > max_days:
		return [
			Finding(
				BLOCK,
				"notice_range",
				_("Notice of {0} days is outside the legal range of {1} to {2} days").format(
					days, min_days, max_days
				),
				"DL 43(1)",
			)
		]
	return []


# ---------------------------------------------------------------- records (DL 13(1))


def retention_until(relieving_date, years) -> date | None:
	if not relieving_date:
		return None
	return getdate(add_months(relieving_date, 12 * years))


def check_retention(employee_status, relieving_date, years, today) -> list[Finding]:
	"""A worker's file is kept for at least `years` after the end of service."""
	if employee_status != "Left":
		return []
	until = retention_until(relieving_date, years)
	if until is None:
		return [
			Finding(
				BLOCK,
				"retention_no_date",
				_(
					"This employee has left but has no relieving date, so the {0}-year retention period cannot be checked"
				).format(years),
				"DL 13(1)",
			)
		]
	if getdate(today) < until:
		return [
			Finding(
				BLOCK,
				"retention",
				_("The worker file must be kept until {0}, {1} years after the end of service").format(
					until, years
				),
				"DL 13(1)",
			)
		]
	return []


# ---------------------------------------------------------------- disciplinary timing (CR 24)


def check_warning_timing(
	detected_on, charged_on, investigation_closed_on, issue_date, charge_days, penalty_days
) -> list[Finding]:
	out = []
	if detected_on and charged_on:
		if getdate(charged_on) < getdate(detected_on):
			out.append(
				Finding(
					BLOCK,
					"charge_before_detection",
					_("The charge date is before the violation was detected"),
				)
			)
		elif date_diff(charged_on, detected_on) > charge_days:
			out.append(
				Finding(
					WARN,
					"charge_late",
					_(
						"The charge was given {0} days after the violation was detected; the limit is {1} days"
					).format(date_diff(charged_on, detected_on), charge_days),
					"CR 24(4)",
				)
			)
	if charged_on and investigation_closed_on and getdate(investigation_closed_on) < getdate(charged_on):
		out.append(
			Finding(
				BLOCK,
				"investigation_before_charge",
				_("The investigation closed before the charge was given"),
			)
		)
	if investigation_closed_on and issue_date:
		if getdate(issue_date) < getdate(investigation_closed_on):
			out.append(
				Finding(
					BLOCK,
					"penalty_before_investigation",
					_("A penalty cannot be issued before the investigation has closed"),
					"CR 24(3)",
				)
			)
		elif date_diff(issue_date, investigation_closed_on) > penalty_days:
			out.append(
				Finding(
					WARN,
					"penalty_late",
					_(
						"The warning is issued {0} days after the investigation closed; the limit is {1} days"
					).format(date_diff(issue_date, investigation_closed_on), penalty_days),
					"CR 24(4)",
				)
			)
	return out


# ---------------------------------------------------------------- service length


def service_length(start, end) -> tuple[int, int, int]:
	"""Calendar years, months and days from start to end, both inclusive of the start day."""
	start, end = getdate(start), getdate(end)
	if end < start:
		return 0, 0, 0
	years = end.year - start.year
	months = end.month - start.month
	days = end.day - start.day
	if days < 0:
		months -= 1
		prev = getdate(add_months(end, -1))
		import calendar

		days += calendar.monthrange(prev.year, prev.month)[1]
	if months < 0:
		years -= 1
		months += 12
	return years, months, days


def format_service(start, end) -> str:
	y, m, d = service_length(start, end)
	return _("{0} years, {1} months, {2} days").format(y, m, d)


# ---------------------------------------------------------------- death nominee (DL 15(2), DL 1)

FAMILY_RELATIONS = ("Spouse", "Son", "Daughter")


def check_nominee(nominee, relation) -> list[Finding]:
	if nominee and not relation:
		return [Finding(WARN, "nominee_relation", _("Give the nominee's relation to the worker"), "DL 15(2)")]
	if relation and relation not in FAMILY_RELATIONS:
		return [
			Finding(
				BLOCK,
				"nominee_family",
				_("The nominee must be a member of the worker's family: spouse, son or daughter"),
				"DL 1, DL 15(2)",
			)
		]
	return []


# ---------------------------------------------------------------- issued items (DL 13(2))

OFFICIAL_DOCUMENT_PATTERNS = (
	r"\bpassport",
	r"emirates\s*id",
	r"\bvisa\b(?!\s*card)",
	r"labou?r\s*card",
	r"work\s*permit",
	r"residen(ce|cy)\s*(visa|permit)",
)


def check_issued_item_type(name: str) -> list[Finding]:
	lowered = (name or "").lower()
	if any(re.search(p, lowered) for p in OFFICIAL_DOCUMENT_PATTERNS):
		return [
			Finding(
				BLOCK,
				"withheld_document",
				_(
					"An official document cannot be an issued item: the employer may not withhold the worker's official documents. "
					"Keep a scan as a UAE Employee Document instead"
				),
				"DL 13(2)",
			)
		]
	return []


# ---------------------------------------------------------------- pay components (DL 1, DL 51(5))


def check_pay_split(basic, housing, transport, other) -> list[Finding]:
	allowances = (housing or 0) + (transport or 0) + (other or 0)
	if allowances and not basic:
		return [
			Finding(
				WARN,
				"no_basic",
				_(
					"Allowances are set but the basic wage is empty. Gratuity, overtime and leave pay are calculated on the basic wage"
				),
				"DL 1, DL 51(5)",
			)
		]
	if any(v and v < 0 for v in (basic, housing, transport, other)):
		return [Finding(BLOCK, "negative_pay", _("Pay components cannot be negative"))]
	return []
