import { Link } from 'react-router-dom'

import { PageShell } from '../components/PageShell.jsx'

export function HomePage() {
  return (
    <PageShell title="Find trusted food near you" eyebrow="FoodFindr">
      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <section className="rounded-md bg-ink p-6 text-white shadow-soft sm:p-8">
          <p className="max-w-2xl text-lg leading-8 text-white/78">
            Discover owner-submitted menus, hygiene signals, offers and external ordering links across UK restaurants.
          </p>
          <form className="mt-8 grid gap-3 rounded-md bg-white p-3 sm:grid-cols-[1fr_auto]">
            <input
              aria-label="Search by area, postcode or cuisine"
              className="min-h-12 rounded-md border border-ink/10 px-4 text-ink outline-none focus:border-leaf"
              placeholder="Try Soho, E1 or Bengali"
            />
            <Link
              to="/restaurants/nearby"
              className="grid min-h-12 place-items-center rounded-md bg-ember px-5 text-sm font-black text-white"
            >
              Search nearby
            </Link>
          </form>
        </section>

        <section className="grid gap-3">
          {['Verified listings', 'Manual hygiene support', 'Owner-submitted offers'].map((item) => (
            <div key={item} className="rounded-md border border-ink/10 bg-white p-5 shadow-soft">
              <h2 className="font-black text-ink">{item}</h2>
              <p className="mt-2 text-sm leading-6 text-ink/65">Built for a UK-first restaurant discovery MVP.</p>
            </div>
          ))}
        </section>
      </div>
    </PageShell>
  )
}
