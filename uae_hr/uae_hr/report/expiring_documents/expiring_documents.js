// Copyright (c) 2026, UAE HR contributors
// License: GNU General Public License v3. See LICENSE

frappe.query_reports["Expiring Documents"] = {
	filters: [
		{ fieldname: "days", label: __("Expiring Within (days)"), fieldtype: "Int", default: 90 },
		{ fieldname: "include_overdue", label: __("Include Overdue"), fieldtype: "Check", default: 1 },
		{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
		{ fieldname: "document_type", label: __("Document Type"), fieldtype: "Link", options: "UAE Document Type" },
		{ fieldname: "employee", label: __("Employee"), fieldtype: "Link", options: "Employee" },
		{ fieldname: "include_inactive", label: __("Include Inactive Employees"), fieldtype: "Check", default: 0 },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "state" && data) {
			const color = data.days_left < 0 ? "red" : data.days_left <= 30 ? "orange" : "blue";
			value = `<span class="indicator-pill ${color}">${value}</span>`;
		}
		return value;
	},
};
