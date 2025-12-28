import React, { createContext, useContext, useState, useCallback, useRef } from 'react'

// AJAX Queue Context
const AjaxQueueContext = createContext({
  queue: [],
  pending: 0,
  completed: 0,
  failed: 0,
  addRequest: () => {},
  updateRequest: () => {},
  clearQueue: () => {},
  isVisible: false,
  setIsVisible: () => {},
})

export function useAjaxQueue() {
  return useContext(AjaxQueueContext)
}

// Helper to generate unique IDs
let requestIdCounter = 0
const generateId = () => `req_${++requestIdCounter}_${Date.now()}`

export function AjaxQueueProvider({ children }) {
  const [queue, setQueue] = useState([])
  const [isVisible, setIsVisible] = useState(false)
  const timeoutRef = useRef(null)
  
  // Add a new request to the queue
  const addRequest = useCallback((label, options = {}) => {
    const id = generateId()
    const request = {
      id,
      label,
      status: 'pending', // pending, success, error
      startTime: Date.now(),
      endTime: null,
      error: null,
      progress: options.progress || null, // { current, total }
      group: options.group || null, // group related requests
    }
    
    setQueue(prev => [...prev, request])
    setIsVisible(true)
    
    // Auto-hide after 3 seconds of no activity
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }
    
    return id
  }, [])
  
  // Update a request's status
  const updateRequest = useCallback((id, updates) => {
    setQueue(prev => prev.map(req => {
      if (req.id !== id) return req
      
      const updated = { ...req, ...updates }
      if (updates.status === 'success' || updates.status === 'error') {
        updated.endTime = Date.now()
      }
      return updated
    }))
    
    // Auto-clear completed requests after delay
    if (updates.status === 'success' || updates.status === 'error') {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
      timeoutRef.current = setTimeout(() => {
        setQueue(prev => {
          const stillPending = prev.some(r => r.status === 'pending')
          if (!stillPending) {
            // Clear old completed requests but keep recent ones briefly
            const cutoff = Date.now() - 2000
            const filtered = prev.filter(r => 
              r.status === 'pending' || (r.endTime && r.endTime > cutoff)
            )
            if (filtered.length === 0) {
              setIsVisible(false)
            }
            return filtered
          }
          return prev
        })
      }, 3000)
    }
  }, [])
  
  // Clear all completed/failed requests
  const clearQueue = useCallback(() => {
    setQueue(prev => prev.filter(r => r.status === 'pending'))
    const hasPending = queue.some(r => r.status === 'pending')
    if (!hasPending) {
      setIsVisible(false)
    }
  }, [queue])
  
  // Calculate stats
  const stats = queue.reduce((acc, req) => {
    if (req.status === 'pending') acc.pending++
    else if (req.status === 'success') acc.completed++
    else if (req.status === 'error') acc.failed++
    return acc
  }, { pending: 0, completed: 0, failed: 0 })
  
  const value = {
    queue,
    ...stats,
    addRequest,
    updateRequest,
    clearQueue,
    isVisible,
    setIsVisible,
  }
  
  return (
    <AjaxQueueContext.Provider value={value}>
      {children}
    </AjaxQueueContext.Provider>
  )
}

// Wrapper function to track fetch requests
export function useTrackedFetch() {
  const { addRequest, updateRequest } = useAjaxQueue()
  
  const trackedFetch = useCallback(async (url, options = {}, trackingOptions = {}) => {
    const label = trackingOptions.label || url.split('/').pop() || 'Request'
    const id = addRequest(label, trackingOptions)
    
    try {
      const response = await fetch(url, options)
      const data = await response.json()
      
      if (response.ok && (data.success !== false)) {
        updateRequest(id, { status: 'success' })
      } else {
        updateRequest(id, { 
          status: 'error', 
          error: data.error || data.message || 'Request failed' 
        })
      }
      
      return { response, data, id }
    } catch (error) {
      updateRequest(id, { status: 'error', error: error.message })
      throw error
    }
  }, [addRequest, updateRequest])
  
  return trackedFetch
}
