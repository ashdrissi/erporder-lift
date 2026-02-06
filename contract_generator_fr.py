"""
Syntax Line - Générateur de Contrat de Services de Développement Logiciel (Version Française)
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
    canvas_obj.drawString(85, A4[1] - 50, "Solutions Logicielles sur Mesure & Implémentation ERP")
    
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
    canvas_obj.drawString(40, 25, "Confidentiel - Syntax Line")
    
    canvas_obj.restoreState()


def header_footer(canvas_obj, doc):
    create_header(canvas_obj, doc)
    create_footer(canvas_obj, doc)


def generate_contract():
    """Generate the PDF contract"""
    
    doc = SimpleDocTemplate(
        "/Users/achraf/Downloads/Dev/Erpnext/erpnext/SyntaxLine_Contrat_Service_Orderlift.pdf",
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
    story.append(Paragraph("CONTRAT DE SERVICES DE DÉVELOPPEMENT LOGICIEL", title_style))
    story.append(Spacer(1, 10))
    
    # Project reference box
    story.append(Paragraph("<b>Référence du Projet:</b> Implémentation ERP sur Mesure (V0) – Multi-Sociétés & Logistique", subtitle_style))
    story.append(Paragraph("<b>Date:</b> 22 Janvier 2026", subtitle_style))
    story.append(Spacer(1, 15))
    
    # Parties
    parties_data = [
        ["<b>Prestataire:</b>", "Syntax Line (Représenté par Achraf Drissi El Bouzaidi et Reda Drissi El Bouzaidi)"],
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
    story.append(Paragraph("1. Résumé Exécutif", section_style))
    story.append(Paragraph(
        "Syntax Line propose de développer et déployer une solution ERP complète et sur mesure. "
        "La solution sera architecturée pour répondre aux exigences fonctionnelles spécifiques d'Orderlift (V0), "
        "en se concentrant sur la gestion centralisée multi-sociétés, l'optimisation logistique automatisée et un portail client B2B dédié.",
        body_style
    ))
    
    # Section 2
    story.append(Paragraph("2. Portée des Travaux (Les Livrables)", section_style))
    story.append(Paragraph(
        "Syntax Line configurera, développera et déploiera un système sécurisé basé sur le cloud pour répondre aux exigences suivantes :",
        body_style
    ))
    
    # 2A
    story.append(Paragraph("A. Architecture Système Centrale", subsection_style))
    story.append(Paragraph("• <b>Structure Multi-Entités :</b> Configuration d'une Société Mère centralisée (Fabrication/Export) et de Sociétés Antennes connectées (Distribution/Installation).", bullet_style))
    story.append(Paragraph("• <b>Logique d'Inventaire :</b> Mise en place d'une gestion multi-entrepôts incluant la logique de stock réel, stock en transit et stock réservé.", bullet_style))
    story.append(Paragraph("• <b>Base de Données Centralisée :</b> Migration et structuration des \"Articles de Base\" (Fichier Article) pour assurer la cohérence des données entre toutes les entités.", bullet_style))
    story.append(Paragraph("• <b>Écosystème de Ventes :</b> Implémentation du flux complet de la Commande à l'Encaissement (Order-to-Cash) avec calculs automatisés des commissions.", bullet_style))
    
    # 2B
    story.append(Paragraph("B. Développement Sur Mesure & Modules", subsection_style))
    story.append(Paragraph("• <b>Portail Client B2B :</b> Développement d'une interface web sécurisée pour les commandes clients, incluant une logique de tarification dynamique basée sur la géographie et le volume.", bullet_style))
    story.append(Paragraph("• <b>Module d'Intelligence Logistique :</b> Développement d'un algorithme propriétaire pour calculer le volume/poids des expéditions et recommander automatiquement le type de Conteneur ou de Camion optimal.", bullet_style))
    story.append(Paragraph("• <b>Documentation Automatisée :</b> Codage de générateurs PDF dynamiques pour Factures, Listes de Colisage et Bons de Livraison correspondant à l'image de marque d'Orderlift.", bullet_style))
    
    # 2C
    story.append(Paragraph("C. Formation & Transfert de Connaissances", subsection_style))
    story.append(Paragraph("• <b>Vidéothèque :</b> Mise à disposition d'une bibliothèque dédiée de vidéos de formation (enregistrements d'écran) couvrant tous les flux opérationnels clés.", bullet_style))
    story.append(Paragraph("• <b>Formation en Direct :</b> Trois (3) sessions de formation interactives sur Zoom (2 heures chacune) pour les administrateurs et les parties prenantes clés.", bullet_style))
    
    # Section 3
    story.append(Paragraph("3. Calendrier & Phases", section_style))
    story.append(Paragraph("<b>Durée Totale Estimée : 10 - 12 Semaines</b>", body_style))
    
    story.append(Paragraph("<b>Phase 1 : Fondation (Semaines 1-4)</b>", bullet_style))
    story.append(Paragraph("• Provisionnement serveur, configuration Sécurité (SSL/Pare-feu), et installation du Moteur Principal.", bullet_style))
    story.append(Paragraph("• Structuration de la base de données et import initial des données (Articles, Clients).", bullet_style))
    
    story.append(Paragraph("<b>Phase 2 : Développement Sur Mesure (Semaines 5-8)</b>", bullet_style))
    story.append(Paragraph("• Développement de l'algorithme Logistique/Conteneur.", bullet_style))
    story.append(Paragraph("• Construction du Portail B2B et du Moteur de Tarification.", bullet_style))
    story.append(Paragraph("• <i>Point de contrôle :</i> Première démonstration des fonctionnalités sur mesure.", bullet_style))
    
    story.append(Paragraph("<b>Phase 3 : UAT & Affinement (Semaines 9-10)</b>", bullet_style))
    story.append(Paragraph("• Tests d'Acceptation Utilisateur (Le Client teste le système dans un environnement de pré-production).", bullet_style))
    story.append(Paragraph("• Exécution des Révisions (voir Section 5).", bullet_style))
    
    story.append(Paragraph("<b>Phase 4 : Mise en Production (Semaines 11-12)</b>", bullet_style))
    story.append(Paragraph("• Migration finale des données.", bullet_style))
    story.append(Paragraph("• Sessions de formation en direct.", bullet_style))
    story.append(Paragraph("• Remise du système et lancement en production.", bullet_style))
    
    # Section 4
    story.append(Paragraph("4. Proposition Financière", section_style))
    
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
    story.append(Paragraph("Valeur Totale du Projet : 10 000,00 USD (Hors Taxes)", total_value_style))
    
    story.append(Paragraph(
        "<b>Échéancier de Paiement :</b> Les paiements sont structurés pour assurer la dynamique du projet et garantir une période de support après le lancement.",
        body_style
    ))
    
    payment_data = [
        ["Jalon", "Montant", "Date d'Échéance"],
        ["Démarrage du Projet (Acompte)", "3 000 USD", "À la signature de ce contrat"],
        ["Livraison & Lancement Bêta", "3 000 USD", "Au déploiement pour UAT (Semaine 8-9)"],
        ["Stabilisation & Retenue de Support", "4 000 USD", "4 mensualités de 1 000 USD\ncommençant 30 jours après le Lancement Bêta"]
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
        "<i>La période de Stabilisation couvre la surveillance, les corrections de bugs et le support général pour assurer une transition opérationnelle fluide.</i>",
        body_style
    ))
    
    # Section 5
    story.append(Paragraph("5. Politique de Révision", section_style))
    story.append(Paragraph(
        "Pour garantir que le projet reste agile tout en respectant le calendrier, le Client a droit à <b>trois (3) cycles complets de révisions groupées</b> durant la phase de développement.",
        body_style
    ))
    story.append(Paragraph(
        "Le Client devra consolider tous les retours pour chaque cycle en une liste unique de demandes. Ce \"regroupement\" des modifications permet à Syntax Line d'implémenter les changements efficacement et assure que l'architecture du système reste stable tout au long du processus de développement.",
        body_style
    ))
    
    # Section 6
    story.append(Paragraph("6. Confidentialité", section_style))
    story.append(Paragraph("Les deux parties conviennent de garder strictement confidentielles toutes les informations techniques et commerciales divulguées au cours de ce projet.", body_style))
    story.append(Paragraph("• Syntax Line s'engage à ne pas divulguer les listes de clients, stratégies de prix ou secrets commerciaux du Client à des tiers.", bullet_style))
    story.append(Paragraph("• Le Client s'engage à ne pas divulguer les méthodes de développement, algorithmes propriétaires ou codes sources de Syntax Line à des concurrents externes.", bullet_style))
    
    # Section 7
    story.append(Paragraph("7. Limitation de Responsabilité", section_style))
    story.append(Paragraph(
        "Syntax Line ne sera pas responsable des dommages indirects, accessoires, spéciaux ou consécutifs, y compris, mais sans s'y limiter, la perte de bénéfices, de revenus, de données ou d'utilisation, encourus par le Client ou tout tiers, que ce soit dans une action contractuelle ou délictuelle. La responsabilité totale de Syntax Line pour toute réclamation découlant du présent Accord ne dépassera pas le montant total payé par le Client à Syntax Line en vertu du présent Accord.",
        body_style
    ))
    
    # Section 8
    story.append(Paragraph("8. Ordres de Modification", section_style))
    story.append(Paragraph(
        "Toute demande de fonctionnalités, de modules ou de personnalisations non explicitement listés dans la Section 2 (Portée des Travaux) ou dépassant la Politique de Révision de la Section 5 sera considérée comme un \"Ordre de Modification\". Syntax Line fournira un devis séparé pour le temps et le coût requis pour de tels ajouts. Les travaux sur les Ordres de Modification ne commenceront qu'après approbation écrite et paiement des frais convenus.",
        body_style
    ))
    
    # Section 9
    story.append(Paragraph("9. Stack Technique & Propriété", section_style))
    story.append(Paragraph("• <b>Technologie :</b> La Solution est construite sur une architecture moderne et évolutive Python & JavaScript, utilisant une base de données SQL robuste (MariaDB/Postgres). Elle est conçue pour être modulaire, permettant des extensions futures (RH, Fabrication) sans reconstruire le cœur.", bullet_style))
    story.append(Paragraph("• <b>Propriété :</b> Après paiement intégral de la valeur totale du projet, Orderlift possédera les droits de propriété complets sur la configuration du système implémenté et le code source de tous les modules sur mesure développés par Syntax Line.", bullet_style))
    story.append(Paragraph("• <b>Hébergement :</b> Syntax Line configurera l'environnement d'hébergement cloud (VPS). Les coûts directs d'hébergement (approx. 20-40 USD/mois) sont à la charge du Client.", bullet_style))
    
    # Section 10
    story.append(Paragraph("10. Accord", section_style))
    story.append(Paragraph(
        "En signant ci-dessous, les deux parties acceptent les termes, la portée et l'échéancier de paiement décrits ci-dessus.",
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
            Paragraph("<b>Pour Syntax Line :</b><br/><br/>Nom : __________________<br/><br/>Date : __________________<br/><br/>Signature : __________________", sig_style),
            Paragraph("<b>Pour Orderlift :</b><br/><br/>Nom : __________________<br/><br/>Date : __________________<br/><br/>Signature : __________________", sig_style)
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
    print("✅ Contrat PDF (Français) généré avec succès !")
    print("📄 Fichier : SyntaxLine_Contrat_Service_Orderlift.pdf")


if __name__ == "__main__":
    generate_contract()
