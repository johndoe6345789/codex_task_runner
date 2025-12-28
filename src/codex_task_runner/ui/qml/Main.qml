import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "Codex Task Runner" + (nerdMode ? " 🤓" : "")
    
    // Theme state
    property string currentTheme: "system"
    property var themeColors: getThemeColors(currentTheme)
    
    // Language state
    property string currentLanguage: "en"
    property var tr: getTranslations(currentLanguage)
    
    color: themeColors.window
    
    // All translations
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
            search: "Search tasks, code, prompts...", noResults: "No matching tasks",
        },
        "es": {
            tasks: "Tareas", newTask: "Nueva Tarea", refresh: "Actualizar", openCodex: "Abrir Codex",
            theme: "Tema", language: "Idioma", autoRefresh: "Auto-actualizar", nerdMode: "Modo Nerd",
            noTasks: "No se encontraron tareas", view: "Ver", getPatch: "Obtener Parche", archive: "Archivar",
            untitledTask: "Tarea sin título", noRepo: "Sin repo", details: "Detalles", turns: "Turnos",
            patch: "Parche", createPR: "Crear PR", selectTask: "Selecciona una tarea para ver detalles",
            ready: "Listo", tasksCount: "tareas", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Volver", loading: "Cargando...", copied: "¡Copiado!",
            currentTurn: "Turno Actual", lines: "líneas", connected: "Conectado",
            search: "Buscar tareas, código, prompts...", noResults: "Sin resultados",
        },
        "fr": {
            tasks: "Tâches", newTask: "Nouvelle Tâche", refresh: "Rafraîchir", openCodex: "Ouvrir Codex",
            theme: "Thème", language: "Langue", autoRefresh: "Auto-rafraîchir", nerdMode: "Mode Nerd",
            noTasks: "Aucune tâche trouvée", view: "Voir", getPatch: "Obtenir Patch", archive: "Archiver",
            untitledTask: "Tâche sans titre", noRepo: "Pas de repo", details: "Détails", turns: "Tours",
            patch: "Patch", createPR: "Créer PR", selectTask: "Sélectionnez une tâche",
            ready: "Prêt", tasksCount: "tâches", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Retour", loading: "Chargement...", copied: "Copié!",
            currentTurn: "Tour Actuel", lines: "lignes", connected: "Connecté",
            search: "Rechercher tâches, code, prompts...", noResults: "Aucun résultat",
        },
        "de": {
            tasks: "Aufgaben", newTask: "Neue Aufgabe", refresh: "Aktualisieren", openCodex: "Codex öffnen",
            theme: "Thema", language: "Sprache", autoRefresh: "Auto-Aktualisieren", nerdMode: "Nerd-Modus",
            noTasks: "Keine Aufgaben gefunden", view: "Ansehen", getPatch: "Patch holen", archive: "Archivieren",
            untitledTask: "Unbenannte Aufgabe", noRepo: "Kein Repo", details: "Details", turns: "Runden",
            patch: "Patch", createPR: "PR erstellen", selectTask: "Aufgabe auswählen",
            ready: "Bereit", tasksCount: "Aufgaben", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Zurück", loading: "Laden...", copied: "Kopiert!",
            currentTurn: "Aktuelle Runde", lines: "Zeilen", connected: "Verbunden",
            search: "Suche Aufgaben, Code, Prompts...", noResults: "Keine Ergebnisse",
        },
        "ja": {
            tasks: "タスク", newTask: "新規タスク", refresh: "更新", openCodex: "Codexを開く",
            theme: "テーマ", language: "言語", autoRefresh: "自動更新", nerdMode: "ナードモード",
            noTasks: "タスクがありません", view: "表示", getPatch: "パッチ取得", archive: "アーカイブ",
            untitledTask: "無題のタスク", noRepo: "リポジトリなし", details: "詳細", turns: "ターン",
            patch: "パッチ", createPR: "PR作成", selectTask: "タスクを選択してください",
            ready: "準備完了", tasksCount: "タスク", rawJson: "JSON", prompt: "プロンプト",
            backToTasks: "戻る", loading: "読み込み中...", copied: "コピー完了!",
            currentTurn: "現在のターン", lines: "行", connected: "接続済み",
            search: "タスク、コード、プロンプトを検索...", noResults: "結果なし",
        },
        "zh": {
            tasks: "任务", newTask: "新任务", refresh: "刷新", openCodex: "打开Codex",
            theme: "主题", language: "语言", autoRefresh: "自动刷新", nerdMode: "极客模式",
            noTasks: "未找到任务", view: "查看", getPatch: "获取补丁", archive: "归档",
            untitledTask: "无标题任务", noRepo: "无仓库", details: "详情", turns: "轮次",
            patch: "补丁", createPR: "创建PR", selectTask: "选择任务查看详情",
            ready: "就绪", tasksCount: "个任务", rawJson: "JSON", prompt: "提示",
            backToTasks: "返回", loading: "加载中...", copied: "已复制!",
            currentTurn: "当前轮次", lines: "行", connected: "已连接",
            search: "搜索任务、代码、提示...", noResults: "无结果",
        },
        "ko": {
            tasks: "작업", newTask: "새 작업", refresh: "새로고침", openCodex: "Codex 열기",
            theme: "테마", language: "언어", autoRefresh: "자동 새로고침", nerdMode: "너드 모드",
            noTasks: "작업 없음", view: "보기", getPatch: "패치 가져오기", archive: "보관",
            untitledTask: "제목 없는 작업", noRepo: "저장소 없음", details: "상세", turns: "턴",
            patch: "패치", createPR: "PR 생성", selectTask: "작업을 선택하세요",
            ready: "준비됨", tasksCount: "개 작업", rawJson: "JSON", prompt: "프롬프트",
            backToTasks: "돌아가기", loading: "로딩 중...", copied: "복사됨!",
            currentTurn: "현재 턴", lines: "줄", connected: "연결됨",
            search: "작업, 코드, 프롬프트 검색...", noResults: "결과 없음",
        },
        "ru": {
            tasks: "Задачи", newTask: "Новая задача", refresh: "Обновить", openCodex: "Открыть Codex",
            theme: "Тема", language: "Язык", autoRefresh: "Автообновление", nerdMode: "Режим гика",
            noTasks: "Задачи не найдены", view: "Просмотр", getPatch: "Получить патч", archive: "Архивировать",
            untitledTask: "Без названия", noRepo: "Нет репо", details: "Детали", turns: "Ходы",
            patch: "Патч", createPR: "Создать PR", selectTask: "Выберите задачу",
            ready: "Готово", tasksCount: "задач", rawJson: "JSON", prompt: "Промпт",
            backToTasks: "Назад", loading: "Загрузка...", copied: "Скопировано!",
            currentTurn: "Текущий ход", lines: "строк", connected: "Подключено",
            search: "Поиск задач, кода, промптов...", noResults: "Нет результатов",
        },
        "ar": {
            tasks: "المهام", newTask: "مهمة جديدة", refresh: "تحديث", openCodex: "فتح Codex",
            theme: "المظهر", language: "اللغة", autoRefresh: "تحديث تلقائي", nerdMode: "وضع المطور",
            noTasks: "لا توجد مهام", view: "عرض", getPatch: "الحصول على التصحيح", archive: "أرشفة",
            untitledTask: "مهمة بدون عنوان", noRepo: "لا يوجد مستودع", details: "التفاصيل", turns: "الأدوار",
            patch: "التصحيح", createPR: "إنشاء PR", selectTask: "اختر مهمة",
            ready: "جاهز", tasksCount: "مهام", rawJson: "JSON", prompt: "طلب",
            backToTasks: "عودة", loading: "جاري التحميل...", copied: "تم النسخ!",
            currentTurn: "الدور الحالي", lines: "سطور", connected: "متصل",
            search: "البحث في المهام، الكود، الطلبات...", noResults: "لا توجد نتائج",
        },
        "hi": {
            tasks: "कार्य", newTask: "नया कार्य", refresh: "रिफ्रेश", openCodex: "Codex खोलें",
            theme: "थीम", language: "भाषा", autoRefresh: "ऑटो-रिफ्रेश", nerdMode: "नर्ड मोड",
            noTasks: "कोई कार्य नहीं", view: "देखें", getPatch: "पैच प्राप्त करें", archive: "संग्रहित करें",
            untitledTask: "शीर्षकहीन कार्य", noRepo: "कोई रेपो नहीं", details: "विवरण", turns: "टर्न",
            patch: "पैच", createPR: "PR बनाएं", selectTask: "कार्य चुनें",
            ready: "तैयार", tasksCount: "कार्य", rawJson: "JSON", prompt: "प्रॉम्प्ट",
            backToTasks: "वापस", loading: "लोड हो रहा है...", copied: "कॉपी किया!",
            currentTurn: "वर्तमान टर्न", lines: "पंक्तियाँ", connected: "जुड़ा हुआ",
            search: "कार्य, कोड, प्रॉम्प्ट खोजें...", noResults: "कोई परिणाम नहीं",
        },
        "pt": {
            tasks: "Tarefas", newTask: "Nova Tarefa", refresh: "Atualizar", openCodex: "Abrir Codex",
            theme: "Tema", language: "Idioma", autoRefresh: "Atualização automática", nerdMode: "Modo Nerd",
            noTasks: "Nenhuma tarefa encontrada", view: "Ver", getPatch: "Obter Patch", archive: "Arquivar",
            untitledTask: "Tarefa sem título", noRepo: "Sem repo", details: "Detalhes", turns: "Turnos",
            patch: "Patch", createPR: "Criar PR", selectTask: "Selecione uma tarefa",
            ready: "Pronto", tasksCount: "tarefas", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Voltar", loading: "Carregando...", copied: "Copiado!",
            currentTurn: "Turno Atual", lines: "linhas", connected: "Conectado",
            search: "Buscar tarefas, código, prompts...", noResults: "Sem resultados",
        },
        "it": {
            tasks: "Attività", newTask: "Nuova Attività", refresh: "Aggiorna", openCodex: "Apri Codex",
            theme: "Tema", language: "Lingua", autoRefresh: "Aggiornamento auto", nerdMode: "Modalità Nerd",
            noTasks: "Nessuna attività trovata", view: "Visualizza", getPatch: "Ottieni Patch", archive: "Archivia",
            untitledTask: "Attività senza titolo", noRepo: "Nessun repo", details: "Dettagli", turns: "Turni",
            patch: "Patch", createPR: "Crea PR", selectTask: "Seleziona un\'attività",
            ready: "Pronto", tasksCount: "attività", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Indietro", loading: "Caricamento...", copied: "Copiato!",
            currentTurn: "Turno Corrente", lines: "righe", connected: "Connesso",
            search: "Cerca attività, codice, prompt...", noResults: "Nessun risultato",
        },
        "nl": {
            tasks: "Taken", newTask: "Nieuwe Taak", refresh: "Vernieuwen", openCodex: "Open Codex",
            theme: "Thema", language: "Taal", autoRefresh: "Auto-vernieuwen", nerdMode: "Nerd Modus",
            noTasks: "Geen taken gevonden", view: "Bekijken", getPatch: "Patch Ophalen", archive: "Archiveren",
            untitledTask: "Naamloze Taak", noRepo: "Geen repo", details: "Details", turns: "Beurten",
            patch: "Patch", createPR: "Maak PR", selectTask: "Selecteer een taak",
            ready: "Gereed", tasksCount: "taken", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Terug", loading: "Laden...", copied: "Gekopieerd!",
            currentTurn: "Huidige Beurt", lines: "regels", connected: "Verbonden",
            search: "Zoek taken, code, prompts...", noResults: "Geen resultaten",
        },
        "pl": {
            tasks: "Zadania", newTask: "Nowe Zadanie", refresh: "Odśwież", openCodex: "Otwórz Codex",
            theme: "Motyw", language: "Język", autoRefresh: "Auto-odświeżanie", nerdMode: "Tryb Nerd",
            noTasks: "Nie znaleziono zadań", view: "Zobacz", getPatch: "Pobierz Łatkę", archive: "Archiwizuj",
            untitledTask: "Zadanie bez tytułu", noRepo: "Brak repo", details: "Szczegóły", turns: "Tury",
            patch: "Łatka", createPR: "Utwórz PR", selectTask: "Wybierz zadanie",
            ready: "Gotowe", tasksCount: "zadań", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Wróć", loading: "Ładowanie...", copied: "Skopiowano!",
            currentTurn: "Bieżąca Tura", lines: "linii", connected: "Połączono",
            search: "Szukaj zadań, kodu, promptów...", noResults: "Brak wyników",
        },
        "sv": {
            tasks: "Uppgifter", newTask: "Ny Uppgift", refresh: "Uppdatera", openCodex: "Öppna Codex",
            theme: "Tema", language: "Språk", autoRefresh: "Auto-uppdatera", nerdMode: "Nördläge",
            noTasks: "Inga uppgifter hittades", view: "Visa", getPatch: "Hämta Patch", archive: "Arkivera",
            untitledTask: "Namnlös Uppgift", noRepo: "Inget repo", details: "Detaljer", turns: "Omgångar",
            patch: "Patch", createPR: "Skapa PR", selectTask: "Välj en uppgift",
            ready: "Redo", tasksCount: "uppgifter", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Tillbaka", loading: "Laddar...", copied: "Kopierat!",
            currentTurn: "Aktuell Omgång", lines: "rader", connected: "Ansluten",
            search: "Sök uppgifter, kod, prompts...", noResults: "Inga resultat",
        },
        "tr": {
            tasks: "Görevler", newTask: "Yeni Görev", refresh: "Yenile", openCodex: "Codex Aç",
            theme: "Tema", language: "Dil", autoRefresh: "Otomatik yenile", nerdMode: "Geek Modu",
            noTasks: "Görev bulunamadı", view: "Görüntüle", getPatch: "Yama Al", archive: "Arşivle",
            untitledTask: "Başlıksız Görev", noRepo: "Repo yok", details: "Detaylar", turns: "Turlar",
            patch: "Yama", createPR: "PR Oluştur", selectTask: "Görev seçin",
            ready: "Hazır", tasksCount: "görev", rawJson: "JSON", prompt: "İstem",
            backToTasks: "Geri", loading: "Yükleniyor...", copied: "Kopyalandı!",
            currentTurn: "Mevcut Tur", lines: "satır", connected: "Bağlı",
            search: "Görev, kod, istem ara...", noResults: "Sonuç yok",
        },
        "uk": {
            tasks: "Завдання", newTask: "Нове завдання", refresh: "Оновити", openCodex: "Відкрити Codex",
            theme: "Тема", language: "Мова", autoRefresh: "Автооновлення", nerdMode: "Режим гіка",
            noTasks: "Завдання не знайдено", view: "Переглянути", getPatch: "Отримати патч", archive: "Архівувати",
            untitledTask: "Без назви", noRepo: "Немає репо", details: "Деталі", turns: "Ходи",
            patch: "Патч", createPR: "Створити PR", selectTask: "Оберіть завдання",
            ready: "Готово", tasksCount: "завдань", rawJson: "JSON", prompt: "Промпт",
            backToTasks: "Назад", loading: "Завантаження...", copied: "Скопійовано!",
            currentTurn: "Поточний хід", lines: "рядків", connected: "Підключено",
            search: "Пошук завдань, коду, промптів...", noResults: "Немає результатів",
        },
        "vi": {
            tasks: "Nhiệm vụ", newTask: "Nhiệm vụ mới", refresh: "Làm mới", openCodex: "Mở Codex",
            theme: "Giao diện", language: "Ngôn ngữ", autoRefresh: "Tự động làm mới", nerdMode: "Chế độ Nerd",
            noTasks: "Không có nhiệm vụ", view: "Xem", getPatch: "Lấy Patch", archive: "Lưu trữ",
            untitledTask: "Chưa đặt tên", noRepo: "Không có repo", details: "Chi tiết", turns: "Lượt",
            patch: "Patch", createPR: "Tạo PR", selectTask: "Chọn nhiệm vụ",
            ready: "Sẵn sàng", tasksCount: "nhiệm vụ", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "Quay lại", loading: "Đang tải...", copied: "Đã sao chép!",
            currentTurn: "Lượt hiện tại", lines: "dòng", connected: "Đã kết nối",
            search: "Tìm nhiệm vụ, mã, prompt...", noResults: "Không có kết quả",
        },
        "th": {
            tasks: "งาน", newTask: "งานใหม่", refresh: "รีเฟรช", openCodex: "เปิด Codex",
            theme: "ธีม", language: "ภาษา", autoRefresh: "รีเฟรชอัตโนมัติ", nerdMode: "โหมดเนิร์ด",
            noTasks: "ไม่พบงาน", view: "ดู", getPatch: "รับ Patch", archive: "เก็บถาวร",
            untitledTask: "งานไม่มีชื่อ", noRepo: "ไม่มี repo", details: "รายละเอียด", turns: "เทิร์น",
            patch: "Patch", createPR: "สร้าง PR", selectTask: "เลือกงาน",
            ready: "พร้อม", tasksCount: "งาน", rawJson: "JSON", prompt: "Prompt",
            backToTasks: "กลับ", loading: "กำลังโหลด...", copied: "คัดลอกแล้ว!",
            currentTurn: "เทิร์นปัจจุบัน", lines: "บรรทัด", connected: "เชื่อมต่อแล้ว",
            search: "ค้นหางาน, โค้ด, prompt...", noResults: "ไม่พบผลลัพธ์",
        },
    })
    
    function getTranslations(langId) {
        return allTranslations[langId] || allTranslations["en"]
    }
    
    function getLanguageFlag(langId) {
        var flags = {
            "en": "🇺🇸", "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪", "ja": "🇯🇵",
            "zh": "🇨🇳", "ko": "🇰🇷", "ru": "🇷🇺", "ar": "🇸🇦", "hi": "🇮🇳",
            "pt": "🇧🇷", "it": "🇮🇹", "nl": "🇳🇱", "pl": "🇵🇱", "sv": "🇸🇪",
            "tr": "🇹🇷", "uk": "🇺🇦", "vi": "🇻🇳", "th": "🇹🇭"
        }
        return flags[langId] || "🌐"
    }
    
    // Theme definitions
    readonly property var allThemes: ({
        "system": {
            window: "#2b2b2b",
            windowText: "#ffffff",
            base: "#1e1e1e",
            alternateBase: "#353535",
            text: "#ffffff",
            highlight: "#0078d4",
            mid: "#3c3c3c",
            accent: "#0078d4",
            success: "#2d7d46",
            error: "#c62828",
            warning: "#f57c00",
            info: "#1a73e8",
            codeBackground: "#1e1e1e",
            codeText: "#d4d4d4",
        },
        "light": {
            window: "#f5f5f5",
            windowText: "#1a1a1a",
            base: "#ffffff",
            alternateBase: "#f0f0f0",
            text: "#1a1a1a",
            highlight: "#0078d4",
            mid: "#d0d0d0",
            accent: "#0078d4",
            success: "#2d7d46",
            error: "#c62828",
            warning: "#f57c00",
            info: "#1a73e8",
            codeBackground: "#f8f8f8",
            codeText: "#333333",
        },
        "dark": {
            window: "#1e1e1e",
            windowText: "#e0e0e0",
            base: "#252526",
            alternateBase: "#2d2d30",
            text: "#e0e0e0",
            highlight: "#264f78",
            mid: "#3c3c3c",
            accent: "#569cd6",
            success: "#4ec9b0",
            error: "#f14c4c",
            warning: "#cca700",
            info: "#3794ff",
            codeBackground: "#1e1e1e",
            codeText: "#d4d4d4",
        },
        "hacker": {
            window: "#0a0a0f",
            windowText: "#00ff41",
            base: "#0d0d14",
            alternateBase: "#151520",
            text: "#00ff41",
            highlight: "#00ff41",
            mid: "#1a1a2e",
            accent: "#00ff41",
            success: "#00ff41",
            error: "#ff0055",
            warning: "#ffcc00",
            info: "#00ccff",
            codeBackground: "#0a0a0f",
            codeText: "#00ff41",
        },
        "ocean": {
            window: "#0d1b2a",
            windowText: "#e0e1dd",
            base: "#1b263b",
            alternateBase: "#273549",
            text: "#e0e1dd",
            highlight: "#778da9",
            mid: "#415a77",
            accent: "#4dabf7",
            success: "#40c057",
            error: "#fa5252",
            warning: "#fab005",
            info: "#4dabf7",
            codeBackground: "#0d1b2a",
            codeText: "#a9d1f7",
        },
        "sunset": {
            window: "#1a1423",
            windowText: "#ffd6ba",
            base: "#241b2f",
            alternateBase: "#2e243a",
            text: "#ffd6ba",
            highlight: "#ff7b54",
            mid: "#3d2c4a",
            accent: "#ff7b54",
            success: "#7ec8ac",
            error: "#ff6b6b",
            warning: "#feca57",
            info: "#48dbfb",
            codeBackground: "#1a1423",
            codeText: "#ffb997",
        },
        "forest": {
            window: "#1a2f1a",
            windowText: "#c8e6c9",
            base: "#1e3a1e",
            alternateBase: "#254725",
            text: "#c8e6c9",
            highlight: "#66bb6a",
            mid: "#2e5a2e",
            accent: "#81c784",
            success: "#a5d6a7",
            error: "#ef9a9a",
            warning: "#fff59d",
            info: "#81d4fa",
            codeBackground: "#1a2f1a",
            codeText: "#a5d6a7",
        },
    })
    
    function getThemeColors(themeId) {
        return allThemes[themeId] || allThemes["system"]
    }
    
    function getThemeIcon(themeId) {
        var icons = {
            "system": "💻",
            "light": "☀️",
            "dark": "🌙",
            "hacker": "🤓",
            "ocean": "🌊",
            "sunset": "🌅",
            "forest": "🌲"
        }
        return icons[themeId] || "🎨"
    }
    
    // Status bar message
    property string statusText: "Ready"
    property bool nerdMode: false
    property bool isLoading: false
    
    Connections {
        target: app
        function onStatusMessage(msg) { 
            statusText = msg
            if (msg.startsWith("Loaded") || msg.startsWith("No tasks")) {
                isLoading = false
            }
        }
        function onErrorOccurred(msg) { 
            statusText = "Error: " + msg
            isLoading = false
        }
        function onTasksLoaded() {
            isLoading = false
        }
        function onPatchReady(patch) { patchDialog.show(patch) }
        function onTaskDetailLoaded(json) { detailPane.taskJson = json }
        function onEnvironmentsLoaded(envList) { sendPromptDialog.setEnvironments(envList) }
        function onPromptSuccess(taskId) { sendPromptDialog.showSuccess(taskId) }
        function onPromptError(msg) { sendPromptDialog.showError(msg) }
        function onNerdModeChanged(enabled) { nerdMode = enabled }
        function onDebugLog(msg) { nerdPanel.appendLog(msg) }
        function onSessionInfoChanged(info) { nerdPanel.sessionInfo = info }
        function onThemeChanged(themeId) { 
            currentTheme = themeId
            themeColors = getThemeColors(themeId)
        }
        function onLanguageChanged(langId) {
            currentLanguage = langId
            tr = getTranslations(langId)
        }
    }
    
    Component.onCompleted: {
        isLoading = true
        app.loadTasks()
        // Load saved theme
        var saved = app.getSavedTheme()
        if (saved) {
            currentTheme = saved
            themeColors = getThemeColors(saved)
        }
        // Load saved language
        var savedLang = app.getSavedLanguage()
        if (savedLang) {
            currentLanguage = savedLang
            tr = getTranslations(savedLang)
        }
    }
    
    // Main layout
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // Toolbar
        ToolBar {
            Layout.fillWidth: true
            background: Rectangle {
                color: themeColors.mid
            }
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 4
                spacing: 8
                
                ToolButton {
                    text: "↻ " + tr.refresh
                    onClicked: {
                        isLoading = true
                        app.loadTasks()
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                ToolSeparator {}
                
                ToolButton {
                    text: "✨ " + tr.newTask
                    highlighted: true
                    onClicked: {
                        app.loadEnvironments()
                        sendPromptDialog.open()
                    }
                    ToolTip.visible: hovered
                    ToolTip.text: tr.newTask
                    
                    background: Rectangle {
                        color: themeColors.accent
                        radius: 4
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                ToolButton {
                    text: "🌐 " + tr.openCodex
                    onClicked: app.openCodexBrowser()
                    ToolTip.visible: hovered
                    ToolTip.text: tr.openCodex
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Item { Layout.fillWidth: true }
                
                // Language selector button
                ToolButton {
                    id: languageButton
                    text: getLanguageFlag(currentLanguage)
                    onClicked: languageSelector.open()
                    ToolTip.visible: hovered
                    ToolTip.text: tr.language
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 16
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    LanguageSelector {
                        id: languageSelector
                        x: -width + parent.width
                        y: parent.height + 4
                        currentLanguage: window.currentLanguage
                        
                        onLanguageSelected: function(langId) {
                            window.currentLanguage = langId
                            window.tr = getTranslations(langId)
                            app.setLanguage(langId)
                        }
                    }
                }
                
                // Theme selector button
                ToolButton {
                    id: themeButton
                    text: getThemeIcon(currentTheme)
                    onClicked: themeSelector.open()
                    ToolTip.visible: hovered
                    ToolTip.text: tr.theme + " (Ctrl+T)"
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 16
                        color: themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    ThemeSelector {
                        id: themeSelector
                        x: -width + parent.width
                        y: parent.height + 4
                        currentTheme: window.currentTheme
                        
                        onThemeSelected: function(themeId) {
                            window.currentTheme = themeId
                            window.themeColors = getThemeColors(themeId)
                            app.setTheme(themeId)
                        }
                    }
                }
                
                ToolSeparator {}
                
                Switch {
                    id: autoRefresh
                    text: tr.autoRefresh
                    onCheckedChanged: app.setPolling(checked)
                    
                    contentItem: Text {
                        text: parent.text
                        color: themeColors.windowText
                        leftPadding: parent.indicator.width + parent.spacing
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                ToolSeparator {}
                
                ToolButton {
                    id: nerdModeButton
                    text: nerdMode ? "🤓 " + tr.nerdMode : "🤓"
                    checkable: true
                    checked: nerdMode
                    onCheckedChanged: app.setNerdMode(checked)
                    ToolTip.visible: hovered
                    ToolTip.text: tr.nerdMode + " (Ctrl+`)"
                    
                    background: Rectangle {
                        color: nerdMode ? themeColors.codeBackground : "transparent"
                        radius: 4
                        border.color: nerdMode ? themeColors.accent : "transparent"
                        border.width: 1
                    }
                    contentItem: Text {
                        text: parent.text
                        color: nerdMode ? themeColors.accent : themeColors.windowText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }
        
        // Main content with optional nerd panel
        SplitView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            orientation: Qt.Vertical
            
            // Top section: task list and detail
            SplitView {
                SplitView.fillHeight: !nerdMode
                SplitView.preferredHeight: nerdMode ? parent.height * 0.65 : parent.height
                orientation: Qt.Horizontal
                
                // Task list
                Rectangle {
                    SplitView.preferredWidth: 400
                    SplitView.minimumWidth: 300
                    color: themeColors.base
                    
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 4
                        
                        RowLayout {
                            Layout.fillWidth: true
                            
                            Label {
                                text: tr.tasks
                                font.bold: true
                                font.pixelSize: 16
                                color: themeColors.windowText
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Label {
                                text: taskList.count + " " + tr.tasksCount
                                opacity: 0.6
                                font.pixelSize: 12
                                color: themeColors.windowText
                            }
                        }
                        
                        // Search bar
                        TextField {
                            id: searchField
                            Layout.fillWidth: true
                            placeholderText: "🔍 " + (tr.search || "Search tasks, code, prompts...")
                            color: themeColors.windowText
                            
                            background: Rectangle {
                                color: themeColors.base
                                border.color: searchField.activeFocus ? themeColors.accent : themeColors.mid
                                border.width: 1
                                radius: 4
                            }
                            
                            onTextChanged: {
                                app.setSearchQuery(text)
                            }
                            
                            // Clear button
                            Button {
                                anchors.right: parent.right
                                anchors.rightMargin: 4
                                anchors.verticalCenter: parent.verticalCenter
                                width: 24
                                height: 24
                                visible: searchField.text.length > 0
                                flat: true
                                text: "✕"
                                
                                onClicked: {
                                    searchField.text = ""
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    color: themeColors.textMuted || themeColors.windowText
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                
                                background: Rectangle {
                                    color: parent.hovered ? themeColors.alternateBase : "transparent"
                                    radius: 12
                                }
                            }
                        }
                        
                        ListView {
                            id: taskList
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            model: app.taskModel
                            currentIndex: -1
                            
                            delegate: ItemDelegate {
                                width: taskList.width
                                height: nerdMode ? 95 : 80
                                highlighted: ListView.isCurrentItem
                                
                                background: Rectangle {
                                    color: parent.highlighted ? themeColors.highlight : (parent.hovered ? themeColors.alternateBase : "transparent")
                                    radius: 4
                                }
                                
                                onClicked: {
                                    taskList.currentIndex = index
                                    app.loadTaskDetail(index)
                                }
                                
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    spacing: 2
                                    
                                    RowLayout {
                                        Layout.fillWidth: true
                                        
                                        Label {
                                            text: "#" + model.alias
                                            font.bold: true
                                            color: themeColors.accent
                                        }
                                        
                                        Label {
                                            Layout.fillWidth: true
                                            text: model.title || "Untitled"
                                            elide: Text.ElideRight
                                            font.bold: true
                                            color: themeColors.windowText
                                        }
                                        
                                        // PR indicator
                                        Label {
                                            text: "🔀"
                                            visible: model.hasPr
                                            ToolTip.visible: prMouseArea.containsMouse
                                            ToolTip.text: "Has pull request"
                                            
                                            MouseArea {
                                                id: prMouseArea
                                                anchors.fill: parent
                                                hoverEnabled: true
                                                cursorShape: model.prUrl ? Qt.PointingHandCursor : Qt.ArrowCursor
                                                onClicked: {
                                                    if (model.prUrl) {
                                                        app.openUrl(model.prUrl)
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    
                                    // Nerd mode: show task ID
                                    Label {
                                        Layout.fillWidth: true
                                        text: model.taskId || ""
                                        elide: Text.ElideMiddle
                                        opacity: 0.5
                                        font.pixelSize: 9
                                        font.family: "Menlo"
                                        visible: nerdMode
                                        color: themeColors.accent
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: model.repo || ""
                                        elide: Text.ElideRight
                                        opacity: 0.7
                                        font.pixelSize: 12
                                        color: themeColors.windowText
                                    }
                                    
                                    RowLayout {
                                        Layout.fillWidth: true
                                        
                                        Label {
                                            text: model.status || ""
                                            font.pixelSize: 11
                                            padding: 2
                                            leftPadding: 6
                                            rightPadding: 6
                                            background: Rectangle {
                                                radius: 3
                                                color: {
                                                    switch(model.status) {
                                                        case "completed": return themeColors.success
                                                        case "running": return themeColors.info
                                                        case "failed": return themeColors.error
                                                        default: return themeColors.mid
                                                    }
                                                }
                                            }
                                            color: "white"
                                        }
                                        
                                        Label {
                                            text: model.branch || ""
                                            elide: Text.ElideRight
                                            opacity: 0.5
                                            font.pixelSize: 11
                                            color: themeColors.windowText
                                        }
                                        
                                        Item { Layout.fillWidth: true }
                                        
                                        Label {
                                            text: model.created || ""
                                            opacity: 0.5
                                            font.pixelSize: 11
                                            color: themeColors.windowText
                                        }
                                    }
                                }
                            }
                            
                            ScrollBar.vertical: ScrollBar {}
                            
                            // Empty state
                            Label {
                                anchors.centerIn: parent
                                text: tr.noTasks || "No tasks found"
                                opacity: 0.5
                                font.pixelSize: 14
                                color: themeColors.windowText
                                visible: taskList.count === 0 && !isLoading
                            }
                        }
                        
                        // Loading overlay
                        Rectangle {
                            anchors.fill: parent
                            color: "#CC1e1e1e"
                            visible: isLoading
                            
                            Column {
                                anchors.centerIn: parent
                                spacing: 12
                                
                                BusyIndicator {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    running: isLoading
                                }
                                
                                Label {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: tr.loading || "Loading..."
                                    color: themeColors.windowText
                                    font.pixelSize: 14
                                }
                            }
                        }
                    }
                }
                
                // Detail pane
                Rectangle {
                    SplitView.fillWidth: true
                    color: themeColors.base
                    
                    DetailPane {
                        id: detailPane
                        anchors.fill: parent
                        anchors.margins: 8
                        taskIndex: taskList.currentIndex
                        nerdMode: window.nerdMode
                        themeColors: window.themeColors
                        onArchiveClicked: app.archiveTask(taskIndex)
                        onPrClicked: app.createPR(taskIndex)
                        onPatchClicked: app.extractPatch(taskIndex)
                    }
                }
            }
            
            // Nerd panel (bottom)
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
            height: 28
            color: themeColors.mid
            
            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 8
                anchors.rightMargin: 8
                
                Label {
                    text: statusText
                    verticalAlignment: Text.AlignVCenter
                    opacity: 0.8
                    color: themeColors.windowText
                }
                
                Item { Layout.fillWidth: true }
                
                Label {
                    text: nerdMode ? "Ctrl+N: New | Ctrl+R: Refresh | Ctrl+T: Theme | Ctrl+`: Nerd" : "Ctrl+N: New | Ctrl+R: Refresh | Ctrl+T: Theme"
                    opacity: 0.5
                    font.pixelSize: 11
                    color: themeColors.windowText
                }
            }
        }
    }
    
    // Patch dialog
    PatchDialog {
        id: patchDialog
    }
    
    // Send prompt dialog
    SendPromptDialog {
        id: sendPromptDialog
        onPromptSubmitted: function(prompt, envId, branch, bestOf) {
            app.sendPrompt(prompt, envId, branch, bestOf)
        }
    }
    
    // AJAX Queue Widget (bottom-right corner)
    AjaxQueueWidget {
        id: ajaxQueueWidget
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 16
        ajaxQueue: app.ajaxQueue
        themeColors: window.themeColors
        z: 1000  // Above everything else
    }
    
    // Keyboard shortcuts
    Shortcut {
        sequence: "Ctrl+N"
        onActivated: {
            app.loadEnvironments()
            sendPromptDialog.open()
        }
    }
    
    Shortcut {
        sequence: "Ctrl+R"
        onActivated: app.loadTasks()
    }
    
    Shortcut {
        sequence: "F5"
        onActivated: app.loadTasks()
    }
    
    Shortcut {
        sequence: "Ctrl+`"
        onActivated: {
            nerdModeButton.checked = !nerdModeButton.checked
        }
    }
    
    Shortcut {
        sequence: "Ctrl+T"
        onActivated: themeSelector.open()
    }
}
