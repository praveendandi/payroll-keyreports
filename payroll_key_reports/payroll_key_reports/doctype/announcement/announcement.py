# Copyright (c) 2024, caratRED Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.print_format import download_pdf
import sys
import traceback


class Announcement(Document):
    def on_submit(self):
        # Check if it's a general announcement
        if self.general_announcement == 1:
            # Retrieve a list of all employees
            all_employees = frappe.db.get_all(
                "Employee", ["employee", "first_name", "employee_name", "department", "designation", "user_id"]
            )
            print(all_employees, '/////////////////////////////////')

            # Prepare email content
            email_content = f"General Announcement:\n\n{self.letter}"

            # Send email to all employees
            send_email_to_employees(all_employees, email_content, self)
            
        elif self.announcement_type == "By Company":
            company_wise_employees = frappe.db.get_all(
                "Employee",{"company":self.company},["employee", "first_name", "employee_name", "department", "designation", "user_id"]
            )
            print(company_wise_employees, '/////////////////////////////////')
            email_content = f"Announcement For All Employees:\n\n{self.letter}"
            
            # Send email to all employees
            send_email_to_employees(company_wise_employees, email_content, self)

        # Check if it's an announcement by employee
        elif self.announcement_type == "By Employee":
            # Retrieve employee information for the specified employee
            employee_data = frappe.db.get_all(
                "Employee", {"employee": self.employee},
                ["employee", "first_name", "employee_name", "department", "designation", "user_id"]
            )
            print(employee_data, 'employee_data')

            # Prepare email content
            email_content = f"Announcement for Employee {self.employee}:\n\n{self.letter}"

            # Send email to the specified employee
            send_email_to_employees([employee_data], email_content, self)

        # Check if it's an announcement by department
        elif self.announcement_type == "By Department":
            # Retrieve a list of employees in the specified department
            department_wise_employees = frappe.db.get_list(
                "Employee", {"department": self.department},
                ["employee", "first_name", "employee_name", "department", "designation", "user_id"]
            )
            print(department_wise_employees, 'department_wise_employees')

            # Prepare email content
            email_content = f"Announcement for Department {self.department}:\n\n{self.letter}"

            # Send email to employees in the specified department
            send_email_to_employees(department_wise_employees, email_content, self)

        # Check if it's an announcement by designation
        elif self.announcement_type == "By Designation":
            # Retrieve a list of employees with the specified designation
            designation_wise_employees = frappe.db.get_list(
                "Employee", {"designation": self.designation},
                ["employee", "first_name", "employee_name", "department", "designation", "user_id"]
            )
            print(designation_wise_employees, 'designation_wise_employees')

            # Prepare email content
            email_content = f"Announcement for Designation {self.designation}:\n\n{self.letter}"

            # Send email to employees with the specified designation
            send_email_to_employees(designation_wise_employees, email_content, self)

        else:
            # Raise an exception if the announcement type is not recognized
            frappe.throw("Please Select General Announcement or Announcement Type")


def send_email_to_employees(employees, content, doc):
    recipients = []

    # Extract user IDs from the employee data
    for employee in employees:
        if isinstance(employee, dict):
            user_id = employee.get("user_id")
            if user_id:
                recipients.append(user_id)
        elif isinstance(employee, list) and len(employee) > 0 and isinstance(employee[0], dict):
            user_id = employee[0].get("user_id")
            if user_id:
                recipients.append(user_id)
        else:
            # Print a message if the data format is unexpected
            frappe.msgprint(f"Unexpected data format for employee: {employee}")

    # Download PDF content for the announcement document
    pdf_content = download_pdf(doc.doctype, doc.name, format="Standard")

    try:
        # Prepare attachments for the email
        attachments = [{
            "fname": f"Announcement_{doc.name}.pdf",
            "content": pdf_content
        }]

        # Include an additional attachment if the document has an associated file
        if doc.attach and frappe.get_all("File", filters={"name": doc.attach}):
            file_doc = frappe.get_doc("File", doc.attach)
            attachments.append({
                "fname": file_doc.name,
                "content": file_doc.filedata
            })
        else:
            frappe.msgprint(f"File {doc.attach} not found.")

        # Send email to the specified recipients
        frappe.sendmail(
            recipients=recipients,
            subject=doc.title,
            content=content,
            attachments=attachments,
            delayed=False
        )

    except Exception as e:
        # Log an error if there is an exception during the email sending process
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error(
            "line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()),
            "Email Notification From Announcement Doctype"
        )

