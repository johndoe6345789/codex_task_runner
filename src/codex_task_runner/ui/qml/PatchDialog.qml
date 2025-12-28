import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dialog
    title: "Git Patch"
    width: 800
    height: 600
    modal: true
    standardButtons: Dialog.Close
    
    property string patchText: ""
    
    function show(patch) {
        patchText = patch
        open()
    }
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 8
        
        RowLayout {
            Layout.fillWidth: true
            
            Label {
                text: "Copy and run: git apply"
                opacity: 0.7
            }
            
            Item { Layout.fillWidth: true }
            
            Button {
                text: "📋 Copy"
                onClicked: {
                    patchArea.selectAll()
                    patchArea.copy()
                    patchArea.deselect()
                }
            }
        }
        
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            
            TextArea {
                id: patchArea
                text: patchText
                readOnly: true
                font.family: "Menlo"
                font.pixelSize: 11
                wrapMode: Text.NoWrap
                selectByMouse: true
                color: "#d4d4d4"
            }
        }
    }
}
