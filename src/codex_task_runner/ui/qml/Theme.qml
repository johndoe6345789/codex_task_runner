pragma Singleton
import QtQuick

QtObject {
    id: root
    
    // Current theme name
    property string currentTheme: "system"
    
    // Available themes
    readonly property var themes: [
        { id: "system", name: "System", icon: "💻" },
        { id: "light", name: "Light", icon: "☀️" },
        { id: "dark", name: "Dark", icon: "🌙" },
        { id: "hacker", name: "Hacker", icon: "🤓" },
        { id: "ocean", name: "Ocean", icon: "🌊" },
        { id: "sunset", name: "Sunset", icon: "🌅" },
        { id: "forest", name: "Forest", icon: "🌲" },
    ]
    
    // Theme definitions
    readonly property var themeColors: ({
        "system": {
            window: "#2b2b2b",
            windowText: "#ffffff",
            base: "#1e1e1e",
            alternateBase: "#353535",
            text: "#ffffff",
            button: "#353535",
            buttonText: "#ffffff",
            highlight: "#0078d4",
            highlightedText: "#ffffff",
            mid: "#3c3c3c",
            accent: "#0078d4",
            success: "#2d7d46",
            error: "#c62828",
            warning: "#f57c00",
            info: "#1a73e8",
            codeBackground: "#1e1e1e",
            codeText: "#d4d4d4",
        },
        "light": {
            window: "#f5f5f5",
            windowText: "#1a1a1a",
            base: "#ffffff",
            alternateBase: "#f0f0f0",
            text: "#1a1a1a",
            button: "#e0e0e0",
            buttonText: "#1a1a1a",
            highlight: "#0078d4",
            highlightedText: "#ffffff",
            mid: "#d0d0d0",
            accent: "#0078d4",
            success: "#2d7d46",
            error: "#c62828",
            warning: "#f57c00",
            info: "#1a73e8",
            codeBackground: "#f8f8f8",
            codeText: "#333333",
        },
        "dark": {
            window: "#1e1e1e",
            windowText: "#e0e0e0",
            base: "#252526",
            alternateBase: "#2d2d30",
            text: "#e0e0e0",
            button: "#3c3c3c",
            buttonText: "#e0e0e0",
            highlight: "#264f78",
            highlightedText: "#ffffff",
            mid: "#3c3c3c",
            accent: "#569cd6",
            success: "#4ec9b0",
            error: "#f14c4c",
            warning: "#cca700",
            info: "#3794ff",
            codeBackground: "#1e1e1e",
            codeText: "#d4d4d4",
        },
        "hacker": {
            window: "#0a0a0f",
            windowText: "#00ff41",
            base: "#0d0d14",
            alternateBase: "#151520",
            text: "#00ff41",
            button: "#1a1a2e",
            buttonText: "#00ff41",
            highlight: "#00ff41",
            highlightedText: "#0a0a0f",
            mid: "#1a1a2e",
            accent: "#00ff41",
            success: "#00ff41",
            error: "#ff0055",
            warning: "#ffcc00",
            info: "#00ccff",
            codeBackground: "#0a0a0f",
            codeText: "#00ff41",
        },
        "ocean": {
            window: "#0d1b2a",
            windowText: "#e0e1dd",
            base: "#1b263b",
            alternateBase: "#273549",
            text: "#e0e1dd",
            button: "#415a77",
            buttonText: "#e0e1dd",
            highlight: "#778da9",
            highlightedText: "#0d1b2a",
            mid: "#415a77",
            accent: "#4dabf7",
            success: "#40c057",
            error: "#fa5252",
            warning: "#fab005",
            info: "#4dabf7",
            codeBackground: "#0d1b2a",
            codeText: "#a9d1f7",
        },
        "sunset": {
            window: "#1a1423",
            windowText: "#ffd6ba",
            base: "#241b2f",
            alternateBase: "#2e243a",
            text: "#ffd6ba",
            button: "#3d2c4a",
            buttonText: "#ffd6ba",
            highlight: "#ff7b54",
            highlightedText: "#1a1423",
            mid: "#3d2c4a",
            accent: "#ff7b54",
            success: "#7ec8ac",
            error: "#ff6b6b",
            warning: "#feca57",
            info: "#48dbfb",
            codeBackground: "#1a1423",
            codeText: "#ffb997",
        },
        "forest": {
            window: "#1a2f1a",
            windowText: "#c8e6c9",
            base: "#1e3a1e",
            alternateBase: "#254725",
            text: "#c8e6c9",
            button: "#2e5a2e",
            buttonText: "#c8e6c9",
            highlight: "#66bb6a",
            highlightedText: "#1a2f1a",
            mid: "#2e5a2e",
            accent: "#81c784",
            success: "#a5d6a7",
            error: "#ef9a9a",
            warning: "#fff59d",
            info: "#81d4fa",
            codeBackground: "#1a2f1a",
            codeText: "#a5d6a7",
        },
    })
    
    // Current theme colors (read-only computed properties)
    readonly property color window: themeColors[currentTheme].window
    readonly property color windowText: themeColors[currentTheme].windowText
    readonly property color base: themeColors[currentTheme].base
    readonly property color alternateBase: themeColors[currentTheme].alternateBase
    readonly property color text: themeColors[currentTheme].text
    readonly property color button: themeColors[currentTheme].button
    readonly property color buttonText: themeColors[currentTheme].buttonText
    readonly property color highlight: themeColors[currentTheme].highlight
    readonly property color highlightedText: themeColors[currentTheme].highlightedText
    readonly property color mid: themeColors[currentTheme].mid
    readonly property color accent: themeColors[currentTheme].accent
    readonly property color success: themeColors[currentTheme].success
    readonly property color error: themeColors[currentTheme].error
    readonly property color warning: themeColors[currentTheme].warning
    readonly property color info: themeColors[currentTheme].info
    readonly property color codeBackground: themeColors[currentTheme].codeBackground
    readonly property color codeText: themeColors[currentTheme].codeText
    
    // Helper to check if theme is dark
    readonly property bool isDark: {
        var bg = themeColors[currentTheme].window
        // Simple luminance check
        return currentTheme !== "light"
    }
    
    // Get theme icon
    function getThemeIcon(themeId) {
        for (var i = 0; i < themes.length; i++) {
            if (themes[i].id === themeId) return themes[i].icon
        }
        return "🎨"
    }
    
    // Get theme name
    function getThemeName(themeId) {
        for (var i = 0; i < themes.length; i++) {
            if (themes[i].id === themeId) return themes[i].name
        }
        return "Unknown"
    }
    
    // Set theme
    function setTheme(themeId) {
        if (themeColors[themeId]) {
            currentTheme = themeId
        }
    }
}
