"use client"

import { useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
} from "recharts"
import { TrendingUp, BarChart3, Activity, ArrowRight, CheckCircle2, Target } from "lucide-react"

const VeroctaAILanding = () => {
  const [activeTab, setActiveTab] = useState("analytics")

  // Sample data for charts
  const lineData = [
    { month: "Jan", revenue: 45000, spending: 32000 },
    { month: "Feb", revenue: 52000, spending: 28000 },
    { month: "Mar", revenue: 48000, spending: 35000 },
    { month: "Apr", revenue: 61000, spending: 31000 },
    { month: "May", revenue: 55000, spending: 29000 },
    { month: "Jun", revenue: 67000, spending: 33000 },
  ]

  const barData = [
    { category: "Marketing", spend: 12500, score: 85 },
    { category: "Operations", spend: 18200, score: 92 },
    { category: "Technology", spend: 8900, score: 78 },
    { category: "HR", spend: 6400, score: 88 },
  ]

  const spendScoreData = [
    { month: "Jan", spendScore: 78, efficiency: 82, optimization: 75 },
    { month: "Feb", spendScore: 85, efficiency: 88, optimization: 83 },
    { month: "Mar", spendScore: 82, efficiency: 85, optimization: 79 },
    { month: "Apr", spendScore: 91, efficiency: 94, optimization: 88 },
    { month: "May", spendScore: 88, efficiency: 91, optimization: 85 },
    { month: "Jun", spendScore: 94, efficiency: 96, optimization: 92 },
  ]

  const departmentScores = [
    { department: "Marketing", currentScore: 85, targetScore: 90, improvement: 12 },
    { department: "Operations", currentScore: 92, targetScore: 95, improvement: 8 },
    { department: "Technology", currentScore: 78, targetScore: 85, improvement: 15 },
    { department: "HR", currentScore: 88, targetScore: 92, improvement: 10 },
    { department: "Finance", currentScore: 95, targetScore: 98, improvement: 5 },
  ]

  const pieData = [
    { name: "Excellent", value: 45, color: "#10b981" },
    { name: "Good", value: 30, color: "#059669" },
    { name: "Average", value: 20, color: "#047857" },
    { name: "Poor", value: 5, color: "#065f46" },
  ]

  const features = [
    { title: "REST API Integration", desc: "Seamless financial data access" },
    { title: "SpendScore Analytics", desc: "AI-powered spending intelligence" },
    { title: "Real-time Insights", desc: "Live financial performance metrics" },
    { title: "Company Branding", desc: "White-label solution support" },
  ]

  return (
    <div className="min-h-screen" style={{ background: "linear-gradient(135deg, #BFDEF3 0%, #B9E9E9 100%)" }}>
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-md border-b border-white/30 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center"
                style={{ background: "linear-gradient(135deg, #b583c8 0%, #00416A 100%)" }}
              >
                <span className="text-white font-bold text-lg">V</span>
              </div>
              <span className="text-2xl font-bold" style={{ color: "#00416A" }}>
                VeroctaAI
              </span>
            </div>
            <nav className="hidden md:flex items-center space-x-8">
              <a
                href="#"
                className="font-medium transition-colors"
                style={{ color: "#00416A" }}
                onMouseEnter={(e) => (e.target.style.color = "#b583c8")}
                onMouseLeave={(e) => (e.target.style.color = "#00416A")}
              >
                Platform
              </a>
              <a
                href="#"
                className="font-medium transition-colors"
                style={{ color: "#00416A" }}
                onMouseEnter={(e) => (e.target.style.color = "#b583c8")}
                onMouseLeave={(e) => (e.target.style.color = "#00416A")}
              >
                API Docs
              </a>
              <a
                href="#"
                className="font-medium transition-colors"
                style={{ color: "#00416A" }}
                onMouseEnter={(e) => (e.target.style.color = "#b583c8")}
                onMouseLeave={(e) => (e.target.style.color = "#00416A")}
              >
                Pricing
              </a>
              <button
                className="text-white px-6 py-2.5 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
                style={{ background: "linear-gradient(135deg, #b583c8 0%, #00416A 100%)" }}
              >
                Get Started
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span style={{ color: "#00416A" }}>Financial Intelligence</span>
            <br />
            <span
              style={{
                background: "linear-gradient(135deg, #b583c8 0%, #00416A 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              Redefined
            </span>
          </h1>
          <p className="text-xl max-w-3xl mx-auto leading-relaxed" style={{ color: "#00416A" }}>
            Comprehensive REST API for financial data analysis, SpendScore calculation, and intelligent insights
            generation with enhanced company branding support.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-10">
            <button
              className="text-white px-8 py-4 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl flex items-center justify-center gap-2 font-semibold"
              style={{ background: "linear-gradient(135deg, #b583c8 0%, #00416A 100%)" }}
            >
              Start Free Trial <ArrowRight className="w-5 h-5" />
            </button>
            <button
              className="px-8 py-4 rounded-xl transition-all duration-200 font-semibold"
              style={{
                border: "2px solid #b583c8",
                color: "#00416A",
                backgroundColor: "rgba(181, 131, 200, 0.1)",
              }}
            >
              View Documentation
            </button>
          </div>
        </div>

        {/* Dashboard Preview */}
        <div
          className="bg-white/70 backdrop-blur-md rounded-2xl shadow-2xl p-8" 
          style={{ border: "1px solid rgba(181, 131, 200, 0.3)" }}
        >
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Sidebar */}
            <div className="lg:w-64">
              <div className="space-y-3">
                {[
                  { id: "analytics", icon: TrendingUp, label: "Revenue Analytics" },
                  { id: "spending", icon: BarChart3, label: "SpendScore Analysis" },
                  { id: "scoretrends", icon: Target, label: "Score Trends" },
                  { id: "insights", icon: Activity, label: "Performance Insights" },
                ].map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                      activeTab === item.id ? "text-white shadow-md" : "hover:bg-white/50"
                    }`}
                    style={
                      activeTab === item.id
                        ? { background: "linear-gradient(135deg, #b583c8 0%, #00416A 100%)" }
                        : { color: "#00416A" }
                    }
                  >
                    <item.icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Main Content */}
            <div className="flex-1">
              {activeTab === "analytics" && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-bold mb-4" style={{ color: "#00416A" }}>
                      Revenue Analytics
                    </h3>
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
                        <span className="text-sm text-slate-600">Revenue</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-green-600 rounded-full"></div>
                        <span className="text-sm text-slate-600">Spending</span>
                      </div>
                    </div>
                  </div>
                  <div className="h-80 rounded-xl p-4" style={{ backgroundColor: "rgba(191, 222, 243, 0.3)" }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={lineData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 65, 106, 0.2)" />
                        <XAxis dataKey="month" stroke="#00416A" />
                        <YAxis stroke="#00416A" />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "white",
                            border: "1px solid #e2e8f0",
                            borderRadius: "12px",
                            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                          }}
                        />
                        <Line
                          type="monotone"
                          dataKey="revenue"
                          stroke="#10b981"
                          strokeWidth={3}
                          dot={{ fill: "#10b981", r: 6 }}
                        />
                        <Line
                          type="monotone"
                          dataKey="spending"
                          stroke="#047857"
                          strokeWidth={3}
                          dot={{ fill: "#047857", r: 6 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              {activeTab === "spending" && (
                <div className="space-y-6">
                  <h3 className="text-2xl font-bold mb-4" style={{ color: "#00416A" }}>
                    SpendScore by Category
                  </h3>
                  <div className="h-80 rounded-xl p-4" style={{ backgroundColor: "rgba(191, 222, 243, 0.3)" }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={barData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 65, 106, 0.2)" />
                        <XAxis dataKey="category" stroke="#00416A" />
                        <YAxis stroke="#00416A" />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "white",
                            border: "1px solid #e2e8f0",
                            borderRadius: "12px",
                            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                          }}
                        />
                        <Bar dataKey="spend" fill="url(#greenBarGradient)" radius={[8, 8, 0, 0]} />
                        <defs>
                          <linearGradient id="greenBarGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#047857" stopOpacity={0.6} />
                          </linearGradient>
                        </defs>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              {activeTab === "scoretrends" && (
                <div className="space-y-6">
                  <h3 className="text-2xl font-bold mb-4" style={{ color: "#00416A" }}>
                    SpendScore Trends
                  </h3>

                  {/* Area Chart for Score Trends */}
                  <div className="h-80 rounded-xl p-4" style={{ backgroundColor: "rgba(191, 222, 243, 0.3)" }}>
                    <div className="flex items-center gap-6 mb-4">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#10b981" }}></div>
                        <span className="text-sm text-slate-600">SpendScore</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#059669" }}></div>
                        <span className="text-sm text-slate-600">Efficiency</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#047857" }}></div>
                        <span className="text-sm text-slate-600">Optimization</span>
                      </div>
                    </div>
                    <ResponsiveContainer width="100%" height="90%">
                      <AreaChart data={spendScoreData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 65, 106, 0.2)" />
                        <XAxis dataKey="month" stroke="#00416A" />
                        <YAxis stroke="#00416A" domain={[70, 100]} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "white",
                            border: "1px solid #e2e8f0",
                            borderRadius: "12px",
                            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                          }}
                        />
                        <Area
                          type="monotone"
                          dataKey="spendScore"
                          stackId="1"
                          stroke="#10b981"
                          fill="rgba(16, 185, 129, 0.3)"
                          strokeWidth={2}
                        />
                        <Area
                          type="monotone"
                          dataKey="efficiency"
                          stackId="2"
                          stroke="#059669"
                          fill="rgba(5, 150, 105, 0.3)"
                          strokeWidth={2}
                        />
                        <Area
                          type="monotone"
                          dataKey="optimization"
                          stackId="3"
                          stroke="#047857"
                          fill="rgba(4, 120, 87, 0.3)"
                          strokeWidth={2}
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Department Score Comparison */}
                  <div className="mt-8">
                    <h4 className="text-xl font-bold mb-4" style={{ color: "#00416A" }}>
                      Department Score Performance
                    </h4>
                    <div className="h-80 rounded-xl p-4" style={{ backgroundColor: "rgba(191, 222, 243, 0.3)" }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={departmentScores} layout="horizontal">
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 65, 106, 0.2)" />
                          <XAxis type="number" domain={[0, 100]} stroke="#00416A" />
                          <YAxis dataKey="department" type="category" stroke="#00416A" width={80} />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: "white",
                              border: "1px solid #e2e8f0",
                              borderRadius: "12px",
                              boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                            }}
                          />
                          <Bar dataKey="currentScore" fill="#10b981" radius={[0, 4, 4, 0]} />
                          <Bar dataKey="targetScore" fill="#d1fae5" radius={[0, 4, 4, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "insights" && (
                <div className="space-y-6">
                  <h3 className="text-2xl font-bold mb-4" style={{ color: "#00416A" }}>
                    Performance Distribution
                  </h3>
                  <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex-1 h-80 rounded-xl p-4" style={{ backgroundColor: "rgba(191, 222, 243, 0.3)" }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={120}
                            paddingAngle={5}
                            dataKey="value"
                          >
                            {pieData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="lg:w-64 space-y-4">
                      {pieData.map((item, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between p-3 bg-white/70 rounded-lg"
                          style={{ border: "1px solid rgba(181, 131, 200, 0.3)" }}
                        >
                          <div className="flex items-center gap-3">
                            <div className="w-4 h-4 rounded-full" style={{ backgroundColor: item.color }}></div>
                            <span className="font-medium" style={{ color: "#00416A" }}>
                              {item.name}
                            </span>
                          </div>
                          <span className="font-semibold" style={{ color: "#00416A" }}>
                            {item.value}%
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4" style={{ color: "#00416A" }}>
            Platform Features
          </h2>
          <p className="text-xl" style={{ color: "#00416A" }}>
            Powerful tools for financial intelligence
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white/70 backdrop-blur-md p-6 rounded-2xl hover:shadow-lg transition-all duration-200"
              style={{ border: "1px solid rgba(181, 131, 200, 0.3)" }}
            >
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
                style={{ background: "linear-gradient(135deg, #b583c8 0%, #00416A 100%)" }}
              >
                <CheckCircle2 className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-2" style={{ color: "#00416A" }}>
                {feature.title}
              </h3>
              <p style={{ color: "#00416A" }}>{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20" style={{ background: "linear-gradient(135deg, #00416A 0%, #b583c8 100%)" }}>
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-4xl font-bold text-white mb-6">Ready to Transform Your Financial Analytics?</h2>
          <p className="text-xl mb-8" style={{ color: "rgba(255, 255, 255, 0.9)" }}>
            Join leading companies using VeroctaAI for smarter financial decisions
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              className="bg-white px-8 py-4 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl font-semibold"
              style={{ color: "#00416A" }}
            >
              Start Free Trial
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl hover:bg-white/10 transition-all duration-200 font-semibold">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ backgroundColor: "#00416A" }} className="text-white py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center"
                style={{ background: "linear-gradient(135deg, #b583c8 0%, #BFDEF3 100%)" }}
              >
                <span className="font-bold" style={{ color: "#00416A" }}>
                  V
                </span>
              </div>
              <span className="text-xl font-bold text-white">VeroctaAI</span>
            </div>
            <p className="text-white/80">&copy; 2024 VeroctaAI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default VeroctaAILanding
