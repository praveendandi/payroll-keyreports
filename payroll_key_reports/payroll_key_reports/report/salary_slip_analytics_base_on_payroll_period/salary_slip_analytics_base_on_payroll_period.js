// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Slip Analytics Base On Payroll Period"] = {
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
			"fieldname":"payroll_period",
			"label": __("Payroll Period"),
			"fieldtype": "Link",
			"options": "Payroll Period",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
		},
	],
	// onload: () => {
    //     frappe.call({
    //         type: "GET",
    //         method: "hrms.hr.utils.get_leave_period",
    //         args: {
    //             "from_date": frappe.defaults.get_default("year_start_date"),
    //             "to_date": frappe.defaults.get_default("year_end_date"),
    //             "company": frappe.defaults.get_user_default("Company")
    //         },
    //         freeze: true,
    //         callback: (data) => {
    //             frappe.query_report.set_filter_value("from_date", data.message[0].from_date);
    //             frappe.query_report.set_filter_value("to_date", data.message[0].to_date);
    //         }
    //     });
    // }
};
