import React from 'react'

export const Pagination = ({ count, page, onChange, size, className = '', ...props }) => (
  <nav className={`pagination ${size ? `pagination--${size}` : ''} ${className}`} {...props}>
    <button className="pagination-btn" disabled={page <= 1} onClick={() => onChange?.(page - 1)}>‹</button>
    {Array.from({ length: count }, (_, i) => (
      <button key={i + 1} className={`pagination-btn ${page === i + 1 ? 'pagination-btn--active' : ''}`} onClick={() => onChange?.(i + 1)}>{i + 1}</button>
    ))}
    <button className="pagination-btn" disabled={page >= count} onClick={() => onChange?.(page + 1)}>›</button>
  </nav>
)
