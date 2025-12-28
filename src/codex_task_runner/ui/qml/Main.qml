import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "Codex Task Runner" + (nerdMode ? " 🤓" : "")
    
    // Theme state
    property string currentTheme: "system"
    property var themeColors: getThemeColors(currentTheme)
    
    color: themeColors.window
    
    // Theme definitions
    readonly property var allThemes: ({
        "system": {
            window: "#2b2b2b",
            windowText: "#ffffff",
            base: "#1e1e1e",
            alternateBase: "#353535",
            text: "#ffffff",
            highlight: "#0078d4",
            mid: "#3c3c3c",
            accent: "#0078d4",
            success: "#2d7d46",
            error: "#c62828",
            warning: "#f57c00",
            info: "#1a73e8",
            codeBackground: "#1e1e1e",
            codeText: "#d4d4d4",
        },
        "light": {
            window: "#f5f5f5",
            windowText: "#1a1a1a",
            base: "#ffffff",
            alternateBase: "#f0f0f0",
            text: "#1a1a1a",
            highlight: "#0078d4",
            mid: "#d0d0d0",
            accent: "#0078d4",
            success: "#2d7d46",
            error: "#c62828",
            warning: "#f57c00",
            info: "#1a73e8",
            codeBackground: "#f8f8f8",
            codeText: "#333333",
        },
        "dark": {
            window: "#1e1e1e",
            windowText: "#e0e0e0",
            base: "#252526",
            alternateBase: "#2d2d30",
            text: "#e0e0e0",
            highlight: "#264f78",
            mid: "#3c3c3c",
            accent: "#569cd6",
            success: "#4ec9b0",
            error: "#f14c4c",
            warning: "#cca700",
            info: "#3794ff",
            codeBackground: "#1e1e1e",
            codeText: "#d4d4d4",
        },
        "hacker": {
            window: "#0a0a0f",
            windowText: "#00ff41",
            base: "#0d0d14",
            alternateBase: "#151520",
            text: "#00ff41",
            highlight: "#00ff41",
            mid: "#1a1a2e",
            accent: "#00ff41",
            success: "#00ff41",
            error: "#ff0055",
            warning: "#ffcc00",
            info: "#00ccff",
            codeBackground: "#0a0a0f",
            codeText: "#00ff41",
        },
        "ocean": {
            window: "#0d1b2a",
            windowText: "#e0e1dd",
            base: "#1b263b",
            alternateBase: "#273549",
            text: "#e0e1dd",
            highlight: "#778da9",
            mid: "#415a77",
            accent: "#4dabf7",
            success: "#40c057",
            error: "#fa5252",
            warning: "#fab005",
            info: "#4dabf7",
            codeBackground: "#0d1b2a",
            codeText: "#a9d1f7",
        },
        "sunset": {
            window: "#1a1423",
            windowText: "#ffd6ba",
            base: "#241b2f",
            alternateBase: "#2e243a",
            text: "#ffd6ba",
            highlight: "#ff7b54",
            mid: "#3d2c4a",
            accent: "#ff7b54",
            success: "#7ec8ac",
            error: "#ff6b6b",
            warning: "#feca57",
            info: "#48dbfb",
            codeBackground: "#1a1423",
            codeText: "#ffb997",
        },
        "forest": {
            window: "#1a2f1a",
            windowText: "#c8e6c9",
            base: "#1e3a1e",
            alternateBase: "#254725",
            text: "#c8e6c9",
            highlight: "#66bb6a",
            mid: "#2e5a2e",
            accent: "#81c784",
            success: "#a5d6a7",
            error: "#ef9a9a",
            warning: "#fff59d",
            info: "#81d4fa",
            codeBackground: "#1a2f1a",
            codeText: "#a5d6a7",
        },
    })
    
    function getThemeColors(themeId) {
        return allThemes[themeId] || allThemes["system"]
    }
    
    function getThemeIcon(themeId) {
        var icons = {
            "system": "💻",
            "light": "☀️",
            "dark": "🌙",
            "hacker": "🤓",
            "ocean": "🌊",
            "sunset": "🌅",
            "forest": "🌲"
        }
        return icons[themeId] || "🎨"
    }
    
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
        function onThemeChanged(themeId) { 
            currentTheme = themeId
            themeColors = getThemeColors(themeId)
        }
    }
    
    Component.onCompleted: {
        app.loadTasks()
        // Load saved theme
        var saved = app.getSavedTheme()
        if (saved) {
            currentTheme = saved
            themeColors = getThemeColors(saved)
        }
    }
    
    // Main layout
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // Toolbar
        ToolBar {
            Layout.fillWidth: true
            background: Rectangle {
                color: themeColors.mid
            }
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 4
                spacing: 8
                
                ToolButton {
                    text: "↻ Refresh"
                    onClicked: app.loadTasks()
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
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
                    
                    background: Rectangle {
                        color: themeColors.accent
                        radius: 4
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                ToolButton {
                    text: "🌐 Open Codex"
                    onClicked: app.openCodexBrowser()
                    ToolTip.visible: hovered
                    ToolTip.text: "Open Codex web interface"
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Item { Layout.fillWidth: true }
                
                // Theme selector button
                ToolButton {
                    id: themeButton
                    text: getThemeIcon(currentTheme) + " Theme"
                    onClicked: themeSelector.open()
                    ToolTip.visible: hovered
                    ToolTip.text: "Change theme (Ctrl+T)"
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    ThemeSelector {
                        id: themeSelector
                        x: -width + parent.width
                        y: parent.height + 4
                        currentTheme: window.currentTheme
                        
                        onThemeSelected: function(themeId) {
                            window.currentTheme = themeId
                            window.themeColors = getThemeColors(themeId)
                            app.setTheme(themeId)
                        }
                    }
                }
                
                ToolSeparator {}
                
                Switch {
                    id: autoRefresh
                    text: "Auto-refresh"
                    onCheckedChanged: app.setPolling(checked)
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        leftPadding: parent.indicator.width + parent.spacing
                        verticalAlignment: Text.AlignVCenter
                    }
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
                        color: nerdMode ? themeColors.codeBackground : "transparent"
                        radius: 4
                        border.color: nerdMode ? themeColors.accent : "transparent"
                        border.width: 1
                    }
                    contentItem: Text {
                        text: parent.text
                        color: nerdMode ? themeColors.accent : themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
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
                    color: themeColors.base
                    
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
                                color: themeColors.windowText
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Label {
                                text: taskList.count + " tasks"
                                opacity: 0.6
                                font.pixelSize: 12
                                color: themeColors.windowText
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
                                
                                background: Rectangle {
                                    color: parent.highlighted ? themeColors.highlight : (parent.hovered ? themeColors.alternateBase : "transparent")
                                    radius: 4
                                }
                                
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
                                            color: themeColors.accent
                                        }
                                        
                                        Label {
                                            Layout.fillWidth: true
                                            text: model.title || "Untitled"
                                            elide: Text.ElideRight
                                            font.bold: true
                                            color: themeColors.windowText
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
                                        color: themeColors.accent
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: model.repo || ""
                                        elide: Text.ElideRight
                                        opacity: 0.7
                                        font.pixelSize: 12
                                        color: themeColors.windowText
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
                                                        case "completed": return themeColors.success
                                                        case "running": return themeColors.info
                                                        case "failed": return themeColors.error
                                                        default: return themeColors.mid
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
                                            color: themeColors.windowText
                                        }
                                        
                                        Item { Layout.fillWidth: true }
                                        
                                        Label {
                                            text: model.created || ""
                                            opacity: 0.5
                                            font.pixelSize: 11
                                            color: themeColors.windowText
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
                    color: themeColors.base
                    
                    DetailPane {
                        id: detailPane
                        anchors.fill: parent
                        anchors.margins: 8
                        taskIndex: taskList.currentIndex
                        nerdMode: window.nerdMode
                        themeColors: window.themeColors
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
                themeColors: window.themeColors
            }
        }
        
        // Status bar
        Rectangle {
            Layout.fillWidth: true
            height: 28
            color: themeColors.mid
            
            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 8
                anchors.rightMargin: 8
                
                Label {
                    text: statusText
                    verticalAlignment: Text.AlignVCenter
                    opacity: 0.8
                    color: themeColors.windowText
                }
                
                Item { Layout.fillWidth: true }
                
                Label {
                    text: nerdMode ? "Ctrl+N: New | Ctrl+R: Refresh | Ctrl+T: Theme | Ctrl+`: Nerd" : "Ctrl+N: New | Ctrl+R: Refresh | Ctrl+T: Theme"
                    opacity: 0.5
                    font.pixelSize: 11
                    color: themeColors.windowText
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
    
    Shortcut {
        sequence: "Ctrl+T"
        onActivated: themeSelector.open()
    }
}
