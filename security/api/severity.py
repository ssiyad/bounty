import frappe


@frappe.whitelist(allow_guest=True)
def get_severities():
	return [
		{
			"value": "Informational",
			"label": "Informational",
			"color": "gray",
		},
		{
			"value": "Low",
			"label": "Low",
			"color": "green",
		},
		{
			"value": "Medium",
			"label": "Medium",
			"color": "blue",
		},
		{
			"value": "High",
			"label": "High",
			"color": "orange",
		},
		{
			"value": "Critical",
			"label": "Critical",
			"color": "red",
		},
	]
