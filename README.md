# AI Resume Analyzer

A Flask web application that compares a candidate's resume with a job description and reports matched, missing, and extra skills along with an estimated match percentage.

## Features

- Upload resumes in **PDF, DOCX, or TXT** format.
- Paste a job description and analyze the two texts.
- Extract education, work experience, and limited contact information from labeled resume sections.
- Detect skills using a curated keyword list and simple text matching.
- View detected, matched, missing, and additional resume skills, plus a percentage score.
- Runs locally without an external API or API key.

## Tech stack

- **Backend:** Python, Flask
- **Frontend:** HTML with inline CSS and Jinja templates
- **Text extraction:** PyPDF2, python-docx
- **Skill analysis:** Python regular expressions and curated skill vocabulary

## Getting started

1. Install Python 3.10+ and clone this repository.
2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate it:

   **Windows (PowerShell):** `venv\Scripts\Activate.ps1`

   **macOS/Linux:** `source venv/bin/activate`

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Open **http://127.0.0.1:5000/**, upload a resume, paste a job description, and select **Analyze**.

## Project structure

```text
AI_Resume_Analyzer/
├── app.py                    # Flask routes, upload handling, result rendering
├── requirements.txt          # Python dependencies
├── templates/
│   ├── index.html            # Upload form
│   └── result.html           # Analysis results
└── utils/
    ├── __init__.py
    ├── analyze_resume.py     # Skills extraction and matching
    ├── extract_text.py       # PDF/DOCX/TXT extraction
    ├── filters.py            # Stopword and role filters
    └── rmp.py                # Skill vocabulary
```

The `uploads/` directory is created when you run the app and is deliberately excluded from version control. The original ZIP also contained a local `venv/` folder and Python cache files; these are not part of the source repository.

## How the matching score works

The application extracts the resume's **Skills** section, identifies keywords from both the resume and job description, compares them, and calculates:

`(number of matched skills / number of detected job-description skills) × 100`

The score is **heuristic**: it is not an official ATS score, trained AI-model output, or guarantee of recruitment success.

## Limitations and privacy

- Extraction relies on recognizable resume section headings; other formats may give incomplete results.
- Image-only/scanned PDFs may not contain extractable text.
- Uploaded resumes are saved locally in `uploads/` and are **not automatically deleted**. Avoid storing sensitive resumes and do not commit this directory.
- The current application uses Flask's development server with debug enabled. It needs secure filename handling, upload validation/limits, retention controls, and production configuration **before public deployment**.

## License

No license has been specified. All rights remain with the repository owner unless a license is added.
