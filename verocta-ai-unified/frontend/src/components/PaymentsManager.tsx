import React, { useState } from 'react'
import { 
  CreditCardIcon, 
  CurrencyDollarIcon,
  GlobeAltIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

interface Subscription {
  id: number
  plan: string
  price: number
  currency: string
  status: 'active' | 'pending' | 'cancelled'
  nextBilling: string
  features: string[]
}

interface PaymentMethod {
  id: number
  type: 'card' | 'bank'
  last4: string
  brand?: string
  isDefault: boolean
}

const PaymentsManager: React.FC = () => {
  const [activeTab, setActiveTab] = useState('subscription')
  const [subscription] = useState<Subscription>({
    id: 1,
    plan: 'Professional (Demo - No Payment Required)',
    price: 99,
    currency: 'USD',
    status: 'active',
    nextBilling: '2025-10-08',
    features: [
      'Unlimited CSV uploads',
      'Advanced AI insights',
      'Custom reporting',
      'API access',
      'Priority support',
      'Multi-currency support'
    ]
  })

  const [paymentMethods] = useState<PaymentMethod[]>([
    { id: 1, type: 'card', last4: '4242', brand: 'Visa', isDefault: true },
    { id: 2, type: 'bank', last4: '1234', isDefault: false }
  ])

  const currencies = [
    { code: 'USD', name: 'US Dollar', supported: true },
    { code: 'GBP', name: 'British Pound', supported: true },
    { code: 'CAD', name: 'Canadian Dollar', supported: true },
    { code: 'AUD', name: 'Australian Dollar', supported: true },
    { code: 'NZD', name: 'New Zealand Dollar', supported: true },
    { code: 'EUR', name: 'Euro', supported: false, comingSoon: true }
  ]

  const invoices = [
    { id: 1, date: '2025-09-08', amount: 99, currency: 'USD', status: 'paid' },
    { id: 2, date: '2025-08-08', amount: 99, currency: 'USD', status: 'paid' },
    { id: 3, date: '2025-07-08', amount: 99, currency: 'USD', status: 'paid' }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'paid':
        return 'text-green-600 bg-green-100'
      case 'pending':
        return 'text-yellow-600 bg-yellow-100'
      case 'cancelled':
      case 'failed':
        return 'text-red-600 bg-red-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
      case 'paid':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'pending':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />
      case 'cancelled':
      case 'failed':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">Payments & Billing</h2>
        <p className="mt-2 text-gray-600">Manage your subscription and payment methods</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'subscription', name: 'Subscription', icon: CreditCardIcon },
            { id: 'methods', name: 'Payment Methods', icon: CreditCardIcon },
            { id: 'currency', name: 'Multi-Currency', icon: GlobeAltIcon },
            { id: 'invoices', name: 'Invoices', icon: CurrencyDollarIcon }
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

      {/* Subscription Tab */}
      {activeTab === 'subscription' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Current Plan</h3>
            <div className="border rounded-lg p-4 bg-indigo-50 border-indigo-200">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="font-medium text-indigo-900">{subscription.plan}</h4>
                  <p className="text-sm text-indigo-700">Perfect for growing businesses</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-indigo-900">
                    ${subscription.price}/{subscription.currency}
                  </div>
                  <div className="text-sm text-indigo-700">per month</div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(subscription.status)}`}>
                  {subscription.status}
                </span>
                <span className="text-sm text-indigo-700">
                  Next billing: {new Date(subscription.nextBilling).toLocaleDateString()}
                </span>
              </div>
            </div>

            <div className="mt-6">
              <h4 className="font-medium text-gray-900 mb-3">Features Included</h4>
              <ul className="space-y-2">
                {subscription.features.map((feature, index) => (
                  <li key={index} className="flex items-center text-sm text-gray-600">
                    <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-6 space-y-3">
              <button className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700">
                Manage Subscription
              </button>
              <button className="w-full border border-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-50">
                View All Plans
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Usage This Month</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">CSV Uploads</span>
                <span className="text-sm font-medium">12 / Unlimited</span>
              </div>
              <div className="bg-gray-200 rounded-full h-2">
                <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '20%' }}></div>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">API Calls</span>
                <span className="text-sm font-medium">1,245 / 10,000</span>
              </div>
              <div className="bg-gray-200 rounded-full h-2">
                <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '12%' }}></div>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Storage Used</span>
                <span className="text-sm font-medium">2.1 GB / 50 GB</span>
              </div>
              <div className="bg-gray-200 rounded-full h-2">
                <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '4%' }}></div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-green-700">
                You're well within your plan limits. Great job optimizing your usage!
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Payment Methods Tab */}
      {activeTab === 'methods' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium text-gray-900">Payment Methods</h3>
            <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
              Add Payment Method
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {paymentMethods.map((method) => (
              <div key={method.id} className={`border rounded-lg p-4 ${method.isDefault ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200'}`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <CreditCardIcon className="h-8 w-8 text-gray-400" />
                    <div className="ml-3">
                      <p className="font-medium text-gray-900">
                        {method.type === 'card' ? method.brand : 'Bank Account'} ••••{method.last4}
                      </p>
                      {method.isDefault && (
                        <span className="text-xs text-indigo-600 font-medium">Default</span>
                      )}
                    </div>
                  </div>
                  <button className="text-gray-400 hover:text-gray-600">
                    •••
                  </button>
                </div>
                {!method.isDefault && (
                  <button className="text-sm text-indigo-600 hover:text-indigo-800">
                    Set as default
                  </button>
                )}
              </div>
            ))}
          </div>

          <div className="bg-gray-50 rounded-lg p-6">
            <h4 className="font-medium text-gray-900 mb-2">Secure Payments</h4>
            <p className="text-sm text-gray-600">
              All payments are processed securely through Stripe. We never store your full payment details.
            </p>
          </div>
        </div>
      )}

      {/* Multi-Currency Tab */}
      {activeTab === 'currency' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Supported Currencies</h3>
            <p className="text-sm text-gray-600 mb-6">
              VEROCTA supports multiple currencies for billing and reporting. USD is our base currency with GBP payouts available.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {currencies.map((currency) => (
                <div 
                  key={currency.code} 
                  className={`border rounded-lg p-4 ${currency.supported ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-gray-50'}`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{currency.code}</p>
                      <p className="text-sm text-gray-600">{currency.name}</p>
                    </div>
                    {currency.supported ? (
                      <CheckCircleIcon className="h-5 w-5 text-green-500" />
                    ) : currency.comingSoon ? (
                      <ClockIcon className="h-5 w-5 text-yellow-500" />
                    ) : (
                      <div className="h-5 w-5"></div>
                    )}
                  </div>
                  {currency.comingSoon && (
                    <p className="text-xs text-yellow-600 mt-1">Coming Soon</p>
                  )}
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">Currency Features</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• USD base currency with real-time conversion</li>
                <li>• GBP payouts for UK customers</li>
                <li>• Multi-currency reporting and analytics</li>
                <li>• Automatic tax calculation by region</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Invoices Tab */}
      {activeTab === 'invoices' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium text-gray-900">Invoice History</h3>
            <button className="text-indigo-600 hover:text-indigo-800 text-sm">
              Download All
            </button>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {invoices.map((invoice) => (
                  <tr key={invoice.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(invoice.date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${invoice.amount} {invoice.currency}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getStatusIcon(invoice.status)}
                        <span className={`ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(invoice.status)}`}>
                          {invoice.status}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-indigo-600">
                      <button className="hover:text-indigo-800">Download PDF</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="bg-gray-50 rounded-lg p-6">
            <h4 className="font-medium text-gray-900 mb-2">Need help with billing?</h4>
            <p className="text-sm text-gray-600 mb-4">
              Contact our support team for any billing questions or issues with your invoices.
            </p>
            <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 text-sm">
              Contact Support
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default PaymentsManager