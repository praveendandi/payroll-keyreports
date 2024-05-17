// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Current Salary Structure With Bonus"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_defaults("Company")
		},
		{
			"fieldname": "employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "designation",
			"label": "Designation",
			"fieldtype": "Link",
			"options": "Designation"
		},
		{
			"fieldname": "department",
			"label": "Department",
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "payroll_period",
			"label": __("Payroll Period"),
			"fieldtype": "Link",
			"options": "Payroll Period",
			"default": erpnext.utils.get_fiscal_year
		},
	],
};

