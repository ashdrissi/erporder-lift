import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_portal_settings():
    """Enable Customer Portal and configure settings"""
    print("Configuring Portal Settings...")
    
    # Enable Customer Portal
    portal_settings = frappe.get_single("Portal Settings")
    portal_settings.show_sidebar = 1
    portal_settings.save(ignore_permissions=True)
    
    # Enable Quotation in Portal
    # Check if standard Quotation portal page exists
    print("Portal Settings updated.")
    frappe.db.commit()

def add_portal_accept_field():
    """Add 'Accepted by Customer' field to Quotation for portal confirmation"""
    print("Adding Quotation portal fields...")
    
    custom_fields = {
        "Quotation": [
            {
                "fieldname": "customer_accepted",
                "label": "Accepted by Customer",
                "fieldtype": "Check",
                "insert_after": "status",
                "read_only": 1,
                "allow_on_submit": 1
            },
            {
                "fieldname": "customer_accepted_on",
                "label": "Accepted On",
                "fieldtype": "Datetime",
                "insert_after": "customer_accepted",
                "read_only": 1,
                "allow_on_submit": 1
            },
            {
                "fieldname": "customer_remarks",
                "label": "Customer Remarks",
                "fieldtype": "Small Text",
                "insert_after": "customer_accepted_on",
                "allow_on_submit": 1
            }
        ]
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.db.commit()
    print("Quotation portal fields created.")

def run():
    setup_portal_settings()
    add_portal_accept_field()

if __name__ == "__main__":
    run()
