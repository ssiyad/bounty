// Copyright (c) 2026, Sabu Siyad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bounty Target", {
	refresh(frm) {
		[
			["Sync Code", "sync_code"],
			["Index Logs", "index_logs"],
			["Index Code", "index_code"],
		].forEach(([label, action]) => {
			frm.add_custom_button(__(label), () => {
				frm.call(action).then(() => {
					frm.refresh();
				});
			});
		});
	},
});
