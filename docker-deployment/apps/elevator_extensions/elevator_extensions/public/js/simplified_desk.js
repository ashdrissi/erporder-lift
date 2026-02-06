// simplified_desk.js - Custom JS to simplify ERPNext Desk UI

// Example: Run code on every page load
/*
$(document).on('app_ready', function() {
    // Hide specific global elements or triggers
});
*/

// Example: Customize specific DocType forms globally
/*
frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        // Simplify the form by hiding less used buttons
        frm.remove_custom_button('Create Subscription');
        
        // Hide standard fields that you can't hide via 'Customize Form'
        // frm.set_df_property('some_field', 'hidden', 1);
    }
});
*/
