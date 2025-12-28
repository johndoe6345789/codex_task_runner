import React from 'react'

const PersonIcon = () => (
  <svg className="icon icon--lg" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
  </svg>
)

export default function UserInfo({ user, apiBase }) {
  if (!user) {
    return (
      <div className="max-w-md mx-auto text-center" style={{ padding: 'var(--spacing-xl)' }}>
        <p className="text-secondary">Loading user info...</p>
      </div>
    )
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card">
        <div className="card-content">
          <div className="flex items-center gap-md mb-lg">
            <div className="avatar avatar--lg flex-center">
              {user.picture || user.image ? (
                <img src={user.picture || user.image} alt="" />
              ) : (
                <PersonIcon />
              )}
            </div>
            <div>
              <h2 className="text-xl" style={{ fontWeight: 600, margin: 0 }}>{user.name || user.email || 'User'}</h2>
              <p className="text-secondary text-sm">{user.email}</p>
            </div>
          </div>

          <div className="divider" />

          <ul className="list">
            {Object.entries(user).map(([key, value]) => {
              if (typeof value === 'object') return null
              return (
                <li key={key} className="list-item">
                  <div className="label">{key}</div>
                  <div className="text-sm">{String(value)}</div>
                </li>
              )
            })}
          </ul>
        </div>
      </div>

      <div className="card mt-md">
        <div className="card-content">
          <h4 className="text-sm mb-sm">API Connection</h4>
          <span className="chip chip--success">Connected</span>
          <p className="text-xs text-secondary font-mono mt-sm">
            API Base: {apiBase || window.location.origin}
          </p>
        </div>
      </div>
    </div>
  )
}
