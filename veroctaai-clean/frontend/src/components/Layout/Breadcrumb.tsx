import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { ChevronRightIcon, HomeIcon } from '@heroicons/react/20/solid'

interface BreadcrumbItem {
  name: string
  href?: string
  current?: boolean
}

const Breadcrumb: React.FC = () => {
  const location = useLocation()
  
  const getBreadcrumbs = (): BreadcrumbItem[] => {
    const pathSegments = location.pathname.split('/').filter(Boolean)
    const breadcrumbs: BreadcrumbItem[] = []
    
    // Always start with home
    breadcrumbs.push({ name: 'Home', href: '/' })
    
    if (pathSegments.includes('dashboard')) {
      breadcrumbs.push({ name: 'Dashboard', href: '/dashboard' })
      
      // Add specific dashboard pages
      if (pathSegments.includes('upload')) {
        breadcrumbs.push({ name: 'Upload Data', current: true })
      } else if (pathSegments.includes('insights')) {
        breadcrumbs.push({ name: 'Insights Engine', current: true })
      } else if (pathSegments.includes('reports')) {
        breadcrumbs.push({ name: 'Reports', current: true })
      } else if (pathSegments.includes('billing')) {
        breadcrumbs.push({ name: 'Billing', current: true })
      } else if (pathSegments.includes('settings')) {
        breadcrumbs.push({ name: 'Settings', current: true })
      } else if (pathSegments.includes('admin')) {
        breadcrumbs.push({ name: 'Admin', current: true })
      } else if (location.pathname === '/dashboard' || location.pathname === '/dashboard/') {
        breadcrumbs[breadcrumbs.length - 1].current = true
      }
    } else {
      // For other pages
      if (pathSegments.includes('about')) {
        breadcrumbs.push({ name: 'About', current: true })
      } else if (pathSegments.includes('services')) {
        breadcrumbs.push({ name: 'Services', current: true })
      } else if (pathSegments.includes('contact')) {
        breadcrumbs.push({ name: 'Contact', current: true })
      } else if (pathSegments.includes('login')) {
        breadcrumbs.push({ name: 'Sign In', current: true })
      } else if (pathSegments.includes('register')) {
        breadcrumbs.push({ name: 'Sign Up', current: true })
      } else if (location.pathname === '/') {
        breadcrumbs[0].current = true
      }
    }
    
    return breadcrumbs
  }

  const breadcrumbs = getBreadcrumbs()

  return (
    <nav className="flex" aria-label="Breadcrumb">
      <ol className="flex items-center space-x-4">
        {breadcrumbs.map((breadcrumb, index) => (
          <li key={breadcrumb.name}>
            <div className="flex items-center">
              {index === 0 && (
                <HomeIcon className="h-4 w-4 text-gray-400 mr-2" />
              )}
              {index > 0 && (
                <ChevronRightIcon className="h-4 w-4 text-gray-400 mr-4" />
              )}
              {breadcrumb.current ? (
                <span className="text-sm font-medium text-gray-900">
                  {breadcrumb.name}
                </span>
              ) : (
                <Link
                  to={breadcrumb.href || '#'}
                  className="text-sm font-medium text-gray-500 hover:text-gray-700 transition-colors"
                >
                  {breadcrumb.name}
                </Link>
              )}
            </div>
          </li>
        ))}
      </ol>
    </nav>
  )
}

export default Breadcrumb