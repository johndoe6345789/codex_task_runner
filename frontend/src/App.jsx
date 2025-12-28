import React, { useState, useEffect, createContext, useContext } from 'react'
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
  Switch,
  FormControlLabel,
  Tooltip,
  Menu,
  MenuItem,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  List as ListIcon,
  Add as AddIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Refresh as RefreshIcon,
  Code as CodeIcon,
  Palette as PaletteIcon,
  Check as CheckIcon,
  Language as LanguageIcon,
  Search as SearchIcon,
} from '@mui/icons-material'

// Nerd mode context
export const NerdModeContext = createContext({ nerdMode: false, setNerdMode: () => {} })

import TaskList from './components/TaskList'
import TaskDetail from './components/TaskDetail'
import NewPrompt from './components/NewPrompt'
import UserInfo from './components/UserInfo'
import SearchDialog from './components/SearchDialog'
import { themes, themeKeys } from './themes'
import { languages, languageKeys } from './i18n'
import { ThemeContext, LanguageContext } from './main'

const drawerWidth = 240

const API_BASE = import.meta.env.DEV ? '/api' : ''

export default function App() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [currentView, setCurrentView] = useState('tasks')
  const [selectedTask, setSelectedTask] = useState(null)
  const [user, setUser] = useState(null)
  const [nerdMode, setNerdMode] = useState(() => {
    const saved = localStorage.getItem('nerdMode')
    return saved ? JSON.parse(saved) : false
  })
  const [themeMenuAnchor, setThemeMenuAnchor] = useState(null)
  const [langMenuAnchor, setLangMenuAnchor] = useState(null)
  const [searchOpen, setSearchOpen] = useState(false)
  const { themeName, setThemeName } = useContext(ThemeContext)
  const { language, setLanguage, t } = useContext(LanguageContext)

  // Keyboard shortcut for search (Cmd/Ctrl + K)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setSearchOpen(true)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  useEffect(() => {
    localStorage.setItem('nerdMode', JSON.stringify(nerdMode))
  }, [nerdMode])

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
            <ListItemText primary={t('tasks')} />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            selected={currentView === 'newPrompt'}
            onClick={() => handleNavigation('newPrompt')}
          >
            <ListItemIcon><AddIcon /></ListItemIcon>
            <ListItemText primary={t('newTask')} />
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
            <ListItemText primary={t('profile')} />
          </ListItemButton>
        </ListItem>
      </List>
      <Divider />
      <Box sx={{ p: 2 }}>
        <Tooltip title="Show technical details, raw JSON, and IDs">
          <FormControlLabel
            control={
              <Switch
                checked={nerdMode}
                onChange={(e) => setNerdMode(e.target.checked)}
                size="small"
                color="primary"
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <CodeIcon fontSize="small" />
                <Typography variant="body2">{t('nerdMode')}</Typography>
              </Box>
            }
          />
        </Tooltip>
      </Box>
      <Box sx={{ px: 2, pb: 1 }}>
        <ListItemButton
          onClick={(e) => setThemeMenuAnchor(e.currentTarget)}
          sx={{ borderRadius: 1, py: 0.5 }}
        >
          <ListItemIcon sx={{ minWidth: 32 }}>
            <PaletteIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText 
            primary={
              <Typography variant="body2">
                {t('theme')}: {themes[themeName]?.name || 'Dark'}
              </Typography>
            } 
          />
        </ListItemButton>
        <Menu
          anchorEl={themeMenuAnchor}
          open={Boolean(themeMenuAnchor)}
          onClose={() => setThemeMenuAnchor(null)}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          transformOrigin={{ vertical: 'top', horizontal: 'left' }}
        >
          {themeKeys.map((key) => (
            <MenuItem
              key={key}
              selected={themeName === key}
              onClick={() => {
                setThemeName(key)
                setThemeMenuAnchor(null)
              }}
              sx={{ minWidth: 150 }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, width: '100%' }}>
                <Box
                  sx={{
                    width: 16,
                    height: 16,
                    borderRadius: '50%',
                    bgcolor: themes[key].theme.palette.primary.main,
                    border: '2px solid',
                    borderColor: themes[key].theme.palette.background.paper,
                  }}
                />
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  {themes[key].name}
                </Typography>
                {themeName === key && <CheckIcon fontSize="small" color="primary" />}
              </Box>
            </MenuItem>
          ))}
        </Menu>
      </Box>
      <Box sx={{ px: 2, pb: 1 }}>
        <ListItemButton
          onClick={(e) => setLangMenuAnchor(e.currentTarget)}
          sx={{ borderRadius: 1, py: 0.5 }}
        >
          <ListItemIcon sx={{ minWidth: 32 }}>
            <LanguageIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText 
            primary={
              <Typography variant="body2">
                {t('language')}: {languages[language]?.flag} {languages[language]?.name}
              </Typography>
            } 
          />
        </ListItemButton>
        <Menu
          anchorEl={langMenuAnchor}
          open={Boolean(langMenuAnchor)}
          onClose={() => setLangMenuAnchor(null)}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          transformOrigin={{ vertical: 'top', horizontal: 'left' }}
        >
          {languageKeys.map((key) => (
            <MenuItem
              key={key}
              selected={language === key}
              onClick={() => {
                setLanguage(key)
                setLangMenuAnchor(null)
              }}
              sx={{ minWidth: 150 }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, width: '100%' }}>
                <Typography variant="body2" sx={{ fontSize: '1.2em' }}>
                  {languages[key].flag}
                </Typography>
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  {languages[key].name}
                </Typography>
                {language === key && <CheckIcon fontSize="small" color="primary" />}
              </Box>
            </MenuItem>
          ))}
        </Menu>
      </Box>
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
    <NerdModeContext.Provider value={{ nerdMode, setNerdMode }}>
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
            {currentView === 'tasks' && t('tasks')}
            {currentView === 'taskDetail' && t('taskDetail')}
            {currentView === 'newPrompt' && t('newTask')}
            {currentView === 'user' && t('profile')}
          </Typography>
          <Tooltip title="Search (⌘K)">
            <IconButton color="inherit" onClick={() => setSearchOpen(true)}>
              <SearchIcon />
            </IconButton>
          </Tooltip>
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
      
      <SearchDialog
        open={searchOpen}
        onClose={() => setSearchOpen(false)}
        onTaskSelect={handleTaskSelect}
        apiBase={API_BASE}
      />
    </Box>
    </NerdModeContext.Provider>
  )
}
