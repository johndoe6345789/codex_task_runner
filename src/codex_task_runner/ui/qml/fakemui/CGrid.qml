import QtQuick
import QtQuick.Layouts

/**
 * CGrid.qml - Responsive grid layout (mirrors _grid.scss)
 * CSS Grid-like component with auto-fill and fixed column options
 * 
 * Usage:
 *   // Fixed 3 columns
 *   CGrid {
 *       columns: 3
 *       gap: "md"
 *       
 *       Repeater {
 *           model: 9
 *           Rectangle { ... }
 *       }
 *   }
 *   
 *   // Auto-fill responsive grid
 *   CGrid {
 *       variant: "auto"
 *       minItemWidth: 300
 *       
 *       Repeater { ... }
 *   }
 */
Item {
    id: root
    
    // Public properties
    property string variant: "fixed"      // fixed, auto
    property int columns: 2               // Number of columns (for fixed variant)
    property string gap: "md"             // none, xs, sm, md, lg, xl or number
    property int minItemWidth: 320        // Minimum item width (for auto variant)
    property string align: "stretch"      // start, center, end, stretch
    
    // Content slot
    default property alias content: gridContainer.data
    
    // Computed gap value
    readonly property int _gap: {
        switch (gap) {
            case "none": return 0
            case "xs": return StyleVariables.spacingXs
            case "sm": return StyleVariables.spacingSm
            case "md": return StyleVariables.spacingMd
            case "lg": return StyleVariables.spacingLg
            case "xl": return StyleVariables.spacingXl
            default: return parseInt(gap) || StyleVariables.spacingMd
        }
    }
    
    // Calculate columns for auto variant based on width
    readonly property int _autoColumns: variant === "auto" 
        ? Math.max(1, Math.floor((width + _gap) / (minItemWidth + _gap)))
        : columns
    
    // Size
    implicitWidth: parent ? parent.width : 400
    implicitHeight: gridContainer.implicitHeight
    
    // Use Flow for auto-fill behavior, GridLayout for fixed
    GridLayout {
        id: gridContainer
        anchors.fill: parent
        columns: root.variant === "auto" ? root._autoColumns : root.columns
        rowSpacing: root._gap
        columnSpacing: root._gap
        
        // Note: Children should use Layout.fillWidth: true for proper sizing
    }
}
