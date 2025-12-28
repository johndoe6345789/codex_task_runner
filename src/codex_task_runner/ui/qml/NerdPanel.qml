import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    color: themeColors.background
    
    property string sessionInfo: "{}"
    property alias logText: logArea.text
    property var themeColors: ({
        background: "#1a1a2e",
        surface: "#252542",
        primary: "#4dabf7",
        secondary: "#69db7c",
        accent: "#ffd43b",
        text: "#ffffff",
        textMuted: "#888888",
        border: "#3d3d5c",
        success: "#51cf66",
        warning: "#fcc419",
        error: "#ff6b6b",
        nerd: "#00ff41"
    })
    
    function appendLog(msg) {
        logArea.text = logArea.text + msg + "\n"
        // Auto-scroll to bottom
        logArea.cursorPosition = logArea.length
    }
    
    function clearLogs() {
        logArea.text = ""
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 8
        
        // Header
        RowLayout {
            Layout.fillWidth: true
            
            Label {
                text: "🤓 NERD MODE"
                font.bold: true
                font.pixelSize: 14
                color: themeColors.nerd
                font.family: "Menlo"
            }
            
            Item { Layout.fillWidth: true }
            
            Label {
                text: "API Logs • Session Info • Debug"
                opacity: 0.6
                color: themeColors.nerd
                font.pixelSize: 11
            }
        }
        
        // Tab bar for different nerd views
        TabBar {
            id: nerdTabs
            Layout.fillWidth: true
            
            background: Rectangle {
                color: Qt.darker(themeColors.background, 1.2)
            }
            
            TabButton {
                text: "📡 API Log"
                font.pixelSize: 11
                
                background: Rectangle {
                    color: nerdTabs.currentIndex === 0 ? themeColors.surface : "transparent"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: nerdTabs.currentIndex === 0 ? themeColors.nerd : themeColors.textMuted
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
            
            TabButton {
                text: "🔐 Session"
                font.pixelSize: 11
                
                background: Rectangle {
                    color: nerdTabs.currentIndex === 1 ? themeColors.surface : "transparent"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: nerdTabs.currentIndex === 1 ? themeColors.nerd : themeColors.textMuted
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
            
            TabButton {
                text: "⌨️ Shortcuts"
                font.pixelSize: 11
                
                background: Rectangle {
                    color: nerdTabs.currentIndex === 2 ? themeColors.surface : "transparent"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: nerdTabs.currentIndex === 2 ? themeColors.nerd : themeColors.textMuted
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
        
        // Tab content
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: nerdTabs.currentIndex
            
            // API Log tab
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 4
                    
                    // Log controls
                    RowLayout {
                        Layout.fillWidth: true
                        
                        Label {
                            text: logArea.text.split('\n').length - 1 + " entries"
                            color: themeColors.textMuted
                            font.pixelSize: 10
                        }
                        
                        Item { Layout.fillWidth: true }
                        
                        Button {
                            text: "Clear"
                            flat: true
                            font.pixelSize: 10
                            onClicked: {
                                app.clearDebugLogs()
                                root.clearLogs()
                            }
                            
                            contentItem: Text {
                                text: parent.text
                                color: themeColors.error
                                horizontalAlignment: Text.AlignHCenter
                            }
                            background: Rectangle {
                                color: parent.hovered ? themeColors.surface : "transparent"
                                radius: 2
                            }
                        }
                        
                        Button {
                            text: "Copy"
                            flat: true
                            font.pixelSize: 10
                            onClicked: app.copyToClipboard(logArea.text)
                            
                            contentItem: Text {
                                text: parent.text
                                color: themeColors.primary
                                horizontalAlignment: Text.AlignHCenter
                            }
                            background: Rectangle {
                                color: parent.hovered ? themeColors.surface : "transparent"
                                radius: 2
                            }
                        }
                    }
                    
                    // Log output
                    ScrollView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        
                        TextArea {
                            id: logArea
                            readOnly: true
                            font.family: "Menlo"
                            font.pixelSize: 11
                            color: themeColors.nerd
                            selectionColor: themeColors.nerd
                            selectedTextColor: themeColors.background
                            wrapMode: Text.NoWrap
                            selectByMouse: true
                            
                            background: Rectangle {
                                color: Qt.darker(themeColors.background, 1.2)
                                radius: 4
                            }
                            
                            // Syntax highlighting simulation
                            text: ""
                        }
                    }
                }
            }
            
            // Session tab
            Item {
                ScrollView {
                    anchors.fill: parent
                    clip: true
                    
                    ColumnLayout {
                        width: parent.width
                        spacing: 12
                        
                        // Session status
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: sessionCol.implicitHeight + 16
                            color: Qt.darker(themeColors.background, 1.2)
                            radius: 4
                            
                            ColumnLayout {
                                id: sessionCol
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 8
                                
                                Label {
                                    text: "Session Status"
                                    font.bold: true
                                    color: themeColors.nerd
                                    font.pixelSize: 12
                                }
                                
                                RowLayout {
                                    spacing: 8
                                    
                                    Rectangle {
                                        width: 8
                                        height: 8
                                        radius: 4
                                        color: {
                                            try {
                                                var info = JSON.parse(sessionInfo)
                                                return info.has_session ? themeColors.success : themeColors.error
                                            } catch(e) {
                                                return themeColors.error
                                            }
                                        }
                                    }
                                    
                                    Label {
                                        text: {
                                            try {
                                                var info = JSON.parse(sessionInfo)
                                                return info.has_session ? "Connected" : "Not Connected"
                                            } catch(e) {
                                                return "Unknown"
                                            }
                                        }
                                        color: themeColors.text
                                        font.pixelSize: 11
                                    }
                                }
                                
                                Label {
                                    text: {
                                        try {
                                            var info = JSON.parse(sessionInfo)
                                            return "Cookie: " + (info.cookie_preview || "N/A")
                                        } catch(e) {
                                            return "Cookie: N/A"
                                        }
                                    }
                                    color: themeColors.textMuted
                                    font.pixelSize: 10
                                    font.family: "Menlo"
                                }
                                
                                Label {
                                    text: {
                                        try {
                                            var info = JSON.parse(sessionInfo)
                                            return "Base URL: " + (info.base_url || "N/A")
                                        } catch(e) {
                                            return "Base URL: N/A"
                                        }
                                    }
                                    color: themeColors.textMuted
                                    font.pixelSize: 10
                                    font.family: "Menlo"
                                }
                            }
                        }
                        
                        // Raw session JSON
                        Label {
                            text: "Raw Session Info"
                            font.bold: true
                            color: themeColors.nerd
                            font.pixelSize: 12
                        }
                        
                        TextArea {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 150
                            text: sessionInfo
                            readOnly: true
                            font.family: "Menlo"
                            font.pixelSize: 10
                            color: themeColors.primary
                            wrapMode: Text.Wrap
                            selectByMouse: true
                            
                            background: Rectangle {
                                color: Qt.darker(themeColors.background, 1.2)
                                radius: 4
                            }
                        }
                    }
                }
            }
            
            // Shortcuts tab
            Item {
                ScrollView {
                    anchors.fill: parent
                    clip: true
                    
                    ColumnLayout {
                        width: parent.width
                        spacing: 8
                        
                        Label {
                            text: "Keyboard Shortcuts"
                            font.bold: true
                            color: themeColors.nerd
                            font.pixelSize: 12
                        }
                        
                        Repeater {
                            model: [
                                { key: "Ctrl+N", action: "New Task" },
                                { key: "Ctrl+R", action: "Refresh Tasks" },
                                { key: "F5", action: "Refresh Tasks" },
                                { key: "Ctrl+T", action: "Toggle Theme" },
                                { key: "Ctrl+`", action: "Toggle Nerd Mode" },
                                { key: "Ctrl+Enter", action: "Send Prompt (in dialog)" },
                                { key: "Escape", action: "Close Dialog" },
                            ]
                            
                            delegate: RowLayout {
                                Layout.fillWidth: true
                                spacing: 16
                                
                                Rectangle {
                                    Layout.preferredWidth: 100
                                    Layout.preferredHeight: 24
                                    color: themeColors.surface
                                    radius: 4
                                    
                                    Label {
                                        anchors.centerIn: parent
                                        text: modelData.key
                                        color: themeColors.accent
                                        font.family: "Menlo"
                                        font.pixelSize: 11
                                    }
                                }
                                
                                Label {
                                    text: modelData.action
                                    color: themeColors.text
                                    font.pixelSize: 11
                                }
                            }
                        }
                        
                        Item { Layout.preferredHeight: 16 }
                        
                        Label {
                            text: "CLI Commands"
                            font.bold: true
                            color: themeColors.nerd
                            font.pixelSize: 12
                        }
                        
                        TextArea {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 120
                            readOnly: true
                            font.family: "Menlo"
                            font.pixelSize: 10
                            color: themeColors.primary
                            text: "codex tasks          # List tasks\ncodex task <id>      # Task detail\ncodex prompt \"...\"   # Create task\ncodex patch <id>     # Extract diff\ncodex yolo           # Auto-merge all\ncodex ui             # Launch this UI"
                            
                            background: Rectangle {
                                color: Qt.darker(themeColors.background, 1.2)
                                radius: 4
                            }
                        }
                    }
                }
            }
        }
    }
}
