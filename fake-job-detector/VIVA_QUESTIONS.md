# Viva Voce & Oral Defense Preparation Guide
## Fake Job & Internship Detection System

This document contains 25+ frequently asked oral examination (Viva Voce) questions with model answers designed to help you secure the highest grades in your project evaluation.

---

### Category 1: Machine Learning & NLP Concepts

#### Q1: What is the main objective of this project?
**Model Answer:**  
"The objective is to detect fraudulent job and internship postings using a hybrid approach combining statistical Natural Language Processing (TF-IDF vectorization with Logistic Regression) and a rule-based Heuristic Engine. It provides an explainable fraud risk score and highlights specific scam red flags like upfront fees and free email domains."

#### Q2: Why did you use TF-IDF instead of simple CountVectorizer (Bag-of-Words)?
**Model Answer:**  
"CountVectorizer only counts raw frequency, which can give undue importance to common words that appear everywhere. TF-IDF downweights words that are common across all documents (via Inverse Document Frequency) and gives higher weight to terms that are specifically distinctive to a particular class (e.g., 'registration fee' or 'wire transfer' in fraudulent postings)."

#### Q3: Why did you use both unigrams and bigrams (`ngram_range=(1, 2)`)?
**Model Answer:**  
"Single words alone can lose critical context. For example, the individual words 'fee' and 'registration' might appear in legitimate documents discussing conference registration. But the bigram phrase 'registration fee' or 'security deposit' has a very strong semantic correlation with internship scams. Bigrams capture this contextual relationship."

#### Q4: Why did you choose Logistic Regression for the final production model?
**Model Answer:**  
"We benchmarked three algorithms: Logistic Regression, Multinomial Naive Bayes, and Random Forest. We selected Logistic Regression for production because:
1. It yields well-calibrated posterior probabilities via the sigmoid function, which allows us to output a precise, granular confidence percentage ($P(\text{fraud})$).
2. It is highly interpretable. By examining the learned coefficients ($w_i$), we can extract the exact words driving the scam prediction.
3. It has minimal inference latency, making web page response instantaneous."

#### Q5: What is the purpose of stopword removal in preprocessing?
**Model Answer:**  
"Stopwords are high-frequency grammatical words (like 'the', 'is', 'at', 'which') that carry little discriminative information for topic classification. Removing them reduces the dimensionality of the feature space, speeds up training and inference, and focuses the model on domain-specific vocabulary."

---

### Category 2: Evaluation Metrics & Confusion Matrix

#### Q6: In fake job detection, which is more important: Precision or Recall?
**Model Answer:**  
"Both are important, but **Recall is more critical for user safety**.  
- **Recall** measures the proportion of actual scams correctly detected. A false negative (missing a scam) means a student might lose hundreds of dollars or fall victim to check fraud.  
- **Precision** measures how many of our flagged scams are truly scams. A false positive simply means a legitimate job posting is flagged for extra manual verification.  
Therefore, we prioritize high Recall while keeping Precision high enough to prevent alert fatigue."

#### Q7: Can you explain the four quadrants of your Confusion Matrix?
**Model Answer:**  
"Yes:
- **True Positive (TP):** A fraudulent job correctly identified as fraud.
- **True Negative (TN):** A legitimate job correctly identified as safe.
- **False Positive (FP - Type I Error):** A legitimate job mistakenly flagged as fraud.
- **False Negative (FN - Type II Error):** A fraudulent job mistakenly classified as legitimate (the most dangerous error)."

#### Q8: What is an F1-Score and why not rely on Accuracy alone?
**Model Answer:**  
"Accuracy can be deceptive if a dataset is imbalanced. For instance, if 95% of postings are real and only 5% are scams, a naive model that predicts 'real' for everything achieves 95% accuracy while missing 100% of scams. The F1-score is the harmonic mean of Precision and Recall:
$$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
It requires both Precision and Recall to be strong to achieve a high score."

#### Q9: How did you prevent data leakage during feature extraction?
**Model Answer:**  
"We strictly performed the `train_test_split` on raw text **before** fitting the `TfidfVectorizer`. The vectorizer was fitted exclusively on the 80% training data, and then used to transform the 20% test partition. This guarantees that test set term frequencies and IDF weights never leaked into the training process."

---

### Category 3: System Architecture & Web Application

#### Q10: Why did you choose Flask for the web backend?
**Model Answer:**  
"Flask is a lightweight, WSGI-compliant micro-framework written in Python. It integrates seamlessly with scientific Python libraries like Scikit-Learn, Pandas, and NumPy without requiring complex intermediary microservices. It allows explicit control over URL routing, HTTP request methods, and Jinja2 server-side template rendering."

#### Q11: Why is this system called a 'Dual-Layer' detector?
**Model Answer:**  
"A purely machine learning model can sometimes miss newly emergent scam patterns if those exact word combinations were underrepresented in the training data. Therefore, our system combines:
1. **Layer 1 (Statistical NLP):** The TF-IDF + Logistic Regression model.
2. **Layer 2 (Heuristic Rule Engine):** Deterministic pattern matchers for known red flags like free email domains (`@gmail.com`), Telegram/WhatsApp redirections, cashier check equipment deposits, and upfront fee demands.  
The composite score blends both layers for robust defense."

#### Q12: How does the preset sample loader work in your UI?
**Model Answer:**  
"To facilitate live demonstrations, we implemented a REST endpoint at `/api/sample/<sample_id>`. When the user selects a preset from the dropdown and clicks 'Load Sample', client-side JavaScript issues an asynchronous `fetch()` call, receives the JSON payload, and populates the form fields instantly without refreshing the page."

---

### Category 4: Domain Knowledge & Cybersecurity

#### Q13: Why is using a `@gmail.com` address considered a red flag for a recruiter?
**Model Answer:**  
"Legitimate corporate recruiters communicate through authenticated enterprise email domains associated with their company website (e.g., `careers@microsoft.com` or `talent@apexcloud.com`). Anyone can create a free account like `microsoft.careers.hr2025@gmail.com` without identity verification. While small startups or family businesses occasionally use free email, large enterprises never do."

#### Q14: How does the 'Cashier Check Equipment Scam' work?
**Model Answer:**  
"The scammer sends the student a fraudulent or stolen cashier's check for an inflated amount (e.g., $4,500) to buy home office gear. By US banking law (Funds Availability Act), banks must make deposited funds available within 1–2 business days before the check has actually cleared. The scammer instructs the student to wire the excess funds to their 'vendor'. Several days later, the check bounces, and the bank debits the student's personal account for the entire sum."

#### Q15: What is a 'Task Scam' targeting university students?
**Model Answer:**  
"Scammers advertise simple online tasks like liking YouTube videos or writing Google Maps reviews for $50/hour. Once the victim completes a few tasks, they are added to a Telegram group and asked to deposit 'crypto security collateral' to unlock VIP tasks. The platform is entirely fake, and the victim cannot withdraw their deposited money."

---

### Category 5: Practical Coding & Architecture Questions

#### Q16: How do you save and reload your trained model in Python?
**Model Answer:**  
"We use the `joblib` library, which is optimized for serializing large NumPy arrays and Scikit-Learn estimator objects:
```python
# Saving
joblib.dump(model, 'models/fake_job_model.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')

# Loading during web inference
model = joblib.load('models/fake_job_model.pkl')
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
```
This avoids retraining the model on every web request."

#### Q17: What happens if a user submits an empty or very short job description?
**Model Answer:**  
"Our web form enforces HTML5 `required` validation on both the Title and Description fields. Furthermore, our server-side `model_utils.py` checks description length; if it is under 80 characters, our heuristic engine triggers a 'Sparse Information' flag because legitimate job postings typically have detailed responsibilities and qualifications."

#### Q18: How would you scale this project for production deployment?
**Model Answer:**  
"In a production environment:
1. Containerize the application using Docker.
2. Serve Flask behind a production WSGI server like Gunicorn with multiple worker processes, behind an Nginx reverse proxy.
3. Build a browser extension (Chrome Manifest V3) that runs the scraper directly on LinkedIn, Indeed, and Handshake web pages."

---

### Category 6: Tips for A+ Viva Presentation
1. **Be confident and concise:** Give structured answers (first state the definition, then explain how you applied it in your project).
2. **Use the live demo presets:** Use the 1-click preset selector on the website to demonstrate both a real job and a scam job without typing errors.
3. **Show the Metrics page:** Walk the examiner through the Confusion Matrix and Model Comparison table at `/metrics`.
4. **Highlight the Student Safety Guide:** Emphasize that your project solves a genuine, pressing issue affecting fellow college students.
