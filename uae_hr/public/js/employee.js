// Copyright (c) 2026, UAE HR contributors
// License: GNU General Public License v3. See LICENSE

frappe.ui.form.on("Employee", {
	// the same check from the button inside the UAE tab, where HR looks for it
	uae_contract_readiness(frm) {
		if (frm.is_new()) {
			frappe.msgprint(__("Save the employee first."));
			return;
		}
		uae_hr_show_readiness(frm);
	},
	refresh(frm) {
		uae_hr_render_exit_items(frm);
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

// Exit tab: company property still with the worker (rows of Issued Items with no Returned On).
function uae_hr_render_exit_items(frm) {
	const field = frm.get_field("uae_exit_items_html");
	if (!field) return;
	const open = (frm.doc.uae_issued_items || []).filter((r) => r.item_type && !r.returned_on);
	const head = `<label class="control-label">${__("Issued Items to Return")}</label>`;
	if (!open.length) {
		field.$wrapper.html(`${head}<p class="text-muted">${__("All issued items are returned.")}</p>`);
		return;
	}
	const rows = open
		.map(
			(r) =>
				`<tr><td>${frappe.utils.escape_html(r.item_type)}</td><td>${frappe.utils.escape_html(
					r.serial_no || r.description || ""
				)}</td><td>${r.issued_on ? frappe.datetime.str_to_user(r.issued_on) : ""}</td></tr>`
		)
		.join("");
	field.$wrapper.html(
		`${head}<p>${__("{0} items still to return:", [open.length])}</p>
		<table class="table table-sm"><thead><tr><th>${__("Item Type")}</th><th>${__("Serial / Asset No")}</th><th>${__(
			"Issued On"
		)}</th></tr></thead><tbody>${rows}</tbody></table>`
	);
}

frappe.ui.form.on("UAE Issued Item", {
	returned_on: uae_hr_render_exit_items,
	item_type: uae_hr_render_exit_items,
	uae_issued_items_remove: uae_hr_render_exit_items,
});
