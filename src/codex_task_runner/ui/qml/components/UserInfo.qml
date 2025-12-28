import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../contexts"
import "../fakemui"

/**
 * UserInfo.qml - User profile and connection status
 * Mirrors React's UserInfo.jsx
 */
Item {
    id: root
    
    property string apiBase: ""
    
    // User state
    property var userData: null
    property bool loading: true
    property string error: ""
    property string connectionStatus: "unknown" // unknown, connected, disconnected
    
    function fetchUserInfo() {
        loading = true
        error = ""
        
        const reqId = AjaxQueueContext.addRequest("Fetching user info")
        
        const xhr = new XMLHttpRequest()
        xhr.open("GET", apiBase + "/me")
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                loading = false
                if (xhr.status === 200) {
                    userData = JSON.parse(xhr.responseText)
                    connectionStatus = "connected"
                    AjaxQueueContext.updateRequest(reqId, { status: "success" })
                } else if (xhr.status === 401) {
                    connectionStatus = "disconnected"
                    error = LanguageContext.t("authRequired")
                    AjaxQueueContext.updateRequest(reqId, { status: "error", error: "Auth required" })
                } else {
                    connectionStatus = "disconnected"
                    error = "Network error"
                    AjaxQueueContext.updateRequest(reqId, { status: "error", error: error })
                }
            }
        }
        xhr.send()
    }
    
    Component.onCompleted: fetchUserInfo()
    
    ScrollView {
        anchors.fill: parent
        anchors.margins: 16
        clip: true
        
        ColumnLayout {
            width: parent.width
            spacing: 16
            
            // User profile card
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
                        text: LanguageContext.t("accountInfo")
                        font.pixelSize: 24
                        font.bold: true
                        color: Theme.text
                    }
                    
                    // Loading indicator
                    BusyIndicator {
                        visible: loading
                        running: loading
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    // Error display
                    Rectangle {
                        Layout.fillWidth: true
                        visible: error !== "" && !loading
                        height: 64
                        color: Qt.rgba(Theme.error.r, Theme.error.g, Theme.error.b, 0.12)
                        radius: 4
                        
                        RowLayout {
                            anchors.centerIn: parent
                            spacing: 12
                            
                            Text {
                                text: "⚠️"
                                font.pixelSize: 24
                            }
                            
                            Text {
                                text: error
                                color: Theme.error
                            }
                        }
                    }
                    
                    // User info display
                    ColumnLayout {
                        Layout.fillWidth: true
                        visible: !loading && userData !== null
                        spacing: 16
                        
                        // Avatar and basic info
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 16
                            
                            // Avatar
                            Rectangle {
                                width: 80
                                height: 80
                                radius: 40
                                color: Theme.primary
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: userData ? (userData.name || userData.email || "?").charAt(0).toUpperCase() : "?"
                                    font.pixelSize: 32
                                    font.bold: true
                                    color: "white"
                                }
                            }
                            
                            ColumnLayout {
                                spacing: 4
                                
                                Text {
                                    text: userData ? (userData.name || LanguageContext.t("noName")) : ""
                                    font.pixelSize: 20
                                    font.bold: true
                                    color: Theme.text
                                }
                                
                                Text {
                                    text: userData ? (userData.email || "") : ""
                                    font.pixelSize: 14
                                    color: Theme.textSecondary
                                }
                            }
                        }
                        
                        // Divider
                        Rectangle {
                            Layout.fillWidth: true
                            height: 1
                            color: Theme.border
                        }
                        
                        // Additional user details
                        GridLayout {
                            Layout.fillWidth: true
                            columns: 2
                            columnSpacing: 16
                            rowSpacing: 12
                            
                            Text {
                                text: LanguageContext.t("userId")
                                font.pixelSize: 14
                                font.bold: true
                                color: Theme.textSecondary
                            }
                            
                            Text {
                                text: userData ? (userData.id || "—") : "—"
                                font.pixelSize: 14
                                color: Theme.text
                                font.family: "Courier New"
                            }
                            
                            Text {
                                text: LanguageContext.t("organization")
                                font.pixelSize: 14
                                font.bold: true
                                color: Theme.textSecondary
                            }
                            
                            Text {
                                text: userData ? (userData.org || "—") : "—"
                                font.pixelSize: 14
                                color: Theme.text
                            }
                            
                            Text {
                                text: LanguageContext.t("role")
                                font.pixelSize: 14
                                font.bold: true
                                color: Theme.textSecondary
                            }
                            
                            Text {
                                text: userData ? (userData.role || "—") : "—"
                                font.pixelSize: 14
                                color: Theme.text
                            }
                        }
                    }
                }
            }
            
            // Connection status card
            CCard {
                Layout.fillWidth: true
                Layout.maximumWidth: 600
                Layout.alignment: Qt.AlignHCenter
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 16
                    
                    Text {
                        text: LanguageContext.t("connectionStatus")
                        font.pixelSize: 18
                        font.bold: true
                        color: Theme.text
                    }
                    
                    RowLayout {
                        spacing: 12
                        
                        // Status indicator
                        Rectangle {
                            width: 12
                            height: 12
                            radius: 6
                            color: connectionStatus === "connected" ? Theme.success :
                                   connectionStatus === "disconnected" ? Theme.error : Theme.warning
                        }
                        
                        Text {
                            text: connectionStatus === "connected" ? LanguageContext.t("connected") :
                                  connectionStatus === "disconnected" ? LanguageContext.t("disconnected") :
                                  LanguageContext.t("unknown")
                            font.pixelSize: 16
                            color: Theme.text
                        }
                    }
                    
                    Text {
                        text: connectionStatus === "connected" ? 
                              LanguageContext.t("connectedDesc") :
                              LanguageContext.t("disconnectedDesc")
                        font.pixelSize: 14
                        color: Theme.textSecondary
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    
                    // Refresh button
                    CButton {
                        text: LanguageContext.t("refresh")
                        variant: "outlined"
                        onClicked: fetchUserInfo()
                        enabled: !loading
                    }
                }
            }
            
            // API Info card (nerd mode only)
            CCard {
                Layout.fillWidth: true
                Layout.maximumWidth: 600
                Layout.alignment: Qt.AlignHCenter
                visible: NerdModeContext.nerdMode
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 16
                    
                    Text {
                        text: LanguageContext.t("apiInfo")
                        font.pixelSize: 18
                        font.bold: true
                        color: Theme.text
                    }
                    
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 2
                        columnSpacing: 16
                        rowSpacing: 12
                        
                        Text {
                            text: LanguageContext.t("apiEndpoint")
                            font.pixelSize: 14
                            font.bold: true
                            color: Theme.textSecondary
                        }
                        
                        Text {
                            text: apiBase
                            font.pixelSize: 14
                            color: Theme.text
                            font.family: "Courier New"
                        }
                        
                        Text {
                            text: LanguageContext.t("requestCount")
                            font.pixelSize: 14
                            font.bold: true
                            color: Theme.textSecondary
                        }
                        
                        Text {
                            text: AjaxQueueContext.queue.length.toString()
                            font.pixelSize: 14
                            color: Theme.text
                        }
                    }
                }
            }
        }
    }
}
