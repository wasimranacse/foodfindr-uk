import { PageShell } from '../components/PageShell.jsx'

export function SimplePage({ title, eyebrow = 'FoodFindr', body }) {
  return (
    <PageShell title={title} eyebrow={eyebrow}>
      <div className="rounded-md border border-ink/10 bg-white p-5 shadow-soft">
        <p className="max-w-3xl leading-7 text-ink/70">{body}</p>
      </div>
    </PageShell>
  )
}
