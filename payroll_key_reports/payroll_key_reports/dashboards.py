import frappe
import erpnext
from datetime import date
from datetime import datetime
from frappe.utils import now
import time



@frappe.whitelist()
def get_next_holiday():
    # user = frappe.session.user
    
    holidays_list = frappe.db.get_list(
        "Holiday List",
        filters=[
            ["Holiday List", "from_date", "Timespan", "this year"],
            ['Holiday', 'weekly_off', '=', 0],
        ],
        fields=["name", 'holidays.holiday_date', 'holidays.description'],
        order_by='holiday_date Asc'
    )

    list_of_holidays = []
    

    for holiday in holidays_list:
        if date.today() < holiday['holiday_date']:
            list_of_holidays.append(holiday)

    if list_of_holidays:
        holiday_date = list_of_holidays[0]['holiday_date'].strftime('%a, %d %B, %Y')
        description = list_of_holidays[0]['description']
        
        message = f"""
        <div>
        <div>
       <h5 style="margin:0;color:green">{description}</h5>
       </div>
       <div>
           <p style="font-size:12px;margin-top:9px;color:red">{holiday_date}</p>
       </div>   
        </div>
        """
        return message
    

@frappe.whitelist()
def employee_on_leave():
    try:
        user = frappe.session.user
        # user_permission = frappe.db.get_list("User Permission",{"user":user,"allow":"Employee"},["for_value"])
        # if len(user_permission)>0:
        employee_leave_data = frappe.db.get_list("Attendance",
                                                filters={"attendance_date":date.today(),"docstatus":1,"status":'On Leave'},fields=["employee_name","attendance_date",'status'],ignore_permissions=True)
        
        
        message = """"""
        if len(employee_leave_data) > 0:
            for each in employee_leave_data:
                message +=f"""<span style='font-size:12px;'>{each['employee_name']},</span>  """
            
        else:
            message += f"""<span style='font-size:12px;'>Everyone is at Office</span>"""

        return message
    
    except Exception as e:
        frappe.log_error(str(e) + "Attendance Regularized")
    
@frappe.whitelist()

def today_date_time():
    user = frappe.session.user
    current_datetime = datetime.now()
    today_date = current_datetime.strftime("%A, %Y-%m-%d %H:%M:%S")
    message = f"<span style='font-size:12px;'>{today_date}</span>"
    return message


@frappe.whitelist()
def employee_brithdays():
    try:
        # user = frappe.session.user
        birthdays_list = frappe.db.get_list("Employee",['employee_name','date_of_birth'],ignore_permissions=True)
        birthday_list = []
        today = date.today()
        
        for birthday in birthdays_list:
            birth_date = birthday['date_of_birth']
            
            birth_month_day = (birth_date.month, birth_date.day)
            
            current_month_day = (today.month, today.day)
            
            if current_month_day == birth_month_day:
                birthday_list.append(birthday)
        if len(birthday_list) > 0:        
            message = f"<span style='font-size:12px;'>🎂{ birthday_list[0]['employee_name']}</span>"
        else:
            message = f"<span style='font-size:12px;'>🎂 No Birthdays Today.</span>"
        
        return message
    
    except Exception as e:
        frappe.log_error(str(e) + "birthday")



@frappe.whitelist()

def announcement():
    return ""

@frappe.whitelist()
def my_team():
    try:
        team_list = []
        user = frappe.session.user
        user_list = frappe.db.get_list("Employee",filters={'user_id':user},
                                        fields=["employee_name",'user_id','department']
                                        )
        if user == 'Administrator':
            my_team_data = frappe.db.get_all("Employee",['employee','employee_name','department','cell_number','prefered_email'])
            
            for i in my_team_data:
                team_list.append(i)
    
        else :
            user_department = user_list[0]['department']
            my_team_data = frappe.db.get_all("Employee",['employee','employee_name','department','cell_number'])
            
            for i in my_team_data:
                if user_department == i['department']:
                    team_list.append(i)
                    user_photo = frappe.db.get_all("File",filters={"attached_to_name":i.employee},fields=["file_url"])
                   
                     

        return team_list
    except Exception as e:
        frappe.log_error(str(e))
    
            
@frappe.whitelist()
def attendance_list():
    try:
        total_present = []
        on_leave = []
        work_from_home = []
        user = frappe.session.user
        user_permission = frappe.db.get_list("User Permission",{"user":user,"allow":"Employee"},["for_value"],ignore_permissions = True)
        if len(user_permission)>0:
            employee_leave_data = frappe.db.get_list("Attendance",
                                                    filters={"attendance_date":date.today(),"docstatus":1},fields=["employee_name","attendance_date",'status'])
            print(employee_leave_data)
            if len(employee_leave_data) > 0:
                attendance_date = employee_leave_data[0]['attendance_date'].strftime('%a, %d %B, %Y')
                status = employee_leave_data[0]['status']
                
                message = f"""
                    <div>
                    <div>
                <h5 style="margin:0;color:palevioletred">{status}</h5>
                </div>
                <div>
                    <p style="font-size:12px;margin-top:-12px;">{attendance_date}</p>
                </div>   
                    </div>
                    """
                    
                return message
            else:
                message = f"<span style='font-size:12px;'>Attendance Regularized</span>"
                return message
        
        else:
            employee_leave_data_total = frappe.db.get_list("Attendance",
                                                    filters={"attendance_date":date.today(),"docstatus":1},fields=["employee_name","attendance_date",'status'])
            if len(employee_leave_data_total) > 0:
                for i in employee_leave_data_total:
                    if 'Present' == i['status']:
                        total_present.append(i)
                    if 'On Leave' == i['status']:
                        on_leave.append(i)
                    if 'Work From Home' == i['status']:
                        work_from_home.append(i)
                    
                    message = f"""
                        <div>
                        <div>
                        <h5 style="margin:0;color:blue">present : {len(total_present)}</h5>
                        </div>
                        <div>
                            <p style="font-size:15px;margin-top:-1px;color:palevioletred">on_leave : {len(on_leave)}</p>
                        </div>
                        <div>
                            <p style="font-size:15px;margin-top:-1px;color:green">Work From Home:{len(work_from_home)}</p>
                        </div>   
                            </div>
                            """
                    return message
            else :
                return ""
    except Exception as e:
        frappe.log_error(str(e) + "Attendance Regularized")        


    