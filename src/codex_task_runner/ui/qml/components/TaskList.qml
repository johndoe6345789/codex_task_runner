import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../contexts"
import "../fakemui"

/**
 * TaskList.qml - Task list component
 * Uses Python AppController (app) directly instead of HTTP/XHR
 */
Item {
    id: root
    
    signal taskSelected(int index)
    
    // State
    property bool loading: true
    property string error: ""
    property string filter: "current"
    property int limit: 20
    
    Component.onCompleted: {
        // Connect to Python controller signals
        app.tasksLoaded.connect(onTasksLoaded)
        app.errorOccurred.connect(onError)
        // Load tasks via Python API
        app.loadTasks()
    }
    
    Component.onDestruction: {
        app.tasksLoaded.disconnect(onTasksLoaded)
        app.errorOccurred.disconnect(onError)
    }
    
    function onTasksLoaded() {
        loading = false
        error = ""
    }
    
    function onError(msg) {
        loading = false
        error = msg
    }
    
    function refresh() {
        loading = true
        error = ""
        app.loadTasks()
    }
    
    function archiveTask(index) {
        app.archiveTask(index)
    }
    
    function getStatusColor(status, hasPr) {
        if (hasPr) return Theme.success
        if (status === "completed") return Theme.success
        if (status === "running") return Theme.warning
        return Theme.textMuted
    }
    
    function getStatusLabel(status, hasPr, prUrl) {
        if (hasPr && prUrl) {
            // Extract PR number from URL if possible
            const match = prUrl.match(/\/pull\/(\d+)/)
            if (match) return "PR #" + match[1]
            return "Has PR"
        }
        return status || "pending"
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 16
        
        // Toolbar
        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            
            // Filter dropdown
            ComboBox {
                id: filterCombo
                model: [
                    { value: "current", text: LanguageContext.t("current") },
                    { value: "archived", text: LanguageContext.t("archived") },
                    { value: "all", text: LanguageContext.t("all") }
                ]
                textRole: "text"
                valueRole: "value"
                currentIndex: 0
                onActivated: filter = currentValue
                
                background: Rectangle {
                    color: Theme.surface
                    border.color: Theme.border
                    border.width: 1
                    radius: 4
                    implicitWidth: 120
                    implicitHeight: 36
                }
            }
            
            // Limit dropdown
            ComboBox {
                id: limitCombo
                model: [10, 20, 50, 100]
                currentIndex: 1
                onActivated: limit = currentValue
                
                background: Rectangle {
                    color: Theme.surface
                    border.color: Theme.border
                    border.width: 1
                    radius: 4
                    implicitWidth: 80
                    implicitHeight: 36
                }
            }
            
            // Refresh button
            CIconButton {
                icon: "🔄"
                onClicked: fetchTasks()
            }
            
            Item { Layout.fillWidth: true }
            
            // Task count
            Text {
                text: tasks.length + " " + LanguageContext.t("tasksCount")
                color: Theme.textSecondary
                font.pixelSize: 14
            }
        }
        
        // Error alert
        Rectangle {
            Layout.fillWidth: true
            visible: error !== ""
            height: 48
            color: Qt.rgba(Theme.error.r, Theme.error.g, Theme.error.b, 0.12)
            radius: 4
            
            Text {
                anchors.centerIn: parent
                text: error
                color: Theme.error
                font.pixelSize: 14
            }
        }
        
        // Loading
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: loading
            
            BusyIndicator {
                anchors.centerIn: parent
                running: loading
            }
        }
        
        // Task Grid
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: !loading
            clip: true
            
            GridLayout {
                width: parent.width
                columns: Math.max(1, Math.floor(width / 360))
                columnSpacing: 16
                rowSpacing: 16
                
                Repeater {
                    model: tasks
                    
                    delegate: CCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 180
                        
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 16
                            spacing: 8
                            
                            // Header row with status chips
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                
                                CChip {
                                    text: getStatusLabel(modelData)
                                    color: getStatusColor(modelData)
                                }
                                
                                CChip {
                                    text: "#" + (modelData._alias || index + 1)
                                    variant: "outlined"
                                    visible: modelData._alias !== undefined
                                }
                            }
                            
                            // Title
                            Text {
                                Layout.fillWidth: true
                                text: modelData.title || LanguageContext.t("untitledTask")
                                font.pixelSize: 16
                                font.bold: true
                                color: Theme.text
                                elide: Text.ElideRight
                                maximumLineCount: 2
                                wrapMode: Text.WordWrap
                            }
                            
                            // Description
                            Text {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                text: (modelData.description || modelData.prompt || "").substring(0, 120) + 
                                      ((modelData.description || modelData.prompt || "").length > 120 ? "..." : "")
                                font.pixelSize: 12
                                color: Theme.textSecondary
                                elide: Text.ElideRight
                                wrapMode: Text.WordWrap
                                maximumLineCount: 2
                            }
                            
                            // Repo
                            Text {
                                text: modelData.repo || LanguageContext.t("noRepo")
                                font.pixelSize: 12
                                color: Theme.textMuted
                            }
                            
                            // ID (nerd mode) or branch
                            Text {
                                text: NerdModeContext.nerdMode ? 
                                      (modelData.task_id || modelData.id) : 
                                      (modelData.base_branch || "main")
                                font.pixelSize: 11
                                font.family: "monospace"
                                color: Theme.textMuted
                                elide: Text.ElideMiddle
                                Layout.maximumWidth: parent.width
                            }
                            
                            // Actions row
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                
                                CButton {
                                    text: LanguageContext.t("view")
                                    variant: "outlined"
                                    size: "small"
                                    onClicked: taskSelected(modelData)
                                }
                                
                                CIconButton {
                                    icon: "📝"
                                    size: "small"
                                    tooltip: LanguageContext.t("getPatch")
                                    onClicked: Qt.openUrlExternally(apiBase + "/tasks/" + (modelData.task_id || modelData.id) + "/patch")
                                }
                                
                                CIconButton {
                                    icon: "📦"
                                    size: "small"
                                    tooltip: LanguageContext.t("archive")
                                    onClicked: archiveTask(modelData.task_id || modelData.id)
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // Empty state
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: !loading && tasks.length === 0
            
            CEmptyState {
                anchors.centerIn: parent
                icon: "📋"
                title: LanguageContext.t("noTasks")
            }
        }
    }
}
