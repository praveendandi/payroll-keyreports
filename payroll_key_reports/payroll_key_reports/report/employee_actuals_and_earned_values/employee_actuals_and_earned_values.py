# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data



import frappe
from frappe import _
from frappe.utils import flt
import re

import erpnext

salary_slip = frappe.qb.DocType("Salary Slip")
salary_detail = frappe.qb.DocType("Salary Detail")
salary_component = frappe.qb.DocType("Salary Component")


def execute(filters=None):
	final_data, columns_earning, columns_deduction = get_data(filters)
	if not filters:
		filters = {}

	currency = None
	if filters.get("currency"):
		currency = filters.get("currency")
	company_currency = erpnext.get_company_currency(filters.get("company"))

	salary_slips = get_salary_slips(filters, company_currency)
	if not salary_slips:
		return [], []

	earning_types, ded_types = get_earning_and_deduction_types(salary_slips)
	columns = get_columns(earning_types, ded_types, final_data)

	ss_earning_map = get_salary_slip_details(salary_slips, currency, company_currency, "earnings")
	ss_ded_map = get_salary_slip_details(salary_slips, currency, company_currency, "deductions")

	doj_map = get_employee_doj_map()

	data = []
	for ss in salary_slips:
		row = {
			"salary_slip_id": ss.name,
			"employee": ss.employee,
			"employee_name": ss.employee_name,
			"data_of_joining": doj_map.get(ss.employee),
			"branch": ss.branch,
			"department": ss.department,
			"designation": ss.designation,
			"company": ss.company,
			"start_date": ss.start_date,
			"end_date": ss.end_date,
			"leave_without_pay": ss.leave_without_pay,
			"salary_structure": ss.salary_structure,
			"payment_days": ss.payment_days,
			"currency": currency or company_currency,
			"total_loan_repayment": ss.total_loan_repayment,
		}

		update_column_width(ss, columns)

		for e in earning_types:
			row.update({frappe.scrub(e): ss_earning_map.get(ss.name, {}).get(e)})

		for d in ded_types:
			row.update({frappe.scrub(d): ss_ded_map.get(ss.name, {}).get(d)})

		if currency == company_currency:
			row.update(
				{
					"gross_pay": flt(ss.gross_pay) * flt(ss.exchange_rate),
					"total_deduction": flt(ss.total_deduction) * flt(ss.exchange_rate),
					"net_pay": flt(ss.net_pay) * flt(ss.exchange_rate),
				}
			)

		else:
			row.update(
				{"gross_pay": ss.gross_pay, "total_deduction": ss.total_deduction, "net_pay": ss.net_pay}
			)

		data.append(row)

	merged_list = []
	for dict1 in data:
		for dict2 in final_data:
			if dict1['employee'] == dict2['employee']:
				merged_dict = {**dict1, **dict2}
				merged_list.append(merged_dict)

	return columns, merged_list


def get_earning_and_deduction_types(salary_slips):
	salary_component_and_type = {_("Earning"): [], _("Deduction"): []}

	for salary_compoent in get_salary_components(salary_slips):
		component_type = get_salary_component_type(salary_compoent)
		salary_component_and_type[_(component_type)].append(salary_compoent)

	return sorted(salary_component_and_type[_("Earning")]), sorted(
		salary_component_and_type[_("Deduction")]
	)


def update_column_width(ss, columns):
	if ss.branch is not None:
		columns[3].update({"width": 120})
	if ss.department is not None:
		columns[4].update({"width": 120})
	if ss.designation is not None:
		columns[5].update({"width": 120})
	if ss.leave_without_pay is not None:
		columns[9].update({"width": 120})


def get_columns(earning_types, ded_types, final_data):
	columns = [
		{
			"label": _("Salary Slip ID"),
			"fieldname": "salary_slip_id",
			"fieldtype": "Link",
			"options": "Salary Slip",
			"width": 150,
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 180,
		},
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120,
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Date of Joining"),
			"fieldname": "data_of_joining",
			"fieldtype": "Date",
			"width": 160,
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Link",
			"options": "Branch",
			"width": -1,
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 80,
		},
		{
			"label": _("Designation"),
			"fieldname": "designation",
			"fieldtype": "Link",
			"options": "Designation",
			"width": 120,
		},
		
		{
			"label": _("Start Date"),
			"fieldname": "start_date",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("End Date"),
			"fieldname": "end_date",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Leave Without Pay"),
			"fieldname": "leave_without_pay",
			"fieldtype": "Float",
			"width": 50,
		},
		{
			"label": _("Salary Structure"),
			"fieldname": "salary_structure",
			"fieldtype": "Link",
			"options": "Salary Structure",
			"width": 120,
		},
		{
			"label": _("Payment Days"),
			"fieldname": "payment_days",
			"fieldtype": "Float",
			"width": 120,
		},
	]

	unique_components = set()

	for employee_data in final_data:
		unique_components.update(employee_data.keys() - {'Salary Structure', 'total_deduction',
														'employee', 'employee_name', 'department', 'designation','Provident Fund', 'Professional Tax','total_deduction'})

	unique_components = sorted(unique_components)

	for component in unique_components:
		columns.append(
			{
				"label": component.replace("_", " ").title(),
				"fieldname": component,
				"fieldtype": "Currency", 
				"width": 120,
			}
		)

	for earning in earning_types:
		columns.append(
			{
				"label": earning,
				"fieldname": frappe.scrub(earning),
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120,
			}
		)

	columns.append(
		{
			"label": _("Gross Pay"),
			"fieldname": "gross_pay",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120,
		}
	)

	for deduction in ded_types:
		columns.append(
			{
				"label": deduction,
				"fieldname": frappe.scrub(deduction),
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120,
			}
		)

	columns.extend(
		[
			{
				"label": _("Loan Repayment"),
				"fieldname": "total_loan_repayment",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120,
			},
			{
				"label": _("Total Deduction"),
				"fieldname": "total_deduction",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120,
			},
			{
				"label": _("Net Pay"),
				"fieldname": "net_pay",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120,
			},
			{
				"label": _("Currency"),
				"fieldtype": "Data",
				"fieldname": "currency",
				"options": "Currency",
				"hidden": 1,
			},
		]
	)
	return columns


def get_salary_components(salary_slips):
	return (
		frappe.qb.from_(salary_detail)
		.where((salary_detail.amount != 0) & (salary_detail.parent.isin([d.name for d in salary_slips])))
		.select(salary_detail.salary_component)
		.distinct()
	).run(pluck=True)


def get_salary_component_type(salary_component):
	return frappe.db.get_value("Salary Component", salary_component, "type", cache=True)


def get_salary_slips(filters, company_currency):
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	query = frappe.qb.from_(salary_slip).select(salary_slip.star)

	if filters.get("docstatus"):
		query = query.where(salary_slip.docstatus == doc_status[filters.get("docstatus")])

	if filters.get("from_date"):
		query = query.where(salary_slip.start_date >= filters.get("from_date"))

	if filters.get("to_date"):
		query = query.where(salary_slip.end_date <= filters.get("to_date"))

	if filters.get("company"):
		query = query.where(salary_slip.company == filters.get("company"))

	if filters.get("employee"):
		query = query.where(salary_slip.employee == filters.get("employee"))

	if filters.get("currency") and filters.get("currency") != company_currency:
		query = query.where(salary_slip.currency == filters.get("currency"))

	salary_slips = query.run(as_dict=1)

	return salary_slips or []


def get_employee_doj_map():
	employee = frappe.qb.DocType("Employee")

	result = (frappe.qb.from_(employee).select(employee.name, employee.date_of_joining)).run()

	return frappe._dict(result)


def get_salary_slip_details(salary_slips, currency, company_currency, component_type):
	salary_slips = [ss.name for ss in salary_slips]

	result = (
		frappe.qb.from_(salary_slip)
		.join(salary_detail)
		.on(salary_slip.name == salary_detail.parent)
		.where((salary_detail.parent.isin(salary_slips)) & (salary_detail.parentfield == component_type))
		.select(
			salary_detail.parent,
			salary_detail.salary_component,
			salary_detail.amount,
			salary_slip.exchange_rate,
		)
	).run(as_dict=1)

	ss_map = {}

	for d in result:
		ss_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_map[d.parent][d.salary_component] += flt(d.amount) * flt(
				d.exchange_rate if d.exchange_rate else 1
			)
		else:
			ss_map[d.parent][d.salary_component] += flt(d.amount)

	return ss_map


def get_data(filters):
	final_data = []
 
	employee_list = frappe.db.get_list("Employee", {"status": "Active"}, ['employee', 'department', 'designation', 'employee_name'], order_by='employee asc')
	for each in employee_list:
		employee_ssa = frappe.db.get_list("Salary Structure Assignment", {'employee': each['employee'], 'docstatus': 1}, ['employee', 'salary_structure', 'base'])

		if len(employee_ssa) > 0:
			salary_earnings = frappe.db.get_list("Salary Detail", {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "earnings"}, ['*'])
			salary_deductions = frappe.db.get_list("Salary Detail", {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "deductions"}, ['*'])

			earning = earnings_details(salary_earnings, employee_ssa)
			print(earning,"earningearningearning")
			duplicate_earning = earning.copy()

			earning.update({"employee": each['employee'], "employee_name": each['employee_name'], "department": each['department'],
							"designation": each['designation']})

			
			deduction = deductions_details(salary_earnings,salary_deductions,employee_ssa)

			final_data.append({**earning, **deduction})
	print(final_data,'/////////////////////')
	return final_data,[],[]


def earnings_details(salary_earnings, employee_ssa):
	try:
		
		final_result = {"Gross Amount": 0.0}

		for each in salary_earnings:
			value_formula = 0.0 
			if "/" in each['formula']:
				abbr_formula_values = each['formula'].split(' / ')
				for abr in salary_earnings:
					if abr["abbr"] == abbr_formula_values[0]:
						formula_value = abr['formula'].split("*")[1]
						value_formula = float(formula_value) / int(abbr_formula_values[1])

				each['formula'] = f"base * {value_formula}"
			else:
				pass

			formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]

			if formula_value:
				component_name = f"Actual_{each['salary_component']}"
				final_result.update({component_name: (employee_ssa[0]['base'] * formula_value[0])})
				final_result["Gross Amount"] += employee_ssa[0]['base'] * formula_value[0]

			else:
				component_name = f"Actual_{each['salary_component']}"
				final_result.update({component_name: (each['amount'])})
				final_result["Gross Amount"] += each['amount']

		
		return final_result
	except Exception as e:
		frappe.log_error(str(e))


def deductions_details(salary_earnings,salary_deductions,employee_ssa):
	try:
		final_deductions = {}
		for each in salary_deductions:
			
			pf_formula = each['formula'].split(' * ')
		
			for abr in salary_earnings:
				if abr["abbr"] == pf_formula[0]:
					pf_abbr = abr['formula'].split(" * ")
					pf_amount = abr['amount']
     
			formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]
   
			if formula_value and employee_ssa[0]['base']:
				component_name = f"Actual_{each['salary_component']}"
				
				final_deductions.update({component_name: (employee_ssa[0]['base'] * float(pf_abbr[1])* formula_value[0])})
			elif formula_value and pf_amount:
				print("elif elif")
				component_name = f"Actual_{each['salary_component']}"
				final_deductions.update({component_name: (float(pf_amount) * formula_value[0])})

			else:
				component_name = f"Actual_{each['salary_component']}"
				final_deductions.update({component_name: (each['amount'])})
				
		return final_deductions
	
	except Exception as e:
		frappe.log_error(str(e))

