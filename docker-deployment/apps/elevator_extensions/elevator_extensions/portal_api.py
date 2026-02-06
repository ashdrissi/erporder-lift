import frappe
from frappe import _

@frappe.whitelist()
def accept_quotation(quotation_name, remarks=None):
    """
    API for customers to accept a quotation via portal.
    This marks the quotation as accepted and can trigger order creation.
    """
    # Verify customer has access to this quotation
    quotation = frappe.get_doc("Quotation", quotation_name)
    
    # Check if user is the customer or has permission
    customer = frappe.db.get_value("Contact", {"user": frappe.session.user}, "name")
    if not customer and frappe.session.user != "Administrator":
        frappe.throw(_("You do not have permission to accept this quotation"))
    
    # Mark as accepted
    quotation.db_set("customer_accepted", 1, update_modified=False)
    quotation.db_set("customer_accepted_on", frappe.utils.now(), update_modified=False)
    if remarks:
        quotation.db_set("customer_remarks", remarks, update_modified=False)
    
    frappe.db.commit()
    
    return {
        "status": "success",
        "message": _("Quotation {0} has been accepted").format(quotation_name)
    }

@frappe.whitelist()
def get_customer_quotations():
    """
    Get all quotations for the logged-in customer via portal.
    """
    user = frappe.session.user
    
    # Find customer linked to this user
    customer = frappe.db.get_value("Customer", {"email_id": user}, "name")
    if not customer:
        # Try via Contact
        contact = frappe.db.get_value("Contact", {"user": user}, "name")
        if contact:
            link = frappe.db.get_value("Dynamic Link", {
                "parent": contact,
                "link_doctype": "Customer"
            }, "link_name")
            customer = link
    
    if not customer:
        return []
    
    quotations = frappe.get_all("Quotation", 
        filters={
            "party_name": customer,
            "docstatus": ["<", 2]
        },
        fields=["name", "transaction_date", "grand_total", "status", "customer_accepted", "valid_till"]
    )
    
    return quotations


@frappe.whitelist()
def get_quotation_details(quotation_name):
    """
    Get detailed quotation info including items for the portal modal view.
    """
    user = frappe.session.user
    
    # Verify access
    customer = _get_customer_for_user(user)
    if not customer:
        frappe.throw(_("Access denied"))
    
    quotation = frappe.get_doc("Quotation", quotation_name)
    
    # Verify this quotation belongs to the customer
    if quotation.party_name != customer:
        frappe.throw(_("Access denied"))
    
    # Return quotation details with items
    return {
        "name": quotation.name,
        "party_name": quotation.party_name,
        "transaction_date": str(quotation.transaction_date),
        "valid_till": str(quotation.valid_till) if quotation.valid_till else None,
        "grand_total": quotation.grand_total,
        "currency": quotation.currency,
        "terms": quotation.terms,
        "customer_accepted": quotation.get("customer_accepted", 0),
        "customer_declined": quotation.get("customer_declined", 0),
        "items": [
            {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount,
                "uom": item.uom
            }
            for item in quotation.items
        ]
    }


@frappe.whitelist()
def decline_quotation(quotation_name, reason=None):
    """
    API for customers to decline a quotation via portal.
    """
    user = frappe.session.user
    
    # Verify access
    customer = _get_customer_for_user(user)
    if not customer:
        frappe.throw(_("Access denied"))
    
    quotation = frappe.get_doc("Quotation", quotation_name)
    
    # Verify this quotation belongs to the customer
    if quotation.party_name != customer:
        frappe.throw(_("Access denied"))
    
    # Mark as declined
    quotation.db_set("customer_declined", 1, update_modified=False)
    quotation.db_set("customer_declined_on", frappe.utils.now(), update_modified=False)
    if reason:
        quotation.db_set("customer_remarks", reason, update_modified=False)
    
    frappe.db.commit()
    
    return {
        "status": "success",
        "message": _("Quotation {0} has been declined").format(quotation_name)
    }


def _get_customer_for_user(user):
    """Helper to get customer linked to a portal user."""
    # Try direct customer lookup
    customer = frappe.db.get_value("Customer", {"email_id": user}, "name")
    if customer:
        return customer
    
    # Try via Portal User table (ERPNext standard)
    from frappe.query_builder import DocType
    PortalUser = DocType("Portal User")
    result = (
        frappe.qb.from_(PortalUser)
        .select(PortalUser.parent)
        .where(PortalUser.user == user)
        .where(PortalUser.parenttype == "Customer")
        .run(pluck="parent")
    )
    if result:
        return result[0]
    
    # Try via Contact Dynamic Link
    contact = frappe.db.get_value("Contact", {"user": user}, "name")
    if contact:
        link = frappe.db.get_value("Dynamic Link", {
            "parent": contact,
            "link_doctype": "Customer"
        }, "link_name")
        return link
    
    return None
