import React, { useState, useEffect, createContext } from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider, CssBaseline } from '@mui/material'
import App from './App'
import { themes, defaultTheme } from './themes'

// Theme context for global access
export const ThemeContext = createContext({
  themeName: defaultTheme,
  setThemeName: () => {},
})

function ThemedApp() {
  const [themeName, setThemeName] = useState(() => {
    const saved = localStorage.getItem('theme')
    return saved && themes[saved] ? saved : defaultTheme
  })

  useEffect(() => {
    localStorage.setItem('theme', themeName)
  }, [themeName])

  const currentTheme = themes[themeName]?.theme || themes[defaultTheme].theme

  return (
    <ThemeContext.Provider value={{ themeName, setThemeName }}>
      <ThemeProvider theme={currentTheme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </ThemeContext.Provider>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemedApp />
  </React.StrictMode>,
)
