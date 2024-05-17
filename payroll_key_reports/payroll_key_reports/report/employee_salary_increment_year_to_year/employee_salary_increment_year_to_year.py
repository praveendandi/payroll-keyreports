# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 120},
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 120},
        {"label": "Gross Pay(2023)", "fieldname": "gross_pay_prev_year", "fieldtype": "Currency", "width": 200},
        {"label": "Gross Pay(2024)", "fieldname": "gross_pay_current_year", "fieldtype": "Currency", "width": 200},
        
        {"label": "Gross Pay Increment Percentage", "fieldname": "gross_pay_increment_percentage", "fieldtype": "Percent", "width": 230},
    ]

    data = get_data(filters)
    total_row = calculate_total(data)

    return columns, data + [total_row]

def get_data(filters):
    conditions = get_conditions(filters)
    data = frappe.db.sql("""
        SELECT
            employee, 
            employee_name,
            designation,
            department,
            gross_pay,
            YEAR(start_date) as year,
            MONTH(start_date) as month
        FROM
            `tabSalary Slip` 
        WHERE
            docstatus = 1 
            {conditions}
    """.format(conditions=conditions),
    filters,
    as_dict=1)

    processed_data = process_data(data, filters)

    return processed_data

def process_data(data, filters):
    selected_month = int(filters.get("month"))
    current_year = int(frappe.utils.nowdate().split("-")[0])

    processed_data = []
    employee_gross_pays = {}

    for entry in data:
        entry_year = int(entry.get("year"))
        entry_month = int(entry.get("month"))

        if entry_month == selected_month:
            employee_key = entry.get("employee")

            if employee_key not in employee_gross_pays:
                employee_gross_pays[employee_key] = {
                    "gross_pay_prev_year": 0,
                    "gross_pay_current_year": 0,
                    "employee_name": entry.get("employee_name"),
                    "designation": entry.get("designation"),
                    "department": entry.get("department"),
                }

            if entry_year == (current_year - 1):
                employee_gross_pays[employee_key]["gross_pay_prev_year"] += entry.get("gross_pay")
            elif entry_year == current_year:
                employee_gross_pays[employee_key]["gross_pay_current_year"] += entry.get("gross_pay")

    for employee_key, values in employee_gross_pays.items():
        gross_pay_prev_year = values["gross_pay_prev_year"]
        gross_pay_current_year = values["gross_pay_current_year"]
        gross_pay_difference = gross_pay_current_year - gross_pay_prev_year

      
        gross_pay_increment_percentage = 0
        if gross_pay_prev_year != 0:
            gross_pay_increment_percentage = (gross_pay_difference / gross_pay_prev_year) * 100
        processed_data.append({
            "employee": employee_key,
            "employee_name": values["employee_name"],
            "designation": values["designation"],
            "department": values["department"],
            "gross_pay_prev_year": gross_pay_prev_year,
            "gross_pay_current_year": gross_pay_current_year,
            "gross_pay_difference": gross_pay_difference,
            "gross_pay_increment_percentage": gross_pay_increment_percentage,
        })

    return processed_data


def calculate_total(data):
    gross_pay_prev_year_total = sum(entry.get("gross_pay_prev_year", 0) for entry in data)
    gross_pay_current_year_total = sum(entry.get("gross_pay_current_year", 0) for entry in data)
    gross_pay_difference_total = sum(entry.get("gross_pay_difference", 0) for entry in data)
    
    # Calculate the increment percentage for the total
    gross_pay_increment_percentage_total = 0
    if gross_pay_prev_year_total != 0:
        gross_pay_increment_percentage_total = ((gross_pay_current_year_total - gross_pay_prev_year_total) / gross_pay_prev_year_total) * 100

    total_row = {
        "employee": "Total",
        "employee_name": "",
        "designation": "",
        "department": "",
        "gross_pay_prev_year": gross_pay_prev_year_total,
        "gross_pay_current_year": gross_pay_current_year_total,
        "gross_pay_difference": gross_pay_difference_total,
        "gross_pay_increment_percentage": gross_pay_increment_percentage_total
    }

    return total_row


def get_conditions(filters):
    conditions = ""
    if filters.get("employee"):
        conditions += f" AND employee = '{filters.get('employee')}'"

    if filters.get("designation"):
        conditions += f" AND designation = '{filters.get('designation')}'"

    if filters.get("department"):
        conditions += f" AND department = '{filters.get('department')}'"

    if filters.get("payroll_period"):
        payroll_period = frappe.get_doc("Payroll Period", filters.get("payroll_period"))

        if payroll_period and hasattr(payroll_period, "start_date") and hasattr(payroll_period, "end_date"):
            start_year = int(str(payroll_period.start_date).split("-")[0])
            end_year = int(str(payroll_period.end_date).split("-")[0])

            # Adjust the SQL query to filter data within the selected payroll period range
            conditions += f" AND YEAR(start_date) BETWEEN {start_year} AND {end_year}"

        else:
            frappe.throw("Invalid or missing start_date or end_date in Payroll Period")

    return conditions
