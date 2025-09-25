// Application constants
export const APP_CONFIG = {
  name: 'VEROCTA',
  description: 'AI-Powered Financial Intelligence Platform',
  version: '2.0.0',
  author: 'VEROCTA Team',
  website: 'https://verocta.ai',
  supportEmail: 'support@verocta.ai',
  contactEmail: 'hello@verocta.ai',
  phone: '+1 (555) 123-4567',
  address: '123 AI Street, Tech City, TC 12345',
  businessHours: 'Mon-Fri: 9AM-6PM EST',
}

// API configuration
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  timeout: 10000,
  retryAttempts: 3,
  retryDelay: 1000,
}

// Feature flags
export const FEATURES = {
  enableAnalytics: true,
  enableNotifications: true,
  enableDarkMode: false,
  enableMultiLanguage: false,
  enableSSO: false,
}

// Social media links
export const SOCIAL_LINKS = {
  twitter: 'https://twitter.com/veroctaai',
  linkedin: 'https://linkedin.com/company/verocta-ai',
  github: 'https://github.com/verocta-ai',
  youtube: 'https://youtube.com/@veroctaai',
}

// Navigation configuration
export const NAVIGATION = {
  main: [
    { name: 'Home', href: '/', icon: 'HomeIcon' },
    { name: 'About', href: '/about', icon: 'InformationCircleIcon' },
    { name: 'Services', href: '/services', icon: 'CogIcon' },
    { name: 'Contact', href: '/contact', icon: 'EnvelopeIcon' },
  ],
  footer: [
    { name: 'Privacy Policy', href: '/privacy' },
    { name: 'Terms of Service', href: '/terms' },
    { name: 'Cookie Policy', href: '/cookies' },
    { name: 'Sitemap', href: '/sitemap' },
  ],
}

// Service categories
export const SERVICE_CATEGORIES = {
  consulting: {
    name: 'AI Consulting',
    description: 'Strategic guidance and planning for AI implementation',
    icon: 'LightBulbIcon',
  },
  development: {
    name: 'Custom Development',
    description: 'Tailored AI solutions for specific business needs',
    icon: 'CodeBracketIcon',
  },
  analytics: {
    name: 'Data Analytics',
    description: 'Advanced analytics and business intelligence',
    icon: 'ChartBarIcon',
  },
  security: {
    name: 'AI Security',
    description: 'Comprehensive security for AI systems',
    icon: 'ShieldCheckIcon',
  },
  cloud: {
    name: 'Cloud Solutions',
    description: 'Scalable AI solutions on cloud infrastructure',
    icon: 'CloudIcon',
  },
}

// Contact form fields
export const CONTACT_FORM_FIELDS = [
  { name: 'name', label: 'Full Name', type: 'text', required: true },
  { name: 'email', label: 'Email Address', type: 'email', required: true },
  { name: 'company', label: 'Company', type: 'text', required: false },
  { name: 'service', label: 'Service Interest', type: 'select', required: true },
  { name: 'message', label: 'Message', type: 'textarea', required: true },
]

// Validation rules
export const VALIDATION_RULES = {
  name: {
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s]+$/,
  },
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  },
  message: {
    minLength: 10,
    maxLength: 1000,
  },
}

// Animation durations
export const ANIMATIONS = {
  fast: 150,
  normal: 300,
  slow: 500,
  verySlow: 1000,
}

// Breakpoints (matching Tailwind CSS)
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
}

// Local storage keys
export const STORAGE_KEYS = {
  authToken: 'authToken',
  userPreferences: 'userPreferences',
  theme: 'theme',
  language: 'language',
}

// Error messages
export const ERROR_MESSAGES = {
  required: 'This field is required',
  invalidEmail: 'Please enter a valid email address',
  invalidPhone: 'Please enter a valid phone number',
  minLength: (min: number) => `Must be at least ${min} characters`,
  maxLength: (max: number) => `Must be no more than ${max} characters`,
  networkError: 'Network error. Please try again.',
  serverError: 'Server error. Please try again later.',
  unauthorized: 'You are not authorized to perform this action.',
  notFound: 'The requested resource was not found.',
}

// Success messages
export const SUCCESS_MESSAGES = {
  contactSubmitted: 'Thank you for your message! We\'ll get back to you within 24 hours.',
  profileUpdated: 'Your profile has been updated successfully.',
  passwordChanged: 'Your password has been changed successfully.',
  emailSent: 'Email sent successfully.',
  dataSaved: 'Data saved successfully.',
}
