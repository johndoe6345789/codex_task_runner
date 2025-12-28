import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../contexts"
import "../fakemui"

/**
 * TaskDetail.qml - Task detail view with tabs
 * Uses Python AppController (app) directly instead of HTTP/XHR
 */
Item {
    id: root
    
    property int taskIndex: -1
    signal back()
    
    // State
    property var detail: null
    property bool loading: true
    property string error: ""
    property int tabIndex: 0
    property string snackbarMessage: ""
    
    onTaskIndexChanged: {
        if (taskIndex >= 0) {
            loading = true
            // Controller will load detail and emit signal
        }
    }
    
    Component.onCompleted: {
        app.taskDetailLoaded.connect(onTaskDetailLoaded)
        app.patchReady.connect(onPatchReady)
        app.errorOccurred.connect(onError)
    }
    
    Component.onDestruction: {
        app.taskDetailLoaded.disconnect(onTaskDetailLoaded)
        app.patchReady.disconnect(onPatchReady)
        app.errorOccurred.disconnect(onError)
    }
    
    function onTaskDetailLoaded(jsonStr) {
        try {
            detail = JSON.parse(jsonStr)
        } catch (e) {
            detail = null
        }
        loading = false
    }
    
    function onPatchReady(diff) {
        detail = detail || {}
        detail.patch = { diff: diff }
        tabIndex = 2
    }
    
    function onError(msg) {
        error = msg
        loading = false
    }
    
    function createPR() {
        app.createPR(taskIndex)
    }
    
    function extractPatch() {
        app.extractPatch(taskIndex)
    }
    
    function copyToClipboard(text) {
        app.copyToClipboard(text)
        showSnackbar(LanguageContext.t("copied"))
    }
    
    function showSnackbar(message) {
        snackbarMessage = message
        snackbarTimer.restart()
    }
    
    Timer {
        id: snackbarTimer
        interval: 3000
        onTriggered: snackbarMessage = ""
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 16
        
        // Back button
        CButton {
            iconText: "←"
            text: LanguageContext.t("backToTasks")
            variant: "text"
            onClicked: back()
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
            }
        }
        
        // Task card header
        CCard {
            Layout.fillWidth: true
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                
                Text {
                    text: task?.title || detail?.title || LanguageContext.t("taskDetail")
                    font.pixelSize: 20
                    font.bold: true
                    color: Theme.text
                }
                
                RowLayout {
                    spacing: 8
                    
                    CChip {
                        text: task?.repo || LanguageContext.t("noRepo")
                    }
                    
                    CChip {
                        text: task?.base_branch || "main"
                        variant: "outlined"
                    }
                    
                    Repeater {
                        model: task?.pr_numbers || []
                        
                        CChip {
                            text: "PR #" + modelData
                            color: Theme.success
                        }
                    }
                }
                
                Text {
                    visible: NerdModeContext.nerdMode
                    text: "ID: " + taskId
                    font.pixelSize: 12
                    font.family: "monospace"
                    color: Theme.textMuted
                }
            }
        }
        
        // Tabs
        TabBar {
            id: tabBar
            Layout.fillWidth: true
            currentIndex: tabIndex
            onCurrentIndexChanged: tabIndex = currentIndex
            
            background: Rectangle {
                color: Theme.surface
            }
            
            TabButton {
                text: LanguageContext.t("details")
                width: implicitWidth
            }
            
            TabButton {
                text: LanguageContext.t("turns")
                width: implicitWidth
            }
            
            TabButton {
                text: LanguageContext.t("patch")
                width: implicitWidth
                onClicked: if (!patch) fetchPatch()
            }
        }
        
        // Tab content
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabIndex
            
            // Details tab
            ScrollView {
                clip: true
                
                CCard {
                    width: parent.width
                    
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 12
                        
                        // Nerd mode: raw JSON
                        TextArea {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            visible: NerdModeContext.nerdMode && detail
                            text: detail ? JSON.stringify(detail, null, 2) : ""
                            font.family: "monospace"
                            font.pixelSize: 12
                            color: Theme.text
                            readOnly: true
                            wrapMode: Text.Wrap
                            
                            background: Rectangle {
                                color: Theme.surface
                                radius: 4
                            }
                        }
                        
                        // Normal mode: formatted
                        ColumnLayout {
                            visible: !NerdModeContext.nerdMode
                            Layout.fillWidth: true
                            spacing: 12
                            
                            Text {
                                text: detail?.title || task?.title || ""
                                font.pixelSize: 18
                                font.bold: true
                                color: Theme.text
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                            
                            MarkdownRenderer {
                                Layout.fillWidth: true
                                text: detail?.description || detail?.prompt || task?.description || task?.prompt || ""
                            }
                            
                            CChip {
                                text: detail?.status || task?.status || "pending"
                                visible: !!(detail?.status || task?.status)
                            }
                        }
                    }
                }
            }
            
            // Turns tab
            ScrollView {
                clip: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: 8
                    
                    Text {
                        visible: NerdModeContext.nerdMode && turns
                        text: LanguageContext.t("currentTurn") + ": " + (turns?.current_turn_id || "")
                        font.family: "monospace"
                        font.pixelSize: 12
                        color: Theme.textMuted
                    }
                    
                    Repeater {
                        model: turns ? Object.keys(turns.turn_mapping || {}) : []
                        
                        delegate: CCard {
                            Layout.fillWidth: true
                            
                            property string turnId: modelData
                            property var turnData: turns?.turn_mapping[modelData]
                            property bool isCurrent: turnId === turns?.current_turn_id
                            property bool expanded: false
                            
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 8
                                
                                RowLayout {
                                    Layout.fillWidth: true
                                    
                                    Text {
                                        text: NerdModeContext.nerdMode ? 
                                              "Turn: " + turnId.substring(0, 8) + "..." :
                                              "Turn " + (index + 1)
                                        font.pixelSize: 14
                                        font.bold: true
                                        color: Theme.text
                                    }
                                    
                                    CChip {
                                        text: "Current"
                                        color: Theme.primary
                                        visible: isCurrent
                                    }
                                    
                                    Item { Layout.fillWidth: true }
                                    
                                    CButton {
                                        text: LanguageContext.t("createPR")
                                        iconText: "🔗"
                                        variant: "contained"
                                        size: "small"
                                        onClicked: createPR(turnId)
                                    }
                                    
                                    CIconButton {
                                        icon: expanded ? "▼" : "▶"
                                        onClicked: expanded = !expanded
                                    }
                                }
                                
                                // Expanded content
                                ColumnLayout {
                                    visible: expanded
                                    Layout.fillWidth: true
                                    spacing: 8
                                    
                                    // Prompt
                                    ColumnLayout {
                                        visible: turnData?.prompt
                                        Layout.fillWidth: true
                                        
                                        Text {
                                            text: "Prompt"
                                            font.pixelSize: 12
                                            font.bold: true
                                            color: Theme.textSecondary
                                        }
                                        
                                        MarkdownRenderer {
                                            Layout.fillWidth: true
                                            text: turnData?.prompt || ""
                                        }
                                    }
                                    
                                    // Response (normal mode)
                                    ColumnLayout {
                                        visible: turnData?.response && !NerdModeContext.nerdMode
                                        Layout.fillWidth: true
                                        
                                        Text {
                                            text: "Response"
                                            font.pixelSize: 12
                                            font.bold: true
                                            color: Theme.textSecondary
                                        }
                                        
                                        MarkdownRenderer {
                                            Layout.fillWidth: true
                                            text: turnData?.response || ""
                                        }
                                    }
                                    
                                    // Raw JSON (nerd mode)
                                    TextArea {
                                        visible: NerdModeContext.nerdMode
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 200
                                        text: turnData ? JSON.stringify(turnData, null, 2) : ""
                                        font.family: "monospace"
                                        font.pixelSize: 11
                                        color: Theme.text
                                        readOnly: true
                                        wrapMode: Text.Wrap
                                        
                                        background: Rectangle {
                                            color: Theme.surface
                                            radius: 4
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            // Patch tab
            CCard {
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 12
                    
                    // Patch loaded
                    ColumnLayout {
                        visible: patch !== null
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 12
                        
                        // Header
                        RowLayout {
                            Layout.fillWidth: true
                            
                            ColumnLayout {
                                spacing: 4
                                
                                Text {
                                    text: patch?.pr_title || "Git Patch"
                                    font.pixelSize: 14
                                    font.bold: true
                                    color: Theme.text
                                }
                                
                                Text {
                                    text: (patch?.diff_lines || 0) + " " + LanguageContext.t("lines")
                                    font.pixelSize: 12
                                    color: Theme.textSecondary
                                }
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            CIconButton {
                                icon: "📋"
                                tooltip: "Copy"
                                onClicked: copyToClipboard(patch?.diff || "")
                            }
                            
                            CIconButton {
                                icon: "💾"
                                tooltip: "Download"
                                // Download would require platform-specific code
                            }
                        }
                        
                        // Description
                        MarkdownRenderer {
                            Layout.fillWidth: true
                            text: patch?.pr_message || patch?.description || patch?.body || ""
                            visible: (patch?.pr_message || patch?.description || patch?.body || "") !== ""
                        }
                        
                        // Diff view
                        ScrollView {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            
                            TextArea {
                                width: parent.width
                                text: patch?.diff || LanguageContext.t("noPatch")
                                font.family: "monospace"
                                font.pixelSize: 12
                                color: Theme.text
                                readOnly: true
                                wrapMode: Text.NoWrap
                                
                                background: Rectangle {
                                    color: Theme.surface
                                    radius: 4
                                }
                            }
                        }
                    }
                    
                    // Load patch button
                    CButton {
                        visible: patch === null
                        text: LanguageContext.t("loadPatch")
                        variant: "contained"
                        onClicked: fetchPatch()
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
        }
        
        // Snackbar
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            visible: snackbarMessage !== ""
            width: snackbarText.width + 32
            height: 48
            color: Theme.paper
            radius: 4
            
            layer.enabled: true
            layer.effect: Item {
                // Shadow effect placeholder
            }
            
            Text {
                id: snackbarText
                anchors.centerIn: parent
                text: snackbarMessage
                color: Theme.text
                font.pixelSize: 14
            }
        }
    }
    
    // Loading overlay
    Item {
        anchors.fill: parent
        visible: loading
        
        Rectangle {
            anchors.fill: parent
            color: Qt.rgba(0, 0, 0, 0.3)
        }
        
        BusyIndicator {
            anchors.centerIn: parent
            running: loading
        }
    }
}
