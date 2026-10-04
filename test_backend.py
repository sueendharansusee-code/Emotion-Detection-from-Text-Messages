import os
import sys
import unittest
import json

# Ensure project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from backend.nlp_processor import NLPProcessor
from backend.predictor import EmotionPredictor
from backend.database import init_db, save_analysis, get_history, get_dashboard_stats, clear_history
from backend.app import app

class TestEmotionDetectionApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.predictor = EmotionPredictor()
        cls.client = app.test_client()

    def test_01_nlp_processor(self):
        nlp = NLPProcessor()
        text = "I am so happy, excited and joyful today!"
        cleaned = nlp.preprocess_text(text)
        stats = nlp.compute_statistics(text)

        self.assertIn("happy", cleaned)
        self.assertEqual(stats["word_count"], 8)
        self.assertGreater(stats["char_count"], 0)
        self.assertGreater(stats["avg_word_len"], 0)

    def test_02_predictions_all_emotions(self):
        samples = {
            "Happy": "I am so happy and overjoyed with this great news!",
            "Sad": "It breaks my heart to see everything turn out so bad.",
            "Angry": "I am furious and outraged by your awful behavior!",
            "Fear": "Panicking because I am terrified of the dark footsteps.",
            "Surprise": "Wow, unbelievable! I never expected this secret party!",
            "Neutral": "The meeting is scheduled for tomorrow at 10 AM."
        }

        for expected_emotion, text in samples.items():
            result = self.predictor.predict(text)
            self.assertEqual(result["predicted_emotion"], expected_emotion, f"Failed prediction for {expected_emotion}")
            self.assertGreaterEqual(result["confidence_score"], 30.0)
            self.assertIn("probabilities", result)
            self.assertEqual(len(result["probabilities"]), 6)

    def test_03_api_analyze(self):
        response = self.client.post(
            "/api/analyze",
            data=json.dumps({"text": "Congratulations on your amazing success!"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["predicted_emotion"], "Happy")
        self.assertIn("disclaimer", data)
        self.assertIn("confidence_score", data)

    def test_04_api_validation_error(self):
        response = self.client.post(
            "/api/analyze",
            data=json.dumps({"text": "   "}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_05_api_stats_and_history(self):
        # Fetch stats
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        stats_data = response.get_json()
        self.assertGreater(stats_data["total_analyzed"], 0)

        # Fetch history
        response = self.client.get("/api/history?emotion=Happy")
        self.assertEqual(response.status_code, 200)
        hist_data = response.get_json()
        self.assertIsInstance(hist_data["history"], list)

        # Fetch samples
        response = self.client.get("/api/samples")
        self.assertEqual(response.status_code, 200)
        samples_data = response.get_json()
        self.assertIn("Happy", samples_data["samples"])

    def test_06_clear_history(self):
        response = self.client.post("/api/clear-history")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/stats")
        stats_data = response.get_json()
        self.assertEqual(stats_data["total_analyzed"], 0)

if __name__ == "__main__":
    unittest.main()
