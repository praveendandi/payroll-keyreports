// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Revision"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width":"50px"
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width":"50px"
		},
		{
			"fieldname":"start_payroll_period",
			"label": __("Start Payroll Period"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			// "depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
		},
	]
};
