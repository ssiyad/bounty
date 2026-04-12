export interface Advisory {
	name: string;
	title: string;
	frappe_reference: string;
	severity: string;
	target: string;
	published_on: string;
	reported_by?: string;
}