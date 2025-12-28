import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../contexts"

/**
 * AjaxQueueWidget.qml - Floating AJAX request queue display
 * Mirrors React's AjaxQueueWidget.jsx
 */
Item {
    id: root
    
    property bool expanded: false
    
    // Position in bottom-right corner
    anchors.right: parent ? parent.right : undefined
    anchors.bottom: parent ? parent.bottom : undefined
    anchors.margins: 16
    
    width: expanded ? 320 : 56
    height: expanded ? Math.min(300, 56 + AjaxQueueContext.queue.length * 48) : 56
    
    visible: AjaxQueueContext.queue.length > 0
    
    Behavior on width { NumberAnimation { duration: 200; easing.type: Easing.OutCubic } }
    Behavior on height { NumberAnimation { duration: 200; easing.type: Easing.OutCubic } }
    
    // Main card
    Rectangle {
        anchors.fill: parent
        color: Theme.surface
        radius: expanded ? 12 : 28
        
        layer.enabled: true
        layer.effect: Item {
            // Shadow effect simulation
        }
        
        // Drop shadow simulation
        Rectangle {
            anchors.fill: parent
            anchors.margins: -2
            z: -1
            radius: parent.radius + 2
            color: "transparent"
            border.color: Qt.rgba(0, 0, 0, 0.2)
            border.width: 4
        }
        
        // Collapsed state - just the badge
        Item {
            anchors.fill: parent
            visible: !expanded
            
            // Activity indicator
            BusyIndicator {
                anchors.centerIn: parent
                width: 32
                height: 32
                running: AjaxQueueContext.queue.some(function(r) { return r.status === "pending" })
            }
            
            // Count badge
            Rectangle {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.margins: 4
                width: 20
                height: 20
                radius: 10
                color: Theme.primary
                visible: AjaxQueueContext.queue.length > 0
                
                Text {
                    anchors.centerIn: parent
                    text: AjaxQueueContext.queue.length.toString()
                    font.pixelSize: 11
                    font.bold: true
                    color: "white"
                }
            }
            
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: expanded = true
            }
        }
        
        // Expanded state - full list
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 8
            visible: expanded
            spacing: 8
            
            // Header
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                
                Text {
                    text: LanguageContext.t("requests")
                    font.pixelSize: 14
                    font.bold: true
                    color: Theme.text
                    Layout.fillWidth: true
                }
                
                // Clear button
                Rectangle {
                    width: 24
                    height: 24
                    radius: 12
                    color: clearMouse.containsMouse ? Theme.background : "transparent"
                    visible: AjaxQueueContext.queue.some(function(r) { return r.status !== "pending" })
                    
                    Text {
                        anchors.centerIn: parent
                        text: "🗑️"
                        font.pixelSize: 12
                    }
                    
                    MouseArea {
                        id: clearMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: AjaxQueueContext.clearQueue()
                    }
                }
                
                // Collapse button
                Rectangle {
                    width: 24
                    height: 24
                    radius: 12
                    color: collapseMouse.containsMouse ? Theme.background : "transparent"
                    
                    Text {
                        anchors.centerIn: parent
                        text: "▼"
                        font.pixelSize: 12
                        color: Theme.textSecondary
                    }
                    
                    MouseArea {
                        id: collapseMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: expanded = false
                    }
                }
            }
            
            // Request list
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: 4
                    
                    Repeater {
                        model: AjaxQueueContext.queue
                        
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            height: 40
                            radius: 4
                            color: requestMouse.containsMouse ? Theme.background : "transparent"
                            
                            MouseArea {
                                id: requestMouse
                                anchors.fill: parent
                                hoverEnabled: true
                            }
                            
                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 8
                                
                                // Status indicator
                                Item {
                                    width: 16
                                    height: 16
                                    
                                    // Pending - spinner
                                    BusyIndicator {
                                        anchors.fill: parent
                                        visible: modelData.status === "pending"
                                        running: visible
                                    }
                                    
                                    // Success - checkmark
                                    Text {
                                        anchors.centerIn: parent
                                        visible: modelData.status === "success"
                                        text: "✓"
                                        font.pixelSize: 14
                                        color: Theme.success
                                    }
                                    
                                    // Error - X
                                    Text {
                                        anchors.centerIn: parent
                                        visible: modelData.status === "error"
                                        text: "✗"
                                        font.pixelSize: 14
                                        color: Theme.error
                                    }
                                }
                                
                                // Description
                                Text {
                                    Layout.fillWidth: true
                                    text: modelData.description || "Request"
                                    font.pixelSize: 12
                                    color: Theme.text
                                    elide: Text.ElideRight
                                }
                                
                                // Time elapsed
                                Text {
                                    text: AjaxQueueContext.getElapsedTime(modelData.startTime)
                                    font.pixelSize: 11
                                    font.family: "Courier New"
                                    color: Theme.textSecondary
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
