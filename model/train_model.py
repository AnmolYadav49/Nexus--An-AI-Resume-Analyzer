import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def train_model():
    print("Loading dataset...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, 'dataset.csv'))
    
    # Preprocess text
    df['cleaned_text'] = df['resume_text'].apply(clean_text)
    
    X = df['cleaned_text']
    y_labels = df['role']
    
    print("Training model components...")
    
    # 1. Label Encoder
    le = LabelEncoder()
    y = le.fit_transform(y_labels)
    
    # 2. TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_vec = vectorizer.fit_transform(X)
    
    # 3. Classifier Model
    clf = LogisticRegression(random_state=42)
    clf.fit(X_vec, y)
    
    print("Training complete. Accuracy (on training set) =", clf.score(X_vec, y))
    
    # Save isolated components
    joblib.dump(clf, os.path.join(base_dir, 'model.pkl'))
    joblib.dump(vectorizer, os.path.join(base_dir, 'tfidf.pkl'))
    joblib.dump(le, os.path.join(base_dir, 'label_encoder.pkl'))
    
    print(f"Models saved successfully to {base_dir}")

if __name__ == "__main__":
    train_model()
