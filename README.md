# LegacyATS

LegacyATS is a resume compatibility checker built to help students understand why resumes get rejected by Applicant Tracking Systems (ATS).

During placements and job applications, students often spend time improving projects, formatting resumes, and applying to multiple roles but still receive no response. One reason is that many resumes are filtered automatically before reaching a recruiter.

Most people are not aware that resume formatting, document structure, and keyword placement can affect how these systems process resumes.

There are already many ATS checking platforms available online, but detailed analysis is usually paid. This project was built to provide a free alternative where users can check resume compatibility and optionally use their own Gemini API key to generate improvement suggestions.

LegacyATS analyzes uploaded resumes, compares them against a target job description, identifies missing keywords, estimates compatibility, and generates recommendations to improve ATS readability.

---

## Features

* Resume upload and analysis (PDF)
* Resume and job description comparison
* Compatibility score generation
* Keyword matching and missing keyword detection
* ATS-style parsing simulation
* AI-generated improvement suggestions using Gemini
* Recruiter demo mode
* Rate-limited backend APIs
* Parser validation tests

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI
* Python

### AI

* Google Gemini API

### Parsing

* pdfplumber

### Testing

* Pytest

---

## Project Structure

```text
LEGACYATS
│
├── backend/
│   ├── main.py
│   ├── legacy_parser.py
│   └── gemini_evaluator.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   └── test_main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Local Setup

Clone the repository:

```bash
git clone https://github.com/Mohammed-Zain-py/LegacyATS.git
cd LEGACYATS
```

Create and activate virtual environment:

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

---

## Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend:

```text
http://localhost:8501
```

---

## Testing

```bash
pytest
```

---

## Notes

* This project is intended for educational and portfolio purposes.
* Compatibility scores should not be treated as actual recruiter decisions.
* AI-based resume improvements require a user-provided Gemini API key.
* The parser intentionally reproduces limitations commonly associated with older ATS workflows.

---

## License

This project is publicly available for learning, personal use, testing, and direct usage through the deployed application.

Please do not republish, redistribute, or present this project as your own work.

See the LICENSE file for full terms.
