// Copyright (c) 2026, Sabu Siyad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bounty Report", {
	refresh(frm) {
		frm.add_custom_button("Create Advisory", () => {
			frm.call("create_advisory").then(() => {
				frm.refresh();
			});
		});
	},
});
