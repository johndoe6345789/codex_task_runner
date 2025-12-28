// Atomic React Components
// Complete replacement for MUI - just CSS class wrappers

import React, { forwardRef } from 'react'

// ============================================================================
// 1. INPUTS - User interaction and form controls
// ============================================================================

export const Button = forwardRef(({ children, primary, secondary, outline, ghost, sm, lg, icon, loading, disabled, className = '', ...props }, ref) => (
  <button ref={ref} className={`btn ${primary ? 'btn--primary' : ''} ${secondary ? 'btn--secondary' : ''} ${outline ? 'btn--outline' : ''} ${ghost ? 'btn--ghost' : ''} ${sm ? 'btn--sm' : ''} ${lg ? 'btn--lg' : ''} ${icon ? 'btn--icon' : ''} ${loading ? 'btn--loading' : ''} ${className}`} disabled={disabled || loading} {...props}>{children}</button>
))

export const IconButton = forwardRef(({ children, sm, lg, className = '', ...props }, ref) => (
  <button ref={ref} className={`icon-btn ${sm ? 'icon-btn--sm' : ''} ${lg ? 'icon-btn--lg' : ''} ${className}`} {...props}>{children}</button>
))

export const Fab = forwardRef(({ children, primary, secondary, sm, extended, className = '', ...props }, ref) => (
  <button ref={ref} className={`fab ${primary ? 'fab--primary' : ''} ${secondary ? 'fab--secondary' : ''} ${sm ? 'fab--sm' : ''} ${extended ? 'fab--extended' : ''} ${className}`} {...props}>{children}</button>
))

export const Input = forwardRef(({ sm, md, lg, error, className = '', ...props }, ref) => (
  <input ref={ref} className={`input ${sm ? 'input--sm' : ''} ${md ? 'input--md' : ''} ${lg ? 'input--lg' : ''} ${error ? 'input--error' : ''} ${className}`} {...props} />
))

export const Textarea = forwardRef(({ error, className = '', ...props }, ref) => (
  <textarea ref={ref} className={`textarea ${error ? 'textarea--error' : ''} ${className}`} {...props} />
))

export const Select = forwardRef(({ children, sm, error, className = '', ...props }, ref) => (
  <select ref={ref} className={`select ${sm ? 'select--sm' : ''} ${error ? 'select--error' : ''} ${className}`} {...props}>{children}</select>
))

export const Checkbox = forwardRef(({ label, className = '', ...props }, ref) => (
  <label className={`checkbox ${className}`}>
    <input ref={ref} type="checkbox" className="checkbox-input" {...props} />
    <span className="checkbox-box" />
    {label && <span className="checkbox-label">{label}</span>}
  </label>
))

export const Radio = forwardRef(({ label, className = '', ...props }, ref) => (
  <label className={`radio ${className}`}>
    <input ref={ref} type="radio" className="radio-input" {...props} />
    <span className="radio-dot" />
    {label && <span className="radio-label">{label}</span>}
  </label>
))

export const Switch = forwardRef(({ label, className = '', ...props }, ref) => (
  <label className={`switch ${className}`}>
    <input ref={ref} type="checkbox" className="switch-input" {...props} />
    <span className="switch-track" />
    {label && <span className="switch-label">{label}</span>}
  </label>
))

export const Slider = forwardRef(({ className = '', ...props }, ref) => (
  <input ref={ref} type="range" className={`slider ${className}`} {...props} />
))

export const FormGroup = ({ children, row, className = '', ...props }) => (
  <div className={`form-group ${row ? 'form-group--row' : ''} ${className}`} {...props}>{children}</div>
)

export const FormLabel = ({ children, required, className = '', ...props }) => (
  <label className={`form-label ${required ? 'form-label--required' : ''} ${className}`} {...props}>{children}</label>
)

export const FormHelperText = ({ children, error, className = '', ...props }) => (
  <span className={`form-helper ${error ? 'form-helper--error' : ''} ${className}`} {...props}>{children}</span>
)

export const TextField = forwardRef(({ label, helperText, error, className = '', ...props }, ref) => (
  <div className={`text-field ${error ? 'text-field--error' : ''} ${className}`}>
    {label && <FormLabel>{label}</FormLabel>}
    <Input ref={ref} error={error} {...props} />
    {helperText && <FormHelperText error={error}>{helperText}</FormHelperText>}
  </div>
))

export const ToggleButton = forwardRef(({ children, selected, className = '', ...props }, ref) => (
  <button ref={ref} className={`toggle-btn ${selected ? 'toggle-btn--selected' : ''} ${className}`} {...props}>{children}</button>
))

export const ToggleButtonGroup = ({ children, className = '', ...props }) => (
  <div className={`toggle-btn-group ${className}`} {...props}>{children}</div>
)

// ============================================================================
// 2. DATA DISPLAY - Visual presentation of information
// ============================================================================

export const Avatar = ({ children, src, alt = '', sm, md, lg, xl, className = '', ...props }) => (
  <div className={`avatar flex-center ${sm ? 'avatar--sm' : ''} ${md ? 'avatar--md' : ''} ${lg ? 'avatar--lg' : ''} ${xl ? 'avatar--xl' : ''} ${className}`} {...props}>
    {src ? <img src={src} alt={alt} /> : children}
  </div>
)

export const AvatarGroup = ({ children, max, className = '', ...props }) => (
  <div className={`avatar-group ${className}`} {...props}>{children}</div>
)

export const Badge = ({ children, content, dot, overlap, color, className = '', ...props }) => (
  <span className={`badge-wrapper ${className}`} {...props}>
    {children}
    <span className={`badge ${dot ? 'badge--dot' : ''} ${overlap ? 'badge--overlap' : ''} ${color ? `badge--${color}` : ''}`}>{!dot && content}</span>
  </span>
)

export const Chip = ({ children, icon, onDelete, clickable, sm, success, error, warning, info, outline, className = '', ...props }) => (
  <span className={`chip ${clickable ? 'chip--clickable' : ''} ${sm ? 'chip--sm' : ''} ${success ? 'chip--success' : ''} ${error ? 'chip--error' : ''} ${warning ? 'chip--warning' : ''} ${info ? 'chip--info' : ''} ${outline ? 'chip--outline' : ''} ${className}`} {...props}>
    {icon && <span className="chip-icon">{icon}</span>}
    {children}
    {onDelete && <button className="chip-delete" onClick={onDelete}>×</button>}
  </span>
)

export const Divider = ({ vertical, className = '', ...props }) => (
  <hr className={`divider ${vertical ? 'divider--vertical' : ''} ${className}`} {...props} />
)

export const Icon = ({ children, sm, lg, color, className = '', ...props }) => (
  <span className={`icon ${sm ? 'icon--sm' : ''} ${lg ? 'icon--lg' : ''} ${color ? `icon--${color}` : ''} ${className}`} {...props}>{children}</span>
)

export const List = ({ children, dense, spaced, className = '', ...props }) => (
  <ul className={`list ${dense ? 'list--dense' : ''} ${spaced ? 'list--spaced' : ''} ${className}`} {...props}>{children}</ul>
)

export const ListItem = ({ children, clickable, selected, disabled, borderless, className = '', ...props }) => (
  <li className={`list-item ${clickable ? 'list-item--clickable' : ''} ${selected ? 'list-item--selected' : ''} ${disabled ? 'list-item--disabled' : ''} ${borderless ? 'list-item--borderless' : ''} ${className}`} {...props}>{children}</li>
)

export const ListItemButton = forwardRef(({ children, selected, className = '', ...props }, ref) => (
  <button ref={ref} className={`list-item-button ${selected ? 'list-item-button--selected' : ''} ${className}`} {...props}>{children}</button>
))

export const ListItemIcon = ({ children, className = '', ...props }) => (
  <span className={`list-item-icon ${className}`} {...props}>{children}</span>
)

export const ListItemText = ({ primary, secondary, className = '', ...props }) => (
  <div className={`list-item-text ${className}`} {...props}>
    {primary && <span className="list-item-title">{primary}</span>}
    {secondary && <span className="list-item-meta">{secondary}</span>}
  </div>
)

export const ListItemAvatar = ({ children, className = '', ...props }) => (
  <div className={`list-item-avatar ${className}`} {...props}>{children}</div>
)

export const ListSubheader = ({ children, className = '', ...props }) => (
  <li className={`list-subheader ${className}`} {...props}>{children}</li>
)

export const Table = ({ children, className = '', ...props }) => (
  <table className={`table ${className}`} {...props}>{children}</table>
)

export const TableHead = ({ children, className = '', ...props }) => (
  <thead className={`table-head ${className}`} {...props}>{children}</thead>
)

export const TableBody = ({ children, className = '', ...props }) => (
  <tbody className={`table-body ${className}`} {...props}>{children}</tbody>
)

export const TableFooter = ({ children, className = '', ...props }) => (
  <tfoot className={`table-footer ${className}`} {...props}>{children}</tfoot>
)

export const TableRow = ({ children, hover, selected, className = '', ...props }) => (
  <tr className={`table-row ${hover ? 'table-row--hover' : ''} ${selected ? 'table-row--selected' : ''} ${className}`} {...props}>{children}</tr>
)

export const TableCell = ({ children, header, align, className = '', ...props }) => {
  const Tag = header ? 'th' : 'td'
  return <Tag className={`table-cell ${align ? `table-cell--${align}` : ''} ${className}`} {...props}>{children}</Tag>
}

export const TableContainer = ({ children, className = '', ...props }) => (
  <div className={`table-container ${className}`} {...props}>{children}</div>
)

export const Tooltip = ({ children, title, placement = 'top', className = '', ...props }) => (
  <span className={`tooltip-wrapper ${className}`} data-tooltip={title} data-placement={placement} {...props}>{children}</span>
)

export const Typography = ({ children, variant, color, align, gutterBottom, noWrap, className = '', as, ...props }) => {
  const Tag = as || (variant === 'h1' || variant === 'h2' || variant === 'h3' || variant === 'h4' || variant === 'h5' || variant === 'h6' ? variant : 'p')
  return <Tag className={`typography ${variant ? `typography--${variant}` : ''} ${color ? `text-${color}` : ''} ${align ? `text-${align}` : ''} ${gutterBottom ? 'mb-md' : ''} ${noWrap ? 'truncate' : ''} ${className}`} {...props}>{children}</Tag>
}

// ============================================================================
// 3. FEEDBACK - Communicating status and results
// ============================================================================

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

export const Backdrop = ({ children, open, onClick, className = '', ...props }) => (
  open ? <div className={`backdrop ${className}`} onClick={onClick} {...props}>{children}</div> : null
)

export const Spinner = ({ sm, lg, className = '', ...props }) => (
  <div className={`spinner ${sm ? 'spinner--sm' : ''} ${lg ? 'spinner--lg' : ''} ${className}`} {...props} />
)

export const CircularProgress = Spinner // alias

export const LinearProgress = ({ value, indeterminate, className = '', ...props }) => (
  <div className={`progress ${indeterminate ? 'progress--indeterminate' : ''} ${className}`} {...props}>
    <div className="progress-bar" style={value !== undefined ? { width: `${value}%` } : undefined} />
  </div>
)

export const Progress = LinearProgress // alias

export const Skeleton = ({ variant = 'text', width, height, className = '', ...props }) => (
  <div className={`skeleton skeleton--${variant} ${className}`} style={{ width, height }} {...props} />
)

export const Snackbar = ({ children, open, anchorOrigin, className = '', ...props }) => (
  open ? <div className={`snackbar ${anchorOrigin?.vertical ? `snackbar--${anchorOrigin.vertical}` : ''} ${anchorOrigin?.horizontal ? `snackbar--${anchorOrigin.horizontal}` : ''} ${className}`} {...props}>{children}</div> : null
)

// ============================================================================
// 4. SURFACES - Structural and layout surfaces
// ============================================================================

export const Paper = ({ children, elevation = 1, square, className = '', ...props }) => (
  <div className={`paper paper--elevation-${elevation} ${square ? 'paper--square' : ''} ${className}`} {...props}>{children}</div>
)

export const Card = ({ children, clickable, raised, className = '', ...props }) => (
  <div className={`card ${clickable ? 'card--clickable' : ''} ${raised ? 'card--raised' : ''} ${className}`} {...props}>{children}</div>
)

export const CardHeader = ({ title, subheader, action, avatar, className = '', ...props }) => (
  <div className={`card-header ${className}`} {...props}>
    {avatar && <div className="card-header-avatar">{avatar}</div>}
    <div className="card-header-content">
      {title && <div className="card-header-title">{title}</div>}
      {subheader && <div className="card-header-subheader">{subheader}</div>}
    </div>
    {action && <div className="card-header-action">{action}</div>}
  </div>
)

export const CardContent = ({ children, className = '', ...props }) => (
  <div className={`card-content ${className}`} {...props}>{children}</div>
)

export const CardActions = ({ children, disableSpacing, className = '', ...props }) => (
  <div className={`card-actions ${disableSpacing ? 'card-actions--no-spacing' : ''} ${className}`} {...props}>{children}</div>
)

export const CardActionArea = forwardRef(({ children, className = '', ...props }, ref) => (
  <button ref={ref} className={`card-action-area ${className}`} {...props}>{children}</button>
))

export const CardMedia = ({ image, alt = '', height, className = '', ...props }) => (
  <div className={`card-media ${className}`} style={{ backgroundImage: `url(${image})`, height }} {...props} role="img" aria-label={alt} />
)

export const Accordion = ({ children, expanded, disabled, className = '', ...props }) => (
  <div className={`accordion ${expanded ? 'accordion--expanded' : ''} ${disabled ? 'accordion--disabled' : ''} ${className}`} {...props}>{children}</div>
)

export const AccordionSummary = forwardRef(({ children, expandIcon, className = '', ...props }, ref) => (
  <button ref={ref} className={`accordion-header ${className}`} {...props}>
    {children}
    {expandIcon && <span className="accordion-expand-icon">{expandIcon}</span>}
  </button>
))

export const AccordionDetails = ({ children, className = '', ...props }) => (
  <div className={`accordion-content ${className}`} {...props}>{children}</div>
)

export const AccordionActions = ({ children, className = '', ...props }) => (
  <div className={`accordion-actions ${className}`} {...props}>{children}</div>
)

export const AppBar = ({ children, position = 'fixed', color, className = '', ...props }) => (
  <header className={`app-bar app-bar--${position} ${color ? `app-bar--${color}` : ''} ${className}`} {...props}>{children}</header>
)

export const Toolbar = ({ children, dense, className = '', ...props }) => (
  <div className={`toolbar ${dense ? 'toolbar--dense' : ''} ${className}`} {...props}>{children}</div>
)

export const Drawer = ({ children, open, anchor = 'left', variant = 'temporary', onClose, className = '', ...props }) => (
  <>
    {variant === 'temporary' && open && <Backdrop open onClick={onClose} />}
    <aside className={`drawer drawer--${anchor} drawer--${variant} ${open ? 'drawer--open' : ''} ${className}`} {...props}>{children}</aside>
  </>
)

// ============================================================================
// 5. NAVIGATION - User flow and movement
// ============================================================================

export const Breadcrumbs = ({ children, separator = '/', className = '', ...props }) => (
  <nav className={`breadcrumbs ${className}`} aria-label="breadcrumb" {...props}>
    <ol className="breadcrumbs-list">
      {React.Children.map(children, (child, i) => (
        <li className="breadcrumbs-item">
          {i > 0 && <span className="breadcrumbs-separator">{separator}</span>}
          {child}
        </li>
      ))}
    </ol>
  </nav>
)

export const Link = forwardRef(({ children, underline = 'hover', color, className = '', ...props }, ref) => (
  <a ref={ref} className={`link link--underline-${underline} ${color ? `link--${color}` : ''} ${className}`} {...props}>{children}</a>
))

export const Menu = ({ children, open, anchorEl, onClose, className = '', ...props }) => (
  open ? (
    <>
      <Backdrop open onClick={onClose} className="backdrop--transparent" />
      <div className={`menu ${className}`} {...props}>{children}</div>
    </>
  ) : null
)

export const MenuItem = forwardRef(({ children, selected, disabled, className = '', ...props }, ref) => (
  <button ref={ref} className={`menu-item ${selected ? 'menu-item--selected' : ''} ${disabled ? 'menu-item--disabled' : ''} ${className}`} disabled={disabled} {...props}>{children}</button>
))

export const MenuList = ({ children, className = '', ...props }) => (
  <div className={`menu-list ${className}`} role="menu" {...props}>{children}</div>
)

export const Tabs = ({ children, value, onChange, variant, className = '', ...props }) => (
  <div className={`tabs ${variant ? `tabs--${variant}` : ''} ${className}`} role="tablist" {...props}>{children}</div>
)

export const Tab = forwardRef(({ children, label, icon, value, selected, disabled, className = '', ...props }, ref) => (
  <button ref={ref} className={`tab ${selected ? 'tab--active' : ''} ${disabled ? 'tab--disabled' : ''} ${className}`} role="tab" aria-selected={selected} disabled={disabled} {...props}>
    {icon && <span className="tab-icon">{icon}</span>}
    {label || children}
  </button>
))

export const Pagination = ({ count, page, onChange, size, className = '', ...props }) => (
  <nav className={`pagination ${size ? `pagination--${size}` : ''} ${className}`} {...props}>
    <button className="pagination-btn" disabled={page <= 1} onClick={() => onChange?.(page - 1)}>‹</button>
    {Array.from({ length: count }, (_, i) => (
      <button key={i + 1} className={`pagination-btn ${page === i + 1 ? 'pagination-btn--active' : ''}`} onClick={() => onChange?.(i + 1)}>{i + 1}</button>
    ))}
    <button className="pagination-btn" disabled={page >= count} onClick={() => onChange?.(page + 1)}>›</button>
  </nav>
)

export const Stepper = ({ children, activeStep, orientation = 'horizontal', className = '', ...props }) => (
  <div className={`stepper stepper--${orientation} ${className}`} {...props}>{children}</div>
)

export const Step = ({ children, active, completed, disabled, className = '', ...props }) => (
  <div className={`step ${active ? 'step--active' : ''} ${completed ? 'step--completed' : ''} ${disabled ? 'step--disabled' : ''} ${className}`} {...props}>{children}</div>
)

export const StepLabel = ({ children, icon, className = '', ...props }) => (
  <span className={`step-label ${className}`} {...props}>
    {icon && <span className="step-icon">{icon}</span>}
    {children}
  </span>
)

export const BottomNavigation = ({ children, value, onChange, className = '', ...props }) => (
  <nav className={`bottom-nav ${className}`} {...props}>{children}</nav>
)

export const BottomNavigationAction = forwardRef(({ label, icon, value, selected, className = '', ...props }, ref) => (
  <button ref={ref} className={`bottom-nav-action ${selected ? 'bottom-nav-action--selected' : ''} ${className}`} {...props}>
    {icon && <span className="bottom-nav-icon">{icon}</span>}
    {label && <span className="bottom-nav-label">{label}</span>}
  </button>
))

// ============================================================================
// 6. LAYOUT - Page and component structure
// ============================================================================

export const Box = forwardRef(({ children, component: Component = 'div', className = '', ...props }, ref) => (
  <Component ref={ref} className={className} {...props}>{children}</Component>
))

export const Container = ({ children, maxWidth, disableGutters, className = '', ...props }) => (
  <div className={`container ${maxWidth ? `container--${maxWidth}` : ''} ${disableGutters ? 'container--no-gutters' : ''} ${className}`} {...props}>{children}</div>
)

export const Grid = ({ children, container, item, xs, sm, md, lg, xl, spacing, direction, alignItems, justifyContent, className = '', ...props }) => (
  <div className={`${container ? 'grid-container' : ''} ${item ? 'grid-item' : ''} ${spacing ? `gap-${spacing}` : ''} ${direction ? `flex-${direction}` : ''} ${alignItems ? `items-${alignItems}` : ''} ${justifyContent ? `justify-${justifyContent}` : ''} ${xs ? `col-${xs}` : ''} ${sm ? `col-sm-${sm}` : ''} ${md ? `col-md-${md}` : ''} ${lg ? `col-lg-${lg}` : ''} ${className}`} {...props}>{children}</div>
)

export const Stack = ({ children, direction = 'column', spacing, alignItems, justifyContent, divider, className = '', ...props }) => (
  <div className={`stack ${direction === 'row' ? 'flex' : 'flex flex-col'} ${spacing ? `gap-${spacing}` : ''} ${alignItems ? `items-${alignItems}` : ''} ${justifyContent ? `justify-${justifyContent}` : ''} ${className}`} {...props}>
    {divider ? React.Children.toArray(children).flatMap((child, i) => i > 0 ? [divider, child] : [child]) : children}
  </div>
)

export const Flex = ({ children, col, row, center, between, around, evenly, start, end, wrap, inline, gap, className = '', ...props }) => (
  <div className={`${inline ? 'inline-flex' : 'flex'} ${col ? 'flex-col' : ''} ${row ? 'flex-row' : ''} ${center ? 'flex-center' : ''} ${between ? 'flex-between' : ''} ${around ? 'justify-around' : ''} ${evenly ? 'justify-evenly' : ''} ${start ? 'items-start' : ''} ${end ? 'items-end' : ''} ${wrap ? 'flex-wrap' : ''} ${gap ? `gap-${gap}` : ''} ${className}`} {...props}>{children}</div>
)

export const ImageList = ({ children, cols = 2, gap, className = '', ...props }) => (
  <div className={`image-list image-list--cols-${cols} ${gap ? `gap-${gap}` : ''} ${className}`} {...props}>{children}</div>
)

export const ImageListItem = ({ children, cols = 1, rows = 1, className = '', ...props }) => (
  <div className={`image-list-item ${className}`} style={{ gridColumn: `span ${cols}`, gridRow: `span ${rows}` }} {...props}>{children}</div>
)

export const ImageListItemBar = ({ title, subtitle, actionIcon, position = 'bottom', className = '', ...props }) => (
  <div className={`image-list-item-bar image-list-item-bar--${position} ${className}`} {...props}>
    <div className="image-list-item-bar-content">
      {title && <span className="image-list-item-bar-title">{title}</span>}
      {subtitle && <span className="image-list-item-bar-subtitle">{subtitle}</span>}
    </div>
    {actionIcon && <span className="image-list-item-bar-action">{actionIcon}</span>}
  </div>
)

// ============================================================================
// 7. UTILS - Low-level helpers and primitives
// ============================================================================

export const Modal = ({ children, open, onClose, className = '', ...props }) => (
  open ? (
    <div className={`modal ${className}`} {...props}>
      <Backdrop open onClick={onClose} />
      <div className="modal-content">{children}</div>
    </div>
  ) : null
)

export const Dialog = Modal // alias

export const DialogOverlay = ({ children, onClick, className = '', ...props }) => (
  <div className={`dialog-overlay ${className}`} onClick={onClick} {...props}>{children}</div>
)

export const DialogPanel = ({ children, sm, lg, xl, className = '', ...props }) => (
  <div className={`dialog-panel ${sm ? 'dialog-panel--sm' : ''} ${lg ? 'dialog-panel--lg' : ''} ${xl ? 'dialog-panel--xl' : ''} ${className}`} onClick={e => e.stopPropagation()} {...props}>{children}</div>
)

export const DialogHeader = ({ children, className = '', ...props }) => (
  <div className={`dialog-header ${className}`} {...props}>{children}</div>
)

export const DialogTitle = ({ children, className = '', ...props }) => (
  <h2 className={`dialog-title ${className}`} {...props}>{children}</h2>
)

export const DialogContent = ({ children, dividers, className = '', ...props }) => (
  <div className={`dialog-content ${dividers ? 'dialog-content--dividers' : ''} ${className}`} {...props}>{children}</div>
)

export const DialogActions = ({ children, className = '', ...props }) => (
  <div className={`dialog-footer ${className}`} {...props}>{children}</div>
)

export const Popover = ({ children, open, anchorEl, onClose, anchorOrigin, transformOrigin, className = '', ...props }) => (
  open ? (
    <>
      <Backdrop open onClick={onClose} className="backdrop--transparent" />
      <div className={`popover ${className}`} {...props}>{children}</div>
    </>
  ) : null
)

export const Collapse = ({ children, in: isIn, className = '', ...props }) => (
  <div className={`collapse ${isIn ? 'collapse--in' : ''} ${className}`} {...props}>{children}</div>
)

export const Fade = ({ children, in: isIn, className = '', ...props }) => (
  <div className={`fade ${isIn ? 'fade--in' : ''} ${className}`} {...props}>{children}</div>
)

export const Grow = ({ children, in: isIn, className = '', ...props }) => (
  <div className={`grow ${isIn ? 'grow--in' : ''} ${className}`} {...props}>{children}</div>
)

export const Slide = ({ children, in: isIn, direction = 'down', className = '', ...props }) => (
  <div className={`slide slide--${direction} ${isIn ? 'slide--in' : ''} ${className}`} {...props}>{children}</div>
)

export const Zoom = ({ children, in: isIn, className = '', ...props }) => (
  <div className={`zoom ${isIn ? 'zoom--in' : ''} ${className}`} {...props}>{children}</div>
)

export const ClickAwayListener = ({ children, onClickAway }) => {
  const ref = React.useRef(null)
  React.useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) onClickAway?.(e)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [onClickAway])
  return <div ref={ref}>{children}</div>
}

export const Portal = ({ children, container }) => {
  const [mounted, setMounted] = React.useState(false)
  React.useEffect(() => setMounted(true), [])
  if (!mounted) return null
  return React.createPortal(children, container || document.body)
}

// ============================================================================
// 8. ADDITIONAL ATOMS
// ============================================================================

export const Title = ({ children, page, card, truncate, className = '', as: Tag = 'h2', ...props }) => (
  <Tag className={`${page ? 'page-title' : ''} ${card ? 'card-title' : ''} ${truncate ? 'truncate' : ''} ${className}`} {...props}>{children}</Tag>
)

export const Subtitle = ({ children, className = '', ...props }) => (
  <p className={`page-subtitle ${className}`} {...props}>{children}</p>
)

export const Label = ({ children, className = '', ...props }) => (
  <span className={`label ${className}`} {...props}>{children}</span>
)

export const Text = ({ children, secondary, disabled, sm, xs, lg, mono, center, truncate, className = '', as: Tag = 'span', ...props }) => (
  <Tag className={`${secondary ? 'text-secondary' : ''} ${disabled ? 'text-disabled' : ''} ${sm ? 'text-sm' : ''} ${xs ? 'text-xs' : ''} ${lg ? 'text-lg' : ''} ${mono ? 'font-mono' : ''} ${center ? 'text-center' : ''} ${truncate ? 'truncate' : ''} ${className}`} {...props}>{children}</Tag>
)

export const StatBadge = ({ children, pending, success, error, info, className = '', ...props }) => (
  <span className={`stat-badge ${pending ? 'stat-badge--pending' : ''} ${success ? 'stat-badge--success' : ''} ${error ? 'stat-badge--error' : ''} ${info ? 'stat-badge--info' : ''} ${className}`} {...props}>{children}</span>
)

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

export const EmptyState = ({ children, icon, title, action, className = '', ...props }) => (
  <div className={`empty-state ${className}`} {...props}>
    {icon && <div className="empty-state-icon">{icon}</div>}
    {title && <div className="empty-state-title">{title}</div>}
    <div className="empty-state-content">{children}</div>
    {action && <div className="empty-state-action">{action}</div>}
  </div>
)

export const LoadingState = ({ children, className = '', ...props }) => (
  <div className={`loading-state ${className}`} {...props}>{children || <Spinner />}</div>
)

export const ErrorState = ({ children, className = '', ...props }) => (
  <div className={`error-state ${className}`} {...props}>{children}</div>
)

export const EditorWrapper = ({ children, sm, lg, xl, className = '', ...props }) => (
  <div className={`editor-wrapper ${sm ? 'editor-wrapper--sm' : ''} ${lg ? 'editor-wrapper--lg' : ''} ${xl ? 'editor-wrapper--xl' : ''} ${className}`} {...props}>{children}</div>
)

export const Panel = ({ children, className = '', ...props }) => (
  <div className={`panel ${className}`} {...props}>{children}</div>
)

export const AutoGrid = ({ children, sm, lg, gap, className = '', ...props }) => (
  <div className={`auto-grid ${sm ? 'auto-grid--sm' : ''} ${lg ? 'auto-grid--lg' : ''} ${gap ? `gap-${gap}` : ''} ${className}`} {...props}>{children}</div>
)
