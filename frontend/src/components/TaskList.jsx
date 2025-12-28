import React, { useState, useEffect, useContext } from 'react'
import { NerdModeContext } from '../App'
import MarkdownRenderer from './MarkdownRenderer'

const Icons = {
  Refresh: () => (
    <svg className="icon" viewBox="0 0 24 24" fill="currentColor">
      <path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0112 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
    </svg>
  ),
  Code: () => (
    <svg className="icon icon--sm" viewBox="0 0 24 24" fill="currentColor">
      <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
    </svg>
  ),
  Archive: () => (
    <svg className="icon icon--sm" viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.54 5.23l-1.39-1.68C18.88 3.21 18.47 3 18 3H6c-.47 0-.88.21-1.16.55L3.46 5.23C3.17 5.57 3 6.02 3 6.5V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6.5c0-.48-.17-.93-.46-1.27zM12 17.5L6.5 12H10v-2h4v2h3.5L12 17.5zM5.12 5l.81-1h12l.94 1H5.12z"/>
    </svg>
  ),
}

export default function TaskList({ onTaskSelect, apiBase }) {
  const { nerdMode } = useContext(NerdModeContext)
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('current')
  const [limit, setLimit] = useState(20)

  useEffect(() => {
    fetchTasks()
  }, [filter, limit])

  const fetchTasks = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${apiBase}/tasks?filter=${filter}&limit=${limit}`)
      const data = await res.json()
      if (data.success) {
        setTasks(data.data || [])
      } else {
        setError(data.error || 'Failed to fetch tasks')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleArchive = async (taskId) => {
    try {
      const res = await fetch(`${apiBase}/tasks/${taskId}/archive`, { method: 'POST' })
      const data = await res.json()
      if (data.success) {
        fetchTasks()
      }
    } catch (err) {
      console.error('Archive failed:', err)
    }
  }

  const getStatusColor = (task) => {
    if (task.pr_numbers && task.pr_numbers.length > 0) return 'success'
    if (task.status === 'completed') return 'success'
    if (task.status === 'running') return 'warning'
    return ''
  }

  const getStatusLabel = (task) => {
    if (task.pr_numbers && task.pr_numbers.length > 0) {
      return `PR #${task.pr_numbers.join(', #')}`
    }
    return task.status || 'pending'
  }

  if (loading) {
    return (
      <div className="task-list__loading">
        <div className="spinner spinner--lg" />
      </div>
    )
  }

  return (
    <div className="task-list">
      <div className="task-list__toolbar">
        <div className="form-group">
          <select
            className="select"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="current">Current</option>
            <option value="archived">Archived</option>
            <option value="all">All</option>
          </select>
        </div>
        <div className="form-group">
          <select
            className="select"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
          >
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </div>
        <button className="icon-btn" onClick={fetchTasks} title="Refresh">
          <Icons.Refresh />
        </button>
        <span className="task-list__count">{tasks.length} tasks</span>
      </div>

      {error && <div className="alert alert--error mb-md">{error}</div>}

      <div className="task-list__grid">
        {tasks.map((task) => (
          <div className="card task-card" key={task.task_id || task.id}>
            <div className="card__content" style={{ flex: 1 }}>
              <div className="task-card__header">
                <span className={`chip chip--${getStatusColor(task)}`}>
                  {getStatusLabel(task)}
                </span>
                {task._alias && (
                  <span className="chip chip--outlined">#{task._alias}</span>
                )}
              </div>
              <h3 className="task-card__title">{task.title || 'Untitled Task'}</h3>
              {(task.description || task.prompt) && (
                <div className="task-card__description">
                  <MarkdownRenderer>
                    {(task.description || task.prompt).slice(0, 200)}
                    {(task.description || task.prompt).length > 200 ? '...' : ''}
                  </MarkdownRenderer>
                </div>
              )}
              <p className="task-card__repo">{task.repo || 'No repo'}</p>
              {nerdMode ? (
                <p className="task-card__id">{task.task_id || task.id}</p>
              ) : (
                <span className="task-card__branch">{task.base_branch || 'main'}</span>
              )}
            </div>
            <div className="card__actions">
              <button className="btn btn--sm btn--secondary" onClick={() => onTaskSelect(task)}>
                View
              </button>
              <button
                className="icon-btn icon-btn--sm"
                onClick={() => window.open(`${apiBase}/tasks/${task.task_id || task.id}/patch`, '_blank')}
                title="Get Patch"
              >
                <Icons.Code />
              </button>
              <button
                className="icon-btn icon-btn--sm"
                onClick={() => handleArchive(task.task_id || task.id)}
                title="Archive"
              >
                <Icons.Archive />
              </button>
            </div>
          </div>
        ))}
      </div>

      {tasks.length === 0 && !loading && (
        <div className="task-list__empty">
          <p>No tasks found</p>
        </div>
      )}
    </div>
  )
}
