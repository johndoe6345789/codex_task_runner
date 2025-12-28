import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    
    property int taskIndex: -1
    property string taskJson: ""
    
    signal archiveClicked()
    signal prClicked()
    signal patchClicked()
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 8
        
        // Header with actions
        RowLayout {
            Layout.fillWidth: true
            
            Label {
                text: taskIndex >= 0 ? "Task #" + (taskIndex + 1) : "Select a task"
                font.bold: true
                font.pixelSize: 18
            }
            
            Item { Layout.fillWidth: true }
            
            Button {
                text: "📋 Patch"
                enabled: taskIndex >= 0
                onClicked: root.patchClicked()
                ToolTip.visible: hovered
                ToolTip.text: "Extract git patch"
            }
            
            Button {
                text: "🔀 PR"
                enabled: taskIndex >= 0
                onClicked: root.prClicked()
                ToolTip.visible: hovered
                ToolTip.text: "Create pull request"
            }
            
            Button {
                text: "✓ Archive"
                enabled: taskIndex >= 0
                onClicked: root.archiveClicked()
                ToolTip.visible: hovered
                ToolTip.text: "Archive this task"
            }
        }
        
        // JSON detail view
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            
            TextArea {
                id: detailText
                text: taskJson || "No task selected"
                readOnly: true
                font.family: "Menlo"
                font.pixelSize: 12
                wrapMode: Text.Wrap
                selectByMouse: true
            }
        }
    }
}
