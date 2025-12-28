pragma Singleton
import QtQuick

QtObject {
    id: theme
    
    // Current theme name
    property string current: "dark"
    property string mode: "dark" // light or dark
    
    // Primary palette - React green accent
    property color primary: "#10a37f"
    property color primaryLight: "#3db896"
    property color primaryDark: "#0d8567"
    property color primaryContrastText: "#ffffff"
    
    // Secondary palette
    property color secondary: "#8e8ea0"
    property color secondaryLight: "#a8a8b6"
    property color secondaryDark: "#6e6e80"
    property color secondaryContrastText: "#ffffff"
    
    // Error palette
    property color error: "#ef4444"
    property color errorLight: "#f87171"
    property color errorDark: "#dc2626"
    property color errorContrastText: "#ffffff"
    
    // Warning palette
    property color warning: "#f59e0b"
    property color warningLight: "#fbbf24"
    property color warningDark: "#d97706"
    property color warningContrastText: "#ffffff"
    
    // Info palette
    property color info: "#3b82f6"
    property color infoLight: "#60a5fa"
    property color infoDark: "#2563eb"
    property color infoContrastText: "#ffffff"
    
    // Success palette
    property color success: "#22c55e"
    property color successLight: "#4ade80"
    property color successDark: "#16a34a"
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
    
    // Background colors - React dark theme
    property color background: mode === "dark" ? "#0d0d0d" : "#ffffff"
    property color surface: mode === "dark" ? "#1a1a1a" : "#ffffff"
    property color surfaceVariant: mode === "dark" ? "#242424" : "#f0f0f0"
    property color card: mode === "dark" ? "#1a1a1a" : "#ffffff"
    
    // Text colors
    property color text: mode === "dark" ? "#ffffff" : "#1a1a1a"
    property color textSecondary: mode === "dark" ? "#a0a0a0" : "#6e6e80"
    property color textMuted: mode === "dark" ? "#666666" : "rgba(0, 0, 0, 0.38)"
    property color textDisabled: mode === "dark" ? "rgba(255, 255, 255, 0.38)" : "rgba(0, 0, 0, 0.38)"
    
    // Divider and border
    property color divider: mode === "dark" ? "#2a2a2a" : "rgba(0, 0, 0, 0.12)"
    property color border: mode === "dark" ? "#333333" : "#e0e0e0"
    
    // Action colors
    property color actionActive: mode === "dark" ? "rgba(255, 255, 255, 0.54)" : "rgba(0, 0, 0, 0.54)"
    property color actionHover: mode === "dark" ? "rgba(255, 255, 255, 0.04)" : "rgba(0, 0, 0, 0.04)"
    property color actionSelected: mode === "dark" ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.08)"
    property color actionDisabled: mode === "dark" ? "rgba(255, 255, 255, 0.26)" : "rgba(0, 0, 0, 0.26)"
    
    // Legacy color aliases
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
    
    // Apply theme
    function applyTheme(themeName) {
        current = themeName
        switch(themeName) {
            case "light":
                mode = "light"
                break
            case "ocean":
                mode = "dark"
                primary = "#4dabf7"
                background = "#0d1b2a"
                surface = "#1b263b"
                surfaceVariant = "#273549"
                card = "#1b263b"
                break
            case "forest":
                mode = "dark"
                primary = "#66bb6a"
                secondary = "#81c784"
                background = "#1a2f1a"
                surface = "#1e3a1e"
                surfaceVariant = "#254725"
                card = "#1e3a1e"
                break
            default: // dark
                mode = "dark"
                primary = "#1976d2"
                secondary = "#9c27b0"
                break
        }
    }
    
    // Create theme with custom options
    function createTheme(options) {
        if (options.palette) {
            if (options.palette.mode) {
                mode = options.palette.mode
            }
            if (options.palette.primary) {
                if (options.palette.primary.main) primary = options.palette.primary.main
                if (options.palette.primary.light) primaryLight = options.palette.primary.light
                if (options.palette.primary.dark) primaryDark = options.palette.primary.dark
            }
            if (options.palette.secondary) {
                if (options.palette.secondary.main) secondary = options.palette.secondary.main
            }
        }
        if (options.shape) {
            if (options.shape.borderRadius) shapeBorderRadius = options.shape.borderRadius
        }
    }
}
