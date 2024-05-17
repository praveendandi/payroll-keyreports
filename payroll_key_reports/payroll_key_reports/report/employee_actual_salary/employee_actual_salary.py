# # Copyright (c) 2024, caratRED Technologies LLP and contributors
# # For license information, please see license.txt

import frappe
import re

def execute(filters=None):
    try:
        conditions, data, final_earning, final_deduction = get_data(filters)
        columns = get_columns(final_earning, final_deduction)

        return columns,data, None
    except Exception as e:
        frappe.log_error(str(e))

def get_columns(final_earning, final_deduction):
    columns = [
        {"label": "Employee", "fieldtype": "Link", "fieldname": "employee", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldtype": "Data", "fieldname": "employee_name", "width": 150},
        {"label": "Company", "fieldtype": "Link", "fieldname": "company", "options": "Company", "width": 150},
        {"label": "Salary Structure", "fieldtype": "Link", "fieldname": "Salary Structure", "options": "Salary Structure", "width": 150},
        {"label": "Department", "fieldtype": "Data", "fieldname": "department", "width": 150},
        {"label": "Designation", "fieldtype": "Data", "fieldname": "designation", "width": 150},
    ]

    unique_components = set()
    for employee_data in final_earning:
        unique_components.update(employee_data.keys() - {"Gross Amount"})

    unique_components = sorted(unique_components)

    for component in unique_components:
        columns.append(
            {
                "label": component.replace("_", " ").capitalize(),
                "fieldname": component,
                "fieldtype": "Currency",
                "width": 120,
            }
        )

    columns.append(
        {
            "label": "Gross Amount",
            "fieldname": "Gross Amount",
            "fieldtype": "Currency",
            "width": 120,
        }
    )

    ded_unique_components = set()
    for employee_data in final_deduction:
        ded_unique_components.update(employee_data.keys())

    ded_unique_components = sorted(ded_unique_components)
    for component_ded in ded_unique_components:
        columns.append(
            {
                "label": component_ded.replace("_", " ").capitalize(),
                "fieldname": component_ded,
                "fieldtype": "Currency",
                "width": 120,
            }
        )
    columns.append(
        {
            "label": "Net Amount",
            "fieldname": "net_pay",
            "fieldtype": "Currency",
            "width": 120,
        }
    )

    return columns

def get_data(filters):
    try:
        conditions = get_conditions(filters)

        columns_deduction = []
        columns_earning = []
        final_data = []
        duplicate_earning = None

        if filters.get("employee"):
            filters_emp = {"status": "Active", 'employee': filters.get("employee")}
        else:
            filters_emp = {"status": "Active"}

        if filters.get("department"):
            filters_emp.update({'department': filters.get("department")})
            
        if filters.get("company"):
            filters_emp.update({'company': filters.get("company")})

        employee_list = frappe.db.get_list("Employee", filters_emp, ['employee', 'company', 'department', 'designation', 'employee_name'], order_by='employee asc')

        for each in employee_list:
            if not filters.get("salary_structure"):
                filters_data = {'employee': each['employee'], 'docstatus': 1}
            else:
                filters_data = {'employee': each['employee'], 'docstatus': 1, "salary_structure": filters.get("salary_structure")}

            employee_ssa = frappe.db.get_list("Salary Structure Assignment", filters_data, ['employee', 'salary_structure', 'base'])

            if len(employee_ssa) > 0:
                salary_earnings = frappe.db.get_list("Salary Detail", {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "earnings"}, ['*'])
                salary_deductions = frappe.db.get_list("Salary Detail", {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "deductions"}, ['*'])

                earning = earnings_details(salary_earnings, employee_ssa)

                duplicate_earning = earning.copy()

                columns_earning.append(duplicate_earning)
                
                deductions = deductions_details(salary_earnings,salary_deductions,employee_ssa)
                total_deduction = 0
                for component in deductions.values():
                    total_deduction += component
                deductions.update({"total_deduction": total_deduction})

                columns_deduction.append(deductions)
                for i in employee_ssa:
                    value = i.get("salary_structure")
                    earning.update({'Salary Structure': value})
                earning.update({"employee": each['employee'], "employee_name": each['employee_name'], "department": each['department'],
                                "designation": each['designation'],"company": each['company']})
                earning.update(deductions)

                final_data.append(earning)
                for i in final_data:
                    net_pay = i.get("Gross Amount") - i.get("total_deduction")
                    i.update({"net_pay": net_pay})

        return conditions, final_data, columns_earning, columns_deduction

    except Exception as e:
        frappe.log_error(str(e))

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
            
            formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]
            
            if formula_value:
                component_name = each['salary_component']
                final_result.update({component_name: (employee_ssa[0]['base'] * formula_value[0])})
                final_result["Gross Amount"] += employee_ssa[0]['base'] * formula_value[0]
            else:
                component_name = each['salary_component']
                final_result.update({component_name: each['amount']})
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
                component_name = f"{each['salary_component']}"
                final_deductions.update({component_name: (employee_ssa[0]['base'] * float(pf_abbr[1])* formula_value[0])})

            elif formula_value and pf_amount:
                component_name = f"{each['salary_component']}"
                final_deductions.update({component_name: (float(pf_amount) * formula_value[0])})

            else:
                component_name = f"{each['salary_component']}"
                final_deductions.update({component_name: (each['amount'])})
                
        return final_deductions
    
    except Exception as e:
        frappe.log_error(str(e))

def get_conditions(filters):
    try:
        conditions = ""
        
        if filters.get("company"):
            conditions += " and company = '%s'" % filters.get("company")
        if filters.get("salary_structure"):
            conditions += " and salary_structure = '%s'" % filters.get("salary_structure")
        if filters.get("employee"):
            conditions += " and employee = '%s'" % filters.get("employee")
        if filters.get("department"):
            conditions += " and department = '%s'" % filters.get("department")
            
        return conditions
    
    except Exception as e:
        frappe.log_error(str(e))








