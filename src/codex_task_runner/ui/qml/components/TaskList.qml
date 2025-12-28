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
                onActivated: {
                    filter = currentValue
                    refresh()
                }
                
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
                onActivated: {
                    limit = currentValue
                    refresh()
                }
                
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
                onClicked: refresh()
            }
            
            Item { Layout.fillWidth: true }
            
            // Task count - use model count
            Text {
                text: app.taskModel.rowCount() + " " + LanguageContext.t("tasksCount")
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
        
        // Task Grid - uses app.taskModel from Python controller
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
                    model: app.taskModel
                    
                    delegate: CCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 180
                        
                        required property int index
                        required property string taskId
                        required property string title
                        required property string status
                        required property string repo
                        required property string branch
                        required property string created
                        required property string alias
                        required property string prUrl
                        required property bool hasPr
                        
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 16
                            spacing: 8
                            
                            // Header row with status chips
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                
                                CChip {
                                    text: getStatusLabel(status, hasPr, prUrl)
                                    color: getStatusColor(status, hasPr)
                                }
                                
                                CChip {
                                    text: "#" + alias
                                    variant: "outlined"
                                }
                            }
                            
                            // Title
                            Text {
                                Layout.fillWidth: true
                                text: title || LanguageContext.t("untitledTask")
                                font.pixelSize: 16
                                font.bold: true
                                color: Theme.text
                                elide: Text.ElideRight
                                maximumLineCount: 2
                                wrapMode: Text.WordWrap
                            }
                            
                            // Repo
                            Text {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                text: repo || LanguageContext.t("noRepo")
                                font.pixelSize: 12
                                color: Theme.textSecondary
                                elide: Text.ElideRight
                            }
                            
                            // Branch / ID (nerd mode)
                            Text {
                                text: NerdModeContext.nerdMode ? taskId : (branch || "main")
                                font.pixelSize: 11
                                font.family: "monospace"
                                color: Theme.textMuted
                                elide: Text.ElideMiddle
                                Layout.maximumWidth: parent.width
                            }
                            
                            // Created date
                            Text {
                                text: created
                                font.pixelSize: 11
                                color: Theme.textMuted
                            }
                            
                            // Actions row
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                
                                CButton {
                                    text: LanguageContext.t("view")
                                    variant: "outlined"
                                    size: "small"
                                    onClicked: taskSelected(index)
                                }
                                
                                CIconButton {
                                    icon: "📦"
                                    size: "small"
                                    tooltip: LanguageContext.t("archive")
                                    onClicked: archiveTask(index)
                                }
                                
                                CIconButton {
                                    icon: "🔗"
                                    size: "small"
                                    tooltip: "Open PR"
                                    visible: hasPr && prUrl
                                    onClicked: app.openUrl(prUrl)
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
            visible: !loading && app.taskModel.rowCount() === 0
            
            CEmptyState {
                anchors.centerIn: parent
                icon: "📋"
                title: LanguageContext.t("noTasks")
            }
        }
    }
}
