import React, { useState } from 'react'
import { Routes, Route, Navigate, Link } from 'react-router-dom'
import Sidebar from '../components/Layout/Sidebar'
import Breadcrumb from '../components/Layout/Breadcrumb'
import DashboardHome from '../components/DashboardHome'
import UploadManager from '../components/UploadManager'
import InsightsEngine from '../components/InsightsEngine'
import ReportsManager from '../components/ReportsManager'
import SettingsManager from '../components/SettingsManager'
import PaymentsManager from '../components/PaymentsManager'
import AdminDashboard from '../components/AdminDashboard'
import { useAuth } from '../contexts/AuthContext'
import { HomeIcon } from '@heroicons/react/24/outline'

const Dashboard: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <div className="flex-1 lg:ml-64">
        {/* Top Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>

                {/* Logo and Title */}
              <div className="flex items-center space-x-4">
                <img 
                  src="/verocta-logo.svg" 
                  alt="VEROCTA - Financial Intelligence Platform" 
                  className="h-8 w-auto"
                  onError={(e) => {
                    e.currentTarget.src = '/verocta-logo.png';
                  }}
                />
                <div>
                  <h1 className="text-xl font-semibold text-gray-900">VeroctaAI Dashboard</h1>
                </div>
              </div>

                {/* Back to Home Button */}
                <Link
                  to="/"
                  className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
                >
                  <HomeIcon className="h-4 w-4" />
                  <span>Back to Home</span>
                </Link>
              </div>

              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-500">
                  Welcome back, {user?.email || 'User'}
                </div>
                <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {user?.email?.charAt(0).toUpperCase() || 'U'}
                </div>
              </div>
            </div>

            {/* Breadcrumb Navigation */}
            <div className="py-3 border-t border-gray-100">
              <Breadcrumb />
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="py-6">
          <div className="px-4 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<DashboardHome />} />
              <Route path="/upload" element={<UploadManager />} />
              <Route path="/insights" element={<InsightsEngine />} />
              <Route path="/reports" element={<ReportsManager />} />
              <Route path="/billing" element={<PaymentsManager />} />
              <Route path="/settings" element={<SettingsManager />} />
              {user?.role === 'admin' && (
                <Route path="/admin" element={<AdminDashboard />} />
              )}
              <Route path="*" element={<Navigate to="/dashboard" />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard