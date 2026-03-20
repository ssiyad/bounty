app_name = "security"
app_title = "Security"
app_publisher = "Sabu Siyad"
app_description = "Manage confidential reports, issues and rewards"
app_email = "hello@ssiyad.com"
app_license = "gpl-3.0"

website_route_rules = [
	{
		"from_route": "/s/<path:app_path>",
		"to_route": "s",
	},
]

permission_query_conditions = {
	"FS Draft": "security.frappe_security.doctype.bounty_draft.bounty_draft.permission_query",
	"FS Hunter": "security.frappe_security.doctype.bounty_hunter.bounty_hunter.permission_query",
}

has_permission = {
	"FS Draft": "security.frappe_security.doctype.bounty_draft.bounty_draft.has_permission",
	"FS Hunter": "security.frappe_security.doctype.bounty_hunter.bounty_hunter.has_permission",
}

doc_events = {
	"User": {
		"after_insert": "security.frappe_security.doctype.bounty_hunter.bounty_hunter.create_hunter",
	}
}
