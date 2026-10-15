"""Every legal number the app uses, with the article it comes from.

This registry is the single source of truth. The UAE HR Settings doctype is generated from it
(dev/gen_doctypes.py), so each parameter is a setting whose default is the law, and code reads
values through get_param(). Nothing else in the app hardcodes a legal number.

Why settings and not constants: DL 70(7) lets the Cabinet change "the periods, percentages, or
values mentioned herein", so an amendment must be a settings change plus a release note.

Sources: Federal Decree-Law No. 33 of 2021 (DL) and Cabinet Resolution No. 1 of 2022 (CR), MOHRE's
official English booklet dated 2025-10-16. DL 66: where the English and Arabic differ, the Arabic
prevails. See docs/law.md for the quotes.

`favours` says which direction is more generous to the worker. A company may move a setting that
way freely (DL 65(1) lets terms be more beneficial). Moving it the other way, or changing a
parameter with no direction, needs a reference to the amending resolution in the settings.
"""

from dataclasses import dataclass

LOWER = "lower"
HIGHER = "higher"


@dataclass(frozen=True)
class LawParam:
	fieldname: str
	label: str
	default: int
	citation: str
	quote: str
	section: str
	favours: str | None = None
	fieldtype: str = "Int"
	# version of the app that first enforces the rule; later ones are stored now, used later
	enforced_in: str = "0.1"


SECTIONS = {
	"probation": "Probation",
	"notice": "Notice and termination",
	"records": "Records and discipline",
	"leave": "Leave",
	"hours": "Working hours and overtime",
	"gratuity": "End of service",
	"wages": "Wage deductions",
	"calendar": "Calendar and age",
}

PARAMS: tuple[LawParam, ...] = (
	# ---------------- probation
	LawParam(
		"probation_max_months",
		"Maximum probation (months)",
		6,
		"DL 9(1)",
		"a probationary period not exceeding (6) six months",
		"probation",
		LOWER,
	),
	LawParam(
		"probation_employer_notice_days",
		"Employer notice to end probation (days)",
		14,
		"DL 9(1)",
		"in writing fourteen (14) days at least before the date specified",
		"probation",
		HIGHER,
	),
	LawParam(
		"probation_move_notice_months",
		"Worker notice, resigning in probation to join another UAE employer (months)",
		1,
		"DL 9(3)",
		"notify the original employer of the same in writing within not less than one month",
		"probation",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"probation_leave_notice_days",
		"Worker notice, resigning in probation to leave the UAE (days)",
		14,
		"DL 9(4)",
		"notify the employer of the same in writing not less than fourteen (14) days",
		"probation",
		LOWER,
		enforced_in="0.4",
	),
	# ---------------- notice
	LawParam(
		"notice_min_days",
		"Minimum notice period (days)",
		30,
		"DL 43(1)",
		"not less than (30) thirty days and not more than (90) ninety days",
		"notice",
	),
	LawParam(
		"notice_max_days",
		"Maximum notice period (days)",
		90,
		"DL 43(1)",
		"not less than (30) thirty days and not more than (90) ninety days",
		"notice",
	),
	LawParam(
		"job_search_days_per_week",
		"Unpaid job-search days per week during employer notice",
		1,
		"DL 43(5)",
		"one working day without pay per week, in order to search for another job",
		"notice",
		HIGHER,
		enforced_in="0.4",
	),
	LawParam(
		"absence_dismissal_intermittent_days",
		"Dismissal for absence: intermittent days in a year (more than)",
		20,
		"DL 44(8)",
		"more than (20) twenty intermittent days during one year",
		"notice",
		HIGHER,
		enforced_in="0.4",
	),
	LawParam(
		"absence_dismissal_consecutive_days",
		"Dismissal for absence: consecutive days (more than)",
		7,
		"DL 44(8)",
		"or more than (7) seven consecutive days",
		"notice",
		HIGHER,
		enforced_in="0.4",
	),
	LawParam(
		"absconding_report_days",
		"Absence report to the Ministry after consecutive days (more than)",
		7,
		"DL 50(3), CR 28(1)",
		"The absence from work shall have exceeded 7 consecutive days",
		"notice",
		HIGHER,
		enforced_in="0.4",
	),
	LawParam(
		"final_settlement_days",
		"Final settlement paid within (days of contract end)",
		14,
		"DL 53",
		"within (14) fourteen days from the end date of the contract term",
		"notice",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"death_dues_days",
		"Dues on a worker's death paid within (days)",
		10,
		"DL 15(1)",
		"within a period not exceeding (10) ten days from the date of death",
		"notice",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"non_compete_max_years",
		"Maximum non-compete after contract end (years)",
		2,
		"DL 10(1), CR 12(1)",
		"shall not be more than two years from the expiry date of the contract",
		"notice",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"accommodation_vacate_days",
		"Worker vacates employer accommodation within (days)",
		30,
		"DL 16(10)",
		"within a period not exceeding (30) thirty days from the date of end of his service",
		"notice",
		HIGHER,
		enforced_in="0.4",
	),
	# ---------------- records and discipline
	LawParam(
		"file_retention_years",
		"Keep the worker file after end of service (years)",
		2,
		"DL 13(1)",
		"shall not be less than two years after the date of the worker's end of service",
		"records",
		HIGHER,
	),
	LawParam(
		"warning_charge_days",
		"Charge a violation within (days of detection)",
		30,
		"CR 24(4)",
		"detected more than (30) thirty days ago",
		"records",
		LOWER,
	),
	LawParam(
		"warning_penalty_days",
		"Impose a penalty within (days of the investigation ending)",
		60,
		"CR 24(4)",
		"no disciplinary sanction may be imposed more than (60) days after",
		"records",
		LOWER,
	),
	LawParam(
		"suspension_max_days",
		"Maximum unpaid suspension as a penalty (days)",
		14,
		"DL 39(1)(d)",
		"Suspension from work for a period not exceeding (14) fourteen days",
		"records",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"investigation_suspension_max_days",
		"Maximum suspension pending investigation (days)",
		30,
		"DL 40(1)",
		"for a period not exceeding (30) thirty days",
		"records",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"work_regulations_threshold",
		"Work regulations mandatory from (workers)",
		50,
		"DL 13(3), CR 14",
		"establishments that employ 50 or more workers",
		"records",
		LOWER,
		enforced_in="0.4",
	),
	# ---------------- leave
	LawParam(
		"annual_leave_days",
		"Annual leave per year of service (days)",
		30,
		"DL 29(1)(a)",
		"Thirty days for each year of extended service",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"annual_leave_first_year_days_per_month",
		"Annual leave between 6 and 12 months of service (days per month)",
		2,
		"DL 29(1)(b)",
		"Two days for each month if his service term is more than six months",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"annual_leave_carry_forward_pct",
		"Annual leave carry-forward cap (% of annual leave)",
		50,
		"DL 29(5)",
		"may carry forward not more than half of the annual leave",
		"leave",
		HIGHER,
		fieldtype="Percent",
		enforced_in="0.3",
	),
	LawParam(
		"maternity_leave_days",
		"Maternity leave (days)",
		60,
		"DL 30(1)",
		"a maternity leave of (60) sixty days",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"maternity_full_pay_days",
		"Maternity leave on full wage (days)",
		45,
		"DL 30(1)",
		"The first (45) forty-five days with full wage",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"maternity_half_pay_days",
		"Maternity leave on half wage (days)",
		15,
		"DL 30(1)",
		"The following (15) fifteen days with half wage",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"sick_leave_days",
		"Sick leave per year after probation (days)",
		90,
		"DL 31(3)",
		"",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"sick_full_pay_days",
		"Sick leave on full pay (days)",
		15,
		"DL 31(3)(a)",
		"The first (15) fifteen days with full pay",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"sick_half_pay_days",
		"Sick leave on half pay (days)",
		30,
		"DL 31(3)(b)",
		"The following (30) thirty days with half pay",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"bereavement_spouse_days",
		"Bereavement leave, spouse (days)",
		5,
		"DL 32(1)(a)",
		"(5) five days, in case of death of the husband or wife",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"bereavement_relative_days",
		"Bereavement leave, parent, child, sibling, grandchild, grandparent (days)",
		3,
		"DL 32(1)(a)",
		"(3) three days in case of death of the mother, father",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"parental_leave_working_days",
		"Parental leave (working days)",
		5,
		"DL 32(1)(b)",
		"A parental leave for a period of (5) five working days",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"parental_leave_window_months",
		"Parental leave taken within (months of the birth)",
		6,
		"DL 32(1)(b)",
		"within (6) six months from the date of the child birth",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"study_leave_working_days",
		"Study leave per year (working days)",
		10,
		"DL 32(2)",
		"a study leave for a period of (10) ten working days per year",
		"leave",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"study_leave_min_service_years",
		"Study leave after service of (years)",
		2,
		"DL 32(2)",
		"the service term at the employer is not less than two years",
		"leave",
		LOWER,
		enforced_in="0.3",
	),
	# ---------------- hours
	LawParam(
		"max_daily_hours",
		"Maximum normal hours per day",
		8,
		"DL 17(1)",
		"(8) eight hours per day or (48) forty-eight hours per week",
		"hours",
		LOWER,
		enforced_in="0.3",
	),
	LawParam(
		"max_weekly_hours",
		"Maximum normal hours per week",
		48,
		"DL 17(1)",
		"(8) eight hours per day or (48) forty-eight hours per week",
		"hours",
		LOWER,
		enforced_in="0.3",
	),
	LawParam(
		"ramadan_reduction_hours",
		"Ramadan reduction of daily hours",
		2,
		"CR 15(2)",
		"reduced by two hours during the holy month of Ramadan",
		"hours",
		HIGHER,
		enforced_in="0.3",
	),
	LawParam(
		"max_overtime_hours_per_day",
		"Maximum overtime per day (hours)",
		2,
		"DL 19(1)",
		"",
		"hours",
		LOWER,
		enforced_in="0.3",
	),
	LawParam(
		"max_hours_per_3_weeks",
		"Maximum total hours per 3 weeks",
		144,
		"CR 15(3)",
		"shall not exceed (144) one hundred and forty four hours every (3) three weeks",
		"hours",
		LOWER,
		enforced_in="0.3",
	),
	LawParam(
		"overtime_premium_pct",
		"Overtime premium on basic wage (%)",
		25,
		"DL 19(2)",
		"an increase of not less than (25 %) twenty five percent",
		"hours",
		HIGHER,
		fieldtype="Percent",
		enforced_in="0.3",
	),
	LawParam(
		"night_overtime_premium_pct",
		"Overtime premium 22:00-04:00 on basic wage (%)",
		50,
		"DL 19(3)",
		"between 10 pm and 4 am … plus an increase of not less than (50 %) fifty percent of that wage",
		"hours",
		HIGHER,
		fieldtype="Percent",
		enforced_in="0.3",
	),
	LawParam(
		"rest_day_premium_pct",
		"Weekend or public-holiday work premium on basic wage (%)",
		50,
		"DL 19(4), DL 28(2)",
		"not less than (50 %) fifty percent of the basic wage for that day",
		"hours",
		HIGHER,
		fieldtype="Percent",
		enforced_in="0.3",
	),
	# ---------------- gratuity
	LawParam(
		"gratuity_first_years",
		"Gratuity: years paid at the lower rate",
		5,
		"DL 51(2)(a)",
		"for each year of the first five years of service",
		"gratuity",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"gratuity_days_first_years",
		"Gratuity: days of basic wage per year, first years",
		21,
		"DL 51(2)(a)",
		"A wage of (21) twenty-one days for each year",
		"gratuity",
		HIGHER,
		enforced_in="0.4",
	),
	LawParam(
		"gratuity_days_after",
		"Gratuity: days of basic wage per year, after that",
		30,
		"DL 51(2)(b)",
		"A wage of (30) thirty days for each year exceeding such period",
		"gratuity",
		HIGHER,
		enforced_in="0.4",
	),
	LawParam(
		"gratuity_min_service_years",
		"Gratuity: minimum continuous service (years)",
		1,
		"DL 51(2)-(3)",
		"provided that he completed one year of continuous service",
		"gratuity",
		LOWER,
		enforced_in="0.4",
	),
	LawParam(
		"gratuity_cap_years",
		"Gratuity: cap (years of wage)",
		2,
		"DL 51(6)",
		"in its entirety does not exceed two years' wage",
		"gratuity",
		HIGHER,
		enforced_in="0.4",
	),
	# ---------------- wage deductions
	LawParam(
		"overpayment_deduction_pct",
		"Overpayment recovery cap (% of wage)",
		20,
		"DL 25(1)(b)",
		"does not exceed (20%) twenty percent of the wage",
		"wages",
		LOWER,
		fieldtype="Percent",
		enforced_in="0.5",
	),
	LawParam(
		"fine_deduction_pct",
		"Disciplinary fines cap (% of wage)",
		5,
		"DL 25(1)(f)",
		"shall not exceed (5%) five percent of the wage",
		"wages",
		LOWER,
		fieldtype="Percent",
		enforced_in="0.5",
	),
	LawParam(
		"court_debt_deduction_pct",
		"Court-judgment debt cap (% of wage, alimony excepted)",
		25,
		"DL 25(1)(g)",
		"without exceeding a quarter of the wage payable to the worker",
		"wages",
		LOWER,
		fieldtype="Percent",
		enforced_in="0.5",
	),
	LawParam(
		"damage_deduction_days_per_month",
		"Damage deduction cap (days' wage per month)",
		5,
		"DL 25(1)(h)",
		"do not exceed the wage of (5) five days per month",
		"wages",
		LOWER,
		enforced_in="0.5",
	),
	LawParam(
		"total_deduction_pct",
		"All deductions combined cap (% of wage)",
		50,
		"DL 25(2)",
		"may not exceed (50%) fifty percent of the wage",
		"wages",
		LOWER,
		fieldtype="Percent",
		enforced_in="0.5",
	),
	# ---------------- calendar and age
	LawParam(
		"year_days",
		"Days in a year for calculations",
		365,
		"DL 67",
		"shall include (365) three hundred and sixty-five days",
		"calendar",
		enforced_in="0.4",
	),
	LawParam(
		"month_days",
		"Days in a month for calculations",
		30,
		"DL 67",
		"the month represents (30) thirty days",
		"calendar",
		enforced_in="0.4",
	),
	LawParam(
		"min_worker_age",
		"Minimum age for a standard work permit",
		18,
		"CR 7(1)",
		"the worker should be at least 18 years old",
		"calendar",
		enforced_in="0.2",
	),
	LawParam(
		"juvenile_min_age",
		"Minimum age for a juvenile permit",
		15,
		"DL 1, CR 6(1)(g)",
		"a person who has reached 15 years of age but is not over 18 years",
		"calendar",
		enforced_in="0.2",
	),
)

BY_FIELDNAME = {p.fieldname: p for p in PARAMS}


def get_param(fieldname: str):
	"""Current value of a law parameter: the setting if one is stored, else the law default."""
	import frappe

	p = BY_FIELDNAME[fieldname]
	value = frappe.db.get_single_value("UAE HR Settings", fieldname)
	if value in (None, "", 0):
		return p.default
	return value


def describe(p: LawParam) -> str:
	if p.quote:
		return f'Law default {p.default}. {p.citation}: "{p.quote}"'
	return f"Law default {p.default}. {p.citation}."


def less_favourable(p: LawParam, value) -> bool:
	"""True when `value` moves away from the law default in a direction the worker does not benefit from."""
	if value == p.default:
		return False
	if p.favours == LOWER:
		return value > p.default
	if p.favours == HIGHER:
		return value < p.default
	return True
