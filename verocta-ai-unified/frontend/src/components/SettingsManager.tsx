import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { 
  UserIcon, 
  BellIcon,
  KeyIcon,
  EnvelopeIcon,
  CogIcon,
  CheckIcon
} from '@heroicons/react/24/outline'

interface NotificationSettings {
  emailReports: boolean
  weeklyDigest: boolean
  spendingAlerts: boolean
  systemUpdates: boolean
  marketingEmails: boolean
}

const SettingsManager: React.FC = () => {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('profile')
  const [saved, setSaved] = useState(false)
  
  const [profile, setProfile] = useState({
    name: user?.email?.split('@')[0] || 'User',
    email: user?.email || '',
    company: user?.company || '',
    phone: '+1 (555) 123-4567',
    timezone: 'America/New_York'
  })

  const [notifications, setNotifications] = useState<NotificationSettings>({
    emailReports: true,
    weeklyDigest: true,
    spendingAlerts: true,
    systemUpdates: true,
    marketingEmails: false
  })

  const [emailSettings, setEmailSettings] = useState({
    deliveryTime: '09:00',
    frequency: 'weekly',
    format: 'pdf',
    includeCharts: true,
    autoSend: true
  })

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const handleNotificationChange = (key: keyof NotificationSettings) => {
    setNotifications(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">Account Settings</h2>
        <p className="mt-2 text-gray-600">Manage your account preferences and configurations</p>
      </div>

      {/* Save Banner */}
      {saved && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <CheckIcon className="h-5 w-5 text-green-600" />
            <p className="ml-2 text-sm text-green-700">Settings saved successfully!</p>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'profile', name: 'Profile', icon: UserIcon },
            { id: 'notifications', name: 'Notifications', icon: BellIcon },
            { id: 'email', name: 'Email Delivery', icon: EnvelopeIcon },
            { id: 'api', name: 'API Access', icon: KeyIcon },
            { id: 'advanced', name: 'Advanced', icon: CogIcon }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`${
                activeTab === tab.id
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center`}
            >
              <tab.icon className="h-5 w-5 mr-2" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Personal Information</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Full Name</label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => setProfile(prev => ({ ...prev, name: e.target.value }))}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Email Address</label>
                <input
                  type="email"
                  value={profile.email}
                  onChange={(e) => setProfile(prev => ({ ...prev, email: e.target.value }))}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Company</label>
                <input
                  type="text"
                  value={profile.company}
                  onChange={(e) => setProfile(prev => ({ ...prev, company: e.target.value }))}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Account Security</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Password</p>
                  <p className="text-sm text-gray-600">Last updated 30 days ago</p>
                </div>
                <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                  Change Password
                </button>
              </div>
              
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Two-Factor Authentication</p>
                  <p className="text-sm text-gray-600">Add an extra layer of security</p>
                </div>
                <button className="bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700">
                  Enable 2FA
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Email Delivery Tab */}
      {activeTab === 'email' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Automated Email Delivery</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">Delivery Time</label>
                <input
                  type="time"
                  value={emailSettings.deliveryTime}
                  onChange={(e) => setEmailSettings(prev => ({ ...prev, deliveryTime: e.target.value }))}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Frequency</label>
                <select
                  value={emailSettings.frequency}
                  onChange={(e) => setEmailSettings(prev => ({ ...prev, frequency: e.target.value }))}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Report Format</label>
                <select
                  value={emailSettings.format}
                  onChange={(e) => setEmailSettings(prev => ({ ...prev, format: e.target.value }))}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                >
                  <option value="pdf">PDF Report</option>
                  <option value="excel">Excel Spreadsheet</option>
                  <option value="html">HTML Email</option>
                </select>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 rounded-lg p-6">
            <h4 className="font-medium text-blue-900 mb-2">Email Delivery Features</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Automated delivery of financial reports</li>
              <li>• Customizable scheduling and formatting</li>
              <li>• Secure delivery with encryption</li>
              <li>• Multiple recipients support</li>
              <li>• Delivery confirmation tracking</li>
            </ul>
          </div>
        </div>
      )}

      {/* API Access Tab */}
      {activeTab === 'api' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">API Access</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">API Key</label>
                <div className="flex">
                  <input
                    type="password"
                    value="vta_live_sk_1234567890abcdef"
                    readOnly
                    className="flex-1 border border-gray-300 rounded-l-md px-3 py-2 text-sm bg-gray-50"
                  />
                  <button className="border border-l-0 border-gray-300 rounded-r-md px-4 py-2 text-sm bg-gray-50 hover:bg-gray-100">
                    Copy
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-6">
            <h4 className="font-medium text-gray-900 mb-2">API Documentation</h4>
            <p className="text-sm text-gray-600 mb-4">
              Access comprehensive API documentation and integration guides.
            </p>
            <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 text-sm">
              View API Docs
            </button>
          </div>
        </div>
      )}

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          className="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700"
        >
          Save Changes
        </button>
      </div>
    </div>
  )
}

export default SettingsManager