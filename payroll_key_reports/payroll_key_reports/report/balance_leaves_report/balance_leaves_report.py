# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt


from datetime import date
from datetime import datetime
import frappe

def execute(filters=None):
    try:
        columns = get_columns(filters)
        data , leave_type = leave_balance(filters)
        chart  =get_chart(data,leave_type)
        
        return columns, data, None,chart
    except Exception as e:
        frappe.log_error(str(e) + " Attendance Regularized")

def get_columns(filters):
    columns = [
        {
            "label": ("Employee Number"),
            "fieldtype": "link",
            "fieldname": "employee",
            "options": "Employee",
            "width": 150,
        },
        {
            "label": ("Employee Name"),
            "fieldtype": "data",
            "fieldname": "employee_name",
            "width": 150,
        },
        {
            "label": ("Leave Type"),
            "fieldtype": "data",
            "fieldname": "leave_type",
            "width": 150,
        },
        {
            "label": ("Leaves Allocated"),
            "fieldtype": "Float",
            "fieldname": "Leaves Allocated",
            "width": 150,
        },
        {
            "label": ("Total Used Leaves"),
            "fieldtype": "Float",
            "fieldname": "Total Used Leaves",
            "width": 150,
        },
        {
            "label": ("Available Leaves"),
            "fieldtype": "Float",
            "fieldname": "Available Leaves",
            "width": 150,
        },
        
    ]
    
    
    return columns

def leave_balance(filters):
    try:
        final_data = []
        total_used_leaves = 0.0

        employee_leave_data = frappe.db.get_list("Leave Allocation", {
            "employee": filters.get("employee"),
            "leave_type": filters.get("leave_type"),
            "docstatus": 1
        }, ["from_date", "employee", "employee_name", "leave_type", "new_leaves_allocated"])

        employee_leave_used = frappe.db.get_list("Leave Application", {
            "employee": filters.get("employee"),
            "leave_type": filters.get("leave_type"),
            "status": "Approved"
        }, ["total_leave_days"])

        for i in employee_leave_data:
            if i["from_date"].year == date.today().year:
                leave_data = {
                    "employee": i["employee"],
                    "employee_name": i["employee_name"],
                    "leave_type": i["leave_type"],
                    "Leaves Allocated": i["new_leaves_allocated"],
                    "Total Used Leaves": 0.0,
                    "Available Leaves": i["new_leaves_allocated"]
                }

                for leave in employee_leave_used:
                    total_used_leaves += leave['total_leave_days']

                if total_used_leaves > 0:
                    available_leave = leave_data['Leaves Allocated'] - total_used_leaves
                    leave_data['Total Used Leaves'] = total_used_leaves
                    leave_data['Available Leaves'] = available_leave

                final_data.append(leave_data)

        leave_type = employee_leave_data[0]['leave_type'] if employee_leave_data else None

        return final_data, leave_type

    except Exception as e:
        frappe.log_error(str(e) + " Attendance Regularized")
 

def get_chart(final_data,leave_type):
    try:
        keys = [list(i.keys()) for i in final_data][0][4:]
        
        values = [list(i.values()) for i in final_data][0][4:]
        
        chart = {
            'data':{
                'labels':keys,
                'datasets':[
                    {'name':leave_type,"values":values,'chartType':'donut'}
                ]
            },
            'type':"donut",
            'colors':['#fa6e0a','#1127f0']

        }
        return chart
    
    except Exception as e:
        frappe.log_error(str(e) + "Attendance Regularized")  
        