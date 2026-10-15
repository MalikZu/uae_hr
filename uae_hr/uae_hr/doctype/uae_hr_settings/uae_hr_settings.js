// Copyright (c) 2026, UAE HR contributors
// License: GNU General Public License v3. See LICENSE

frappe.ui.form.on("UAE HR Settings", {
	refresh(frm) {
		frm.add_custom_button(__("Reset Law Values to the Law"), () => {
			frappe.confirm(__("Set every law parameter back to the value in the 2022 law?"), () =>
				frappe
					.call("uae_hr.uae_hr.doctype.uae_hr_settings.uae_hr_settings.reset_to_law_defaults")
					.then(() => frm.reload_doc())
			);
		});
	},
});
