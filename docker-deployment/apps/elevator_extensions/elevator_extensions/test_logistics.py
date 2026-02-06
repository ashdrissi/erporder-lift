import frappe

def test_logistics_logic():
    print("Testing Logistics Logic...")
    
    # 1. Setup Item with Volume
    item_code = "Test-Lift-Motor"
    if not frappe.db.exists("Item", item_code):
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = "Test Lift Motor"
        item.item_group = "All Item Groups"
        item.stock_uom = "Nos"
        item.volume = 2.0 # 2 m3 per unit
        item.insert(ignore_permissions=True)
        print(f"Created Item: {item_code} with Volume 2.0")
    else:
        # Ensure volume is set
        doc = frappe.get_doc("Item", item_code)
        if doc.volume != 2.0:
            doc.volume = 2.0
            doc.save()
            print(f"Updated Item: {item_code} volume to 2.0")

    # 2. Setup Dummy Customer
    customer = "Test Client A"
    if not frappe.db.exists("Customer", customer):
        cust = frappe.new_doc("Customer")
        cust.customer_name = customer
        cust.customer_type = "Company"
        cust.insert(ignore_permissions=True)
        print(f"Created Customer: {customer}")

    # 3. Create Quotation with 10 units (Total 20 m3)
    # 20 m3 should recommend "20ft Container" (since <= 28)
    
    qo = frappe.new_doc("Quotation")
    qo.party_name = customer
    qo.transaction_date = frappe.utils.nowdate()
    qo.append("items", {
        "item_code": item_code,
        "qty": 10
    })
    
    try:
        qo.save(ignore_permissions=True) # This triggers 'validate' hook
        print(f"Created Quote: {qo.name}")
        print(f"Total Volume: {qo.total_volume}")
        print(f"Recommended Transport: {qo.recommended_transport}")
        
        expected = "20ft Container"
        if qo.recommended_transport == expected:
            print("✅ TEST PASSED: Recommendation correct.")
        else:
            print(f"❌ TEST FAILED: Expected '{expected}', got '{qo.recommended_transport}'")
            
    except Exception as e:
        print(f"❌ Error saving Quotation: {e}")

if __name__ == "__main__":
    test_logistics_logic()
