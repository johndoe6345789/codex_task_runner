import React, { useState } from 'react'
import './NewPrompt.scss'

const SendIcon = () => (
  <svg className="icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
  </svg>
)

export default function NewPrompt({ onSuccess, apiBase }) {
  const [prompt, setPrompt] = useState('')
  const [branch, setBranch] = useState('main')
  const [bestOf, setBestOf] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const res = await fetch(`${apiBase}/prompt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt_text: prompt,
          branch,
          best_of: bestOf,
        }),
      })
      const data = await res.json()
      if (data.success) {
        setSuccess('Task created successfully!')
        setPrompt('')
        setTimeout(() => onSuccess?.(), 2000)
      } else {
        setError(data.error || 'Failed to create task')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="new-prompt">
      <div className="card">
        <div className="card__content">
          <h2 className="new-prompt__title">Create New Task</h2>
          <p className="new-prompt__subtitle">
            Send a prompt to Codex to create a new coding task
          </p>

          {error && <div className="alert alert--error mb-md">{error}</div>}
          {success && <div className="alert alert--success mb-md">{success}</div>}

          <form onSubmit={handleSubmit} className="new-prompt__form">
            <div className="form-group">
              <label className="form-group__label">Task Prompt</label>
              <textarea
                className="textarea"
                rows={6}
                placeholder="Describe what you want Codex to do..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="new-prompt__row">
              <div className="form-group">
                <label className="form-group__label">Branch</label>
                <input
                  type="text"
                  className="input input--sm"
                  value={branch}
                  onChange={(e) => setBranch(e.target.value)}
                  disabled={loading}
                />
              </div>
              <div className="form-group">
                <label className="form-group__label">Best Of</label>
                <select
                  className="select select--sm"
                  value={bestOf}
                  onChange={(e) => setBestOf(Number(e.target.value))}
                  disabled={loading}
                >
                  <option value={1}>1</option>
                  <option value={2}>2</option>
                  <option value={3}>3</option>
                  <option value={5}>5</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              className="btn btn--primary btn--lg"
              disabled={loading || !prompt.trim()}
            >
              {loading ? <span className="spinner spinner--sm" /> : <SendIcon />}
              {loading ? 'Creating...' : 'Create Task'}
            </button>
          </form>
        </div>
      </div>

      <div className="card" style={{ marginTop: 'var(--spacing-lg)' }}>
        <div className="card__content">
          <div className="new-prompt__tips">
            <h4>Tips</h4>
            <p>
              • Be specific about what you want Codex to implement<br />
              • Mention file paths if you know them<br />
              • Include any constraints or requirements<br />
              • Use "Best Of" &gt; 1 to generate multiple solutions and pick the best
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
