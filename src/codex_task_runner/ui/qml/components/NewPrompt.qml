import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../contexts"
import "../fakemui"

/**
 * NewPrompt.qml - Create new task form
 * Mirrors React's NewPrompt.jsx
 */
Item {
    id: root
    
    property string apiBase: ""
    signal success()
    
    // Form state
    property string prompt: ""
    property string branch: "main"
    property int bestOf: 1
    property bool loading: false
    property string error: ""
    property string successMessage: ""
    
    function handleSubmit() {
        if (!prompt.trim()) {
            error = LanguageContext.t("enterPrompt")
            return
        }
        
        loading = true
        error = ""
        successMessage = ""
        
        const reqId = AjaxQueueContext.addRequest("Creating task")
        
        const xhr = new XMLHttpRequest()
        xhr.open("POST", apiBase + "/prompt")
        xhr.setRequestHeader("Content-Type", "application/json")
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                loading = false
                if (xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText)
                    if (data.success) {
                        successMessage = LanguageContext.t("taskCreated")
                        prompt = ""
                        AjaxQueueContext.updateRequest(reqId, { status: "success" })
                        successTimer.start()
                    } else {
                        error = data.error || LanguageContext.t("failedCreate")
                        AjaxQueueContext.updateRequest(reqId, { status: "error", error: error })
                    }
                } else {
                    error = "Network error"
                    AjaxQueueContext.updateRequest(reqId, { status: "error", error: error })
                }
            }
        }
        xhr.send(JSON.stringify({
            prompt_text: prompt,
            branch: branch,
            best_of: bestOf
        }))
    }
    
    Timer {
        id: successTimer
        interval: 2000
        onTriggered: success()
    }
    
    ScrollView {
        anchors.fill: parent
        anchors.margins: 16
        clip: true
        
        ColumnLayout {
            width: parent.width
            spacing: 16
            
            // Main form card
            CCard {
                Layout.fillWidth: true
                Layout.maximumWidth: 600
                Layout.alignment: Qt.AlignHCenter
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 16
                    
                    // Title
                    Text {
                        text: LanguageContext.t("createNewTask")
                        font.pixelSize: 24
                        font.bold: true
                        color: Theme.text
                    }
                    
                    Text {
                        text: LanguageContext.t("sendPromptDesc")
                        font.pixelSize: 14
                        color: Theme.textSecondary
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
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
                    
                    // Success alert
                    Rectangle {
                        Layout.fillWidth: true
                        visible: successMessage !== ""
                        height: 48
                        color: Qt.rgba(Theme.success.r, Theme.success.g, Theme.success.b, 0.12)
                        radius: 4
                        
                        Text {
                            anchors.centerIn: parent
                            text: successMessage
                            color: Theme.success
                        }
                    }
                    
                    // Prompt textarea
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        
                        Text {
                            text: LanguageContext.t("taskPrompt")
                            font.pixelSize: 14
                            font.bold: true
                            color: Theme.text
                        }
                        
                        ScrollView {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 160
                            
                            TextArea {
                                id: promptInput
                                text: prompt
                                onTextChanged: prompt = text
                                placeholderText: LanguageContext.t("promptPlaceholder")
                                wrapMode: Text.Wrap
                                enabled: !loading
                                font.pixelSize: 14
                                color: Theme.text
                                
                                background: Rectangle {
                                    color: Theme.surface
                                    border.color: promptInput.activeFocus ? Theme.primary : Theme.border
                                    border.width: promptInput.activeFocus ? 2 : 1
                                    radius: 4
                                }
                            }
                        }
                    }
                    
                    // Branch and Best Of row
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 16
                        
                        // Branch input
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 8
                            
                            Text {
                                text: LanguageContext.t("branch")
                                font.pixelSize: 14
                                font.bold: true
                                color: Theme.text
                            }
                            
                            TextField {
                                id: branchInput
                                Layout.fillWidth: true
                                text: branch
                                onTextChanged: branch = text
                                enabled: !loading
                                font.pixelSize: 14
                                color: Theme.text
                                
                                background: Rectangle {
                                    color: Theme.surface
                                    border.color: branchInput.activeFocus ? Theme.primary : Theme.border
                                    border.width: branchInput.activeFocus ? 2 : 1
                                    radius: 4
                                    implicitHeight: 40
                                }
                            }
                        }
                        
                        // Best Of dropdown
                        ColumnLayout {
                            spacing: 8
                            
                            Text {
                                text: LanguageContext.t("bestOf")
                                font.pixelSize: 14
                                font.bold: true
                                color: Theme.text
                            }
                            
                            ComboBox {
                                id: bestOfCombo
                                model: [1, 2, 3, 5]
                                currentIndex: 0
                                onActivated: bestOf = currentValue
                                enabled: !loading
                                
                                background: Rectangle {
                                    color: Theme.surface
                                    border.color: Theme.border
                                    border.width: 1
                                    radius: 4
                                    implicitWidth: 80
                                    implicitHeight: 40
                                }
                            }
                        }
                    }
                    
                    // Submit button
                    CButton {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 48
                        text: loading ? LanguageContext.t("creating") : LanguageContext.t("createNewTask")
                        variant: "contained"
                        color: Theme.primary
                        enabled: !loading && prompt.trim() !== ""
                        onClicked: handleSubmit()
                        
                        BusyIndicator {
                            anchors.left: parent.left
                            anchors.leftMargin: 16
                            anchors.verticalCenter: parent.verticalCenter
                            running: loading
                            visible: loading
                            width: 24
                            height: 24
                        }
                    }
                }
            }
            
            // Tips card
            CCard {
                Layout.fillWidth: true
                Layout.maximumWidth: 600
                Layout.alignment: Qt.AlignHCenter
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 12
                    
                    Text {
                        text: LanguageContext.t("tips")
                        font.pixelSize: 16
                        font.bold: true
                        color: Theme.text
                    }
                    
                    Text {
                        text: "• " + LanguageContext.t("tip1")
                        font.pixelSize: 14
                        color: Theme.textSecondary
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    
                    Text {
                        text: "• " + LanguageContext.t("tip2")
                        font.pixelSize: 14
                        color: Theme.textSecondary
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    
                    Text {
                        text: "• " + LanguageContext.t("tip3")
                        font.pixelSize: 14
                        color: Theme.textSecondary
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    
                    Text {
                        text: "• " + LanguageContext.t("tip4")
                        font.pixelSize: 14
                        color: Theme.textSecondary
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
