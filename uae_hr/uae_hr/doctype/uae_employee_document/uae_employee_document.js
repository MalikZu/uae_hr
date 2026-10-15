// Copyright (c) 2026, UAE HR contributors
// License: GNU General Public License v3. See LICENSE

frappe.ui.form.on("UAE Employee Document", {
	refresh(frm) {
		if (frm.is_new()) return;
		if (frm.doc.status === "Unverified" && frappe.user.has_role(["HR Manager", "System Manager"])) {
			frm.add_custom_button(__("Verify"), () =>
				frm.call("verify").then(() => frm.reload_doc())
			).addClass("btn-primary");
		}
		if (frm.doc.status !== "Unverified" && frappe.user.has_role(["HR Manager", "System Manager"])) {
			frm.add_custom_button(__("Reopen"), () =>
				frappe.confirm(
					__("Reopen this document so it can be corrected? The Employee keeps its current values until you verify it again."),
					() => frm.call("reopen").then(() => frm.reload_doc())
				)
			);
		}
		if (frm.doc.status !== "Cancelled") {
			frm.add_custom_button(__("Mark Cancelled"), () => {
				frappe.prompt(
					{ fieldname: "reason", label: __("Reason"), fieldtype: "Small Text" },
					({ reason }) => frm.call("cancel_document", { reason }).then(() => frm.reload_doc()),
					__("Mark Cancelled")
				);
			});
		}
	},
});
