export function StatCard({ label, value }) {
  return (
    <div className="rounded-md border border-ink/10 bg-white p-4 shadow-soft">
      <p className="text-sm font-bold text-ink/55">{label}</p>
      <p className="mt-2 text-2xl font-black text-ink">{value}</p>
    </div>
  )
}
