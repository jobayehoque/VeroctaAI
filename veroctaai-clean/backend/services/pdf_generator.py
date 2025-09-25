"""
PDF Report Generation Service
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logging.warning("ReportLab library not installed. PDF generation will not work.")

class PDFGeneratorService:
    """PDF report generation service"""
    
    def __init__(self):
        self.output_dir = 'outputs'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_report_pdf(self, analysis_data: Dict[str, Any], 
                           transactions: List[Dict] = None, 
                           company_name: str = "VeroctaAI") -> str:
        """Generate PDF report"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab library not available")
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"verocta_report_{timestamp}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.darkblue
            )
            
            # Build content
            content = []
            
            # Title
            content.append(Paragraph("VeroctaAI Financial Analysis Report", title_style))
            content.append(Spacer(1, 20))
            
            # Company info
            content.append(Paragraph(f"Company: {company_name}", styles['Normal']))
            content.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            content.append(Spacer(1, 20))
            
            # SpendScore section
            content.append(Paragraph("SpendScore Analysis", heading_style))
            
            spend_score = analysis_data.get('spend_score', 0)
            score_label = analysis_data.get('score_label', 'Unknown')
            score_color = analysis_data.get('score_color', 'Gray')
            
            score_data = [
                ['Metric', 'Value'],
                ['SpendScore', f"{spend_score}/100"],
                ['Rating', score_label],
                ['Status', score_color]
            ]
            
            score_table = Table(score_data, colWidths=[2*inch, 2*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            content.append(score_table)
            content.append(Spacer(1, 20))
            
            # Transaction summary
            content.append(Paragraph("Transaction Summary", heading_style))
            
            total_transactions = analysis_data.get('total_transactions', 0)
            total_amount = analysis_data.get('total_amount', 0)
            
            summary_data = [
                ['Metric', 'Value'],
                ['Total Transactions', f"{total_transactions:,}"],
                ['Total Amount', f"${total_amount:,.2f}"],
                ['Average Transaction', f"${total_amount/total_transactions:,.2f}" if total_transactions > 0 else "$0.00"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            content.append(summary_table)
            content.append(Spacer(1, 20))
            
            # Category breakdown
            category_breakdown = analysis_data.get('category_breakdown', {})
            if category_breakdown:
                content.append(Paragraph("Category Breakdown", heading_style))
                
                category_data = [['Category', 'Amount', 'Percentage']]
                for category, amount in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / total_amount * 100) if total_amount > 0 else 0
                    category_data.append([category, f"${amount:,.2f}", f"{percentage:.1f}%"])
                
                category_table = Table(category_data, colWidths=[2*inch, 1.5*inch, 1*inch])
                category_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                content.append(category_table)
                content.append(Spacer(1, 20))
            
            # AI Insights
            suggestions = analysis_data.get('suggestions', [])
            if suggestions:
                content.append(Paragraph("AI-Powered Insights", heading_style))
                
                for i, suggestion in enumerate(suggestions, 1):
                    priority = suggestion.get('priority', 'Medium')
                    text = suggestion.get('text', '')
                    
                    priority_color = colors.red if priority == 'High' else colors.orange if priority == 'Medium' else colors.green
                    
                    insight_text = f"<b>{priority} Priority:</b> {text}"
                    content.append(Paragraph(insight_text, styles['Normal']))
                    content.append(Spacer(1, 8))
            
            # Footer
            content.append(Spacer(1, 30))
            content.append(Paragraph("Generated by VeroctaAI - AI-Powered Financial Intelligence", 
                                   ParagraphStyle('Footer', parent=styles['Normal'], 
                                                fontSize=8, alignment=TA_CENTER, 
                                                textColor=colors.grey)))
            
            # Build PDF
            doc.build(content)
            
            logging.info(f"PDF report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logging.error(f"PDF generation failed: {e}")
            raise e
