# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data



#To Dispaly The Columns In The Report
def get_columns():
    return[
        {
            "label": ("Company"),
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
        },
        {
            "label": ("Employee Number"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "label": ("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data"
        },
         {
            "label": ("Gender"),
            "fieldname": "gender",
            "fieldtype": "Data",
        },
        {
            "label": ("Employment Status"),
            "fieldname": "status",
            "fieldtype": "Data"
        },
        {
            "label": ("Worker Type"),
            "fieldname": "employment_type",
            "fieldtype": "Data"
        },
        {
            "label": ("Job Title"),
            "fieldname": "designation",
            "fieldtype": "Link",
            "options": "Designation",
            "width": "195px"
        },
        {
            "label": ("Department"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": "195px"
        },
        {
            "label": ("Location"),
            "fieldname": "branch",
            "fieldtype": "Data",
        },
        {
            "label": ("Date of Joining"),
            "fieldname": "business_unit",
            "fieldtype": "Data",
        },
        {
            "label": ("Cost Center"),
            "fieldname": "payroll_cost_center",
            "fieldtype": "Data",
        },
        {
            "label": ("Salary Payment Mode"),
            "fieldname": "salary_mode",
            "fieldtype": "Data",
        },
        {
            "label": ("Bank Name"),
            "fieldname": "bank_name",
            "fieldtype": "Data",
            "width": "180px"
        },
        {
            "label": ("Account Number"),
            "fieldname": "bank_ac_no",
            "fieldtype": "Link",
            "options": "Employee",
        },
        # {
        #     "label": ("Name On the Account"),
        #     "fieldname": "account_holder_name",
        #     "fieldtype": "Data",
        # },
        {
            "label": ("IFSC Code"),
            "fieldname": "ifsc_code",
            "fieldtype": "Data",
        },
        {
            "label": ("Pan Number"),
            "fieldname": "pan_number",
            "fieldtype": "Data",
        },
        {
            "label": ("Date of Birth"),
            "fieldname": "date_of_birth",
            "fieldtype": "Date",
        },
        # {
        #     "label": ("Name on PAN Card"),
        #     "fieldname": "employee_name",
        #     "fieldtype": "Data",
        # },
        {
            "label": ("Parent's/Spouse's Name"),
            "fieldname": "person_to_be_contacted",
            "fieldtype": "Data",
        },
        {
            "label": ("Emergency Phone"),
            "fieldname": "emergency_phone_number",
            "fieldtype": "Data",
        },
        # {
        #     "label": ("Name on PAN Card"),
        #     "fieldname": "employee_name",
        #     "fieldtype": "Data",
        # },
        
       
        {
            "label": ("PF Number"),
            "fieldname": "provident_fund_account",
            "fieldtype": "Data",
            "width":"120px"
        }
        
    ]

#To get Filters wise data
def get_conditions(filters):
    conditions = []
    if filters.get("company"):
        conditions.append(f" AND company = '{filters.company}'")

    if filters.get("employee"):
        conditions.append(f" AND employee = '{filters.employee}'")
        
    if filters.get("department"):
        conditions.append(f" AND department = '{filters.department}'")
        
    if filters.get("designation"):
        conditions.append(f" AND designation = '{filters.designation}'")

    return " ".join(conditions)


#To get all the details of Employee from Employee Doctype
def get_data(filters):
    conditions = get_conditions(filters)

    employee_data = frappe.db.sql(f"""
        SELECT
            company,name,employee_name,gender,status,employment_type,designation,department,branch,date_of_joining,payroll_cost_center,salary_mode,
            bank_name,bank_ac_no,ifsc_code,pan_number,date_of_birth,person_to_be_contacted,emergency_phone_number,provident_fund_account
        FROM
            `tabEmployee`
        WHERE
            1 = 1 {conditions}
    """)
    print(employee_data,'//////')
    return employee_data
