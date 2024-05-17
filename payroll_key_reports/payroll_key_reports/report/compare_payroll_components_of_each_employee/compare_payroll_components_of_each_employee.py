# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta
import calendar



def execute(filters=None):
    
    validation(filters)
    conds = conditions(filters)
    start_date,end_date = start_and_end_date(filters)
    
    if start_date and end_date:
        
        data = get_data(filters,conds)
        columns = get_columns(filters,start_date,end_date)
    
        return columns, data
    else:
        return [],[]


def validation(filters):
    
    # if filters.get("end_date") < filters.get("start_date"):
    #     frappe.throw(_("Start Date Is Not Greater Than End Date"))
        
    # if not filters.get("end_date") or not filters.get("start_date"):
    #     frappe.throw(_("Date is Required"))
        
    if not filters.get("company"):
        frappe.throw(_("Company Is Required"))
    

def conditions(filters):
    
    condition = {}
    condition.update({
        # "start_date":["Between In",[filters.get("start_date"),filters.get("end_date")]],
        "company":filters.get("company"),
        "docstatus":1
    })
 
    return condition

    
def get_columns(filters,start_date,end_date):
    columns = [
        {
            "label":("Employee"),
            "fieldtype": "link",
            "fieldname": "employee",
            "options": "Employee",
            "width": 150,
        },
        {
            "label":("Employee Name"),
            "fieldtype": "data",
            "fieldname": "employee_name",
            "width": 150,
        },
        {
            "label":("Employement Status"),
            "fieldtype": "Data",
            "fieldname": "employement_status",
            "width": 150,
        },
        {
            "label":("Employment Type"),
            "fieldtype": "Data",
            "fieldname": "employment_type",
            "width": 150,
        },
        {
            "label":("Job Title"),
            "fieldtype": "Data",
            "fieldname": "job_title",
            "width": 150,
        },
        
        {
            "label":("Department"),
            "fieldtype": "Data",
            "fieldname": "department",
            "width": 150,
        },
        {
            "label":("Location"),
            "fieldtype": "Data",
            "fieldname": "location",
            "width": 150,
        },
        # {
        #     "label":("Business Unit"),
        #     "fieldtype": "Data",
        #     "fieldname": "business_unit",
        #     "width": 150,
        # },
        {
            "label":("Cost Center"),
            "fieldtype": "Data",
            "fieldname": "cost_center",
            "width": 150,
        },
    ]

    if filters.get("from_fiscal_year"):
        # start_date, end_date = start_and_end_date(filters)
        # end_date = start_and_end_date(filters)
        # start_date = datetime.strptime(filters.get("start_date"), "%Y-%m-%d")
        # end_date = datetime.strptime(filters.get("end_date"), "%Y-%m-%d")
        current_date = start_date

        # while current_date < end_date:
        month_year = f"Gross Pay({current_date.strftime('%b-%Y')})"
        
        columns.append({
            "label":_(month_year),
            "fieldtype": "Currency",
            "fieldname": month_year.lower(),
            "width": "150px",
        })
        
        month_year = f"Net Pay({current_date.strftime('%b-%Y')})"
        columns.append({
            "label":_(month_year),
            "fieldtype": "Currency",
            "fieldname": month_year.lower(),
            "width": "150px",
        })
        # current_date = current_date + timedelta(days=calendar.monthrange(current_date.year, current_date.month)[1])
        
        month_year = f"Gross Pay({end_date.strftime('%b-%Y')})"
        columns.append({
            "label":_(month_year),
            "fieldtype": "Currency",
            "fieldname": month_year.lower(),
            "width": "150px",
        })
        month_year = f"Net Pay({end_date.strftime('%b-%Y')})"
        columns.append({
            "label":_(month_year),
            "fieldtype": "Currency",
            "fieldname": month_year.lower(),
            "width": "150px",
            "color":"Red"
        })
            
   

    return columns

def get_data(filters,conds):
    final_data = {}
    employees_net_pay = frappe.db.get_list("Salary Slip", conds, ['name', 'employee', 'start_date', 'employee_name', 'net_pay',"gross_pay"])
   
    
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
                    "employement_status":employee_detail.status,
                    "employment_type":employee_detail.employment_type,
                    "job_title":employee_detail.designation,
                    "department":employee_detail.department,
                    "location":employee_detail.branch,
                    "cost_center":employee_detail.payroll_cost_center,
                }

            final_data[employee_key][f"Gross Pay({month_year})".lower()] = employee.get("gross_pay")
            final_data[employee_key][f"Net Pay({month_year})".lower()] = employee.get("net_pay")
    
           
    print(final_data)
    return list(final_data.values())

def get_employee_detail(employee_key):
    
    return frappe.get_doc("Employee", employee_key)

def start_and_end_date(filters):
    
    start_date = None
    end_date =None
    
    start_year,end_year = filters.get("from_fiscal_year").split("-")
    if filters.get('select_month'):
    
        start_date_str = f"{start_year}-{filters.get('select_month')}-01"
        end_date_str = f"{end_year}-{filters.get('select_month')}-01"
        
        start_date = datetime.strptime(start_date_str, "%Y-%b-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%b-%d")
        
        return start_date,end_date
    else:
        return start_date,end_date
    