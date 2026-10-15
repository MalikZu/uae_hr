app_name = "uae_hr"
app_title = "UAE HR"
app_publisher = "UAE HR contributors"
app_description = "UAE private-sector labour law for Frappe HR: employee documents, expiry reminders, pay components and cited legal checks"
app_email = "6082784+MalikZu@users.noreply.github.com"
app_license = "gpl-3.0"

required_apps = ["frappe/erpnext", "frappe/hrms"]

before_install = "uae_hr.install.before_install"
after_install = "uae_hr.install.after_install"
before_migrate = "uae_hr.install.before_migrate"
after_migrate = "uae_hr.install.after_migrate"
before_uninstall = "uae_hr.install.before_uninstall"
before_tests = "uae_hr.tests.utils.before_tests"

doctype_js = {"Employee": "public/js/employee.js"}

doc_events = {
	"Employee": {"validate": "uae_hr.employee.validate"},
	"Salary Structure Assignment": {"validate": "uae_hr.salary.validate_assignment"},
	"File": {
		"after_insert": "uae_hr.uae_hr.doctype.uae_employee_document.uae_employee_document.make_files_private"
	},
}

override_doctype_dashboards = {"Employee": "uae_hr.employee.get_dashboard_data"}

scheduler_events = {
	"daily": ["uae_hr.uae_hr.doctype.uae_employee_document.uae_employee_document.mark_expired"],
}
