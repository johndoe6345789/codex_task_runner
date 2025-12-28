import React, { useState, useEffect, useContext } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Spinner,
  Alert,
  Divider,
  Paper,
  IconButton,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Snackbar,
} from '../fakemui'
import { NerdModeContext } from '../App'
import MarkdownRenderer from './MarkdownRenderer'
import Editor, { loader } from '@monaco-editor/react'

// Icons as SVG components
const ArrowBackIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
const ExpandMoreIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>
const CopyIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
const DownloadIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
const GitHubIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1.27a11 11 0 00-3.48 21.46c.55.09.73-.28.73-.55v-1.84c-3.03.64-3.67-1.46-3.67-1.46-.55-1.29-1.28-1.65-1.28-1.65-.92-.65.1-.65.1-.65 1.1 0 1.73 1.1 1.73 1.1.92 1.65 2.57 1.2 3.21.92a2.16 2.16 0 01.64-1.47c-2.47-.27-5.04-1.19-5.04-5.5 0-1.1.46-2.1 1.2-2.84a3.76 3.76 0 010-2.93s.91-.28 3.11 1.1c1.8-.49 3.7-.49 5.5 0 2.1-1.38 3.02-1.1 3.02-1.1a3.76 3.76 0 010 2.93c.83.74 1.2 1.74 1.2 2.94 0 4.21-2.57 5.13-5.04 5.4.45.37.82.92.82 2.02v3.03c0 .27.1.64.73.55A11 11 0 0012 1.27"/></svg>

// Register diff language with proper syntax highlighting
loader.init().then((monaco) => {
  // Register the diff language if not already registered
  if (!monaco.languages.getLanguages().some(({ id }) => id === 'gitdiff')) {
    monaco.languages.register({ id: 'gitdiff' })
    
    monaco.languages.setMonarchTokensProvider('gitdiff', {
      tokenizer: {
        root: [
          // File headers
          [/^diff --git.*$/, 'keyword'],
          [/^index [a-f0-9]+\.\.[a-f0-9]+.*$/, 'comment'],
          [/^---.*$/, 'keyword.deleted'],
          [/^\+\+\+.*$/, 'keyword.added'],
          // Hunk headers
          [/^@@.*@@.*$/, 'tag'],
          // Added lines
          [/^\+.*$/, 'string.added'],
          // Removed lines
          [/^-.*$/, 'string.deleted'],
          // Context lines
          [/^ .*$/, 'comment'],
          // New file mode
          [/^new file mode.*$/, 'keyword'],
          [/^deleted file mode.*$/, 'keyword'],
        ],
      },
    })

    // Define custom theme for diffs
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

export default function TaskDetail({ task, onBack, apiBase }) {
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

  if (loading) {
    return (
      <Box className="loading-container">
        <Spinner />
      </Box>
    )
  }

  return (
    <Box>
      <Button icon={<ArrowBackIcon />} onClick={onBack} className="back-button">
        Back to Tasks
      </Button>

      {error && (
        <Alert severity="error" className="error-alert">
          {error}
        </Alert>
      )}

      <Card className="task-card">
        <CardContent>
          <Typography variant="h5">
            {task?.title || detail?.title || 'Task Detail'}
          </Typography>
          <Box className="chip-row">
            <Chip>{task?.repo || 'No repo'}</Chip>
            <Chip outline>{task?.base_branch || 'main'}</Chip>
            {task?.pr_numbers?.map((pr) => (
              <Chip
                key={pr}
                color="success"
                icon={<GitHubIcon />}
              >
                PR #{pr}
              </Chip>
            ))}
          </Box>
          {nerdMode && (
            <Typography 
              variant="caption" 
              className="task-id mono"
            >
              ID: {taskId}
            </Typography>
          )}
        </CardContent>
      </Card>

      <Box className="tabs-container">
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Details" />
          <Tab label="Turns" />
          <Tab label="Patch" onClick={fetchPatch} />
        </Tabs>
      </Box>

      {tabValue === 0 && detail && (
        <Paper className="tab-panel">
          {nerdMode ? (
            <>
              <Typography variant="subtitle2">
                Raw Task Data
              </Typography>
              <Box className="editor-container">
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
              </Box>
            </>
          ) : (
            <Box>
              <Typography variant="h6">
                {detail.title || task?.title || 'No title'}
              </Typography>
              {(detail.description || detail.prompt) && (
                <MarkdownRenderer>
                  {detail.description || detail.prompt}
                </MarkdownRenderer>
              )}
              {detail.status && (
                <Chip className="status-chip">{detail.status}</Chip>
              )}
            </Box>
          )}
        </Paper>
      )}

      {tabValue === 1 && turns && (
        <Box>
          {nerdMode && (
            <Typography variant="subtitle2" className="mono">
              Current Turn: {turns.current_turn_id}
            </Typography>
          )}
          {Object.entries(turns.turn_mapping || {}).map(([turnId, turnData]) => (
            <Accordion key={turnId}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography className="turn-title">
                  {nerdMode ? `Turn: ${turnId.slice(0, 8)}...` : `Turn ${Object.keys(turns.turn_mapping || {}).indexOf(turnId) + 1}`}
                </Typography>
                {turnId === turns.current_turn_id && (
                  <Chip color="primary" className="current-chip">Current</Chip>
                )}
              </AccordionSummary>
              <AccordionDetails>
                <Box className="turn-actions">
                  <Button
                    variant="contained"
                    icon={<GitHubIcon />}
                    onClick={() => handleCreatePR(turnId)}
                  >
                    Create PR
                  </Button>
                  {nerdMode && (
                    <IconButton onClick={() => copyToClipboard(turnId)}>
                      <CopyIcon />
                    </IconButton>
                  )}
                </Box>
                {/* Turn content with markdown support */}
                {turnData?.prompt && (
                  <Box className="turn-section">
                    <Typography variant="subtitle2">Prompt</Typography>
                    <Paper className="turn-content">
                      <MarkdownRenderer>{turnData.prompt}</MarkdownRenderer>
                    </Paper>
                  </Box>
                )}
                {turnData?.response && !nerdMode && (
                  <Box className="turn-section">
                    <Typography variant="subtitle2">Response</Typography>
                    <Paper className="turn-content">
                      <MarkdownRenderer>{turnData.response}</MarkdownRenderer>
                    </Paper>
                  </Box>
                )}
                {nerdMode && (
                  <Box className="editor-container small">
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
                  </Box>
                )}
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      )}

      {tabValue === 2 && (
        <Paper className="tab-panel">
          {patch ? (
            <>
              <Box className="patch-header">
                <Box>
                  <Typography variant="subtitle2">
                    {patch.pr_title || 'Git Patch'}
                  </Typography>
                  <Typography variant="caption" className="text-secondary">
                    {patch.diff_lines} lines
                  </Typography>
                </Box>
                <Box className="patch-actions">
                  <IconButton onClick={() => copyToClipboard(patch.diff)}>
                    <CopyIcon />
                  </IconButton>
                  <IconButton onClick={downloadPatch}>
                    <DownloadIcon />
                  </IconButton>
                </Box>
              </Box>
              {(patch.pr_message || patch.description || patch.body) && (
                <Box className="patch-description">
                  <Typography variant="subtitle2" className="text-secondary">
                    Description
                  </Typography>
                  <MarkdownRenderer>{patch.pr_message || patch.description || patch.body}</MarkdownRenderer>
                </Box>
              )}
              <Box className="editor-container large">
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
              </Box>
            </>
          ) : patch === null ? (
            <Button onClick={fetchPatch}>Load Patch</Button>
          ) : (
            <Typography className="text-secondary">No patch data available</Typography>
          )}
        </Paper>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        message={snackbar.message}
      />
    </Box>
  )
}
