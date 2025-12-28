import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: popup
    width: 200
    padding: 8
    
    property string currentTheme: "system"
    
    signal themeSelected(string themeId)
    
    // Theme definitions inline (since singleton may not load in all contexts)
    readonly property var themes: [
        { id: "system", name: "System", icon: "💻" },
        { id: "light", name: "Light", icon: "☀️" },
        { id: "dark", name: "Dark", icon: "🌙" },
        { id: "hacker", name: "Hacker", icon: "🤓" },
        { id: "ocean", name: "Ocean", icon: "🌊" },
        { id: "sunset", name: "Sunset", icon: "🌅" },
        { id: "forest", name: "Forest", icon: "🌲" },
    ]
    
    background: Rectangle {
        color: "#2b2b2b"
        border.color: "#555"
        border.width: 1
        radius: 8
    }
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 4
        
        Label {
            text: "🎨 Theme"
            font.bold: true
            font.pixelSize: 12
            color: "#fff"
            Layout.bottomMargin: 4
        }
        
        Repeater {
            model: popup.themes
            
            delegate: ItemDelegate {
                Layout.fillWidth: true
                Layout.preferredHeight: 36
                
                highlighted: modelData.id === popup.currentTheme
                
                background: Rectangle {
                    color: parent.highlighted ? "#0078d4" : (parent.hovered ? "#3c3c3c" : "transparent")
                    radius: 4
                }
                
                contentItem: RowLayout {
                    spacing: 8
                    
                    Label {
                        text: modelData.icon
                        font.pixelSize: 16
                    }
                    
                    Label {
                        text: modelData.name
                        color: parent.parent.highlighted ? "#fff" : "#ddd"
                        Layout.fillWidth: true
                    }
                    
                    Label {
                        text: "✓"
                        visible: modelData.id === popup.currentTheme
                        color: "#fff"
                    }
                }
                
                onClicked: {
                    popup.themeSelected(modelData.id)
                    popup.close()
                }
            }
        }
    }
}
