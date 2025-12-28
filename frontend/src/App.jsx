import React, { useState, useEffect, createContext, useContext } from 'react'
import {
  Box,
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
  Tooltip,
  Menu,
  MenuItem,
} from './fakemui'
import './App.scss'

// Icon components (simple SVG replacements for MUI icons)
const MenuIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
const ListIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>
const AddIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
const PersonIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
const RefreshIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
const CodeIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
const PaletteIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9c.83 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.01-.23-.26-.38-.61-.38-.99 0-.83.67-1.5 1.5-1.5H16c2.76 0 5-2.24 5-5 0-4.42-4.03-8-9-8zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 9 6.5 9 8 9.67 8 10.5 7.33 12 6.5 12zm3-4C8.67 8 8 7.33 8 6.5S8.67 5 9.5 5s1.5.67 1.5 1.5S10.33 8 9.5 8zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 5 14.5 5s1.5.67 1.5 1.5S15.33 8 14.5 8zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 9 17.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
const CheckIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
const LanguageIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.91 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2 0 .68.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.63-3.37-1.9-4.33-3.56zm2.95-8H5.08c.96-1.66 2.49-2.93 4.33-3.56C8.81 5.55 8.35 6.75 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2 0-.68.07-1.35.16-2h4.68c.09.65.16 1.32.16 2 0 .68-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.65-2.49 2.93-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2 0-.68-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z"/></svg>
const SearchIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
const BookIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/></svg>

// Nerd mode context
export const NerdModeContext = createContext({ nerdMode: false, setNerdMode: () => {} })

import TaskList from './components/TaskList'
import TaskDetail from './components/TaskDetail'
import NewPrompt from './components/NewPrompt'
import UserInfo from './components/UserInfo'
import SearchDialog from './components/SearchDialog'
import AjaxQueueWidget from './components/AjaxQueueWidget'
import Documentation from './components/Documentation'
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
    <Box className="drawer-content">
      <Toolbar className="drawer-header">
        <Typography className="drawer-title text-primary">
          Codex Runner
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        <ListItem>
          <ListItemButton
            selected={currentView === 'tasks'}
            onClick={() => handleNavigation('tasks')}
          >
            <ListItemIcon><ListIcon /></ListItemIcon>
            <ListItemText primary={t('tasks')} />
          </ListItemButton>
        </ListItem>
        <ListItem>
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
        <ListItem>
          <ListItemButton
            selected={currentView === 'user'}
            onClick={() => handleNavigation('user')}
          >
            <ListItemIcon><PersonIcon /></ListItemIcon>
            <ListItemText primary={t('profile')} />
          </ListItemButton>
        </ListItem>
        <ListItem>
          <ListItemButton
            selected={currentView === 'docs'}
            onClick={() => handleNavigation('docs')}
          >
            <ListItemIcon><BookIcon /></ListItemIcon>
            <ListItemText primary={t('documentation') || 'Docs'} />
          </ListItemButton>
        </ListItem>
      </List>
      <Divider />
      <Box className="drawer-settings">
        <Tooltip title="Show technical details, raw JSON, and IDs">
          <label className="switch-label">
            <Switch
              checked={nerdMode}
              onChange={(e) => setNerdMode(e.target.checked)}
            />
            <Box className="switch-label-content">
              <CodeIcon />
              <span>{t('nerdMode')}</span>
            </Box>
          </label>
        </Tooltip>
      </Box>
      <Box className="drawer-menu-item">
        <ListItemButton
          onClick={(e) => setThemeMenuAnchor(e.currentTarget)}
        >
          <ListItemIcon><PaletteIcon /></ListItemIcon>
          <ListItemText 
            primary={`${t('theme')}: ${themes[themeName]?.name || 'Dark'}`}
          />
        </ListItemButton>
        <Menu
          open={Boolean(themeMenuAnchor)}
          onClose={() => setThemeMenuAnchor(null)}
          anchorEl={themeMenuAnchor}
        >
          {themeKeys.map((key) => (
            <MenuItem
              key={key}
              selected={themeName === key}
              onClick={() => {
                setThemeName(key)
                setThemeMenuAnchor(null)
              }}
            >
              <Box className="menu-item-content">
                <span 
                  className="color-dot"
                  style={{ backgroundColor: themes[key].palette.primary.main }}
                />
                <span className="menu-item-label">{themes[key].name}</span>
                {themeName === key && <CheckIcon />}
              </Box>
            </MenuItem>
          ))}
        </Menu>
      </Box>
      <Box className="drawer-menu-item">
        <ListItemButton
          onClick={(e) => setLangMenuAnchor(e.currentTarget)}
        >
          <ListItemIcon><LanguageIcon /></ListItemIcon>
          <ListItemText 
            primary={`${t('language')}: ${languages[language]?.flag} ${languages[language]?.name}`}
          />
        </ListItemButton>
        <Menu
          open={Boolean(langMenuAnchor)}
          onClose={() => setLangMenuAnchor(null)}
          anchorEl={langMenuAnchor}
        >
          {languageKeys.map((key) => (
            <MenuItem
              key={key}
              selected={language === key}
              onClick={() => {
                setLanguage(key)
                setLangMenuAnchor(null)
              }}
            >
              <Box className="menu-item-content">
                <span className="lang-flag">{languages[key].flag}</span>
                <span className="menu-item-label">{languages[key].name}</span>
                {language === key && <CheckIcon />}
              </Box>
            </MenuItem>
          ))}
        </Menu>
      </Box>
      {user && (
        <Box className="drawer-user">
          <Chip
            icon={<PersonIcon />}
            outline
          >
            {user.email || user.name || 'Connected'}
          </Chip>
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
      case 'docs':
        return <Documentation />
      default:
        return <TaskList onTaskSelect={handleTaskSelect} apiBase={API_BASE} />
    }
  }

  return (
    <NerdModeContext.Provider value={{ nerdMode, setNerdMode }}>
    <Box className="app-layout">
      <AppBar className="app-bar">
        <Toolbar>
          <IconButton
            className="menu-button mobile-only"
            onClick={handleDrawerToggle}
          >
            <MenuIcon />
          </IconButton>
          <Typography className="app-title">
            {currentView === 'tasks' && t('tasks')}
            {currentView === 'taskDetail' && t('taskDetail')}
            {currentView === 'newPrompt' && t('newTask')}
            {currentView === 'user' && t('profile')}
            {currentView === 'docs' && (t('documentation') || 'Documentation')}
          </Typography>
          <Tooltip title="Search (⌘K)">
            <IconButton onClick={() => setSearchOpen(true)}>
              <SearchIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title={t('documentation') || 'Documentation'}>
            <IconButton onClick={() => handleNavigation('docs')}>
              <BookIcon />
            </IconButton>
          </Tooltip>
          <IconButton onClick={fetchUser}>
            <RefreshIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box component="nav" className="nav-drawer">
        <Drawer
          open={mobileOpen}
          onClose={handleDrawerToggle}
          className="drawer-mobile"
        >
          {drawer}
        </Drawer>
        <Box className="drawer-permanent">
          {drawer}
        </Box>
      </Box>
      <Box component="main" className="main-content">
        {renderContent()}
      </Box>
      
      <SearchDialog
        open={searchOpen}
        onClose={() => setSearchOpen(false)}
        onTaskSelect={handleTaskSelect}
        apiBase={API_BASE}
      />
      
      <AjaxQueueWidget />
    </Box>
    </NerdModeContext.Provider>
  )
}
