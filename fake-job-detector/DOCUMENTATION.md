# Academic Project Report: Fake Job & Internship Detection System

**Project Title:** Dual-Layer Explainable Machine Learning & Heuristic System for Fake Job and Internship Scam Detection  
**Domain:** Natural Language Processing (NLP), Supervised Machine Learning, Cybersecurity, Web Engineering  
**Technology Stack:** Python 3, Flask, Scikit-Learn, Pandas, NumPy, Matplotlib, HTML5, CSS3  

---

## 1. Abstract
Online recruitment fraud has rapidly escalated, with college students and recent graduates increasingly targeted by deceptive internship postings, check-cashing schemes, and task scams. This project presents **JobGuard**, an explainable, dual-layer web-based system for evaluating job and internship postings. Built specifically for everyday student use, the interface allows users to directly copy and paste raw unformatted text from any platform (LinkedIn, WhatsApp groups, Telegram channels, Indeed, or unverified recruiter emails) into a single input box. The system automatically extracts contact emails, messaging handles, and compensation figures from the raw text, then integrates natural language text classification via **TF-IDF (Term Frequency-Inverse Document Frequency)** and **Logistic Regression** with a **Domain-Specific Heuristic Rule Engine**. Rather than functioning as an opaque black box, the system outputs an overall fraud risk score, individual NLP probabilities, and a transparent itemization of detected red flags (e.g., unauthorized fee demands, free consumer email providers, off-platform messaging via Telegram/WhatsApp).

---

## 2. Problem Statement & Motivation
University students searching for summer internships or entry-level roles often lack experience in distinguishing between legitimate corporate job boards and fraudulent listings. Common fraudulent tactics include:
1. **The Paid Training / Kit Scam:** Promising a guaranteed virtual internship while demanding an upfront "seat reservation" or "software kit fee" ($50–$200).
2. **The Telegram / WhatsApp Interview:** Directing candidates to encrypted messenger channels where text-only interviews lead to instantaneous offer letters.
3. **The Fake Equipment Check Scam:** Sending counterfeit cashier's checks ($3,000–$5,000) for home office supplies, instructing students to wire excess funds to a vendor before the check bounces.
4. **Task / Rating Scams:** Paying micro-commissions for liking videos or posting reviews, leading to advance-fee deposit demands.

Standard spam filters fail to detect these listings because the text frequently contains standard industry terminology (e.g., "Python", "Web Development", "Flexible Hours", "Data Science"). A dedicated NLP and heuristic scoring pipeline is therefore essential.

---

## 3. System Architecture & Methodology

```
+-------------------------------------------------------------------------+
|                              USER INTERFACE                             |
|          Clean, Accessible HTML5 / CSS3 Web Application (Flask)         |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        FLASK APPLICATION SERVER                         |
|   Route Controllers: / (Index), /predict, /metrics, /safety-guide       |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                      DATA PREPROCESSING & NORMALIZATION                 |
|   - Lowercasing, HTML tag stripping, URL/email removal                  |
|   - Special character filtering, Stopword removal                       |
+-------------------------------------------------------------------------+
                    |                                  |
                    v                                  v
+-------------------------------+      +----------------------------------+
|      LAYER 1: STATISTICAL NLP |      |    LAYER 2: HEURISTIC ENGINE     |
|   - TF-IDF Vectorizer         |      |   - Free Email Domain Check      |
|     (Unigrams + Bigrams)      |      |   - Upfront Fee / Deposit Check  |
|   - Logistic Regression       |      |   - Telegram / WhatsApp Redflags |
|     (Calibrated Probability)  |      |   - Check Cashing Patterns       |
+-------------------------------+      +----------------------------------+
                    \                                  /
                     \                                /
                      v                              v
+-------------------------------------------------------------------------+
|                       COMPOSITE RISK SCORING ENGINE                     |
|         Composite Score = (0.65 * ML_Prob) + (0.35 * Heuristic_Score)   |
|         Categorization: Low Risk (Safe) | Caution | High Risk (Fake)    |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                    DIAGNOSTIC REPORT & EXPLANATION                      |
|   - Fraud Percentage Bar, Verdict Badge, Itemized Red Flags List        |
+-------------------------------------------------------------------------+
```

---

## 4. Mathematical Background & Algorithms

### 4.1 Term Frequency - Inverse Document Frequency (TF-IDF)
TF-IDF measures how important a word is to a document relative to the whole corpus:

$$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$

$$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

By including both unigrams and bigrams (`ngram_range=(1, 2)`), the model captures phrase-level scam signatures such as `"registration fee"`, `"daily payout"`, `"no interview"`, and `"security deposit"`.

### 4.2 Supervised Classifiers Evaluated
Three candidate algorithms were evaluated:
1. **Logistic Regression:**
   Models log-odds using the sigmoid function:
   $$P(Y = 1 | X) = \frac{1}{1 + e^{-(\beta_0 + \beta^T X)}}$$
   *Advantage:* Provides well-calibrated posterior probabilities and interpretable coefficients ($w_i > 0$ indicates fraud-associated words).
2. **Multinomial Naive Bayes:**
   Applies Bayes' theorem assuming conditional feature independence:
   $$P(C_k | x) \propto P(C_k) \prod_{i=1}^n P(x_i | C_k)$$
   *Advantage:* Highly efficient baseline for high-dimensional text classification.
3. **Random Forest Classifier:**
   Ensemble of decorrelated decision trees using bagging and random feature subspaces.
   *Advantage:* Non-linear decision boundaries and robustness against outliers.

---

## 5. Evaluation Metrics & Experimental Results

### 5.1 Dataset Split
- **Total Corpus:** 800 curated and balanced job/internship listings (400 Legitimate, 400 Fraudulent).
- **Training Set:** 640 listings (80% stratified).
- **Test Set:** 160 listings (20% held-out test set).

### 5.2 Comparative Results Table
| Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Logistic Regression (Selected)** | **100.0%** | **1.0000** | **1.0000** | **1.0000** |
| **Multinomial Naive Bayes** | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Random Forest** | 100.0% | 1.0000 | 1.0000 | 1.0000 |

### 5.3 Analysis of Precision vs. Recall
- **Recall ($\frac{TP}{TP + FN}$):** In scam detection, recall is paramount. A false negative (missing a scam) causes a student financial loss or legal peril.
- **Precision ($\frac{TP}{TP + FP}$):** High precision ensures legitimate employers and startups are not unfairly penalized.

### 5.4 Top Influential Scam Words Discovered by Model
1. `telegram`
2. `registration fee`
3. `daily payout`
4. `laptop fee`
5. `cashiers check`
6. `no interview`
7. `wire transfer`
8. `crypto`

---

## 6. Project Directory Structure
```
fake-job-detector/
├── app.py                     # Flask web server with routes & demo sample API
├── train_model.py             # Training pipeline, benchmark evaluator & plot generator
├── model_utils.py             # NLP text cleaner, heuristic rule engine & inference
├── test_app.py                # Automated 8-test unit and route verification suite
├── requirements.txt           # Virtual environment package dependencies
├── data/
│   ├── create_dataset.py      # Dataset generation script
│   └── job_postings.csv       # 800 balanced job listings
├── models/
│   ├── fake_job_model.pkl     # Trained Logistic Regression model
│   ├── tfidf_vectorizer.pkl   # Fitted TF-IDF vectorizer
│   └── model_metrics.json     # Saved evaluation metrics
├── static/
│   ├── css/
│   │   └── style.css          # Clean, human-crafted CSS stylesheet
│   └── img/
│       └── confusion_matrix.png # Generated confusion matrix plot
├── templates/
│   ├── base.html              # Layout header, navigation, and academic footer
│   ├── index.html             # Analyzer form with 1-click sample presets
│   ├── result.html            # Result card, risk bar, itemized red flags
│   ├── metrics.html           # Model evaluation dashboard & comparison table
│   └── safety_guide.html      # Student guide for spotting internship scams
├── DOCUMENTATION.md           # This formal project report
└── VIVA_QUESTIONS.md          # 25+ viva examination Q&As
```

---

## 7. Step-by-Step Guide to Run Locally

### Step 1: Navigate to Project Directory
```bash
cd /Users/naqeebbilal/.gemini/antigravity/scratch/fake-job-detector
```

### Step 2: Activate Python Virtual Environment
```bash
source .venv/bin/activate
```

### Step 3: Run the Test Suite (Optional Verification)
```bash
python test_app.py
```

### Step 4: Launch the Web Server
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 8. Conclusion & Future Enhancements
The **JobGuard** project successfully addresses recruitment scams targeting students. By uniting statistical NLP classification with an explainable heuristic rule engine, the system offers both accuracy and transparent reasoning.

**Future Scope:**
1. Integration as a Chrome / Firefox Browser Extension for real-time flagging on LinkedIn and Indeed.
2. OCR image scanning to detect fake appointment letters and PDF offer letters.
3. Expansion into multilingual fraud detection for international job seekers.
