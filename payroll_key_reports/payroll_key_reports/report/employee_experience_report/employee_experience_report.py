# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from datetime import date


def execute(filters=None):
	try:
		columns = get_columns(filters)
		data, count_0_to_3_years, count_3_to_5_years, count_5_to_10_years, count__10_years = employee_experience(filters)
		if filters.get("group_by_experience") == 1:
			return columns, [
				{"experience_range": "0-3", "Total count": count_0_to_3_years},
				{"experience_range": "3-5", "Total count": count_3_to_5_years},
				{"experience_range": "5-10", "Total count": count_5_to_10_years},
				{"experience_range": "10+", "Total count": count__10_years}
			], None
		else:
			return columns, data, None
	except Exception as e:
		frappe.log_error(str(e))

def get_columns(filters):
	if filters.get("group_by_experience") == 1:
		return [
			{"label": "Experience Range", "fieldtype": "Data", "fieldname": "experience_range", "width": 150},
			{"label": "Total Count", "fieldtype": "Data", "fieldname": "Total count", "width": 150}
		]
	else:
		return [
			{"label": "Employee", "fieldtype": "Link", "fieldname": "employee", "options": "Employee", "width": 150},
			{"label": "Employee Name", "fieldtype": "Data", "fieldname": "employee_name", "width": 150},
			{"label": "Experience", "fieldtype": "Data", "fieldname": "experience_years", "width": 150},
		]

def employee_experience(filters):
	try:
		conditions = get_conditions(filters)
		
		final_data = []
		count_0_to_3_years = 0
		count_3_to_5_years = 0
		count_5_to_10_years = 0
		count__10_years = 0
		if filters.get("employee"):
			filters_emp = {"status": "Active", 'employee': filters.get("employee")}

		else:
			filters_emp = {"status": "Active"}

		if filters.get("company"):
				filters_emp.update({'company': filters.get("company")})

		employee_data = frappe.db.get_list("Employee",filters_emp, ['name', 'employee_name', 'date_of_joining'])

		for emp in employee_data:
			if date.today() > emp['date_of_joining']:
				experience_duration = date.today() - emp['date_of_joining']
				years = experience_duration.days // 365
				months = (experience_duration.days % 365) // 30
				if 0 <= years <= 3:
					count_0_to_3_years += 1
				elif 3 < years <= 5:
					count_3_to_5_years += 1
				elif 5 < years <= 10:
					count_5_to_10_years += 1
				elif years >= 10:
					count__10_years += 1
					
				experience_years = f"{years} years {months} months"    
				final_data.append({
					'employee': emp['name'],
					'employee_name': emp['employee_name'],
					'experience_years': experience_years
				})

		return final_data, count_0_to_3_years, count_3_to_5_years, count_5_to_10_years, count__10_years
	except Exception as e:
		frappe.log_error(str(e))

def get_conditions(filters):
	try:
		conditions = ""
		if filters.get("employee"):
			conditions += " and employee = '%s'" % filters.get("employee")
		if filters.get("company"):
				conditions += " and company = '%s'" % filters.get("company")
		return conditions 
	except Exception as e:
		frappe.log_error(str(e))          
