import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { apiClient } from '../../utils/api'

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()
  const [systemStatus, setSystemStatus] = useState<'online' | 'offline' | 'checking'>('checking')

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'About', href: '/about' },
    { name: 'Services', href: '/services' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Contact', href: '/contact' },
  ]

  const isActive = (path: string) => location.pathname === path

  useEffect(() => {
    checkSystemStatus()
  }, [])

  const checkSystemStatus = async () => {
    try {
      await apiClient.get('/health')
      setSystemStatus('online')
    } catch (error) {
      setSystemStatus('offline')
    }
  }

  const getStatusIndicator = () => {
    switch (systemStatus) {
      case 'online':
        return (
          <div className="flex items-center text-green-600 text-xs">
            <div className="w-2 h-2 bg-green-600 rounded-full mr-1"></div>
            Online
          </div>
        )
      case 'offline':
        return (
          <div className="flex items-center text-red-600 text-xs">
            <div className="w-2 h-2 bg-red-600 rounded-full mr-1"></div>
            Offline
          </div>
        )
      case 'checking':
        return (
          <div className="flex items-center text-yellow-600 text-xs">
            <div className="w-2 h-2 bg-yellow-600 rounded-full mr-1 animate-pulse"></div>
            Checking
          </div>
        )
    }
  }

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <nav className="container-max">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <img 
              src="/verocta-logo.svg" 
              alt="VEROCTA - Financial Intelligence Platform" 
              className="h-10 w-auto"
              onError={(e) => {
                // Fallback to PNG if SVG fails
                e.currentTarget.src = '/verocta-logo.png';
              }}
            />
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                  isActive(item.href)
                    ? 'text-primary-600 bg-primary-50'
                    : 'text-gray-700 hover:text-primary-600 hover:bg-gray-50'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* CTA Button */}
          <div className="hidden md:flex space-x-3">
            <Link
              to="/login"
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-primary-600 transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/dashboard"
              className="btn-primary"
            >
              Dashboard
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 text-gray-700 hover:text-primary-600 transition-colors duration-200"
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4">
            <div className="space-y-2">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`block px-3 py-2 text-base font-medium rounded-md transition-colors duration-200 ${
                    isActive(item.href)
                      ? 'text-primary-600 bg-primary-50'
                      : 'text-gray-700 hover:text-primary-600 hover:bg-gray-50'
                  }`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              <div className="pt-4">
                <Link
                  to="/contact"
                  className="btn-primary block text-center"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Get Started
                </Link>
              </div>
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}

export default Header