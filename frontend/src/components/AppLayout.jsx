import { NavLink, Outlet } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'

const mainLinks = [
  { to: '/', label: 'Discover' },
  { to: '/restaurants', label: 'Restaurants' },
  { to: '/offers', label: 'Offers' },
  { to: '/for-restaurants', label: 'Owners' },
]

const mobileLinks = [
  { to: '/', label: 'Home' },
  { to: '/restaurants/nearby', label: 'Nearby' },
  { to: '/offers', label: 'Offers' },
  { to: '/customer/saved', label: 'Saved' },
]

export function AppLayout() {
  const { user, logout } = useAuth()

  return (
    <div className="app-shell">
      <header className="sticky top-0 z-30 border-b border-ink/10 bg-paper/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
          <NavLink to="/" className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-md bg-ink text-sm font-black text-mint">
              FF
            </span>
            <span>
              <span className="block text-lg font-black tracking-normal text-ink">FoodFindr</span>
              <span className="hidden text-xs font-semibold text-ink/55 sm:block">Trusted UK restaurant discovery</span>
            </span>
          </NavLink>

          <nav className="hidden items-center gap-1 md:flex">
            {mainLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `rounded-md px-3 py-2 text-sm font-bold ${
                    isActive ? 'bg-mint text-ink' : 'text-ink/70 hover:bg-ink/5 hover:text-ink'
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            {user ? (
              <>
                <span className="hidden max-w-40 truncate text-sm font-bold text-ink/70 sm:block">{user.full_name}</span>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded-md bg-ink px-4 py-2 text-sm font-bold text-white"
                >
                  Sign out
                </button>
              </>
            ) : (
              <NavLink to="/login" className="rounded-md bg-ink px-4 py-2 text-sm font-bold text-white">
                Sign in
              </NavLink>
            )}
          </div>
        </div>
      </header>

      <main>
        <Outlet />
      </main>

      <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-ink/10 bg-paper/95 px-3 pb-[calc(0.5rem+env(safe-area-inset-bottom))] pt-2 backdrop-blur md:hidden">
        <div className="mx-auto grid max-w-md grid-cols-4 gap-1">
          {mobileLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `rounded-md px-2 py-2 text-center text-xs font-black ${
                  isActive ? 'bg-ink text-white' : 'text-ink/65'
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  )
}
