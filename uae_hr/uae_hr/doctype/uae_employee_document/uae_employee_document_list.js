// Copyright (c) 2026, UAE HR contributors
// License: GNU General Public License v3. See LICENSE

frappe.listview_settings["UAE Employee Document"] = {
	get_indicator(doc) {
		const colors = { Unverified: "orange", Current: "green", Superseded: "gray", Expired: "red", Cancelled: "darkgray" };
		return [__(doc.status), colors[doc.status] || "gray", "status,=," + doc.status];
	},
	onload(listview) {
		if (!frappe.user.has_role(["HR Manager", "System Manager"])) return;
		listview.page.add_action_item(__("Verify"), () => {
			const names = listview.get_checked_items(true);
			if (!names.length) return;
			frappe.call({
				method: "uae_hr.uae_hr.doctype.uae_employee_document.uae_employee_document.verify_many",
				args: { names },
				freeze: true,
				callback({ message }) {
					const failed = message.filter((r) => !r.ok);
					const warned = message.filter((r) => r.ok && r.warnings.length);
					let html = __("{0} verified.", [message.length - failed.length]);
					if (warned.length) html += "<br>" + warned.map((r) => `<b>${r.name}</b>: ${r.warnings.join("; ")}`).join("<br>");
					if (failed.length) html += "<br>" + failed.map((r) => `<b>${r.name}</b>: ${r.error}`).join("<br>");
					frappe.msgprint({ title: __("Verify"), message: html, indicator: failed.length ? "orange" : "green" });
					listview.refresh();
				},
			});
		});
	},
};
