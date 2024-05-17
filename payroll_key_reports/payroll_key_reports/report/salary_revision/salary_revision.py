# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe import _


def execute(filters=None):
    
    if not filters.get("employee"):
        return [],[]
    
    start_date,end_date = start_and_end_date(filters)

    filters.update({
        "from_date":start_date,
        "to_date":end_date
    })
    
    employee = employee_detail(filters)
    salary_structure_assig = get_salary_structure_assignment(employee,filters)
   
    if len(salary_structure_assig) <= 0:
        return [],[]
    
    earning_data,basic = get_earnings(salary_structure_assig)
    deduction_data = get_deductions(salary_structure_assig,basic)
    
    
    total_net_month = round((earning_data[-2]["monthly"] - deduction_data[-2]['monthly']),2)
    total_net_annually = round((earning_data[-2]["annually"] - deduction_data[-2]['annually']),2)
    
    # Calculate net total
    net_total  = [{
        "component":"Net Total",
        "monthly":total_net_month,
        "annually":total_net_annually
    }]
    
    # combined Of calculate
    data = earning_data + deduction_data + net_total
    columns = get_columns()
    
    
    return columns, data
    
def start_and_end_date(filters):
    
    start_date = None
    end_date =None
    year = filters.get("start_payroll_period")
    company	= filters.get("company")
    
    if filters.get("start_payroll_period"):
    
        payroll_period = frappe.db.get_list("Payroll Period",
                                    filters=[["Payroll Period","start_date","fiscal year",year],
                                             ["Payroll Period","company","=",company]
                                            ],
                                    fields=['start_date','end_date'],
                                    ignore_permissions=True
        )
  
        if not payroll_period:
            frappe.throw(_(f"Please Define Payroll Period of {year} and {company}"))
        else: 
            start_date = datetime.strftime(payroll_period[0]["start_date"], "%Y-%m-%d")
            end_date = datetime.strftime(payroll_period[0]["end_date"], "%Y-%m-%d")
                
            return start_date,end_date
  
    

def get_columns():
    
    columns = [
       {
            "label":("Component"),
            "fieldtype": "Data",
            "fieldname": "component",
            "width": 200,
        },
        {
            "label":("Monthly"),
            "fieldtype": "Data",
            "fieldname": "monthly",
            "width": 150,
        },
        {
            "label":("Annually"),
            "fieldtype": "Data",
            "fieldname": "annually",
            "width": 150,
        },
    ]
   
    return columns

def employee_detail(filters):
    return frappe.db.get_list("Employee",{"status":"Active","name":filters.get("employee")})

def get_salary_structure_assignment(employee,filters):
    
    salary_ass = []
    employee_ssa = frappe.db.get_list("Salary Structure Assignment",
                                        {
                                        'employee':employee[0]['name'],'docstatus':1,
                                        "from_date":["fiscal year",filters.get("start_payroll_period")]
                                        },
                                        ['name','employee',"employee_name",'salary_structure','from_date','base'],
                                        ignore_permissions=True
                                    )
    
    if len(employee_ssa)>0:
        salary_ass.append(employee_ssa[0])
            
    return salary_ass



def get_earnings(row_data):
    
    final_data = []
    base_assignment =  0.0 # if base value assign in salary structure assignment take from it.
    basic = 0.0 
    
    salary_earnings = frappe.db.get_list("Salary Detail",{'parent':row_data[0]['salary_structure'],'parentfield':"earnings"},['*'],order_by="name DESC",ignore_permissions=True)    
    
    # base on formula and amount
    for each in salary_earnings:
        amount = {}
        if each['salary_component'] == "Basic":
            
            formula = each['formula']
        
            if each['amount'] == 0.0:
                base_assignment = row_data[0]['base']
            else:
                base_assignment = each['amount']
            
            base = base_assignment
            if formula:
                basic = round(float(eval(formula)),2)
            else:
                basic = base_assignment
            
            amount.update({
            "component":(_(each['salary_component'])),
            "monthly":basic,
            "annually":basic*12
            })
            
        else:
            if each['formula']:
                
                if "base" in each['formula']:
                    formula = each['formula']
                    base = base_assignment
                    other_component = round(float(eval(formula)),2)           
                    amount.update({
                    "component":(_(each['salary_component'])),
                    "monthly":other_component,
                    "annually":other_component*12
                    })
                else:
                    formula = each['formula']
                    B = basic
                    other_component = round(float(eval(formula)),2)                   
                    amount.update({
                    "component":(_(each['salary_component'])),
                    "monthly":other_component,
                    "annually":other_component*12
                    })
            else:
                other_component = each['amount']
                amount.update({
                    "component":(_(each['salary_component'])),
                    "monthly":other_component,
                    "annually":other_component*12
                    })
        
        final_data.append(amount)
        
    # final total of earnings 
    total_month  = 0.0
    total_annually = 0.0
    total_month = round(sum([i['monthly'] for i in final_data]),2)
    total_annually = round(sum([i['annually'] for i in final_data]),2)
    
    final_data.append({
        "component":(_("Total Earning")),
        "monthly":total_month,
        "annually":total_annually
    })
    final_data.append([{}]) # add extra row in report
        
    
    return final_data,basic

def get_deductions(row_data,basic):
    
    salary_deductions = frappe.db.get_list("Salary Detail",{'parent':row_data[0]['salary_structure'],'parentfield':"deductions"},['*'],order_by="name DESC",ignore_permissions=True)
    final_data = []   
     
    for each in salary_deductions:
        amount = {}
        
        if each['formula']:
            
            formula = each['formula'].replace("B","base")
            base = basic
            deduction_amount = round(float(eval(formula)),2)
            
            amount.update({
            "component":(_(each['salary_component'])),
            "monthly":deduction_amount,
            "annually":deduction_amount*12
            })            
        else:
            if each['amount'] >0:
                other_component = each['amount']
                
                amount.update({
                "component":(_(each['salary_component'])),
                "monthly":other_component,
                "annually":other_component*12
                })
                
            else:
                other_component = each['amount']
                amount.update({
                "component":(_(each['salary_component'])),
                "monthly":other_component,
                "annually":other_component*12
                })
                
        final_data.append(amount)
    
    # final total of deductions
    total_month  = 0.0
    total_annually = 0.0
    total_month = round(sum([i['monthly'] for i in final_data]),2)
    total_annually = round(sum([i['annually'] for i in final_data]),2)
    
    final_data.append({
        "component":(_("Total Deduction")),
        "monthly":total_month,
        "annually":total_annually
    })
    final_data.append([{}]) # add extra row in report
                    
    return final_data
    