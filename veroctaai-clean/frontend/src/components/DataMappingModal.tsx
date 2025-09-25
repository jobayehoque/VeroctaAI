
import React, { useState, useEffect } from 'react'
import { XMarkIcon, CheckIcon, ExclamationTriangleIcon, SparklesIcon } from '@heroicons/react/24/outline'

interface DataMappingModalProps {
  isOpen: boolean
  onClose: () => void
  csvData: any[]
  onConfirm: (mapping: ColumnMapping) => void
  autoMapping?: ColumnMapping
}

interface ColumnMapping {
  date: string
  description: string
  amount: string
  category?: string
  vendor?: string
  [key: string]: string | undefined
}

const DataMappingModal: React.FC<DataMappingModalProps> = ({
  isOpen,
  onClose,
  csvData,
  onConfirm,
  autoMapping
}) => {
  const [mapping, setMapping] = useState<ColumnMapping>({
    date: '',
    description: '',
    amount: '',
    category: '',
    vendor: ''
  })
  const [availableColumns, setAvailableColumns] = useState<string[]>([])
  const [previewData, setPreviewData] = useState<any[]>([])
  const [errors, setErrors] = useState<string[]>([])
  const [isAutoDetected, setIsAutoDetected] = useState(false)

  useEffect(() => {
    if (csvData && csvData.length > 0) {
      const columns = Object.keys(csvData[0])
      setAvailableColumns(columns)
      setPreviewData(csvData.slice(0, 5))
      
      // Use auto-mapping if provided, otherwise detect
      if (autoMapping) {
        setMapping(autoMapping)
        setIsAutoDetected(true)
      } else {
        const autoDetected = autoDetectColumns(columns)
        setMapping(autoDetected)
        setIsAutoDetected(Object.values(autoDetected).some(Boolean))
      }
    }
  }, [csvData, autoMapping])

  const autoDetectColumns = (columns: string[]): ColumnMapping => {
    const mapping: ColumnMapping = {
      date: '',
      description: '',
      amount: '',
      category: '',
      vendor: ''
    }

    const lowerColumns = columns.map(col => col.toLowerCase())

    columns.forEach((col, index) => {
      const lowerCol = lowerColumns[index]
      
      // Date detection with enhanced patterns
      if (!mapping.date && (
        lowerCol.includes('date') || 
        lowerCol.includes('time') ||
        lowerCol === 'transaction date' ||
        lowerCol === 'txn date' ||
        lowerCol === 'posted' ||
        lowerCol === 'posting date' ||
        lowerCol === 'completed date'
      )) {
        mapping.date = col
      }
      
      // Amount detection with enhanced patterns
      if (!mapping.amount && (
        lowerCol.includes('amount') || 
        lowerCol.includes('total') ||
        lowerCol.includes('price') ||
        lowerCol.includes('cost') ||
        lowerCol.includes('value') ||
        lowerCol.includes('debit') ||
        lowerCol.includes('credit') ||
        lowerCol.includes('transaction value') ||
        lowerCol.includes('payment amount')
      )) {
        mapping.amount = col
      }
      
      // Description detection
      if (!mapping.description && (
        lowerCol.includes('description') || 
        lowerCol.includes('memo') ||
        lowerCol.includes('details') ||
        lowerCol.includes('reference') ||
        lowerCol.includes('notes') ||
        lowerCol.includes('comment')
      )) {
        mapping.description = col
      }
      
      // Category detection
      if (!mapping.category && (
        lowerCol.includes('category') || 
        lowerCol.includes('class') ||
        lowerCol.includes('type') ||
        lowerCol.includes('account') ||
        lowerCol.includes('classification')
      )) {
        mapping.category = col
      }
      
      // Vendor detection with enhanced patterns
      if (!mapping.vendor && (
        lowerCol.includes('vendor') || 
        lowerCol.includes('payee') ||
        lowerCol.includes('merchant') ||
        lowerCol.includes('supplier') ||
        lowerCol.includes('name') ||
        lowerCol.includes('counterparty') ||
        lowerCol.includes('recipient') ||
        lowerCol.includes('business name') ||
        lowerCol.includes('company')
      )) {
        mapping.vendor = col
      }
    })

    return mapping
  }

  const validateMapping = (): string[] => {
    const errors: string[] = []
    
    if (!mapping.amount) {
      errors.push('Amount column is required')
    }
    
    // Check for duplicate mappings
    const mappedColumns = Object.values(mapping).filter(Boolean)
    const uniqueColumns = new Set(mappedColumns)
    if (mappedColumns.length !== uniqueColumns.size) {
      errors.push('Each column can only be mapped once')
    }
    
    return errors
  }

  const handleMappingChange = (field: keyof ColumnMapping, value: string) => {
    setMapping(prev => ({
      ...prev,
      [field]: value
    }))
    setIsAutoDetected(false)
  }

  const handleConfirm = () => {
    const validationErrors = validateMapping()
    setErrors(validationErrors)
    
    if (validationErrors.length === 0) {
      onConfirm(mapping)
    }
  }

  const resetAutoDetection = () => {
    const autoDetected = autoDetectColumns(availableColumns)
    setMapping(autoDetected)
    setIsAutoDetected(true)
    setErrors([])
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center">
            <h3 className="text-lg font-medium text-gray-900">Configure Column Mapping</h3>
            {isAutoDetected && (
              <span className="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <SparklesIcon className="w-3 h-3 mr-1" />
                Auto-detected
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          {/* Auto-detection banner */}
          {isAutoDetected && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center">
                <SparklesIcon className="h-5 w-5 text-green-600 mr-2" />
                <div>
                  <h4 className="font-medium text-green-900">Smart Detection Active</h4>
                  <p className="text-sm text-green-700">
                    We've automatically detected your column mappings. Review and adjust if needed.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Error display */}
          {errors.length > 0 && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center mb-2">
                <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2" />
                <h4 className="font-medium text-red-900">Validation Errors</h4>
              </div>
              <ul className="text-sm text-red-700">
                {errors.map((error, index) => (
                  <li key={index}>• {error}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Mapping Configuration */}
            <div>
              <h4 className="font-medium text-gray-900 mb-4">Column Mapping</h4>
              <div className="space-y-4">
                {[
                  { key: 'amount', label: 'Amount', required: true, description: 'Transaction amount (required)' },
                  { key: 'date', label: 'Date', required: false, description: 'Transaction date' },
                  { key: 'vendor', label: 'Vendor/Merchant', required: false, description: 'Vendor or merchant name' },
                  { key: 'description', label: 'Description', required: false, description: 'Transaction description' },
                  { key: 'category', label: 'Category', required: false, description: 'Transaction category' }
                ].map(({ key, label, required, description }) => (
                  <div key={key}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {label}
                      {required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    <select
                      value={mapping[key as keyof ColumnMapping] || ''}
                      onChange={(e) => handleMappingChange(key as keyof ColumnMapping, e.target.value)}
                      className={`w-full border rounded-md px-3 py-2 ${
                        required && !mapping[key as keyof ColumnMapping] 
                          ? 'border-red-300 focus:border-red-500' 
                          : 'border-gray-300 focus:border-indigo-500'
                      } focus:outline-none focus:ring-1 focus:ring-indigo-500`}
                    >
                      <option value="">Select column...</option>
                      {availableColumns.map(column => (
                        <option key={column} value={column}>
                          {column}
                        </option>
                      ))}
                    </select>
                    <p className="text-xs text-gray-500 mt-1">{description}</p>
                  </div>
                ))}
              </div>

              <button
                onClick={resetAutoDetection}
                className="mt-4 text-sm text-indigo-600 hover:text-indigo-800 flex items-center"
              >
                <SparklesIcon className="w-4 h-4 mr-1" />
                Re-run Auto Detection
              </button>
            </div>

            {/* Data Preview */}
            <div>
              <h4 className="font-medium text-gray-900 mb-4">Data Preview</h4>
              {previewData.length > 0 ? (
                <div className="overflow-x-auto border rounded-lg">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        {availableColumns.slice(0, 4).map(column => (
                          <th key={column} className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            {column}
                            {Object.values(mapping).includes(column) && (
                              <span className="ml-1 text-green-600">✓</span>
                            )}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {previewData.slice(1).map((row, index) => (
                        <tr key={index}>
                          {availableColumns.slice(0, 4).map(column => (
                            <td key={column} className="px-3 py-2 text-sm text-gray-900 truncate max-w-32">
                              {row[column]}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No preview data available
                </div>
              )}

              {/* Mapping Summary */}
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <h5 className="font-medium text-gray-900 mb-2">Current Mapping Summary</h5>
                <div className="space-y-1 text-sm">
                  {Object.entries(mapping).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-gray-600 capitalize">{key}:</span>
                      <span className={value ? 'text-gray-900 font-medium' : 'text-gray-400'}>
                        {value || 'Not mapped'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between p-6 border-t bg-gray-50">
          <div className="flex items-center text-sm text-gray-600">
            <ExclamationTriangleIcon className="h-4 w-4 mr-1" />
            Amount column is required for processing
          </div>
          <div className="flex space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              onClick={handleConfirm}
              disabled={!mapping.amount}
              className={`px-4 py-2 rounded-md font-medium ${
                mapping.amount
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              <CheckIcon className="h-4 w-4 inline mr-1" />
              Confirm Mapping
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DataMappingModal
