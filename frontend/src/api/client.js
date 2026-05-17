import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const TOKEN_KEYS = {
  access: 'foodfindr_access_token',
  refresh: 'foodfindr_refresh_token',
}

export const tokenStore = {
  getAccessToken: () => localStorage.getItem(TOKEN_KEYS.access),
  getRefreshToken: () => localStorage.getItem(TOKEN_KEYS.refresh),
  setTokens: ({ access, refresh }) => {
    if (access) localStorage.setItem(TOKEN_KEYS.access, access)
    if (refresh) localStorage.setItem(TOKEN_KEYS.refresh, refresh)
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEYS.access)
    localStorage.removeItem(TOKEN_KEYS.refresh)
  },
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

let refreshPromise = null

apiClient.interceptors.request.use((config) => {
  const token = tokenStore.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const status = error.response?.status

    if (status === 401 && !originalRequest?._retry && tokenStore.getRefreshToken()) {
      originalRequest._retry = true
      refreshPromise =
        refreshPromise ||
        axios
          .post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: tokenStore.getRefreshToken(),
          })
          .finally(() => {
            refreshPromise = null
          })

      try {
        const { data } = await refreshPromise
        tokenStore.setTokens({ access: data.access, refresh: data.refresh })
        originalRequest.headers.Authorization = `Bearer ${data.access}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        tokenStore.clear()
        return Promise.reject(normaliseApiError(refreshError))
      }
    }

    return Promise.reject(normaliseApiError(error))
  },
)

export function normaliseApiError(error) {
  const data = error.response?.data
  if (data?.detail) {
    return new Error(Array.isArray(data.detail) ? data.detail.join(' ') : data.detail)
  }
  if (data && typeof data === 'object') {
    const firstError = Object.values(data).flat().filter(Boolean)[0]
    if (firstError) return new Error(String(firstError))
  }
  return new Error(error.message || 'Something went wrong. Please try again.')
}

export async function getRestaurants(params = {}) {
  const { data } = await apiClient.get('/restaurants/', { params })
  return data
}

export async function getFeaturedRestaurants() {
  const { data } = await apiClient.get('/restaurants/featured/')
  return data
}

export async function getActiveOffers() {
  const { data } = await apiClient.get('/offers/active/')
  return data
}

export async function getProfile() {
  const { data } = await apiClient.get('/auth/profile/')
  return data
}
