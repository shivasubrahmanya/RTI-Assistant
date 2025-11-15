import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def preprocess_text(text):
    """Basic text cleaning"""
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def train_model():
    print("📂 Loading dataset...")
    df = pd.read_csv('PIO_Final_Synthetic_60000_fresh.csv')

    print(f"✅ Dataset loaded: {len(df)} rows")
    print(f"Departments: {df['Department'].nunique()} | Authorities: {df['Authority_Name'].nunique()}")

    # Combine Problem Description + Keywords for richer text context
    df['Combined_Text'] = (
        df['Problem_Description'].fillna('') + ' ' + df['Keywords'].fillna('')
    ).apply(preprocess_text)

    X = df['Combined_Text']
    y_dept = df['Department']
    y_auth = df['Authority_Name']

    print("\n✂️ Splitting data...")
    X_train, X_test, y_train_dept, y_test_dept, y_train_auth, y_test_auth = train_test_split(
        X, y_dept, y_auth, test_size=0.2, random_state=42, shuffle=True
    )

    print("🧠 Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=7000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.85
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("🚀 Training Logistic Regression models...")
    model_dept = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs', C=1.0)
    model_auth = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs', C=1.0)

    model_dept.fit(X_train_tfidf, y_train_dept)
    model_auth.fit(X_train_tfidf, y_train_auth)

    print("\n📊 Evaluating models...")

    y_pred_dept = model_dept.predict(X_test_tfidf)
    y_pred_auth = model_auth.predict(X_test_tfidf)

    acc_dept = accuracy_score(y_test_dept, y_pred_dept)
    acc_auth = accuracy_score(y_test_auth, y_pred_auth)

    print(f"✅ Department Model Accuracy: {acc_dept:.4f}")
    print(f"✅ Authority Model Accuracy: {acc_auth:.4f}")

    print("\n🧾 Department Classification Report:")
    print(classification_report(y_test_dept, y_pred_dept))

    print("\n🧾 Authority Classification Report:")
    print(classification_report(y_test_auth, y_pred_auth))

    print("\n💾 Saving both models and vectorizer...")
    model_data = {
        'vectorizer': vectorizer,
        'department_model': model_dept,
        'authority_model': model_auth,
        'accuracy': {
            'department': acc_dept,
            'authority': acc_auth
        },
        'version': 'v2.0'
    }

    with open('model.pkl', 'wb') as f:
        pickle.dump(model_data, f)

    print("🎉 Models saved as model.pkl")
    print("\n✅ Training complete!")


if __name__ == "__main__":
    train_model()
