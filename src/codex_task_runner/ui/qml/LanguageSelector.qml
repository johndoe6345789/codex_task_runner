import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: popup
    width: 220
    height: Math.min(400, langList.contentHeight + 60)
    padding: 8
    
    property string currentLanguage: "en"
    
    signal languageSelected(string langId)
    
    readonly property var languages: [
        { id: "en", name: "English", flag: "🇺🇸" },
        { id: "es", name: "Español", flag: "🇪🇸" },
        { id: "fr", name: "Français", flag: "🇫🇷" },
        { id: "de", name: "Deutsch", flag: "🇩🇪" },
        { id: "it", name: "Italiano", flag: "🇮🇹" },
        { id: "pt", name: "Português", flag: "🇧🇷" },
        { id: "nl", name: "Nederlands", flag: "🇳🇱" },
        { id: "pl", name: "Polski", flag: "🇵🇱" },
        { id: "sv", name: "Svenska", flag: "🇸🇪" },
        { id: "tr", name: "Türkçe", flag: "🇹🇷" },
        { id: "ru", name: "Русский", flag: "🇷🇺" },
        { id: "uk", name: "Українська", flag: "🇺🇦" },
        { id: "ar", name: "العربية", flag: "🇸🇦" },
        { id: "hi", name: "हिंदी", flag: "🇮🇳" },
        { id: "th", name: "ไทย", flag: "🇹🇭" },
        { id: "vi", name: "Tiếng Việt", flag: "🇻🇳" },
        { id: "zh", name: "中文", flag: "🇨🇳" },
        { id: "ja", name: "日本語", flag: "🇯🇵" },
        { id: "ko", name: "한국어", flag: "🇰🇷" },
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
            text: "🌐 Language"
            font.bold: true
            font.pixelSize: 12
            color: "#fff"
            Layout.bottomMargin: 4
        }
        
        ListView {
            id: langList
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: popup.languages
            
            delegate: ItemDelegate {
                width: langList.width
                height: 36
                
                highlighted: modelData.id === popup.currentLanguage
                
                background: Rectangle {
                    color: parent.highlighted ? "#0078d4" : (parent.hovered ? "#3c3c3c" : "transparent")
                    radius: 4
                }
                
                contentItem: RowLayout {
                    spacing: 8
                    
                    Label {
                        text: modelData.flag
                        font.pixelSize: 16
                    }
                    
                    Label {
                        text: modelData.name
                        color: parent.parent.highlighted ? "#fff" : "#ddd"
                        Layout.fillWidth: true
                    }
                    
                    Label {
                        text: "✓"
                        visible: modelData.id === popup.currentLanguage
                        color: "#fff"
                    }
                }
                
                onClicked: {
                    popup.languageSelected(modelData.id)
                    popup.close()
                }
            }
            
            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
            }
        }
    }
}
