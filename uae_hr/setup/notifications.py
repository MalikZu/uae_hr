"""Expiry reminders as standard Frappe Notifications (plan 3.4).

One Notification per lead time in use ("Days Before" on UAE Employee Document.expiry_date). Each
document carries its own reminder days (from its type, or the settings default), and the condition
fires only the notifications whose lead time is in that list. Lead times come from data, so they
are generated here rather than shipped as fixtures.
"""

import frappe

from uae_hr.utils import parse_days, reminder_days_for

PREFIX = "UAE HR: document expires in "
MODULE = "UAE HR"


def wanted_days():
	days = set(
		parse_days(frappe.db.get_single_value("UAE HR Settings", "default_reminder_days") or "60,30,7")
	)
	for value in frappe.get_all(
		"UAE Document Type", filters={"enabled": 1, "has_expiry": 1}, pluck="reminder_days"
	):
		days.update(parse_days(value))
	return sorted(days, reverse=True)


def notification_values(days, copy_hr):
	recipients = [{"receiver_by_role": "UAE PRO"}]
	if copy_hr:
		recipients.append({"receiver_by_role": "HR Manager"})
	return {
		"subject": f"{{{{ doc.document_type }}}} of {{{{ doc.employee_name }}}} expires in {days} days ({{{{ doc.expiry_date }}}})",
		"document_type": "UAE Employee Document",
		"event": "Days Before",
		"date_changed": "expiry_date",
		"days_in_advance": days,
		"channel": "Email",
		"send_system_notification": 1,
		"condition": f'doc.status == "Current" and "{days}" in (doc.reminder_days or "").split(",")',
		"message": (
			f"<p>{{{{ doc.document_type }}}} <b>{{{{ doc.document_number or '' }}}}</b> of "
			f"<b>{{{{ doc.employee_name }}}}</b> ({{{{ doc.employee }}}}) expires on <b>{{{{ doc.expiry_date }}}}</b>, "
			f"in {days} days.</p><p>Start the renewal, then record and verify the new document.</p>"
		),
		"module": MODULE,
		"is_standard": 0,
		"recipients": recipients,
	}


def sync_notifications():
	copy_hr = frappe.db.get_single_value("UAE HR Settings", "copy_hr_manager")
	copy_hr = 1 if copy_hr is None else copy_hr
	wanted = set(wanted_days())
	for days in wanted:
		_upsert(PREFIX + f"{days} days", notification_values(days, copy_hr))
	for name, enabled in frappe.get_all(
		"Notification", filters={"name": ("like", PREFIX + "%")}, fields=["name", "enabled"], as_list=True
	):
		days = int(name[len(PREFIX) :].split()[0])
		if days not in wanted and enabled:
			frappe.db.set_value("Notification", name, "enabled", 0)


def _upsert(name, values):
	recipients = values.pop("recipients")
	if not frappe.db.exists("Notification", name):
		doc = frappe.get_doc(
			{"doctype": "Notification", "name": name, "enabled": 1, **values, "recipients": recipients}
		)
		doc.flags.ignore_permissions = True
		doc.insert()
		return
	doc = frappe.get_doc("Notification", name)
	current = {k: doc.get(k) for k in values}
	current_recipients = [{"receiver_by_role": r.receiver_by_role} for r in doc.recipients]
	if current == values and current_recipients == recipients and doc.enabled:
		return
	doc.update(values)
	doc.enabled = 1
	doc.set("recipients", recipients)
	doc.flags.ignore_permissions = True
	doc.save()


def refresh_reminder_days():
	"""The settings default changed: recompute every document's reminder days, then the notifications."""
	for dtype in frappe.get_all("UAE Document Type", fields=["name", "has_expiry"]):
		days = reminder_days_for(dtype.name) if dtype.has_expiry else ""
		frappe.db.set_value(
			"UAE Employee Document",
			{"document_type": dtype.name, "reminder_days": ("!=", days)},
			"reminder_days",
			days,
			update_modified=False,
		)
	sync_notifications()
