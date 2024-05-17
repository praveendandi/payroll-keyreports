

frappe.pages['my-team'].on_page_load = function (wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "My Team Details",
        single_column: true
    });

    // Create a parent div to contain all the individual number cards
    let parentDiv = $('<div> </div>').appendTo(page.body);
    parentDiv[0].style.display = 'flex';
    parentDiv[0].style.alignItems = 'center';
    parentDiv[0].style.gap = '10px';
    parentDiv[0].style.flexWrap = 'wrap';
    fetchDataAndCreateCards();

    function createEmployeeNumberCards(employee) {
       
        let employee_name = employee.employee_name;
        let department = employee.department;
        let employee_id = employee.employee;
        let mobile_no = employee.cell_number;
        let prefered_email = employee.prefered_email;

        let numberCard = `<div class="number-card" style="margin-bottom: 5px; padding: 5px; border: 1px solid lightgrey; background: White;width: 30%;">
            <div style='display:flex;'>
                
                <div class="card-value"><b> ${employee_name} </b></div>
            </div>
            <div style='display:flex;'>
                <div class="card-title">Department : </div>
                <div class="card-value">${department} </div>
            </div>
            <div style='display:flex;'>
                <div class="card-title">Employee ID : </div>
                <div class="card-value">${employee_id} </div>
            </div>
            <div style='display:flex;'>
                <div class="card-title">Mobile No : </div>
                <div class="card-value">${mobile_no} </div>
            </div>
            <div style='display:flex;'>
                <div class="card-title">Mail : </div>
                <div class="card-value">${prefered_email} </div>
            </div>
        </div>`;

        return numberCard;
    }

    function fetchDataAndCreateCards() {
        frappe.call({
            method: 'payroll_key_reports.payroll_key_reports.dashboards.my_team',
            callback: function (response) {
                console.log(response.message, "//////////////////////");

                if (response.message.length > 0) {
                    for (let i = 0; i < response.message.length; i++) {
                        let employee = response.message[i];
                        let numberCard = createEmployeeNumberCards(employee);
                        parentDiv.append(numberCard); // Append to the parent div
                    }
                } else {
                    console.error("Error fetching data from API");
                }
            }
        });
    }
};

