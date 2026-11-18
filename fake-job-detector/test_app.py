"""
Automated Test Suite for Fake Job & Internship Detection System
Verifies raw copy-pasted text analysis, model inference, and web routes.
"""

import os
import unittest
from app import app
from model_utils import analyze_raw_job_text, predict_job_posting

class TestFakeJobDetector(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.models_dir = os.path.join(os.path.dirname(__file__), "models")

    def test_model_files_exist(self):
        """Check that model serialization artifacts exist."""
        self.assertTrue(os.path.exists(os.path.join(self.models_dir, "fake_job_model.pkl")))
        self.assertTrue(os.path.exists(os.path.join(self.models_dir, "tfidf_vectorizer.pkl")))
        self.assertTrue(os.path.exists(os.path.join(self.models_dir, "model_metrics.json")))

    def test_legitimate_prediction_raw_text(self):
        """Verify that genuine engineering internship is flagged as low risk from raw text."""
        raw_text = """Software Engineering Intern (Summer 2025) - Apex Cloud Technologies
We are seeking a computer science intern to write Python and Go microservices under senior engineer mentorship.
Collaborative agile team using Docker, Kubernetes, and PostgreSQL.
Requirements: Pursuing BS in Computer Science. Knowledge of Python and basic data structures.
Benefits: $40/hr stipend, dedicated mentor, hybrid work policy.
Contact university recruiting at careers@apexcloud.com."""

        result = analyze_raw_job_text(self.models_dir, raw_text)
        self.assertEqual(result["verdict_class"], "success")
        self.assertLess(result["risk_percentage"], 35.0)
        self.assertEqual(len(result["heuristic_flags"]), 0)

    def test_scam_prediction_raw_text(self):
        """Verify that raw WhatsApp message with Telegram and fee is flagged as high risk."""
        raw_scam = """URGENT HIRING! Work from home online data entry clerk.
Earn $75 per hour! No interview needed. Guaranteed 100% selection!
Message our hiring coordinator on Telegram @FastRecruiter.
Note: Send small $85 registration fee to hr.fastjobs24@gmail.com for laptop setup."""

        result = analyze_raw_job_text(self.models_dir, raw_scam)
        self.assertEqual(result["verdict_class"], "danger")
        self.assertGreaterEqual(result["risk_percentage"], 65.0)
        self.assertGreater(len(result["heuristic_flags"]), 0)
        # Check that Telegram and @gmail.com were auto-detected
        self.assertTrue(any(f["category"] == "Free Email Used by Recruiter" for f in result["heuristic_flags"]))
        self.assertTrue(any(f["category"] == "Informal / Secret Messaging" for f in result["heuristic_flags"]))

    def test_home_page_route(self):
        """Test GET / returns HTTP 200 with student title."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fake Job & Internship", response.data)
        self.assertIn(b"Paste the Full Job", response.data)

    def test_metrics_page_route(self):
        """Test GET /metrics returns HTTP 200 and loads comparison table."""
        response = self.app.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Machine Learning Model Performance", response.data)
        self.assertIn(b"Logistic Regression", response.data)

    def test_safety_guide_route(self):
        """Test GET /safety-guide returns HTTP 200."""
        response = self.app.get("/safety-guide")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Safety Guide", response.data)

    def test_sample_api_endpoint(self):
        """Test GET /api/sample/scam_whatsapp_typing returns sample JSON."""
        response = self.app.get("/api/sample/scam_whatsapp_typing")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("text", data)
        self.assertIn("Telegram", data["text"])

    def test_predict_raw_post_route(self):
        """Test POST /predict with raw pasted text returns rendered result."""
        payload = {
            "raw_text": "Join our data team as an intern. Analyzing databases with SQL and python. Paid $30/hr. Apply to hr@biohealthanalytics.org."
        }
        response = self.app.post("/predict", data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Calculated Scam Risk", response.data)

if __name__ == "__main__":
    unittest.main()
