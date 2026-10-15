// Copyright (c) 2026, UAE HR contributors
// License: GNU General Public License v3. See LICENSE

frappe.ui.form.on("Employee", {
	refresh(frm) {
		if (frm.is_new()) return;
		frappe.call({
			method: "uae_hr.employee.get_form_context",
			args: { employee: frm.doc.name },
			callback({ message: ctx }) {
				if (!ctx) return;
				if (!ctx.covered) {
					frm.set_intro(__("UAE HR checks are off for this company (DIFC, ADGM or outside the UAE)."), "blue");
					return;
				}
				const end = frm.doc.final_confirmation_date;
				if (end && frappe.datetime.get_diff(end, frappe.datetime.get_today()) >= 0) {
					frm.set_intro(
						__("In probation until {0}. To end it early, give at least {1} days' written notice (DL 9(1)).", [
							frappe.datetime.str_to_user(end),
							ctx.probation_employer_notice_days,
						]),
						"yellow"
					);
				}
				frm.add_custom_button(__("Contract Readiness"), () => uae_hr_show_readiness(frm), __("UAE"));
				frm.add_custom_button(
					__("Documents"),
					() => frappe.set_route("List", "UAE Employee Document", { employee: frm.doc.name }),
					__("UAE")
				);
			},
		});
	},
});

function uae_hr_show_readiness(frm) {
	frappe.call({
		method: "uae_hr.readiness.get_contract_readiness",
		args: { employee: frm.doc.name },
		callback({ message: r }) {
			const rows = r.items
				.map((i) => {
					const mark = i.manual ? "&#9675;" : i.ok ? "&#10003;" : "&#10007;";
					const color = i.manual ? "text-muted" : i.ok ? "text-success" : "text-danger";
					const hint = !i.ok && i.hint ? `<div class="text-muted small">${frappe.utils.escape_html(i.hint)}</div>` : "";
					return `<tr><td class="${color}">${mark}</td><td>${frappe.utils.escape_html(i.item)}${hint}</td><td class="text-muted small">${frappe.utils.escape_html(i.citation)}</td></tr>`;
				})
				.join("");
			const head = r.ready
				? __("Everything CR 10(1) asks for is on the record.")
				: __("{0} items missing before the MOHRE contract can be prepared.", [r.missing]);
			frappe.msgprint({
				title: __("Contract Readiness"),
				message: `<p>${head}</p><table class="table table-sm">${rows}</table>`,
				wide: true,
			});
		},
	});
}
