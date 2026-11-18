"""
Flask Web Application for Fake Job & Internship Detection
Designed for students: simple copy-paste scanner from any platform (LinkedIn, WhatsApp, Telegram, etc.)
"""

import os
import json
from flask import Flask, render_template, request, jsonify
from model_utils import analyze_raw_job_text, predict_job_posting

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

# Realistic raw text samples that students actually see on LinkedIn, WhatsApp, Telegram, and job boards
STUDENT_SAMPLES = {
    "scam_whatsapp_typing": {
        "title": "❌ Fake WhatsApp / Telegram Typing Job Scam",
        "platform": "WhatsApp Message / Telegram Channel",
        "text": """URGENT HIRING! Work From Home Online Data Entry & Typist Needed!

Make $45 to $75 per hour working simply from your mobile phone or laptop.
Daily workload: 2-3 hours only.
Work includes typing MS Word documents, copy-pasting customer survey data, and form filling.

Requirements:
- Anyone can apply: College students, freshers, housewives welcome!
- No prior experience or coding knowledge required.
- NO INTERVIEW NEEDED! 100% Guaranteed Selection.

Benefits:
- Daily payout directly via PayPal, CashApp, or Zelle.
- Earn up to $4,500 every single week!
- Free company laptop and Apple iPad sent to your home address after a small refundable registration and verification fee of $85.

To claim your position and start working today, message our hiring manager on Telegram: @HiringManager_Official or WhatsApp +1-829-491-0021.
Contact Email: hr.globalplacement24@gmail.com"""
    },
    "scam_internship_fee": {
        "title": "❌ Fake Paid Certificate & Training Internship",
        "platform": "College WhatsApp Group / Unverified Email",
        "text": """Summer Web Development & Artificial Intelligence Internship 2025

National Career Placement Hub is offering an elite 8-week virtual summer internship program for undergraduate students.

What you will do:
- Work on industry-grade live projects in Python, Web Development, and AI.
- Receive mentorship from top software engineers.
- 100% GUARANTEED placement assistance in top tier MNC companies upon completion.

Eligibility:
- B.Tech, BCA, BSc, and Diploma students of all semesters.
- No technical interview or coding test required. Instant selection letter issued.

IMPORTANT NOTE:
All selected candidates must pay a mandatory one-time registration and software toolkit fee of $150 (refundable with your first month stipend). This fee covers your seat reservation, study modules, and ISO certified internship certificate.

To apply, send your resume and fee receipt screenshot to: nationalplacement.team@gmail.com"""
    },
    "scam_equipment_check": {
        "title": "❌ Fake Check Cashing & Equipment Scam",
        "platform": "Cold Recruiter Email / Freelance Board",
        "text": """Job Offer: Remote Customer Service Representative - SwiftPay Solutions

Dear Applicant,
We have reviewed your profile and are pleased to offer you the position of Remote Customer Support Clerk. Starting pay is $42.00 per hour with flexible hours.

Equipment Setup:
Because this is a work-from-home position, our financial department will courier you an official company cashier's check of $4,500. You must deposit this check into your personal bank account via mobile deposit.

Once the funds reflect in your account, you will wire the balance via Zelle or Western Union to our certified IT vendor who will ship your home office package (MacBook Pro, dual monitors, headset, and laser printer).

Reply with your full name, mobile number, and home mailing address to swiftpay.careers@yahoo.com to receive your check tracking number."""
    },
    "legit_google_intern": {
        "title": "✅ Real Software Engineering Internship (Google / Enterprise)",
        "platform": "Official Company Careers Page (LinkedIn)",
        "text": """Software Engineering Intern (Summer 2025) - Apex Cloud Technologies
Location: Hybrid (San Jose, CA / Remote options available)

About the Role:
As a Software Engineering Intern on our Infrastructure team, you will write clean, maintainable code in Python and Go, contribute to distributed backend services, and participate in daily agile standups and code reviews.

Key Responsibilities:
- Design and deploy containerized microservices using Docker and Kubernetes.
- Write unit and integration test suites using pytest.
- Collaborate with senior mentors and product managers on architectural designs.

Qualifications:
- Currently enrolled in a BS or MS degree program in Computer Science, Software Engineering, or related STEM field.
- Experience with at least one programming language (Python, Java, C++, or Go).
- Understanding of data structures, algorithms, and relational databases (SQL).

Compensation & Benefits:
- Competitive hourly compensation ($42 - $48 / hour).
- Housing stipend and relocation assistance for eligible students.
- 1-on-1 mentorship and conversion opportunities for full-time graduate roles.

Apply directly through our careers portal or reach out to university recruiting at careers@apexcloud.com."""
    },
    "legit_startup_dev": {
        "title": "✅ Real Startup Frontend Developer Role",
        "platform": "AngelList / Wellfound / LinkedIn",
        "text": """Junior Frontend Web Developer (React / TypeScript) - Starlight Labs
Company: Starlight Software Labs (Series A Developer Tools Startup)
Location: Remote (US & Canada)

We are looking for a junior developer who is passionate about user experience and developer tools. You'll work directly with our engineering founders to build responsive interfaces.

What you'll do:
- Build reusable UI components using React, TypeScript, and modern CSS.
- Connect frontend components to RESTful and GraphQL backend endpoints.
- Participate in weekly sprint planning and async GitHub pull request discussions.

Requirements:
- Portfolio projects or GitHub repositories showing hands-on experience with React and TypeScript.
- Clear understanding of web standards, DOM, and responsive design.
- Ability to communicate clearly in a remote-first team.

Benefits:
- Salary: $70,000 - $80,000 per year + equity options.
- Health, dental, and vision insurance.
- $1,500 annual home office setup and learning budget.

To apply, send your GitHub link and portfolio to hiring@starlightlabs.dev."""
    }
}

@app.route("/")
def index():
    """Main page with large copy-paste box and student preset buttons."""
    return render_template("index.html", samples=STUDENT_SAMPLES)

@app.route("/predict", methods=["POST"])
def predict():
    """Handles raw copy-pasted text from any job board or messaging app."""
    raw_text = request.form.get("raw_text", "").strip()

    # Also handle legacy structured inputs if submitted
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not raw_text and not description:
        return render_template(
            "index.html",
            samples=STUDENT_SAMPLES,
            error="Please paste some job or internship text into the box to analyze."
        )

    # Use raw_text if provided, otherwise assemble structured input
    if raw_text:
        input_text = raw_text
    else:
        company = request.form.get("company", "").strip()
        contact_email = request.form.get("contact_email", "").strip()
        salary = request.form.get("salary", "").strip()
        reqs = request.form.get("requirements", "").strip()
        benefits = request.form.get("benefits", "").strip()
        input_text = f"{title}\nCompany: {company}\nContact: {contact_email}\nSalary: {salary}\n\nDescription:\n{description}\n\nRequirements:\n{reqs}\n\nBenefits:\n{benefits}"

    try:
        result = analyze_raw_job_text(MODELS_DIR, input_text, custom_title=title)
        return render_template("result.html", result=result, raw_text=input_text)
    except Exception as e:
        return render_template(
            "index.html",
            samples=STUDENT_SAMPLES,
            error=f"Prediction error: {str(e)}. Make sure train_model.py has run."
        )

@app.route("/metrics")
def metrics():
    """Shows accuracy, confusion matrix, and model comparison for grading."""
    if not os.path.exists(METRICS_PATH):
        return render_template("metrics.html", metrics_data=None, error="Model metrics not found. Run train_model.py first.")
    
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)

    return render_template("metrics.html", metrics_data=metrics_data)

@app.route("/safety-guide")
def safety_guide():
    """Educational guide for spotting student internship scams."""
    return render_template("safety_guide.html")

@app.route("/api/sample/<sample_id>")
def get_sample(sample_id):
    """Returns sample text for 1-click loading."""
    sample = STUDENT_SAMPLES.get(sample_id)
    if sample:
        return jsonify(sample)
    return jsonify({"error": "Sample not found"}), 404

if __name__ == "__main__":
    print("Starting Student Fake Job Detector on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
