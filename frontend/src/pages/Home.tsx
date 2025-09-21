import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRightIcon, ChartBarIcon, CurrencyDollarIcon, DocumentChartBarIcon, SparklesIcon } from '@heroicons/react/24/outline'

const Home: React.FC = () => {
  const features = [
    {
      icon: ChartBarIcon,
      title: 'SpendScore™ Analytics',
      description: 'Get your financial health score (0-100) with actionable insights to optimize spending patterns.'
    },
    {
      icon: CurrencyDollarIcon,
      title: 'Waste Detection',
      description: 'Automatically identify duplicate subscriptions, unused services, and spending anomalies.'
    },
    {
      icon: DocumentChartBarIcon,
      title: 'Smart Reports',
      description: 'Generate comprehensive PDF reports with charts, recommendations, and forecasting.'
    },
    {
      icon: SparklesIcon,
      title: 'AI-Powered Insights',
      description: 'Advanced analytics with category breakdowns, trends, and optimization recommendations.'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Hero Section */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Optimize Your Business Spending with{' '}
            <span className="text-gradient">VEROCTA AI</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            VEROCTA analyzes your financial data to identify waste, track spending patterns, 
            and provide actionable AI-powered recommendations to reduce costs and improve efficiency.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/dashboard" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 flex items-center justify-center">
              Demo Dashboard
              <ArrowRightIcon className="w-5 h-5 ml-2" />
            </Link>
            <Link to="/register" className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg hover:bg-gray-50">
              Start Free Trial
            </Link>
          </div>
        </div>
      </section>

      {/* Demo Dashboard Feature */}
      <section className="py-16 bg-gradient-to-r from-green-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-white rounded-2xl shadow-lg p-8 max-w-4xl mx-auto">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
              <ChartBarIcon className="w-8 h-8 text-green-600" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              🚀 NEW: Interactive Demo Dashboard
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Experience the full power of VEROCTA's financial intelligence platform. 
              No signup required - explore all features instantly!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link 
                to="/dashboard" 
                className="bg-green-600 text-white px-8 py-4 rounded-lg hover:bg-green-700 flex items-center justify-center text-lg font-medium"
              >
                🎯 Try Demo Dashboard
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </Link>
              <Link 
                to="/services" 
                className="border border-gray-300 text-gray-700 px-8 py-4 rounded-lg hover:bg-gray-50 text-lg font-medium"
              >
                Learn More
              </Link>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
              <div className="flex items-center justify-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                SpendScore™ Analytics
              </div>
              <div className="flex items-center justify-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Waste Detection
              </div>
              <div className="flex items-center justify-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                PDF Reports
              </div>
              <div className="flex items-center justify-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Admin Dashboard
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Powerful Financial Intelligence
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to understand, optimize, and control your business spending.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-lg font-medium text-gray-600 mb-8">
            Trusted by finance teams at growing companies
          </h3>
          <div className="flex items-center justify-center space-x-8 opacity-50">
            <div className="bg-gray-200 h-8 w-24 rounded"></div>
            <div className="bg-gray-200 h-8 w-24 rounded"></div>
            <div className="bg-gray-200 h-8 w-24 rounded"></div>
            <div className="bg-gray-200 h-8 w-24 rounded"></div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to optimize your spending?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join hundreds of businesses already saving money with VEROCTA's AI-powered insights.
          </p>
          <Link to="/register" className="bg-white text-blue-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors">
            Start Your Free Trial
          </Link>
        </div>
      </section>

    </div>
  )
}

export default Home