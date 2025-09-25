import os
import logging
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.flowables import HRFlowable
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
import io
import base64
from reportlab.platypus import Image as ReportLabImage
from statistics import median
from collections import defaultdict

def create_enhanced_pie_chart(category_data, title="Spending by Category"):
    """Create enhanced pie chart with superior design and fallback to bar chart for many categories"""
    try:
        if not category_data:
            return None

        # Prepare and sort data by amount (largest first)
        sorted_items = sorted(category_data.items(), key=lambda x: x[1], reverse=True)
        categories = [item[0] for item in sorted_items]
        amounts = [item[1] for item in sorted_items]

        # If more than 6 categories, create horizontal bar chart instead
        if len(categories) > 6:
            return create_horizontal_bar_chart(category_data, title)

        # Create pie chart for <= 6 categories with superior design
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

        # Enhanced color scheme with professional colors
        professional_colors = [
            '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', 
            '#6A994E', '#577590', '#F2CC8F', '#81B29A'
        ]
        colors_list = professional_colors[:len(categories)]

        # Create pie chart with enhanced styling
        wedges, texts, autotexts = ax1.pie(
            amounts, 
            labels=None,  # We'll create a separate legend
            autopct='%1.1f%%',
            colors=colors_list, 
            startangle=90,
            explode=[0.08] * len(categories),  # More separation for clarity
            shadow=True,
            pctdistance=0.85,
            textprops={'fontsize': 10, 'fontweight': 'bold', 'color': 'white'}
        )

        # Style the percentage labels
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
            autotext.set_bbox(dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

        ax1.set_title(title, fontsize=16, fontweight='bold', pad=25, color='#2E86AB')

        # Create detailed legend table in the second subplot
        ax2.axis('off')
        legend_data = []
        total_amount = sum(amounts)

        for i, (cat, amt) in enumerate(zip(categories, amounts)):
            percentage = (amt / total_amount) * 100
            legend_data.append([
                f"● {cat}", 
                f"${amt:,.2f}", 
                f"{percentage:.1f}%"
            ])

        # Create table for legend
        table_data = [['Category', 'Amount', 'Percentage']] + legend_data

        # Color the bullet points to match pie slices
        table_text = []
        for i, row in enumerate(table_data):
            if i == 0:  # Header row
                table_text.append(row)
            else:
                colored_category = row[0].replace('●', f'●')  # Keep the bullet
                table_text.append([colored_category, row[1], row[2]])

        table = ax2.table(
            cellText=table_text,
            cellLoc='left',
            loc='center',
            colWidths=[0.5, 0.25, 0.25]
        )

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)

        # Style the table
        for i in range(len(table_data)):
            for j in range(3):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor('#2E86AB')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    if j == 0:  # Category column - color the bullet
                        cell.set_text_props(color=colors_list[i-1])
                        cell.set_text_props(weight='bold')
                    cell.set_facecolor('#f8f9fa')
                cell.set_edgecolor('#dee2e6')
                cell.set_linewidth(1.5)

        ax2.set_title('Spending Breakdown', fontsize=14, fontweight='bold', pad=20, color='#2E86AB')

        plt.tight_layout()

        # Save to bytes with high quality
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        img_buffer.seek(0)
        plt.close()

        return img_buffer

    except Exception as e:
        logging.error(f"Error creating enhanced pie chart: {str(e)}")
        return None

def create_clean_pie_chart(category_data, title="Spending by Category"):
    """Create clean, simple pie chart with minimal design"""
    try:
        if not category_data:
            return None

        # Prepare and sort data by amount (largest first)
        sorted_items = sorted(category_data.items(), key=lambda x: x[1], reverse=True)
        categories = [item[0] for item in sorted_items]
        amounts = [item[1] for item in sorted_items]

        # Create single clean pie chart
        fig, ax = plt.subplots(figsize=(10, 10))

        # Clean color scheme
        clean_colors = [
            '#3498db', '#e74c3c', '#2ecc71', '#f39c12', 
            '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
        ]
        colors_list = clean_colors[:len(categories)]

        # Create clean pie chart
        wedges, texts, autotexts = ax.pie(
            amounts, 
            labels=categories,
            autopct='%1.1f%%',
            colors=colors_list, 
            startangle=90,
            explode=[0.05] * len(categories),
            shadow=False,
            pctdistance=0.85,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )

        # Style the percentage labels
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
            autotext.set_bbox(dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))

        # Style category labels
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')

        ax.set_title(title, fontsize=18, fontweight='bold', pad=30, color='#2c3e50')

        plt.tight_layout()

        # Save to bytes with high quality
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        img_buffer.seek(0)
        plt.close()

        return img_buffer

    except Exception as e:
        logging.error(f"Error creating clean pie chart: {str(e)}")
        return None

def create_spending_trend_chart(transactions, title="Monthly Spending Trend"):
    """Create a spending trend chart over time"""
    try:
        if not transactions:
            return None

        # Group transactions by month
        monthly_data = defaultdict(float)
        for transaction in transactions:
            date_str = transaction.get('date', '')
            amount = abs(float(transaction.get('amount', 0)))

            # Try to parse date
            try:
                if '/' in date_str:
                    date_obj = datetime.strptime(date_str.split()[0], '%m/%d/%Y')
                elif '-' in date_str:
                    date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
                else:
                    continue

                month_key = date_obj.strftime('%Y-%m')
                monthly_data[month_key] += amount
            except:
                continue

        if len(monthly_data) < 2:
            return None

        # Sort by month
        sorted_months = sorted(monthly_data.items())
        months = [item[0] for item in sorted_months]
        amounts = [item[1] for item in sorted_months]

        fig, ax = plt.subplots(figsize=(12, 6))

        # Create line chart
        ax.plot(months, amounts, marker='o', linewidth=3, markersize=8, color='#3498db')
        ax.fill_between(months, amounts, alpha=0.3, color='#3498db')

        ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Amount ($)', fontsize=12, fontweight='bold')

        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        img_buffer.seek(0)
        plt.close()

        return img_buffer

    except Exception as e:
        logging.error(f"Error creating trend chart: {str(e)}")
        return None

def create_horizontal_bar_chart(category_data, title="Spending by Category"):
    """Create horizontal bar chart for categories > 6"""
    try:
        if not category_data:
            return None

        # Sort by amount (highest first)
        sorted_items = sorted(category_data.items(), key=lambda x: x[1], reverse=True)
        categories = [item[0] for item in sorted_items]
        amounts = [item[1] for item in sorted_items]

        # Create horizontal bar chart with professional styling
        fig, ax = plt.subplots(figsize=(12, max(8, len(categories) * 0.8)))

        # Professional color gradient
        colors_list = plt.cm.viridis(np.linspace(0, 1, len(categories)))

        bars = ax.barh(categories, amounts, color=colors_list, height=0.7)

        # Add value labels on bars with professional formatting
        max_amount = max(amounts)
        for i, (bar, amount) in enumerate(zip(bars, amounts)):
            width = bar.get_width()
            # Position label inside bar if bar is wide enough, outside if not
            label_x = width * 0.95 if width > max_amount * 0.15 else width + max_amount * 0.02
            label_color = 'white' if width > max_amount * 0.15 else 'black'

            ax.text(label_x, bar.get_y() + bar.get_height()/2, 
                   f'${amount:,.0f}',
                   ha='right' if width > max_amount * 0.15 else 'left',
                   va='center', 
                   fontweight='bold',
                   fontsize=10,
                   color=label_color)

        # Professional styling
        ax.set_xlabel('Amount ($)', fontsize=12, fontweight='bold', color='#2E86AB')
        ax.set_ylabel('Categories', fontsize=12, fontweight='bold', color='#2E86AB')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#2E86AB')

        # Format x-axis labels as currency
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Style the grid
        ax.grid(True, alpha=0.3, axis='x')
        ax.set_axisbelow(True)

        # Improve layout
        plt.tight_layout()

        # Add a subtle border
        for spine in ax.spines.values():
            spine.set_color('#dee2e6')
            spine.set_linewidth(1.5)

        # Format x-axis
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        plt.tight_layout()

        # Save to bytes with high quality
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        img_buffer.seek(0)
        plt.close()

        return img_buffer

    except Exception as e:
        logging.error(f"Error creating horizontal bar chart: {str(e)}")
        return None

def get_score_color_rgb(score):
    """Get RGB color values for score with enhanced traffic light system"""
    if score >= 90:
        return colors.HexColor('#28a745')  # Green
    elif score >= 70:
        return colors.HexColor('#ffc107')  # Amber
    else:
        return colors.HexColor('#dc3545')  # Red

def add_company_branding(story, company_name=None, logo_path=None):
    """Add enhanced company branding to PDF header with improved logo handling"""
    try:
        styles = getSampleStyleSheet()

        # Enhanced company header style
        header_style = ParagraphStyle(
            'CompanyHeader',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=25,
            spaceBefore=10,
            textColor=colors.HexColor('#2E86AB'),
            alignment=1  # Center alignment
        )

        # Create header section with logo and company info
        header_elements = []

        if logo_path and os.path.exists(logo_path):
            # Enhanced logo handling with better sizing and positioning
            try:
                # Determine optimal logo size based on file
                from PIL import Image as PILImage
                try:
                    pil_img = PILImage.open(logo_path)
                    aspect_ratio = pil_img.width / pil_img.height

                    # Calculate optimal dimensions (max 3 inches wide, 2 inches tall)
                    if aspect_ratio > 1.5:  # Wide logo
                        logo_width = 3*inch
                        logo_height = 3*inch / aspect_ratio
                    else:  # Square or tall logo
                        logo_height = 1.5*inch
                        logo_width = 1.5*inch * aspect_ratio

                except:
                    # Fallback dimensions
                    logo_width, logo_height = 2*inch, 1*inch

                logo = ReportLabImage(logo_path, width=logo_width, height=logo_height)
                story.append(logo)
                story.append(Spacer(1, 15))

            except Exception as e:
                logging.warning(f"Could not load logo from {logo_path}: {str(e)}")

        # Company name and report title
        if company_name:
            company_header = Paragraph(f"<b>{company_name}</b><br/>Financial Intelligence Report", header_style)
        else:
            # Use the new VeroctaAI logo as default
            default_logo_path = os.path.join('static', 'assets', 'images', 'verocta-logo.png')
            if os.path.exists(default_logo_path):
                try:
                    from PIL import Image as PILImage
                    pil_img = PILImage.open(default_logo_path)
                    aspect_ratio = pil_img.width / pil_img.height
                    
                    if aspect_ratio > 1.5:
                        logo_width = 3*inch
                        logo_height = 3*inch / aspect_ratio
                    else:
                        logo_height = 1.5*inch
                        logo_width = 1.5*inch * aspect_ratio
                        
                    logo = ReportLabImage(default_logo_path, width=logo_width, height=logo_height)
                    story.append(logo)
                    story.append(Spacer(1, 15))
                except Exception as e:
                    logging.warning(f"Could not load default logo: {str(e)}")
            
            company_header = Paragraph("<b>VeroctaAI</b><br/>AI-Powered Financial Intelligence Report", header_style)

        story.append(company_header)
        story.append(Spacer(1, 25))

        # Add a professional separator line
        story.append(HRFlowable(width="100%", thickness=1.5, lineCap='round', color=colors.HexColor('#2E86AB')))
        story.append(Spacer(1, 20))

    except Exception as e:
        logging.error(f"Error adding company branding: {str(e)}")
        # Add fallback header
        fallback_style = ParagraphStyle(
            'FallbackHeader',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=16,
            alignment=1,
            textColor=colors.HexColor('#2E86AB')
        )
        story.append(Paragraph("<b>VeroctaAI AI-Powered Financial Intelligence Report</b>", fallback_style))
        story.append(Spacer(1, 20))

def create_score_badge_section(story, styles, score, tier_info):
    """Create enhanced score badge section with reward information"""
    try:
        # Score badge with enhanced styling
        score_color = get_score_color_rgb(score)

        score_style = ParagraphStyle(
            'ScoreBadge',
            parent=styles['Normal'],
            fontSize=24,
            spaceAfter=10,
            spaceBefore=10,
            textColor=colors.white,
            backColor=score_color,
            borderColor=score_color,
            borderWidth=2,
            borderPadding=10,
            alignment=1,  # Center alignment
            borderRadius=15
        )

        # Enhanced score display
        score_text = f"<b>SpendScore: {score}/100</b><br/>{tier_info['tier']} ({tier_info['color']})"
        score_paragraph = Paragraph(score_text, score_style)

        # Keep score and description together
        score_section = [
            score_paragraph,
            Spacer(1, 12),
            Paragraph(f"<i>{tier_info['description']}</i>", styles['Normal'])
        ]

        # Add reward eligibility if Green tier
        if tier_info.get('green_reward_eligible', False):
            reward_style = ParagraphStyle(
                'RewardStyle',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=10,
                spaceBefore=10,
                textColor=colors.HexColor('#28a745'),
                backColor=colors.HexColor('#d4edda'),
                borderColor=colors.HexColor('#28a745'),
                borderWidth=1,
                borderPadding=8,
                alignment=1
            )

            reward_text = "🎉 <b>Green Tier Reward Eligible!</b><br/>You've qualified for 15% off next month's premium features!"
            score_section.append(Spacer(1, 10))
            score_section.append(Paragraph(reward_text, reward_style))

        # Keep everything together
        story.append(KeepTogether(score_section))
        story.append(Spacer(1, 20))

    except Exception as e:
        logging.error(f"Error creating score badge: {str(e)}")

def generate_report_pdf(analysis_data, transactions, company_name=None, logo_path=None):
    """Generate comprehensive PDF report with enhanced features"""
    try:
        # Ensure output directory exists
        os.makedirs('outputs', exist_ok=True)
        pdf_path = os.path.join('outputs', 'verocta_report.pdf')

        # Create PDF document with enhanced margins
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4, 
            rightMargin=50, 
            leftMargin=50,
            topMargin=50, 
            bottomMargin=50
        )

        # Get styles
        styles = getSampleStyleSheet()

        # Enhanced custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=26,
            spaceAfter=30,
            spaceBefore=20,
            textColor=colors.HexColor('#2E86AB'),
            alignment=1  # Center alignment
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=25,
            textColor=colors.HexColor('#2E86AB')
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            leading=14
        )

        # Build PDF content
        story = []

        # Add enhanced company branding at the top
        add_company_branding(story, company_name, logo_path)

        # Report metadata with enhanced styling
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        metadata_style = ParagraphStyle(
            'MetadataStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            alignment=1  # Center alignment
        )

        story.append(Paragraph(f"Generated: {report_date}", metadata_style))
        story.append(Paragraph(f"Data Source: {analysis_data.get('filename', 'Financial Data')}", metadata_style))
        if company_name:
            story.append(Paragraph(f"Prepared for: {company_name}", metadata_style))
        story.append(Spacer(1, 25))

        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))

        spend_score = analysis_data.get('spend_score', 0)
        score_color = get_score_color_rgb(spend_score)

        # Enhanced SpendScore with visual badge and explanation
        score_emoji = "🟩" if spend_score >= 80 else "🟧" if spend_score >= 60 else "🟥"
        score_text = f"<font color='{score_color}' size='20'><b>{score_emoji} SpendScore: {spend_score:.1f}/100</b></font>"
        story.append(Paragraph(score_text, body_style))

        score_label = analysis_data.get('score_label', 'Unknown')
        color_name = analysis_data.get('score_color', 'Gray')

        badge_text = f"<font color='{score_color}' size='14'><b>Financial Health: {score_label} ({color_name})</b></font>"
        story.append(Paragraph(badge_text, body_style))

        # Add score interpretation
        if spend_score >= 80:
            interpretation = "Excellent financial discipline with optimized spending patterns."
        elif spend_score >= 60:
            interpretation = "Good financial management with opportunities for improvement."
        else:
            interpretation = "Significant optimization potential - immediate action recommended."

        story.append(Paragraph(f"<i>{interpretation}</i>", body_style))
        story.append(Spacer(1, 15))

        # Key metrics table
        metrics_data = [
            ['Metric', 'Value'],
            ['Total Transactions', f"{analysis_data.get('total_transactions', 0):,}"],
            ['Total Amount', f"${analysis_data.get('total_amount', 0):,.2f}"],
            ['Average Transaction', f"${analysis_data.get('total_amount', 0) / max(analysis_data.get('total_transactions', 1), 1):,.2f}"],
            ['Financial Health', f"{score_label} ({color_name})"]
        ]

        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(metrics_table)
        story.append(Spacer(1, 20))

        # Enhanced AI Recommendations with action items
        story.append(Paragraph("🤖 AI-Powered Financial Recommendations", heading_style))

        # Add summary of recommendations
        suggestions = analysis_data.get('suggestions', [])
        high_priority = len([s for s in suggestions if s.get('priority') == 'High'])
        medium_priority = len([s for s in suggestions if s.get('priority') == 'Medium'])
        low_priority = len([s for s in suggestions if s.get('priority') == 'Low'])

        summary_text = f"Analysis identified {high_priority} high-priority, {medium_priority} medium-priority, and {low_priority} low-priority optimization opportunities."
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 10))

        for i, suggestion in enumerate(suggestions, 1):
            priority = suggestion.get('priority', 'Medium')
            text = suggestion.get('text', 'No recommendation available')

            # Enhanced color coding and symbols
            if priority == 'High':
                priority_color = colors.red
                symbol = "🔴"
            elif priority == 'Medium':
                priority_color = colors.orange
                symbol = "🟡"
            else:
                priority_color = colors.green
                symbol = "🟢"

            priority_text = f"<font color='{priority_color}'><b>{symbol} {priority} Priority:</b></font> {text}"
            story.append(Paragraph(f"{i}. {priority_text}", body_style))
            story.append(Spacer(1, 12))

        # Category Analysis
        if transactions:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Spending Analysis", heading_style))

            # Calculate category breakdown
            category_totals = {}
            vendor_totals = {}

            for transaction in transactions:
                category = transaction.get('category', 'Uncategorized')
                vendor = transaction.get('vendor', 'Unknown')
                amount = transaction.get('amount', 0)

                category_totals[category] = category_totals.get(category, 0) + amount
                vendor_totals[vendor] = vendor_totals.get(vendor, 0) + amount

            # Top categories table
            if category_totals:
                story.append(Paragraph("Top Spending Categories", styles['Heading3']))

                sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:10]
                total_amount = sum(category_totals.values())

                category_data = [['Category', 'Amount', 'Percentage']]
                for category, amount in sorted_categories:
                    percentage = (amount / total_amount) * 100
                    category_data.append([category, f"${amount:,.2f}", f"{percentage:.1f}%"])

                category_table = Table(category_data, colWidths=[2*inch, 1.5*inch, 1*inch])
                category_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
                ]))

                story.append(category_table)
                story.append(Spacer(1, 15))

            # Top vendors table
            if vendor_totals:
                story.append(Paragraph("Top Vendors", styles['Heading3']))

                sorted_vendors = sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True)[:10]
                total_amount = sum(vendor_totals.values())

                vendor_data = [['Vendor', 'Amount', 'Percentage']]
                for vendor, amount in sorted_vendors:
                    percentage = (amount / total_amount) * 100
                    vendor_data.append([vendor[:30], f"${amount:,.2f}", f"{percentage:.1f}%"])  # Truncate long vendor names

                vendor_table = Table(vendor_data, colWidths=[2*inch, 1.5*inch, 1*inch])
                vendor_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
                ]))

                story.append(vendor_table)

        # Enhanced Visual Analytics Section
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=2, lineCap='round', color=colors.HexColor('#2E86AB')))
        story.append(Spacer(1, 20))
        story.append(Paragraph("📊 Comprehensive Visual Analytics", heading_style))

        # Multiple chart section with enhanced pie charts and additional visualizations
        category_totals = locals().get('category_totals', {})
        if category_totals:

            # Chart 1: Clean Simple Pie Chart
            story.append(Paragraph("💰 Clean Spending Distribution", styles['Heading3']))
            clean_chart_buffer = create_clean_pie_chart(category_totals, "Clean Spending Breakdown")
            if clean_chart_buffer:
                story.append(Spacer(1, 10))
                clean_chart_image = ReportLabImage(clean_chart_buffer, width=6*inch, height=6*inch)
                story.append(clean_chart_image)
                story.append(Spacer(1, 15))

            # Chart 2: Enhanced Dual-Panel Pie Chart (existing)
            story.append(Paragraph("📈 Detailed Spending Analysis", styles['Heading3']))
            chart_description = """
            <b>Enhanced Spending Distribution:</b><br/>
            This comprehensive visualization combines visual charts with detailed breakdowns, 
            automatically adapting based on the number of categories for optimal clarity.
            """
            story.append(Paragraph(chart_description, body_style))
            story.append(Spacer(1, 10))

            chart_buffer = create_enhanced_pie_chart(category_totals, "Comprehensive Spending Breakdown")
            if chart_buffer:
                # Add enhanced chart with larger size for better visibility
                chart_image = ReportLabImage(chart_buffer, width=7*inch, height=5.25*inch)
                story.append(chart_image)
                story.append(Spacer(1, 15))

            # Chart 3: Spending Trend Over Time
            story.append(Paragraph("📅 Spending Trends Over Time", styles['Heading3']))
            trend_chart_buffer = create_spending_trend_chart(transactions, "Monthly Spending Patterns")
            if trend_chart_buffer:
                story.append(Spacer(1, 10))
                trend_description = """
                <b>Temporal Analysis:</b> Track your spending patterns over time to identify seasonal trends, 
                spending spikes, and overall financial behavior patterns.
                """
                story.append(Paragraph(trend_description, body_style))
                story.append(Spacer(1, 10))

                trend_chart_image = ReportLabImage(trend_chart_buffer, width=6.5*inch, height=4*inch)
                story.append(trend_chart_image)
                story.append(Spacer(1, 15))

            # Add comprehensive insights about all visualizations
            total_spending = sum(category_totals.values())
            top_category = max(category_totals.items(), key=lambda x: x[1])
            top_percentage = (top_category[1] / total_spending) * 100

            insight_text = f"""
            <b>📊 Visual Analytics Summary:</b><br/>
            • <b>Primary Focus:</b> {top_category[0]} represents {top_percentage:.1f}% of total spending<br/>
            • <b>Diversification:</b> Spending distributed across {len(category_totals)} categories<br/>
            • <b>Total Volume:</b> ${total_spending:,.2f} analyzed across all transactions<br/>
            • <b>Chart Types:</b> Clean pie chart, detailed breakdown, and trend analysis included<br/>
            • <b>Insights:</b> Multiple visualization perspectives for comprehensive understanding
            """

            insight_style = ParagraphStyle(
                'ComprehensiveInsightStyle',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=15,
                leftIndent=20,
                rightIndent=20,
                backColor=colors.HexColor('#f0f8ff'),
                borderColor=colors.HexColor('#2E86AB'),
                borderWidth=2,
                borderPadding=15
            )

            story.append(Paragraph(insight_text, insight_style))

        else:
            # Fallback if no category data
            story.append(Paragraph("📊 Chart visualizations unavailable - insufficient category data for meaningful analysis", body_style))

        # Enhanced Footer with action summary
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=2, lineCap='round', color=colors.HexColor('#2E86AB')))
        story.append(Spacer(1, 15))

        # Action summary
        story.append(Paragraph("📋 Next Steps Summary", styles['Heading3']))
        action_summary = f"""1. Implement high-priority recommendations for immediate impact
2. Schedule monthly reviews to track progress
3. Reassess SpendScore quarterly to measure improvement
4. Consider professional consultation for complex optimizations"""
        story.append(Paragraph(action_summary, body_style))
        story.append(Spacer(1, 15))

        footer_text = """This comprehensive financial analysis was generated by the Verocta AI Financial Insight Platform. 
Report generated with OpenAI GPT-4o analysis engine. For questions or professional financial advice, 
consult with your certified financial advisor."""
        story.append(Paragraph(footer_text, styles['Normal']))

        # Build PDF
        doc.build(story)

        logging.info(f"PDF report generated successfully: {pdf_path}")
        return pdf_path

    except Exception as e:
        logging.error(f"Error generating PDF report: {str(e)}")
        raise Exception(f"Failed to generate PDF report: {str(e)}")


# Backward compatibility function
def create_pie_chart(category_data, title="Spending by Category"):
    """Backward compatibility wrapper for enhanced pie chart"""
    return create_enhanced_pie_chart(category_data, title)