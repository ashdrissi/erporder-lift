import frappe

def setup_customer_groups():
    """Create Customer Groups: Installer, Distributor, Internal"""
    print("Setting up Customer Groups...")
    
    groups = ["Installer", "Distributor", "Internal"]
    parent_group = "All Customer Groups"
    
    for group_name in groups:
        if not frappe.db.exists("Customer Group", group_name):
            cg = frappe.new_doc("Customer Group")
            cg.customer_group_name = group_name
            cg.parent_customer_group = parent_group
            cg.insert(ignore_permissions=True)
            print(f"Created Customer Group: {group_name}")
        else:
            print(f"Customer Group {group_name} already exists")
    
    frappe.db.commit()
    print("Customer Groups setup complete.")

def setup_price_lists():
    """Create Price Lists for different zones"""
    print("Setting up Price Lists...")
    
    price_lists = [
        {"name": "Zone A - Local", "currency": "EUR"},
        {"name": "Zone B - Export Europe", "currency": "EUR"},
        {"name": "Zone C - Export International", "currency": "USD"}
    ]
    
    for pl in price_lists:
        if not frappe.db.exists("Price List", pl["name"]):
            doc = frappe.new_doc("Price List")
            doc.price_list_name = pl["name"]
            doc.currency = pl["currency"]
            doc.selling = 1
            doc.enabled = 1
            doc.insert(ignore_permissions=True)
            print(f"Created Price List: {pl['name']}")
        else:
            print(f"Price List {pl['name']} already exists")
    
    frappe.db.commit()
    print("Price Lists setup complete.")

def setup_pricing_rules():
    """Create Volume-based Pricing Rules with correct child table"""
    print("Setting up Pricing Rules...")
    
    rules = [
        {"title": "Volume Discount 5%", "min_qty": 10, "discount": 5},
        {"title": "Volume Discount 10%", "min_qty": 50, "discount": 10},
        {"title": "Volume Discount 15%", "min_qty": 100, "discount": 15}
    ]
    
    for rule in rules:
        if not frappe.db.exists("Pricing Rule", rule["title"]):
            pr = frappe.new_doc("Pricing Rule")
            pr.title = rule["title"]
            pr.apply_on = "Item Group"
            pr.selling = 1
            pr.min_qty = rule["min_qty"]
            pr.rate_or_discount = "Discount Percentage"
            pr.discount_percentage = rule["discount"]
            pr.priority = 1
            pr.valid_from = frappe.utils.nowdate()
            # Use correct child table for Item Group
            pr.append("item_groups", {
                "item_group": "All Item Groups"
            })
            pr.insert(ignore_permissions=True)
            print(f"Created Pricing Rule: {rule['title']}")
        else:
            print(f"Pricing Rule {rule['title']} already exists")
    
    frappe.db.commit()
    print("Pricing Rules setup complete.")

def setup_sales_partners():
    """Create Sales Partners for Commission tracking"""
    print("Setting up Sales Partners...")
    
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
            sp.insert(ignore_permissions=True)
            print(f"Created Sales Partner: {p['name']} ({p['commission_rate']}%)")
        else:
            print(f"Sales Partner {p['name']} already exists")
    
    frappe.db.commit()
    print("Sales Partners setup complete.")

def run():
    setup_customer_groups()
    setup_price_lists()
    setup_pricing_rules()
    setup_sales_partners()

if __name__ == "__main__":
    run()
