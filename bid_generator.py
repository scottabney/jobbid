"""
Bid Generator - Creates professional bid documents
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class BidGenerator:
    """Generate professional bid documents in PDF format"""
    
    def __init__(self, company_info: Optional[Dict] = None):
        """Initialize bid generator with company information"""
        self.company_info = company_info or self._default_company_info()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _default_company_info(self) -> Dict:
        """Return default company information"""
        return {
            'name': 'Premium Metal Fabrication & Welding',
            'address': '123 Industrial Way, Manufacturing City, ST 12345',
            'phone': '(555) 123-4567',
            'email': 'bids@metalfab.com',
            'website': 'www.metalfab.com',
            'license': 'Contractor License #12345'
        }
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            borderWidth=0,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=5,
            leftIndent=0
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#555555')
        ))
    
    def generate_bid(self, 
                     bid_data: Dict,
                     output_path: str,
                     client_info: Optional[Dict] = None) -> str:
        """
        Generate a complete bid document
        
        Args:
            bid_data: Dictionary containing all bid information
            output_path: Path where PDF should be saved
            client_info: Optional client information
            
        Returns:
            Path to generated PDF file
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build document content
        story = []
        
        # Add header
        story.extend(self._create_header(bid_data))
        
        # Add client information if provided
        if client_info:
            story.extend(self._create_client_section(client_info))
        
        # Add project description
        story.extend(self._create_project_section(bid_data))
        
        # Add scope of work
        story.extend(self._create_scope_section(bid_data))
        
        # Add cost breakdown
        story.extend(self._create_cost_section(bid_data))
        
        # Add terms and conditions
        story.extend(self._create_terms_section(bid_data))
        
        # Add signature section
        story.extend(self._create_signature_section())
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_header(self, bid_data: Dict) -> List:
        """Create document header"""
        elements = []
        
        # Company name
        company_name = Paragraph(
            self.company_info['name'],
            self.styles['CustomTitle']
        )
        elements.append(company_name)
        
        # Company details
        contact_info = f"""
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']}<br/>
        {self.company_info.get('website', '')}
        """
        
        elements.append(Paragraph(contact_info, self.styles['CompanyInfo']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Bid title
        bid_title = Paragraph(
            f"<b>JOB BID PROPOSAL</b>",
            self.styles['CustomTitle']
        )
        elements.append(bid_title)
        
        # Bid details
        bid_number = bid_data.get('bid_number', f"BID-{datetime.now().strftime('%Y%m%d-%H%M')}")
        bid_date = bid_data.get('date', datetime.now().strftime('%B %d, %Y'))
        
        bid_info = f"""
        <b>Bid Number:</b> {bid_number}<br/>
        <b>Date:</b> {bid_date}<br/>
        <b>Valid Until:</b> {bid_data.get('valid_until', '30 days from date')}
        """
        
        elements.append(Paragraph(bid_info, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_client_section(self, client_info: Dict) -> List:
        """Create client information section"""
        elements = []
        
        elements.append(Paragraph("<b>PREPARED FOR:</b>", self.styles['SectionHeader']))
        
        client_text = f"""
        <b>{client_info.get('name', 'Client Name')}</b><br/>
        {client_info.get('address', '')}<br/>
        Phone: {client_info.get('phone', '')}<br/>
        Email: {client_info.get('email', '')}
        """
        
        elements.append(Paragraph(client_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_project_section(self, bid_data: Dict) -> List:
        """Create project description section"""
        elements = []
        
        elements.append(Paragraph("PROJECT DESCRIPTION", self.styles['SectionHeader']))
        
        project_name = bid_data.get('project_name', 'Metal Fabrication Project')
        project_desc = bid_data.get('project_description', 'Custom metal fabrication and welding work')
        
        desc_text = f"""
        <b>Project:</b> {project_name}<br/><br/>
        {project_desc}
        """
        
        elements.append(Paragraph(desc_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_scope_section(self, bid_data: Dict) -> List:
        """Create scope of work section"""
        elements = []
        
        elements.append(Paragraph("SCOPE OF WORK", self.styles['SectionHeader']))
        
        scope_items = bid_data.get('scope_of_work', [])
        if not scope_items:
            scope_items = [
                'Material procurement and preparation',
                'Metal cutting and fabrication',
                'Welding and assembly',
                'Grinding and finishing',
                'Quality inspection',
                'Delivery and installation (if applicable)'
            ]
        
        scope_text = "<br/>".join([f"• {item}" for item in scope_items])
        elements.append(Paragraph(scope_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Materials and processes
        if 'materials' in bid_data:
            elements.append(Paragraph("<b>Materials:</b>", self.styles['Normal']))
            materials_text = ", ".join(bid_data['materials'])
            elements.append(Paragraph(materials_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        if 'processes' in bid_data:
            elements.append(Paragraph("<b>Processes:</b>", self.styles['Normal']))
            processes_text = ", ".join(bid_data['processes'])
            elements.append(Paragraph(processes_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_cost_section(self, bid_data: Dict) -> List:
        """Create cost breakdown section"""
        elements = []
        
        elements.append(Paragraph("COST BREAKDOWN", self.styles['SectionHeader']))
        
        cost_data = bid_data.get('cost_breakdown', {})
        
        # Create cost table
        table_data = [
            ['Description', 'Amount']
        ]
        
        # Add line items
        if cost_data.get('material_cost', 0) > 0:
            table_data.append(['Materials', f"${cost_data['material_cost']:,.2f}"])
        
        if cost_data.get('labor_cost', 0) > 0:
            labor_hours = cost_data.get('breakdown', {}).get('labor_hours', 0)
            table_data.append([f'Labor ({labor_hours} hours)', f"${cost_data['labor_cost']:,.2f}"])
        
        if cost_data.get('process_cost', 0) > 0:
            table_data.append(['Specialized Processes', f"${cost_data['process_cost']:,.2f}"])
        
        if cost_data.get('subtotal', 0) > 0:
            table_data.append(['Subtotal', f"${cost_data['subtotal']:,.2f}"])
        
        if cost_data.get('overhead', 0) > 0:
            overhead_rate = cost_data.get('overhead_rate', 0.15) * 100
            table_data.append([f'Overhead ({overhead_rate:.0f}%)', f"${cost_data['overhead']:,.2f}"])
        
        # Total
        final_price = cost_data.get('final_price', 0)
        table_data.append(['', ''])  # Blank row
        table_data.append(['TOTAL BID PRICE', f"${final_price:,.2f}"])
        
        # Create table
        table = Table(table_data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -2), 1, colors.grey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#2c3e50'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_terms_section(self, bid_data: Dict) -> List:
        """Create terms and conditions section"""
        elements = []
        
        elements.append(Paragraph("TERMS & CONDITIONS", self.styles['SectionHeader']))
        
        terms = bid_data.get('terms', [])
        if not terms:
            terms = [
                'Payment: 50% deposit required, balance due upon completion',
                'Timeline: Work to commence within 5 business days of deposit receipt',
                'Warranty: 1 year warranty on workmanship',
                'Changes: Any changes to scope may affect price and timeline',
                'Materials: All materials meet industry standards and specifications',
                'Permits: Client responsible for obtaining necessary permits unless otherwise specified',
                'Liability: We carry full liability and workers compensation insurance'
            ]
        
        terms_text = "<br/>".join([f"• {term}" for term in terms])
        elements.append(Paragraph(terms_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_signature_section(self) -> List:
        """Create signature section"""
        elements = []
        
        elements.append(Paragraph("ACCEPTANCE", self.styles['SectionHeader']))
        
        acceptance_text = """
        By signing below, you accept this bid proposal and authorize us to proceed with the work 
        as described above under the terms and conditions stated.
        """
        elements.append(Paragraph(acceptance_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Signature table
        sig_data = [
            ['Client Signature: _________________________', 'Date: _______________'],
            ['', ''],
            ['Print Name: _________________________', '']
        ]
        
        sig_table = Table(sig_data, colWidths=[4*inch, 2*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(sig_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = f"""
        <i>Thank you for considering {self.company_info['name']} for your project. 
        We look forward to working with you!</i>
        """
        elements.append(Paragraph(footer_text, self.styles['CompanyInfo']))
        
        return elements
    
    def generate_quick_bid(self,
                          project_name: str,
                          total_price: float,
                          output_path: str,
                          labor_hours: float = 0,
                          materials_desc: str = "") -> str:
        """Generate a quick, simple bid document"""
        bid_data = {
            'project_name': project_name,
            'project_description': materials_desc or 'Custom metal fabrication and welding project',
            'cost_breakdown': {
                'final_price': total_price,
                'breakdown': {
                    'labor_hours': labor_hours
                }
            }
        }
        
        return self.generate_bid(bid_data, output_path)
