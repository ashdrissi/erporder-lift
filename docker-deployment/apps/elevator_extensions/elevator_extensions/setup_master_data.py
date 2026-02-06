import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_item_customizations():
    # (Previous Item fields - relying on idempotency or commented out)
    pass

def setup_transaction_customizations():
    print("Setting up Transaction customizations...")
    fields = [
        {
            "fieldname": "total_volume",
            "label": "Total Volume (m3)",
            "fieldtype": "Float",
            "insert_after": "total_net_weight",
            "read_only": 1,
            "precision": "4"
        },
        {
            "fieldname": "recommended_transport",
            "label": "Recommended Transport",
            "fieldtype": "Data",
            "insert_after": "total_volume",
            "read_only": 1
        }
    ]
    
    custom_fields = {
        "Sales Order": fields,
        "Delivery Note": fields,
        "Quotation": fields
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.db.commit()
    print("Transaction customizations created.")

def run():
    setup_transaction_customizations()

if __name__ == "__main__":
    run()
