# Emotion Detection from Text Messages

A full-stack Natural Language Processing (NLP) and Machine Learning web application designed to analyze text messages and predict the expressed emotional category (`Happy`, `Sad`, `Angry`, `Fear`, `Surprise`, `Neutral`).

> [!IMPORTANT]
> **Psychological Disclaimer**: The predicted emotion represents the emotion expressed in the text message and does not determine a person's actual psychological or mental state.

---

## Features

1. **Text Input & Live Counter**: Textarea with character and word count tracking.
2. **Sample Message Presets**: One-click sample text triggers for all 6 emotion categories.
3. **Empty-Input Validation**: Client-side and server-side validation to prevent empty submissions.
4. **NLP Preprocessing Pipeline**: Tokenization, lowercasing, stopword removal, and WordNet lemmatization powered by NLTK.
5. **Machine Learning Classification**: Multi-class TF-IDF vectorizer + Logistic Regression classifier with fine-grained probability scores.
6. **Detailed Prediction Output**: Expressed emotion badge, confidence percentage, copy-to-clipboard summary, and mandatory disclaimer text.
7. **Text Statistics**: Character count, word count, average word length, unique word count, and lexical density.
8. **Interactive Visualizations**:
   - **Probability Breakdown Chart**: Horizontal bar chart showing confidence scores across all 6 emotion classes (Chart.js).
   - **Historical Emotion Distribution Chart**: Doughnut chart rendering cumulative prediction distribution (Chart.js).
9. **Analysis History & Filtering**: Logs predictions to SQLite database with filtering options by emotion (`All`, `Happy`, `Sad`, `Angry`, `Fear`, `Surprise`, `Neutral`).
10. **Dashboard Overview Stats**: Total analyzed count, dominant emotion, average confidence score.
11. **Clear History Action**: Confirmation modal dialog to purge saved logs.
12. **Responsive Modern UI**: Glassmorphic styling, responsive flexbox/grid layout, emotion-specific color themes, and toast notifications.

---

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+ Fetch API), Chart.js (v4.x), FontAwesome (v6.x)
- **Backend**: Python 3.9+, Flask (REST API)
- **NLP & Machine Learning**: NLTK, Scikit-Learn (TF-IDF Vectorizer + Logistic Regression), Joblib
- **Database**: SQLite3 (`data/emotions.db`)
- **Data & Model**: Pandas, NumPy

---

## Directory Structure

```text
emotion_detection_app/
├── backend/
│   ├── __init__.py
│   ├── app.py                # Main Flask application & REST API routes
│   ├── database.py           # SQLite database schema & CRUD operations
│   ├── nlp_processor.py      # NLTK text preprocessing & statistics calculator
│   └── predictor.py          # Model inference & confidence scoring
├── data/
│   ├── dataset.csv           # Educational training dataset (6 emotion classes)
│   └── emotions.db           # SQLite database (auto-created)
├── model/
│   ├── train_model.py        # Model training script
│   ├── emotion_model.pkl     # Saved trained Scikit-Learn model
│   └── tfidf_vectorizer.pkl  # Saved TF-IDF vectorizer
├── static/
│   ├── css/
│   │   └── style.css         # Responsive modern CSS styling
│   └── js/
│       ├── app.js            # Main UI events, API calls & toast handling
│       └── charts.js         # Chart.js visualization logic
├── templates/
│   └── index.html            # SPA template
├── frontend/
│   └── README.md             # Frontend architecture details
├── requirements.txt          # Python dependencies
└── README.md                 # Complete documentation
```

---

## Setup & Installation Instructions

### 1. Prerequisites
- Python 3.9 or higher installed on your system.
- Git (optional).

### 2. Virtual Environment Setup
Open a terminal in the project directory (`emotion_detection_app`):

**On Windows (PowerShell / Command Prompt):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model
An educational dataset with balanced text samples across all 6 emotions is provided in `data/dataset.csv`. Run the training script:

```bash
python model/train_model.py
```
*(Note: If you skip this step, the backend will automatically run the training script on first launch!)*

### 5. Launch the Web Application
```bash
python backend/app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## REST API Reference

### `POST /api/analyze`
Analyzes a text message and logs the result.

**Request Body:**
```json
{
  "text": "I am so excited and happy about the new project!"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "text": "I am so excited and happy about the new project!",
  "predicted_emotion": "Happy",
  "confidence_score": 96.45,
  "probabilities": {
    "Happy": 96.45,
    "Sad": 0.82,
    "Angry": 0.61,
    "Fear": 0.54,
    "Surprise": 1.12,
    "Neutral": 0.46
  },
  "text_statistics": {
    "char_count": 48,
    "word_count": 9,
    "avg_word_len": 4.33,
    "unique_word_count": 9,
    "lexical_density": 100.0,
    "sentence_count": 1
  },
  "disclaimer": "The predicted emotion represents the emotion expressed in the text message and does not determine a person's actual psychological or mental state."
}
```

### `GET /api/history?emotion=Happy`
Fetches analysis history logs with optional emotion filtering.

### `GET /api/stats`
Fetches aggregate dashboard metrics and emotion count distribution.

### `POST /api/clear-history`
Clears all saved records from the SQLite database.

### `GET /api/samples`
Returns preset sample messages for each emotion category.

---

## Sample Test Examples

Try testing the following text messages in the input box:

| Emotion | Test Input Message |
| :--- | :--- |
| **Happy** | *"I am so excited and happy about the promotion today!"* |
| **Sad** | *"It breaks my heart to see everything turn out like this, I feel so lost."* |
| **Angry** | *"I am completely furious about the unfair treatment and terrible service!"* |
| **Fear** | *"Panicking because I heard strange terrifying sounds in the dark outside."* |
| **Surprise** | *"Wow, unbelievable! I never expected us to win first place!"* |
| **Neutral** | *"The project status meeting is scheduled for tomorrow at 10 AM."* |

---

## License & Attribution

This project is created for educational and demonstration purposes. It combines NLTK text processing, TF-IDF feature extraction, Scikit-Learn classification, SQLite data logging, and Chart.js frontend analytics.
