import frappe

def fix_portal_permissions():
    """Add Customer role permissions to Quotation for portal access"""
    print("Fixing Portal Permissions for Quotation...")
    
    # 1. Add Customer role permission to Quotation
    doctype = "Quotation"
    
    # Check if permission exists
    existing = frappe.db.exists("Custom DocPerm", {
        "parent": doctype,
        "role": "Customer"
    })
    
    if not existing:
        # Add read permission for Customer role
        perm = frappe.new_doc("Custom DocPerm")
        perm.parent = doctype
        perm.parenttype = "DocType"
        perm.parentfield = "permissions"
        perm.role = "Customer"
        perm.read = 1
        perm.permlevel = 0
        perm.if_owner = 0
        perm.insert(ignore_permissions=True)
        print(f"Added Customer read permission to {doctype}")
    else:
        print(f"Customer permission already exists for {doctype}")
    
    # 2. Enable has_web_view for Quotation
    frappe.db.set_value("DocType", doctype, "has_web_view", 1)
    print(f"Enabled has_web_view for {doctype}")
    
    # 3. Clear cache
    frappe.clear_cache(doctype=doctype)
    
    frappe.db.commit()
    print("Portal permissions fixed!")

def run():
    fix_portal_permissions()

if __name__ == "__main__":
    run()
