// User types
export interface User {
  id: string
  email: string
  name: string
  role: 'user' | 'admin'
  avatar?: string
  createdAt: Date
  updatedAt: Date
}

// Auth types
export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  name: string
  email: string
  password: string
  confirmPassword: string
}

export interface AuthResponse {
  user: User
  token: string
}

// Contact types
export interface ContactForm {
  name: string
  email: string
  company?: string
  service: string
  message: string
}

export interface ContactSubmission {
  id: string
  ...ContactForm
  status: 'pending' | 'reviewed' | 'responded'
  createdAt: Date
  updatedAt: Date
}

// Service types
export interface Service {
  id: string
  title: string
  description: string
  features: string[]
  price: string
  icon: string
  category: 'consulting' | 'development' | 'analytics' | 'security' | 'cloud'
}

// Project types
export interface Project {
  id: string
  title: string
  description: string
  client: string
  services: string[]
  status: 'planning' | 'in-progress' | 'completed' | 'maintenance'
  startDate: Date
  endDate?: Date
  technologies: string[]
  image?: string
}

// API response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

// Form types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'checkbox'
  required?: boolean
  placeholder?: string
  options?: { value: string; label: string }[]
  validation?: {
    minLength?: number
    maxLength?: number
    pattern?: RegExp
    custom?: (value: any) => string | undefined
  }
}

// UI types
export interface NavItem {
  name: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  children?: NavItem[]
}

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  children: React.ReactNode
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  className?: string
}

// Theme types
export interface Theme {
  name: string
  primary: string
  secondary: string
  background: string
  surface: string
  text: string
  textSecondary: string
}

// Notification types
export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}
