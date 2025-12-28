pragma Singleton
import QtQuick

/**
 * Theme.qml - Unified theme system for fakemui components
 * Combines Material-UI style properties with React app's multi-theme support
 */
QtObject {
    id: theme
    
    // Current theme name
    property string current: "dark"
    property string mode: "dark"
    
    // Available themes list
    readonly property var themeKeys: [
        "system", "dark", "light", "midnight", "forest", "ocean", "sunset", "rose", "highContrast"
    ]
    
    // Theme definitions - matches React themes.js
    readonly property var themes: ({
        system: { name: "System", mode: "dark", primary: "#10a37f", background: "#0d0d0d", paper: "#1a1a1a", surface: "#242424", text: "#ffffff", textSecondary: "#a0a0a0", border: "#333333", error: "#ef4444", warning: "#f59e0b", success: "#22c55e", info: "#3b82f6" },
        dark: { name: "Dark", mode: "dark", primary: "#10a37f", background: "#0d0d0d", paper: "#1a1a1a", surface: "#242424", text: "#ffffff", textSecondary: "#a0a0a0", border: "#333333", error: "#ef4444", warning: "#f59e0b", success: "#22c55e", info: "#3b82f6" },
        light: { name: "Light", mode: "light", primary: "#10a37f", background: "#ffffff", paper: "#f7f7f8", surface: "#eeeeee", text: "#1a1a1a", textSecondary: "#6e6e80", border: "#e0e0e0", error: "#d32f2f", warning: "#ed6c02", success: "#2e7d32", info: "#0288d1" },
        midnight: { name: "Midnight", mode: "dark", primary: "#6366f1", background: "#0f172a", paper: "#1e293b", surface: "#334155", text: "#f1f5f9", textSecondary: "#94a3b8", border: "#334155", error: "#ef4444", warning: "#f59e0b", success: "#22c55e", info: "#3b82f6" },
        forest: { name: "Forest", mode: "dark", primary: "#22c55e", background: "#0a1f0a", paper: "#14331a", surface: "#1a4d23", text: "#ecfdf5", textSecondary: "#a7f3d0", border: "#166534", error: "#ef4444", warning: "#f59e0b", success: "#22c55e", info: "#3b82f6" },
        ocean: { name: "Ocean", mode: "dark", primary: "#0ea5e9", background: "#0c1929", paper: "#132f4c", surface: "#1e4976", text: "#e0f2fe", textSecondary: "#7dd3fc", border: "#0369a1", error: "#ef4444", warning: "#f59e0b", success: "#22c55e", info: "#0ea5e9" },
        sunset: { name: "Sunset", mode: "dark", primary: "#f97316", background: "#1c1210", paper: "#2d1f1a", surface: "#44302a", text: "#fff7ed", textSecondary: "#fed7aa", border: "#9a3412", error: "#ef4444", warning: "#f97316", success: "#22c55e", info: "#3b82f6" },
        rose: { name: "Rose", mode: "dark", primary: "#f43f5e", background: "#1a0f12", paper: "#2d1a1f", surface: "#44252d", text: "#fff1f2", textSecondary: "#fecdd3", border: "#be123c", error: "#f43f5e", warning: "#f59e0b", success: "#22c55e", info: "#3b82f6" },
        highContrast: { name: "High Contrast", mode: "dark", primary: "#ffff00", background: "#000000", paper: "#111111", surface: "#222222", text: "#ffffff", textSecondary: "#eeeeee", border: "#ffffff", error: "#ff0000", warning: "#ffff00", success: "#00ff00", info: "#00ffff" }
    })
    
    // Current theme object
    readonly property var currentTheme: themes[current] || themes.dark
    
    // Primary palette from current theme
    property color primary: currentTheme.primary
    property color primaryLight: Qt.lighter(primary, 1.2)
    property color primaryDark: Qt.darker(primary, 1.2)
    property color primaryContrastText: "#ffffff"
    
    // Secondary palette
    property color secondary: "#8e8ea0"
    property color secondaryLight: "#a8a8b6"
    property color secondaryDark: "#6e6e80"
    property color secondaryContrastText: "#ffffff"
    
    // Status colors from current theme
    property color error: currentTheme.error
    property color errorLight: Qt.lighter(error, 1.2)
    property color errorDark: Qt.darker(error, 1.2)
    property color errorContrastText: "#ffffff"
    
    property color warning: currentTheme.warning
    property color warningLight: Qt.lighter(warning, 1.2)
    property color warningDark: Qt.darker(warning, 1.2)
    property color warningContrastText: "#ffffff"
    
    property color info: currentTheme.info
    property color infoLight: Qt.lighter(info, 1.2)
    property color infoDark: Qt.darker(info, 1.2)
    property color infoContrastText: "#ffffff"
    
    property color success: currentTheme.success
    property color successLight: Qt.lighter(success, 1.2)
    property color successDark: Qt.darker(success, 1.2)
    property color successContrastText: "#ffffff"
    
    // Grey scale
    property color grey50: "#fafafa"
    property color grey100: "#f5f5f5"
    property color grey200: "#eeeeee"
    property color grey300: "#e0e0e0"
    property color grey400: "#bdbdbd"
    property color grey500: "#9e9e9e"
    property color grey600: "#757575"
    property color grey700: "#616161"
    property color grey800: "#424242"
    property color grey900: "#212121"
    
    // Background colors from current theme
    property color background: currentTheme.background
    property color paper: currentTheme.paper
    property color surface: currentTheme.surface
    property color surfaceVariant: Qt.lighter(surface, 1.1)
    property color card: currentTheme.paper
    
    // Text colors from current theme
    property color text: currentTheme.text
    property color textSecondary: currentTheme.textSecondary
    property color textMuted: Qt.darker(textSecondary, 1.2)
    property color textDisabled: mode === "dark" ? "rgba(255, 255, 255, 0.38)" : "rgba(0, 0, 0, 0.38)"
    
    // Border and divider from current theme
    property color border: currentTheme.border
    property color divider: Qt.darker(border, 1.1)
    
    // Action colors
    property color actionActive: mode === "dark" ? "rgba(255, 255, 255, 0.54)" : "rgba(0, 0, 0, 0.54)"
    property color actionHover: mode === "dark" ? "rgba(255, 255, 255, 0.04)" : "rgba(0, 0, 0, 0.04)"
    property color actionSelected: mode === "dark" ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.08)"
    property color actionDisabled: mode === "dark" ? "rgba(255, 255, 255, 0.26)" : "rgba(0, 0, 0, 0.26)"
    
    // Legacy aliases
    property alias accent: primary
    
    // Typography
    property int fontSizeXs: 10
    property int fontSizeSm: 12
    property int fontSizeMd: 14
    property int fontSizeLg: 16
    property int fontSizeXl: 20
    property int fontSizeXxl: 24
    property int fontSizeH1: 96
    property int fontSizeH2: 60
    property int fontSizeH3: 48
    property int fontSizeH4: 34
    property int fontSizeH5: 24
    property int fontSizeH6: 20
    
    property int fontWeightLight: 300
    property int fontWeightRegular: 400
    property int fontWeightMedium: 500
    property int fontWeightBold: 700
    
    property string fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif'
    property string fontFamilyMono: "Menlo, Monaco, Consolas, monospace"
    
    // Spacing (8px base unit)
    property int spacingUnit: 8
    property int spacingXs: 4
    property int spacingSm: 8
    property int spacingMd: 12
    property int spacingLg: 16
    property int spacingXl: 24
    property int spacingXxl: 32
    
    // Spacing function
    function spacing(factor) {
        return spacingUnit * factor
    }
    
    // Border radius
    property int radiusSm: 4
    property int radiusMd: 8
    property int radiusLg: 12
    property int radiusXl: 16
    property int radiusFull: 9999
    property int shapeBorderRadius: 4
    
    // Shadows
    property color shadowColor: "#000000"
    property var shadows: [
        "none",
        "0px 2px 1px -1px rgba(0,0,0,0.2)",
        "0px 3px 1px -2px rgba(0,0,0,0.2)",
        "0px 3px 3px -2px rgba(0,0,0,0.2)",
        "0px 2px 4px -1px rgba(0,0,0,0.2)"
    ]
    
    // Transitions
    property int transitionShortest: 150
    property int transitionShorter: 200
    property int transitionShort: 250
    property int transitionStandard: 300
    property int transitionComplex: 375
    
    // Animation (legacy)
    property alias animFast: transitionShortest
    property alias animNormal: transitionStandard
    property alias animSlow: transitionComplex
    
    // Z-index
    property int zIndexMobileStepper: 1000
    property int zIndexFab: 1050
    property int zIndexAppBar: 1100
    property int zIndexDrawer: 1200
    property int zIndexModal: 1300
    property int zIndexSnackbar: 1400
    property int zIndexTooltip: 1500
    
    // Breakpoints
    property int breakpointXs: 0
    property int breakpointSm: 600
    property int breakpointMd: 900
    property int breakpointLg: 1200
    property int breakpointXl: 1536
    
    // Status colors (utility function)
    function statusColor(status) {
        switch(status) {
            case "completed": return success
            case "running": return info
            case "queued": return warning
            case "failed": return error
            default: return textMuted
        }
    }
    
    // Get color by name
    function getColor(colorName) {
        switch(colorName) {
            case "primary": return primary
            case "secondary": return secondary
            case "error": return error
            case "warning": return warning
            case "info": return info
            case "success": return success
            default: return grey500
        }
    }
    
    // Set theme by name
    function setTheme(name) {
        if (themes[name]) {
            current = name
            mode = themes[name].mode
        }
    }
    
    // Toggle between light and dark
    function toggleMode() {
        setTheme(mode === "dark" ? "light" : "dark")
    }
    
    // Get theme info by name
    function getTheme(name) {
        return themes[name] || themes.dark
    }
    
    // Legacy function
    function applyTheme(themeName) {
        setTheme(themeName)
    }
    
    // Create theme with custom options (MUI compatibility)
    function createTheme(options) {
        if (options.palette) {
            if (options.palette.mode) mode = options.palette.mode
        }
        if (options.shape) {
            if (options.shape.borderRadius) shapeBorderRadius = options.shape.borderRadius
        }
    }
}
