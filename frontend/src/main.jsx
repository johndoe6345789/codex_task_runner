import React, { useState, useEffect, createContext } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { themes, defaultTheme, applyTheme } from './themes'
import { languages, defaultLanguage } from './i18n'
import { AjaxQueueProvider } from './contexts/AjaxQueueContext'
import './styles/base.scss'
import './styles/components.scss'

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
    applyTheme(themeName)
  }, [themeName])

  useEffect(() => {
    localStorage.setItem('language', language)
  }, [language])

  // Apply initial theme
  useEffect(() => {
    applyTheme(themeName)
  }, [])

  // Translation function
  const t = (key) => {
    return languages[language]?.translations[key] || languages.en.translations[key] || key
  }

  return (
    <AjaxQueueProvider>
      <LanguageContext.Provider value={{ language, setLanguage, t }}>
        <ThemeContext.Provider value={{ themeName, setThemeName }}>
          <App />
        </ThemeContext.Provider>
      </LanguageContext.Provider>
    </AjaxQueueProvider>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemedApp />
  </React.StrictMode>,
)
