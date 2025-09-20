# VEROCTA Front-End

A modern, responsive front-end application for VEROCTA Financial Intelligence Platform, built with React, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Modern React 18** with TypeScript
- **Responsive Design** with Tailwind CSS
- **Component-Based Architecture** for maintainability
- **Routing** with React Router
- **Form Handling** with controlled components
- **Mobile-First** responsive design
- **SEO Optimized** with proper meta tags
- **Performance Optimized** with Vite build tool

## 🛠️ Tech Stack

- **Frontend Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Icons**: Heroicons
- **Linting**: ESLint
- **Code Formatting**: Prettier

## 📁 Project Structure

```
veroctaai-frontend/
├── public/                 # Static assets
├── src/                    # Source code
│   ├── components/         # Reusable UI components
│   │   └── Layout/        # Layout components (Header, Footer, etc.)
│   ├── pages/             # Page components
│   │   ├── Home.tsx       # Home page
│   │   ├── About.tsx      # About page
│   │   ├── Services.tsx   # Services page
│   │   └── Contact.tsx    # Contact page
│   ├── assets/            # Images, icons, and other assets
│   ├── styles/            # CSS and styling files
│   ├── utils/             # Utility functions and helpers
│   ├── config/            # Configuration files and constants
│   ├── types/             # TypeScript type definitions
│   ├── App.tsx            # Main App component
│   └── main.tsx           # Application entry point
├── docs/                  # Documentation and project files
├── .eslintrc.js          # ESLint configuration
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
├── tsconfig.json          # TypeScript configuration
├── vite.config.js         # Vite build configuration
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Node.js 16.0.0 or higher
- npm 8.0.0 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd veroctaai-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run test` - Run tests
- `npm run test:ui` - Run tests with UI

## 🎨 Design System

### Colors
- **Primary**: Blue shades (#3b82f6 to #1e3a8a)
- **Secondary**: Gray shades (#64748b to #0f172a)
- **Accent**: Gradient combinations

### Typography
- **Primary Font**: Inter (Google Fonts)
- **Monospace Font**: JetBrains Mono
- **Font Weights**: 300, 400, 500, 600, 700

### Components
- **Buttons**: Primary, Secondary, Outline variants
- **Cards**: Consistent shadow and border styling
- **Forms**: Accessible form controls with validation
- **Navigation**: Responsive navigation with mobile menu

## 📱 Responsive Design

The application is built with a mobile-first approach and includes:
- Responsive grid layouts
- Mobile navigation menu
- Touch-friendly interface elements
- Optimized typography for all screen sizes

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=VeroctaAI
VITE_APP_VERSION=1.0.0
```

### Tailwind CSS
Custom configuration in `tailwind.config.js` includes:
- Custom color palette
- Extended spacing and typography
- Custom animations and transitions

## 🧪 Testing

The project includes testing setup with Vitest:
- Unit testing for components
- Integration testing for pages
- Test utilities and mocks

## 📦 Building for Production

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Preview the build**
   ```bash
   npm run preview
   ```

3. **Deploy the `dist` folder** to your hosting service

## 🚀 Deployment

### Static Hosting (Netlify, Vercel, etc.)
1. Build the project: `npm run build`
2. Deploy the `dist` folder
3. Configure redirects for SPA routing

### Docker Deployment
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Code Style
- Use TypeScript for all new code
- Follow ESLint and Prettier configurations
- Write meaningful commit messages
- Include tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Email**: support@verocta.ai
- **Documentation**: [docs.verocta.ai](https://docs.verocta.ai)
- **Issues**: [GitHub Issues](https://github.com/verocta-ai/frontend/issues)

## 🙏 Acknowledgments

- [React Team](https://reactjs.org/) for the amazing framework
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Vite](https://vitejs.dev/) for the fast build tool
- [Heroicons](https://heroicons.com/) for the beautiful icons

---

**Built with ❤️ by the VeroctaAI Team**
