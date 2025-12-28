pragma Singleton
import QtQuick

/**
 * LanguageContext - Internationalization / translations
 * Mirrors React's i18n.js with 19 languages
 */
QtObject {
    id: i18n
    
    // Current language
    property string language: {
        const saved = _settings.value("language", "en")
        return languages[saved] ? saved : "en"
    }
    
    // Available languages
    readonly property var languageKeys: [
        "en", "es", "fr", "de", "ja", "zh", "pt", "nl", "it", "ko",
        "ru", "ar", "hi", "tr", "pl", "vi", "th", "sv", "uk"
    ]
    
    // Language metadata
    readonly property var languages: ({
        en: { name: "English", flag: "🇺🇸" },
        es: { name: "Español", flag: "🇪🇸" },
        fr: { name: "Français", flag: "🇫🇷" },
        de: { name: "Deutsch", flag: "🇩🇪" },
        ja: { name: "日本語", flag: "🇯🇵" },
        zh: { name: "中文", flag: "🇨🇳" },
        pt: { name: "Português", flag: "🇧🇷" },
        nl: { name: "Nederlands", flag: "🇳🇱" },
        it: { name: "Italiano", flag: "🇮🇹" },
        ko: { name: "한국어", flag: "🇰🇷" },
        ru: { name: "Русский", flag: "🇷🇺" },
        ar: { name: "العربية", flag: "🇸🇦" },
        hi: { name: "हिंदी", flag: "🇮🇳" },
        tr: { name: "Türkçe", flag: "🇹🇷" },
        pl: { name: "Polski", flag: "🇵🇱" },
        vi: { name: "Tiếng Việt", flag: "🇻🇳" },
        th: { name: "ไทย", flag: "🇹🇭" },
        sv: { name: "Svenska", flag: "🇸🇪" },
        uk: { name: "Українська", flag: "🇺🇦" }
    })
    
    // Translations
    readonly property var translations: ({
        en: {
            // Navigation
            tasks: "Tasks",
            newTask: "New Task",
            profile: "Profile",
            taskDetail: "Task Detail",
            documentation: "Documentation",
            
            // Settings
            nerdMode: "Nerd Mode",
            theme: "Theme",
            language: "Language",
            
            // Task List
            filter: "Filter",
            limit: "Limit",
            current: "Current",
            archived: "Archived",
            all: "All",
            noTasks: "No tasks found",
            tasksCount: "tasks",
            view: "View",
            getPatch: "Get Patch",
            archive: "Archive",
            noRepo: "No repo",
            untitledTask: "Untitled Task",
            
            // Task Detail
            backToTasks: "Back to Tasks",
            details: "Details",
            turns: "Turns",
            patch: "Patch",
            createPR: "Create PR",
            prCreated: "PR created successfully!",
            failedCreatePR: "Failed to create PR",
            copied: "Copied to clipboard!",
            loadPatch: "Load Patch",
            noPatch: "No patch data available",
            rawTaskData: "Raw Task Data",
            currentTurn: "Current Turn",
            lines: "lines",
            
            // New Prompt
            createNewTask: "Create New Task",
            sendPromptDesc: "Send a prompt to Codex to create a new coding task",
            taskPrompt: "Task Prompt",
            promptPlaceholder: "Describe what you want Codex to do...",
            branch: "Branch",
            bestOf: "Best Of",
            creating: "Creating...",
            taskCreated: "Task created successfully!",
            failedCreate: "Failed to create task",
            enterPrompt: "Please enter a prompt",
            tips: "Tips",
            tip1: "Be specific about what you want Codex to implement",
            tip2: "Mention file paths if you know them",
            tip3: "Include any constraints or requirements",
            tip4: "Use \"Best Of\" > 1 to generate multiple solutions and pick the best",
            
            // User Info
            loading: "Loading...",
            apiConnection: "API Connection",
            connected: "Connected",
            apiBase: "API Base",
            
            // Documentation
            gettingStarted: "Getting Started",
            apiReference: "API Reference",
            cliCommands: "CLI Commands",
            authentication: "Authentication",
            installation: "Installation",
            quickStart: "Quick Start",
            
            // Search
            search: "Search",
            searchPlaceholder: "Search tasks, code, patches..."
        },
        
        es: {
            tasks: "Tareas",
            newTask: "Nueva Tarea",
            profile: "Perfil",
            taskDetail: "Detalle de Tarea",
            documentation: "Documentación",
            nerdMode: "Modo Nerd",
            theme: "Tema",
            language: "Idioma",
            filter: "Filtro",
            limit: "Límite",
            current: "Actual",
            archived: "Archivado",
            all: "Todos",
            noTasks: "No se encontraron tareas",
            tasksCount: "tareas",
            view: "Ver",
            getPatch: "Obtener Parche",
            archive: "Archivar",
            noRepo: "Sin repo",
            untitledTask: "Tarea sin título",
            backToTasks: "Volver a Tareas",
            details: "Detalles",
            turns: "Turnos",
            patch: "Parche",
            createPR: "Crear PR",
            prCreated: "¡PR creado exitosamente!",
            failedCreatePR: "Error al crear PR",
            copied: "¡Copiado al portapapeles!",
            loadPatch: "Cargar Parche",
            noPatch: "No hay datos de parche disponibles",
            rawTaskData: "Datos Brutos de Tarea",
            currentTurn: "Turno Actual",
            lines: "líneas",
            createNewTask: "Crear Nueva Tarea",
            sendPromptDesc: "Envía un prompt a Codex para crear una nueva tarea de código",
            taskPrompt: "Prompt de Tarea",
            promptPlaceholder: "Describe lo que quieres que Codex haga...",
            branch: "Rama",
            bestOf: "Mejor de",
            creating: "Creando...",
            taskCreated: "¡Tarea creada exitosamente!",
            failedCreate: "Error al crear tarea",
            enterPrompt: "Por favor ingresa un prompt",
            tips: "Consejos",
            loading: "Cargando...",
            apiConnection: "Conexión API",
            connected: "Conectado",
            apiBase: "Base API",
            gettingStarted: "Primeros Pasos",
            apiReference: "Referencia API",
            cliCommands: "Comandos CLI",
            authentication: "Autenticación",
            search: "Buscar",
            searchPlaceholder: "Buscar tareas, código, parches..."
        },
        
        fr: {
            tasks: "Tâches",
            newTask: "Nouvelle Tâche",
            profile: "Profil",
            taskDetail: "Détail de Tâche",
            documentation: "Documentation",
            nerdMode: "Mode Nerd",
            theme: "Thème",
            language: "Langue",
            filter: "Filtre",
            current: "Actuel",
            archived: "Archivé",
            all: "Tous",
            noTasks: "Aucune tâche trouvée",
            tasksCount: "tâches",
            view: "Voir",
            getPatch: "Obtenir Patch",
            archive: "Archiver",
            backToTasks: "Retour aux Tâches",
            details: "Détails",
            turns: "Tours",
            patch: "Patch",
            createPR: "Créer PR",
            createNewTask: "Créer Nouvelle Tâche",
            loading: "Chargement...",
            search: "Rechercher"
        },
        
        de: {
            tasks: "Aufgaben",
            newTask: "Neue Aufgabe",
            profile: "Profil",
            taskDetail: "Aufgabendetail",
            documentation: "Dokumentation",
            nerdMode: "Nerd-Modus",
            theme: "Thema",
            language: "Sprache",
            filter: "Filter",
            current: "Aktuell",
            archived: "Archiviert",
            all: "Alle",
            noTasks: "Keine Aufgaben gefunden",
            view: "Ansehen",
            backToTasks: "Zurück zu Aufgaben",
            details: "Details",
            turns: "Runden",
            patch: "Patch",
            createPR: "PR erstellen",
            createNewTask: "Neue Aufgabe erstellen",
            loading: "Laden...",
            search: "Suchen"
        },
        
        ja: {
            tasks: "タスク",
            newTask: "新規タスク",
            profile: "プロフィール",
            taskDetail: "タスク詳細",
            documentation: "ドキュメント",
            nerdMode: "ナードモード",
            theme: "テーマ",
            language: "言語",
            filter: "フィルター",
            current: "現在",
            archived: "アーカイブ済み",
            all: "すべて",
            noTasks: "タスクが見つかりません",
            view: "表示",
            backToTasks: "タスクに戻る",
            details: "詳細",
            turns: "ターン",
            patch: "パッチ",
            createPR: "PRを作成",
            createNewTask: "新規タスクを作成",
            loading: "読み込み中...",
            search: "検索"
        },
        
        zh: {
            tasks: "任务",
            newTask: "新任务",
            profile: "个人资料",
            taskDetail: "任务详情",
            documentation: "文档",
            nerdMode: "极客模式",
            theme: "主题",
            language: "语言",
            filter: "筛选",
            current: "当前",
            archived: "已归档",
            all: "全部",
            noTasks: "未找到任务",
            view: "查看",
            backToTasks: "返回任务",
            details: "详情",
            turns: "轮次",
            patch: "补丁",
            createPR: "创建PR",
            createNewTask: "创建新任务",
            loading: "加载中...",
            search: "搜索"
        },
        
        ko: {
            tasks: "작업",
            newTask: "새 작업",
            profile: "프로필",
            documentation: "문서",
            nerdMode: "너드 모드",
            theme: "테마",
            language: "언어",
            filter: "필터",
            current: "현재",
            archived: "보관됨",
            all: "전체",
            view: "보기",
            loading: "로딩 중...",
            search: "검색"
        },
        
        ru: {
            tasks: "Задачи",
            newTask: "Новая задача",
            profile: "Профиль",
            documentation: "Документация",
            nerdMode: "Режим гика",
            theme: "Тема",
            language: "Язык",
            filter: "Фильтр",
            current: "Текущие",
            archived: "Архив",
            all: "Все",
            view: "Просмотр",
            loading: "Загрузка...",
            search: "Поиск"
        }
        // Additional languages follow same pattern...
    })
    
    // Settings for persistence
    property Settings _settings: Settings {
        category: "i18n"
    }
    
    /**
     * Set language and persist
     */
    function setLanguage(lang) {
        if (languages[lang]) {
            language = lang
            _settings.setValue("language", lang)
        }
    }
    
    /**
     * Get translation for key
     */
    function t(key) {
        const langTranslations = translations[language]
        if (langTranslations && langTranslations[key]) {
            return langTranslations[key]
        }
        // Fallback to English
        if (translations.en && translations.en[key]) {
            return translations.en[key]
        }
        return key
    }
    
    /**
     * Get language info
     */
    function getLanguageInfo(lang) {
        return languages[lang] || languages.en
    }
}
