import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton,
  Chip,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  List as ListIcon,
  Add as AddIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material'

import TaskList from './components/TaskList'
import TaskDetail from './components/TaskDetail'
import NewPrompt from './components/NewPrompt'
import UserInfo from './components/UserInfo'

const drawerWidth = 240

const API_BASE = import.meta.env.DEV ? '/api' : ''

export default function App() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [currentView, setCurrentView] = useState('tasks')
  const [selectedTask, setSelectedTask] = useState(null)
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetchUser()
  }, [])

  const fetchUser = async () => {
    try {
      const res = await fetch(`${API_BASE}/me`)
      const data = await res.json()
      if (data.success) {
        setUser(data.data)
      }
    } catch (err) {
      console.error('Failed to fetch user:', err)
    }
  }

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const handleNavigation = (view) => {
    setCurrentView(view)
    setSelectedTask(null)
    setMobileOpen(false)
  }

  const handleTaskSelect = (task) => {
    setSelectedTask(task)
    setCurrentView('taskDetail')
  }

  const drawer = (
    <Box>
      <Toolbar>
        <Typography variant="h6" noWrap sx={{ color: 'primary.main', fontWeight: 'bold' }}>
          Codex Runner
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            selected={currentView === 'tasks'}
            onClick={() => handleNavigation('tasks')}
          >
            <ListItemIcon><ListIcon /></ListItemIcon>
            <ListItemText primary="Tasks" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            selected={currentView === 'newPrompt'}
            onClick={() => handleNavigation('newPrompt')}
          >
            <ListItemIcon><AddIcon /></ListItemIcon>
            <ListItemText primary="New Task" />
          </ListItemButton>
        </ListItem>
      </List>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            selected={currentView === 'user'}
            onClick={() => handleNavigation('user')}
          >
            <ListItemIcon><PersonIcon /></ListItemIcon>
            <ListItemText primary="Profile" />
          </ListItemButton>
        </ListItem>
      </List>
      {user && (
        <Box sx={{ p: 2, mt: 'auto' }}>
          <Chip
            icon={<PersonIcon />}
            label={user.email || user.name || 'Connected'}
            size="small"
            color="primary"
            variant="outlined"
          />
        </Box>
      )}
    </Box>
  )

  const renderContent = () => {
    switch (currentView) {
      case 'tasks':
        return <TaskList onTaskSelect={handleTaskSelect} apiBase={API_BASE} />
      case 'taskDetail':
        return <TaskDetail task={selectedTask} onBack={() => handleNavigation('tasks')} apiBase={API_BASE} />
      case 'newPrompt':
        return <NewPrompt onSuccess={() => handleNavigation('tasks')} apiBase={API_BASE} />
      case 'user':
        return <UserInfo user={user} apiBase={API_BASE} />
      default:
        return <TaskList onTaskSelect={handleTaskSelect} apiBase={API_BASE} />
    }
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: 'background.paper',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {currentView === 'tasks' && 'Tasks'}
            {currentView === 'taskDetail' && 'Task Detail'}
            {currentView === 'newPrompt' && 'New Task'}
            {currentView === 'user' && 'Profile'}
          </Typography>
          <IconButton color="inherit" onClick={fetchUser}>
            <RefreshIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: '64px',
        }}
      >
        {renderContent()}
      </Box>
    </Box>
  )
}
