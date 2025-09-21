"""
Payment Service Integration for VeroctaAI
Handles Stripe subscriptions, billing, and payment processing
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import stripe

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class PaymentService:
    """Payment service for handling Stripe subscriptions and billing"""
    
    def __init__(self):
        self.stripe_enabled = bool(stripe.api_key)
        if not self.stripe_enabled:
            logging.warning("Stripe not configured - using demo mode")
    
    def create_customer(self, email: str, name: str = None, company: str = None) -> Optional[Dict]:
        """Create Stripe customer"""
        if not self.stripe_enabled:
            return self._demo_customer(email, name, company)
        
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    'company': company or 'Default Company',
                    'platform': 'verocta-ai'
                }
            )
            return customer
        except Exception as e:
            logging.error(f"Error creating Stripe customer: {str(e)}")
            return None
    
    def create_subscription(self, customer_id: str, price_id: str) -> Optional[Dict]:
        """Create subscription for customer"""
        if not self.stripe_enabled:
            return self._demo_subscription(customer_id, price_id)
        
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent']
            )
            return subscription
        except Exception as e:
            logging.error(f"Error creating subscription: {str(e)}")
            return None
    
    def get_subscription(self, subscription_id: str) -> Optional[Dict]:
        """Get subscription details"""
        if not self.stripe_enabled:
            return self._demo_subscription(subscription_id, 'price_professional')
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription
        except Exception as e:
            logging.error(f"Error retrieving subscription: {str(e)}")
            return None
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel subscription"""
        if not self.stripe_enabled:
            logging.info(f"Demo: Cancelled subscription {subscription_id}")
            return True
        
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            logging.error(f"Error cancelling subscription: {str(e)}")
            return False
    
    def create_payment_intent(self, amount: int, currency: str = 'usd', customer_id: str = None) -> Optional[Dict]:
        """Create payment intent for one-time payments"""
        if not self.stripe_enabled:
            return self._demo_payment_intent(amount, currency)
        
        try:
            intent_data = {
                'amount': amount,
                'currency': currency,
                'automatic_payment_methods': {'enabled': True}
            }
            
            if customer_id:
                intent_data['customer'] = customer_id
            
            payment_intent = stripe.PaymentIntent.create(**intent_data)
            return payment_intent
        except Exception as e:
            logging.error(f"Error creating payment intent: {str(e)}")
            return None
    
    def handle_webhook(self, payload: str, sig_header: str) -> bool:
        """Handle Stripe webhook events"""
        if not self.stripe_enabled:
            logging.info("Demo: Webhook received")
            return True
        
        try:
            webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
            if not webhook_secret:
                logging.error("Stripe webhook secret not configured")
                return False
            
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            
            # Handle different event types
            if event['type'] == 'customer.subscription.created':
                self._handle_subscription_created(event['data']['object'])
            elif event['type'] == 'customer.subscription.updated':
                self._handle_subscription_updated(event['data']['object'])
            elif event['type'] == 'customer.subscription.deleted':
                self._handle_subscription_deleted(event['data']['object'])
            elif event['type'] == 'invoice.payment_succeeded':
                self._handle_payment_succeeded(event['data']['object'])
            elif event['type'] == 'invoice.payment_failed':
                self._handle_payment_failed(event['data']['object'])
            
            return True
        except Exception as e:
            logging.error(f"Error handling webhook: {str(e)}")
            return False
    
    def _handle_subscription_created(self, subscription: Dict):
        """Handle subscription created event"""
        logging.info(f"Subscription created: {subscription['id']}")
        # Update user subscription status in database
    
    def _handle_subscription_updated(self, subscription: Dict):
        """Handle subscription updated event"""
        logging.info(f"Subscription updated: {subscription['id']}")
        # Update user subscription status in database
    
    def _handle_subscription_deleted(self, subscription: Dict):
        """Handle subscription deleted event"""
        logging.info(f"Subscription deleted: {subscription['id']}")
        # Update user subscription status in database
    
    def _handle_payment_succeeded(self, invoice: Dict):
        """Handle successful payment"""
        logging.info(f"Payment succeeded: {invoice['id']}")
        # Send confirmation email, update user status
    
    def _handle_payment_failed(self, invoice: Dict):
        """Handle failed payment"""
        logging.info(f"Payment failed: {invoice['id']}")
        # Send notification email, update user status
    
    def _demo_customer(self, email: str, name: str = None, company: str = None) -> Dict:
        """Demo customer for testing"""
        return {
            'id': f'demo_customer_{email.replace("@", "_")}',
            'email': email,
            'name': name,
            'metadata': {'company': company or 'Default Company'}
        }
    
    def _demo_subscription(self, customer_id: str, price_id: str) -> Dict:
        """Demo subscription for testing"""
        return {
            'id': f'demo_sub_{customer_id}',
            'customer': customer_id,
            'status': 'active',
            'current_period_start': int(datetime.now().timestamp()),
            'current_period_end': int((datetime.now() + timedelta(days=30)).timestamp()),
            'items': {'data': [{'price': {'id': price_id}}]}
        }
    
    def _demo_payment_intent(self, amount: int, currency: str) -> Dict:
        """Demo payment intent for testing"""
        return {
            'id': f'demo_pi_{int(datetime.now().timestamp())}',
            'amount': amount,
            'currency': currency,
            'status': 'succeeded',
            'client_secret': f'demo_secret_{int(datetime.now().timestamp())}'
        }

# Global payment service instance
payment_service = PaymentService()
