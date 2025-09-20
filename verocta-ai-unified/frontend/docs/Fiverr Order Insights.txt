export default function Insights() {
  const insights = [
    { title: 'Reduce SaaS overlap', detail: 'Two tools with similar features; consolidate to save ~$120/mo.' },
    { title: 'Negotiate vendor contract', detail: 'Your top vendor raised rates 12% YoY; consider a 1-year commitment for discount.' },
    { title: 'Switch to annual billing', detail: 'Annual plan for Tool X saves 15% vs monthly.' },
  ]
  const categories = [
    { name: 'Subscriptions', amount: 1240 },
    { name: 'Marketing', amount: 860 },
    { name: 'Operations', amount: 540 },
    { name: 'Other', amount: 220 },
  ]
  return (
    <div className="container-page py-16">
      <h1 className="text-3xl font-bold">Insights</h1>
      <div className="grid md:grid-cols-2 gap-6 mt-8">
        <div className="rounded-xl bg-slate-900 p-6 border border-slate-800">
          <div className="text-slate-300 font-medium mb-3">AI Recommendations</div>
          <ul className="space-y-3">
            {insights.map((i) => (
              <li key={i.title} className="p-4 rounded-lg bg-slate-800/60">
                <div className="text-indigo-300 font-semibold">{i.title}</div>
                <div className="text-slate-300 text-sm mt-1">{i.detail}</div>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-xl bg-slate-900 p-6 border border-slate-800">
          <div className="text-slate-300 font-medium mb-3">Spending Categories</div>
          <ul className="space-y-2 text-slate-300">
            {categories.map((c) => (
              <li key={c.name} className="flex items-center justify-between">
                <span>{c.name}</span>
                <span className="text-slate-200 font-semibold">${c.amount}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}


