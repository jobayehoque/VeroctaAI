import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  CurrencyDollarIcon,
  UsersIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CloudArrowUpIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'
import { apiClient } from '../utils/api'

interface SpendScore {
  score: number
  status: 'excellent' | 'good' | 'warning' | 'critical'
  recommendations: string[]
}

const DashboardHome: React.FC = () => {
  const [stats, setStats] = useState([
    { name: 'Total Reports', value: '0', icon: DocumentTextIcon, change: '+0%', changeType: 'positive' },
    { name: 'SpendScore™', value: '0', icon: ChartBarIcon, change: '+0%', changeType: 'positive' },
    { name: 'Cost Savings', value: '$0', icon: CurrencyDollarIcon, change: '+0%', changeType: 'positive' },
    { name: 'Waste Detected', value: '0%', icon: ExclamationTriangleIcon, change: '+0%', changeType: 'negative' },
  ])
  
  const [spendScore, setSpendScore] = useState<SpendScore>({
    score: 0,
    status: 'critical',
    recommendations: ['Upload your first financial data to get started with insights']
  })
  
  const [recentReports, setRecentReports] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      // Fetch reports with error handling
      let reports = []
      try {
        const reportsResponse = await apiClient.get('/reports')
        reports = reportsResponse.data?.reports || []
      } catch (reportsError) {
        console.log('Reports not available:', reportsError.message)
      }
      
      // Fetch latest spend score if available
      let latestScore = null
      try {
        const scoreResponse = await apiClient.get('/spend-score')
        latestScore = scoreResponse.data
      } catch (scoreError) {
        console.log('No spend score data available yet')
      }
      
      // Update stats
      if (reports.length > 0) {
        const avgScore = Math.round(reports.reduce((sum: number, r: any) => sum + (r.spend_score || 0), 0) / reports.length)
        const totalSavings = reports.reduce((sum: number, r: any) => sum + ((r.data?.total_amount || 0) * 0.15), 0)
        const wastePercentage = reports.length > 0 ? Math.round(reports.reduce((sum: number, r: any) => sum + (r.insights?.waste_percentage || 0), 0) / reports.length) : 0
        
        setStats([
          { name: 'Total Reports', value: reports.length.toString(), icon: DocumentTextIcon, change: '+2.1%', changeType: 'positive' },
          { name: 'SpendScore™', value: avgScore.toString(), icon: ChartBarIcon, change: '+4.3%', changeType: 'positive' },
          { name: 'Cost Savings', value: `$${Math.round(totalSavings).toLocaleString()}`, icon: CurrencyDollarIcon, change: '+12.5%', changeType: 'positive' },
          { name: 'Waste Detected', value: `${wastePercentage}%`, icon: ExclamationTriangleIcon, change: '-3.2%', changeType: 'negative' },
        ])
      }
      
      // Update spend score
      if (latestScore) {
        const scoreValue = latestScore.score || 0
        let status: 'excellent' | 'good' | 'warning' | 'critical' = 'critical'
        if (scoreValue >= 80) status = 'excellent'
        else if (scoreValue >= 60) status = 'good'
        else if (scoreValue >= 40) status = 'warning'
        
        setSpendScore({
          score: scoreValue,
          status,
          recommendations: latestScore.recommendations || ['Upload more data for better insights']
        })
      }
      
      setRecentReports(reports.slice(0, 5))
      
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'text-green-600 bg-green-100'
      case 'good': return 'text-blue-600 bg-blue-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getScoreRing = (score: number, status: string) => {
    const percentage = (score / 100) * 283 // 283 is circumference of circle with radius 45
    let strokeColor = '#ef4444' // red
    if (status === 'excellent') strokeColor = '#22c55e' // green
    else if (status === 'good') strokeColor = '#3b82f6' // blue
    else if (status === 'warning') strokeColor = '#f59e0b' // yellow
    
    return { strokeDasharray: `${percentage} 283`, stroke: strokeColor }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
        <p className="mt-1 text-sm text-gray-500">
          Your financial intelligence dashboard with insights and analytics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div key={item.name} className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <item.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{item.name}</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{item.value}</div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        item.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {item.changeType === 'positive' ? (
                          <ArrowUpIcon className="h-3 w-3 mr-1" />
                        ) : (
                          <ArrowDownIcon className="h-3 w-3 mr-1" />
                        )}
                        {item.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* SpendScore and Quick Actions Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* SpendScore Card */}
        <div className="lg:col-span-1">
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">SpendScore™</h3>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getScoreColor(spendScore.status)}`}>
                {spendScore.status.charAt(0).toUpperCase() + spendScore.status.slice(1)}
              </span>
            </div>
            
            <div className="flex items-center justify-center">
              <div className="relative w-32 h-32">
                <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 100 100">
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    stroke="#e5e7eb"
                    strokeWidth="8"
                    fill="none"
                  />
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    strokeWidth="8"
                    fill="none"
                    strokeLinecap="round"
                    style={getScoreRing(spendScore.score, spendScore.status)}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <span className="text-2xl font-bold text-gray-900">{spendScore.score}</span>
                    <span className="text-sm text-gray-500 block">/ 100</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Recommendations:</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                {spendScore.recommendations.slice(0, 2).map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-1 h-1 bg-gray-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Link
                to="/dashboard/upload"
                className="relative group bg-blue-50 p-4 rounded-lg border-2 border-dashed border-blue-300 hover:border-blue-400 transition-colors"
              >
                <div className="flex items-center">
                  <CloudArrowUpIcon className="h-8 w-8 text-blue-500" />
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-blue-900">Upload Data</h4>
                    <p className="text-sm text-blue-700">Import CSV or connect Google Sheets</p>
                  </div>
                </div>
              </Link>
              
              <Link
                to="/dashboard/insights"
                className="relative group bg-green-50 p-4 rounded-lg border border-green-200 hover:border-green-300 transition-colors"
              >
                <div className="flex items-center">
                  <ChartBarIcon className="h-8 w-8 text-green-500" />
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-green-900">View Insights</h4>
                    <p className="text-sm text-green-700">Analyze spending patterns</p>
                  </div>
                </div>
              </Link>
              
              <Link
                to="/dashboard/reports"
                className="relative group bg-purple-50 p-4 rounded-lg border border-purple-200 hover:border-purple-300 transition-colors"
              >
                <div className="flex items-center">
                  <DocumentTextIcon className="h-8 w-8 text-purple-500" />
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-purple-900">Generate Report</h4>
                    <p className="text-sm text-purple-700">Create PDF analysis</p>
                  </div>
                </div>
              </Link>
              
              <Link
                to="/dashboard/billing"
                className="relative group bg-yellow-50 p-4 rounded-lg border border-yellow-200 hover:border-yellow-300 transition-colors"
              >
                <div className="flex items-center">
                  <CurrencyDollarIcon className="h-8 w-8 text-yellow-500" />
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-yellow-900">Billing</h4>
                    <p className="text-sm text-yellow-700">Manage subscription</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Reports */}
      {recentReports.length > 0 ? (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Recent Reports</h3>
              <Link
                to="/dashboard/reports"
                className="text-sm text-blue-600 hover:text-blue-500"
              >
                View all
              </Link>
            </div>
            
            <div className="overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Report Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      SpendScore
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recentReports.map((report: any) => (
                    <tr key={report.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {report.title || `Report ${report.id}`}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(report.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          (report.spend_score || 0) >= 80 ? 'bg-green-100 text-green-800' :
                          (report.spend_score || 0) >= 60 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {report.spend_score || 0}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                          Completed
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg p-6 text-center">
          <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No reports yet</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by uploading your financial data.</p>
          <div className="mt-6">
            <Link
              to="/dashboard/upload"
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <CloudArrowUpIcon className="-ml-1 mr-2 h-5 w-5" />
              Upload Data
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}

export default DashboardHome