# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from hrms.payroll.report.salary_register.salary_register import execute as execute_

def execute(filters=None):
    
    row_data = execute_(filters)
    
    if len(row_data[1]):
        data = get_data(row_data[1])
        columns = row_data[0]
        data = row_data[1]
      
        return columns, data
    else:
        columns=[],data=[]
        

def get_data(row_data):
    
    for each in row_data:
        print(each,"oooooooooooooooooooooo")
        
