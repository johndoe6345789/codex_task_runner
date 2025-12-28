pragma Singleton
import QtQuick

/**
 * ThemeContext - Theme management with multiple presets
 * Mirrors React's themes.js with 9 themes
 */
QtObject {
    id: themeContext
    
    // Current theme name - default to dark
    property string themeName: "dark"
    
    // Alias for compatibility
    property var colors: current
    
    // Available theme keys
    readonly property var themeKeys: [
        "system", "dark", "light", "midnight", "forest", "ocean", "sunset", "rose", "highContrast"
    ]
    
    // Theme definitions - mirrors React themes.js
    readonly property var themes: ({
        system: {
            name: "System",
            mode: "dark",
            primary: "#10a37f",
            secondary: "#8e8ea0",
            background: "#0d0d0d",
            paper: "#1a1a1a",
            surface: "#242424",
            text: "#ffffff",
            textSecondary: "#a0a0a0",
            textMuted: "#666666",
            border: "#333333",
            divider: "#2a2a2a",
            error: "#ef4444",
            warning: "#f59e0b",
            success: "#22c55e",
            info: "#3b82f6"
        },
        dark: {
            name: "Dark",
            mode: "dark",
            primary: "#10a37f",
            secondary: "#8e8ea0",
            background: "#0d0d0d",
            paper: "#1a1a1a",
            surface: "#242424",
            text: "#ffffff",
            textSecondary: "#a0a0a0",
            textMuted: "#666666",
            border: "#333333",
            divider: "#2a2a2a",
            error: "#ef4444",
            warning: "#f59e0b",
            success: "#22c55e",
            info: "#3b82f6"
        },
        light: {
            name: "Light",
            mode: "light",
            primary: "#10a37f",
            secondary: "#6e6e80",
            background: "#ffffff",
            paper: "#f7f7f8",
            surface: "#eeeeee",
            text: "#1a1a1a",
            textSecondary: "#6e6e80",
            textMuted: "#999999",
            border: "#e0e0e0",
            divider: "#eeeeee",
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
            surface: "#334155",
            text: "#f1f5f9",
            textSecondary: "#94a3b8",
            textMuted: "#64748b",
            border: "#334155",
            divider: "#1e293b",
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
            surface: "#1a4d23",
            text: "#ecfdf5",
            textSecondary: "#a7f3d0",
            textMuted: "#6ee7b7",
            border: "#166534",
            divider: "#14532d",
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
            surface: "#1e4976",
            text: "#e0f2fe",
            textSecondary: "#7dd3fc",
            textMuted: "#38bdf8",
            border: "#0369a1",
            divider: "#075985",
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
            surface: "#44302a",
            text: "#fff7ed",
            textSecondary: "#fed7aa",
            textMuted: "#fdba74",
            border: "#9a3412",
            divider: "#7c2d12",
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
            surface: "#44252d",
            text: "#fff1f2",
            textSecondary: "#fecdd3",
            textMuted: "#fda4af",
            border: "#be123c",
            divider: "#9f1239",
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
            surface: "#222222",
            text: "#ffffff",
            textSecondary: "#eeeeee",
            textMuted: "#cccccc",
            border: "#ffffff",
            divider: "#444444",
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
    readonly property color surface: current.surface || current.paper
    readonly property color text: current.text
    readonly property color textSecondary: current.textSecondary
    readonly property color textMuted: current.textMuted || current.textSecondary
    readonly property color border: current.border || "#333333"
    readonly property color divider: current.divider || current.border
    readonly property color error: current.error
    readonly property color warning: current.warning
    readonly property color success: current.success
    readonly property color info: current.info
    
    /**
     * Set theme
     */
    function setTheme(name) {
        if (themes[name]) {
            themeName = name
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
