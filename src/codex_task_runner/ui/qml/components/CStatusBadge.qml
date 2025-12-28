import QtQuick

Rectangle {
    id: badge
    
    property string status: "unknown" // completed, running, queued, failed, unknown
    property string text: status
    property bool showDot: true
    
    implicitHeight: 22
    implicitWidth: badgeRow.implicitWidth + 12
    radius: 4
    
    color: {
        switch(status) {
            case "completed": return "#1b5e20"
            case "running": return "#0d47a1"
            case "queued": return "#e65100"
            case "failed": return "#b71c1c"
            default: return "#424242"
        }
    }
    
    Row {
        id: badgeRow
        anchors.centerIn: parent
        spacing: 6
        
        // Animated dot for running status
        Rectangle {
            anchors.verticalCenter: parent.verticalCenter
            width: 6
            height: 6
            radius: 3
            color: "#ffffff"
            visible: badge.showDot && badge.status === "running"
            
            SequentialAnimation on opacity {
                running: badge.status === "running"
                loops: Animation.Infinite
                NumberAnimation { to: 0.3; duration: 500 }
                NumberAnimation { to: 1.0; duration: 500 }
            }
        }
        
        Text {
            text: badge.text
            font.pixelSize: 11
            font.weight: Font.Medium
            color: "#ffffff"
            textFormat: Text.PlainText
        }
    }
}
