# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
import erpnext
from hrms.payroll.report.salary_register.salary_register import execute as execute_
from frappe.utils import flt, formatdate

def execute(filters=None):
    
    row_data = execute_(filters)
    
    if len(row_data[1]):
        
        data = get_data(row_data[1])
        
        columns = row_data[0]
      
        return columns, data
    else:
        return [],[]
        

def get_data(row_data):
    
    for each in row_data:
        each.update({
            "data_of_joining":formatdate(each.get('data_of_joining'), "dd-mm-yyyy"),
            "start_date":formatdate(each.get("start_date"), "dd-mm-yyyy"),
            "start_date":formatdate(each.get("end_date"), "dd-mm-yyyy")
        })
        
        department_name = None
        if each.get("department"):
            department_name = each.get("department").split(" - ")[0] if " - " in each.get("department") else each.get("department")
            
        each.update({
            "department":department_name
        })
        
    return row_data

        
        
        
