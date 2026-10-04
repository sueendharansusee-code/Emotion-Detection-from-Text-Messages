# Frontend Architecture - Emotion Detection from Text Messages

This directory contains the documentation and references for the user interface components of the **Emotion Detection from Text Messages** web application.

## Technologies Used
- **HTML5**: Semantic document structure with accessible input elements, badges, stats cards, and modal dialogs.
- **CSS3**: Custom modern styling with CSS variables, responsive Flexbox and Grid layouts, glassmorphism cards, and emotion-specific color themes.
- **JavaScript (ES6+)**: Fetch API for asynchronous REST communication, dynamic DOM updates, input validation, clipboard integration, and toast notifications.
- **Chart.js (v4.x)**: Interactive charts for probability distributions (Horizontal Bar) and historical emotion distribution (Doughnut).
- **FontAwesome (v6.x)**: Iconography for UI actions, emotions, and metrics.

## Key UI Components
1. **Header & Notice**: Branding banner featuring the mandatory psychological disclaimer badge.
2. **Overview Statistics Grid**: Stat cards rendering total analyzed messages, primary emotion, average confidence score, and supported categories.
3. **Interactive Text Input**: Text area with live character/word counters, empty input validation alerts, sample preset buttons, and clear action.
4. **Preset Sample Chips**: Quick-fill sample text buttons for all 6 emotions (`Happy`, `Sad`, `Angry`, `Fear`, `Surprise`, `Neutral`).
5. **Prediction Result Card**: Expressed emotion badge with custom emoji, confidence percentage score, text statistics box, copy button, and Chart.js probability breakdown bar chart.
6. **Historical Analytics & Distribution**: Interactive Chart.js doughnut chart depicting historical emotion trends.
7. **Filterable History Table**: Table displaying past predictions with emotion filter dropdown (`All`, `Happy`, `Sad`, etc.) and a "Clear History" confirmation modal.

## Folder Organization
```text
frontend/
└── README.md
templates/
└── index.html         # Main single-page application layout
static/
├── css/
│   └── style.css      # Complete modern stylesheet
└── js/
    ├── app.js         # API calls, event handlers, clipboard copy & DOM updates
    └── charts.js      # Chart.js initialization and rendering functions
```
