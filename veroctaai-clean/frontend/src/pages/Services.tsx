import React from 'react'
import { Link } from 'react-router-dom'
import { 
  ChartBarIcon, 
  DocumentArrowUpIcon, 
  LightBulbIcon, 
  DocumentTextIcon,
  MagnifyingGlassIcon,
  CalculatorIcon 
} from '@heroicons/react/24/outline'

const Services: React.FC = () => {
  const services = [
    {
      icon: ChartBarIcon,
      title: '🚀 Demo Dashboard (NEW)',
      description: 'Interactive financial intelligence platform - try all features instantly without signup!',
      features: ['SpendScore™ Analytics', 'Waste Detection', 'PDF Reports', 'Admin Dashboard'],
      price: 'Free Demo',
      isDemo: true,
      link: '/dashboard'
    },
    {
      icon: CalculatorIcon,
      title: 'SpendScore™ Analytics',
      description: 'AI-powered 6-metric financial health scoring system that analyzes spending patterns and identifies optimization opportunities.',
      features: ['Frequency Analysis', 'Category Diversity', 'Budget Adherence', 'Redundancy Detection'],
      price: 'From $99/month'
    },
    {
      icon: DocumentArrowUpIcon,
      title: 'Multi-Platform Data Integration',
      description: 'Seamlessly connect and analyze data from QuickBooks, Wave, Revolut, Xero, and other accounting platforms.',
      features: ['CSV Upload Processing', 'Intelligent Header Mapping', 'Google Sheets Integration', 'Real-time Sync'],
      price: 'From $149/month'
    },
    {
      icon: LightBulbIcon,
      title: 'AI-Powered Insights Engine',
      description: 'GPT-4 powered financial analysis that provides actionable recommendations to optimize business spending.',
      features: ['Spending Pattern Analysis', 'Waste Detection', 'Cost Optimization Tips', 'Trend Predictions'],
      price: 'From $199/month'
    },
    {
      icon: DocumentTextIcon,
      title: 'Professional PDF Reports',
      description: 'Automatically generated comprehensive financial reports with charts, insights, and custom branding.',
      features: ['Custom Company Branding', 'Interactive Charts', 'Executive Summaries', 'Scheduled Delivery'],
      price: 'From $79/month'
    },
    {
      icon: MagnifyingGlassIcon,
      title: 'Financial Health Monitoring',
      description: 'Continuous monitoring of financial metrics with alerts for spending anomalies and budget variances.',
      features: ['Real-time Alerts', 'Spike Detection', 'Budget Tracking', 'Performance Dashboards'],
      price: 'From $129/month'
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 to-secondary-50 section-padding">
        <div className="container-max text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Financial Intelligence <span className="text-gradient">Services</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Transform your business spending with AI-powered financial analytics, 
            automated insights, and comprehensive reporting solutions.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="section-padding bg-white">
        <div className="container-max">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <div key={index} className={`card hover:shadow-xl transition-all duration-300 hover:-translate-y-1 relative ${
                service.isDemo ? 'ring-2 ring-green-500 bg-gradient-to-br from-green-50 to-blue-50' : ''
              }`}>
                {service.isDemo && (
                  <div className="bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full absolute -top-2 -right-2">
                    NEW
                  </div>
                )}
                <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-6 ${
                  service.isDemo ? 'bg-green-100' : 'bg-primary-100'
                }`}>
                  <service.icon className={`w-8 h-8 ${
                    service.isDemo ? 'text-green-600' : 'text-primary-600'
                  }`} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {service.title}
                </h3>
                <p className="text-gray-600 mb-4">
                  {service.description}
                </p>
                <ul className="space-y-2 mb-6">
                  {service.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center text-sm text-gray-600">
                      <div className={`w-2 h-2 rounded-full mr-3 ${
                        service.isDemo ? 'bg-green-400' : 'bg-primary-400'
                      }`}></div>
                      {feature}
                    </li>
                  ))}
                </ul>
                <div className="border-t border-gray-100 pt-4">
                  <p className={`text-lg font-semibold mb-4 ${
                    service.isDemo ? 'text-green-600' : 'text-primary-600'
                  }`}>
                    {service.price}
                  </p>
                  {service.isDemo ? (
                    <Link 
                      to={service.link} 
                      className="bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 w-full text-center inline-block"
                    >
                      🎯 Try Demo Now
                    </Link>
                  ) : (
                    <Link 
                      to="/contact" 
                      className="btn-primary w-full text-center"
                    >
                      Get Started
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section-padding bg-gray-50">
        <div className="container-max">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How VEROCTA Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Simple steps to unlock actionable financial intelligence and optimize your business spending.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-xl font-bold">1</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Data</h3>
              <p className="text-gray-600">
                Connect CSV files from QuickBooks, Wave, Revolut, Xero, or Google Sheets.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-xl font-bold">2</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                Our SpendScore™ engine analyzes patterns and identifies waste opportunities.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-xl font-bold">3</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Get Insights</h3>
              <p className="text-gray-600">
                Receive actionable recommendations and clear explanations to cut waste.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-xl font-bold">4</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Take Action</h3>
              <p className="text-gray-600">
                Implement recommendations and track your savings with automated reports.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 section-padding">
        <div className="container-max text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Optimize Your Financial Health?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Start with our free demo dashboard or contact us to discuss how VEROCTA 
            can help you cut waste and unlock savings.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/dashboard" 
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-8 rounded-lg transition-colors duration-200 text-lg"
            >
              🎯 Try Free Demo
            </Link>
            <Link 
              to="/contact" 
              className="bg-white text-blue-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors duration-200 text-lg"
            >
              Schedule Consultation
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Services
