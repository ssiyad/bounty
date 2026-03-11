// Copyright (c) 2026, Sabu Siyad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bounty Report", {
	refresh(frm) {
		frm.add_custom_button("Create Advisory", () => {
			if (!frm.doc.target) {
				frappe.throw(__("Target is required to create an advisory."));
			}
			if (frm.doc.status !== "Accepted") {
				frappe.throw(__("Report must be accepted to create an advisory."));
			}
			frappe.new_doc("Bounty Advisory", {}, (doc) => {
				doc.report = frm.doc.name;
				doc.target = frm.doc.target;
				doc.title = frm.doc.title;
				doc.content = frm.doc.content;
				doc.published = 0;
			});
		});

		frm.timeline.timeline_actions_wrapper.find(".reply-btn").remove();
		frm.timeline
			.add_action_button(
				"Reply",
				() => {
					const d = new frappe.ui.Dialog({
						title: "Reply",
						fields: [
							{
								fieldname: "info",
								fieldtype: "HTML",
								options:
									'<p class="text-muted">What would you like to tell the reporter?</p>',
							},
							{
								fieldname: "content",
								fieldtype: "Small Text",
								label: "Message",
								reqd: 1,
								placeholder: "Jot down your thoughts...",
							},
						],
						primary_action_label: "Send",
						primary_action(values) {
							frm.call("reply", { content: values.content }).then(() => {
								d.hide();
								frm.refresh();
							});
						},
					});
					d.show();
				},
				"es-line-add",
				"btn-secondary",
			)
			.addClass("reply-btn");
	},
});
