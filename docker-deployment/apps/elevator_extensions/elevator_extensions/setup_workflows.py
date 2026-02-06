import frappe

def create_stock_transfer_workflow():
    """Create simplified workflow for Stock Entry (Material Transfer)"""
    print("Creating Stock Transfer Workflow...")
    
    workflow_name = "Stock Transfer Approval"
    
    if frappe.db.exists("Workflow", workflow_name):
        print(f"Workflow {workflow_name} already exists")
        return
    
    wf = frappe.new_doc("Workflow")
    wf.workflow_name = workflow_name
    wf.document_type = "Stock Entry"
    wf.is_active = 1
    wf.send_email_alert = 0
    
    # Simplified states - avoid cancelled (doc_status 2) from submitted (1)
    states = [
        {"state": "Draft", "doc_status": "0", "allow_edit": "Stock User"},
        {"state": "Pending Approval", "doc_status": "0", "allow_edit": "Stock Manager"},
        {"state": "Approved", "doc_status": "1", "allow_edit": "Administrator"},
        {"state": "Rejected", "doc_status": "0", "allow_edit": "Stock User"}
    ]
    
    for s in states:
        wf.append("states", {
            "state": s["state"],
            "doc_status": s["doc_status"],
            "allow_edit": s["allow_edit"]
        })
    
    transitions = [
        {"state": "Draft", "action": "Request Transfer", "next_state": "Pending Approval", "allowed": "Stock User"},
        {"state": "Pending Approval", "action": "Approve", "next_state": "Approved", "allowed": "Stock Manager"},
        {"state": "Pending Approval", "action": "Reject", "next_state": "Rejected", "allowed": "Stock Manager"},
        {"state": "Rejected", "action": "Revise", "next_state": "Draft", "allowed": "Stock User"}
    ]
    
    for t in transitions:
        wf.append("transitions", {
            "state": t["state"],
            "action": t["action"],
            "next_state": t["next_state"],
            "allowed": t["allowed"]
        })
    
    wf.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Created Workflow: {workflow_name}")

def create_purchase_workflow():
    """Create workflow for Purchase Order approval"""
    print("Creating Purchase Order Workflow...")
    
    workflow_name = "Purchase Order Approval"
    
    if frappe.db.exists("Workflow", workflow_name):
        print(f"Workflow {workflow_name} already exists")
        return
    
    wf = frappe.new_doc("Workflow")
    wf.workflow_name = workflow_name
    wf.document_type = "Purchase Order"
    wf.is_active = 1
    wf.send_email_alert = 0
    
    states = [
        {"state": "Draft", "doc_status": "0", "allow_edit": "Purchase User"},
        {"state": "Pending Approval", "doc_status": "0", "allow_edit": "Purchase Manager"},
        {"state": "Approved", "doc_status": "1", "allow_edit": "Administrator"},
        {"state": "Rejected", "doc_status": "0", "allow_edit": "Purchase User"}
    ]
    
    for s in states:
        wf.append("states", {
            "state": s["state"],
            "doc_status": s["doc_status"],
            "allow_edit": s["allow_edit"]
        })
    
    transitions = [
        {"state": "Draft", "action": "Submit for Approval", "next_state": "Pending Approval", "allowed": "Purchase User"},
        {"state": "Pending Approval", "action": "Approve", "next_state": "Approved", "allowed": "Purchase Manager"},
        {"state": "Pending Approval", "action": "Reject", "next_state": "Rejected", "allowed": "Purchase Manager"},
        {"state": "Rejected", "action": "Revise", "next_state": "Draft", "allowed": "Purchase User"}
    ]
    
    for t in transitions:
        wf.append("transitions", {
            "state": t["state"],
            "action": t["action"],
            "next_state": t["next_state"],
            "allowed": t["allowed"]
        })
    
    wf.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Created Workflow: {workflow_name}")

def run():
    create_stock_transfer_workflow()
    create_purchase_workflow()

if __name__ == "__main__":
    run()
