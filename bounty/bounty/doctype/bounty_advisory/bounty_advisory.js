// Copyright (c) 2026, Sabu Siyad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bounty Advisory", {
	refresh(frm) {
		if (!frm.is_new() && !frm.doc.github_reference) {
			frm.add_custom_button(
				__("Publish to GitHub"),
				() => {
					frappe.confirm(
						__(
							"This will create and publish a security advisory on GitHub. Continue?",
						),
						() => {
							frm.call("publish_to_github").then(() => {
								frm.reload_doc();
							});
						},
					);
				},
			);
		}
	},
});
