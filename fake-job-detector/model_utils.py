"""
Model Utilities: Text Preprocessing, Heuristic Red Flag Engine, and Inference Pipeline.
Supports both direct raw copy-pasted text from any platform (LinkedIn, WhatsApp, Telegram,
Indeed, emails) and structured field analysis. Designed with student-friendly explanations.
"""

import re
import os
import joblib

# Curated list of English stopwords to avoid external runtime download dependencies
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "can", "did", "do", "does", "doing", "don", "down", "during", "each", "few", "for", 
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", 
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", 
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", 
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", 
    "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", 
    "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", 
    "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
}

FREE_EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "protonmail.com"]

def clean_text(text: str) -> str:
    """Cleans raw text for NLP vectorization: lowercases, removes URLs, punctuation, and stopwords."""
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    
    # 3. Strip URLs & email addresses
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    
    # 4. Remove special characters and digits, keep alphabetic words
    text = re.sub(r"[^a-z\s]", " ", text)
    
    # 5. Tokenize and remove stopwords
    tokens = [word for word in text.split() if word not in STOPWORDS and len(word) > 2]
    
    return " ".join(tokens)


def extract_metadata_from_raw_text(text: str) -> dict:
    """
    Automatically extracts emails, messaging handles, and salary figures
    from raw text copied from any platform.
    """
    found_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    found_handles = re.findall(r'(?:@[\w\d_]{3,30}|https?://t\.me/\S+|https?://wa\.me/\S+)', text, re.IGNORECASE)
    found_salaries = re.findall(r'\$\s*\d+(?:,\d+)*(?:\.\d+)?(?:\s*(?:per hour|/hr|weekly|daily|per month|/month|a week|per week))?', text, re.IGNORECASE)

    return {
        "emails": list(set(found_emails)),
        "handles": list(set(found_handles)),
        "salaries": list(set(found_salaries))
    }


def analyze_heuristics(full_content: str, extracted_email: str = "") -> dict:
    """
    Evaluates rule-based red flags commonly seen in fake job and internship scams.
    Returns a dictionary of detected flags, risk penalty points, and trigger keywords.
    """
    content_lower = full_content.lower()
    detected_flags = []
    penalty_score = 0
    trigger_words = []

    # 1. Free/Public Email Provider Check for Corporate Hiring
    # Search either extracted email or inline text
    found_free_domain = None
    for domain in FREE_EMAIL_DOMAINS:
        if domain in content_lower or (extracted_email and domain in extracted_email.lower()):
            found_free_domain = domain
            break

    if found_free_domain:
        detected_flags.append({
            "category": "Free Email Used by Recruiter",
            "severity": "High",
            "description": f"The posting uses a free public email provider (@{found_free_domain}) instead of an official company email address. Real companies use their own web domain (like @google.com or @company.com)."
        })
        penalty_score += 25
        trigger_words.append(found_free_domain)

    # 2. Demands for Upfront Fees or Financial Payments (Classic Internship Scam)
    fee_patterns = [
        (r"registration fee", "Mentions a 'registration fee' to apply, register, or get the offer letter."),
        (r"security deposit", "Asks for a refundable or non-refundable 'security deposit'."),
        (r"training fee|toolkit fee|setup fee|kit fee", "Charges the candidate for training, study material, software kit, or laptop setup."),
        (r"wire transfer|western union|moneygram", "Asks to transfer money using wire transfers or Western Union."),
        (r"cashier'?s check|check deposit", "Mentions sending you a check to deposit for purchasing office supplies (common fake check scam)."),
        (r"bitcoin|crypto|usdt|cryptocurrency", "Mentions cryptocurrency or gift cards for payments or tasks.")
    ]
    for pattern, reason in fee_patterns:
        match = re.search(pattern, content_lower)
        if match:
            detected_flags.append({
                "category": "Upfront Money / Fee Demand",
                "severity": "Critical",
                "description": f"{reason} A real job or internship will NEVER ask you to pay them."
            })
            penalty_score += 35
            trigger_words.append(match.group(0))

    # 3. Off-Platform / Anonymous Messaging Channels (Telegram / WhatsApp)
    comm_patterns = [
        (r"\btelegram\b|https?://t\.me/\S+|(?<!\S)@[\w\d_]+(?!\.\w+)", "Directs you to contact on Telegram rather than an official company portal or email."),
        (r"\bwhatsapp\b|https?://wa\.me/\S+", "Conducts interviews or hiring conversations via WhatsApp messages."),
        (r"skype interview only", "Text-only interview on Skype without official video/email verification.")
    ]
    for pattern, reason in comm_patterns:
        match = re.search(pattern, content_lower)
        if match:
            detected_flags.append({
                "category": "Informal / Secret Messaging",
                "severity": "High",
                "description": reason
            })
            penalty_score += 25
            trigger_words.append(match.group(0))

    # 4. Unrealistic Guarantees & Lack of Screening
    unrealistic_patterns = [
        (r"no interview", "Claims 'no interview needed' or guaranteed hiring without testing your skills."),
        (r"guaranteed selection|100% guaranteed", "Promises 100% guaranteed selection or MNC job placement."),
        (r"no experience needed|no prior knowledge", "Promises high compensation for basic work with zero skills required."),
        (r"earn \$\d{3,4}|make \$\d{2,4}\s*(?:per hour|/hr|weekly|daily)", "Promises unusually high pay ($40–$100+/hr) for simple student tasks.")
    ]
    for pattern, reason in unrealistic_patterns:
        match = re.search(pattern, content_lower)
        if match:
            detected_flags.append({
                "category": "Unrealistic Promises",
                "severity": "Medium",
                "description": reason
            })
            penalty_score += 15
            trigger_words.append(match.group(0))

    # 5. Suspicious Task Scams / Reshipping Scams
    task_patterns = [
        (r"like and subscribe|youtube task|maps review", "Pays money for liking YouTube videos or writing Google Maps reviews (Task scam pattern)."),
        (r"package forward|package inspect|reship", "Asks you to receive packages at home and ship them overseas (Reshipping mule scam).")
    ]
    for pattern, reason in task_patterns:
        match = re.search(pattern, content_lower)
        if match:
            detected_flags.append({
                "category": "Suspicious / Illegal Task",
                "severity": "Critical",
                "description": reason
            })
            penalty_score += 35
            trigger_words.append(match.group(0))

    # 6. Brevity / Missing Context Penalty
    if len(full_content.strip()) < 80:
        detected_flags.append({
            "category": "Very Short Description",
            "severity": "Low",
            "description": "The posting is very short and does not explain standard company background or responsibilities."
        })
        penalty_score += 10

    return {
        "flags": detected_flags,
        "penalty_score": min(penalty_score, 70), # Cap penalty score
        "trigger_words": list(set(trigger_words))
    }


def analyze_raw_job_text(model_dir: str, raw_text: str, custom_title: str = "", custom_email: str = "") -> dict:
    """
    Main prediction pipeline. Analyzes full raw text copied from any platform.
    """
    model_path = os.path.join(model_dir, "fake_job_model.pkl")
    vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        raise FileNotFoundError("Model artifacts not found. Please run train_model.py first.")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # 1. Auto-extract metadata from the pasted text
    extracted = extract_metadata_from_raw_text(raw_text)
    primary_email = custom_email or (extracted["emails"][0] if extracted["emails"] else "")

    # 2. Machine Learning TF-IDF Prediction
    cleaned = clean_text(raw_text)
    tfidf_feats = vectorizer.transform([cleaned])
    ml_probabilities = model.predict_proba(tfidf_feats)[0] # [prob_legit, prob_fraud]
    ml_fraud_prob = float(ml_probabilities[1]) * 100.0

    # 3. Heuristic Rules
    heuristics = analyze_heuristics(raw_text, extracted_email=primary_email)
    heuristic_penalty = heuristics["penalty_score"]

    # 4. Composite Risk Score: 65% ML + 35% Heuristics
    composite_risk = (0.65 * ml_fraud_prob) + (0.35 * (heuristic_penalty / 70.0 * 100.0))

    # Critical rule override (e.g. asking for money or cashier checks)
    if any(f["severity"] == "Critical" for f in heuristics["flags"]):
        composite_risk = max(composite_risk, 75.0)

    composite_risk = min(max(round(composite_risk, 1), 0.0), 99.9)

    # 5. Student-Friendly Verdict & Recommendations
    if composite_risk >= 65.0:
        verdict = "HIGH RISK: Likely a Fake Job / Scam"
        verdict_class = "danger"
        badge_text = "FAKE / SCAM ALERT"
        recommendation = "Do NOT apply or reply to this offer! Never pay any fees or send your ID card/bank account details."
    elif composite_risk >= 35.0:
        verdict = "SUSPICIOUS: Proceed with Caution"
        verdict_class = "warning"
        badge_text = "SUSPICIOUS POSTING"
        recommendation = "Some details look unusual. Verify the company on LinkedIn and their official website before sharing any info."
    else:
        verdict = "LOOKS LEGITIMATE: Standard Hiring Pattern"
        verdict_class = "success"
        badge_text = "LIKELY REAL JOB"
        recommendation = "This posting follows standard corporate recruitment patterns. Standard job search safety still applies."

    # Extract first line or snippet as title if not provided
    display_title = custom_title or (raw_text.strip().split("\n")[0][:80] if raw_text.strip() else "Pasted Job Posting")

    return {
        "verdict": verdict,
        "verdict_class": verdict_class,
        "badge_text": badge_text,
        "risk_percentage": composite_risk,
        "ml_probability": round(ml_fraud_prob, 1),
        "legit_probability": round(100.0 - ml_fraud_prob, 1),
        "heuristic_flags": heuristics["flags"],
        "flag_count": len(heuristics["flags"]),
        "trigger_words": heuristics["trigger_words"],
        "recommendation": recommendation,
        "extracted_meta": extracted,
        "raw_text_preview": raw_text[:400] + ("..." if len(raw_text) > 400 else ""),
        "display_title": display_title
    }


def predict_job_posting(model_dir: str, title: str, company: str, description: str, 
                        requirements: str, benefits: str, contact_email: str = "", 
                        salary_text: str = "") -> dict:
    """Backward compatible wrapper for structured inputs."""
    combined_raw = f"{title}\nCompany: {company}\nContact: {contact_email}\nSalary: {salary_text}\n\nDescription:\n{description}\n\nRequirements:\n{requirements}\n\nBenefits:\n{benefits}"
    res = analyze_raw_job_text(model_dir, combined_raw, custom_title=title, custom_email=contact_email)
    res["details"] = {
        "title": title,
        "company": company,
        "contact_email": contact_email
    }
    return res
