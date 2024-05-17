// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Salary Increment Year To Year"] = {
	"filters": [
		// # ... Your existing filters
		{
			'fieldname': "employee",
			'label': "Employee",
			'fieldtype': "Link",
			'options': "Employee"
		},

		{
			'fieldname': "designation",
			'label': __("Designation"),
			'fieldtype': "Link",
			'options': "Designation"
		},
		{
			'fieldname': "department",
			'label': __("Department"),
			'fieldtype': "Link",
			'options': "Department"
		},
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": [
				{ "value": 1, "label": __("Jan") },
				{ "value": 2, "label": __("Feb") },
				{ "value": 3, "label": __("Mar") },
				{ "value": 4, "label": __("Apr") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("Aug") },
				{ "value": 9, "label": __("Sep") },
				{ "value": 10, "label": __("Oct") },
				{ "value": 11, "label": __("Nov") },
				{ "value": 12, "label": __("Dec") },
			],
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		},
		{
			"fieldname": "payroll_period",
			"label": __("Payroll Period"),
			"fieldtype": "Link",
			"options": "Payroll Period",
			"default": erpnext.utils.get_fiscal_year()
		},

	]
};