// Atomic React Components
// Simple wrappers around CSS atom classes

import React from 'react'

// Layout
export const Flex = ({ children, col, center, between, wrap, gap, className = '', ...props }) => (
  <div className={`flex ${col ? 'flex-col' : ''} ${center ? 'flex-center' : ''} ${between ? 'flex-between' : ''} ${wrap ? 'flex-wrap' : ''} ${gap ? `gap-${gap}` : ''} ${className}`} {...props}>{children}</div>
)

export const Grid = ({ children, auto, cols, gap, className = '', ...props }) => (
  <div className={`${auto ? 'auto-grid' : 'grid'} ${cols ? `grid-cols-${cols}` : ''} ${gap ? `gap-${gap}` : ''} ${className}`} {...props}>{children}</div>
)

// Card
export const Card = ({ children, clickable, fullHeight, className = '', ...props }) => (
  <div className={`card ${clickable ? 'card--clickable' : ''} ${fullHeight ? 'card--full-height' : ''} ${className}`} {...props}>{children}</div>
)

export const CardHeader = ({ children, className = '', ...props }) => (
  <div className={`card-header ${className}`} {...props}>{children}</div>
)

export const CardContent = ({ children, className = '', ...props }) => (
  <div className={`card-content ${className}`} {...props}>{children}</div>
)

export const CardActions = ({ children, className = '', ...props }) => (
  <div className={`card-actions ${className}`} {...props}>{children}</div>
)

// Typography
export const Title = ({ children, page, card, truncate, className = '', as: Tag = 'h2', ...props }) => (
  <Tag className={`${page ? 'page-title' : ''} ${card ? 'card-title' : ''} ${truncate ? 'card-title--truncate' : ''} ${className}`} {...props}>{children}</Tag>
)

export const Subtitle = ({ children, className = '', ...props }) => (
  <p className={`page-subtitle ${className}`} {...props}>{children}</p>
)

export const Label = ({ children, className = '', ...props }) => (
  <span className={`label ${className}`} {...props}>{children}</span>
)

export const Text = ({ children, secondary, disabled, sm, xs, mono, center, truncate, className = '', as: Tag = 'span', ...props }) => (
  <Tag className={`${secondary ? 'text-secondary' : ''} ${disabled ? 'text-disabled' : ''} ${sm ? 'text-sm' : ''} ${xs ? 'text-xs' : ''} ${mono ? 'font-mono' : ''} ${center ? 'text-center' : ''} ${truncate ? 'truncate' : ''} ${className}`} {...props}>{children}</Tag>
)

// Form
export const Input = ({ sm, md, className = '', ...props }) => (
  <input className={`input ${sm ? 'input--sm' : ''} ${md ? 'input--md' : ''} ${className}`} {...props} />
)

export const Textarea = ({ className = '', ...props }) => (
  <textarea className={`textarea ${className}`} {...props} />
)

export const Select = ({ children, sm, className = '', ...props }) => (
  <select className={`select ${sm ? 'select--sm' : ''} ${className}`} {...props}>{children}</select>
)

export const FormGroup = ({ children, className = '', ...props }) => (
  <div className={`form-group ${className}`} {...props}>{children}</div>
)

export const FormLabel = ({ children, className = '', ...props }) => (
  <label className={`form-label ${className}`} {...props}>{children}</label>
)

// Button
export const Button = ({ children, primary, secondary, outline, sm, lg, icon, className = '', ...props }) => (
  <button className={`btn ${primary ? 'btn--primary' : ''} ${secondary ? 'btn--secondary' : ''} ${outline ? 'btn--outline' : ''} ${sm ? 'btn--sm' : ''} ${lg ? 'btn--lg' : ''} ${icon ? 'btn--icon' : ''} ${className}`} {...props}>{children}</button>
)

export const IconButton = ({ children, className = '', ...props }) => (
  <button className={`icon-btn ${className}`} {...props}>{children}</button>
)

// Chip
export const Chip = ({ children, success, error, warning, info, sm, className = '', ...props }) => (
  <span className={`chip ${success ? 'chip--success' : ''} ${error ? 'chip--error' : ''} ${warning ? 'chip--warning' : ''} ${info ? 'chip--info' : ''} ${sm ? 'chip--sm' : ''} ${className}`} {...props}>{children}</span>
)

// Badge / Stat
export const Badge = ({ children, className = '', ...props }) => (
  <span className={`badge ${className}`} {...props}>{children}</span>
)

export const StatBadge = ({ children, pending, success, error, info, className = '', ...props }) => (
  <span className={`stat-badge ${pending ? 'stat-badge--pending' : ''} ${success ? 'stat-badge--success' : ''} ${error ? 'stat-badge--error' : ''} ${info ? 'stat-badge--info' : ''} ${className}`} {...props}>{children}</span>
)

// List
export const List = ({ children, spaced, className = '', ...props }) => (
  <ul className={`list ${spaced ? 'list--spaced' : ''} ${className}`} {...props}>{children}</ul>
)

export const ListItem = ({ children, clickable, borderless, className = '', ...props }) => (
  <li className={`list-item ${clickable ? 'list-item--clickable' : ''} ${borderless ? 'list-item--borderless' : ''} ${className}`} {...props}>{children}</li>
)

// Dialog
export const DialogOverlay = ({ children, onClick, className = '', ...props }) => (
  <div className={`dialog-overlay ${className}`} onClick={onClick} {...props}>{children}</div>
)

export const DialogPanel = ({ children, sm, lg, xl, className = '', onClick, ...props }) => (
  <div className={`dialog-panel ${sm ? 'dialog-panel--sm' : ''} ${lg ? 'dialog-panel--lg' : ''} ${xl ? 'dialog-panel--xl' : ''} ${className}`} onClick={e => e.stopPropagation()} {...props}>{children}</div>
)

export const DialogHeader = ({ children, className = '', ...props }) => (
  <div className={`dialog-header ${className}`} {...props}>{children}</div>
)

export const DialogTitle = ({ children, className = '', ...props }) => (
  <h2 className={`dialog-title ${className}`} {...props}>{children}</h2>
)

export const DialogContent = ({ children, className = '', ...props }) => (
  <div className={`dialog-content ${className}`} {...props}>{children}</div>
)

export const DialogFooter = ({ children, className = '', ...props }) => (
  <div className={`dialog-footer ${className}`} {...props}>{children}</div>
)

// Section
export const Section = ({ children, sm, className = '', ...props }) => (
  <div className={`section ${sm ? 'section--sm' : ''} ${className}`} {...props}>{children}</div>
)

export const SectionHeader = ({ children, className = '', ...props }) => (
  <div className={`section-header ${className}`} {...props}>{children}</div>
)

export const SectionTitle = ({ children, className = '', ...props }) => (
  <h3 className={`section-title ${className}`} {...props}>{children}</h3>
)

export const SectionContent = ({ children, className = '', ...props }) => (
  <div className={`section-content ${className}`} {...props}>{children}</div>
)

// Toolbar
export const Toolbar = ({ children, sm, end, between, className = '', ...props }) => (
  <div className={`toolbar ${sm ? 'toolbar--sm' : ''} ${end ? 'toolbar--end' : ''} ${between ? 'toolbar--between' : ''} ${className}`} {...props}>{children}</div>
)

// Feedback
export const Spinner = ({ sm, lg, className = '', ...props }) => (
  <div className={`spinner ${sm ? 'spinner--sm' : ''} ${lg ? 'spinner--lg' : ''} ${className}`} {...props} />
)

export const Alert = ({ children, success, error, warning, info, className = '', ...props }) => (
  <div className={`alert ${success ? 'alert--success' : ''} ${error ? 'alert--error' : ''} ${warning ? 'alert--warning' : ''} ${info ? 'alert--info' : ''} ${className}`} {...props}>{children}</div>
)

export const EmptyState = ({ children, className = '', ...props }) => (
  <div className={`empty-state ${className}`} {...props}>{children}</div>
)

export const LoadingState = ({ children, className = '', ...props }) => (
  <div className={`loading-state ${className}`} {...props}>{children}</div>
)

export const ErrorState = ({ children, className = '', ...props }) => (
  <div className={`error-state ${className}`} {...props}>{children}</div>
)

// Avatar
export const Avatar = ({ children, src, alt = '', sm, md, lg, className = '', ...props }) => (
  <div className={`avatar flex-center ${sm ? 'avatar--sm' : ''} ${md ? 'avatar--md' : ''} ${lg ? 'avatar--lg' : ''} ${className}`} {...props}>
    {src ? <img src={src} alt={alt} /> : children}
  </div>
)

// Divider
export const Divider = ({ className = '', ...props }) => (
  <hr className={`divider ${className}`} {...props} />
)

// Panel (floating)
export const Panel = ({ children, className = '', ...props }) => (
  <div className={`panel ${className}`} {...props}>{children}</div>
)

// Tabs
export const Tabs = ({ children, className = '', ...props }) => (
  <div className={`tabs ${className}`} {...props}>{children}</div>
)

export const Tab = ({ children, active, className = '', ...props }) => (
  <button className={`tab ${active ? 'tab--active' : ''} ${className}`} {...props}>{children}</button>
)

// Accordion
export const Accordion = ({ children, className = '', ...props }) => (
  <div className={`accordion ${className}`} {...props}>{children}</div>
)

export const AccordionItem = ({ children, expanded, className = '', ...props }) => (
  <div className={`accordion-item ${expanded ? 'accordion-item--expanded' : ''} ${className}`} {...props}>{children}</div>
)

export const AccordionHeader = ({ children, className = '', ...props }) => (
  <button className={`accordion-header ${className}`} {...props}>{children}</button>
)

export const AccordionContent = ({ children, className = '', ...props }) => (
  <div className={`accordion-content ${className}`} {...props}>{children}</div>
)

// Editor wrapper
export const EditorWrapper = ({ children, sm, lg, xl, className = '', ...props }) => (
  <div className={`editor-wrapper ${sm ? 'editor-wrapper--sm' : ''} ${lg ? 'editor-wrapper--lg' : ''} ${xl ? 'editor-wrapper--xl' : ''} ${className}`} {...props}>{children}</div>
)

// Progress
export const Progress = ({ value, max = 100, className = '', ...props }) => (
  <div className={`progress ${className}`} {...props}>
    <div className="progress-bar" style={{ width: `${(value / max) * 100}%` }} />
  </div>
)

// Icon wrapper
export const Icon = ({ children, sm, lg, className = '', ...props }) => (
  <span className={`icon ${sm ? 'icon--sm' : ''} ${lg ? 'icon--lg' : ''} ${className}`} {...props}>{children}</span>
)
