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
    
    // When true, don't add internal padding - let child manage it
    property bool noPadding: false
    
    signal clicked()
    
    default property alias cardContent: contentColumn.data
    
    color: Theme.paper
    radius: 8
    border.width: 1
    border.color: hoverable && mouseArea.containsMouse ? Theme.primary : Theme.border
    
    implicitHeight: contentColumn.implicitHeight + (noPadding ? 0 : 0)
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
    
    // Simple content column - children are placed here
    ColumnLayout {
        id: contentColumn
        anchors.fill: parent
        spacing: 0
    }
}
