import React, { useState, useEffect, useContext } from 'react'
import { NerdModeContext } from '../App'
import MarkdownRenderer from './MarkdownRenderer'
import Editor, { loader } from '@monaco-editor/react'
import './TaskDetail.scss'

// Simple SVG icons (replace MUI icons)
const Icons = {
  ArrowBack: () => (
    <svg className="icon" viewBox="0 0 24 24" fill="currentColor">
      <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
    </svg>
  ),
  ExpandMore: () => (
    <svg className="icon" viewBox="0 0 24 24" fill="currentColor">
      <path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/>
    </svg>
  ),
  Copy: () => (
    <svg className="icon icon--sm" viewBox="0 0 24 24" fill="currentColor">
      <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
    </svg>
  ),
  Download: () => (
    <svg className="icon" viewBox="0 0 24 24" fill="currentColor">
      <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
    </svg>
  ),
  GitHub: () => (
    <svg className="icon icon--sm" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 1.27a11 11 0 00-3.48 21.46c.55.09.73-.28.73-.55v-1.84c-3.03.64-3.67-1.46-3.67-1.46-.55-1.29-1.28-1.65-1.28-1.65-.92-.65.1-.65.1-.65 1.1 0 1.73 1.1 1.73 1.1.92 1.65 2.57 1.2 3.21.92a2.16 2.16 0 01.64-1.47c-2.47-.27-5.04-1.19-5.04-5.5 0-1.1.46-2.1 1.2-2.84a3.76 3.76 0 010-2.93s.91-.28 3.11 1.1c1.8-.49 3.7-.49 5.5 0 2.1-1.38 3.02-1.1 3.02-1.1a3.76 3.76 0 010 2.93c.83.74 1.2 1.74 1.2 2.94 0 4.21-2.57 5.13-5.04 5.4.45.37.82.92.82 2.02v3.03c0 .27.1.64.73.55A11 11 0 0012 1.27"/>
    </svg>
  ),
}

// Register diff language with proper syntax highlighting
loader.init().then((monaco) => {
  if (!monaco.languages.getLanguages().some(({ id }) => id === 'gitdiff')) {
    monaco.languages.register({ id: 'gitdiff' })
    
    monaco.languages.setMonarchTokensProvider('gitdiff', {
      tokenizer: {
        root: [
          [/^diff --git.*$/, 'keyword'],
          [/^index [a-f0-9]+\.\.[a-f0-9]+.*$/, 'comment'],
          [/^---.*$/, 'keyword.deleted'],
          [/^\+\+\+.*$/, 'keyword.added'],
          [/^@@.*@@.*$/, 'tag'],
          [/^\+.*$/, 'string.added'],
          [/^-.*$/, 'string.deleted'],
          [/^ .*$/, 'comment'],
          [/^new file mode.*$/, 'keyword'],
          [/^deleted file mode.*$/, 'keyword'],
        ],
      },
    })

    monaco.editor.defineTheme('diff-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'string.added', foreground: '98c379', fontStyle: 'bold' },
        { token: 'string.deleted', foreground: 'e06c75', fontStyle: 'bold' },
        { token: 'keyword.added', foreground: '61afef' },
        { token: 'keyword.deleted', foreground: 'e06c75' },
        { token: 'keyword', foreground: 'c678dd' },
        { token: 'tag', foreground: '56b6c2', fontStyle: 'bold' },
        { token: 'comment', foreground: '5c6370' },
      ],
      colors: {},
    })
  }
})

// Simple Accordion component
function Accordion({ title, children, badge, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen)
  
  return (
    <div className={`accordion ${open ? 'accordion--open' : ''}`}>
      <div className="accordion__header" onClick={() => setOpen(!open)}>
        <div className="task-detail__turn-header">
          <span className="task-detail__turn-title">{title}</span>
          {badge}
        </div>
        <span className="accordion__icon"><Icons.ExpandMore /></span>
      </div>
      {open && <div className="accordion__content">{children}</div>}
    </div>
  )
}

export default function TaskDetailPlain({ task, onBack, apiBase }) {
  const { nerdMode } = useContext(NerdModeContext)
  const [detail, setDetail] = useState(null)
  const [turns, setTurns] = useState(null)
  const [patch, setPatch] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [tabValue, setTabValue] = useState(0)
  const [snackbar, setSnackbar] = useState({ open: false, message: '' })

  const taskId = task?.task_id || task?.id

  useEffect(() => {
    if (taskId) {
      fetchDetail()
      fetchTurns()
    }
  }, [taskId])

  const fetchDetail = async () => {
    try {
      const res = await fetch(`${apiBase}/tasks/${taskId}`)
      const data = await res.json()
      if (data.success) {
        setDetail(data.data)
      }
    } catch (err) {
      console.error('Failed to fetch detail:', err)
    }
  }

  const fetchTurns = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${apiBase}/tasks/${taskId}/turns`)
      const data = await res.json()
      if (data.success) {
        setTurns(data.data)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchPatch = async () => {
    try {
      const res = await fetch(`${apiBase}/tasks/${taskId}/patch`)
      const data = await res.json()
      if (data.success) {
        setPatch(data.data)
        setTabValue(2)
      } else {
        setError(data.data?.error || 'Failed to fetch patch')
      }
    } catch (err) {
      setError(err.message)
    }
  }

  const handleCreatePR = async (turnId) => {
    try {
      const res = await fetch(`${apiBase}/tasks/${taskId}/create-pr`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ turn_id: turnId }),
      })
      const data = await res.json()
      if (data.success) {
        setSnackbar({ open: true, message: 'PR created successfully!' })
        fetchDetail()
      } else {
        setSnackbar({ open: true, message: data.error || 'Failed to create PR' })
      }
    } catch (err) {
      setSnackbar({ open: true, message: err.message })
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setSnackbar({ open: true, message: 'Copied to clipboard!' })
  }

  const downloadPatch = () => {
    if (!patch?.diff) return
    const blob = new Blob([patch.diff], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${taskId}.patch`
    a.click()
    URL.revokeObjectURL(url)
  }

  // Auto-hide snackbar
  useEffect(() => {
    if (snackbar.open) {
      const timer = setTimeout(() => setSnackbar({ ...snackbar, open: false }), 3000)
      return () => clearTimeout(timer)
    }
  }, [snackbar.open])

  if (loading) {
    return (
      <div className="task-detail__loading">
        <div className="spinner spinner--lg"></div>
      </div>
    )
  }

  const tabs = ['Details', 'Turns', 'Patch']

  return (
    <div className="task-detail">
      {/* Back button */}
      <button className="btn btn--secondary task-detail__back-btn" onClick={onBack}>
        <Icons.ArrowBack />
        Back to Tasks
      </button>

      {/* Error alert */}
      {error && (
        <div className="alert alert--error" style={{ marginBottom: 'var(--spacing-md)' }}>
          {error}
        </div>
      )}

      {/* Header card */}
      <div className="card task-detail__header">
        <div className="card__content">
          <h2 className="task-detail__title">
            {task?.title || detail?.title || 'Task Detail'}
          </h2>
          <div className="task-detail__meta">
            <span className="chip">{task?.repo || 'No repo'}</span>
            <span className="chip chip--outlined">{task?.base_branch || 'main'}</span>
            {task?.pr_numbers?.map((pr) => (
              <span key={pr} className="chip chip--success">
                <Icons.GitHub /> PR #{pr}
              </span>
            ))}
          </div>
          {nerdMode && (
            <span className="task-detail__task-id">ID: {taskId}</span>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs task-detail__tabs">
        {tabs.map((label, idx) => (
          <button
            key={label}
            className={`tabs__tab ${tabValue === idx ? 'tabs__tab--active' : ''}`}
            onClick={() => {
              setTabValue(idx)
              if (idx === 2 && !patch) fetchPatch()
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Tab panels */}
      {tabValue === 0 && detail && (
        <div className="task-detail__panel">
          {nerdMode ? (
            <>
              <h4 className="task-detail__details-title">Raw Task Data</h4>
              <div className="task-detail__json-editor">
                <Editor
                  height="100%"
                  defaultLanguage="json"
                  value={JSON.stringify(detail, null, 2)}
                  theme="vs-dark"
                  options={{
                    readOnly: true,
                    minimap: { enabled: false },
                    fontSize: 12,
                    lineNumbers: 'on',
                    scrollBeyondLastLine: false,
                    wordWrap: 'on',
                    automaticLayout: true,
                  }}
                />
              </div>
            </>
          ) : (
            <>
              <h3 className="task-detail__details-title">
                {detail.title || task?.title || 'No title'}
              </h3>
              {(detail.description || detail.prompt) && (
                <MarkdownRenderer>
                  {detail.description || detail.prompt}
                </MarkdownRenderer>
              )}
              {detail.status && (
                <span className="chip" style={{ marginTop: 'var(--spacing-sm)' }}>
                  {detail.status}
                </span>
              )}
            </>
          )}
        </div>
      )}

      {tabValue === 1 && turns && (
        <div>
          {nerdMode && (
            <p className="task-detail__current-turn">
              Current Turn: {turns.current_turn_id}
            </p>
          )}
          {Object.entries(turns.turn_mapping || {}).map(([turnId, turnData], idx) => (
            <Accordion
              key={turnId}
              title={nerdMode ? `Turn: ${turnId.slice(0, 8)}...` : `Turn ${idx + 1}`}
              badge={
                turnId === turns.current_turn_id && (
                  <span className="chip chip--primary" style={{ marginRight: 'var(--spacing-sm)' }}>
                    Current
                  </span>
                )
              }
            >
              <div className="task-detail__turn-actions">
                <button
                  className="btn btn--primary btn--sm"
                  onClick={() => handleCreatePR(turnId)}
                >
                  <Icons.GitHub /> Create PR
                </button>
                {nerdMode && (
                  <button
                    className="icon-btn icon-btn--sm"
                    onClick={() => copyToClipboard(turnId)}
                  >
                    <Icons.Copy />
                  </button>
                )}
              </div>

              {turnData?.prompt && (
                <div className="task-detail__turn-section">
                  <p className="task-detail__turn-section-label">Prompt</p>
                  <div className="task-detail__turn-content">
                    <MarkdownRenderer>{turnData.prompt}</MarkdownRenderer>
                  </div>
                </div>
              )}

              {turnData?.response && !nerdMode && (
                <div className="task-detail__turn-section">
                  <p className="task-detail__turn-section-label">Response</p>
                  <div className="task-detail__turn-content">
                    <MarkdownRenderer>{turnData.response}</MarkdownRenderer>
                  </div>
                </div>
              )}

              {nerdMode && (
                <div className="task-detail__turn-json-editor">
                  <Editor
                    height="100%"
                    defaultLanguage="json"
                    value={JSON.stringify(turnData, null, 2)}
                    theme="vs-dark"
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      fontSize: 12,
                      lineNumbers: 'on',
                      scrollBeyondLastLine: false,
                      wordWrap: 'on',
                      automaticLayout: true,
                    }}
                  />
                </div>
              )}
            </Accordion>
          ))}
        </div>
      )}

      {tabValue === 2 && (
        <div className="task-detail__panel">
          {patch ? (
            <>
              <div className="task-detail__patch-header">
                <div className="task-detail__patch-info">
                  <h4>{patch.pr_title || 'Git Patch'}</h4>
                  <span>{patch.diff_lines} lines</span>
                </div>
                <div className="task-detail__patch-actions">
                  <button className="icon-btn" onClick={() => copyToClipboard(patch.diff)}>
                    <Icons.Copy />
                  </button>
                  <button className="icon-btn" onClick={downloadPatch}>
                    <Icons.Download />
                  </button>
                </div>
              </div>

              {(patch.pr_message || patch.description || patch.body) && (
                <div className="task-detail__patch-description">
                  <h5>Description</h5>
                  <MarkdownRenderer>
                    {patch.pr_message || patch.description || patch.body}
                  </MarkdownRenderer>
                </div>
              )}

              <div className="task-detail__editor-wrapper">
                <Editor
                  height="100%"
                  defaultLanguage="gitdiff"
                  value={patch.diff || 'No diff available'}
                  theme="diff-dark"
                  options={{
                    readOnly: true,
                    minimap: { enabled: true },
                    fontSize: 12,
                    lineNumbers: 'on',
                    scrollBeyondLastLine: false,
                    wordWrap: 'on',
                    automaticLayout: true,
                  }}
                />
              </div>
            </>
          ) : patch === null ? (
            <button className="btn btn--primary" onClick={fetchPatch}>
              Load Patch
            </button>
          ) : (
            <p style={{ color: 'var(--color-text-secondary)' }}>No patch data available</p>
          )}
        </div>
      )}

      {/* Snackbar */}
      {snackbar.open && (
        <div className="snackbar">{snackbar.message}</div>
      )}
    </div>
  )
}
