import { createTheme } from '@mui/material'

export const themes = {
  dark: {
    name: 'Dark',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#10a37f' },
        secondary: { main: '#8e8ea0' },
        background: { default: '#0d0d0d', paper: '#1a1a1a' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  light: {
    name: 'Light',
    theme: createTheme({
      palette: {
        mode: 'light',
        primary: { main: '#10a37f' },
        secondary: { main: '#6e6e80' },
        background: { default: '#ffffff', paper: '#f7f7f8' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  midnight: {
    name: 'Midnight',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#6366f1' },
        secondary: { main: '#a5b4fc' },
        background: { default: '#0f172a', paper: '#1e293b' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  forest: {
    name: 'Forest',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#22c55e' },
        secondary: { main: '#86efac' },
        background: { default: '#0a1f0a', paper: '#14331a' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  ocean: {
    name: 'Ocean',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#0ea5e9' },
        secondary: { main: '#7dd3fc' },
        background: { default: '#0c1929', paper: '#132f4c' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  sunset: {
    name: 'Sunset',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#f97316' },
        secondary: { main: '#fdba74' },
        background: { default: '#1c1210', paper: '#2d1f1a' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  rose: {
    name: 'Rose',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#f43f5e' },
        secondary: { main: '#fda4af' },
        background: { default: '#1a0f12', paper: '#2d1a1f' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
  highContrast: {
    name: 'High Contrast',
    theme: createTheme({
      palette: {
        mode: 'dark',
        primary: { main: '#ffff00' },
        secondary: { main: '#00ffff' },
        background: { default: '#000000', paper: '#111111' },
        text: { primary: '#ffffff', secondary: '#eeeeee' },
      },
      typography: { fontFamily: 'Roboto, sans-serif' },
    }),
  },
}

export const themeKeys = Object.keys(themes)
export const defaultTheme = 'dark'
