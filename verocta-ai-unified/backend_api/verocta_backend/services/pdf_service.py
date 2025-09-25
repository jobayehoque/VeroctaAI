"""
PDF Generation Service
Creates professional PDF reports with charts and analytics
"""

import os
from datetime import datetime
from typing import Optional
from flask import current_app

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import base64

from ..models import Report
from ..core.database import db


class PDFGeneratorService:
    """Service for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f2937'),
            spaceBefore=20,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#059669'),
            alignment=TA_CENTER
        ))
    
    def generate_report_pdf(self, report_id: int, output_dir: Optional[str] = None) -> str:
        """
        Generate PDF report for given report ID
        Returns path to generated PDF file
        """
        try:
            report = Report.query.get(report_id)
            if not report:
                raise ValueError(f"Report {report_id} not found")
            
            if not output_dir:
                output_dir = os.path.join(current_app.instance_path, 'outputs')
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"financial_report_{report_id}_{timestamp}.pdf"
            file_path = os.path.join(output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = self._build_report_content(report)
            
            # Generate PDF
            doc.build(story)
            
            current_app.logger.info(f"Generated PDF report: {file_path}")
            return file_path
            
        except Exception as e:
            current_app.logger.error(f"PDF generation error: {str(e)}")
            raise
    
    def _build_report_content(self, report: Report) -> list:
        """Build the content elements for the PDF report"""
        story = []
        
        # Title
        title = f"Financial Analysis Report"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        
        if report.company_name:
            story.append(Paragraph(report.company_name, self.styles['CustomTitle']))
        
        story.append(Spacer(1, 20))
        
        # Report Info
        story.append(self._build_report_info_section(report))
        story.append(Spacer(1, 20))
        
        # SpendScore Section
        if report.spend_score is not None:
            story.append(self._build_spendscore_section(report))
            story.append(Spacer(1, 20))
        
        # Metrics Section
        if report.metrics:
            story.append(self._build_metrics_section(report))
            story.append(Spacer(1, 20))
        
        # Insights Section
        if report.ai_insights:
            story.append(self._build_insights_section(report))
            story.append(Spacer(1, 20))
        
        # Transaction Summary
        story.append(self._build_transaction_summary(report))
        
        return story
    
    def _build_report_info_section(self, report: Report) -> Table:
        """Build report information section"""
        data = [
            ['Report Generated:', datetime.utcnow().strftime('%B %d, %Y')],
            ['Report Title:', report.title],
            ['Original File:', report.original_filename or 'N/A'],
            ['File Format:', report.file_format or 'Generic'],
            ['Status:', report.status.title()],
        ]
        
        if report.date_range_start and report.date_range_end:
            data.append(['Date Range:', f"{report.date_range_start} to {report.date_range_end}"])
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        return table
    
    def _build_spendscore_section(self, report: Report) -> list:
        """Build SpendScore section"""
        elements = []
        
        elements.append(Paragraph("SpendScore Analysis", self.styles['SectionHeader']))
        
        # Score display
        score = report.spend_score or 0
        tier = report.score_tier or 'Unknown'
        
        # Color based on tier
        color_map = {
            'Green': colors.HexColor('#10b981'),
            'Amber': colors.HexColor('#f59e0b'),
            'Red': colors.HexColor('#ef4444'),
        }
        score_color = color_map.get(tier, colors.black)
        
        score_data = [
            ['SpendScore', 'Tier', 'Interpretation'],
            [f'{score:.1f}/100', tier, self._get_tier_interpretation(tier)]
        ]
        
        score_table = Table(score_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#f9fafb')),
            ('BACKGROUND', (1, 1), (1, 1), score_color),
            ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(score_table)
        return elements
    
    def _build_metrics_section(self, report: Report) -> list:
        """Build metrics breakdown section"""
        elements = []
        
        elements.append(Paragraph("Detailed Metrics Breakdown", self.styles['SectionHeader']))
        
        if not report.metrics:
            elements.append(Paragraph("No metrics data available.", self.styles['Normal']))
            return elements
        
        metrics = report.metrics
        
        # Metrics table
        metric_names = {
            'frequency_score': 'Transaction Frequency',
            'category_diversity': 'Category Diversity',
            'budget_adherence': 'Budget Adherence',
            'redundancy_detection': 'Redundancy Detection',
            'spike_detection': 'Spike Detection',
            'waste_ratio': 'Waste Ratio'
        }
        
        data = [['Metric', 'Score', 'Weight', 'Description']]
        
        weights = {
            'frequency_score': '15%',
            'category_diversity': '10%',
            'budget_adherence': '20%',
            'redundancy_detection': '15%',
            'spike_detection': '20%',
            'waste_ratio': '20%'
        }
        
        descriptions = {
            'frequency_score': 'Consistency of transaction patterns',
            'category_diversity': 'Variety in spending categories',
            'budget_adherence': 'Staying within estimated budgets',
            'redundancy_detection': 'Detection of duplicate transactions',
            'spike_detection': 'Control of unusual large expenses',
            'waste_ratio': 'Ratio of essential vs non-essential spending'
        }
        
        for key, name in metric_names.items():
            if key in metrics:
                score = metrics[key]
                weight = weights.get(key, 'N/A')
                description = descriptions.get(key, '')
                data.append([name, f'{score:.1f}', weight, description])
        
        metrics_table = Table(data, colWidths=[2*inch, 0.8*inch, 0.8*inch, 2.4*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(metrics_table)
        return elements
    
    def _build_insights_section(self, report: Report) -> list:
        """Build AI insights section"""
        elements = []
        
        elements.append(Paragraph("Financial Insights", self.styles['SectionHeader']))
        
        if not report.ai_insights:
            elements.append(Paragraph("No insights available.", self.styles['Normal']))
            return elements
        
        insights = report.ai_insights
        
        if 'summary' in insights:
            elements.append(Paragraph(f"Summary: {insights['summary']}", self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        if 'recommendations' in insights and insights['recommendations']:
            elements.append(Paragraph("Recommendations:", self.styles['Normal']))
            for i, rec in enumerate(insights['recommendations'], 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        return elements
    
    def _build_transaction_summary(self, report: Report) -> list:
        """Build transaction summary section"""
        elements = []
        
        elements.append(Paragraph("Transaction Summary", self.styles['SectionHeader']))
        
        # Summary stats
        data = [
            ['Total Transactions:', str(report.total_transactions or 0)],
            ['Total Amount:', f"${report.total_amount or 0:.2f}"],
        ]
        
        if report.date_range_start:
            data.append(['Period Start:', str(report.date_range_start)])
        if report.date_range_end:
            data.append(['Period End:', str(report.date_range_end)])
        
        summary_table = Table(data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(summary_table)
        
        # Footer
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            f"Report generated on {datetime.utcnow().strftime('%B %d, %Y at %I:%M %p')} by VeroctaAI Financial Intelligence Platform",
            self.styles['Normal']
        ))
        
        return elements
    
    def _get_tier_interpretation(self, tier: str) -> str:
        """Get interpretation text for score tier"""
        interpretations = {
            'Green': 'Excellent financial discipline and spending patterns',
            'Amber': 'Good financial management with room for optimization',
            'Red': 'Significant improvement needed in spending habits'
        }
        return interpretations.get(tier, 'Financial analysis completed')