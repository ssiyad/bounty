app_name = "bounty"
app_title = "Bounty"
app_publisher = "Sabu Siyad"
app_description = "Manage confidential reports, issues and rewards"
app_email = "hello@ssiyad.com"
app_license = "gpl-3.0"

website_route_rules = [
	{
		"from_route": "/b/<path:app_path>",
		"to_route": "b",
	},
]

permission_query_conditions = {
	"Bounty Hunter": "bounty.bounty.doctype.bounty_hunter.bounty_hunter.permission_query",
}

has_permission = {
	"Bounty Hunter": "bounty.bounty.doctype.bounty_hunter.bounty_hunter.has_permission",
}
