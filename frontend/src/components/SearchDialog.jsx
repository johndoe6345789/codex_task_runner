import React, { useState, useEffect, useCallback, useContext } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Typography,
  Box,
  Chip,
  CircularProgress,
  InputAdornment,
  Divider,
  Paper,
  IconButton,
} from '@mui/material'
import {
  Search as SearchIcon,
  Task as TaskIcon,
  Code as CodeIcon,
  Description as DescriptionIcon,
  Close as CloseIcon,
} from '@mui/icons-material'
import { LanguageContext } from '../main'

// Debounce hook
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value)
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)
    
    return () => clearTimeout(handler)
  }, [value, delay])
  
  return debouncedValue
}

export default function SearchDialog({ open, onClose, onTaskSelect, apiBase }) {
  const { t } = useContext(LanguageContext)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState({ tasks: [], code: [] })
  const [loading, setLoading] = useState(false)
  const [allTasks, setAllTasks] = useState([])
  
  const debouncedQuery = useDebounce(query, 300)
  
  // Fetch all tasks on open
  useEffect(() => {
    if (open && allTasks.length === 0) {
      fetchAllTasks()
    }
  }, [open])
  
  const fetchAllTasks = async () => {
    try {
      const res = await fetch(`${apiBase}/tasks?filter=all&limit=100`)
      const data = await res.json()
      if (data.success) {
        setAllTasks(data.data || [])
      }
    } catch (err) {
      console.error('Failed to fetch tasks:', err)
    }
  }
  
  // Search when query changes
  useEffect(() => {
    if (debouncedQuery.length < 2) {
      setResults({ tasks: [], code: [] })
      return
    }
    
    performSearch(debouncedQuery)
  }, [debouncedQuery, allTasks])
  
  const performSearch = async (searchQuery) => {
    setLoading(true)
    const lowerQuery = searchQuery.toLowerCase()
    
    // Search in tasks (title, description, prompt, repo)
    const taskResults = allTasks.filter(task => {
      const title = (task.title || '').toLowerCase()
      const description = (task.description || task.prompt || '').toLowerCase()
      const repo = (task.repo || '').toLowerCase()
      const taskId = (task.task_id || task.id || '').toLowerCase()
      
      return title.includes(lowerQuery) ||
             description.includes(lowerQuery) ||
             repo.includes(lowerQuery) ||
             taskId.includes(lowerQuery)
    }).slice(0, 10)
    
    // Search in code/patches (fetch patches for matching tasks)
    const codeResults = []
    
    // Search for code in patches of recent tasks
    for (const task of allTasks.slice(0, 20)) {
      try {
        const taskId = task.task_id || task.id
        const res = await fetch(`${apiBase}/tasks/${taskId}/patch`)
        const data = await res.json()
        
        if (data.success && data.data?.diff) {
          const diff = data.data.diff.toLowerCase()
          if (diff.includes(lowerQuery)) {
            // Find matching lines
            const lines = data.data.diff.split('\n')
            const matchingLines = lines
              .map((line, idx) => ({ line, idx }))
              .filter(({ line }) => line.toLowerCase().includes(lowerQuery))
              .slice(0, 3)
            
            if (matchingLines.length > 0) {
              codeResults.push({
                task,
                matches: matchingLines,
                totalMatches: lines.filter(l => l.toLowerCase().includes(lowerQuery)).length,
              })
            }
          }
        }
      } catch (err) {
        // Skip failed patch fetches
      }
      
      if (codeResults.length >= 5) break
    }
    
    setResults({ tasks: taskResults, code: codeResults })
    setLoading(false)
  }
  
  const handleSelect = (task) => {
    onTaskSelect(task)
    onClose()
    setQuery('')
  }
  
  const highlightMatch = (text, query) => {
    if (!query || query.length < 2) return text
    const lowerText = text.toLowerCase()
    const lowerQuery = query.toLowerCase()
    const idx = lowerText.indexOf(lowerQuery)
    
    if (idx === -1) return text
    
    return (
      <>
        {text.slice(0, idx)}
        <Box component="span" sx={{ bgcolor: 'warning.main', color: 'warning.contrastText', px: 0.5, borderRadius: 0.5 }}>
          {text.slice(idx, idx + query.length)}
        </Box>
        {text.slice(idx + query.length)}
      </>
    )
  }
  
  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { 
          minHeight: 400,
          maxHeight: '80vh',
        }
      }}
    >
      <DialogTitle sx={{ pb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
        <SearchIcon />
        <Typography variant="h6" sx={{ flexGrow: 1 }}>Search</Typography>
        <IconButton size="small" onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          fullWidth
          placeholder="Search tasks, code, patches..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="action" />
              </InputAdornment>
            ),
          }}
          sx={{ mb: 2 }}
        />
        
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress size={32} />
          </Box>
        )}
        
        {!loading && query.length >= 2 && (
          <Box>
            {/* Task Results */}
            {results.tasks.length > 0 && (
              <>
                <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                  <TaskIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                  Tasks ({results.tasks.length})
                </Typography>
                <List dense sx={{ mb: 2 }}>
                  {results.tasks.map((task) => (
                    <ListItem key={task.task_id || task.id} disablePadding>
                      <ListItemButton onClick={() => handleSelect(task)}>
                        <ListItemText
                          primary={highlightMatch(task.title || 'Untitled Task', query)}
                          secondary={
                            <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', mt: 0.5 }}>
                              <Chip label={task.repo || 'No repo'} size="small" variant="outlined" />
                              {(task.description || task.prompt) && (
                                <Typography variant="caption" color="text.secondary" noWrap sx={{ maxWidth: 300 }}>
                                  {highlightMatch((task.description || task.prompt).slice(0, 100), query)}
                                </Typography>
                              )}
                            </Box>
                          }
                        />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </>
            )}
            
            {/* Code Results */}
            {results.code.length > 0 && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                  <CodeIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                  Code Matches ({results.code.length})
                </Typography>
                <List dense>
                  {results.code.map(({ task, matches, totalMatches }) => (
                    <ListItem key={task.task_id || task.id} disablePadding>
                      <ListItemButton onClick={() => handleSelect(task)}>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="body2">
                                {task.title || 'Untitled Task'}
                              </Typography>
                              <Chip 
                                label={`${totalMatches} match${totalMatches > 1 ? 'es' : ''}`} 
                                size="small" 
                                color="primary" 
                                variant="outlined"
                              />
                            </Box>
                          }
                          secondary={
                            <Paper 
                              variant="outlined" 
                              sx={{ 
                                mt: 1, 
                                p: 1, 
                                bgcolor: 'background.default',
                                fontFamily: 'monospace',
                                fontSize: '0.75rem',
                                overflow: 'hidden',
                              }}
                            >
                              {matches.map(({ line, idx }) => (
                                <Box key={idx} sx={{ py: 0.25 }}>
                                  <Typography 
                                    component="span" 
                                    sx={{ 
                                      color: 'text.disabled', 
                                      mr: 1,
                                      fontSize: '0.7rem',
                                    }}
                                  >
                                    {idx + 1}
                                  </Typography>
                                  <Typography 
                                    component="span" 
                                    sx={{ 
                                      fontFamily: 'monospace',
                                      fontSize: '0.75rem',
                                      color: line.startsWith('+') ? 'success.main' : 
                                             line.startsWith('-') ? 'error.main' : 'text.primary',
                                    }}
                                  >
                                    {highlightMatch(line.slice(0, 80), query)}
                                    {line.length > 80 ? '...' : ''}
                                  </Typography>
                                </Box>
                              ))}
                            </Paper>
                          }
                        />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </>
            )}
            
            {/* No Results */}
            {results.tasks.length === 0 && results.code.length === 0 && (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography color="text.secondary">
                  No results found for "{query}"
                </Typography>
              </Box>
            )}
          </Box>
        )}
        
        {!loading && query.length < 2 && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography color="text.secondary">
              Type at least 2 characters to search
            </Typography>
            <Typography variant="caption" color="text.disabled" sx={{ mt: 1, display: 'block' }}>
              Search tasks by title, description, repo, or search in code patches
            </Typography>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  )
}
