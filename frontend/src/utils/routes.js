export const roleDashboards = {
  customer: '/customer/dashboard',
  restaurant_owner: '/owner/dashboard',
  admin: '/admin/restaurants',
  super_admin: '/admin/restaurants',
}

export function getRoleDashboard(role) {
  return roleDashboards[role] || '/'
}
