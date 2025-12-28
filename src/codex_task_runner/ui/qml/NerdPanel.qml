import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    color: "#1a1a2e"
    
    property string sessionInfo: "{}"
    property alias logText: logArea.text
    
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
                color: "#00ff41"
                font.family: "Menlo, Monaco, Consolas, monospace"
            }
            
            Item { Layout.fillWidth: true }
            
            Label {
                text: "API Logs • Session Info • Debug"
                opacity: 0.6
                color: "#00ff41"
                font.pixelSize: 11
            }
        }
        
        // Tab bar for different nerd views
        TabBar {
            id: nerdTabs
            Layout.fillWidth: true
            
            background: Rectangle {
                color: "#0f0f1a"
            }
            
            TabButton {
                text: "📡 API Log"
                font.pixelSize: 11
                
                background: Rectangle {
                    color: nerdTabs.currentIndex === 0 ? "#2a2a4a" : "transparent"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: nerdTabs.currentIndex === 0 ? "#00ff41" : "#888"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
            
            TabButton {
                text: "🔐 Session"
                font.pixelSize: 11
                
                background: Rectangle {
                    color: nerdTabs.currentIndex === 1 ? "#2a2a4a" : "transparent"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: nerdTabs.currentIndex === 1 ? "#00ff41" : "#888"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
            
            TabButton {
                text: "⌨️ Shortcuts"
                font.pixelSize: 11
                
                background: Rectangle {
                    color: nerdTabs.currentIndex === 2 ? "#2a2a4a" : "transparent"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: nerdTabs.currentIndex === 2 ? "#00ff41" : "#888"
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
                            color: "#666"
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
                                color: "#ff6b6b"
                                horizontalAlignment: Text.AlignHCenter
                            }
                            background: Rectangle {
                                color: parent.hovered ? "#2a2a4a" : "transparent"
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
                                color: "#4dabf7"
                                horizontalAlignment: Text.AlignHCenter
                            }
                            background: Rectangle {
                                color: parent.hovered ? "#2a2a4a" : "transparent"
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
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 11
                            color: "#00ff41"
                            selectionColor: "#00ff41"
                            selectedTextColor: "#1a1a2e"
                            wrapMode: Text.NoWrap
                            selectByMouse: true
                            
                            background: Rectangle {
                                color: "#0f0f1a"
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
                            color: "#0f0f1a"
                            radius: 4
                            
                            ColumnLayout {
                                id: sessionCol
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 8
                                
                                Label {
                                    text: "Session Status"
                                    font.bold: true
                                    color: "#00ff41"
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
                                                return info.has_session ? "#00ff41" : "#ff6b6b"
                                            } catch(e) {
                                                return "#ff6b6b"
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
                                        color: "#ccc"
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
                                    color: "#888"
                                    font.pixelSize: 10
                                    font.family: "Menlo, Monaco, Consolas, monospace"
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
                                    color: "#888"
                                    font.pixelSize: 10
                                    font.family: "Menlo, Monaco, Consolas, monospace"
                                }
                            }
                        }
                        
                        // Raw session JSON
                        Label {
                            text: "Raw Session Info"
                            font.bold: true
                            color: "#00ff41"
                            font.pixelSize: 12
                        }
                        
                        TextArea {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 150
                            text: sessionInfo
                            readOnly: true
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#4dabf7"
                            wrapMode: Text.Wrap
                            selectByMouse: true
                            
                            background: Rectangle {
                                color: "#0f0f1a"
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
                            color: "#00ff41"
                            font.pixelSize: 12
                        }
                        
                        Repeater {
                            model: [
                                { key: "Ctrl+N", action: "New Task" },
                                { key: "Ctrl+R", action: "Refresh Tasks" },
                                { key: "F5", action: "Refresh Tasks" },
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
                                    color: "#2a2a4a"
                                    radius: 4
                                    
                                    Label {
                                        anchors.centerIn: parent
                                        text: modelData.key
                                        color: "#ffd43b"
                                        font.family: "Menlo, Monaco, Consolas, monospace"
                                        font.pixelSize: 11
                                    }
                                }
                                
                                Label {
                                    text: modelData.action
                                    color: "#ccc"
                                    font.pixelSize: 11
                                }
                            }
                        }
                        
                        Item { Layout.preferredHeight: 16 }
                        
                        Label {
                            text: "CLI Commands"
                            font.bold: true
                            color: "#00ff41"
                            font.pixelSize: 12
                        }
                        
                        TextArea {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 120
                            readOnly: true
                            font.family: "Menlo, Monaco, Consolas, monospace"
                            font.pixelSize: 10
                            color: "#4dabf7"
                            text: "codex tasks          # List tasks\ncodex task <id>      # Task detail\ncodex prompt \"...\"   # Create task\ncodex patch <id>     # Extract diff\ncodex yolo           # Auto-merge all\ncodex ui             # Launch this UI"
                            
                            background: Rectangle {
                                color: "#0f0f1a"
                                radius: 4
                            }
                        }
                    }
                }
            }
        }
    }
}
