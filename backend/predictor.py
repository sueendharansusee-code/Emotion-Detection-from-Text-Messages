import os
import joblib
import numpy as np
from backend.nlp_processor import NLPProcessor

class EmotionPredictor:
    def __init__(self, model_dir: str = None):
        if model_dir is None:
            model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
        
        self.model_dir = model_dir
        self.vec_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")
        self.model_path = os.path.join(model_dir, "emotion_model.pkl")
        self.nlp = NLPProcessor()
        self.vectorizer = None
        self.model = None
        
        self.load_or_train_model()

    def load_or_train_model(self):
        """Loads trained vectorizer and model, or trains them if missing."""
        if not (os.path.exists(self.vec_path) and os.path.exists(self.model_path)):
            print("Model files missing. Running automated training script...")
            from model.train_model import train_and_save_model
            train_and_save_model()

        self.vectorizer = joblib.load(self.vec_path)
        self.model = joblib.load(self.model_path)

    def predict(self, raw_text: str) -> dict:
        """
        Predict emotion expressed in text message.
        Returns predicted_emotion, confidence_score, probabilities dict, and text statistics.
        """
        if not raw_text or not raw_text.strip():
            raise ValueError("Input text cannot be empty.")

        text_stats = self.nlp.compute_statistics(raw_text)
        processed = self.nlp.preprocess_text(raw_text)

        # Handle cases where preprocessing strips all words (e.g. numbers or punctuation only)
        if not processed:
            processed = raw_text.lower().strip()

        X = self.vectorizer.transform([processed])
        probs = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        # Map classes to probabilities
        prob_dict = {str(cls): round(float(prob) * 100, 2) for cls, prob in zip(classes, probs)}

        # Guarantee all 6 standard emotions are present in prob_dict
        standard_emotions = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Neutral']
        for emo in standard_emotions:
            if emo not in prob_dict:
                prob_dict[emo] = 0.0

        top_idx = int(np.argmax(probs))
        predicted_emotion = str(classes[top_idx])
        confidence_score = prob_dict[predicted_emotion]

        return {
            "predicted_emotion": predicted_emotion,
            "confidence_score": confidence_score,
            "probabilities": prob_dict,
            "text_statistics": text_stats
        }
