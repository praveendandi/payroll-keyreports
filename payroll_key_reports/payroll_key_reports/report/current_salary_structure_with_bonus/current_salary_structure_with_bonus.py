# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee"},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data"},
        {"fieldname": "gender", "label": "Gender", "fieldtype": "Data"},
        {"fieldname": "designation", "label": "Designation", "fieldtype": "Link", "options": "Designation"},
        {"fieldname": "department", "label": "Department", "fieldtype": "Link", "options": "Department"},
        {"fieldname": "branch", "label": "Branch", "fieldtype": "Link", "options": "Branch"},
        {"fieldname": "bonus_amount", "label": "Retention Bonus Amount", "fieldtype": "Currency"},
        
    ]

    data = get_data(filters)
    return columns, data
def get_data(filters):
    try:
        conditions = get_conditions(filters)

        query = """
            SELECT
            emp.designation, emp.department, rb.employee, rb.employee_name, rb.salary_component, rb.company, rb.bonus_payment_date, SUM(rb.bonus_amount) as bonus_amount
            FROM `tabRetention Bonus` as rb
            LEFT JOIN `tabEmployee` as emp ON rb.employee = emp.name
            WHERE 
            rb.docstatus=1 {cond}
            GROUP BY rb.employee
        """.format(cond=conditions)

        data = frappe.db.sql(query, as_dict=True)
        
        for i in data:
            emp = frappe.db.get_list("Employee",
                                    {"name": i["employee"]},
                                    ["designation", "department", "gender", "branch"],
                                    limit=1
                                    )

            if emp:
                i.update({
                    "designation": emp[0]["designation"],
                    "department": emp[0]["department"],
                    "gender": emp[0]["gender"],
                    "branch": emp[0]["branch"]
                })

        print(data)
        return data
    except Exception as e:
        frappe.log_error(str(e))
        


def get_conditions(filters):
    try:
        conditions = ""
        conditions+= f" AND rb.company = '{filters.company}'"

        if filters.employee:
            conditions += f" AND rb.employee = '{filters.employee}'"
        if filters.designation:
            conditions += f" AND emp.designation = '{filters.designation}'"
        if filters.department:
            conditions += f" AND emp.department = '{filters.department}'"


        if filters.payroll_period:
            payroll_period = frappe.get_doc("Payroll Period", filters.payroll_period)
            conditions += f" AND rb.bonus_payment_date BETWEEN '{payroll_period.start_date}' AND '{payroll_period.end_date}'"


        return conditions
    except Exception as e:
        frappe.log_error(str(e))