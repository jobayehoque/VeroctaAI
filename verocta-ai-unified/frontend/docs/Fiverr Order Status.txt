import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, X, FileText, CheckCircle, AlertCircle, Download, Shield, Zap, BarChart } from 'lucide-react';

const FileUploadPopup = ({ isOpen, onClose }) => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (fileList) => {
    const validFiles = Array.from(fileList).filter(file => 
      file.type === 'text/csv' || 
      file.name.toLowerCase().endsWith('.csv') ||
      file.type === 'application/vnd.ms-excel' ||
      file.name.toLowerCase().endsWith('.xlsx')
    );
    
    if (validFiles.length > 0) {
      setFiles(validFiles);
    }
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    
    setUploading(true);
    
    // Simulate upload process
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setUploading(false);
    setUploadComplete(true);
    
    // Auto close after success
    setTimeout(() => {
      onClose();
      resetState();
    }, 2000);
  };

  const resetState = () => {
    setFiles([]);
    setUploading(false);
    setUploadComplete(false);
    setDragActive(false);
  };

  const handleClose = () => {
    onClose();
    resetState();
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0  backdrop-blur-sm z-50 flex items-center justify-center p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
          >
            {/* Modal */}
            <motion.div
              className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden"
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                      <Upload className="h-5 w-5 text-black" />
                    </div>
                    <div>
                      <h2 className="text-xl font-bold">Upload Your Financial Data</h2>
                      <p className="text-blue-100 text-sm">Secure, encrypted upload</p>
                    </div>
                  </div>
                  <button
                    onClick={handleClose}
                    className="w-8 h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center hover:bg-opacity-30 transition-colors"
                  >
                    <X className="h-4 w-4 text-black" />
                  </button>
                </div>
              </div>

              {/* Content */}
              <div className="p-6">
                {!uploadComplete ? (
                  <>
                    {/* Security badges */}
                    <div className="grid grid-cols-3 gap-4 mb-6">
                      {[
                        { icon: Shield, title: "Bank-grade Security", desc: "256-bit encryption" },
                        { icon: Zap, title: "Fast Processing", desc: "Results in 2 minutes" },
                        { icon: BarChart, title: "AI Analysis", desc: "94% accuracy rate" }
                      ].map((feature, index) => (
                        <div key={index} className="text-center">
                          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mx-auto mb-2">
                            <feature.icon className="h-6 w-6 text-blue-600" />
                          </div>
                          <h4 className="font-semibold text-sm text-slate-800">{feature.title}</h4>
                          <p className="text-xs text-slate-500">{feature.desc}</p>
                        </div>
                      ))}
                    </div>

                    {/* File upload area */}
                    <div
                      className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
                        dragActive
                          ? 'border-blue-500 bg-blue-50'
                          : files.length > 0
                          ? 'border-green-500 bg-green-50'
                          : 'border-slate-300 bg-slate-50 hover:border-blue-400 hover:bg-blue-25'
                      }`}
                      onDragEnter={handleDrag}
                      onDragLeave={handleDrag}
                      onDragOver={handleDrag}
                      onDrop={handleDrop}
                    >
                      <input
                        ref={fileInputRef}
                        type="file"
                        className="hidden"
                        multiple
                        accept=".csv,.xlsx,.xls"
                        onChange={handleChange}
                      />

                      {files.length === 0 ? (
                        <>
                          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <Upload className="h-8 w-8 text-blue-600" />
                          </div>
                          <h3 className="text-lg font-semibold text-slate-800 mb-2">
                            Drop your files here, or <button onClick={onButtonClick} className="text-blue-600 hover:underline">browse</button>
                          </h3>
                          <p className="text-sm text-slate-500 mb-4">
                            Supports CSV, Excel files up to 50MB
                          </p>
                          <div className="flex flex-wrap justify-center gap-2 text-xs text-slate-400">
                            <span className="bg-slate-200 px-2 py-1 rounded">.csv</span>
                            <span className="bg-slate-200 px-2 py-1 rounded">.xlsx</span>
                            <span className="bg-slate-200 px-2 py-1 rounded">.xls</span>
                          </div>
                        </>
                      ) : (
                        <div className="space-y-3">
                          {files.map((file, index) => (
                            <div key={index} className="flex items-center justify-between bg-white p-3 rounded-lg border">
                              <div className="flex items-center space-x-3">
                                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                                  <FileText className="h-5 w-5 text-green-600" />
                                </div>
                                <div>
                                  <p className="font-medium text-slate-800 text-sm">{file.name}</p>
                                  <p className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                </div>
                              </div>
                              <button
                                onClick={() => removeFile(index)}
                                className="w-6 h-6 bg-red-100 text-red-600 rounded-full flex items-center justify-center hover:bg-red-200 transition-colors"
                              >
                                <X className="h-3 w-3" />
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Sample file download */}
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Download className="h-5 w-5 text-blue-600" />
                          <div>
                            <p className="font-medium text-blue-900 text-sm">Need a sample file?</p>
                            <p className="text-blue-700 text-xs">Download our CSV template to get started</p>
                          </div>
                        </div>
                        <button className="text-blue-600 hover:text-blue-700 font-medium text-sm hover:underline">
                          Download Template
                        </button>
                      </div>
                    </div>

                    {/* Action buttons */}
                    <div className="flex gap-3 mt-6">
                      <button
                        onClick={handleClose}
                        className="flex-1 py-3 px-4 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors font-medium"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleUpload}
                        disabled={files.length === 0 || uploading}
                        className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                          files.length === 0 || uploading
                            ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg hover:shadow-xl'
                        }`}
                      >
                        {uploading ? (
                          <div className="flex items-center justify-center space-x-2">
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            <span>Analyzing...</span>
                          </div>
                        ) : (
                          `Analyze ${files.length} file${files.length !== 1 ? 's' : ''}`
                        )}
                      </button>
                    </div>
                  </>
                ) : (
                  /* Success state */
                  <div className="text-center py-8">
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4"
                    >
                      <CheckCircle className="h-10 w-10 text-green-600" />
                    </motion.div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">Upload Successful!</h3>
                    <p className="text-slate-600 mb-4">
                      Your financial data is being processed. You'll receive your SpendScore report shortly.
                    </p>
                    <div className="flex items-center justify-center space-x-2 text-sm text-slate-500">
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                      <span>Processing your data securely...</span>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default FileUploadPopup;