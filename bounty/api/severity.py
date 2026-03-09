import frappe


@frappe.whitelist()
def get_severities():
	return [
		{
			"value": "informational",
			"label": "Informational",
			"color": "gray",
		},
		{
			"value": "low",
			"label": "Low",
			"color": "green",
		},
		{
			"value": "medium",
			"label": "Medium",
			"color": "blue",
		},
		{
			"value": "high",
			"label": "High",
			"color": "orange",
		},
		{
			"value": "critical",
			"label": "Critical",
			"color": "red",
		},
	]
