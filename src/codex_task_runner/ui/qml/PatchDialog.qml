import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dialog
    title: "Git Patch"
    width: 900
    height: 650
    modal: true
    standardButtons: Dialog.Close
    
    property string patchText: ""
    property int additions: 0
    property int deletions: 0
    
    function show(patch) {
        patchText = patch
        // Count additions and deletions
        var lines = patch.split('\n')
        additions = 0
        deletions = 0
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].startsWith('+') && !lines[i].startsWith('+++')) additions++
            if (lines[i].startsWith('-') && !lines[i].startsWith('---')) deletions++
        }
        open()
    }
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        
        // Stats and actions
        RowLayout {
            Layout.fillWidth: true
            spacing: 16
            
            Label {
                text: "+" + additions
                color: "#4caf50"
                font.bold: true
            }
            
            Label {
                text: "-" + deletions
                color: "#f44336"
                font.bold: true
            }
            
            Label {
                text: patchText.split('\n').length + " lines"
                opacity: 0.7
            }
            
            Item { Layout.fillWidth: true }
            
            Button {
                text: "📋 Copy to Clipboard"
                onClicked: {
                    app.copyToClipboard(patchText)
                }
            }
            
            Button {
                text: "💾 Save to File"
                onClicked: {
                    // For now just copy - could add file save dialog later
                    app.copyToClipboard(patchText)
                }
            }
        }
        
        // Instructions
        Label {
            text: "Apply with: git apply < patch.diff"
            opacity: 0.7
            font.pixelSize: 12
        }
        
        // Diff view with syntax highlighting
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            
            TextArea {
                id: patchArea
                text: patchText
                readOnly: true
                font.family: "Menlo, Monaco, Consolas, monospace"
                font.pixelSize: 12
                wrapMode: Text.NoWrap
                selectByMouse: true
                textFormat: Text.PlainText
                
                background: Rectangle {
                    color: "#1e1e1e"
                    radius: 4
                }
                
                // Basic diff coloring via palette
                color: "#d4d4d4"
            }
        }
    }
}
