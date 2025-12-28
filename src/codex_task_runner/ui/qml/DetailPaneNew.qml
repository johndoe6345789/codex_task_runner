import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components" as C

Item {
    id: root
    
    property int taskIndex: -1
    property string taskJson: ""
    property var taskData: taskJson ? JSON.parse(taskJson) : null
    property bool nerdMode: false
    property var themeColors
    property var tr
    
    signal archiveClicked()
    signal prClicked()
    signal patchClicked()
    
    // Empty state
    C.CEmptyState {
        anchors.centerIn: parent
        visible: taskIndex < 0
        icon: "👈"
        title: tr.selectTask || "Select a task"
        description: "Choose a task from the list to view its details"
    }
    
    // Main content
    ColumnLayout {
        anchors.fill: parent
        spacing: 16
        visible: taskIndex >= 0
        
        // Header card
        C.CCard {
            Layout.fillWidth: true
            elevated: true
            
            content: Component {
                ColumnLayout {
                    spacing: 12
                    
                    // Title row
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        
                        Text {
                            Layout.fillWidth: true
                            text: taskData ? (taskData.title || "Untitled Task") : ""
                            font.pixelSize: 18
                            font.weight: Font.Bold
                            color: "#ffffff"
                            wrapMode: Text.Wrap
                        }
                        
                        C.CStatusBadge {
                            status: taskData ? (taskData.status || "unknown") : "unknown"
                        }
                    }
                    
                    // Repo and branch row
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 16
                        
                        C.CChip {
                            text: taskData && taskData.repository ? taskData.repository.full_name : "No repo"
                            icon: "📁"
                            clickable: taskData && taskData.repository
                            onClicked: {
                                if (taskData && taskData.repository) {
                                    app.openUrl("https://github.com/" + taskData.repository.full_name)
                                }
                            }
                        }
                        
                        C.CChip {
                            text: taskData ? (taskData.head_branch || taskData.branch || "No branch") : ""
                            icon: "🌿"
                            visible: taskData && (taskData.head_branch || taskData.branch)
                        }
                        
                        Item { Layout.fillWidth: true }
                        
                        Text {
                            text: taskData && taskData.created_at ? taskData.created_at.substring(0, 10) : ""
                            font.pixelSize: 12
                            color: "#888888"
                        }
                    }
                    
                    // PR link if exists
                    RowLayout {
                        Layout.fillWidth: true
                        visible: taskData && taskData.pull_request
                        
                        C.CChip {
                            text: "View Pull Request"
                            icon: "🔀"
                            variant: "success"
                            clickable: true
                            onClicked: {
                                var pr = taskData.pull_request
                                var url = pr.html_url || pr.url || ""
                                if (url) app.openUrl(url)
                            }
                        }
                    }
                    
                    // Nerd mode extra info
                    Rectangle {
                        Layout.fillWidth: true
                        height: nerdGrid.implicitHeight + 16
                        color: "#0d1117"
                        radius: 6
                        border.width: 1
                        border.color: "#00ff41"
                        visible: nerdMode && taskData
                        opacity: 0.9
                        
                        GridLayout {
                            id: nerdGrid
                            anchors.fill: parent
                            anchors.margins: 8
                            columns: 2
                            columnSpacing: 16
                            rowSpacing: 4
                            
                            Text { text: "Task ID:"; font.pixelSize: 10; color: "#00ff41"; opacity: 0.6 }
                            Text {
                                text: taskData ? (taskData.id || "N/A") : "N/A"
                                font.pixelSize: 10
                                font.family: "Menlo"
                                color: "#00ff41"
                                Layout.fillWidth: true
                                elide: Text.ElideMiddle
                                
                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: taskData && taskData.id && app.copyToClipboard(taskData.id)
                                }
                            }
                            
                            Text { text: "Turn ID:"; font.pixelSize: 10; color: "#00ff41"; opacity: 0.6 }
                            Text {
                                text: taskData && taskData.current_turn_id ? taskData.current_turn_id : "N/A"
                                font.pixelSize: 10
                                font.family: "Menlo"
                                color: "#00ff41"
                                Layout.fillWidth: true
                                elide: Text.ElideMiddle
                            }
                            
                            Text { text: "Env ID:"; font.pixelSize: 10; color: "#00ff41"; opacity: 0.6 }
                            Text {
                                text: taskData && taskData.environment_id ? taskData.environment_id : "N/A"
                                font.pixelSize: 10
                                font.family: "Menlo"
                                color: "#00ff41"
                                Layout.fillWidth: true
                                elide: Text.ElideMiddle
                            }
                        }
                    }
                }
            }
        }
        
        // Action buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
            C.CButton {
                text: "📋 " + (tr.patch || "Patch")
                enabled: taskIndex >= 0
                onClicked: root.patchClicked()
            }
            
            C.CButton {
                text: "🔀 " + (tr.createPR || "Create PR")
                variant: "primary"
                enabled: taskIndex >= 0 && taskData && !taskData.pull_request
                onClicked: root.prClicked()
            }
            
            C.CButton {
                text: "✓ " + (tr.archive || "Archive")
                variant: "secondary"
                enabled: taskIndex >= 0
                onClicked: root.archiveClicked()
            }
            
            Item { Layout.fillWidth: true }
        }
        
        // Tabs
        C.CTabBar {
            id: tabBar
            Layout.fillWidth: true
            tabs: [
                {label: tr.details || "Details", icon: "📝"},
                {label: tr.prompt || "Prompt", icon: "💬"},
                {label: tr.rawJson || "JSON", icon: "🔧"}
            ]
        }
        
        // Tab content
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabBar.currentIndex
            
            // Details tab
            ScrollView {
                clip: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: 12
                    
                    C.CCard {
                        Layout.fillWidth: true
                        title: "Turns"
                        visible: taskData && taskData.turns && taskData.turns.length > 0
                        
                        content: Component {
                            ColumnLayout {
                                spacing: 4
                                
                                Text {
                                    text: "Total turns: " + (taskData && taskData.turns ? taskData.turns.length : 0)
                                    font.pixelSize: 13
                                    color: "#ffffff"
                                }
                                
                                Text {
                                    text: taskData && taskData.current_turn_id ? ("Current: " + taskData.current_turn_id.substring(0, 12) + "...") : ""
                                    font.pixelSize: 12
                                    color: "#888888"
                                }
                            }
                        }
                    }
                    
                    C.CEmptyState {
                        Layout.fillWidth: true
                        visible: !(taskData && taskData.turns && taskData.turns.length > 0)
                        icon: "📄"
                        title: "No turn data"
                        description: "Check the JSON tab for full task details"
                    }
                }
            }
            
            // Prompt tab
            ScrollView {
                clip: true
                
                Rectangle {
                    width: parent.width
                    height: Math.max(promptText.implicitHeight + 24, parent.height)
                    color: "#1e1e1e"
                    radius: 8
                    
                    TextArea {
                        id: promptText
                        anchors.fill: parent
                        anchors.margins: 12
                        text: {
                            if (!taskData) return ""
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
                        color: "#ffffff"
                        wrapMode: Text.Wrap
                        selectByMouse: true
                        background: Item {}
                    }
                }
            }
            
            // JSON tab
            ScrollView {
                clip: true
                
                Rectangle {
                    width: parent.width
                    height: Math.max(jsonText.implicitHeight + 24, parent.height)
                    color: "#0d1117"
                    radius: 8
                    
                    TextArea {
                        id: jsonText
                        anchors.fill: parent
                        anchors.margins: 12
                        text: taskJson || "No task selected"
                        readOnly: true
                        font.family: "Menlo"
                        font.pixelSize: 11
                        color: "#e6edf3"
                        wrapMode: Text.Wrap
                        selectByMouse: true
                        background: Item {}
                    }
                }
            }
        }
    }
}
