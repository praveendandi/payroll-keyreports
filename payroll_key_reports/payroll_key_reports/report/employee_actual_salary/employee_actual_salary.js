// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Actual Salary"] = {
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
			"fieldname": "salary_structure",
			"label": __("Salary Structure"),
			"fieldtype": "Link",
			"options": "Salary Structure",
			"width": "50px"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": "50px"
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "50px"
		}

	]
};
