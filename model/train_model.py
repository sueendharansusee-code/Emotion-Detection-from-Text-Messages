import os
import sys
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Add root project path to import backend modules
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from backend.nlp_processor import NLPProcessor

EMOTIONS = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Neutral']

def train_and_save_model():
    dataset_path = os.path.join(ROOT_DIR, "data", "dataset.csv")
    model_dir = os.path.join(ROOT_DIR, "model")

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at {dataset_path}")

    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    print(f"Dataset shape: {df.shape}")
    print("Class distribution:\n", df['emotion'].value_counts())

    nlp = NLPProcessor()
    print("Preprocessing dataset text with NLTK...")
    df['processed_text'] = df['text'].apply(lambda x: nlp.preprocess_text(str(x)))

    # Fallback for empty processed text
    df['processed_text'] = df['processed_text'].replace('', 'neutral')

    X = df['processed_text']
    y = df['emotion']

    print("Extracting features with TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )
    X_tfidf = vectorizer.fit_transform(X)

    print("Training Logistic Regression Classifier...")
    model = LogisticRegression(C=2.0, max_iter=1000, solver='lbfgs')
    model.fit(X_tfidf, y)

    # Evaluate on training data
    y_pred = model.predict(X_tfidf)
    acc = accuracy_score(y, y_pred)
    print(f"\nTraining Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y, y_pred, target_names=model.classes_))

    # Save vectorizer and model
    os.makedirs(model_dir, exist_ok=True)
    vec_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")
    model_path = os.path.join(model_dir, "emotion_model.pkl")

    joblib.dump(vectorizer, vec_path)
    joblib.dump(model, model_path)

    print(f"\nVectorizer saved to: {vec_path}")
    print(f"Model saved to: {model_path}")
    print("Model training complete!")

if __name__ == "__main__":
    train_and_save_model()
