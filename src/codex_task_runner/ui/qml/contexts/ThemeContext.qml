pragma Singleton
import QtQuick

/**
 * ThemeContext - Theme management with multiple presets
 * Mirrors React's themes.js with 8 themes
 */
QtObject {
    id: themeContext
    
    // Current theme name
    property string themeName: {
        const saved = _settings.value("theme", "dark")
        return themes[saved] ? saved : "dark"
    }
    
    // Available theme keys
    readonly property var themeKeys: [
        "dark", "light", "midnight", "forest", "ocean", "sunset", "rose", "highContrast"
    ]
    
    // Theme definitions - mirrors React themes.js
    readonly property var themes: ({
        dark: {
            name: "Dark",
            mode: "dark",
            primary: "#10a37f",
            secondary: "#8e8ea0",
            background: "#0d0d0d",
            paper: "#1a1a1a",
            text: "#ffffff",
            textSecondary: "#a0a0a0",
            error: "#f44336",
            warning: "#ff9800",
            success: "#4caf50",
            info: "#2196f3"
        },
        light: {
            name: "Light",
            mode: "light",
            primary: "#10a37f",
            secondary: "#6e6e80",
            background: "#ffffff",
            paper: "#f7f7f8",
            text: "#1a1a1a",
            textSecondary: "#6e6e80",
            error: "#d32f2f",
            warning: "#ed6c02",
            success: "#2e7d32",
            info: "#0288d1"
        },
        midnight: {
            name: "Midnight",
            mode: "dark",
            primary: "#6366f1",
            secondary: "#a5b4fc",
            background: "#0f172a",
            paper: "#1e293b",
            text: "#f1f5f9",
            textSecondary: "#94a3b8",
            error: "#ef4444",
            warning: "#f59e0b",
            success: "#22c55e",
            info: "#3b82f6"
        },
        forest: {
            name: "Forest",
            mode: "dark",
            primary: "#22c55e",
            secondary: "#86efac",
            background: "#0a1f0a",
            paper: "#14331a",
            text: "#ecfdf5",
            textSecondary: "#a7f3d0",
            error: "#ef4444",
            warning: "#f59e0b",
            success: "#22c55e",
            info: "#3b82f6"
        },
        ocean: {
            name: "Ocean",
            mode: "dark",
            primary: "#0ea5e9",
            secondary: "#7dd3fc",
            background: "#0c1929",
            paper: "#132f4c",
            text: "#e0f2fe",
            textSecondary: "#7dd3fc",
            error: "#ef4444",
            warning: "#f59e0b",
            success: "#22c55e",
            info: "#0ea5e9"
        },
        sunset: {
            name: "Sunset",
            mode: "dark",
            primary: "#f97316",
            secondary: "#fdba74",
            background: "#1c1210",
            paper: "#2d1f1a",
            text: "#fff7ed",
            textSecondary: "#fed7aa",
            error: "#ef4444",
            warning: "#f97316",
            success: "#22c55e",
            info: "#3b82f6"
        },
        rose: {
            name: "Rose",
            mode: "dark",
            primary: "#f43f5e",
            secondary: "#fda4af",
            background: "#1a0f12",
            paper: "#2d1a1f",
            text: "#fff1f2",
            textSecondary: "#fecdd3",
            error: "#f43f5e",
            warning: "#f59e0b",
            success: "#22c55e",
            info: "#3b82f6"
        },
        highContrast: {
            name: "High Contrast",
            mode: "dark",
            primary: "#ffff00",
            secondary: "#00ffff",
            background: "#000000",
            paper: "#111111",
            text: "#ffffff",
            textSecondary: "#eeeeee",
            error: "#ff0000",
            warning: "#ffff00",
            success: "#00ff00",
            info: "#00ffff"
        }
    })
    
    // Current theme colors (convenience properties)
    readonly property var current: themes[themeName] || themes.dark
    readonly property string mode: current.mode
    readonly property color primary: current.primary
    readonly property color secondary: current.secondary
    readonly property color background: current.background
    readonly property color paper: current.paper
    readonly property color text: current.text
    readonly property color textSecondary: current.textSecondary
    readonly property color error: current.error
    readonly property color warning: current.warning
    readonly property color success: current.success
    readonly property color info: current.info
    
    // Settings for persistence
    property Settings _settings: Settings {
        category: "theme"
    }
    
    /**
     * Set theme and persist
     */
    function setTheme(name) {
        if (themes[name]) {
            themeName = name
            _settings.setValue("theme", name)
        }
    }
    
    /**
     * Get theme info
     */
    function getTheme(name) {
        return themes[name] || themes.dark
    }
    
    /**
     * Toggle between light and dark
     */
    function toggleMode() {
        if (current.mode === "dark") {
            setTheme("light")
        } else {
            setTheme("dark")
        }
    }
}
