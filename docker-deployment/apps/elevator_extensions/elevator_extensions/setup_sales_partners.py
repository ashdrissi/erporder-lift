import frappe

def setup_sales_partners():
    """Create Sales Partners for Commission tracking"""
    print("Setting up Sales Partners...")
    
    # Get default territory
    default_territory = frappe.db.get_single_value("Selling Settings", "territory") or "All Territories"
    
    partners = [
        {"name": "Agent Region North", "commission_rate": 5},
        {"name": "Agent Region South", "commission_rate": 7},
        {"name": "Agent International", "commission_rate": 10}
    ]
    
    for p in partners:
        if not frappe.db.exists("Sales Partner", p["name"]):
            sp = frappe.new_doc("Sales Partner")
            sp.partner_name = p["name"]
            sp.commission_rate = p["commission_rate"]
            sp.partner_type = "Reseller"
            sp.territory = default_territory
            sp.insert(ignore_permissions=True)
            print(f"Created Sales Partner: {p['name']} ({p['commission_rate']}%)")
        else:
            print(f"Sales Partner {p['name']} already exists")
    
    frappe.db.commit()
    print("Sales Partners setup complete.")

def run():
    setup_sales_partners()

if __name__ == "__main__":
    run()
