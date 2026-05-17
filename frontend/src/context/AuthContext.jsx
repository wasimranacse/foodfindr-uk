import { createContext, useContext, useEffect, useMemo, useState } from 'react'

import { apiClient, getProfile, tokenStore } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(Boolean(tokenStore.getAccessToken()))
  const [authError, setAuthError] = useState('')

  useEffect(() => {
    let active = true
    async function loadProfile() {
      if (!tokenStore.getAccessToken()) {
        setIsLoading(false)
        return
      }
      try {
        const profile = await getProfile()
        if (active) setUser(profile)
      } catch {
        tokenStore.clear()
        if (active) setUser(null)
      } finally {
        if (active) setIsLoading(false)
      }
    }
    loadProfile()
    return () => {
      active = false
    }
  }, [])

  async function login(email, password) {
    setAuthError('')
    const { data } = await apiClient.post('/auth/login/', { email, password })
    tokenStore.setTokens({ access: data.access, refresh: data.refresh })
    setUser(data.user)
    return data.user
  }

  async function logout() {
    const refresh = tokenStore.getRefreshToken()
    try {
      if (refresh) {
        await apiClient.post('/auth/logout/', { refresh })
      }
    } finally {
      tokenStore.clear()
      setUser(null)
    }
  }

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      authError,
      setAuthError,
      login,
      logout,
      hasRole: (...roles) => Boolean(user && roles.includes(user.role)),
    }),
    [authError, isLoading, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
