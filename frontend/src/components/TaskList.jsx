import React, { useState, useEffect, useContext } from 'react'
import {
  Box,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  Grid,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  IconButton,
  Tooltip,
} from '@mui/material'
import {
  Refresh as RefreshIcon,
  OpenInNew as OpenInNewIcon,
  Archive as ArchiveIcon,
  Code as CodeIcon,
  ContentCopy as CopyIcon,
} from '@mui/icons-material'
import { NerdModeContext } from '../App'

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
    return 'default'
  }

  const getStatusLabel = (task) => {
    if (task.pr_numbers && task.pr_numbers.length > 0) {
      return `PR #${task.pr_numbers.join(', #')}`
    }
    return task.status || 'pending'
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
      <Box sx={{ mb: 3, display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Filter</InputLabel>
          <Select value={filter} label="Filter" onChange={(e) => setFilter(e.target.value)}>
            <MenuItem value="current">Current</MenuItem>
            <MenuItem value="archived">Archived</MenuItem>
            <MenuItem value="all">All</MenuItem>
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 80 }}>
          <InputLabel>Limit</InputLabel>
          <Select value={limit} label="Limit" onChange={(e) => setLimit(e.target.value)}>
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={20}>20</MenuItem>
            <MenuItem value={50}>50</MenuItem>
            <MenuItem value={100}>100</MenuItem>
          </Select>
        </FormControl>
        <IconButton onClick={fetchTasks} color="primary">
          <RefreshIcon />
        </IconButton>
        <Typography variant="body2" color="text.secondary">
          {tasks.length} tasks
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={2}>
        {tasks.map((task) => (
          <Grid item xs={12} md={6} lg={4} key={task.task_id || task.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': { bgcolor: 'action.hover' },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Chip
                    label={getStatusLabel(task)}
                    size="small"
                    color={getStatusColor(task)}
                  />
                  {task._alias && (
                    <Chip label={`#${task._alias}`} size="small" variant="outlined" />
                  )}
                </Box>
                <Typography variant="h6" component="div" gutterBottom noWrap>
                  {task.title || 'Untitled Task'}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {task.repo || 'No repo'}
                </Typography>
                {nerdMode && (
                  <Box sx={{ mt: 1 }}>
                    <Typography 
                      variant="caption" 
                      sx={{ 
                        fontFamily: 'monospace', 
                        color: 'text.disabled',
                        display: 'block',
                        fontSize: '0.65rem',
                        wordBreak: 'break-all'
                      }}
                    >
                      {task.task_id || task.id}
                    </Typography>
                  </Box>
                )}
                {!nerdMode && (
                  <Typography variant="caption" color="text.secondary">
                    {task.base_branch || 'main'}
                  </Typography>
                )}
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => onTaskSelect(task)}>
                  View
                </Button>
                <Tooltip title="Get Patch">
                  <IconButton
                    size="small"
                    onClick={() => window.open(`${apiBase}/tasks/${task.task_id || task.id}/patch`, '_blank')}
                  >
                    <CodeIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Archive">
                  <IconButton
                    size="small"
                    onClick={() => handleArchive(task.task_id || task.id)}
                  >
                    <ArchiveIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {tasks.length === 0 && !loading && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography color="text.secondary">No tasks found</Typography>
        </Box>
      )}
    </Box>
  )
}
