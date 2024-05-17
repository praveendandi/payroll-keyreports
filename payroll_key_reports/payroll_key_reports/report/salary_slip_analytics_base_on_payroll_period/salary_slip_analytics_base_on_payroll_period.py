# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from hrms.payroll.report.salary_register.salary_register import execute as execute_
from frappe import _
import pandas as pd



def execute(filters=None):
    
    if not filters.get("payroll_period"):
        frappe.throw(_(f"Select Please Any Payroll Period of This {filters.get('company')} Company"))
        return [],[]
    
    start_date,end_date = start_and_end_date(filters)
    print(start_date,end_date)
    
    
    filters.update({
        "from_date":start_date,
        "to_date":end_date
    })
    
    row_data = execute_(filters)
    print(row_data[1])
    
    if len(row_data[1])>0:
        
        data = get_data(filters,row_data[1])
        columns = get_columns(row_data[0])
        
        return columns, data
    else:
        columns, data = [], []


def start_and_end_date(filters):
    
    start_date = None
    end_date =None
    year = filters.get("payroll_period")
    company	= filters.get("company")
    
    if filters.get("payroll_period"):
    
        payroll_period = frappe.db.get_list("Payroll Period",
                                    filters=[["Payroll Period","start_date","fiscal year",year],
                                             ["Payroll Period","company","=",company]
                                            ],
                                    fields=['start_date','end_date']
        )
    
        if not payroll_period:
            frappe.throw(_(f"Please Define Payroll Period of {year} Of This {company} Company"))
        else: 
            start_date = datetime.strftime(payroll_period[0]["start_date"], "%Y-%m-%d")
            end_date = datetime.strftime(payroll_period[0]["end_date"], "%Y-%m-%d")
                
            return start_date,end_date
   

def get_data(filters,row_data):
    
    data_df = pd.DataFrame.from_records(row_data)
    print(data_df.dtypes)
   
    del data_df['data_of_joining']
    del data_df["start_date"]
    del data_df["end_date"]
    del data_df["currency"]
   
    group_data = data_df.groupby(by=["employee","employee_name","department","designation","company"],as_index=False).sum()
    
    final_data  = group_data.to_dict(orient='records')
    
    return final_data


def get_columns(row_columns):
    
    columns = []
    
    columns.extend(row_columns[1:3])
    columns.extend(row_columns[4:8])
    columns.extend(row_columns[10:])
    
    return columns

