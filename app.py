from flask import Flask, render_template, request
import os, re
from utils.extract_text import extract_text_from_file
from utils.analyze_resume import compare_skills

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        jd_text = request.form.get("job_description", "")

        if resume_file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filepath)
            resume_text = extract_text_from_file(filepath)

            personal_info, education_text, experience_text = {}, "", ""
            lines = resume_text.splitlines()
            capture_section = None

            for line in lines:
                line_clean = line.strip().lower()
                if line_clean.startswith("personal information"):
                    capture_section = "personal_info"
                    continue
                elif line_clean.startswith("education"):
                    capture_section = "education"
                    continue
                elif line_clean.startswith("experience"):
                    capture_section = "experience"
                    continue
                elif any(line_clean.startswith(h) for h in ["projects","certifications","languages","skills"]):
                    capture_section = None

                if capture_section == "personal_info":
                    if "linkedin" in line.lower():
                        personal_info["LinkedIn"] = line.strip()
                    if re.search(r"\b\d{10}\b", line):
                        personal_info["Phone"] = re.search(r"\b\d{10}\b", line).group()
                elif capture_section == "education":
                    education_text += line + "\n"
                elif capture_section == "experience":
                    experience_text += line + "\n"

            skills_result = compare_skills(resume_text, jd_text)

            return render_template("result.html",
                                   personal_info=personal_info,
                                   education=education_text.strip(),
                                   experience=experience_text.strip(),
                                   skills=skills_result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
