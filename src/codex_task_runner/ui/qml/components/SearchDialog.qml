import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../contexts"
import "../fakemui"

/**
 * SearchDialog.qml - Search dialog with task and code results
 * Mirrors React's SearchDialog.jsx
 */
Dialog {
    id: root
    
    property string apiBase: ""
    signal taskSelected(string taskId)
    
    title: LanguageContext.t("search")
    modal: true
    standardButtons: Dialog.Close
    width: 600
    height: 500
    
    // Search state
    property string query: ""
    property var taskResults: []
    property var codeResults: []
    property bool loading: false
    property int activeTab: 0 // 0: tasks, 1: code
    
    // Debounce timer
    Timer {
        id: searchTimer
        interval: 300
        onTriggered: performSearch()
    }
    
    function performSearch() {
        if (!query.trim()) {
            taskResults = []
            codeResults = []
            return
        }
        
        loading = true
        
        const reqId = AjaxQueueContext.addRequest("Searching: " + query)
        
        const xhr = new XMLHttpRequest()
        xhr.open("GET", apiBase + "/search?q=" + encodeURIComponent(query))
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                loading = false
                if (xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText)
                    taskResults = data.tasks || []
                    codeResults = data.code || []
                    AjaxQueueContext.updateRequest(reqId, { status: "success" })
                } else {
                    taskResults = []
                    codeResults = []
                    AjaxQueueContext.updateRequest(reqId, { status: "error", error: "Search failed" })
                }
            }
        }
        xhr.send()
    }
    
    function highlightMatch(text, searchQuery) {
        if (!searchQuery || !text) return text
        const regex = new RegExp("(" + searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ")", "gi")
        return text.replace(regex, "<b style='color:" + Theme.primary + "'>$1</b>")
    }
    
    onOpened: {
        searchInput.forceActiveFocus()
    }
    
    onClosed: {
        query = ""
        taskResults = []
        codeResults = []
    }
    
    background: Rectangle {
        color: Theme.surface
        radius: 8
        border.color: Theme.border
    }
    
    header: ColumnLayout {
        spacing: 0
        
        // Title bar
        Rectangle {
            Layout.fillWidth: true
            height: 48
            color: Theme.surface
            
            Text {
                anchors.centerIn: parent
                text: root.title
                font.pixelSize: 18
                font.bold: true
                color: Theme.text
            }
        }
        
        // Search input
        TextField {
            id: searchInput
            Layout.fillWidth: true
            Layout.margins: 16
            Layout.bottomMargin: 8
            placeholderText: LanguageContext.t("searchPlaceholder")
            text: query
            onTextChanged: {
                query = text
                searchTimer.restart()
            }
            font.pixelSize: 16
            color: Theme.text
            
            leftPadding: 40
            
            Text {
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "🔍"
                font.pixelSize: 18
            }
            
            background: Rectangle {
                color: Theme.background
                border.color: searchInput.activeFocus ? Theme.primary : Theme.border
                border.width: searchInput.activeFocus ? 2 : 1
                radius: 4
                implicitHeight: 44
            }
        }
        
        // Tab bar
        TabBar {
            id: tabBar
            Layout.fillWidth: true
            Layout.leftMargin: 16
            Layout.rightMargin: 16
            currentIndex: activeTab
            onCurrentIndexChanged: activeTab = currentIndex
            
            background: Rectangle {
                color: "transparent"
            }
            
            TabButton {
                text: LanguageContext.t("tasks") + " (" + taskResults.length + ")"
                width: implicitWidth
                
                background: Rectangle {
                    color: tabBar.currentIndex === 0 ? 
                           Qt.rgba(Theme.primary.r, Theme.primary.g, Theme.primary.b, 0.12) : 
                           "transparent"
                    radius: 4
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 14
                    font.bold: tabBar.currentIndex === 0
                    color: tabBar.currentIndex === 0 ? Theme.primary : Theme.textSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
            
            TabButton {
                text: LanguageContext.t("code") + " (" + codeResults.length + ")"
                width: implicitWidth
                
                background: Rectangle {
                    color: tabBar.currentIndex === 1 ? 
                           Qt.rgba(Theme.primary.r, Theme.primary.g, Theme.primary.b, 0.12) : 
                           "transparent"
                    radius: 4
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 14
                    font.bold: tabBar.currentIndex === 1
                    color: tabBar.currentIndex === 1 ? Theme.primary : Theme.textSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
    }
    
    contentItem: StackLayout {
        currentIndex: activeTab
        
        // Tasks results
        ScrollView {
            clip: true
            
            ColumnLayout {
                width: parent.width
                spacing: 8
                
                // Loading indicator
                BusyIndicator {
                    Layout.alignment: Qt.AlignHCenter
                    visible: loading
                    running: loading
                }
                
                // No results
                Text {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 32
                    visible: !loading && query.trim() !== "" && taskResults.length === 0
                    text: LanguageContext.t("noResults")
                    font.pixelSize: 14
                    color: Theme.textSecondary
                }
                
                // Empty state
                Text {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 32
                    visible: !loading && query.trim() === ""
                    text: LanguageContext.t("searchHelp")
                    font.pixelSize: 14
                    color: Theme.textSecondary
                }
                
                // Task results
                Repeater {
                    model: taskResults
                    
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.leftMargin: 4
                        Layout.rightMargin: 4
                        height: taskColumn.height + 16
                        color: taskMouse.containsMouse ? 
                               Qt.rgba(Theme.primary.r, Theme.primary.g, Theme.primary.b, 0.08) : 
                               "transparent"
                        radius: 4
                        
                        MouseArea {
                            id: taskMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                taskSelected(modelData.id)
                                root.close()
                            }
                        }
                        
                        ColumnLayout {
                            id: taskColumn
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.margins: 8
                            spacing: 4
                            
                            RowLayout {
                                spacing: 8
                                
                                // Status badge
                                Rectangle {
                                    width: 8
                                    height: 8
                                    radius: 4
                                    color: modelData.status === "completed" ? Theme.success :
                                           modelData.status === "running" ? Theme.primary :
                                           modelData.status === "error" ? Theme.error : Theme.warning
                                }
                                
                                Text {
                                    text: modelData.id || ""
                                    font.pixelSize: 12
                                    font.family: "Courier New"
                                    color: Theme.primary
                                }
                            }
                            
                            Text {
                                Layout.fillWidth: true
                                text: modelData.prompt ? highlightMatch(modelData.prompt.substring(0, 100), query) : ""
                                textFormat: Text.RichText
                                font.pixelSize: 14
                                color: Theme.text
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }
        }
        
        // Code results
        ScrollView {
            clip: true
            
            ColumnLayout {
                width: parent.width
                spacing: 8
                
                // Loading indicator
                BusyIndicator {
                    Layout.alignment: Qt.AlignHCenter
                    visible: loading
                    running: loading
                }
                
                // No results
                Text {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 32
                    visible: !loading && query.trim() !== "" && codeResults.length === 0
                    text: LanguageContext.t("noResults")
                    font.pixelSize: 14
                    color: Theme.textSecondary
                }
                
                // Code results
                Repeater {
                    model: codeResults
                    
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.leftMargin: 4
                        Layout.rightMargin: 4
                        height: codeColumn.height + 16
                        color: Theme.background
                        radius: 4
                        border.color: Theme.border
                        
                        ColumnLayout {
                            id: codeColumn
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.margins: 8
                            spacing: 4
                            
                            Text {
                                text: modelData.file || ""
                                font.pixelSize: 12
                                font.family: "Courier New"
                                color: Theme.primary
                            }
                            
                            Rectangle {
                                Layout.fillWidth: true
                                height: codeText.height + 8
                                color: Qt.rgba(0, 0, 0, 0.2)
                                radius: 4
                                
                                Text {
                                    id: codeText
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.margins: 4
                                    text: modelData.snippet ? highlightMatch(modelData.snippet, query) : ""
                                    textFormat: Text.RichText
                                    font.pixelSize: 12
                                    font.family: "Courier New"
                                    color: Theme.text
                                    wrapMode: Text.WrapAnywhere
                                }
                            }
                            
                            Text {
                                text: "Line " + (modelData.line || "?")
                                font.pixelSize: 11
                                color: Theme.textSecondary
                            }
                        }
                    }
                }
            }
        }
    }
}
