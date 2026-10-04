import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure required NLTK resources are available
NLTK_RESOURCES = ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'punkt_tab']
for resource in NLTK_RESOURCES:
    try:
        nltk.download(resource, quiet=True)
    except Exception as e:
        print(f"Warning: Failed to download NLTK resource '{resource}': {e}")

class NLPProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'it', 'this', 'that'}

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text: lowercasing, non-alphanumeric cleaning, tokenization,
        stopword removal, and lemmatization.
        """
        if not text:
            return ""

        # Lowercase
        cleaned = text.lower()

        # Keep letters and basic whitespace
        cleaned = re.sub(r'[^a-z\s]', ' ', cleaned)

        # Tokenize
        try:
            tokens = word_tokenize(cleaned)
        except Exception:
            tokens = cleaned.split()

        # Remove stopwords & lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 1
        ]

        return " ".join(processed_tokens)

    def compute_statistics(self, text: str) -> dict:
        """
        Compute text statistics such as character count, word count,
        average word length, unique words, and lexical density.
        """
        if not text:
            return {
                "char_count": 0,
                "word_count": 0,
                "avg_word_len": 0.0,
                "unique_word_count": 0,
                "lexical_density": 0.0,
                "sentence_count": 0
            }

        char_count = len(text)
        
        # Word extraction
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        if word_count > 0:
            avg_word_len = round(sum(len(w) for w in words) / word_count, 2)
            unique_word_count = len(set(w.lower() for w in words))
            lexical_density = round((unique_word_count / word_count) * 100, 1)
        else:
            avg_word_len = 0.0
            unique_word_count = 0
            lexical_density = 0.0

        try:
            sentences = sent_tokenize(text)
            sentence_count = len(sentences)
        except Exception:
            sentence_count = len(re.split(r'[.!?]+', text)) - 1
            if sentence_count <= 0:
                sentence_count = 1

        return {
            "char_count": char_count,
            "word_count": word_count,
            "avg_word_len": avg_word_len,
            "unique_word_count": unique_word_count,
            "lexical_density": lexical_density,
            "sentence_count": sentence_count
        }
