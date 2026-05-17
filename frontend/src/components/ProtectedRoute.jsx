import { Navigate, Outlet, useLocation } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'

export function ProtectedRoute({ roles }) {
  const { user, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return <div className="p-6 text-sm font-bold text-ink/70">Loading your FoodFindr session...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  if (roles?.length && !roles.includes(user.role)) {
    return <Navigate to="/" replace />
  }

  return <Outlet />
}
