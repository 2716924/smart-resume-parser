# Smart Resume Parser + Ranker

A full-stack web application that allows users to:

* **Upload and parse resumes** (PDF) to extract text
* **Extract key features** such as skills and years of experience using NLP
* **Upload a Job Description (JD)** (text or PDF) to extract required skills and experience
* **Match and rank** one or multiple resumes against the JD
* **Display results** in a leaderboard with detailed feedback

---

## 🚀 Features

1. **Resume Parsing**

   * PDF text extraction using **PyMuPDF**
   * Preview extracted text

2. **NLP Extraction**

   * Entity extraction of **skills** and **years of experience**
   * Configurable skill list in `resume_nlp.py`

3. **Job Description Processing**

   * Accept JD as raw text or PDF
   * Extract required skills and experience

4. **Matching & Scoring**

   * Skill-match percentage (70% weight)
   * Experience compliance score (30% weight)
   * Combined **total score** (0–100)
   * Feedback: matching skills, missing skills, experience gap

5. **Frontend Interface**

   * Simple HTML/JS upload page (`index.html`)
   * Full leaderboard UI (`leaderboard.html`) to upload JD and multiple resumes
   * Dynamic results table display

6. **Extensibility**

   * Skill list and scoring weights configurable
   * Easily extendable to use DB storage (SQLite/MongoDB)
   * Placeholder for LLM or fuzzy matching enhancements

---

## 🛠️ Tech Stack

* **Backend**: Python 3.8+, Flask
* **PDF Parsing**: PyMuPDF (`fitz`)
* **NLP**: spaCy (`en_core_web_sm`)
* **Frontend**: HTML, JavaScript (Fetch API)
* **Storage**: Local file uploads in `uploads/`

---

## 📥 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/2716924/smart-resume-parser.git
   cd smart-resume-parser
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   venv\Scripts\activate        # Windows

   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run the Flask server**

   ```bash
   python app.py
   ```

4. **Access the app**

   * **Resume Ranker:**    [http://127.0.0.1:5000/leaderboard](http://127.0.0.1:5000/leaderboard)


## 🧩 Project Structure

```
smart-resume-parser/
├── app.py
├── resume_nlp.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── leaderboard.html
└── static/
    └── styles.css        
```

---

## 🔧 Configuration

* **UPLOAD\_FOLDER** in `app.py`: location where PDF files are saved
* **ALLOWED\_EXTENSIONS**: restrict file types (default `{'pdf'}`)
* **COMMON\_SKILLS** in `resume_nlp.py`: extend or modify this set with domain-specific skills
* **Scoring weights**: adjust in `/match_resume` (defaults: 70% skills, 30% experience)

---

## 🚀 Usage Workflow

1. **Start server**
2. Navigate to **Leaderboard** page
3. **Upload** the Job Description (paste text or upload PDF)
4. **Upload** one or more resume PDFs
5. View the **ranked results** and feedback table

---

## 📈 Future Improvements

* **Database integration:** Store JD and resume records in a database
* **Fuzzy matching:** Use Levenshtein or embeddings for skill variations
* **LLM enhancements:** Summarize resumes, suggest missing qualifications
* **User authentication:** Multi-user support and dashboards
* **Styling:** Use Tailwind CSS or Bootstrap for a polished UI


## 📄 License

MIT © Matimu
