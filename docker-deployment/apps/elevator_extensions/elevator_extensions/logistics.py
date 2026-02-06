import frappe

def calculate_logistics(doc, method):
    """
    Calculate Total Volume and Recommend Transport Type
    Hooked to: Quotation, Sales Order, Delivery Note (validate)
    Uses configurable settings from Logistics Settings DocType
    """
    total_volume = 0.0
    
    for item in doc.items:
        if not item.item_code:
            continue
            
        item_volume = frappe.db.get_value("Item", item.item_code, "volume") or 0.0
        row_volume = item_volume * item.qty
        total_volume += row_volume

    doc.total_volume = total_volume
    doc.recommended_transport = get_recommendation(total_volume)

def get_recommendation(volume):
    """Get transport recommendation based on configurable thresholds"""
    if volume <= 0:
        return "N/A"
    
    # Try to get settings from DocType, fall back to defaults
    try:
        settings = frappe.get_single("Logistics Settings")
        lcl_max = settings.lcl_max_volume or 15
        c20_max = settings.container_20ft_max_volume or 28
        c40_max = settings.container_40ft_max_volume or 58
        c40hq_max = settings.container_40ft_hq_max_volume or 68
        
        lcl_label = settings.lcl_label or "LCL (Shared Container) / Small Truck"
        c20_label = settings.container_20ft_label or "20ft Container"
        c40_label = settings.container_40ft_label or "40ft Container"
        c40hq_label = settings.container_40ft_hq_label or "40ft High Cube Container"
        multi_label = settings.multiple_containers_label or "Multiple Containers"
    except Exception:
        # Default values if settings don't exist yet
        lcl_max, c20_max, c40_max, c40hq_max = 15, 28, 58, 68
        lcl_label = "LCL (Shared Container) / Small Truck"
        c20_label = "20ft Container"
        c40_label = "40ft Container"
        c40hq_label = "40ft High Cube Container"
        multi_label = "Multiple Containers"
    
    if volume < lcl_max:
        return lcl_label
    elif volume <= c20_max:
        return c20_label
    elif volume <= c40_max:
        return c40_label
    elif volume <= c40hq_max:
        return c40hq_label
    else:
        containers_20 = int(volume / c20_max) + 1
        return f"{multi_label} (approx {containers_20} x 20ft)"
