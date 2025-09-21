# 🎨 VeroctaAI Frontend Integration Guide

This guide helps you integrate the VeroctaAI API with any frontend framework or application.

## 🚀 Quick Start

### 1. Get API Access
```bash
# Register for API access
curl -X POST https://veroctaai.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password",
    "company": "Your Company"
  }'
```

### 2. Set Environment Variables
```bash
# Frontend environment variables
VITE_API_URL=https://veroctaai.onrender.com/api
VITE_APP_NAME=VeroctaAI
VITE_APP_VERSION=2.0.0
```

### 3. Install HTTP Client
```bash
# For React/Vue/Angular
npm install axios

# For vanilla JavaScript
# Use fetch API (built-in)
```

## 📱 Framework-Specific Integration

### React Integration

#### 1. Create API Service
```javascript
// src/services/veroctaAPI.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://veroctaai.onrender.com/api';

class VeroctaAPI {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for auth
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('verocta_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('verocta_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(email, password) {
    const response = await this.client.post('/auth/login', { email, password });
    localStorage.setItem('verocta_token', response.data.token);
    return response.data;
  }

  async register(email, password, company) {
    const response = await this.client.post('/auth/register', { email, password, company });
    localStorage.setItem('verocta_token', response.data.token);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // File Upload and Analysis
  async uploadFile(file, mapping = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (mapping) {
      formData.append('mapping', JSON.stringify(mapping));
    }

    const response = await this.client.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getSpendScore() {
    const response = await this.client.get('/spend-score');
    return response.data;
  }

  // Reports
  async getReports() {
    const response = await this.client.get('/reports');
    return response.data;
  }

  async downloadReport(reportId) {
    const response = await this.client.get(`/reports/${reportId}/pdf`, {
      responseType: 'blob',
    });
    return response.data;
  }

  // System
  async getHealth() {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export default new VeroctaAPI();
```

#### 2. Create React Components
```jsx
// src/components/FileUpload.jsx
import React, { useState } from 'react';
import VeroctaAPI from '../services/veroctaAPI';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    try {
      const result = await VeroctaAPI.uploadFile(file);
      setAnalysis(result.analysis);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <h2>Upload Financial Data</h2>
      
      <div className="upload-section">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="file-input"
        />
        
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="upload-button"
        >
          {uploading ? 'Analyzing...' : 'Upload & Analyze'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {analysis && (
        <div className="analysis-results">
          <h3>Analysis Results</h3>
          <div className="spend-score">
            <h4>SpendScore: {analysis.spend_score}/100</h4>
            <div className={`score-tier ${analysis.score_tier.color.toLowerCase()}`}>
              {analysis.score_tier.tier}
            </div>
          </div>
          
          <div className="insights">
            <h4>AI Insights</h4>
            <ul>
              {analysis.insights.map((insight, index) => (
                <li key={index} className={`priority-${insight.priority.toLowerCase()}`}>
                  <strong>{insight.priority}:</strong> {insight.text}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
```

#### 3. Create Authentication Context
```jsx
// src/contexts/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import VeroctaAPI from '../services/veroctaAPI';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('verocta_token');
      if (token) {
        try {
          const userData = await VeroctaAPI.getCurrentUser();
          setUser(userData.user);
        } catch (error) {
          localStorage.removeItem('verocta_token');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    const response = await VeroctaAPI.login(email, password);
    setUser(response.user);
    return response;
  };

  const register = async (email, password, company) => {
    const response = await VeroctaAPI.register(email, password, company);
    setUser(response.user);
    return response;
  };

  const logout = () => {
    localStorage.removeItem('verocta_token');
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

### Vue.js Integration

#### 1. Create API Service
```javascript
// src/services/veroctaAPI.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://veroctaai.onrender.com/api';

export const veroctaAPI = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
veroctaAPI.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('verocta_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
veroctaAPI.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('verocta_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => veroctaAPI.post('/auth/login', { email, password }),
  register: (email, password, company) => veroctaAPI.post('/auth/register', { email, password, company }),
  getCurrentUser: () => veroctaAPI.get('/auth/me'),
};

export const analysisAPI = {
  uploadFile: (file, mapping = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (mapping) {
      formData.append('mapping', JSON.stringify(mapping));
    }
    return veroctaAPI.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getSpendScore: () => veroctaAPI.get('/spend-score'),
};

export const reportsAPI = {
  getReports: () => veroctaAPI.get('/reports'),
  downloadReport: (reportId) => veroctaAPI.get(`/reports/${reportId}/pdf`, { responseType: 'blob' }),
};
```

#### 2. Create Vue Components
```vue
<!-- src/components/FileUpload.vue -->
<template>
  <div class="file-upload">
    <h2>Upload Financial Data</h2>
    
    <div class="upload-section">
      <input
        type="file"
        accept=".csv"
        @change="handleFileChange"
        class="file-input"
      />
      
      <button
        @click="handleUpload"
        :disabled="!file || uploading"
        class="upload-button"
      >
        {{ uploading ? 'Analyzing...' : 'Upload & Analyze' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="analysis" class="analysis-results">
      <h3>Analysis Results</h3>
      <div class="spend-score">
        <h4>SpendScore: {{ analysis.spend_score }}/100</h4>
        <div :class="`score-tier ${analysis.score_tier.color.toLowerCase()}`">
          {{ analysis.score_tier.tier }}
        </div>
      </div>
      
      <div class="insights">
        <h4>AI Insights</h4>
        <ul>
          <li
            v-for="(insight, index) in analysis.insights"
            :key="index"
            :class="`priority-${insight.priority.toLowerCase()}`"
          >
            <strong>{{ insight.priority }}:</strong> {{ insight.text }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { analysisAPI } from '../services/veroctaAPI';

export default {
  name: 'FileUpload',
  setup() {
    const file = ref(null);
    const uploading = ref(false);
    const analysis = ref(null);
    const error = ref(null);

    const handleFileChange = (e) => {
      file.value = e.target.files[0];
      error.value = null;
    };

    const handleUpload = async () => {
      if (!file.value) {
        error.value = 'Please select a file';
        return;
      }

      uploading.value = true;
      try {
        const response = await analysisAPI.uploadFile(file.value);
        analysis.value = response.data.analysis;
      } catch (err) {
        error.value = err.response?.data?.error || 'Upload failed';
      } finally {
        uploading.value = false;
      }
    };

    return {
      file,
      uploading,
      analysis,
      error,
      handleFileChange,
      handleUpload,
    };
  },
};
</script>
```

### Angular Integration

#### 1. Create API Service
```typescript
// src/app/services/verocta-api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class VeroctaApiService {
  private readonly baseUrl = environment.apiUrl || 'https://veroctaai.onrender.com/api';
  private tokenSubject = new BehaviorSubject<string | null>(localStorage.getItem('verocta_token'));
  
  constructor(private http: HttpClient) {}

  private get headers(): HttpHeaders {
    const token = this.tokenSubject.value;
    return new HttpHeaders({
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    });
  }

  // Authentication
  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/login`, { email, password })
      .pipe(tap((response: any) => {
        localStorage.setItem('verocta_token', response.token);
        this.tokenSubject.next(response.token);
      }));
  }

  register(email: string, password: string, company: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/register`, { email, password, company })
      .pipe(tap((response: any) => {
        localStorage.setItem('verocta_token', response.token);
        this.tokenSubject.next(response.token);
      }));
  }

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.baseUrl}/auth/me`, { headers: this.headers });
  }

  // File Upload
  uploadFile(file: File, mapping?: any): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (mapping) {
      formData.append('mapping', JSON.stringify(mapping));
    }

    return this.http.post(`${this.baseUrl}/upload`, formData, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.tokenSubject.value}`
      })
    });
  }

  // Analysis
  getSpendScore(): Observable<any> {
    return this.http.get(`${this.baseUrl}/spend-score`, { headers: this.headers });
  }

  // Reports
  getReports(): Observable<any> {
    return this.http.get(`${this.baseUrl}/reports`, { headers: this.headers });
  }

  downloadReport(reportId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/reports/${reportId}/pdf`, {
      headers: this.headers,
      responseType: 'blob'
    });
  }

  logout(): void {
    localStorage.removeItem('verocta_token');
    this.tokenSubject.next(null);
  }
}
```

#### 2. Create Angular Components
```typescript
// src/app/components/file-upload.component.ts
import { Component } from '@angular/core';
import { VeroctaApiService } from '../services/verocta-api.service';

@Component({
  selector: 'app-file-upload',
  template: `
    <div class="file-upload">
      <h2>Upload Financial Data</h2>
      
      <div class="upload-section">
        <input
          type="file"
          accept=".csv"
          (change)="onFileSelected($event)"
          #fileInput
        />
        
        <button
          (click)="uploadFile()"
          [disabled]="!selectedFile || uploading"
        >
          {{ uploading ? 'Analyzing...' : 'Upload & Analyze' }}
        </button>
      </div>

      <div *ngIf="error" class="error-message">
        {{ error }}
      </div>

      <div *ngIf="analysis" class="analysis-results">
        <h3>Analysis Results</h3>
        <div class="spend-score">
          <h4>SpendScore: {{ analysis.spend_score }}/100</h4>
          <div [class]="'score-tier ' + analysis.score_tier.color.toLowerCase()">
            {{ analysis.score_tier.tier }}
          </div>
        </div>
        
        <div class="insights">
          <h4>AI Insights</h4>
          <ul>
            <li
              *ngFor="let insight of analysis.insights; let i = index"
              [class]="'priority-' + insight.priority.toLowerCase()"
            >
              <strong>{{ insight.priority }}:</strong> {{ insight.text }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  `
})
export class FileUploadComponent {
  selectedFile: File | null = null;
  uploading = false;
  analysis: any = null;
  error: string | null = null;

  constructor(private veroctaApi: VeroctaApiService) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
    this.error = null;
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.error = 'Please select a file';
      return;
    }

    this.uploading = true;
    this.veroctaApi.uploadFile(this.selectedFile).subscribe({
      next: (response) => {
        this.analysis = response.analysis;
        this.uploading = false;
      },
      error: (err) => {
        this.error = err.error?.error || 'Upload failed';
        this.uploading = false;
      }
    });
  }
}
```

## 🎨 UI Components Library

### SpendScore Display Component
```jsx
// src/components/SpendScoreDisplay.jsx
import React from 'react';

const SpendScoreDisplay = ({ score, tier, breakdown }) => {
  const getScoreColor = (score) => {
    if (score >= 90) return '#4ade80'; // Green
    if (score >= 70) return '#fbbf24'; // Amber
    return '#ef4444'; // Red
  };

  return (
    <div className="spend-score-display">
      <div className="score-circle">
        <div 
          className="score-value"
          style={{ color: getScoreColor(score) }}
        >
          {score}
        </div>
        <div className="score-label">SpendScore</div>
      </div>
      
      <div className="tier-info">
        <h3 className={`tier-${tier.color.toLowerCase()}`}>
          {tier.tier}
        </h3>
        <p>{tier.description}</p>
      </div>

      {breakdown && (
        <div className="score-breakdown">
          <h4>Score Breakdown</h4>
          <div className="breakdown-grid">
            {Object.entries(breakdown).map(([metric, value]) => (
              <div key={metric} className="breakdown-item">
                <span className="metric-name">{metric.replace('_', ' ')}</span>
                <span className="metric-value">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SpendScoreDisplay;
```

### Analysis Insights Component
```jsx
// src/components/AnalysisInsights.jsx
import React from 'react';

const AnalysisInsights = ({ insights }) => {
  const getPriorityIcon = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return '🔴';
      case 'medium': return '🟡';
      case 'low': return '🟢';
      default: return '⚪';
    }
  };

  return (
    <div className="analysis-insights">
      <h3>AI-Powered Insights</h3>
      <div className="insights-list">
        {insights.map((insight, index) => (
          <div 
            key={index} 
            className={`insight-item priority-${insight.priority.toLowerCase()}`}
          >
            <div className="insight-header">
              <span className="priority-icon">
                {getPriorityIcon(insight.priority)}
              </span>
              <span className="priority-label">{insight.priority}</span>
            </div>
            <p className="insight-text">{insight.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnalysisInsights;
```

## 🎯 Best Practices

### 1. Error Handling
```javascript
// Centralized error handling
const handleApiError = (error) => {
  if (error.response?.status === 401) {
    // Redirect to login
    window.location.href = '/login';
  } else if (error.response?.status === 413) {
    // File too large
    return 'File is too large. Please upload a smaller file.';
  } else if (error.response?.data?.error) {
    // API error message
    return error.response.data.error;
  } else {
    // Generic error
    return 'An unexpected error occurred. Please try again.';
  }
};
```

### 2. Loading States
```javascript
// Loading state management
const [loading, setLoading] = useState({
  upload: false,
  analysis: false,
  reports: false
});

const setLoadingState = (key, value) => {
  setLoading(prev => ({ ...prev, [key]: value }));
};
```

### 3. File Validation
```javascript
// File validation
const validateFile = (file) => {
  const maxSize = 16 * 1024 * 1024; // 16MB
  const allowedTypes = ['text/csv', 'application/csv'];
  
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Only CSV files are allowed');
  }
  
  if (file.size > maxSize) {
    throw new Error('File size must be less than 16MB');
  }
  
  return true;
};
```

### 4. Caching Strategy
```javascript
// Simple caching for reports
const cache = new Map();

const getCachedReport = (reportId) => {
  return cache.get(reportId);
};

const setCachedReport = (reportId, data) => {
  cache.set(reportId, data);
  // Clear cache after 5 minutes
  setTimeout(() => cache.delete(reportId), 5 * 60 * 1000);
};
```

## 🔧 Configuration

### Environment Variables
```bash
# .env
VITE_API_URL=https://veroctaai.onrender.com/api
VITE_APP_NAME=VeroctaAI
VITE_APP_VERSION=2.0.0
VITE_MAX_FILE_SIZE=16777216
VITE_SUPPORTED_FORMATS=csv
```

### TypeScript Definitions
```typescript
// src/types/verocta.ts
export interface User {
  id: number;
  email: string;
  company: string;
  role: string;
  created_at: string;
}

export interface SpendScore {
  spend_score: number;
  score_breakdown: {
    frequency_score: number;
    category_diversity: number;
    budget_adherence: number;
    redundancy_detection: number;
    spike_detection: number;
    waste_ratio: number;
  };
  tier_info: {
    color: 'Green' | 'Amber' | 'Red';
    tier: string;
    green_reward_eligible: boolean;
    description: string;
  };
}

export interface AnalysisResult {
  spend_score: number;
  total_transactions: number;
  total_amount: number;
  categories: Record<string, number>;
  insights: Array<{
    priority: 'High' | 'Medium' | 'Low';
    text: string;
  }>;
  score_tier: SpendScore['tier_info'];
}

export interface Report {
  id: number;
  title: string;
  spend_score: number;
  total_amount: number;
  total_transactions: number;
  created_at: string;
  filename: string;
}
```

## 🧪 Testing

### Unit Tests Example
```javascript
// src/services/__tests__/veroctaAPI.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import VeroctaAPI from '../veroctaAPI';

describe('VeroctaAPI', () => {
  test('should upload file successfully', async () => {
    const mockFile = new File(['test,data'], 'test.csv', { type: 'text/csv' });
    const mockResponse = {
      data: {
        success: true,
        analysis: {
          spend_score: 85,
          insights: []
        }
      }
    };

    jest.spyOn(VeroctaAPI.client, 'post').mockResolvedValue(mockResponse);

    const result = await VeroctaAPI.uploadFile(mockFile);
    
    expect(result.success).toBe(true);
    expect(result.analysis.spend_score).toBe(85);
  });
});
```

## 📱 Mobile Integration

### React Native
```javascript
// Using react-native-document-picker
import DocumentPicker from 'react-native-document-picker';

const pickFile = async () => {
  try {
    const result = await DocumentPicker.pick({
      type: [DocumentPicker.types.csv],
    });
    
    const file = {
      uri: result[0].uri,
      type: result[0].type,
      name: result[0].name,
    };
    
    return file;
  } catch (err) {
    console.log('Document picker error:', err);
  }
};
```

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure API URL is correct
   - Check if API supports your domain

2. **Authentication Issues**
   - Verify token is stored correctly
   - Check token expiration

3. **File Upload Failures**
   - Validate file format and size
   - Check network connectivity

4. **Analysis Errors**
   - Ensure CSV has minimum 3 transactions
   - Verify column mapping

## 📞 Support

- **Documentation**: [API Docs](API_DOCUMENTATION.md)
- **Issues**: [GitHub Issues](https://github.com/your-username/veroctaai/issues)
- **Email**: support@verocta.ai

---

**Happy Integrating! 🎨**
