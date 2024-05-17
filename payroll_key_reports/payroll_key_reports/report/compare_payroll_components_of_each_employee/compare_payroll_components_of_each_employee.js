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
		// {
		// 	"fieldname":"start_date",
		// 	"label":__("Start Date"),
		// 	"fieldtype":"Date",
		// 	"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		// 	"width": "80"
		// },
		// {
		// 	"fieldname":"end_date",
		// 	"label":__("End Date"),
		// 	"fieldtype":"Date",
		// 	"default": frappe.datetime.add_months(frappe.datetime.get_today(),0),
		// 	"width": "80"
		// },
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			// "depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
		},
		// {
		// 	"fieldname":"to_fiscal_year",
		// 	"label": __("End Year"),
		// 	"fieldtype": "Link",
		// 	"options": "Fiscal Year",
		// 	"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
		// 	// "depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
		// },
		{
			"fieldname":"select_month",
			"label": __("Select Month"),
			"fieldtype": "Select",
			"options": ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
			// "default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			// "depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
		},
	]
};

erpnext.utils.add_dimensions('Compare Payroll Components Of Each Employee', 15)
