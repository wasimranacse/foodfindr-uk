import { useParams } from 'react-router-dom'

import { PageShell } from '../components/PageShell.jsx'

export function RestaurantDetailPage() {
  const { slug } = useParams()
  const name = slug
    .split('-')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')

  return (
    <PageShell title={name} eyebrow="Restaurant profile">
      <div className="grid gap-5 lg:grid-cols-[1fr_22rem]">
        <section className="rounded-md border border-ink/10 bg-white p-5 shadow-soft">
          <p className="text-ink/70">Menus, offers, hygiene details, reviews and CTA tracking will render here from the backend.</p>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {['View menu', 'Call restaurant', 'Get directions', 'Order directly'].map((cta) => (
              <button key={cta} className="min-h-12 rounded-md bg-ink px-4 text-sm font-black text-white">
                {cta}
              </button>
            ))}
          </div>
        </section>
        <aside className="rounded-md border border-ink/10 bg-mint p-5">
          <h2 className="font-black text-ink">Trust snapshot</h2>
          <p className="mt-2 text-sm leading-6 text-ink/70">Approved listing, hygiene support, offer status and review health.</p>
        </aside>
      </div>
    </PageShell>
  )
}
