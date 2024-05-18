// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compare Payroll Components Of Each Employee"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Payroll Period"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
		},
		{
			"fieldname":"select_month",
			"label": __("Select Month"),
			"fieldtype": "Select",
			"options": ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],

		},
	]
};

erpnext.utils.add_dimensions('Compare Payroll Components Of Each Employee', 15)
