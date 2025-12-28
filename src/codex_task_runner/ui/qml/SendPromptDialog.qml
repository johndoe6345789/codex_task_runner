import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dialog
    title: "Send Prompt to Codex"
    width: 700
    height: 500
    modal: true
    standardButtons: Dialog.Cancel
    
    property var environments: []
    property bool sending: false
    
    signal promptSubmitted(string prompt, string envId, string branch, int bestOf)
    
    function open() {
        promptField.text = ""
        branchField.text = "main"
        bestOfSpinner.value = 1
        errorLabel.text = ""
        sending = false
        visible = true
    }
    
    function setEnvironments(envList) {
        environments = envList
        envCombo.model = envList.map(e => e.name || e.full_name || e.id)
        if (envList.length > 0) {
            envCombo.currentIndex = 0
        }
    }
    
    function showError(msg) {
        errorLabel.text = msg
        sending = false
    }
    
    function showSuccess(taskId) {
        sending = false
        close()
    }
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 16
        
        // Environment selector
        GridLayout {
            Layout.fillWidth: true
            columns: 2
            columnSpacing: 12
            rowSpacing: 8
            
            Label {
                text: "Environment:"
                Layout.alignment: Qt.AlignRight
            }
            
            ComboBox {
                id: envCombo
                Layout.fillWidth: true
                model: []
                enabled: !sending
            }
            
            Label {
                text: "Branch:"
                Layout.alignment: Qt.AlignRight
            }
            
            TextField {
                id: branchField
                Layout.fillWidth: true
                text: "main"
                placeholderText: "main"
                enabled: !sending
            }
            
            Label {
                text: "Best of N:"
                Layout.alignment: Qt.AlignRight
            }
            
            SpinBox {
                id: bestOfSpinner
                from: 1
                to: 5
                value: 1
                enabled: !sending
            }
        }
        
        // Prompt input
        Label {
            text: "Prompt:"
            font.bold: true
        }
        
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            
            TextArea {
                id: promptField
                placeholderText: "Describe the task you want Codex to perform...\n\nExample:\nAdd a dark mode toggle to the settings page. It should persist the preference in localStorage."
                wrapMode: Text.Wrap
                font.pixelSize: 14
                enabled: !sending
                selectByMouse: true
            }
        }
        
        // Error message
        Label {
            id: errorLabel
            Layout.fillWidth: true
            color: "#ff6b6b"
            wrapMode: Text.Wrap
            visible: text.length > 0
        }
        
        // Submit button
        RowLayout {
            Layout.fillWidth: true
            
            Item { Layout.fillWidth: true }
            
            BusyIndicator {
                running: sending
                visible: sending
                Layout.preferredWidth: 24
                Layout.preferredHeight: 24
            }
            
            Button {
                id: sendButton
                text: sending ? "Sending..." : "🚀 Send Prompt"
                enabled: !sending && promptField.text.trim().length > 0 && envCombo.currentIndex >= 0
                highlighted: true
                
                onClicked: {
                    if (promptField.text.trim().length === 0) {
                        errorLabel.text = "Please enter a prompt"
                        return
                    }
                    if (environments.length === 0 || envCombo.currentIndex < 0) {
                        errorLabel.text = "No environment selected"
                        return
                    }
                    
                    sending = true
                    errorLabel.text = ""
                    
                    var env = environments[envCombo.currentIndex]
                    var envId = env.id || env.environment_id
                    
                    dialog.promptSubmitted(
                        promptField.text.trim(),
                        envId,
                        branchField.text || "main",
                        bestOfSpinner.value
                    )
                }
            }
        }
    }
    
    // Keyboard shortcuts
    Shortcut {
        sequence: "Ctrl+Return"
        enabled: sendButton.enabled
        onActivated: sendButton.clicked()
    }
}
