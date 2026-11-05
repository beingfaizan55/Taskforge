import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold, cross_val_score
import pickle

print("--- Training Naive Bayes (Category Predictor) ---")

# 1. Dataset Load Karein
df = pd.read_csv('taskforge_large_dataset.csv')

# 2. Text Vectorization
vectorizer = CountVectorizer()
X_text = vectorizer.fit_transform(df['Task_Text'])
y_category = df['Category']

# 3. Model Training
nb_model = MultinomialNB()
nb_model.fit(X_text, y_category)

# 4. K-Fold Cross Validation Evaluation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(nb_model, X_text, y_category, cv=kf)
print(f"K-Fold Accuracy (Naive Bayes): {scores.mean() * 100:.2f}%")

# 5. Save Model & Vectorizer
with open('nb_model.pkl', 'wb') as f:
    pickle.dump({'vectorizer': vectorizer, 'model': nb_model}, f)

print("Saved: nb_model.pkl\n")