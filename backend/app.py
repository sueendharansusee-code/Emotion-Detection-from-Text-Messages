import os
import sys
from flask import Flask, render_template, request, jsonify

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from backend.predictor import EmotionPredictor
from backend.database import init_db, save_analysis, get_history, get_dashboard_stats, clear_history

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT_DIR, "templates"),
    static_folder=os.path.join(ROOT_DIR, "static")
)

# Initialize database schema and emotion predictor
init_db()
predictor = EmotionPredictor()

DISCLAIMER_TEXT = "The predicted emotion represents the emotion expressed in the text message and does not determine a person's actual psychological or mental state."

SAMPLE_MESSAGES = {
    "Happy": "I am so excited and grateful for the wonderful news today!",
    "Sad": "It breaks my heart to see everything turn out like this, I feel so lost.",
    "Angry": "I am completely furious about the unfair treatment and terrible service!",
    "Fear": "Panicking because I heard strange terrifying sounds in the dark outside.",
    "Surprise": "Wow, unbelievable! I never expected us to win first place!",
    "Neutral": "The project status meeting is scheduled for tomorrow at 10 AM."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Validation Error: Please enter a text message to analyze."
        }), 400

    try:
        result = predictor.predict(text)
        
        # Save to database
        record_id = save_analysis(
            text=text,
            predicted_emotion=result["predicted_emotion"],
            confidence_score=result["confidence_score"],
            probabilities=result["probabilities"],
            text_stats=result["text_statistics"]
        )
        
        result["id"] = record_id
        result["text"] = text
        result["disclaimer"] = DISCLAIMER_TEXT

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Analysis Error: {str(e)}"}), 500

@app.route("/api/history", methods=["GET"])
def history():
    emotion_filter = request.args.get("emotion", "All")
    logs = get_history(emotion_filter=emotion_filter)
    return jsonify({"history": logs, "filter": emotion_filter}), 200

@app.route("/api/stats", methods=["GET"])
def stats():
    dashboard_data = get_dashboard_stats()
    return jsonify(dashboard_data), 200

@app.route("/api/clear-history", methods=["POST"])
def clear_all_history():
    clear_history()
    return jsonify({"message": "Analysis history cleared successfully."}), 200

@app.route("/api/samples", methods=["GET"])
def samples():
    return jsonify({"samples": SAMPLE_MESSAGES}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
