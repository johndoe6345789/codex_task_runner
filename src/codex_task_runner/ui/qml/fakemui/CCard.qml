import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: card
    
    property string title: ""
    property string subtitle: ""
    property bool elevated: false
    property bool hoverable: false
    property bool clickable: false
    property alias content: contentLoader.sourceComponent
    property alias headerContent: headerLoader.sourceComponent
    
    signal clicked()
    
    color: "#1e1e1e"
    radius: 12
    border.width: 1
    border.color: hoverable && mouseArea.containsMouse ? "#4dabf7" : "#2d2d2d"
    
    implicitHeight: mainColumn.implicitHeight
    implicitWidth: 300
    
    Behavior on border.color { ColorAnimation { duration: 150 } }
    
    layer.enabled: elevated
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowColor: "#40000000"
        shadowBlur: 0.3
        shadowVerticalOffset: 4
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: card.hoverable || card.clickable
        cursorShape: card.clickable ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: if (card.clickable) card.clicked()
    }
    
    ColumnLayout {
        id: mainColumn
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12
        
        // Header
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4
            visible: card.title || headerLoader.item
            
            RowLayout {
                Layout.fillWidth: true
                
                Text {
                    Layout.fillWidth: true
                    text: card.title
                    font.pixelSize: 16
                    font.weight: Font.DemiBold
                    color: "#ffffff"
                    visible: card.title
                }
                
                Loader {
                    id: headerLoader
                }
            }
            
            Text {
                Layout.fillWidth: true
                text: card.subtitle
                font.pixelSize: 12
                color: "#888888"
                visible: card.subtitle
            }
        }
        
        // Content
        Loader {
            id: contentLoader
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
