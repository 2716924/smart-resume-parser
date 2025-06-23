# app.py

from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF
import os
from werkzeug.utils import secure_filename
from resume_nlp import extract_resume_features

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jd_features = {}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper: Allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Home page for simple preview
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Leaderboard page for JD upload & resume ranking
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return render_template("leaderboard.html")

# Upload Job Description (text or PDF)
@app.route("/upload_jd", methods=["POST"])
def upload_jd():
    jd_text = ""

    if 'jd_text' in request.form and request.form['jd_text'].strip():
        jd_text = request.form['jd_text']
    elif 'jd_file' in request.files:
        jd_file = request.files['jd_file']
        if jd_file and allowed_file(jd_file.filename):
            filename = secure_filename(jd_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            jd_file.save(filepath)
            jd_text = extract_text_from_pdf(filepath)
        else:
            return jsonify({"error": "Invalid JD file"}), 400
    else:
        return jsonify({"error": "No JD input provided"}), 400

    # Extract features
    global jd_features
    jd_features = extract_resume_features(jd_text)

    return jsonify({
        "jd_skills": jd_features.get("skills", []),
        "jd_experience_required": jd_features.get("experience_years", 0)
    })

# Match a single resume against stored JD
@app.route("/match_resume", methods=["POST"])
def match_resume():
    global jd_features

    if not jd_features:
        return jsonify({"error": "No Job Description uploaded yet"}), 400

    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files['resume']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        extracted_text = extract_text_from_pdf(filepath)
        resume_features = extract_resume_features(extracted_text)

        # Scoring logic
        jd_skills = set(jd_features.get("skills", []))
        resume_skills = set(resume_features.get("skills", []))
        matching_skills = jd_skills.intersection(resume_skills)

        skill_score = (len(matching_skills) / len(jd_skills)) if jd_skills else 0

        jd_exp = jd_features.get("experience_years", 0) or 0
        resume_exp = resume_features.get("experience_years", 0) or 0
        experience_score = 1.0 if resume_exp >= jd_exp else (resume_exp / jd_exp if jd_exp else 0)

        total_score = round((skill_score * 0.7 + experience_score * 0.3) * 100, 2)

        return jsonify({
            "filename": filename,
            "total_score": total_score,
            "matching_skills": list(matching_skills),
            "missing_skills": list(jd_skills - resume_skills),
            "resume_experience": resume_exp,
            "jd_experience_required": jd_exp
        })

    return jsonify({"error": "Unsupported file type or no file"}), 400

# Simple resume parse preview endpoint
@app.route("/upload", methods=["POST"])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        extracted_text = extract_text_from_pdf(filepath)
        features = extract_resume_features(extracted_text)

        return jsonify({
            "filename": filename,
            "extracted_text": extracted_text[:2000],
            "skills": features.get("skills", []),
            "experience_years": features.get("experience_years", None)
        })

    return jsonify({"error": "Unsupported file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
