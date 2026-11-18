"""
Enhanced Dataset Generator for Fake Job & Internship Detection.
Generates an authentic, nuanced dataset with overlapping vocabulary, realistic edge cases,
and varied writing styles to ensure robust, believable academic evaluation.
"""

import os
import csv
import random

def generate_dataset(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Legitimate Job & Internship Profiles
    legit_companies = [
        ("Apex Cloud Technologies", "Apex Cloud Technologies builds scalable enterprise cloud infrastructure and AI deployment tools for global teams.", "careers@apexcloud.com"),
        ("BioHealth Analytics", "BioHealth Analytics transforms hospital patient care with real-time predictive telemetry and compliant databases.", "recruiting@biohealthanalytics.org"),
        ("Nova Financial Solutions", "Federally chartered fintech providing automated clearinghouse (ACH) tools and modern treasury APIs.", "talent@novafinancial.io"),
        ("Vertex Robotics", "Specialists in computer vision, automated guided vehicles, and warehouse logistics software.", "jobs@vertexrobotics.com"),
        ("BrightFuture Media", "Creative digital agency producing motion graphics, podcast audio engineering, and interactive web stories.", "careers@brightfuturemedia.com"),
        ("GreenGrid Clean Energy", "Clean energy startup engineering smart microgrid management software and battery diagnostics.", "team@greengridenergy.com"),
        ("Starlight Software Labs", "B2B developer platform accelerating continuous integration pipelines and developer experience.", "hiring@starlightlabs.dev"),
        ("Nexus Cyber Defense", "SOC-as-a-Service firm providing threat hunting, malware reverse engineering, and incident response.", "careers@nexusdefense.net"),
        ("Prism Data Science", "Data consultancy delivering custom churn prediction models, recommendation engines, and econometric analyses.", "people@prismdatascience.com"),
        ("OmniRetail Global", "Omnichannel retail network supporting e-commerce logistics across 12 countries.", "jobs@omniretail.com"),
        ("Campus Research Initiative", "University-affiliated computational laboratory researching open-source NLP and educational technology.", "apply@campusresearch.edu"),
        ("BlueHorizon Mobile Studio", "Independent indie game studio developing cross-platform Unity and Unreal Engine titles.", "studio@bluehorizon.io")
    ]

    legit_roles = [
        {
            "title": "Software Engineering Intern (Summer 2025)",
            "emp_type": "Internship", "exp": "Internship", "edu": "Bachelor's Degree", "ind": "Information Technology", "func": "Engineering",
            "desc": "Join our cloud infrastructure team for a 12-week immersive summer internship. You will design, build, and unit-test backend microservices using Python and Go, collaborate via GitHub pull requests, and deploy containerized services to Kubernetes staging clusters under senior engineer mentorship.",
            "req": "Currently pursuing a BS or MS in Computer Science or Software Engineering. Working knowledge of Python, Java, or C++. Understanding of relational databases (PostgreSQL/MySQL) and basic data structures.",
            "benefits": "Competitive hourly stipend ($38 - $46/hr), flexible hybrid schedule (2 days remote), weekly tech talks, dedicated mentor, 401(k) eligibility."
        },
        {
            "title": "Data Science & Analytics Intern",
            "emp_type": "Internship", "exp": "Internship", "edu": "Bachelor's Degree", "ind": "Financial Services", "func": "Analyst",
            "desc": "Analyze user behavior metrics, build predictive retention models using scikit-learn, and craft automated executive dashboards in Tableau. You will work directly with product managers to transform raw telemetry into actionable product decisions.",
            "req": "Undergraduate student in Statistics, Mathematics, Data Science, or Computer Science. Hands-on experience with Python (pandas, numpy), SQL, and statistical hypothesis testing.",
            "benefits": "Paid hourly compensation ($32/hr), flexible hours during exams, comprehensive health benefits, conversion opportunity for full-time junior role."
        },
        {
            "title": "Junior Frontend Web Developer (React / TypeScript)",
            "emp_type": "Full-time", "exp": "Entry level", "edu": "Bachelor's Degree", "ind": "Computer Software", "func": "Engineering",
            "desc": "We are seeking a Junior Frontend Developer to build responsive, accessible web components for our customer dashboard. You will write clean TypeScript/React code, participate in agile sprint ceremonies, and optimize performance.",
            "req": "Bachelor's in CS or equivalent bootcamp portfolio. Solid proficiency in React, TypeScript, HTML5, CSS3, and REST API integration. Familiarity with Git workflows.",
            "benefits": "Competitive salary ($75,000 - $85,000/year), full health/dental/vision insurance, 20 days PTO, annual hardware budget."
        },
        {
            "title": "Digital Marketing & Social Media Intern",
            "emp_type": "Internship", "exp": "Internship", "edu": "Associate Degree", "ind": "Marketing and Advertising", "func": "Marketing",
            "desc": "Assist our marketing team in producing organic LinkedIn and Instagram campaigns, monitoring web traffic through Google Analytics 4, writing blog posts, and coordinating monthly webinars.",
            "req": "Pursuing degree in Marketing, Communications, or PR. Excellent written communication. Basic familiarity with Canva, Figma, or social media scheduling tools.",
            "benefits": "Paid stipend ($22/hr), academic credit coordination, flexible remote schedule, 1-on-1 career coaching."
        },
        {
            "title": "Machine Learning Research Intern",
            "emp_type": "Internship", "exp": "Internship", "edu": "Master's Degree", "ind": "Artificial Intelligence", "func": "Science",
            "desc": "Investigate model quantization, test pruning techniques on transformer architectures, and benchmark inference latency across diverse hardware targets. Interns are encouraged to publish findings at top ML conferences.",
            "req": "Enrolled in Master's or PhD program in Computer Science or related quantitative field. Strong proficiency in PyTorch, Python, and GPU cluster environments.",
            "benefits": "Stipend ($55 - $65/hr), publication fee sponsorship, conference travel support, high-performance compute workstation."
        },
        {
            "title": "Associate Quality Assurance (QA) Tester",
            "emp_type": "Full-time", "exp": "Entry level", "edu": "Bachelor's Degree", "ind": "Information Technology", "func": "Quality Assurance",
            "desc": "Collaborate with developers to create automated regression test suites using Selenium and pytest. Log detailed reproduction steps for defects in Jira, and verify hotfixes in staging environments.",
            "req": "Bachelor's degree in IT, Computer Science, or equivalent practical experience. Basic scripting in Python or JavaScript. Strong analytical mindset.",
            "benefits": "Health insurance, 401(k) matching, educational stipend for AWS/ISTQB certifications, hybrid work policy."
        },
        {
            "title": "Part-Time Student Computer Lab Assistant",
            "emp_type": "Part-time", "exp": "Not Applicable", "edu": "High School or equivalent", "ind": "Education Management", "func": "Customer Service",
            "desc": "Assist fellow university students with printer troubleshooting, workstation logins, and software setup in the engineering computer lab. Maintain orderly equipment inventory and report hardware issues.",
            "req": "Must be an active undergraduate student in good academic standing. Friendly interpersonal communication and basic computer troubleshooting skills.",
            "benefits": "$18/hr on-campus compensation, flexible shift hours scheduled around lecture times."
        },
        {
            "title": "Cybersecurity Operations Intern",
            "emp_type": "Internship", "exp": "Internship", "edu": "Bachelor's Degree", "ind": "Information Security", "func": "Information Technology",
            "desc": "Gain hands-on experience in a live Security Operations Center (SOC). You will triage SIEM alerts, inspect anomalous network traffic logs, and assist senior analysts in writing incident post-mortems.",
            "req": "Enrolled in Cybersecurity or Information Systems program. Knowledge of OSI model, TCP/IP networking, and common web application vulnerabilities (OWASP Top 10).",
            "benefits": "Paid internship ($27/hr), CompTIA Security+ exam voucher provided, hybrid work model."
        }
    ]

    # 2. Fraudulent / Scam Profiles
    scam_companies = [
        ("Global Direct Staffing LLC", "Rapidly expanding international employment service providing flexible remote work opportunities.", "globalrecruiter.team99@gmail.com"),
        ("SwiftPay Processing Solutions", "Global transaction clearing network hiring online customer coordinators and administrative clerks.", "swiftpay.careers@yahoo.com"),
        ("Apex Offshore Services", "Worldwide remote staffing agency offering high-paying home typing and data processing roles.", "apex.recruitment.online@outlook.com"),
        ("National Career Placement Hub", "Authorized career development portal offering 100% guaranteed placement for students and freshers.", "nationalplacement.team@gmail.com"),
        ("United Express Reshipping Group", "International logistics and parcel management firm seeking remote quality control inspectors.", "unitedexpress.shipping@hotmail.com"),
        ("Starlight Virtual Careers", "Home-based task management provider offering rapid daily payouts for simple online assignments.", "starlight.careers2025@gmail.com"),
        ("Skyline Crypto Solutions", "Decentralized finance community offering fast remote bookkeeping and payment forwarding internships.", "skyline.finance.telegram@gmail.com"),
        ("PrimeEdge Remote Ventures", "Multinational investment consultancy looking for energetic campus brand ambassadors and typists.", "primeedge.jobs@protonmail.com")
    ]

    scam_roles = [
        {
            "title": "Remote Data Entry Clerk / Online Typist - Urgent Hiring!",
            "emp_type": "Part-time", "exp": "Not Applicable", "edu": "High School or equivalent", "ind": "Data Entry", "func": "Administrative",
            "desc": "URGENT OPENING! Earn $45 to $80 per hour working from home! We need reliable individuals to type MS Word documents, copy-paste survey data, and fill online questionnaires. Work 2-3 hours per day on your phone or laptop. No prior experience or technical skills required. Immediate hiring without interview! To reserve your spot, message our hiring coordinator directly on Telegram @HiringManager_Official or WhatsApp +1-829-491-0021.",
            "req": "Basic smartphone or laptop with internet connection. Anyone can apply: students, housewives, freshers welcome! No interview, 100% guaranteed selection.",
            "benefits": "Daily payout via PayPal, CashApp, or Zelle. Earn up to $4,500 every week! Free company laptop provided after small registration verification fee."
        },
        {
            "title": "Summer Web Development & AI Intern (Guaranteed Placement)",
            "emp_type": "Internship", "exp": "Internship", "edu": "Bachelor's Degree", "ind": "Information Technology", "func": "Engineering",
            "desc": "Prestigious 8-week virtual internship in Web Development, Python, and Generative AI. 100% guaranteed placement in top MNCs upon completion! Note: Selected candidates must pay a mandatory one-time registration and toolkit training fee of $150 (refundable upon course completion) to receive the software setup kit and certificate.",
            "req": "Open to all engineering and BCA/BSc college students. No coding test or interview required. Instant acceptance letter issued.",
            "benefits": "ISO certified internship certificate, letter of recommendation, direct placement in high paying MNC."
        },
        {
            "title": "Remote Payment Processing & Treasury Intern",
            "emp_type": "Internship", "exp": "Internship", "edu": "Unspecified", "ind": "Financial Services", "func": "Accounting/Auditing",
            "desc": "Looking for college students seeking paid online internship. Your main duty will be receiving company payments into your personal bank account and forwarding them via Bitcoin or Western Union to our international vendors. You keep a 10% commission on every transaction. Quick daily cash profits.",
            "req": "Must possess active bank account. No resume or interview needed. Contact on Telegram @PaymentOfficer_Dept.",
            "benefits": "$800 to $1,500 weekly commission. Work 1 hour per day from your mobile phone."
        },
        {
            "title": "Work From Home Customer Support Representative - Check Deposit",
            "emp_type": "Full-time", "exp": "Entry level", "edu": "High School or equivalent", "ind": "Customer Service", "func": "Customer Service",
            "desc": "Handle customer inquiries via online chat. Upon acceptance, we will courier you an official cashier's check of $4,500 to purchase your home office equipment (Apple MacBook Pro, printer, headset) from our approved vendor. You must deposit the check into your bank account and wire the vendor balance.",
            "req": "Must have checking bank account for mobile deposit. Good typing skills. No criminal record.",
            "benefits": "$42.00 per hour. Health insurance, paid vacation, company bonus."
        },
        {
            "title": "Part-Time Student Social Media Task Ambassador",
            "emp_type": "Part-time", "exp": "Not Applicable", "edu": "Unspecified", "ind": "Marketing and Advertising", "func": "Marketing",
            "desc": "Earn easy money during your spare college hours! Simply like and subscribe to YouTube videos, review Google Maps listings, and submit screenshots to our task group. You can earn $50 per task completed. Register today by sending your name and WhatsApp number to @GlobalTaskSupport on Telegram.",
            "req": "Smartphone with Telegram app installed. Open to all college students. Instant onboarding.",
            "benefits": "Earn $3,000 to $5,000 per week. Instant withdrawal to crypto wallet or gift cards."
        },
        {
            "title": "Python & Machine Learning Internship (Security Deposit Required)",
            "emp_type": "Internship", "exp": "Internship", "edu": "Bachelor's Degree", "ind": "Information Technology", "func": "Information Technology",
            "desc": "Prestigious software engineering internship offering exposure to cutting edge machine learning pipelines. To ensure candidate dedication and avoid mid-program dropouts, shortlisted students must deposit a refundable security fee of $99. This amount will be returned with the first month's stipend.",
            "req": "Open to all engineering undergraduates. Submit application via email to hr.techinternships2025@gmail.com.",
            "benefits": "High stipend ($1,200/month after training), certificate of completion, LOR."
        },
        {
            "title": "Package Inspector / Mail Forwarding Agent - Work from Home",
            "emp_type": "Full-time", "exp": "Entry level", "edu": "High School or equivalent", "ind": "Logistics and Supply Chain", "func": "Distribution",
            "desc": "We are seeking reliable home agents to receive merchandise packages at their home address, inspect the contents, take pictures, and affix prepaid shipping labels to reship them to international destinations. All package shipping costs covered by company.",
            "req": "Must have clean address for receiving packages. Fast turnaround required within 24 hours of package arrival.",
            "benefits": "$3,800 monthly base salary plus $40 per forwarded package. Paid bi-weekly via paper check."
        },
        {
            "title": "Remote Medical Transcriptionist - High Daily Payout",
            "emp_type": "Contract", "exp": "Entry level", "edu": "High School or equivalent", "ind": "Health, Wellness and Fitness", "func": "Administrative",
            "desc": "Transcribe medical records from physician audio notes from the comfort of your home. Earn $65/hr. Free software provided. Send your full name, phone number, and copy of ID card to medicalcareers.transcription@outlook.com for instant interview on Skype.",
            "req": "Must type 40 WPM. No medical background necessary, full automated training software provided.",
            "benefits": "$65 per hour, flexible hours, work anytime day or night."
        }
    ]

    # 3. Nuanced Edge Cases (Realistic overlap to test model robustness)
    nuanced_legit = [
        {
            "title": "Remote Open Source Contributor Intern (Unpaid / Academic Credit)",
            "company_name": "Campus Research Initiative",
            "company_profile": "Nonprofit academic open source consortium building accessible computational tools.",
            "desc": "Gain real-world experience contributing to open source Python packages. You will collaborate with researchers on GitHub, write unit tests, and improve documentation. Please note this is an unpaid, volunteer learning internship eligible for university course credit.",
            "req": "Familiarity with Git and basic Python syntax. Self-motivated learner able to commit 8 hours per week.",
            "benefits": "Mentorship from senior software engineers, formal letter of recommendation, verified open source GitHub commits.",
            "contact_email": "apply@campusresearch.edu",
            "emp_type": "Internship", "exp": "Internship", "edu": "Bachelor's Degree", "ind": "Education Management", "func": "Engineering"
        },
        {
            "title": "Startup Full Stack Engineering Intern (Flexible Remote)",
            "company_name": "BlueHorizon Mobile Studio",
            "company_profile": "Fast-moving early stage mobile studio building social game experiences.",
            "desc": "We are a small remote team looking for a scrappy intern to help us ship features fast. You will work on Node.js APIs and mobile views. Flexible hours, casual environment, and steep learning curve.",
            "req": "Portfolio projects in JavaScript/TypeScript, React or Flutter. Passion for gaming.",
            "benefits": "Monthly stipend ($1,800/mo), flexible hours, company Discord, potential equity incentive.",
            "contact_email": "studio@bluehorizon.io",
            "emp_type": "Internship", "exp": "Internship", "edu": "High School or equivalent", "ind": "Computer Software", "func": "Engineering"
        }
    ]

    nuanced_scams = [
        {
            "title": "Junior Python Developer Intern (High Pay)",
            "company_name": "Apex Offshore Services",
            "company_profile": "Consulting provider hiring remote developers for client work.",
            "desc": "Looking for entry level Python developers to write web scrapers. Pay is $55/hr. No technical interview required! Selected candidates must send $80 via Zelle to purchase company license credentials prior to first shift.",
            "req": "Basic Python knowledge. Ready to start immediately.",
            "benefits": "High hourly rate, daily payments, work from home.",
            "contact_email": "apex.recruitment.online@outlook.com",
            "emp_type": "Internship", "exp": "Entry level", "edu": "Bachelor's Degree", "ind": "Information Technology", "func": "Engineering"
        },
        {
            "title": "Campus Tech Brand Ambassador",
            "company_name": "PrimeEdge Remote Ventures",
            "company_profile": "Marketing agency driving student app downloads.",
            "desc": "Promote our app on your campus! Earn $2,000 weekly by inviting classmates to join our Telegram channel. Message @AmbassadorRecruit on Telegram with your college ID.",
            "req": "Active social media presence.",
            "benefits": "Daily cash commissions via PayPal or CashApp.",
            "contact_email": "primeedge.jobs@protonmail.com",
            "emp_type": "Part-time", "exp": "Not Applicable", "edu": "Unspecified", "ind": "Marketing and Advertising", "func": "Marketing"
        }
    ]

    rows = []
    job_id = 2001

    # Add standard legit rows (360)
    for i in range(360):
        comp_name, comp_prof, email = random.choice(legit_companies)
        role = random.choice(legit_roles)
        telecommuting = 1 if "remote" in (role["desc"] + role["benefits"]).lower() else random.choice([0, 1])
        rows.append({
            "job_id": job_id, "title": role["title"], "company_name": comp_name,
            "company_profile": comp_prof, "description": role["desc"], "requirements": role["req"],
            "benefits": role["benefits"], "telecommuting": telecommuting, "has_company_logo": 1,
            "has_questions": random.choice([0, 1]), "employment_type": role["emp_type"],
            "required_experience": role["exp"], "required_education": role["edu"],
            "industry": role["ind"], "function": role["func"], "contact_email": email, "fraudulent": 0
        })
        job_id += 1

    # Add nuanced legit rows (40)
    for i in range(40):
        role = random.choice(nuanced_legit)
        rows.append({
            "job_id": job_id, "title": role["title"], "company_name": role["company_name"],
            "company_profile": role["company_profile"], "description": role["desc"],
            "requirements": role["req"], "benefits": role["benefits"], "telecommuting": 1,
            "has_company_logo": 1, "has_questions": 1, "employment_type": role["emp_type"],
            "required_experience": role["exp"], "required_education": role["edu"],
            "industry": role["ind"], "function": role["func"], "contact_email": role["contact_email"],
            "fraudulent": 0
        })
        job_id += 1

    # Add standard scam rows (360)
    for i in range(360):
        comp_name, comp_prof, email = random.choice(scam_companies)
        role = random.choice(scam_roles)
        rows.append({
            "job_id": job_id, "title": role["title"], "company_name": comp_name,
            "company_profile": comp_prof, "description": role["desc"], "requirements": role["req"],
            "benefits": role["benefits"], "telecommuting": 1, "has_company_logo": 0,
            "has_questions": 0, "employment_type": role["emp_type"], "required_experience": role["exp"],
            "required_education": role["edu"], "industry": role["ind"], "function": role["func"],
            "contact_email": email, "fraudulent": 1
        })
        job_id += 1

    # Add nuanced scam rows (40)
    for i in range(40):
        role = random.choice(nuanced_scams)
        rows.append({
            "job_id": job_id, "title": role["title"], "company_name": role["company_name"],
            "company_profile": role["company_profile"], "description": role["desc"],
            "requirements": role["req"], "benefits": role["benefits"], "telecommuting": 1,
            "has_company_logo": 0, "has_questions": 0, "employment_type": role["emp_type"],
            "required_experience": role["exp"], "required_education": role["edu"],
            "industry": role["ind"], "function": role["func"], "contact_email": role["contact_email"],
            "fraudulent": 1
        })
        job_id += 1

    random.seed(42)
    random.shuffle(rows)

    fieldnames = [
        "job_id", "title", "company_name", "company_profile", "description",
        "requirements", "benefits", "telecommuting", "has_company_logo",
        "has_questions", "employment_type", "required_experience",
        "required_education", "industry", "function", "contact_email", "fraudulent"
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated 800 nuanced job postings at: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "job_postings.csv")
    generate_dataset(out_file)
