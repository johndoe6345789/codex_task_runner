import React, { useState, useEffect, useContext } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  CircularProgress,
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
} from '@mui/material'
import {
  ArrowBack as ArrowBackIcon,
  ExpandMore as ExpandMoreIcon,
  ContentCopy as CopyIcon,
  Download as DownloadIcon,
  GitHub as GitHubIcon,
} from '@mui/icons-material'
import { NerdModeContext } from '../App'
import MarkdownRenderer from './MarkdownRenderer'
import Editor from '@monaco-editor/react'

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
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Button startIcon={<ArrowBackIcon />} onClick={onBack} sx={{ mb: 2 }}>
        Back to Tasks
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            {task?.title || detail?.title || 'Task Detail'}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
            <Chip label={task?.repo || 'No repo'} size="small" />
            <Chip label={task?.base_branch || 'main'} size="small" variant="outlined" />
            {task?.pr_numbers?.map((pr) => (
              <Chip
                key={pr}
                label={`PR #${pr}`}
                size="small"
                color="success"
                icon={<GitHubIcon />}
              />
            ))}
          </Box>
          {nerdMode && (
            <Typography 
              variant="caption" 
              sx={{ fontFamily: 'monospace', color: 'text.disabled', display: 'block' }}
            >
              ID: {taskId}
            </Typography>
          )}
        </CardContent>
      </Card>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Details" />
          <Tab label="Turns" />
          <Tab label="Patch" onClick={fetchPatch} />
        </Tabs>
      </Box>

      {tabValue === 0 && detail && (
        <Paper sx={{ p: 2 }}>
          {nerdMode ? (
            <>
              <Typography variant="subtitle2" gutterBottom>
                Raw Task Data
              </Typography>
              <Box sx={{ borderRadius: 1, overflow: 'hidden', height: 400 }}>
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
              <Typography variant="h6" gutterBottom>
                {detail.title || task?.title || 'No title'}
              </Typography>
              {(detail.description || detail.prompt) && (
                <MarkdownRenderer>
                  {detail.description || detail.prompt}
                </MarkdownRenderer>
              )}
              {detail.status && (
                <Chip label={detail.status} size="small" sx={{ mt: 1 }} />
              )}
            </Box>
          )}
        </Paper>
      )}

      {tabValue === 1 && turns && (
        <Box>
          {nerdMode && (
            <Typography variant="subtitle2" gutterBottom sx={{ fontFamily: 'monospace' }}>
              Current Turn: {turns.current_turn_id}
            </Typography>
          )}
          {Object.entries(turns.turn_mapping || {}).map(([turnId, turnData]) => (
            <Accordion key={turnId}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography sx={{ flexGrow: 1 }}>
                  {nerdMode ? `Turn: ${turnId.slice(0, 8)}...` : `Turn ${Object.keys(turns.turn_mapping || {}).indexOf(turnId) + 1}`}
                </Typography>
                {turnId === turns.current_turn_id && (
                  <Chip label="Current" size="small" color="primary" sx={{ mr: 1 }} />
                )}
              </AccordionSummary>
              <AccordionDetails>
                <Box sx={{ mb: 2 }}>
                  <Button
                    variant="contained"
                    size="small"
                    startIcon={<GitHubIcon />}
                    onClick={() => handleCreatePR(turnId)}
                    sx={{ mr: 1 }}
                  >
                    Create PR
                  </Button>
                  {nerdMode && (
                    <IconButton size="small" onClick={() => copyToClipboard(turnId)}>
                      <CopyIcon fontSize="small" />
                    </IconButton>
                  )}
                </Box>
                {/* Turn content with markdown support */}
                {turnData?.prompt && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>Prompt</Typography>
                    <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                      <MarkdownRenderer>{turnData.prompt}</MarkdownRenderer>
                    </Paper>
                  </Box>
                )}
                {turnData?.response && !nerdMode && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>Response</Typography>
                    <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                      <MarkdownRenderer>{turnData.response}</MarkdownRenderer>
                    </Paper>
                  </Box>
                )}
                {nerdMode && (
                  <Box sx={{ borderRadius: 1, overflow: 'hidden', height: 300 }}>
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
        <Paper sx={{ p: 2 }}>
          {patch ? (
            <>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Box>
                  <Typography variant="subtitle2">
                    {patch.pr_title || 'Git Patch'}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {patch.diff_lines} lines
                  </Typography>
                </Box>
                <Box>
                  <IconButton onClick={() => copyToClipboard(patch.diff)}>
                    <CopyIcon />
                  </IconButton>
                  <IconButton onClick={downloadPatch}>
                    <DownloadIcon />
                  </IconButton>
                </Box>
              </Box>
              {(patch.pr_message || patch.description || patch.body) && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
                  <Typography variant="subtitle2" gutterBottom color="text.secondary">
                    Description
                  </Typography>
                  <MarkdownRenderer>{patch.pr_message || patch.description || patch.body}</MarkdownRenderer>
                </Box>
              )}
              <Box sx={{ borderRadius: 1, overflow: 'hidden', height: 500 }}>
                <Editor
                  height="100%"
                  defaultLanguage="diff"
                  value={patch.diff || 'No diff available'}
                  theme="vs-dark"
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
            <Typography color="text.secondary">No patch data available</Typography>
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
