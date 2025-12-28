# UI Components Documentation

This document covers the desktop UI implementations: **PyQt6 fakemui** widgets and **QML** components that mirror the React frontend.

## Overview

The project provides two parallel UI implementations:

| Implementation | Location | Purpose |
|----------------|----------|---------|
| **React Frontend** | `frontend/src/` | Web-based UI |
| **QML Desktop** | `src/codex_task_runner/ui/qml/` | Qt Quick desktop app |
| **PyQt6 fakemui** | `src/codex_task_runner/ui/fakemui/` | PyQt6 MUI-style widgets |

---

## QML Component Coverage

### React → QML Mapping (100% Coverage)

| React File | QML Equivalent | Status |
|------------|----------------|--------|
| **contexts/** | | |
| `AjaxQueueContext.jsx` | `contexts/AjaxQueueContext.qml` | ✅ |
| *(themes.js)* | `contexts/ThemeContext.qml` | ✅ |
| *(i18n.js)* | `contexts/LanguageContext.qml` | ✅ |
| *(App.jsx nerdMode)* | `contexts/NerdModeContext.qml` | ✅ |
| **components/** | | |
| `TaskList.jsx` | `components/TaskList.qml` | ✅ |
| `TaskDetail.jsx` | `components/TaskDetail.qml` | ✅ |
| `TaskDetailPlain.jsx` | *(merged into TaskDetail)* | ✅ |
| `NewPrompt.jsx` | `components/NewPrompt.qml` | ✅ |
| `UserInfo.jsx` | `components/UserInfo.qml` | ✅ |
| `SearchDialog.jsx` | `components/SearchDialog.qml` | ✅ |
| `Documentation.jsx` | `components/Documentation.qml` | ✅ |
| `MarkdownRenderer.jsx` | `components/MarkdownRenderer.qml` | ✅ |
| `AjaxQueueWidget.jsx` | `components/AjaxQueueWidget.qml` | ✅ |
| **root files/** | | |
| `App.jsx` | `App.qml` | ✅ |
| `main.jsx` | `main.qml` | ✅ |
| `themes.js` | `contexts/ThemeContext.qml` | ✅ |
| `i18n.js` | `contexts/LanguageContext.qml` | ✅ |

### QML Contexts (Singletons)

Located in `src/codex_task_runner/ui/qml/contexts/`:

| Context | Purpose |
|---------|---------|
| `ThemeContext.qml` | 8 themes (dark, light, midnight, forest, ocean, sunset, rose, highContrast) |
| `LanguageContext.qml` | 19 languages with full translations |
| `NerdModeContext.qml` | Developer mode toggle with persistence |
| `AjaxQueueContext.qml` | AJAX request tracking and queue management |

### QML Fakemui Components

Located in `src/codex_task_runner/ui/qml/components/`:

#### Core UI Components
| Component | Description |
|-----------|-------------|
| `CButton.qml` | MUI-style button with variants (contained, outlined, text) |
| `CCard.qml` | Material card with elevation |
| `CChip.qml` | Chip/tag component |
| `CTextField.qml` | Text input field |
| `CListItem.qml` | List item with icon/text |
| `CToolbar.qml` | App bar / toolbar |
| `CIconButton.qml` | Icon-only button |
| `CTabBar.qml` | Tab navigation |
| `CStatusBadge.qml` | Status indicator badge |
| `CLoadingOverlay.qml` | Loading state overlay |
| `CEmptyState.qml` | Empty state placeholder |
| `CSidebar.qml` | Sidebar / drawer |

#### Lab Components
| Component | Description |
|-----------|-------------|
| `CLoadingButton.qml` | Button with loading spinner |
| `CTimeline.qml` | Timeline container |
| `CTimelineItem.qml` | Timeline item |
| `CTreeView.qml` | Tree view / hierarchy |
| `CMasonry.qml` | Masonry grid layout |

#### MUI X Components
| Component | Description |
|-----------|-------------|
| `CDataGrid.qml` | Data grid with sorting/filtering |
| `CDatePicker.qml` | Date picker dialog |
| `CTimePicker.qml` | Time picker dialog |
| `CDateTimePicker.qml` | Combined date/time picker |

---

## PyQt6 Fakemui Library

Located in `src/codex_task_runner/ui/fakemui/`:

### Package Structure

```
fakemui/
├── __init__.py          # Package exports
├── theme.py             # Theme system (8 themes, palette management)
├── button.py            # MButton, MIconButton, MLoadingButton
├── card.py              # MCard with elevation
├── chip.py              # MChip with variants
├── text_field.py        # MTextField, MTextArea
├── list_widgets.py      # MList, MListItem
├── tabs.py              # MTabs, MTabPanel
├── menu.py              # MMenu, MMenuItem
├── dialog.py            # MDialog, MAlertDialog
├── progress.py          # MCircularProgress, MLinearProgress
├── snackbar.py          # MSnackbar notifications
├── toolbar.py           # MToolbar / AppBar
├── drawer.py            # MDrawer sidebar
├── data_grid.py         # MDataGrid with sorting/pagination
├── date_picker.py       # MDatePicker
├── time_picker.py       # MTimePicker
├── timeline.py          # MTimeline, MTimelineItem
├── tree_view.py         # MTreeView
├── demo.py              # Interactive demo application
└── i18n.py              # Internationalization (19 languages)
```

### Theme System

8 built-in themes matching React:

| Theme | Description |
|-------|-------------|
| `dark` | Default dark theme |
| `light` | Light theme |
| `midnight` | Deep blue dark theme |
| `forest` | Green nature theme |
| `ocean` | Blue ocean theme |
| `sunset` | Warm orange/pink theme |
| `rose` | Pink/rose theme |
| `highContrast` | High contrast accessibility |

### Usage Example

```python
from codex_task_runner.ui.fakemui import (
    MButton, MCard, MTextField, MTheme
)
from PyQt6.QtWidgets import QApplication

app = QApplication([])

# Set theme
MTheme.set_theme("ocean")

# Create widgets
card = MCard()
button = MButton("Click Me", variant="contained")
text_field = MTextField(label="Username")

# Show
card.show()
app.exec()
```

### Running the Demo

```bash
cd /path/to/codex-task-runner-json
source venv/bin/activate
python -c "from codex_task_runner.ui.fakemui.demo import main; main()"
```

---

## i18n Support

Both QML and PyQt6 implementations support 19 languages:

| Code | Language | Flag |
|------|----------|------|
| `en` | English | 🇺🇸 |
| `es` | Español | 🇪🇸 |
| `fr` | Français | 🇫🇷 |
| `de` | Deutsch | 🇩🇪 |
| `ja` | 日本語 | 🇯🇵 |
| `zh` | 中文 | 🇨🇳 |
| `pt` | Português | 🇧🇷 |
| `nl` | Nederlands | 🇳🇱 |
| `it` | Italiano | 🇮🇹 |
| `ko` | 한국어 | 🇰🇷 |
| `ru` | Русский | 🇷🇺 |
| `ar` | العربية | 🇸🇦 |
| `hi` | हिंदी | 🇮🇳 |
| `tr` | Türkçe | 🇹🇷 |
| `pl` | Polski | 🇵🇱 |
| `vi` | Tiếng Việt | 🇻🇳 |
| `th` | ไทย | 🇹🇭 |
| `sv` | Svenska | 🇸🇪 |
| `uk` | Українська | 🇺🇦 |

---

## File Structure Summary

```
src/codex_task_runner/ui/
├── fakemui/                    # PyQt6 MUI-style library
│   ├── __init__.py
│   ├── theme.py
│   ├── button.py
│   ├── card.py
│   ├── ... (15+ modules)
│   └── demo.py
│
└── qml/                        # QML desktop UI
    ├── qmldir                  # Module definition
    ├── Main.qml                # Entry point (legacy, full-featured)
    ├── App.qml                 # Main application (new, context-based)
    ├── NerdPanel.qml           # Developer debug panel
    ├── PatchDialog.qml         # Patch viewer dialog
    ├── SendPromptDialog.qml    # New task dialog
    ├── ThemeSelector.qml       # Theme picker popup
    ├── LanguageSelector.qml    # Language picker popup
    ├── TaskListItem.qml        # Task list item delegate
    │
    ├── contexts/               # Singleton providers
    │   ├── qmldir
    │   ├── ThemeContext.qml
    │   ├── LanguageContext.qml
    │   ├── NerdModeContext.qml
    │   └── AjaxQueueContext.qml
    │
    ├── components/             # App components (React mirrors)
    │   ├── qmldir
    │   ├── TaskList.qml
    │   ├── TaskDetail.qml
    │   ├── NewPrompt.qml
    │   ├── UserInfo.qml
    │   ├── SearchDialog.qml
    │   ├── Documentation.qml
    │   └── MarkdownRenderer.qml
    │
    ├── fakemui/                # QML MUI-style widgets
    │   ├── qmldir
    │   ├── Theme.qml           # Theme singleton
    │   ├── CButton.qml
    │   ├── CCard.qml
    │   ├── CChip.qml
    │   ├── ... (21 components)
    │   └── CDateTimePicker.qml
```

---

## Component Count Summary

| Category | Count |
|----------|-------|
| React Components | 9 |
| React Contexts | 1 |
| React Root Files | 4 |
| **Total React** | **14** |
| QML App Components | 8 |
| QML Contexts | 4 |
| QML Fakemui Components | 21 |
| QML Root Files | 2 |
| **Total QML** | **35** |
| PyQt6 Fakemui Modules | 17 |
| **Grand Total UI Files** | **52+** |

**Coverage: 100%** ✅
