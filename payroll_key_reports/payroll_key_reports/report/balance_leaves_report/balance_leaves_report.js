// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance Leaves Report"] = {
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
				"fieldname": "employee",
				"label": __("Employee"),
				"fieldtype": "Link",
				"options": "Employee",
				// "default": frappe.defaults.get_user_default("employee"),
			},
			// {
			// 	"fieldname":"payroll_period",
			// 	"label": __("Payroll Period"),
			// 	"fieldtype": "Link",
			// 	"options": "Fiscal Year",
			// 	"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			// },
			{
				"fieldname":"leave_type",
				"label": __("Leave Type"),
				"fieldtype": "Link",
				"options": "Leave Type",
				"default": "Casual Leave",
			},


	],
	onload :()=>{
		let user_id = frappe.session.user

		let emp = frappe.db.get_list('Employee',{fields:['user_id','name']},{filters:{"user_id":user_id}}).then((res) => {
			frappe.query_report.set_filter_value('employee',res[0]['name'])
		})
	}

};
