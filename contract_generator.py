"""
Syntax Line - Software Development Service Agreement PDF Generator
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.graphics import renderPDF

# Colors
PRIMARY_COLOR = HexColor("#1a365d")  # Deep Navy Blue
ACCENT_COLOR = HexColor("#3182ce")   # Bright Blue
LIGHT_ACCENT = HexColor("#ebf8ff")   # Light Blue
DARK_TEXT = HexColor("#2d3748")      # Dark Gray
LIGHT_TEXT = HexColor("#718096")     # Light Gray


def create_header(canvas_obj, doc):
    """Draw the header with logo on each page"""
    canvas_obj.saveState()
    
    # Smaller header background (70px instead of 100px)
    header_height = 70
    canvas_obj.setFillColor(PRIMARY_COLOR)
    canvas_obj.rect(0, A4[1] - header_height, A4[0], header_height, fill=1, stroke=0)
    
    # Draw the actual logo image
    logo_path = "/Users/achraf/.gemini/antigravity/brain/39c32483-501e-485a-9155-bfa9558e99c5/syntaxline_logo_1769021368116.png"
    try:
        canvas_obj.drawImage(logo_path, 30, A4[1] - 60, width=45, height=45, mask='auto')
    except:
        # Fallback geometric logo if image fails
        canvas_obj.setFillColor(ACCENT_COLOR)
        canvas_obj.circle(52, A4[1] - 35, 20, fill=1, stroke=0)
        canvas_obj.setFillColor(white)
        canvas_obj.circle(52, A4[1] - 35, 12, fill=1, stroke=0)
        canvas_obj.setFillColor(PRIMARY_COLOR)
        canvas_obj.circle(52, A4[1] - 35, 6, fill=1, stroke=0)
    
    # Company Name
    canvas_obj.setFillColor(white)
    canvas_obj.setFont("Helvetica-Bold", 20)
    canvas_obj.drawString(85, A4[1] - 35, "Syntax Line")
    
    # Tagline
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(HexColor("#a0c4e8"))
    canvas_obj.drawString(85, A4[1] - 50, "Custom Software Solutions & ERP Implementation")
    
    # Decorative line at bottom of header
    canvas_obj.setStrokeColor(ACCENT_COLOR)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(30, A4[1] - header_height, A4[0] - 30, A4[1] - header_height)
    
    canvas_obj.restoreState()


def create_footer(canvas_obj, doc):
    """Draw the footer on each page"""
    canvas_obj.saveState()
    
    # Footer line
    canvas_obj.setStrokeColor(LIGHT_TEXT)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(40, 40, A4[0] - 40, 40)
    
    # Page number
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(LIGHT_TEXT)
    canvas_obj.drawCentredString(A4[0] / 2, 25, f"Page {doc.page}")
    
    # Confidential notice
    canvas_obj.setFont("Helvetica-Oblique", 8)
    canvas_obj.drawString(40, 25, "Confidential - Syntax Line")
    
    canvas_obj.restoreState()


def header_footer(canvas_obj, doc):
    create_header(canvas_obj, doc)
    create_footer(canvas_obj, doc)


def generate_contract():
    """Generate the PDF contract"""
    
    doc = SimpleDocTemplate(
        "/Users/achraf/Downloads/Dev/Erpnext/erpnext/SyntaxLine_Service_Agreement_Orderlift.pdf",
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=90,
        bottomMargin=60
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=PRIMARY_COLOR,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_TEXT,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=PRIMARY_COLOR,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        borderColor=ACCENT_COLOR,
        borderWidth=0,
        borderPadding=0,
    )
    
    subsection_style = ParagraphStyle(
        'Subsection',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=ACCENT_COLOR,
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        textColor=DARK_TEXT,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=4
    )
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("SOFTWARE DEVELOPMENT SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 10))
    
    # Project reference box
    story.append(Paragraph("<b>Project Reference:</b> Custom ERP Implementation (V0) – Multi-Company & Logistics", subtitle_style))
    story.append(Paragraph("<b>Date:</b> January 22, 2026", subtitle_style))
    story.append(Spacer(1, 15))
    
    # Parties
    parties_data = [
        ["<b>Provider:</b>", "Syntax Line (Represented by Achraf Drissi El Bouzaidi and Reda Drissi El Bouzaidi)"],
        ["<b>Client:</b>", "Orderlift"]
    ]
    parties_table = Table([[Paragraph(cell, body_style) for cell in row] for row in parties_data], colWidths=[80, 400])
    parties_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_TEXT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 1, ACCENT_COLOR),
    ]))
    story.append(parties_table)
    
    # Section 1
    story.append(Paragraph("1. Executive Summary", section_style))
    story.append(Paragraph(
        "Syntax Line proposes to develop and deploy a comprehensive, custom-tailored ERP solution. "
        "The Solution will be architected to address the specific functional requirements of Orderlift (V0), "
        "focusing on centralized multi-company management, automated logistics optimization, and a dedicated B2B client portal.",
        body_style
    ))
    
    # Section 2
    story.append(Paragraph("2. Scope of Work (The Deliverables)", section_style))
    story.append(Paragraph(
        "Syntax Line will configure, develop, and deploy a secure, cloud-based system to meet the following requirements:",
        body_style
    ))
    
    # 2A
    story.append(Paragraph("A. Core System Architecture", subsection_style))
    story.append(Paragraph("• <b>Multi-Entity Structure:</b> Configuration of a centralized Parent Company (Manufacturing/Export) and connected Antenna Companies (Distribution/Installation).", bullet_style))
    story.append(Paragraph("• <b>Inventory Logic:</b> Setup of multi-warehouse management including real stock, transit stock, and reserved stock logic.", bullet_style))
    story.append(Paragraph("• <b>Centralized Database:</b> Migration and structuring of the \"Base Articles\" (Item Master) to ensure data consistency across all entities.", bullet_style))
    story.append(Paragraph("• <b>Sales Ecosystem:</b> Implementation of the complete Order-to-Cash workflow with automated commission calculations.", bullet_style))
    
    # 2B
    story.append(Paragraph("B. Custom Development & Modules", subsection_style))
    story.append(Paragraph("• <b>B2B Client Portal:</b> Development of a secure web interface for clients to place orders, featuring dynamic pricing logic based on geography and volume.", bullet_style))
    story.append(Paragraph("• <b>Logistics Intelligence Module:</b> Development of a proprietary algorithm to calculate shipment volume/weight and automatically recommend the optimal Container or Truck type.", bullet_style))
    story.append(Paragraph("• <b>Automated Documentation:</b> Coding of dynamic PDF generators for Invoices, Packing Lists, and Delivery Notes to match Orderlift's corporate branding.", bullet_style))
    
    # 2C
    story.append(Paragraph("C. Training & Knowledge Transfer", subsection_style))
    story.append(Paragraph("• <b>Video Library:</b> Provision of a dedicated library of training videos (screen recordings) covering all key operational workflows.", bullet_style))
    story.append(Paragraph("• <b>Live Training:</b> Three (3) interactive Zoom training sessions (2 hours each) for administrators and key stakeholders.", bullet_style))
    
    # Section 3
    story.append(Paragraph("3. Timeline & Phases", section_style))
    story.append(Paragraph("<b>Total Estimated Duration: 10 - 12 Weeks</b>", body_style))
    
    story.append(Paragraph("<b>Phase 1: Foundation (Weeks 1-4)</b>", bullet_style))
    story.append(Paragraph("• Server provisioning, Security setup (SSL/Firewall), and Core Engine installation.", bullet_style))
    story.append(Paragraph("• Database structuring and initial data import (Items, Customers).", bullet_style))
    
    story.append(Paragraph("<b>Phase 2: Custom Development (Weeks 5-8)</b>", bullet_style))
    story.append(Paragraph("• Development of the Logistics/Container algorithm.", bullet_style))
    story.append(Paragraph("• Construction of the B2B Portal and Pricing Engine.", bullet_style))
    story.append(Paragraph("• <i>Checkpoint:</i> First demonstration of custom features.", bullet_style))
    
    story.append(Paragraph("<b>Phase 3: UAT & Refinement (Weeks 9-10)</b>", bullet_style))
    story.append(Paragraph("• User Acceptance Testing (Client tests the system in a staging environment).", bullet_style))
    story.append(Paragraph("• Execution of Revisions (see Section 5).", bullet_style))
    
    story.append(Paragraph("<b>Phase 4: Go-Live (Weeks 11-12)</b>", bullet_style))
    story.append(Paragraph("• Final data migration.", bullet_style))
    story.append(Paragraph("• Live Training sessions.", bullet_style))
    story.append(Paragraph("• System handover and production launch.", bullet_style))
    
    # Section 4
    story.append(Paragraph("4. Financial Proposal", section_style))
    
    total_value_style = ParagraphStyle(
        'TotalValue',
        parent=body_style,
        fontSize=12,
        textColor=PRIMARY_COLOR,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10
    )
    story.append(Paragraph("Total Project Value: $10,000.00 USD (Tax Excluded)", total_value_style))
    
    story.append(Paragraph(
        "<b>Payment Schedule:</b> Payments are structured to ensure project momentum and provide a guaranteed support period post-launch.",
        body_style
    ))
    
    payment_data = [
        ["Milestone", "Amount", "Due Date"],
        ["Project Initiation (Prepayment)", "$3,000 USD", "Upon signing this contract"],
        ["Delivery & Beta Launch", "$3,000 USD", "Upon deployment for UAT (Week 8-9)"],
        ["Stabilization & Support Retainer", "$4,000 USD", "4 monthly installments of $1,000 USD\nstarting 30 days after Beta Launch"]
    ]
    
    payment_table = Table(payment_data, colWidths=[180, 100, 200])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_ACCENT),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_TEXT),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, ACCENT_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(payment_table)
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "<i>The Stabilization period covers monitoring, bug fixes, and general support to ensure a smooth operational transition.</i>",
        body_style
    ))
    
    # Section 5
    story.append(Paragraph("5. Revision Policy", section_style))
    story.append(Paragraph(
        "To ensure the project remains agile while adhering to the timeline, the Client is entitled to <b>three (3) comprehensive rounds of grouped revisions</b> during the development phase.",
        body_style
    ))
    story.append(Paragraph(
        "The Client shall consolidate all feedback for each round into a single list of requests. This \"batching\" of edits allows Syntax Line to implement changes efficiently and ensures the system architecture remains stable throughout the development process.",
        body_style
    ))
    
    # Section 6
    story.append(Paragraph("6. Confidentiality", section_style))
    story.append(Paragraph("Both parties agree to keep all technical and business information disclosed during this project strictly confidential.", body_style))
    story.append(Paragraph("• Syntax Line agrees not to disclose the Client's customer lists, pricing strategies, or trade secrets to any third party.", bullet_style))
    story.append(Paragraph("• The Client agrees not to disclose Syntax Line' development methods, proprietary algorithms, or source code to external competitors.", bullet_style))
    
    # Section 7
    story.append(Paragraph("7. Limitation of Liability", section_style))
    story.append(Paragraph(
        "Syntax Line shall not be liable for any indirect, incidental, special, or consequential damages, including but not limited to loss of profits, revenue, data, or use, incurred by the Client or any third party, whether in an action in contract or tort. The total liability of Syntax Line for any claim arising out of this Agreement shall not exceed the total amount paid by the Client to Syntax Line under this Agreement.",
        body_style
    ))
    
    # Section 8
    story.append(Paragraph("8. Change Orders", section_style))
    story.append(Paragraph(
        "Any request for features, functionality, or customizations not explicitly listed in Section 2 (Scope of Work) or exceeding the Revision Policy in Section 5 will be considered a \"Change Order.\" Syntax Line will provide a separate quote for the time and cost required for any such additions. Work on Change Orders will commence only upon written approval and payment of the agreed fee.",
        body_style
    ))
    
    # Section 9
    story.append(Paragraph("9. Technical Stack & Ownership", section_style))
    story.append(Paragraph("• <b>Technology:</b> The Solution is built on a modern, scalable Python & JavaScript architecture, utilizing a robust SQL database (MariaDB/Postgres). It is designed to be modular, allowing for future extensions (HR, Manufacturing) without rebuilding the core.", bullet_style))
    story.append(Paragraph("• <b>Ownership:</b> Upon full payment of the total project value, Orderlift will possess full ownership rights to the implemented system configuration and the source code of all custom modules developed by Syntax Line.", bullet_style))
    story.append(Paragraph("• <b>Hosting:</b> Syntax Line will configure the cloud hosting environment (VPS). Direct hosting costs (approx. $20-$40/month) are the responsibility of the Client.", bullet_style))
    
    # Section 10
    story.append(Paragraph("10. Agreement", section_style))
    story.append(Paragraph(
        "By signing below, both parties agree to the terms, scope, and payment schedule outlined above.",
        body_style
    ))
    story.append(Spacer(1, 30))
    
    # Signature boxes
    sig_style = ParagraphStyle(
        'Signature',
        parent=body_style,
        fontSize=10,
        leading=18
    )
    
    sig_data = [
        [
            Paragraph("<b>For Syntax Line:</b><br/><br/>Name: __________________<br/><br/>Date: __________________<br/><br/>Signature: __________________", sig_style),
            Paragraph("<b>For Orderlift:</b><br/><br/>Name: __________________<br/><br/>Date: __________________<br/><br/>Signature: __________________", sig_style)
        ]
    ]
    
    sig_table = Table(sig_data, colWidths=[240, 240])
    sig_table.setStyle(TableStyle([
        ('BOX', (0, 0), (0, 0), 1, PRIMARY_COLOR),
        ('BOX', (1, 0), (1, 0), 1, PRIMARY_COLOR),
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(sig_table)
    
    # Build PDF
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("✅ PDF contract generated successfully!")
    print("📄 File: SyntaxLine_Service_Agreement_Orderlift.pdf")


if __name__ == "__main__":
    generate_contract()
