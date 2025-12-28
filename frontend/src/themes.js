// Theme definitions without MUI dependency
// These are used for CSS custom properties

export const themes = {
  dark: {
    name: 'Dark',
    palette: {
      mode: 'dark',
      primary: { main: '#10a37f' },
      secondary: { main: '#8e8ea0' },
      background: { default: '#0d0d0d', paper: '#1a1a1a' },
      text: { primary: '#ffffff', secondary: '#a0a0a0' },
      error: { main: '#f44336' },
      warning: { main: '#ff9800' },
      success: { main: '#4caf50' },
      info: { main: '#2196f3' },
    },
  },
  light: {
    name: 'Light',
    palette: {
      mode: 'light',
      primary: { main: '#10a37f' },
      secondary: { main: '#6e6e80' },
      background: { default: '#ffffff', paper: '#f7f7f8' },
      text: { primary: '#1a1a1a', secondary: '#6e6e80' },
      error: { main: '#d32f2f' },
      warning: { main: '#ed6c02' },
      success: { main: '#2e7d32' },
      info: { main: '#0288d1' },
    },
  },
  midnight: {
    name: 'Midnight',
    palette: {
      mode: 'dark',
      primary: { main: '#6366f1' },
      secondary: { main: '#a5b4fc' },
      background: { default: '#0f172a', paper: '#1e293b' },
      text: { primary: '#f1f5f9', secondary: '#94a3b8' },
      error: { main: '#ef4444' },
      warning: { main: '#f59e0b' },
      success: { main: '#22c55e' },
      info: { main: '#3b82f6' },
    },
  },
  forest: {
    name: 'Forest',
    palette: {
      mode: 'dark',
      primary: { main: '#22c55e' },
      secondary: { main: '#86efac' },
      background: { default: '#0a1f0a', paper: '#14331a' },
      text: { primary: '#ecfdf5', secondary: '#a7f3d0' },
      error: { main: '#ef4444' },
      warning: { main: '#f59e0b' },
      success: { main: '#22c55e' },
      info: { main: '#3b82f6' },
    },
  },
  ocean: {
    name: 'Ocean',
    palette: {
      mode: 'dark',
      primary: { main: '#0ea5e9' },
      secondary: { main: '#7dd3fc' },
      background: { default: '#0c1929', paper: '#132f4c' },
      text: { primary: '#e0f2fe', secondary: '#7dd3fc' },
      error: { main: '#ef4444' },
      warning: { main: '#f59e0b' },
      success: { main: '#22c55e' },
      info: { main: '#0ea5e9' },
    },
  },
  sunset: {
    name: 'Sunset',
    palette: {
      mode: 'dark',
      primary: { main: '#f97316' },
      secondary: { main: '#fdba74' },
      background: { default: '#1c1210', paper: '#2d1f1a' },
      text: { primary: '#fff7ed', secondary: '#fed7aa' },
      error: { main: '#ef4444' },
      warning: { main: '#f97316' },
      success: { main: '#22c55e' },
      info: { main: '#3b82f6' },
    },
  },
  rose: {
    name: 'Rose',
    palette: {
      mode: 'dark',
      primary: { main: '#f43f5e' },
      secondary: { main: '#fda4af' },
      background: { default: '#1a0f12', paper: '#2d1a1f' },
      text: { primary: '#fff1f2', secondary: '#fecdd3' },
      error: { main: '#f43f5e' },
      warning: { main: '#f59e0b' },
      success: { main: '#22c55e' },
      info: { main: '#3b82f6' },
    },
  },
  highContrast: {
    name: 'High Contrast',
    palette: {
      mode: 'dark',
      primary: { main: '#ffff00' },
      secondary: { main: '#00ffff' },
      background: { default: '#000000', paper: '#111111' },
      text: { primary: '#ffffff', secondary: '#eeeeee' },
      error: { main: '#ff0000' },
      warning: { main: '#ffff00' },
      success: { main: '#00ff00' },
      info: { main: '#00ffff' },
    },
  },
}

export const themeKeys = Object.keys(themes)
export const defaultTheme = 'dark'

// Apply theme as CSS variables to document root
export function applyTheme(themeName) {
  const theme = themes[themeName] || themes[defaultTheme]
  const root = document.documentElement
  
  // Set color scheme for native elements
  root.style.colorScheme = theme.palette.mode
  
  // Set CSS custom properties
  root.style.setProperty('--color-primary', theme.palette.primary.main)
  root.style.setProperty('--color-secondary', theme.palette.secondary.main)
  root.style.setProperty('--color-bg', theme.palette.background.default)
  root.style.setProperty('--color-bg-paper', theme.palette.background.paper)
  root.style.setProperty('--color-text', theme.palette.text.primary)
  root.style.setProperty('--color-text-secondary', theme.palette.text.secondary)
  root.style.setProperty('--color-error', theme.palette.error.main)
  root.style.setProperty('--color-warning', theme.palette.warning.main)
  root.style.setProperty('--color-success', theme.palette.success.main)
  root.style.setProperty('--color-info', theme.palette.info.main)
  
  // Set body class for light/dark mode
  document.body.classList.remove('light-mode', 'dark-mode')
  document.body.classList.add(`${theme.palette.mode}-mode`)
}
