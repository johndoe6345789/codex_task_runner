import React, { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Collapse,
  LinearProgress,
  Chip,
  Tooltip,
  Fade,
  Badge,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material'
import {
  CloudSync as CloudSyncIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  HourglassEmpty as PendingIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Close as CloseIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material'
import { useAjaxQueue } from '../contexts/AjaxQueueContext'

export default function AjaxQueueWidget() {
  const { queue, pending, completed, failed, isVisible, setIsVisible, clearQueue } = useAjaxQueue()
  const [expanded, setExpanded] = useState(false)
  
  // Don't render if not visible and no pending requests
  if (!isVisible && pending === 0) return null
  
  const total = pending + completed + failed
  const progress = total > 0 ? ((completed + failed) / total) * 100 : 0
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon fontSize="small" color="success" />
      case 'error':
        return <ErrorIcon fontSize="small" color="error" />
      default:
        return <PendingIcon fontSize="small" color="action" sx={{ animation: 'pulse 1s infinite' }} />
    }
  }
  
  const getElapsedTime = (startTime, endTime) => {
    const elapsed = (endTime || Date.now()) - startTime
    if (elapsed < 1000) return `${elapsed}ms`
    return `${(elapsed / 1000).toFixed(1)}s`
  }
  
  return (
    <Fade in={isVisible || pending > 0}>
      <Paper
        elevation={6}
        sx={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          minWidth: 280,
          maxWidth: 400,
          zIndex: 1300,
          overflow: 'hidden',
          borderRadius: 2,
        }}
      >
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            p: 1.5,
            bgcolor: 'primary.dark',
            color: 'primary.contrastText',
            cursor: 'pointer',
          }}
          onClick={() => setExpanded(!expanded)}
        >
          <Badge badgeContent={pending} color="warning" max={99}>
            <CloudSyncIcon 
              sx={{ 
                animation: pending > 0 ? 'spin 2s linear infinite' : 'none',
                '@keyframes spin': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' },
                },
              }} 
            />
          </Badge>
          <Typography variant="subtitle2" sx={{ flexGrow: 1 }}>
            AJAX Queue
          </Typography>
          <Box sx={{ display: 'flex', gap: 0.5, mr: 1 }}>
            {pending > 0 && (
              <Chip 
                label={pending} 
                size="small" 
                color="warning" 
                sx={{ height: 20, '& .MuiChip-label': { px: 0.75 } }}
              />
            )}
            {completed > 0 && (
              <Chip 
                label={completed} 
                size="small" 
                color="success" 
                sx={{ height: 20, '& .MuiChip-label': { px: 0.75 } }}
              />
            )}
            {failed > 0 && (
              <Chip 
                label={failed} 
                size="small" 
                color="error" 
                sx={{ height: 20, '& .MuiChip-label': { px: 0.75 } }}
              />
            )}
          </Box>
          <IconButton 
            size="small" 
            sx={{ color: 'inherit' }}
            onClick={(e) => {
              e.stopPropagation()
              setExpanded(!expanded)
            }}
          >
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
          <IconButton 
            size="small" 
            sx={{ color: 'inherit' }}
            onClick={(e) => {
              e.stopPropagation()
              if (pending === 0) {
                clearQueue()
                setIsVisible(false)
              }
            }}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        </Box>
        
        {/* Progress bar */}
        {pending > 0 && (
          <LinearProgress 
            variant="determinate" 
            value={progress}
            sx={{ height: 3 }}
          />
        )}
        
        {/* Expanded queue list */}
        <Collapse in={expanded}>
          <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
            <List dense sx={{ py: 0 }}>
              {queue.slice().reverse().map((request) => (
                <ListItem
                  key={request.id}
                  sx={{
                    borderBottom: '1px solid',
                    borderColor: 'divider',
                    opacity: request.status === 'pending' ? 1 : 0.7,
                    bgcolor: request.status === 'error' ? 'error.dark' : 'transparent',
                    '&:hover': { bgcolor: 'action.hover' },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    {getStatusIcon(request.status)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="body2" noWrap sx={{ maxWidth: 180 }}>
                          {request.label}
                        </Typography>
                        {request.progress && (
                          <Chip
                            label={`${request.progress.current}/${request.progress.total}`}
                            size="small"
                            variant="outlined"
                            sx={{ height: 18, '& .MuiChip-label': { px: 0.5, fontSize: '0.65rem' } }}
                          />
                        )}
                      </Box>
                    }
                    secondary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="caption" color="text.secondary">
                          {getElapsedTime(request.startTime, request.endTime)}
                        </Typography>
                        {request.error && (
                          <Typography variant="caption" color="error" noWrap sx={{ maxWidth: 150 }}>
                            {request.error}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
            {queue.length === 0 && (
              <Box sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">
                  No recent requests
                </Typography>
              </Box>
            )}
          </Box>
        </Collapse>
        
        {/* Summary when collapsed */}
        {!expanded && queue.length > 0 && (
          <Box sx={{ px: 2, py: 1 }}>
            <Typography variant="caption" color="text.secondary" noWrap>
              {queue[queue.length - 1]?.label || 'Processing...'}
              {pending > 1 && ` (+${pending - 1} more)`}
            </Typography>
          </Box>
        )}
        
        {/* Add keyframes for pulse animation */}
        <style>{`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
          }
        `}</style>
      </Paper>
    </Fade>
  )
}
