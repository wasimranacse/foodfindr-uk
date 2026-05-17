import { Navigate, Route, Routes } from 'react-router-dom'

import { AppLayout } from '../components/AppLayout.jsx'
import { ProtectedRoute } from '../components/ProtectedRoute.jsx'
import { AuthPlaceholderPage, LoginPage } from '../pages/AuthPages.jsx'
import { DashboardPage } from '../pages/DashboardPages.jsx'
import { HomePage } from '../pages/HomePage.jsx'
import { RestaurantDetailPage } from '../pages/RestaurantDetailPage.jsx'
import { RestaurantsPage } from '../pages/RestaurantsPage.jsx'
import { SimplePage } from '../pages/SimplePage.jsx'

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="restaurants" element={<RestaurantsPage />} />
        <Route path="restaurants/nearby" element={<RestaurantsPage nearby />} />
        <Route path="restaurants/:slug" element={<RestaurantDetailPage />} />
        <Route path="offers" element={<SimplePage title="Offers" body="Browse active restaurant offers, lunch deals, family bundles and student savings." />} />
        <Route path="cuisines" element={<SimplePage title="Cuisines" body="Explore cuisines from Bengali and Turkish to vegan bowls, desserts and coffee." />} />
        <Route path="cities" element={<SimplePage title="Cities" body="FoodFindr starts in London and is structured for Manchester, Birmingham, Leeds and more UK cities." />} />
        <Route path="about" element={<SimplePage title="About FoodFindr" body="FoodFindr is a UK-first platform for restaurant discovery, trust, offers and owner-led promotion." />} />
        <Route path="for-restaurants" element={<SimplePage title="For restaurants" body="Create a trusted listing, add menus, publish offers and track customer actions without scraping third-party platforms." />} />

        <Route path="login" element={<LoginPage />} />
        <Route path="register/customer" element={<AuthPlaceholderPage title="Customer registration" />} />
        <Route path="register/restaurant-owner" element={<AuthPlaceholderPage title="Restaurant owner registration" />} />
        <Route path="verify-email" element={<AuthPlaceholderPage title="Verify email" />} />
        <Route path="forgot-password" element={<AuthPlaceholderPage title="Forgot password" />} />
        <Route path="reset-password" element={<AuthPlaceholderPage title="Reset password" />} />

        <Route element={<ProtectedRoute roles={['customer']} />}>
          <Route path="customer/dashboard" element={<DashboardPage title="Customer dashboard" role="customer" />} />
          <Route path="customer/saved" element={<DashboardPage title="Saved restaurants" role="customer" />} />
          <Route path="customer/preferences" element={<DashboardPage title="Preferences" role="customer" />} />
          <Route path="customer/profile" element={<DashboardPage title="Profile" role="customer" />} />
        </Route>

        <Route element={<ProtectedRoute roles={['restaurant_owner', 'super_admin']} />}>
          <Route path="owner/dashboard" element={<DashboardPage title="Owner dashboard" role="owner" />} />
          <Route path="owner/restaurant" element={<DashboardPage title="Restaurant profile" role="owner" />} />
          <Route path="owner/menu" element={<DashboardPage title="Menu manager" role="owner" />} />
          <Route path="owner/offers" element={<DashboardPage title="Offers manager" role="owner" />} />
          <Route path="owner/analytics" element={<DashboardPage title="Analytics" role="owner" />} />
          <Route path="owner/approval-status" element={<DashboardPage title="Approval status" role="owner" />} />
        </Route>

        <Route element={<ProtectedRoute roles={['admin', 'super_admin']} />}>
          <Route path="admin/restaurants" element={<DashboardPage title="Restaurant approvals" role="admin" />} />
          <Route path="admin/reviews" element={<DashboardPage title="Review moderation" role="admin" />} />
          <Route path="admin/featured" element={<DashboardPage title="Featured placements" role="admin" />} />
          <Route path="admin/security-logs" element={<DashboardPage title="Security logs" role="admin" />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
