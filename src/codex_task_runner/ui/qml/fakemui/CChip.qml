import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: chip
    
    property string text: ""
    property string icon: ""
    property string variant: "default" // default, success, warning, error, info, primary
    property string size: "sm" // sm, md
    property bool clickable: false
    property bool closable: false
    
    signal clicked()
    signal closeClicked()
    
    implicitHeight: size === "sm" ? 24 : 32
    implicitWidth: chipRow.implicitWidth + (size === "sm" ? 16 : 20)
    radius: height / 2
    
    color: {
        switch(variant) {
            case "success": return "#1b5e20"
            case "warning": return "#e65100"
            case "error": return "#b71c1c"
            case "info": return "#0d47a1"
            case "primary": return "#1565c0"
            default: return "#2d2d2d"
        }
    }
    
    Behavior on color { ColorAnimation { duration: 150 } }
    
    MouseArea {
        anchors.fill: parent
        hoverEnabled: chip.clickable
        cursorShape: chip.clickable ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: if (chip.clickable) chip.clicked()
    }
    
    RowLayout {
        id: chipRow
        anchors.centerIn: parent
        spacing: 4
        
        Text {
            text: chip.icon
            font.pixelSize: chip.size === "sm" ? 12 : 14
            color: "#ffffff"
            visible: chip.icon
        }
        
        Text {
            text: chip.text
            font.pixelSize: chip.size === "sm" ? 11 : 13
            font.weight: Font.Medium
            color: "#ffffff"
        }
        
        Text {
            text: "✕"
            font.pixelSize: chip.size === "sm" ? 10 : 12
            color: "#cccccc"
            visible: chip.closable
            
            MouseArea {
                anchors.fill: parent
                anchors.margins: -4
                cursorShape: Qt.PointingHandCursor
                onClicked: chip.closeClicked()
            }
        }
    }
}
