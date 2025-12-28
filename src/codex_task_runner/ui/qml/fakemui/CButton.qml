import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: control
    
    property string variant: "default" // default, primary, secondary, ghost, danger, text
    property string size: "md" // sm, md, lg
    property string iconSource: ""
    property string iconText: "" // Alias for simpler icon usage (emoji/text icons)
    property bool loading: false
    
    // Effective icon: prefer iconText over iconSource
    readonly property string _effectiveIcon: iconText || iconSource
    
    implicitHeight: size === "sm" ? 32 : size === "lg" ? 44 : 36
    implicitWidth: Math.max(implicitHeight, contentRow.implicitWidth + (size === "sm" ? 16 : 24))
    
    font.pixelSize: size === "sm" ? 12 : size === "lg" ? 16 : 14
    font.weight: Font.Medium
    
    background: Rectangle {
        radius: 6
        color: {
            if (!control.enabled) return Theme.surface
            if (control.down) {
                switch(control.variant) {
                    case "primary": return Qt.darker(Theme.primary, 1.3)
                    case "secondary": return Qt.darker(Theme.success, 1.3)
                    case "danger": return Qt.darker(Theme.error, 1.3)
                    case "ghost": return Theme.actionSelected
                    case "text": return Theme.actionSelected
                    default: return Qt.darker(Theme.surface, 1.2)
                }
            }
            if (control.hovered) {
                switch(control.variant) {
                    case "primary": return Qt.darker(Theme.primary, 1.1)
                    case "secondary": return Qt.darker(Theme.success, 1.1)
                    case "danger": return Qt.darker(Theme.error, 1.1)
                    case "ghost": return Theme.actionHover
                    case "text": return Theme.actionHover
                    default: return Qt.lighter(Theme.surface, 1.1)
                }
            }
            switch(control.variant) {
                case "primary": return Theme.primary
                case "secondary": return Theme.success
                case "danger": return Theme.error
                case "ghost": return "transparent"
                case "text": return "transparent"
                default: return Theme.surface
            }
        }
        border.width: control.variant === "ghost" ? 1 : 0
        border.color: Theme.border
        
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
            visible: control._effectiveIcon && !control.loading
            text: control._effectiveIcon
            font.pixelSize: control.font.pixelSize
            color: control.enabled ? Theme.text : Theme.textDisabled
        }
        
        Text {
            text: control.text
            font: control.font
            color: control.enabled ? Theme.text : Theme.textDisabled
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    
    Behavior on opacity { NumberAnimation { duration: 150 } }
    opacity: enabled ? 1.0 : 0.5
}
