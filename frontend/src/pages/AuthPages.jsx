import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'
import { PageShell } from '../components/PageShell.jsx'
import { getRoleDashboard } from '../utils/routes.js'

export function LoginPage() {
  const { login } = useAuth()
  const [email, setEmail] = useState('customer@foodfindr.local')
  const [password, setPassword] = useState('FoodFindrDev123!')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const location = useLocation()

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    try {
      const user = await login(email, password)
      navigate(location.state?.from?.pathname || getRoleDashboard(user.role), { replace: true })
    } catch (loginError) {
      setError(loginError.message)
    }
  }

  return (
    <PageShell title="Sign in" eyebrow="Secure access">
      <form onSubmit={handleSubmit} className="mx-auto grid max-w-md gap-4 rounded-md border border-ink/10 bg-white p-5 shadow-soft">
        <label className="grid gap-2 text-sm font-bold text-ink">
          Email
          <input className="min-h-12 rounded-md border border-ink/10 px-3" value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>
        <label className="grid gap-2 text-sm font-bold text-ink">
          Password
          <input className="min-h-12 rounded-md border border-ink/10 px-3" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
        </label>
        {error ? <p className="rounded-md bg-red-50 p-3 text-sm font-bold text-red-700">{error}</p> : null}
        <button className="min-h-12 rounded-md bg-ink text-sm font-black text-white">Sign in</button>
        <div className="flex justify-between text-sm font-bold text-leaf">
          <Link to="/forgot-password">Forgot password?</Link>
          <Link to="/register/customer">Create account</Link>
        </div>
      </form>
    </PageShell>
  )
}

export function AuthPlaceholderPage({ title }) {
  return (
    <PageShell title={title} eyebrow="Account">
      <div className="rounded-md border border-ink/10 bg-white p-5 shadow-soft">
        <p className="leading-7 text-ink/70">This account flow is scaffolded and ready to connect to the authentication API.</p>
      </div>
    </PageShell>
  )
}
