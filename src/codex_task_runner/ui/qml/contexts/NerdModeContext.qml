pragma Singleton
import QtQuick

/**
 * NerdModeContext - Toggle for showing technical details
 * Mirrors React's NerdModeContext from App.jsx
 */
QtObject {
    id: nerdModeContext
    
    // Nerd mode state - shows raw JSON, task IDs, debug info
    property bool nerdMode: {
        const saved = _settings.value("nerdMode", "false")
        return saved === "true"
    }
    
    // Settings for persistence
    property Settings _settings: Settings {
        category: "nerdMode"
    }
    
    /**
     * Set nerd mode and persist
     */
    function setNerdMode(enabled) {
        nerdMode = enabled
        _settings.setValue("nerdMode", enabled ? "true" : "false")
    }
    
    /**
     * Toggle nerd mode
     */
    function toggle() {
        setNerdMode(!nerdMode)
    }
}
