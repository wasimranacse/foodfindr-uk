import { PageShell } from '../components/PageShell.jsx'
import { StatCard } from '../components/StatCard.jsx'

export function DashboardPage({ title, role }) {
  const stats = role === 'owner'
    ? [['Profile views', '128'], ['Menu views', '74'], ['Offer clicks', '21']]
    : role === 'admin'
      ? [['Pending restaurants', '6'], ['Reviews to check', '14'], ['Featured slots', '4']]
      : [['Saved restaurants', '8'], ['Recent offers', '12'], ['Preferences', 'Ready']]

  return (
    <PageShell title={title} eyebrow={role === 'admin' ? 'Admin' : role === 'owner' ? 'Owner tools' : 'Customer'}>
      <div className="grid gap-4 sm:grid-cols-3">
        {stats.map(([label, value]) => (
          <StatCard key={label} label={label} value={value} />
        ))}
      </div>
      <div className="mt-5 rounded-md border border-ink/10 bg-white p-5 shadow-soft">
        <p className="leading-7 text-ink/70">This workspace is scaffolded with protected routing and role-aware access.</p>
      </div>
    </PageShell>
  )
}
