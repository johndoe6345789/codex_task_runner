import React, { useState } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import { Send as SendIcon } from '@mui/icons-material'

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
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Create New Task
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Send a prompt to Codex to create a new coding task
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {success}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              multiline
              rows={6}
              label="Task Prompt"
              placeholder="Describe what you want Codex to do..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              sx={{ mb: 2 }}
              disabled={loading}
            />

            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <TextField
                label="Branch"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                size="small"
                sx={{ width: 200 }}
                disabled={loading}
              />
              <FormControl size="small" sx={{ width: 120 }}>
                <InputLabel>Best Of</InputLabel>
                <Select
                  value={bestOf}
                  label="Best Of"
                  onChange={(e) => setBestOf(e.target.value)}
                  disabled={loading}
                >
                  <MenuItem value={1}>1</MenuItem>
                  <MenuItem value={2}>2</MenuItem>
                  <MenuItem value={3}>3</MenuItem>
                  <MenuItem value={5}>5</MenuItem>
                </Select>
              </FormControl>
            </Box>

            <Button
              type="submit"
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
              disabled={loading || !prompt.trim()}
            >
              {loading ? 'Creating...' : 'Create Task'}
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="subtitle2" gutterBottom>
            Tips
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • Be specific about what you want Codex to implement<br />
            • Mention file paths if you know them<br />
            • Include any constraints or requirements<br />
            • Use "Best Of" &gt; 1 to generate multiple solutions and pick the best
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}
