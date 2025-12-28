pragma Singleton
import QtQuick

QtObject {
    id: theme
    
    // Current theme name
    property string current: "dark"
    
    // Color palette
    property color primary: "#4dabf7"
    property color primaryDark: "#1a73e8"
    property color secondary: "#69db7c"
    property color accent: "#ffd43b"
    
    property color background: "#121212"
    property color surface: "#1e1e1e"
    property color surfaceVariant: "#2d2d2d"
    property color card: "#252525"
    
    property color text: "#ffffff"
    property color textSecondary: "#b0b0b0"
    property color textMuted: "#666666"
    
    property color success: "#4caf50"
    property color warning: "#ff9800"
    property color error: "#f44336"
    property color info: "#2196f3"
    
    property color border: "#3d3d3d"
    property color divider: "#2d2d2d"
    
    // Typography
    property int fontSizeXs: 10
    property int fontSizeSm: 12
    property int fontSizeMd: 14
    property int fontSizeLg: 16
    property int fontSizeXl: 20
    property int fontSizeXxl: 24
    
    property string fontFamily: "SF Pro Display, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"
    property string fontFamilyMono: "Menlo"
    
    // Spacing
    property int spacingXs: 4
    property int spacingSm: 8
    property int spacingMd: 12
    property int spacingLg: 16
    property int spacingXl: 24
    property int spacingXxl: 32
    
    // Border radius
    property int radiusSm: 4
    property int radiusMd: 8
    property int radiusLg: 12
    property int radiusXl: 16
    property int radiusFull: 9999
    
    // Shadows
    property color shadowColor: "#000000"
    
    // Animation
    property int animFast: 150
    property int animNormal: 250
    property int animSlow: 400
    
    // Status colors
    function statusColor(status) {
        switch(status) {
            case "completed": return success
            case "running": return info
            case "queued": return warning
            case "failed": return error
            default: return textMuted
        }
    }
    
    // Apply theme
    function applyTheme(themeName) {
        current = themeName
        switch(themeName) {
            case "light":
                background = "#f5f5f5"
                surface = "#ffffff"
                surfaceVariant = "#f0f0f0"
                card = "#ffffff"
                text = "#1a1a1a"
                textSecondary = "#666666"
                textMuted = "#999999"
                border = "#e0e0e0"
                divider = "#eeeeee"
                break
            case "ocean":
                background = "#0d1b2a"
                surface = "#1b263b"
                surfaceVariant = "#273549"
                card = "#1b263b"
                primary = "#4dabf7"
                accent = "#778da9"
                break
            case "forest":
                background = "#1a2f1a"
                surface = "#1e3a1e"
                surfaceVariant = "#254725"
                card = "#1e3a1e"
                primary = "#66bb6a"
                accent = "#81c784"
                break
            default: // dark
                background = "#121212"
                surface = "#1e1e1e"
                surfaceVariant = "#2d2d2d"
                card = "#252525"
                text = "#ffffff"
                textSecondary = "#b0b0b0"
                textMuted = "#666666"
                border = "#3d3d3d"
                divider = "#2d2d2d"
                primary = "#4dabf7"
                break
        }
    }
}
