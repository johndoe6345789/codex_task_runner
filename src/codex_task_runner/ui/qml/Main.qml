import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "Codex Task Runner" + (nerdMode ? " 🤓" : "")
    
    color: palette.window
    
    // Status bar message
    property string statusText: "Ready"
    property bool nerdMode: false
    
    Connections {
        target: app
        function onStatusMessage(msg) { statusText = msg }
        function onErrorOccurred(msg) { statusText = "Error: " + msg }
        function onPatchReady(patch) { patchDialog.show(patch) }
        function onTaskDetailLoaded(json) { detailPane.taskJson = json }
        function onEnvironmentsLoaded(envList) { sendPromptDialog.setEnvironments(envList) }
        function onPromptSuccess(taskId) { sendPromptDialog.showSuccess(taskId) }
        function onPromptError(msg) { sendPromptDialog.showError(msg) }
        function onNerdModeChanged(enabled) { nerdMode = enabled }
        function onDebugLog(msg) { nerdPanel.appendLog(msg) }
        function onSessionInfoChanged(info) { nerdPanel.sessionInfo = info }
    }
    
    Component.onCompleted: {
        app.loadTasks()
    }
    
    // Main layout
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // Toolbar
        ToolBar {
            Layout.fillWidth: true
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 4
                spacing: 8
                
                ToolButton {
                    text: "↻ Refresh"
                    onClicked: app.loadTasks()
                }
                
                ToolSeparator {}
                
                ToolButton {
                    text: "✨ New Task"
                    highlighted: true
                    onClicked: {
                        app.loadEnvironments()
                        sendPromptDialog.open()
                    }
                    ToolTip.visible: hovered
                    ToolTip.text: "Create a new Codex task with a prompt"
                }
                
                ToolButton {
                    text: "🌐 Open Codex"
                    onClicked: app.openCodexBrowser()
                    ToolTip.visible: hovered
                    ToolTip.text: "Open Codex web interface"
                }
                
                Item { Layout.fillWidth: true }
                
                Switch {
                    id: autoRefresh
                    text: "Auto-refresh"
                    onCheckedChanged: app.setPolling(checked)
                }
                
                ToolSeparator {}
                
                ToolButton {
                    id: nerdModeButton
                    text: nerdMode ? "🤓 Nerd" : "🤓"
                    checkable: true
                    checked: nerdMode
                    onCheckedChanged: app.setNerdMode(checked)
                    ToolTip.visible: hovered
                    ToolTip.text: "Toggle Nerd Mode (Ctrl+`)"
                    
                    background: Rectangle {
                        color: nerdMode ? "#1a1a2e" : "transparent"
                        radius: 4
                        border.color: nerdMode ? "#00ff41" : "transparent"
                        border.width: 1
                    }
                }
            }
        }
        
        // Main content with optional nerd panel
        SplitView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            orientation: Qt.Vertical
            
            // Top section: task list and detail
            SplitView {
                SplitView.fillHeight: !nerdMode
                SplitView.preferredHeight: nerdMode ? parent.height * 0.65 : parent.height
                orientation: Qt.Horizontal
                
                // Task list
                Rectangle {
                    SplitView.preferredWidth: 400
                    SplitView.minimumWidth: 300
                    color: palette.base
                    
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 4
                        
                        RowLayout {
                            Layout.fillWidth: true
                            
                            Label {
                                text: "Tasks"
                                font.bold: true
                                font.pixelSize: 16
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Label {
                                text: taskList.count + " tasks"
                                opacity: 0.6
                                font.pixelSize: 12
                            }
                        }
                        
                        ListView {
                            id: taskList
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            model: app.taskModel
                            currentIndex: -1
                            
                            delegate: ItemDelegate {
                                width: taskList.width
                                height: nerdMode ? 95 : 80
                                highlighted: ListView.isCurrentItem
                                
                                onClicked: {
                                    taskList.currentIndex = index
                                    app.loadTaskDetail(index)
                                }
                                
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    spacing: 2
                                    
                                    RowLayout {
                                        Layout.fillWidth: true
                                        
                                        Label {
                                            text: "#" + model.alias
                                            font.bold: true
                                            color: palette.highlight
                                        }
                                        
                                        Label {
                                            Layout.fillWidth: true
                                            text: model.title || "Untitled"
                                            elide: Text.ElideRight
                                            font.bold: true
                                        }
                                        
                                        // PR indicator
                                        Label {
                                            text: "🔀"
                                            visible: model.hasPr
                                            ToolTip.visible: prMouseArea.containsMouse
                                            ToolTip.text: "Has pull request"
                                            
                                            MouseArea {
                                                id: prMouseArea
                                                anchors.fill: parent
                                                hoverEnabled: true
                                                cursorShape: model.prUrl ? Qt.PointingHandCursor : Qt.ArrowCursor
                                                onClicked: {
                                                    if (model.prUrl) {
                                                        app.openUrl(model.prUrl)
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    
                                    // Nerd mode: show task ID
                                    Label {
                                        Layout.fillWidth: true
                                        text: model.taskId || ""
                                        elide: Text.ElideMiddle
                                        opacity: 0.5
                                        font.pixelSize: 9
                                        font.family: "Menlo, Monaco, Consolas, monospace"
                                        visible: nerdMode
                                        color: "#00ff41"
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: model.repo || ""
                                        elide: Text.ElideRight
                                        opacity: 0.7
                                        font.pixelSize: 12
                                    }
                                    
                                    RowLayout {
                                        Layout.fillWidth: true
                                        
                                        Label {
                                            text: model.status || ""
                                            font.pixelSize: 11
                                            padding: 2
                                            leftPadding: 6
                                            rightPadding: 6
                                            background: Rectangle {
                                                radius: 3
                                                color: {
                                                    switch(model.status) {
                                                        case "completed": return "#2d7d46"
                                                        case "running": return "#1a73e8"
                                                        case "failed": return "#c62828"
                                                        default: return palette.mid
                                                    }
                                                }
                                            }
                                            color: "white"
                                        }
                                        
                                        Label {
                                            text: model.branch || ""
                                            elide: Text.ElideRight
                                            opacity: 0.5
                                            font.pixelSize: 11
                                        }
                                        
                                        Item { Layout.fillWidth: true }
                                        
                                        Label {
                                            text: model.created || ""
                                            opacity: 0.5
                                            font.pixelSize: 11
                                        }
                                    }
                                }
                            }
                            
                            ScrollBar.vertical: ScrollBar {}
                        }
                    }
                }
                
                // Detail pane
                Rectangle {
                    SplitView.fillWidth: true
                    color: palette.base
                    
                    DetailPane {
                        id: detailPane
                        anchors.fill: parent
                        anchors.margins: 8
                        taskIndex: taskList.currentIndex
                        nerdMode: window.nerdMode
                        onArchiveClicked: app.archiveTask(taskIndex)
                        onPrClicked: app.createPR(taskIndex)
                        onPatchClicked: app.extractPatch(taskIndex)
                    }
                }
            }
            
            // Nerd panel (bottom)
            NerdPanel {
                id: nerdPanel
                SplitView.preferredHeight: 250
                SplitView.minimumHeight: 150
                visible: nerdMode
            }
        }
        
        // Status bar
        Rectangle {
            Layout.fillWidth: true
            height: 28
            color: nerdMode ? "#1a1a2e" : palette.mid
            
            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 8
                anchors.rightMargin: 8
                
                Label {
                    text: statusText
                    verticalAlignment: Text.AlignVCenter
                    opacity: 0.8
                    color: nerdMode ? "#00ff41" : palette.windowText
                }
                
                Item { Layout.fillWidth: true }
                
                Label {
                    text: nerdMode ? "Ctrl+N: New | Ctrl+R: Refresh | Ctrl+`: Nerd" : "Ctrl+N: New Task | Ctrl+R: Refresh"
                    opacity: 0.5
                    font.pixelSize: 11
                    color: nerdMode ? "#00ff41" : palette.windowText
                }
            }
        }
    }
    
    // Patch dialog
    PatchDialog {
        id: patchDialog
    }
    
    // Send prompt dialog
    SendPromptDialog {
        id: sendPromptDialog
        onPromptSubmitted: function(prompt, envId, branch, bestOf) {
            app.sendPrompt(prompt, envId, branch, bestOf)
        }
    }
    
    // Keyboard shortcuts
    Shortcut {
        sequence: "Ctrl+N"
        onActivated: {
            app.loadEnvironments()
            sendPromptDialog.open()
        }
    }
    
    Shortcut {
        sequence: "Ctrl+R"
        onActivated: app.loadTasks()
    }
    
    Shortcut {
        sequence: "F5"
        onActivated: app.loadTasks()
    }
    
    Shortcut {
        sequence: "Ctrl+`"
        onActivated: {
            nerdModeButton.checked = !nerdModeButton.checked
        }
    }
}
