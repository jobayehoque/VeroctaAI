
import React, { useState, useCallback } from 'react'
import { apiClient, endpoints } from '../utils/api'
import DataMappingModal from './DataMappingModal'
import { 
  CloudArrowUpIcon, 
  DocumentChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  CogIcon,
  ExclamationTriangleIcon,
  DocumentIcon
} from '@heroicons/react/24/outline'

interface UploadedFile {
  file: File
  progress: number
  status: 'uploading' | 'processing' | 'completed' | 'error' | 'mapping' | 'auto-mapping'
  result?: any
  error?: string
  csvData?: any[]
  mapping?: any
  autoMapping?: any
  uploadId?: string
}

const UploadManager: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const [mappingModalOpen, setMappingModalOpen] = useState(false)
  const [currentMappingFile, setCurrentMappingFile] = useState<UploadedFile | null>(null)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      handleFiles(files)
    }
  }

  const autoDetectMapping = (headers: string[]) => {
    const mapping: any = {
      date: '',
      description: '',
      amount: '',
      category: '',
      vendor: ''
    }

    const lowerHeaders = headers.map(h => h.toLowerCase())

    // Auto-detect date column
    for (let i = 0; i < headers.length; i++) {
      const lower = lowerHeaders[i]
      if (!mapping.date && (
        lower.includes('date') || 
        lower.includes('time') ||
        lower === 'transaction date' ||
        lower === 'txn date' ||
        lower === 'posted'
      )) {
        mapping.date = headers[i]
      }
    }

    // Auto-detect amount column
    for (let i = 0; i < headers.length; i++) {
      const lower = lowerHeaders[i]
      if (!mapping.amount && (
        lower.includes('amount') || 
        lower.includes('total') ||
        lower.includes('price') ||
        lower.includes('cost') ||
        lower.includes('value') ||
        lower.includes('debit') ||
        lower.includes('credit')
      )) {
        mapping.amount = headers[i]
      }
    }

    // Auto-detect vendor/merchant column
    for (let i = 0; i < headers.length; i++) {
      const lower = lowerHeaders[i]
      if (!mapping.vendor && (
        lower.includes('vendor') || 
        lower.includes('payee') ||
        lower.includes('merchant') ||
        lower.includes('supplier') ||
        lower.includes('name') ||
        lower.includes('counterparty') ||
        lower.includes('recipient')
      )) {
        mapping.vendor = headers[i]
      }
    }

    // Auto-detect description column
    for (let i = 0; i < headers.length; i++) {
      const lower = lowerHeaders[i]
      if (!mapping.description && (
        lower.includes('description') || 
        lower.includes('memo') ||
        lower.includes('details') ||
        lower.includes('reference') ||
        lower.includes('notes')
      )) {
        mapping.description = headers[i]
      }
    }

    // Auto-detect category column
    for (let i = 0; i < headers.length; i++) {
      const lower = lowerHeaders[i]
      if (!mapping.category && (
        lower.includes('category') || 
        lower.includes('class') ||
        lower.includes('type') ||
        lower.includes('account')
      )) {
        mapping.category = headers[i]
      }
    }

    return mapping
  }

  const readCsvForAutoMapping = async (file: File, uploadFile: UploadedFile) => {
    try {
      const text = await file.text()
      const lines = text.split('\n').filter(line => line.trim())
      
      if (lines.length < 2) {
        throw new Error('CSV file must have at least 2 lines (header + data)')
      }

      const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''))
      
      // Parse sample data for preview
      const csvData = []
      for (let i = 0; i < Math.min(6, lines.length); i++) {
        const row: any = {}
        const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''))
        headers.forEach((header, index) => {
          row[header] = values[index] || ''
        })
        csvData.push(row)
      }

      // Auto-detect column mapping
      const autoMapping = autoDetectMapping(headers)
      
      // Update file status with detected mapping
      setUploadedFiles(prev => prev.map(uf => 
        uf.file === file ? { 
          ...uf, 
          status: 'auto-mapping',
          csvData: csvData,
          autoMapping: autoMapping,
          progress: 50
        } : uf
      ))

      // Check if we have the essential columns (amount is required)
      if (!autoMapping.amount) {
        setUploadedFiles(prev => prev.map(uf => 
          uf.file === file ? { 
            ...uf, 
            status: 'mapping',
            error: 'Could not auto-detect amount column. Manual mapping required.'
          } : uf
        ))
        return
      }

      // Automatically proceed with processing after a brief delay
      setTimeout(() => {
        processFileWithMapping(file, autoMapping)
      }, 1500)
      
    } catch (error) {
      console.error('CSV parsing error:', error)
      setUploadedFiles(prev => prev.map(uf => 
        uf.file === file ? { 
          ...uf, 
          status: 'error',
          error: error instanceof Error ? error.message : 'Failed to read CSV file'
        } : uf
      ))
    }
  }

  const processFileWithMapping = async (file: File, mapping: any) => {
    try {
      setUploadedFiles(prev => prev.map(uf => 
        uf.file === file ? { ...uf, status: 'processing', progress: 70 } : uf
      ))

      const formData = new FormData()
      formData.append('file', file)
      formData.append('mapping', JSON.stringify(mapping))
      formData.append('company_name', 'FinDash Demo Company')

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorData = {}
        try {
          errorData = JSON.parse(errorText)
        } catch (e) {
          errorData = { error: errorText || `Upload failed: ${response.statusText}` }
        }
        throw new Error(errorData.error || `Upload failed: ${response.statusText}`)
      }

      const result = await response.json()
      
      // Process the API response
      const processedResult = {
        transactions_processed: result.transaction_summary?.total_transactions || 0,
        spend_score: result.spend_score || 0,
        insights: {
          waste_detected: Math.round(((result.score_breakdown?.waste_ratio || 0) * 100)),
          duplicates_found: result.score_breakdown?.redundancy_count || 0,
          top_categories: result.transaction_summary?.category_breakdown ? 
            Object.keys(result.transaction_summary.category_breakdown).slice(0, 3) : [],
          recommendations: result.ai_insights?.recommendations || [
            'Upload processed successfully',
            'View detailed insights in the Insights section'
          ]
        },
        raw_result: result
      }

      setUploadedFiles(prev => prev.map(uf => 
        uf.file === file ? { 
          ...uf, 
          progress: 100,
          status: 'completed',
          result: processedResult,
          mapping: mapping
        } : uf
      ))

    } catch (error) {
      console.error('Upload error:', error)
      setUploadedFiles(prev => prev.map(uf => 
        uf.file === file ? { 
          ...uf, 
          status: 'error',
          error: error instanceof Error ? error.message : 'Upload failed. Please try again.'
        } : uf
      ))
    }
  }

  const handleFiles = (files: File[]) => {
    const csvFiles = files.filter(file => 
      file.name.endsWith('.csv') || file.type === 'text/csv' || file.type === 'application/vnd.ms-excel'
    )
    
    if (csvFiles.length === 0) {
      alert('Please select CSV files only. Supported formats: .csv')
      return
    }

    csvFiles.forEach(file => {
      const uploadFile: UploadedFile = {
        file,
        progress: 0,
        status: 'uploading',
        uploadId: `upload_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      }
      
      setUploadedFiles(prev => [...prev, uploadFile])
      
      // Start with auto-mapping
      setUploadedFiles(prev => prev.map(uf => 
        uf.file === file ? { ...uf, progress: 20, status: 'uploading' } : uf
      ))
      
      readCsvForAutoMapping(file, uploadFile)
    })
  }

  const removeFile = (file: File) => {
    setUploadedFiles(prev => prev.filter(uf => uf.file !== file))
  }

  const openMappingModal = (uploadFile: UploadedFile) => {
    setCurrentMappingFile(uploadFile)
    setMappingModalOpen(true)
  }

  const handleMappingConfirm = (mapping: any) => {
    if (currentMappingFile) {
      processFileWithMapping(currentMappingFile.file, mapping)
    }
    setCurrentMappingFile(null)
    setMappingModalOpen(false)
  }

  const retryUpload = (uploadFile: UploadedFile) => {
    setUploadedFiles(prev => prev.map(uf => 
      uf.file === uploadFile.file ? { 
        ...uf, 
        status: 'uploading',
        progress: 0,
        error: undefined
      } : uf
    ))
    readCsvForAutoMapping(uploadFile.file, uploadFile)
  }

  const createReportFromFile = async (uploadFile: UploadedFile) => {
    try {
      const response = await apiClient.post('/reports', {
        title: `Financial Analysis: ${uploadFile.file.name}`,
        data: {
          filename: uploadFile.file.name,
          transactions: uploadFile.result.transactions_processed,
          spend_score: uploadFile.result.spend_score,
          waste_percentage: uploadFile.result.insights.waste_detected,
          duplicates_found: uploadFile.result.insights.duplicates_found,
          top_categories: uploadFile.result.insights.top_categories,
          recommendations: uploadFile.result.insights.recommendations,
          upload_timestamp: new Date().toISOString(),
          raw_analysis: uploadFile.result.raw_result,
          mapping_used: uploadFile.mapping
        }
      })
      alert('Report created successfully! View it in the Reports tab.')
    } catch (error) {
      console.error('Report creation error:', error)
      alert('Failed to create report. Please try again.')
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
      case 'processing':
        return <ArrowPathIcon className="h-5 w-5 text-blue-500 animate-spin" />
      case 'auto-mapping':
        return <ArrowPathIcon className="h-5 w-5 text-green-500 animate-spin" />
      case 'mapping':
        return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'error':
        return <XCircleIcon className="h-5 w-5 text-red-500" />
      default:
        return null
    }
  }

  const getStatusMessage = (uploadFile: UploadedFile) => {
    switch (uploadFile.status) {
      case 'uploading':
        return 'Reading file...'
      case 'auto-mapping':
        return 'Auto-detecting columns...'
      case 'processing':
        return 'Processing data with AI...'
      case 'mapping':
        return 'Manual column mapping required'
      case 'completed':
        return 'Analysis complete!'
      case 'error':
        return uploadFile.error || 'An error occurred'
      default:
        return 'Unknown status'
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">Smart CSV Upload</h2>
        <p className="mt-2 text-gray-600">
          Upload your financial data for AI-powered analysis with automatic column detection
        </p>
      </div>

      {/* Enhanced Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${
          isDragging 
            ? 'border-indigo-500 bg-indigo-50 scale-105' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
        <div className="mt-4">
          <h3 className="text-lg font-medium text-gray-900">Smart CSV Upload</h3>
          <p className="mt-1 text-sm text-gray-600">
            Drag and drop your CSV files here, or click to browse
          </p>
          <p className="mt-1 text-xs text-gray-500">
            ✨ Automatic column detection • ⚡ Instant processing • 🔒 Secure upload
          </p>
        </div>
        <div className="mt-6">
          <label className="cursor-pointer">
            <span className="bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition-colors inline-flex items-center">
              <DocumentIcon className="h-5 w-5 mr-2" />
              Choose Files
            </span>
            <input
              type="file"
              multiple
              accept=".csv,text/csv,application/vnd.ms-excel"
              className="hidden"
              onChange={handleFileSelect}
            />
          </label>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-4 text-xs text-gray-500">
          <div>
            <strong>Supported Formats:</strong>
            <br />QuickBooks, Wave, Revolut, Xero
          </div>
          <div>
            <strong>Auto-Detection:</strong>
            <br />Date, Amount, Vendor, Category
          </div>
        </div>
      </div>

      {/* Google Sheets Integration */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-center">
          <DocumentChartBarIcon className="h-8 w-8 text-green-600" />
          <div className="ml-3">
            <h3 className="text-lg font-medium text-green-900">Google Sheets Integration</h3>
            <p className="text-sm text-green-700">Connect your Google Sheets for real-time data sync</p>
          </div>
        </div>
        <div className="mt-4">
          <button className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors">
            Connect Google Sheets (Coming Soon)
          </button>
        </div>
      </div>

      {/* Enhanced File Processing List */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900">Processing Files</h3>
          {uploadedFiles.map((uploadFile, index) => (
            <div key={index} className="bg-white border rounded-lg p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  {getStatusIcon(uploadFile.status)}
                  <div className="ml-3">
                    <p className="font-medium text-gray-900">{uploadFile.file.name}</p>
                    <p className="text-sm text-gray-500">
                      {getStatusMessage(uploadFile)}
                    </p>
                    {uploadFile.status === 'auto-mapping' && uploadFile.autoMapping && (
                      <p className="text-xs text-green-600 mt-1">
                        ✓ Auto-detected: {Object.values(uploadFile.autoMapping).filter(Boolean).length} columns
                      </p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => removeFile(uploadFile.file)}
                  className="text-gray-400 hover:text-gray-600 text-xl"
                >
                  ×
                </button>
              </div>

              {/* Enhanced Progress Bar */}
              {(uploadFile.status === 'uploading' || uploadFile.status === 'processing' || uploadFile.status === 'auto-mapping') && (
                <div className="mt-4">
                  <div className="bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-500 ${
                        uploadFile.status === 'auto-mapping' ? 'bg-green-600' : 
                        uploadFile.status === 'processing' ? 'bg-blue-600' : 'bg-indigo-600'
                      }`}
                      style={{ width: `${uploadFile.progress}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>{uploadFile.progress}% complete</span>
                    <span>
                      {uploadFile.status === 'auto-mapping' ? 'Auto-detecting...' :
                       uploadFile.status === 'processing' ? 'AI Processing...' : 'Uploading...'}
                    </span>
                  </div>
                </div>
              )}

              {/* Manual Mapping Option */}
              {uploadFile.status === 'mapping' && (
                <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                    <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500 mr-2" />
                    Manual Column Mapping Required
                  </h4>
                  <p className="text-sm text-gray-600 mb-3">
                    Automatic detection couldn't find the amount column. Please configure mapping manually.
                  </p>
                  <button
                    onClick={() => openMappingModal(uploadFile)}
                    className="bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700 text-sm inline-flex items-center"
                  >
                    <CogIcon className="h-4 w-4 mr-2" />
                    Configure Mapping
                  </button>
                </div>
              )}

              {/* Error State */}
              {uploadFile.status === 'error' && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded">
                  <h4 className="font-medium text-red-900 mb-2 flex items-center">
                    <XCircleIcon className="h-5 w-5 text-red-500 mr-2" />
                    Upload Failed
                  </h4>
                  <p className="text-sm text-red-600 mb-3">{uploadFile.error}</p>
                  <div className="flex space-x-3">
                    <button
                      onClick={() => retryUpload(uploadFile)}
                      className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm"
                    >
                      Retry Upload
                    </button>
                    <button
                      onClick={() => openMappingModal(uploadFile)}
                      className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 text-sm"
                    >
                      Manual Mapping
                    </button>
                  </div>
                </div>
              )}

              {/* Enhanced Results Display */}
              {uploadFile.status === 'completed' && uploadFile.result && (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
                  <h4 className="font-medium text-gray-900 mb-3 flex items-center">
                    <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                    Analysis Complete
                  </h4>
                  <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                    <div className="space-y-2">
                      <div>
                        <span className="text-gray-500">Transactions:</span>
                        <span className="ml-2 font-medium">{uploadFile.result.transactions_processed}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">SpendScore:</span>
                        <span className="ml-2 font-medium text-green-600">{uploadFile.result.spend_score}</span>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div>
                        <span className="text-gray-500">Waste Detected:</span>
                        <span className="ml-2 font-medium text-red-600">{uploadFile.result.insights.waste_detected}%</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Duplicates:</span>
                        <span className="ml-2 font-medium">{uploadFile.result.insights.duplicates_found}</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Mapping Summary */}
                  {uploadFile.mapping && (
                    <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded text-xs">
                      <strong>Column Mapping Used:</strong>
                      <div className="mt-1 flex flex-wrap gap-2">
                        {Object.entries(uploadFile.mapping).map(([key, value]) => 
                          value && (
                            <span key={key} className="bg-blue-100 px-2 py-1 rounded">
                              {key}: {value as string}
                            </span>
                          )
                        )}
                      </div>
                    </div>
                  )}

                  <div className="flex space-x-3">
                    <button
                      onClick={() => createReportFromFile(uploadFile)}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 text-sm"
                    >
                      Create Full Report
                    </button>
                    <button
                      onClick={() => openMappingModal(uploadFile)}
                      className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 text-sm inline-flex items-center"
                    >
                      <CogIcon className="h-4 w-4 mr-2" />
                      Reconfigure Mapping
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Enhanced Data Mapping Modal */}
      <DataMappingModal
        isOpen={mappingModalOpen}
        onClose={() => {
          setMappingModalOpen(false)
          setCurrentMappingFile(null)
        }}
        csvData={currentMappingFile?.csvData || []}
        onConfirm={handleMappingConfirm}
        autoMapping={currentMappingFile?.autoMapping}
      />
    </div>
  )
}

export default UploadManager
