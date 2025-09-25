"""
Email Service Integration for VeroctaAI
Handles email notifications, reports, and communications
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
import json

class EmailService:
    """Email service for handling notifications and communications"""
    
    def __init__(self):
        self.resend_api_key = os.environ.get('RESEND_API_KEY')
        self.postmark_api_key = os.environ.get('POSTMARK_API_KEY')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@verocta.ai')
        self.from_name = os.environ.get('FROM_NAME', 'VeroctaAI')
        
        # Determine which service to use
        if self.resend_api_key:
            self.service = 'resend'
            self.api_key = self.resend_api_key
        elif self.postmark_api_key:
            self.service = 'postmark'
            self.api_key = self.postmark_api_key
        else:
            self.service = None
            logging.warning("No email service configured - using demo mode")
    
    def send_welcome_email(self, user_email: str, user_name: str, company: str = None) -> bool:
        """Send welcome email to new user"""
        subject = "Welcome to VeroctaAI - Your Financial Intelligence Platform"
        html_content = self._get_welcome_email_template(user_name, company)
        
        return self._send_email(
            to=user_email,
            subject=subject,
            html_content=html_content,
            template_type='welcome'
        )
    
    def send_report_email(self, user_email: str, user_name: str, report_data: Dict) -> bool:
        """Send financial report via email"""
        subject = f"Your VeroctaAI Financial Report - {report_data.get('title', 'Financial Analysis')}"
        html_content = self._get_report_email_template(user_name, report_data)
        
        return self._send_email(
            to=user_email,
            subject=subject,
            html_content=html_content,
            template_type='report',
            attachments=report_data.get('attachments', [])
        )
    
    def send_subscription_confirmation(self, user_email: str, user_name: str, subscription_data: Dict) -> bool:
        """Send subscription confirmation email"""
        subject = "Subscription Confirmed - VeroctaAI Professional Plan"
        html_content = self._get_subscription_email_template(user_name, subscription_data)
        
        return self._send_email(
            to=user_email,
            subject=subject,
            html_content=html_content,
            template_type='subscription'
        )
    
    def send_payment_failed_notification(self, user_email: str, user_name: str, payment_data: Dict) -> bool:
        """Send payment failed notification"""
        subject = "Payment Failed - Action Required"
        html_content = self._get_payment_failed_template(user_name, payment_data)
        
        return self._send_email(
            to=user_email,
            subject=subject,
            html_content=html_content,
            template_type='payment_failed'
        )
    
    def send_weekly_digest(self, user_email: str, user_name: str, digest_data: Dict) -> bool:
        """Send weekly financial digest"""
        subject = "Your Weekly Financial Digest - VeroctaAI"
        html_content = self._get_digest_email_template(user_name, digest_data)
        
        return self._send_email(
            to=user_email,
            subject=subject,
            html_content=html_content,
            template_type='digest'
        )
    
    def _send_email(self, to: str, subject: str, html_content: str, 
                   template_type: str = 'general', attachments: List = None) -> bool:
        """Send email using configured service"""
        if not self.service:
            logging.info(f"Demo: Email sent to {to} - {subject}")
            return True
        
        try:
            if self.service == 'resend':
                return self._send_via_resend(to, subject, html_content, attachments)
            elif self.service == 'postmark':
                return self._send_via_postmark(to, subject, html_content, attachments)
            else:
                logging.error("Unknown email service")
                return False
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return False
    
    def _send_via_resend(self, to: str, subject: str, html_content: str, attachments: List = None) -> bool:
        """Send email via Resend API"""
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {self.resend_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [to],
            "subject": subject,
            "html": html_content
        }
        
        if attachments:
            data["attachments"] = attachments
        
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200
    
    def _send_via_postmark(self, to: str, subject: str, html_content: str, attachments: List = None) -> bool:
        """Send email via Postmark API"""
        url = "https://api.postmarkapp.com/email"
        headers = {
            "X-Postmark-Server-Token": self.postmark_api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "From": f"{self.from_name} <{self.from_email}>",
            "To": to,
            "Subject": subject,
            "HtmlBody": html_content
        }
        
        if attachments:
            data["Attachments"] = attachments
        
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200
    
    def _get_welcome_email_template(self, user_name: str, company: str = None) -> str:
        """Generate welcome email HTML template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to VeroctaAI</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #4F46E5;">Welcome to VeroctaAI!</h1>
                <p>Hi {user_name},</p>
                <p>Welcome to VeroctaAI - your AI-powered financial intelligence platform!</p>
                <p>We're excited to help you optimize your financial operations and gain valuable insights from your spending data.</p>
                
                <h2 style="color: #4F46E5;">Getting Started:</h2>
                <ul>
                    <li>Upload your CSV files from QuickBooks, Wave, Revolut, or Xero</li>
                    <li>Get instant SpendScore analysis</li>
                    <li>Receive AI-powered insights and recommendations</li>
                    <li>Generate professional financial reports</li>
                </ul>
                
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Best regards,<br>The VeroctaAI Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_report_email_template(self, user_name: str, report_data: Dict) -> str:
        """Generate report email HTML template"""
        spend_score = report_data.get('spend_score', 0)
        title = report_data.get('title', 'Financial Analysis')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Your VeroctaAI Report</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #4F46E5;">Your Financial Report is Ready!</h1>
                <p>Hi {user_name},</p>
                <p>Your financial analysis report "{title}" has been completed.</p>
                
                <div style="background: #F3F4F6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #4F46E5; margin-top: 0;">SpendScore: {spend_score}/100</h3>
                    <p>Your financial efficiency score based on our AI analysis.</p>
                </div>
                
                <p>Key insights from your analysis:</p>
                <ul>
                    <li>Identified {report_data.get('duplicate_expenses', 0)} duplicate expenses</li>
                    <li>Found {report_data.get('spending_spikes', 0)} spending spikes</li>
                    <li>Discovered {report_data.get('savings_opportunities', 0)} savings opportunities</li>
                </ul>
                
                <p>Your detailed report is attached to this email.</p>
                <p>Best regards,<br>The VeroctaAI Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_subscription_email_template(self, user_name: str, subscription_data: Dict) -> str:
        """Generate subscription confirmation email template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Subscription Confirmed</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #4F46E5;">Subscription Confirmed!</h1>
                <p>Hi {user_name},</p>
                <p>Thank you for subscribing to VeroctaAI Professional!</p>
                <p>Your subscription is now active and you have access to all premium features.</p>
                <p>Best regards,<br>The VeroctaAI Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_payment_failed_template(self, user_name: str, payment_data: Dict) -> str:
        """Generate payment failed email template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Payment Failed</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #DC2626;">Payment Failed</h1>
                <p>Hi {user_name},</p>
                <p>We were unable to process your payment. Please update your payment method to continue using VeroctaAI.</p>
                <p>Best regards,<br>The VeroctaAI Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_digest_email_template(self, user_name: str, digest_data: Dict) -> str:
        """Generate weekly digest email template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Weekly Financial Digest</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #4F46E5;">Your Weekly Financial Digest</h1>
                <p>Hi {user_name},</p>
                <p>Here's your weekly financial summary from VeroctaAI.</p>
                <p>Best regards,<br>The VeroctaAI Team</p>
            </div>
        </body>
        </html>
        """

# Global email service instance
email_service = EmailService()
