import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { getRestaurants } from '../api/client.js'
import { PageShell } from '../components/PageShell.jsx'
import { RestaurantCard } from '../components/RestaurantCard.jsx'

const fallbackRestaurants = [
  { slug: 'brick-lane-garden-kitchen', name: 'Brick Lane Garden Kitchen', area_name: 'Whitechapel', city_name: 'London', average_rating: '4.6', price_level: 2, trust_score: 94, delivery_available: true, description: 'Fictional Bengali and Indian comfort food with lunch offers.' },
  { slug: 'canary-wharf-green-bowl', name: 'Canary Wharf Green Bowl', area_name: 'Canary Wharf', city_name: 'London', average_rating: '4.4', price_level: 3, trust_score: 91, delivery_available: true, description: 'Plant-powered bowls and premium weekday lunches.' },
  { slug: 'soho-pasta-social', name: 'Soho Pasta Social', area_name: 'Soho', city_name: 'London', average_rating: '4.1', price_level: 3, trust_score: 82, delivery_available: true, description: 'Italian plates, student pasta nights and direct ordering.' },
]

export function RestaurantsPage({ nearby = false }) {
  const [restaurants, setRestaurants] = useState(fallbackRestaurants)
  const [status, setStatus] = useState('Showing sample listings')

  useEffect(() => {
    const params = nearby ? { lat: 51.5136, lng: -0.1365, radius: 5, sort: 'distance' } : { sort: 'smart' }
    getRestaurants(params)
      .then((data) => {
        setRestaurants(data.results || data)
        setStatus('Live backend listings')
      })
      .catch(() => setStatus('Showing sample listings'))
  }, [nearby])

  return (
    <PageShell title={nearby ? 'Nearby restaurants' : 'Restaurants'} eyebrow={status}>
      <div className="mb-5 grid gap-3 rounded-md border border-ink/10 bg-white p-3 shadow-soft sm:grid-cols-4">
        {['City', 'Cuisine', 'Dietary', 'Sort'].map((label) => (
          <select key={label} className="min-h-11 rounded-md border border-ink/10 bg-paper px-3 text-sm font-bold text-ink">
            <option>{label}</option>
          </select>
        ))}
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {restaurants.map((restaurant) => (
          <Link key={restaurant.slug || restaurant.id} to={`/restaurants/${restaurant.slug || restaurant.id}`}>
            <RestaurantCard restaurant={restaurant} />
          </Link>
        ))}
      </div>
    </PageShell>
  )
}
