"""
Model Training and Evaluation Pipeline for Fake Job & Internship Detection.
Trains, evaluates, and compares Logistic Regression, Naive Bayes, and Random Forest.
Generates evaluation metrics, confusion matrix visualization, and saves serialized artifacts.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg") # Non-interactive headless backend for server/CLI
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

from model_utils import clean_text

def train_and_evaluate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "job_postings.csv")
    models_dir = os.path.join(base_dir, "models")
    img_dir = os.path.join(base_dir, "static", "img")
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    print("==================================================")
    print("      FAKE JOB & INTERNSHIP DETECTION - ML PIPELINE")
    print("==================================================")
    print(f"Loading dataset from: {data_path}")

    df = pd.read_csv(data_path)
    print(f"Total postings in dataset: {len(df)}")
    print("Class distribution:")
    print(df["fraudulent"].value_counts().rename({0: "Legitimate (0)", 1: "Fraudulent (1)"}))

    # 1. Feature Preprocessing
    # Combine informative textual columns
    text_columns = ["title", "company_name", "company_profile", "description", "requirements", "benefits"]
    for col in text_columns:
        df[col] = df[col].fillna("")

    print("\n[Step 1/5] Cleaning and tokenizing text corpus...")
    df["full_text"] = (
        df["title"] + " " +
        df["company_name"] + " " +
        df["company_profile"] + " " +
        df["description"] + " " +
        df["requirements"] + " " +
        df["benefits"]
    )
    df["cleaned_text"] = df["full_text"].apply(clean_text)

    X = df["cleaned_text"]
    y = df["fraudulent"]

    # 2. Strict Supervised Split (Train: 80%, Test: 20%)
    print("[Step 2/5] Performing stratified train-test split (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)} | Test samples: {len(X_test)}")

    # 3. TF-IDF Featurization
    print("[Step 3/5] Fitting TF-IDF Vectorizer (unigrams + bigrams)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"TF-IDF Feature vocabulary size: {X_train_tfidf.shape[1]}")

    # 4. Model Training & Comparison
    print("\n[Step 4/5] Training and benchmarking candidate models...")
    candidates = {
        "Logistic Regression": LogisticRegression(C=1.0, solver="liblinear", random_state=42),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.5),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = {}
    best_model_name = "Logistic Regression"
    best_f1 = 0.0

    for name, clf in candidates.items():
        clf.fit(X_train_tfidf, y_train)
        y_pred = clf.predict(X_test_tfidf)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm
        }

        print(f" - {name:25s} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    # Preferred production model is Logistic Regression for well-calibrated probabilities
    prod_model = candidates["Logistic Regression"]
    prod_metrics = results["Logistic Regression"]

    # 5. Extract Most Influential Scam Keywords
    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = prod_model.coef_[0]
    top_scam_indices = np.argsort(coefs)[-15:][::-1]
    top_legit_indices = np.argsort(coefs)[:15]

    top_scam_words = [
        {"word": str(feature_names[i]), "weight": round(float(coefs[i]), 3)} 
        for i in top_scam_indices
    ]
    top_legit_words = [
        {"word": str(feature_names[i]), "weight": round(float(coefs[i]), 3)} 
        for i in top_legit_indices
    ]

    # 6. Generate & Save Confusion Matrix Plot
    print("\n[Step 5/5] Generating confusion matrix visualization...")
    y_test_pred = prod_model.predict(X_test_tfidf)
    cm = confusion_matrix(y_test, y_test_pred)

    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(cm, cmap="Blues", alpha=0.85)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = cm[i, j]
            label = f"{val}\n("
            if i == 0 and j == 0:
                label += "True Legit)"
            elif i == 0 and j == 1:
                label += "False Fraud)"
            elif i == 1 and j == 0:
                label += "False Legit)"
            else:
                label += "True Fraud)"
            ax.text(j, i, label, ha="center", va="center", color="black", fontsize=11, fontweight="bold")

    fig.colorbar(cax)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Legitimate (0)", "Fraudulent (1)"], fontsize=10)
    ax.set_yticklabels(["Legitimate (0)", "Fraudulent (1)"], fontsize=10)
    ax.set_xlabel("Predicted Label", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Actual Ground Truth Label", fontsize=11, fontweight="bold")
    ax.set_title("Confusion Matrix - Logistic Regression Classifier", fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()

    cm_chart_path = os.path.join(img_dir, "confusion_matrix.png")
    plt.savefig(cm_chart_path, dpi=200)
    plt.close()
    print(f"Confusion matrix chart saved to: {cm_chart_path}")

    # 7. Save Serialized Model and Metadata
    model_save_path = os.path.join(models_dir, "fake_job_model.pkl")
    vec_save_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    metrics_save_path = os.path.join(models_dir, "model_metrics.json")

    joblib.dump(prod_model, model_save_path)
    joblib.dump(vectorizer, vec_save_path)

    metadata = {
        "dataset_summary": {
            "total_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "legitimate_count": int((df["fraudulent"] == 0).sum()),
            "fraudulent_count": int((df["fraudulent"] == 1).sum()),
        },
        "model_comparison": results,
        "selected_production_model": "Logistic Regression",
        "production_metrics": prod_metrics,
        "top_scam_words": top_scam_words,
        "top_legit_words": top_legit_words
    }

    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"Model saved to: {model_save_path}")
    print(f"Vectorizer saved to: {vec_save_path}")
    print(f"Metrics metadata saved to: {metrics_save_path}")
    print("\n Model training & evaluation complete! Everything ready for web app.")

if __name__ == "__main__":
    train_and_evaluate()
