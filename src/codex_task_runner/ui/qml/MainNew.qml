import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components" as C

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "Codex Task Runner" + (nerdMode ? " 🤓" : "")
    color: "#121212"
    
    // Theme state
    property string currentTheme: "system"
    property var themeColors: getThemeColors(currentTheme)
    
    // Language state
    property string currentLanguage: "en"
    property var tr: getTranslations(currentLanguage)
    
    // All translations (collapsed for brevity - keep existing)
    readonly property var allTranslations: ({
        "en": {
            tasks: "Tasks", newTask: "New Task", refresh: "Refresh", openCodex: "Open Codex",
            theme: "Theme", language: "Language", autoRefresh: "Auto-refresh", nerdMode: "Nerd Mode",
            noTasks: "No tasks found", view: "View", getPatch: "Get Patch", archive: "Archive",
            untitledTask: "Untitled Task", noRepo: "No repo", details: "Details", turns: "Turns",
            patch: "Patch", createPR: "Create PR", selectTask: "Select a task to view details",
            ready: "Ready", tasksCount: "tasks", rawJson: "Raw JSON", prompt: "Prompt",
            backToTasks: "Back to Tasks", loading: "Loading...", copied: "Copied!",
            currentTurn: "Current Turn", lines: "lines", connected: "Connected",
            search: "Search tasks...", noResults: "No matching tasks",
        },
        "es": { tasks: "Tareas", newTask: "Nueva Tarea", refresh: "Actualizar", openCodex: "Abrir Codex", noTasks: "Sin tareas", loading: "Cargando...", search: "Buscar tareas..." },
        "fr": { tasks: "Tâches", newTask: "Nouvelle Tâche", refresh: "Rafraîchir", openCodex: "Ouvrir Codex", noTasks: "Aucune tâche", loading: "Chargement...", search: "Rechercher..." },
        "de": { tasks: "Aufgaben", newTask: "Neue Aufgabe", refresh: "Aktualisieren", openCodex: "Codex öffnen", noTasks: "Keine Aufgaben", loading: "Laden...", search: "Suchen..." },
        "ja": { tasks: "タスク", newTask: "新規タスク", refresh: "更新", openCodex: "Codexを開く", noTasks: "タスクがありません", loading: "読み込み中...", search: "検索..." },
    })
    
    function getTranslations(langId) {
        var trans = allTranslations[langId] || {}
        var en = allTranslations["en"]
        // Merge with English as fallback
        for (var key in en) {
            if (!trans[key]) trans[key] = en[key]
        }
        return trans
    }
    
    function getLanguageFlag(langId) {
        var flags = { "en": "🇺🇸", "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪", "ja": "🇯🇵" }
        return flags[langId] || "🌐"
    }
    
    // Theme definitions
    readonly property var allThemes: ({
        "system": { window: "#121212", surface: "#1e1e1e", surfaceAlt: "#252525", background: "#121212", base: "#1e1e1e", text: "#ffffff", textMuted: "#888888", windowText: "#ffffff", accent: "#4dabf7", primary: "#4dabf7", secondary: "#69db7c", success: "#4caf50", error: "#f44336", warning: "#ff9800", info: "#2196f3", border: "#333333", nerd: "#00ff41", codeBackground: "#0d1117", codeText: "#e6edf3", highlight: "#1a3a5c", mid: "#2d2d2d", alternateBase: "#252525" },
        "light": { window: "#f5f5f5", surface: "#ffffff", surfaceAlt: "#f0f0f0", background: "#f5f5f5", base: "#ffffff", text: "#1a1a1a", textMuted: "#666666", windowText: "#1a1a1a", accent: "#1a73e8", primary: "#1a73e8", secondary: "#2d7d46", success: "#2d7d46", error: "#c62828", warning: "#f57c00", info: "#1a73e8", border: "#e0e0e0", nerd: "#00aa00", codeBackground: "#f8f8f8", codeText: "#333333", highlight: "#e3f2fd", mid: "#d0d0d0", alternateBase: "#f0f0f0" },
        "dark": { window: "#0d0d0d", surface: "#1a1a1a", surfaceAlt: "#252525", background: "#0d0d0d", base: "#1a1a1a", text: "#e0e0e0", textMuted: "#888888", windowText: "#e0e0e0", accent: "#569cd6", primary: "#569cd6", secondary: "#4ec9b0", success: "#4ec9b0", error: "#f14c4c", warning: "#cca700", info: "#3794ff", border: "#333333", nerd: "#00ff41", codeBackground: "#1e1e1e", codeText: "#d4d4d4", highlight: "#264f78", mid: "#3c3c3c", alternateBase: "#2d2d30" },
        "ocean": { window: "#0d1b2a", surface: "#1b263b", surfaceAlt: "#273549", background: "#0d1b2a", base: "#1b263b", text: "#e0e1dd", textMuted: "#778da9", windowText: "#e0e1dd", accent: "#4dabf7", primary: "#4dabf7", secondary: "#40c057", success: "#40c057", error: "#fa5252", warning: "#fab005", info: "#4dabf7", border: "#415a77", nerd: "#00ff88", codeBackground: "#0d1b2a", codeText: "#a9d1f7", highlight: "#273549", mid: "#273549", alternateBase: "#273549" },
        "forest": { window: "#1a2f1a", surface: "#1e3a1e", surfaceAlt: "#254725", background: "#1a2f1a", base: "#1e3a1e", text: "#c8e6c9", textMuted: "#81c784", windowText: "#c8e6c9", accent: "#66bb6a", primary: "#66bb6a", secondary: "#a5d6a7", success: "#a5d6a7", error: "#ef9a9a", warning: "#fff59d", info: "#81d4fa", border: "#2e5a2e", nerd: "#00ff41", codeBackground: "#1a2f1a", codeText: "#a5d6a7", highlight: "#254725", mid: "#2e5a2e", alternateBase: "#254725" },
        "hacker": { window: "#0a0a0f", surface: "#0d0d14", surfaceAlt: "#151520", background: "#0a0a0f", base: "#0d0d14", text: "#00ff41", textMuted: "#008f11", windowText: "#00ff41", accent: "#00ff41", primary: "#00ff41", secondary: "#00ccff", success: "#00ff41", error: "#ff0055", warning: "#ffcc00", info: "#00ccff", border: "#1a1a2e", nerd: "#00ff41", codeBackground: "#0a0a0f", codeText: "#00ff41", highlight: "#1a1a2e", mid: "#151520", alternateBase: "#151520" },
    })
    
    function getThemeColors(themeId) { return allThemes[themeId] || allThemes["system"] }
    function getThemeIcon(themeId) {
        var icons = { "system": "💻", "light": "☀️", "dark": "🌙", "hacker": "🤓", "ocean": "🌊", "forest": "🌲" }
        return icons[themeId] || "🎨"
    }
    
    property string statusText: "Ready"
    property bool nerdMode: false
    property bool isLoading: false
    property string searchQuery: ""
    
    Connections {
        target: app
        function onStatusMessage(msg) { statusText = msg; if (msg.startsWith("Loaded")) isLoading = false }
        function onErrorOccurred(msg) { statusText = "Error: " + msg; isLoading = false }
        function onTasksLoaded() { isLoading = false }
        function onPatchReady(patch) { patchDialog.show(patch) }
        function onTaskDetailLoaded(json) { detailPane.taskJson = json }
        function onEnvironmentsLoaded(envList) { sendPromptDialog.setEnvironments(envList) }
        function onPromptSuccess(taskId) { sendPromptDialog.showSuccess(taskId) }
        function onPromptError(msg) { sendPromptDialog.showError(msg) }
        function onNerdModeChanged(enabled) { nerdMode = enabled }
        function onDebugLog(msg) { nerdPanel.appendLog(msg) }
        function onSessionInfoChanged(info) { nerdPanel.sessionInfo = info }
        function onThemeChanged(themeId) { currentTheme = themeId; themeColors = getThemeColors(themeId) }
        function onLanguageChanged(langId) { currentLanguage = langId; tr = getTranslations(langId) }
    }
    
    Component.onCompleted: {
        isLoading = true
        app.loadTasks()
        var saved = app.getSavedTheme()
        if (saved) { currentTheme = saved; themeColors = getThemeColors(saved) }
        var savedLang = app.getSavedLanguage()
        if (savedLang) { currentLanguage = savedLang; tr = getTranslations(savedLang) }
    }
    
    // Main layout
    RowLayout {
        anchors.fill: parent
        spacing: 0
        
        // Sidebar
        C.CSidebar {
            id: sidebar
            Layout.fillHeight: true
            title: "Codex"
            items: [
                {icon: "📋", label: tr.tasks},
                {icon: "✨", label: tr.newTask},
                {icon: "🌐", label: tr.openCodex}
            ]
            
            onItemClicked: function(index) {
                switch(index) {
                    case 0: break // Tasks - already shown
                    case 1: app.loadEnvironments(); sendPromptDialog.open(); break
                    case 2: app.openCodexBrowser(); break
                }
                sidebar.currentIndex = 0 // Always return to tasks view
            }
            
            footer: Component {
                ColumnLayout {
                    spacing: 8
                    
                    // Auto-refresh toggle
                    RowLayout {
                        Layout.fillWidth: true
                        Layout.leftMargin: 16
                        Layout.rightMargin: 16
                        
                        Text {
                            text: "Auto-refresh"
                            font.pixelSize: 12
                            color: "#888888"
                        }
                        Item { Layout.fillWidth: true }
                        Switch {
                            id: autoRefreshSwitch
                            onCheckedChanged: app.setPolling(checked)
                        }
                    }
                    
                    // Theme/Language row
                    RowLayout {
                        Layout.fillWidth: true
                        Layout.leftMargin: 12
                        Layout.rightMargin: 12
                        Layout.bottomMargin: 12
                        spacing: 8
                        
                        C.CIconButton {
                            icon: getLanguageFlag(currentLanguage)
                            size: "sm"
                            onClicked: languageSelector.open()
                            
                            LanguageSelector {
                                id: languageSelector
                                x: 0
                                y: -height - 4
                                currentLanguage: window.currentLanguage
                                onLanguageSelected: function(langId) {
                                    window.currentLanguage = langId
                                    window.tr = getTranslations(langId)
                                    app.setLanguage(langId)
                                }
                            }
                        }
                        
                        C.CIconButton {
                            icon: getThemeIcon(currentTheme)
                            size: "sm"
                            onClicked: themeSelector.open()
                            
                            ThemeSelector {
                                id: themeSelector
                                x: 0
                                y: -height - 4
                                currentTheme: window.currentTheme
                                onThemeSelected: function(themeId) {
                                    window.currentTheme = themeId
                                    window.themeColors = getThemeColors(themeId)
                                    app.setTheme(themeId)
                                }
                            }
                        }
                        
                        Item { Layout.fillWidth: true }
                        
                        C.CIconButton {
                            icon: "🤓"
                            size: "sm"
                            variant: nerdMode ? "primary" : "default"
                            onClicked: app.setNerdMode(!nerdMode)
                        }
                    }
                }
            }
        }
        
        // Main content area
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0
            
            // Top toolbar
            C.CToolbar {
                Layout.fillWidth: true
                title: tr.tasks
                
                leftContent: Component {
                    RowLayout {
                        spacing: 8
                        
                        C.CIconButton {
                            icon: "↻"
                            onClicked: { isLoading = true; app.loadTasks() }
                            loading: isLoading
                        }
                    }
                }
                
                rightContent: Component {
                    RowLayout {
                        spacing: 12
                        
                        C.CTextField {
                            id: searchField
                            Layout.preferredWidth: 250
                            placeholderText: "🔍 " + tr.search
                            clearable: true
                            onTextChanged: {
                                searchQuery = text
                                app.setSearchQuery(text)
                            }
                        }
                        
                        C.CButton {
                            text: "✨ " + tr.newTask
                            variant: "primary"
                            onClicked: {
                                app.loadEnvironments()
                                sendPromptDialog.open()
                            }
                        }
                    }
                }
            }
            
            // Content split view
            SplitView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                orientation: Qt.Vertical
                
                SplitView {
                    SplitView.fillHeight: !nerdMode
                    SplitView.preferredHeight: nerdMode ? parent.height * 0.65 : parent.height
                    orientation: Qt.Horizontal
                    
                    // Task list panel
                    Rectangle {
                        SplitView.preferredWidth: 380
                        SplitView.minimumWidth: 300
                        color: themeColors.surface
                        
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 8
                            
                            // Task count header
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Text {
                                    text: taskList.count + " " + tr.tasksCount
                                    font.pixelSize: 12
                                    color: themeColors.textMuted
                                }
                                
                                Item { Layout.fillWidth: true }
                                
                                C.CChip {
                                    text: isLoading ? "Syncing..." : "Live"
                                    variant: isLoading ? "warning" : "success"
                                    size: "sm"
                                }
                            }
                            
                            // Task list
                            ListView {
                                id: taskList
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                clip: true
                                model: app.taskModel
                                currentIndex: -1
                                spacing: 4
                                
                                delegate: TaskListItem {
                                    width: taskList.width
                                    taskAlias: model.alias
                                    taskTitle: model.title || "Untitled"
                                    taskRepo: model.repo || ""
                                    taskBranch: model.branch || ""
                                    taskStatus: model.status || "unknown"
                                    taskCreated: model.created || ""
                                    taskId: model.taskId || ""
                                    hasPr: model.hasPr
                                    prUrl: model.prUrl || ""
                                    isSelected: taskList.currentIndex === index
                                    showNerdInfo: nerdMode
                                    themeColors: window.themeColors
                                    
                                    onClicked: {
                                        taskList.currentIndex = index
                                        app.loadTaskDetail(index)
                                    }
                                    
                                    onPrClicked: {
                                        if (prUrl) app.openUrl(prUrl)
                                    }
                                }
                                
                                ScrollBar.vertical: ScrollBar {
                                    policy: ScrollBar.AsNeeded
                                }
                            }
                            
                            // Empty state
                            C.CEmptyState {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                visible: taskList.count === 0 && !isLoading
                                icon: searchQuery ? "🔍" : "📭"
                                title: searchQuery ? tr.noResults : tr.noTasks
                                description: searchQuery ? "Try a different search term" : "Create a new task to get started"
                                actionText: searchQuery ? "" : tr.newTask
                                onActionClicked: {
                                    app.loadEnvironments()
                                    sendPromptDialog.open()
                                }
                            }
                        }
                        
                        // Loading overlay
                        C.CLoadingOverlay {
                            anchors.fill: parent
                            loading: isLoading && taskList.count === 0
                            message: tr.loading
                        }
                    }
                    
                    // Detail pane
                    Rectangle {
                        SplitView.fillWidth: true
                        color: themeColors.window
                        
                        DetailPaneNew {
                            id: detailPane
                            anchors.fill: parent
                            anchors.margins: 16
                            taskIndex: taskList.currentIndex
                            nerdMode: window.nerdMode
                            themeColors: window.themeColors
                            tr: window.tr
                            onArchiveClicked: app.archiveTask(taskIndex)
                            onPrClicked: app.createPR(taskIndex)
                            onPatchClicked: app.extractPatch(taskIndex)
                        }
                    }
                }
                
                // Nerd panel
                NerdPanel {
                    id: nerdPanel
                    SplitView.preferredHeight: 250
                    SplitView.minimumHeight: 150
                    visible: nerdMode
                    themeColors: window.themeColors
                }
            }
            
            // Status bar
            Rectangle {
                Layout.fillWidth: true
                height: 32
                color: themeColors.surface
                
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    
                    // Status indicator dot
                    Rectangle {
                        width: 8
                        height: 8
                        radius: 4
                        color: isLoading ? themeColors.warning : themeColors.success
                        
                        SequentialAnimation on opacity {
                            running: isLoading
                            loops: Animation.Infinite
                            NumberAnimation { to: 0.3; duration: 500 }
                            NumberAnimation { to: 1.0; duration: 500 }
                        }
                    }
                    
                    Text {
                        text: statusText
                        font.pixelSize: 12
                        color: themeColors.textMuted
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Text {
                        text: "⌘N New • ⌘R Refresh • ⌘T Theme"
                        font.pixelSize: 11
                        color: themeColors.textMuted
                        opacity: 0.6
                    }
                }
            }
        }
    }
    
    // Dialogs
    PatchDialog { id: patchDialog }
    SendPromptDialog {
        id: sendPromptDialog
        onPromptSubmitted: function(prompt, envId, branch, bestOf) {
            app.sendPrompt(prompt, envId, branch, bestOf)
        }
    }
    
    // AJAX Queue Widget
    AjaxQueueWidget {
        id: ajaxQueueWidget
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 16
        ajaxQueue: app.ajaxQueue
        themeColors: window.themeColors
        z: 1000
    }
    
    // Keyboard shortcuts
    Shortcut { sequence: "Ctrl+N"; onActivated: { app.loadEnvironments(); sendPromptDialog.open() } }
    Shortcut { sequence: "Ctrl+R"; onActivated: { isLoading = true; app.loadTasks() } }
    Shortcut { sequence: "F5"; onActivated: { isLoading = true; app.loadTasks() } }
    Shortcut { sequence: "Ctrl+`"; onActivated: app.setNerdMode(!nerdMode) }
    Shortcut { sequence: "Ctrl+T"; onActivated: themeSelector.open() }
}
