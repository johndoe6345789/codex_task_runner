import React from 'react'

export const Alert = ({ children, title, severity = 'info', icon, action, className = '', ...props }) => (
  <div className={`alert alert--${severity} ${className}`} role="alert" {...props}>
    {icon && <span className="alert-icon">{icon}</span>}
    <div className="alert-content">
      {title && <strong className="alert-title">{title}</strong>}
      {children}
    </div>
    {action && <div className="alert-action">{action}</div>}
  </div>
)
