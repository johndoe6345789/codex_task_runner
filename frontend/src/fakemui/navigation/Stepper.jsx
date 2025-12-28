import React from 'react'

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
