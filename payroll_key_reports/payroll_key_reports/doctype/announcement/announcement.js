// Copyright (c) 2024, caratRED Technologies LLP and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Announcement', {
// 	on_submit: async (frm) => {
// 		let promise = new Promise((resolve, reject) => {
// 			if (frm.doc.workflow_state == "Open") {
// 				frappe.confirm(
// 					"<b>Do you want to send announcement mail notification to the employee?</b>",
// 					() => Yes(),
// 					() => No()
// 				);
// 			}
// 		});
// 		await promise.catch(() => frappe.throw());
// }
// });



frappe.ui.form.on('Announcement', {
	// refresh: function(frm) {

	// }
});
