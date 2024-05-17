// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Experience Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width": "50px"
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			
			"width": "50px"
		},
		{
			"fieldname": "group_by_experience",
			"label": __("Group By Experience"),
			"fieldtype": "Check",
			"width": "50px"
		}

	]
};
