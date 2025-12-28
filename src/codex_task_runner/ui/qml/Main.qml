import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "Codex Task Runner"
    
    color: palette.window
    
    // Status bar message
    property string statusText: "Ready"
    
    Connections {
        target: app
        function onStatusMessage(msg) { statusText = msg }
        function onErrorOccurred(msg) { statusText = "Error: " + msg }
        function onPatchReady(patch) { patchDialog.show(patch) }
        function onTaskDetailLoaded(json) { detailPane.taskJson = json }
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
                
                ToolButton {
                    text: "🌐 New Task"
                    onClicked: app.openCodexBrowser()
                    ToolTip.visible: hovered
                    ToolTip.text: "Opens Codex in browser (task creation uses WebSocket)"
                }
                
                Item { Layout.fillWidth: true }
                
                Switch {
                    id: autoRefresh
                    text: "Auto-refresh"
                    onCheckedChanged: app.setPolling(checked)
                }
            }
        }
        
        // Main content
        SplitView {
            Layout.fillWidth: true
            Layout.fillHeight: true
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
                    
                    Label {
                        text: "Tasks"
                        font.bold: true
                        font.pixelSize: 16
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
                            height: 72
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
                    onArchiveClicked: app.archiveTask(taskIndex)
                    onPrClicked: app.createPR(taskIndex)
                    onPatchClicked: app.extractPatch(taskIndex)
                }
            }
        }
        
        // Status bar
        Rectangle {
            Layout.fillWidth: true
            height: 24
            color: palette.mid
            
            Label {
                anchors.fill: parent
                anchors.leftMargin: 8
                text: statusText
                verticalAlignment: Text.AlignVCenter
                opacity: 0.8
            }
        }
    }
    
    // Patch dialog
    PatchDialog {
        id: patchDialog
    }
}
