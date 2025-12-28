import React, { useState, useEffect, createContext } from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider, CssBaseline } from '@mui/material'
import App from './App'
import { themes, defaultTheme } from './themes'
import { languages, defaultLanguage } from './i18n'

// Theme context for global access
export const ThemeContext = createContext({
  themeName: defaultTheme,
  setThemeName: () => {},
})

// Language context for global access
export const LanguageContext = createContext({
  language: defaultLanguage,
  setLanguage: () => {},
  t: (key) => key,
})

function ThemedApp() {
  const [themeName, setThemeName] = useState(() => {
    const saved = localStorage.getItem('theme')
    return saved && themes[saved] ? saved : defaultTheme
  })

  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem('language')
    return saved && languages[saved] ? saved : defaultLanguage
  })

  useEffect(() => {
    localStorage.setItem('theme', themeName)
  }, [themeName])

  useEffect(() => {
    localStorage.setItem('language', language)
  }, [language])

  const currentTheme = themes[themeName]?.theme || themes[defaultTheme].theme

  // Translation function
  const t = (key) => {
    return languages[language]?.translations[key] || languages.en.translations[key] || key
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      <ThemeContext.Provider value={{ themeName, setThemeName }}>
        <ThemeProvider theme={currentTheme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
      </ThemeContext.Provider>
    </LanguageContext.Provider>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemedApp />
  </React.StrictMode>,
)
