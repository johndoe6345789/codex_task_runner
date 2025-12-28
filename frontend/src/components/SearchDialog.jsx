import React, { useState, useEffect, useCallback, useContext } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Input,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Typography,
  Box,
  Chip,
  Spinner,
  Divider,
  Paper,
  IconButton,
  LinearProgress,
} from '../fakemui'
import { LanguageContext } from '../main'
import { useAjaxQueue } from '../contexts/AjaxQueueContext'

// Icons as SVG components
const SearchIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
const TaskIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
const CodeIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
const CloseIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>

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
  const { addRequest, updateRequest } = useAjaxQueue()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState({ tasks: [], code: [] })
  const [loading, setLoading] = useState(false)
  const [searching, setSearching] = useState(false)
  const [codeSearchProgress, setCodeSearchProgress] = useState(null) // { current, total }
  const [allTasks, setAllTasks] = useState([])
  const [tasksFetched, setTasksFetched] = useState(false)
  const [error, setError] = useState(null)
  
  const debouncedQuery = useDebounce(query, 400)
  
  // Fetch all tasks on open
  useEffect(() => {
    if (open && !tasksFetched) {
      fetchAllTasks()
    }
  }, [open, tasksFetched])
  
  // Reset when dialog closes
  useEffect(() => {
    if (!open) {
      setQuery('')
      setResults({ tasks: [], code: [] })
    }
  }, [open])
  
  const fetchAllTasks = async () => {
    setLoading(true)
    setError(null)
    const reqId = addRequest('Fetching tasks')
    try {
      const res = await fetch(`${apiBase}/tasks?filter=all&limit=100`)
      const data = await res.json()
      if (data.success) {
        setAllTasks(data.data || [])
        setTasksFetched(true)
        updateRequest(reqId, { status: 'success' })
      } else {
        setError('Failed to fetch tasks')
        updateRequest(reqId, { status: 'error', error: 'Failed to fetch' })
      }
    } catch (err) {
      console.error('Failed to fetch tasks:', err)
      setError(err.message)
      updateRequest(reqId, { status: 'error', error: err.message })
    } finally {
      setLoading(false)
    }
  }
  
  // Search when query changes
  useEffect(() => {
    if (debouncedQuery.length < 2) {
      setResults({ tasks: [], code: [] })
      return
    }
    
    if (allTasks.length > 0) {
      performSearch(debouncedQuery)
    }
  }, [debouncedQuery, allTasks])
  
  const performSearch = async (searchQuery) => {
    setLoading(true)
    setSearching(true)
    setError(null)
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
    
    // Show task results immediately
    setResults({ tasks: taskResults, code: [] })
    setLoading(false)
    
    // Now search code in patches - queue up AJAX requests
    const tasksWithPatches = allTasks.filter(t => 
      t.status === 'completed' || t.status === 'pr_created'
    ).slice(0, 20) // Limit to 20 to avoid too many requests
    
    if (tasksWithPatches.length === 0) {
      setSearching(false)
      return
    }
    
    setCodeSearchProgress({ current: 0, total: tasksWithPatches.length })
    const codeResults = []
    
    // Process in batches of 3 for better UX
    const batchSize = 3
    for (let i = 0; i < tasksWithPatches.length; i += batchSize) {
      const batch = tasksWithPatches.slice(i, i + batchSize)
      
      // Process batch in parallel
      const batchPromises = batch.map(async (task) => {
        const taskId = task.task_id || task.id
        const reqId = addRequest(`Searching ${task.title?.slice(0, 25) || taskId}...`, {
          progress: { current: i + 1, total: tasksWithPatches.length },
          group: 'codeSearch'
        })
        
        try {
          const res = await fetch(`${apiBase}/tasks/${taskId}/patch`)
          const data = await res.json()
          
          if (data.success && data.data?.patch) {
            const patch = data.data.patch
            const lines = patch.split('\n')
            const matches = []
            
            lines.forEach((line, idx) => {
              if (line.toLowerCase().includes(lowerQuery)) {
                matches.push({ line, idx })
              }
            })
            
            if (matches.length > 0) {
              updateRequest(reqId, { status: 'success' })
              return { task, matches: matches.slice(0, 3), totalMatches: matches.length }
            }
          }
          updateRequest(reqId, { status: 'success' })
          return null
        } catch (err) {
          updateRequest(reqId, { status: 'error', error: err.message })
          return null
        }
      })
      
      const batchResults = await Promise.all(batchPromises)
      const validResults = batchResults.filter(r => r !== null)
      
      if (validResults.length > 0) {
        codeResults.push(...validResults)
        // Update results progressively
        setResults(prev => ({ ...prev, code: [...codeResults] }))
      }
      
      setCodeSearchProgress({ current: Math.min(i + batchSize, tasksWithPatches.length), total: tasksWithPatches.length })
    }
    
    setSearching(false)
    setCodeSearchProgress(null)
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
        <span className="highlight">
          {text.slice(idx, idx + query.length)}
        </span>
        {text.slice(idx + query.length)}
      </>
    )
  }
  
  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      className="search-dialog"
    >
      <DialogTitle className="search-dialog-title">
        <SearchIcon />
        <Typography variant="h6" className="flex-grow">Search</Typography>
        <IconButton onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent className="search-dialog-content">
        <Input
          autoFocus
          placeholder="Search tasks, code, patches..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        
        {(loading || searching) && (
          <Box className="search-loading">
            <Box className="search-loading-row">
              <Spinner size="small" />
              <Typography variant="body2" className="text-secondary">
                {loading ? 'Loading tasks...' : 'Searching code...'}
              </Typography>
            </Box>
            {codeSearchProgress && (
              <Box className="search-progress">
                <LinearProgress 
                  value={(codeSearchProgress.current / codeSearchProgress.total) * 100}
                />
                <Typography variant="caption" className="text-secondary text-center">
                  Searching patches: {codeSearchProgress.current} / {codeSearchProgress.total}
                </Typography>
              </Box>
            )}
          </Box>
        )}
        
        {error && (
          <Box className="search-error">
            <Typography color="error">
              Error: {error}
            </Typography>
          </Box>
        )}
        
        {!loading && !error && query.length >= 2 && (
          <Box>
            {/* Task Results */}
            {results.tasks.length > 0 && (
              <>
                <Typography variant="subtitle2" className="text-secondary search-section-title">
                  <TaskIcon /> Tasks ({results.tasks.length})
                </Typography>
                <List className="search-results-list">
                  {results.tasks.map((task) => (
                    <ListItem key={task.task_id || task.id}>
                      <ListItemButton onClick={() => handleSelect(task)}>
                        <ListItemText
                          primary={highlightMatch(task.title || 'Untitled Task', query)}
                          secondary={
                            <Box className="search-result-meta">
                              <Chip outline>{task.repo || 'No repo'}</Chip>
                              {(task.description || task.prompt) && (
                                <Typography variant="caption" className="text-secondary search-result-desc">
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
                <Divider className="search-divider" />
                <Typography variant="subtitle2" className="text-secondary search-section-title">
                  <CodeIcon /> Code Matches ({results.code.length})
                </Typography>
                <List>
                  {results.code.map(({ task, matches, totalMatches }) => (
                    <ListItem key={task.task_id || task.id}>
                      <ListItemButton onClick={() => handleSelect(task)}>
                        <ListItemText
                          primary={
                            <Box className="search-code-title">
                              <Typography variant="body2">
                                {task.title || 'Untitled Task'}
                              </Typography>
                              <Chip outline color="primary">
                                {totalMatches} match{totalMatches > 1 ? 'es' : ''}
                              </Chip>
                            </Box>
                          }
                          secondary={
                            <Paper className="search-code-preview">
                              {matches.map(({ line, idx }) => (
                                <Box key={idx} className="search-code-line">
                                  <span className="line-number">{idx + 1}</span>
                                  <span className={`line-content ${line.startsWith('+') ? 'added' : line.startsWith('-') ? 'removed' : ''}`}>
                                    {highlightMatch(line.slice(0, 80), query)}
                                    {line.length > 80 ? '...' : ''}
                                  </span>
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
            {!searching && results.tasks.length === 0 && results.code.length === 0 && (
              <Box className="search-empty">
                <Typography className="text-secondary">
                  No results found for "{query}"
                </Typography>
              </Box>
            )}
          </Box>
        )}
        
        {!loading && !error && query.length < 2 && (
          <Box className="search-empty">
            <Typography className="text-secondary">
              Type at least 2 characters to search
            </Typography>
            <Typography variant="caption" className="text-disabled">
              Search tasks by title, description, repo
            </Typography>
            {allTasks.length > 0 && (
              <Typography variant="caption" className="text-disabled">
                {allTasks.length} tasks loaded
              </Typography>
            )}
          </Box>
        )}
      </DialogContent>
    </Dialog>
  )
}
