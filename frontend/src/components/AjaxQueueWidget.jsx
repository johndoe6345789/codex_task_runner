import React, { useState } from 'react'
import { useAjaxQueue } from '../contexts/AjaxQueueContext'
import './AjaxQueueWidget.scss'

// Simple inline SVG icons
const CloudSyncIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4s1.79-4 4-4h.71C7.37 7.69 9.48 6 12 6c3.04 0 5.5 2.46 5.5 5.5v.5H19c1.66 0 3 1.34 3 3s-1.34 3-3 3z"/>
    <path d="M12 10l-3 3h2v4h2v-4h2z"/>
  </svg>
)
const CheckIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
  </svg>
)
const ErrorIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
  </svg>
)
const PendingIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M6 2v6h.01L6 8.01 10 12l-4 4 .01.01H6V22h12v-5.99h-.01L18 16l-4-4 4-3.99-.01-.01H18V2H6zm10 14.5V20H8v-3.5l4-4 4 4zm-4-5l-4-4V4h8v3.5l-4 4z"/>
  </svg>
)
const ExpandMoreIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/>
  </svg>
)
const ExpandLessIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"/>
  </svg>
)
const CloseIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
  </svg>
)

export default function AjaxQueueWidget() {
  const { queue, pending, completed, failed, isVisible, setIsVisible, clearQueue } = useAjaxQueue()
  const [expanded, setExpanded] = useState(false)
  
  if (!isVisible && pending === 0) return null
  
  const total = pending + completed + failed
  const progress = total > 0 ? ((completed + failed) / total) * 100 : 0
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <span className="list-item-icon list-item-icon--success"><CheckIcon /></span>
      case 'error':
        return <span className="list-item-icon list-item-icon--error"><ErrorIcon /></span>
      default:
        return <span className="list-item-icon list-item-icon--pending"><PendingIcon /></span>
    }
  }
  
  const getElapsedTime = (startTime, endTime) => {
    const elapsed = (endTime || Date.now()) - startTime
    if (elapsed < 1000) return `${elapsed}ms`
    return `${(elapsed / 1000).toFixed(1)}s`
  }
  
  return (
    <div className="panel panel--fixed-br ajax-queue">
      {/* Header */}
      <div className="panel-header panel-header--clickable" onClick={() => setExpanded(!expanded)}>
        <div className={`ajax-queue-icon ${pending > 0 ? 'ajax-queue-icon--spinning' : ''}`}>
          <CloudSyncIcon />
          {pending > 0 && <span className="badge badge--warning">{pending > 99 ? '99+' : pending}</span>}
        </div>
        <span className="panel-title">AJAX Queue</span>
        <div className="ajax-queue-stats">
          {pending > 0 && <span className="ajax-queue-stat ajax-queue-stat--pending">{pending}</span>}
          {completed > 0 && <span className="ajax-queue-stat ajax-queue-stat--success">{completed}</span>}
          {failed > 0 && <span className="ajax-queue-stat ajax-queue-stat--error">{failed}</span>}
        </div>
        <button
          className="icon-btn icon-btn--sm"
          onClick={(e) => { e.stopPropagation(); setExpanded(!expanded) }}
        >
          {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </button>
        <button
          className="icon-btn icon-btn--sm"
          onClick={(e) => {
            e.stopPropagation()
            if (pending === 0) {
              clearQueue()
              setIsVisible(false)
            }
          }}
        >
          <CloseIcon />
        </button>
      </div>
      
      {/* Progress bar */}
      {pending > 0 && (
        <div className="progress progress--thin">
          <div className="progress__bar" style={{ width: `${progress}%` }} />
        </div>
      )}
      
      {/* Expanded queue list */}
      {expanded && (
        <div className="panel-body">
          {queue.slice().reverse().map((request) => (
            <div
              key={request.id}
              className={`list-item ${request.status === 'error' ? 'list-item--error' : ''} ${request.status !== 'pending' ? 'list-item--muted' : ''}`}
            >
              {getStatusIcon(request.status)}
              <div className="list-item-content">
                <div className="ajax-queue-item-label list-item-primary">
                  {request.label}
                  {request.progress && (
                    <span className="ajax-queue-item-progress">
                      {request.progress.current}/{request.progress.total}
                    </span>
                  )}
                </div>
                <div className="list-item-secondary">
                  <span>{getElapsedTime(request.startTime, request.endTime)}</span>
                  {request.error && (
                    <span className="ajax-queue-item-error" title={request.error}>
                      {' · '}{request.error}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
          {queue.length === 0 && (
            <div className="ajax-queue-empty">No recent requests</div>
          )}
        </div>
      )}
      
      {/* Summary when collapsed */}
      {!expanded && queue.length > 0 && (
        <div className="panel-footer ajax-queue-summary">
          {queue[queue.length - 1]?.label || 'Processing...'}
          {pending > 1 && ` (+${pending - 1} more)`}
        </div>
      )}
    </div>
  )
}
