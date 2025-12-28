import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    
    property int taskIndex: -1
    property string taskJson: ""
    property var taskData: taskJson ? JSON.parse(taskJson) : null
    property bool nerdMode: false
    
    signal archiveClicked()
    signal prClicked()
    signal patchClicked()
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        
        // Header with actions
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
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
                ToolTip.text: "Extract git patch (Ctrl+P)"
            }
            
            Button {
                text: "🔀 Create PR"
                enabled: taskIndex >= 0 && taskData && !taskData.pull_request
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
        
        // Task summary card
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: summaryColumn.implicitHeight + 24
            color: palette.alternateBase
            radius: 8
            visible: taskIndex >= 0 && taskData
            
            ColumnLayout {
                id: summaryColumn
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8
                
                // Title
                Label {
                    Layout.fillWidth: true
                    text: taskData ? (taskData.title || "Untitled Task") : ""
                    font.bold: true
                    font.pixelSize: 16
                    wrapMode: Text.Wrap
                }
                
                // Repository & Branch
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 16
                    
                    Label {
                        text: "📁 " + (taskData && taskData.repository ? taskData.repository.full_name : "")
                        opacity: 0.8
                        visible: taskData && taskData.repository
                        
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (taskData && taskData.repository) {
                                    app.openUrl("https://github.com/" + taskData.repository.full_name)
                                }
                            }
                        }
                    }
                    
                    Label {
                        text: "🌿 " + (taskData ? (taskData.head_branch || taskData.branch || "") : "")
                        opacity: 0.8
                        visible: taskData && (taskData.head_branch || taskData.branch)
                    }
                }
                
                // Status & PR
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 16
                    
                    // Status badge
                    Label {
                        text: taskData ? (taskData.status || "unknown") : ""
                        font.pixelSize: 12
                        padding: 4
                        leftPadding: 10
                        rightPadding: 10
                        background: Rectangle {
                            radius: 4
                            color: {
                                if (!taskData) return palette.mid
                                switch(taskData.status) {
                                    case "completed": return "#2d7d46"
                                    case "running": return "#1a73e8"
                                    case "failed": return "#c62828"
                                    case "queued": return "#f57c00"
                                    default: return palette.mid
                                }
                            }
                        }
                        color: "white"
                    }
                    
                    // PR link
                    Label {
                        text: "🔀 View Pull Request"
                        visible: taskData && taskData.pull_request
                        color: palette.highlight
                        
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            hoverEnabled: true
                            onClicked: {
                                var pr = taskData.pull_request
                                var url = pr.html_url || pr.url || ""
                                if (url) app.openUrl(url)
                            }
                            onEntered: parent.font.underline = true
                            onExited: parent.font.underline = false
                        }
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    // Created date
                    Label {
                        text: taskData && taskData.created_at ? ("Created: " + taskData.created_at.substring(0, 10)) : ""
                        opacity: 0.6
                        font.pixelSize: 12
                    }
                }
                
                // Nerd mode: extra info
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    visible: nerdMode && taskData
                    
                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: "#00ff41"
                        opacity: 0.3
                    }
                    
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 2
                        columnSpacing: 16
                        rowSpacing: 4
                        
                        Label {
                            text: "Task ID:"
                            opacity: 0.6
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                        Label {
                            text: taskData ? (taskData.id || "N/A") : "N/A"
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#00ff41"
                            Layout.fillWidth: true
                            elide: Text.ElideMiddle
                            
                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (taskData && taskData.id) {
                                        app.copyToClipboard(taskData.id)
                                    }
                                }
                            }
                        }
                        
                        Label {
                            text: "Turn ID:"
                            opacity: 0.6
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                        Label {
                            text: taskData && taskData.current_turn_id ? taskData.current_turn_id : "N/A"
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#00ff41"
                            Layout.fillWidth: true
                            elide: Text.ElideMiddle
                            
                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (taskData && taskData.current_turn_id) {
                                        app.copyToClipboard(taskData.current_turn_id)
                                    }
                                }
                            }
                        }
                        
                        Label {
                            text: "Env ID:"
                            opacity: 0.6
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                        Label {
                            text: taskData && taskData.environment_id ? taskData.environment_id : "N/A"
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#00ff41"
                            Layout.fillWidth: true
                            elide: Text.ElideMiddle
                        }
                        
                        Label {
                            text: "Created:"
                            opacity: 0.6
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                        Label {
                            text: taskData && taskData.created_at ? taskData.created_at : "N/A"
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                        
                        Label {
                            text: "Updated:"
                            opacity: 0.6
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                        Label {
                            text: taskData && taskData.updated_at ? taskData.updated_at : "N/A"
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#00ff41"
                        }
                    }
                }
            }
        }
        
        // Tabs for different views
        TabBar {
            id: tabBar
            Layout.fillWidth: true
            visible: taskIndex >= 0
            
            TabButton {
                text: "📝 Details"
            }
            TabButton {
                text: "💬 Prompt"
            }
            TabButton {
                text: "🔧 Raw JSON"
            }
        }
        
        // Tab content
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabBar.currentIndex
            visible: taskIndex >= 0
            
            // Details tab
            ScrollView {
                clip: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: 12
                    
                    // Turn info if available
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: turnsColumn.implicitHeight + 16
                        color: palette.window
                        radius: 4
                        visible: taskData && taskData.turns && taskData.turns.length > 0
                        
                        ColumnLayout {
                            id: turnsColumn
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 4
                            
                            Label {
                                text: "Turns: " + (taskData && taskData.turns ? taskData.turns.length : 0)
                                font.bold: true
                            }
                            
                            Label {
                                text: taskData && taskData.current_turn_id ? ("Current: " + taskData.current_turn_id.substring(0, 8) + "...") : ""
                                opacity: 0.7
                                font.pixelSize: 12
                            }
                        }
                    }
                    
                    // Placeholder for more structured details
                    Label {
                        Layout.fillWidth: true
                        text: "Select 'Raw JSON' tab to see full task details"
                        opacity: 0.5
                        horizontalAlignment: Text.AlignHCenter
                        visible: !(taskData && taskData.turns && taskData.turns.length > 0)
                    }
                }
            }
            
            // Prompt tab
            ScrollView {
                clip: true
                
                TextArea {
                    text: {
                        if (!taskData) return ""
                        // Try to find the prompt in various locations
                        if (taskData.prompt) return taskData.prompt
                        if (taskData.input_items) {
                            for (var i = 0; i < taskData.input_items.length; i++) {
                                var item = taskData.input_items[i]
                                if (item.content) {
                                    for (var j = 0; j < item.content.length; j++) {
                                        if (item.content[j].text) {
                                            return item.content[j].text
                                        }
                                    }
                                }
                            }
                        }
                        return taskData.title || "No prompt found"
                    }
                    readOnly: true
                    font.pixelSize: 14
                    wrapMode: Text.Wrap
                    selectByMouse: true
                    background: Rectangle {
                        color: palette.window
                        radius: 4
                    }
                }
            }
            
            // Raw JSON tab
            ScrollView {
                clip: true
                
                TextArea {
                    id: detailText
                    text: taskJson || "No task selected"
                    readOnly: true
                    font.family: "Menlo, Monaco, Consolas, monospace"
                    font.pixelSize: 12
                    wrapMode: Text.Wrap
                    selectByMouse: true
                    background: Rectangle {
                        color: "#1e1e1e"
                        radius: 4
                    }
                    color: "#d4d4d4"
                }
            }
        }
        
        // Empty state
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: taskIndex < 0
            
            Label {
                anchors.centerIn: parent
                text: "← Select a task to view details"
                opacity: 0.5
                font.pixelSize: 16
            }
        }
    }
}
