export function RestaurantCard({ restaurant }) {
  return (
    <article className="rounded-md border border-ink/10 bg-white p-4 shadow-soft">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-black text-ink">{restaurant.name}</h2>
          <p className="text-sm font-semibold text-ink/60">
            {[restaurant.area_name, restaurant.city_name].filter(Boolean).join(', ') || 'London'}
          </p>
        </div>
        <span className="rounded-md bg-mint px-2 py-1 text-xs font-black text-ink">
          {restaurant.trust_score || 0} trust
        </span>
      </div>
      <p className="line-clamp-2 text-sm leading-6 text-ink/70">{restaurant.description}</p>
      <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs font-bold text-ink/70">
        <span className="rounded-md bg-paper px-2 py-2">{restaurant.average_rating || 'New'} rating</span>
        <span className="rounded-md bg-paper px-2 py-2">Level {restaurant.price_level}</span>
        <span className="rounded-md bg-paper px-2 py-2">{restaurant.delivery_available ? 'Delivery' : 'Collection'}</span>
      </div>
    </article>
  )
}
