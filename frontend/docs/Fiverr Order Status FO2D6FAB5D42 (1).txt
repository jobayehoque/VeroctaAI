import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Landing from './pages/Landing'
import Product from './pages/Product'
import Pricing from './pages/Pricing'
import About from './pages/About'
import Auth from './pages/Auth'
import Dashboard from './pages/Dashboard'
import Insights from './pages/Insights'
import Company from './pages/CompanyPage'
import Legal from './pages/Legal'
import Resources from './pages/Resources'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}> 
          <Route path="/" element={<Landing />} />
          <Route path="/product" element={<Product />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/about" element={<About />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/dashboard" element={<Dashboard />} />
    
          <Route path="/insights" element={<Insights />} />
    
          <Route path="/Company" element={<Company />} />
          <Route path="/Legal" element={<Legal />} />
          <Route path="/Resources" element={<Resources />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
