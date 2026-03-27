app_name = "security"
app_title = "Security"
app_publisher = "Sabu Siyad"
app_description = "Comprehensive system to manage security related affairs."
app_email = "hello@ssiyad.com"
app_license = "gpl-3.0"

website_route_rules = [
	{
		"from_route": "/s/<path:app_path>",
		"to_route": "s",
	},
]

permission_query_conditions = {
	"FS Draft": "security.frappe_security.doctype.fs_draft.fs_draft.permission_query",
	"FS Hunter": "security.frappe_security.doctype.fs_hunter.fs_hunter.permission_query",
	"FS Notification": "security.frappe_security.doctype.fs_notification.fs_notification.permission_query",
	"FS Report": "security.frappe_security.doctype.fs_report.fs_report.permission_query",
}

has_permission = {
	"FS Draft": "security.frappe_security.doctype.fs_draft.fs_draft.has_permission",
	"FS Hunter": "security.frappe_security.doctype.fs_hunter.fs_hunter.has_permission",
	"FS Notification": "security.frappe_security.doctype.fs_notification.fs_notification.has_permission",
	"FS Report": "security.frappe_security.doctype.fs_report.fs_report.has_permission",
}

doc_events = {
	"User": {
		"after_insert": "security.frappe_security.doctype.fs_hunter.fs_hunter.create_hunter",
	}
}
