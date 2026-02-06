import frappe
from frappe.utils import nowdate, add_days

def create_portal_test_data():
    """Create test Customer, User, Contact, and Quotation for B2B portal testing"""
    
    # Test data with strong password
    customer_name = "Acme Elevators"
    user_email = "portal@acme.test"
    user_password = "P0rtal$ecure2026!"
    
    print("Creating B2B Portal Test Data...")
    
    # 1. Create User (Website User role for portal access)
    if not frappe.db.exists("User", user_email):
        user = frappe.new_doc("User")
        user.email = user_email
        user.first_name = "Portal"
        user.last_name = "User"
        user.new_password = user_password
        user.send_welcome_email = 0
        user.user_type = "Website User"
        user.append("roles", {"role": "Customer"})
        user.flags.ignore_password_policy = True
        user.insert(ignore_permissions=True)
        print(f"Created User: {user_email}")
    else:
        print(f"User {user_email} already exists")
    
    # 2. Create Customer
    if not frappe.db.exists("Customer", customer_name):
        customer = frappe.new_doc("Customer")
        customer.customer_name = customer_name
        customer.customer_type = "Company"
        customer.customer_group = "Installer"
        customer.territory = "All Territories"
        customer.insert(ignore_permissions=True)
        print(f"Created Customer: {customer_name}")
    else:
        print(f"Customer {customer_name} already exists")
    
    # 2b. Add portal user to Customer's portal_users table (REQUIRED for ERPNext portal)
    # ERPNext uses this table (not Contact Dynamic Links) to determine portal user access
    customer = frappe.get_doc("Customer", customer_name)
    existing_portal_users = [pu.user for pu in customer.portal_users]
    if user_email not in existing_portal_users:
        customer.append("portal_users", {"user": user_email})
        customer.save(ignore_permissions=True)
        print(f"Added {user_email} to Customer portal_users")
    
    # 3. Create Contact linking User to Customer
    existing_contact = frappe.db.exists("Contact", {"email_id": user_email})
    if not existing_contact:
        contact = frappe.new_doc("Contact")
        contact.first_name = "Portal"
        contact.last_name = "User"
        contact.email_id = user_email
        contact.user = user_email
        contact.append("links", {
            "link_doctype": "Customer",
            "link_name": customer_name
        })
        contact.append("email_ids", {
            "email_id": user_email,
            "is_primary": 1
        })
        contact.insert(ignore_permissions=True)
        print(f"Created Contact linking {user_email} to {customer_name}")
    else:
        print(f"Contact for {user_email} already exists")
    
    # 4. Create Test Item (if not exists)
    item_code = "Test-Lift-Motor"
    if not frappe.db.exists("Item", item_code):
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = "Test Lift Motor"
        item.item_group = "All Item Groups"
        item.stock_uom = "Nos"
        item.volume = 2.0
        item.standard_rate = 500
        item.insert(ignore_permissions=True)
        print(f"Created Item: {item_code}")
    else:
        # Update volume if needed
        frappe.db.set_value("Item", item_code, "volume", 2.0)
        print(f"Item {item_code} already exists (volume set to 2.0)")
    
    # 5. Create Quotation for this Customer
    qo = frappe.new_doc("Quotation")
    qo.party_name = customer_name
    qo.transaction_date = nowdate()
    qo.valid_till = add_days(nowdate(), 10)
    qo.append("items", {
        "item_code": item_code,
        "qty": 5,
        "rate": 500
    })
    qo.save(ignore_permissions=True)
    qo.submit()
    print(f"Created and Submitted Quotation: {qo.name}")
    
    frappe.db.commit()
    
    print("\n" + "="*50)
    print("B2B PORTAL TEST DATA CREATED")
    print("="*50)
    print(f"Customer: {customer_name}")
    print(f"Quotation: {qo.name}")
    print(f"\nPORTAL LOGIN:")
    print(f"  URL: http://erpnext.localhost:8000/login")
    print(f"  Email: {user_email}")
    print(f"  Password: {user_password}")
    print(f"\nAfter login, visit: http://erpnext.localhost:8000/quotations")
    print("="*50)

def run():
    create_portal_test_data()

if __name__ == "__main__":
    run()
