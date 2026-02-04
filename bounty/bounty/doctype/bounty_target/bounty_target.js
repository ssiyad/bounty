// Copyright (c) 2026, Sabu Siyad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bounty Target", {
	refresh(frm) {
		[["↓", "Get Code", "get_code"]].forEach(([icon, label, action]) => {
			frm.add_custom_button(icon + " " + __(label), () => {
				frm.call(action).then(() => {
					frm.refresh();
				});
			});
		});
	},
});
