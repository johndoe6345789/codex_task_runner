import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: control
    
    property string variant: "default" // default, primary, secondary, ghost, danger
    property string size: "md" // sm, md, lg
    property string iconSource: ""
    property bool loading: false
    
    implicitHeight: size === "sm" ? 32 : size === "lg" ? 44 : 36
    implicitWidth: Math.max(implicitHeight, contentRow.implicitWidth + (size === "sm" ? 16 : 24))
    
    font.pixelSize: size === "sm" ? 12 : size === "lg" ? 16 : 14
    font.weight: Font.Medium
    
    background: Rectangle {
        radius: 6
        color: {
            if (!control.enabled) return "#2d2d2d"
            if (control.down) {
                switch(control.variant) {
                    case "primary": return "#1565c0"
                    case "secondary": return "#2e7d32"
                    case "danger": return "#c62828"
                    case "ghost": return "#3d3d3d"
                    default: return "#404040"
                }
            }
            if (control.hovered) {
                switch(control.variant) {
                    case "primary": return "#1976d2"
                    case "secondary": return "#388e3c"
                    case "danger": return "#d32f2f"
                    case "ghost": return "#2d2d2d"
                    default: return "#3d3d3d"
                }
            }
            switch(control.variant) {
                case "primary": return "#1a73e8"
                case "secondary": return "#4caf50"
                case "danger": return "#f44336"
                case "ghost": return "transparent"
                default: return "#2d2d2d"
            }
        }
        border.width: control.variant === "ghost" ? 1 : 0
        border.color: "#3d3d3d"
        
        Behavior on color { ColorAnimation { duration: 150 } }
    }
    
    contentItem: RowLayout {
        id: contentRow
        spacing: 6
        
        BusyIndicator {
            Layout.preferredWidth: 16
            Layout.preferredHeight: 16
            running: control.loading
            visible: control.loading
        }
        
        Text {
            visible: control.iconSource && !control.loading
            text: control.iconSource
            font.pixelSize: control.font.pixelSize
            color: control.enabled ? "#ffffff" : "#666666"
        }
        
        Text {
            text: control.text
            font: control.font
            color: control.enabled ? "#ffffff" : "#666666"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    
    Behavior on opacity { NumberAnimation { duration: 150 } }
    opacity: enabled ? 1.0 : 0.5
}
