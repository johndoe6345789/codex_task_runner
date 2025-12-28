import React from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material'
import App from './App'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#10a37f',
    },
    secondary: {
      main: '#8e8ea0',
    },
    background: {
      default: '#0d0d0d',
      paper: '#1a1a1a',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
