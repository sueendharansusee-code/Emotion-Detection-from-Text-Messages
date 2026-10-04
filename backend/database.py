import os
import sqlite3
import json

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "emotions.db"))

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            predicted_emotion TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            probabilities_json TEXT NOT NULL,
            char_count INTEGER,
            word_count INTEGER,
            avg_word_len REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(text: str, predicted_emotion: str, confidence_score: float, probabilities: dict, text_stats: dict):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_history 
        (text, predicted_emotion, confidence_score, probabilities_json, char_count, word_count, avg_word_len)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        text,
        predicted_emotion,
        confidence_score,
        json.dumps(probabilities),
        text_stats.get('char_count', 0),
        text_stats.get('word_count', 0),
        text_stats.get('avg_word_len', 0.0)
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_history(emotion_filter: str = None, limit: int = 100):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    if emotion_filter and emotion_filter.strip() and emotion_filter.lower() != 'all':
        cursor.execute("""
            SELECT id, text, predicted_emotion, confidence_score, probabilities_json,
                   char_count, word_count, avg_word_len, created_at
            FROM analysis_history
            WHERE LOWER(predicted_emotion) = LOWER(?)
            ORDER BY created_at DESC
            LIMIT ?
        """, (emotion_filter, limit))
    else:
        cursor.execute("""
            SELECT id, text, predicted_emotion, confidence_score, probabilities_json,
                   char_count, word_count, avg_word_len, created_at
            FROM analysis_history
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

    rows = cursor.fetchall()
    history = []
    for r in rows:
        item = dict(r)
        try:
            item['probabilities'] = json.loads(item['probabilities_json'])
        except Exception:
            item['probabilities'] = {}
        history.append(item)

    conn.close()
    return history

def get_dashboard_stats():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Total analyzed
    cursor.execute("SELECT COUNT(*) as total FROM analysis_history")
    total_count = cursor.fetchone()['total']

    if total_count == 0:
        conn.close()
        return {
            "total_analyzed": 0,
            "top_emotion": "None",
            "avg_confidence": 0.0,
            "emotion_counts": {
                "Happy": 0, "Sad": 0, "Angry": 0, "Fear": 0, "Surprise": 0, "Neutral": 0
            }
        }

    # Average confidence
    cursor.execute("SELECT AVG(confidence_score) as avg_conf FROM analysis_history")
    avg_confidence = round(cursor.fetchone()['avg_conf'] or 0.0, 1)

    # Breakdown by emotion
    cursor.execute("""
        SELECT predicted_emotion, COUNT(*) as count 
        FROM analysis_history 
        GROUP BY predicted_emotion
    """)
    rows = cursor.fetchall()

    emotion_counts = {
        "Happy": 0, "Sad": 0, "Angry": 0, "Fear": 0, "Surprise": 0, "Neutral": 0
    }
    top_emotion = "None"
    max_c = -1

    for r in rows:
        emo = r['predicted_emotion']
        cnt = r['count']
        emotion_counts[emo] = cnt
        if cnt > max_c:
            max_c = cnt
            top_emotion = emo

    conn.close()
    return {
        "total_analyzed": total_count,
        "top_emotion": top_emotion,
        "avg_confidence": avg_confidence,
        "emotion_counts": emotion_counts
    }

def clear_history():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history")
    conn.commit()
    conn.close()
    return True
