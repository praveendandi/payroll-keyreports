# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta
import calendar
import sys
import traceback



def execute(filters=None):
    validation(filters)
    
    try:
        conds = conditions(filters)
        start_date, end_date = start_and_end_date(filters)

        if start_date and end_date:
            data , earning_component= get_data(filters, conds)
            columns = get_columns(filters, start_date, end_date,earning_component)
            
            return columns, data
        else:
            return [], []
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "update_earning_table")
        



def validation(filters):
    if not filters.get("company"):
        frappe.throw(_("Company Is Required"))
    if not filters.get("from_fiscal_year"):
        frappe.throw(_("Fiscal Year Is Required"))
    if not filters.get("select_month"):
        frappe.throw(_("Month Is Required"))


def conditions(filters):
    condition = {}
    condition.update({
        "company": filters.get("company"),
        "docstatus": 0,
        # "start_date":("fiscal year",filters.get("from_fiscal_year"))
        
    })
    return condition


def get_columns(filters, start_date, end_date,earning_component):
    columns = [
        {
            "label": _("Employee ID"),
            "fieldtype": "Data",
            "fieldname": "employee",
            "width": 150,
        },
        {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 150,
        },
        {
            "label": _("Employement Status"),
            "fieldtype": "Data",
            "fieldname": "employement_status",
            "width": 150,
        },
        {
            "label": _("Employment Type"),
            "fieldtype": "Data",
            "fieldname": "employment_type",
            "width": 150,
        },
        {
            "label": _("Designation"),
            "fieldtype": "Data",
            "fieldname": "job_title",
            "width": 150,
        },
        {
            "label": _("Department"),
            "fieldtype": "Data",
            "fieldname": "department",
            "width": 150,
        },
        {
            "label": _("Location"),
            "fieldtype": "Data",
            "fieldname": "location",
            "width": 150,
        },
        {
            "label": _("Cost Center"),
            "fieldtype": "Data",
            "fieldname": "cost_center",
            "width": 150,
        },
    ]

    for e in earning_component:
        columns.append(
            {
                "label": f"{e}-({start_date.strftime('%b-%Y')})",
                "fieldname": f"{e}_({start_date.strftime('%b-%Y')})".lower(),
                "fieldtype": "Currency",
                "options": "currency",
                "width": "200px",
            }
        )
  
    month_year = f"Gross Pay({start_date.strftime('%b-%Y')})"
    columns.append({
        "label": _(month_year),
        "fieldtype": "Currency",
        "fieldname": month_year.lower(),
        "width": "200px",
    })

    month_year = f"Net Pay({start_date.strftime('%b-%Y')})"
    columns.append({
        "label": _(month_year),
        "fieldtype": "Currency",
        "fieldname": month_year.lower(),
        "width": "200px",
    })
    
    for e in earning_component:
        print(e)
        columns.append(
            {
                "label": f"{e}-({end_date.strftime('%b-%Y')})",
                "fieldname": f"{e}_({end_date.strftime('%b-%Y')})".lower(),
                "fieldtype": "Currency",
                "options": "currency",
                "width": "200px",
            }
        )

    month_year = f"Gross Pay({end_date.strftime('%b-%Y')})"
    columns.append({
        "label": _(month_year),
        "fieldtype": "Currency",
        "fieldname": month_year.lower(),
        "width": "200px",
    })

    month_year = f"Net Pay({end_date.strftime('%b-%Y')})"
    columns.append({
        "label": _(month_year),
        "fieldtype": "Currency",
        "fieldname": month_year.lower(),
        "width": "150px",
        "color": "Red"
    })

    return columns


def get_data(filters, conds):
    final_data = {}
    earning_component = set()
    employees_net_pay = frappe.db.get_list("Salary Slip", conds, ['name', 'employee', 'start_date', 'employee_name', 'net_pay', "gross_pay"])

    for employee in employees_net_pay:
        start_date = employee.get("start_date")
        if start_date:
            month_year = start_date.strftime("%b-%Y")
            employee_key = employee.get("employee")

            employee_detail = get_employee_detail(employee_key)

            if employee_key not in final_data:
                final_data[employee_key] = {
                    "employee": employee_key,
                    "employee_name": employee.get("employee_name"),
                    "employement_status": employee_detail.status,
                    "employment_type": employee_detail.employment_type,
                    "job_title": employee_detail.designation,
                    "department": employee_detail.department.split(" - ")[0] if " - " in employee_detail.get("department") else employee_detail.get("department"),
                    "location": employee_detail.branch,
                    "cost_center": employee_detail.payroll_cost_center.split(" - ")[0] if " - " in employee_detail.get("payroll_cost_center") else employee_detail.get("payroll_cost_center"),
                }
                
            salary_slip_child = update_earning_table(employee)
            for each_chid in  salary_slip_child:
                earning_component.add(each_chid.get('salary_component'))
                final_data[employee_key][f"{each_chid.get('salary_component')}_({month_year})".lower()] = each_chid.get("amount",0)
                
            final_data[employee_key][f"Gross Pay({month_year})".lower()] = employee.get("gross_pay")
            final_data[employee_key][f"Net Pay({month_year})".lower()] = employee.get("net_pay")
            

    return list(final_data.values()), sorted(earning_component)


def update_earning_table(employee):
    
    row_data = employee
    
    name = row_data.get("name")

    get_salary_detail = frappe.db.sql("""
        SELECT salary_component, amount, abbr
        FROM `tabSalary Detail`
        WHERE parent = %s
        AND parentfield = %s
        AND parenttype = %s
        ORDER BY idx ASC
    """, (name, 'earnings', "Salary Slip"), as_dict=True)

    return get_salary_detail

def get_employee_detail(employee_key):
    return frappe.get_doc("Employee", employee_key)


def start_and_end_date(filters):
    start_date = None
    end_date = None

    start_year, end_year = filters.get("from_fiscal_year").split("-")
    start_date_str = f"{start_year}-{filters.get('select_month')}-01"
    end_date_str = f"{end_year}-{filters.get('select_month')}-01"

    start_date = datetime.strptime(start_date_str, "%Y-%b-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%b-%d")

    return start_date, end_date

def get_salary_component_type(type):
	return frappe.db.get_list("Salary Component",{"type":type,'do_not_include_in_total':0},['name'],order_by="name DESC",as_list=1)