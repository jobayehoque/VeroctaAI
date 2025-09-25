# 🎨 VeroctaAI Frontend

Modern React frontend for the VeroctaAI financial intelligence platform.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:5000/api` |
| `VITE_APP_NAME` | Application name | `VeroctaAI` |
| `VITE_APP_VERSION` | Application version | `2.0.0` |

### Example .env file
```bash
VITE_API_URL=https://veroctaai.onrender.com/api
VITE_APP_NAME=VeroctaAI
VITE_APP_VERSION=2.0.0
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Layout/         # Layout components
│   │   ├── AdminDashboard.tsx
│   │   ├── DashboardHome.tsx
│   │   ├── UploadManager.tsx
│   │   └── ...
│   ├── pages/              # Page components
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   └── ...
│   ├── contexts/           # React contexts
│   │   └── AuthContext.tsx
│   ├── utils/              # Utility functions
│   │   └── api.ts
│   ├── types/              # TypeScript types
│   │   └── index.ts
│   ├── styles/             # CSS styles
│   └── assets/             # Static assets
├── public/                 # Public assets
├── package.json           # Dependencies
├── vite.config.js         # Vite configuration
└── tailwind.config.js     # Tailwind CSS configuration
```

## 🎯 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues
- `npm run format` - Format code with Prettier

## 🔌 API Integration

The frontend integrates with the VeroctaAI backend API:

```typescript
// Example API usage
import { apiClient } from './utils/api';

// Upload file for analysis
const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post('/upload', formData);
  return response.data;
};

// Get SpendScore
const getSpendScore = async () => {
  const response = await apiClient.get('/spend-score');
  return response.data;
};
```

## 🎨 UI Components

### Core Components
- **UploadManager**: File upload and analysis
- **DashboardHome**: Main dashboard view
- **InsightsEngine**: AI insights display
- **ReportsManager**: Report management
- **SettingsManager**: User settings

### Layout Components
- **Header**: Navigation header
- **Sidebar**: Navigation sidebar
- **Footer**: Page footer
- **Layout**: Main layout wrapper

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Netlify
```bash
# Build the project
npm run build

# Deploy dist folder to Netlify
```

## 🧪 Testing

### Run Tests
```bash
npm run test
```

### Test Coverage
```bash
npm run test:coverage
```

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🎨 Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Custom Components**: Reusable UI components
- **Dark Mode**: Built-in dark mode support
- **Responsive**: Mobile-first responsive design

## 🔐 Authentication

The frontend uses JWT-based authentication:

```typescript
// Login example
const login = async (email: string, password: string) => {
  const response = await apiClient.post('/auth/login', {
    email,
    password
  });
  
  // Store token
  localStorage.setItem('auth_token', response.data.token);
  
  return response.data;
};
```

## 📊 Features

### Dashboard
- Financial overview
- SpendScore display
- Recent transactions
- Quick actions

### File Upload
- Drag & drop interface
- CSV format validation
- Progress indicators
- Error handling

### Analysis
- Real-time SpendScore calculation
- AI-powered insights
- Category breakdown
- Trend analysis

### Reports
- PDF report generation
- Historical data
- Export functionality
- Sharing options

## 🆘 Support

For frontend-specific issues:
- Check the [API Documentation](../docs/API_DOCUMENTATION.md)
- Review the [Frontend Integration Guide](../docs/FRONTEND_INTEGRATION_GUIDE.md)
- Open an issue on GitHub

---

**VeroctaAI Frontend v2.0**  
*Built with React, TypeScript, and Tailwind CSS*