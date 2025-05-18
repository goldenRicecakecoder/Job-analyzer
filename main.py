from flask import Flask, render_template, request
from app.analyzer import extract_keywords, extract_experience_phrases, group_keywords

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def analyze():
    keywords = experience_phrases = None
    if request.method == "POST":
        job_desc = request.form.get("job_description", "")
        keywords = extract_keywords(job_desc)
        experience_phrases = extract_experience_phrases(job_desc)
    return render_template("index.html", keywords=keywords, experience_phrases=experience_phrases)

@app.route("/match", methods=["GET", "POST"])
def match():
    match_stats = experience_phrases = None
    if request.method == "POST":
        job_desc = request.form.get("job_description", "")
        resume = request.form.get("resume", "")
        # Analyze both job and resume
        job_keywords = [word for word, _ in extract_keywords(job_desc, limit=100)]
        resume_keywords = [word for word, _ in extract_keywords(resume, limit=100)]
        grouped_job = group_keywords(job_keywords)
        grouped_resume = group_keywords(resume_keywords)
        # Compute match %
        def match_percent(job_list, resume_list):
            matches = [word for word in job_list if word in resume_list]
            percent = int(len(matches) / len(job_list) * 100) if job_list else 0
            missing = [word for word in job_list if word not in resume_list]
            return percent, matches, missing
        match_stats = {
            category: match_percent(grouped_job[category], grouped_resume[category])
            for category in ["TOOLS", "TECH", "SOFT_SKILLS"]
        }
        experience_phrases = extract_experience_phrases(job_desc)
    return render_template("match.html", match_stats=match_stats, experience_phrases=experience_phrases)

    match_stats = experience_phrases = None
    if request.method == "POST":
        job_desc = request.form.get("job_description", "")
        resume = request.form.get("resume", "")
        # Analyze both job and resume
        job_keywords = [word for word, _ in extract_keywords(job_desc, limit=100)]
        resume_keywords = [word for word, _ in extract_keywords(resume, limit=100)]
        grouped_job = group_keywords(job_keywords)
        grouped_resume = group_keywords(resume_keywords)
        # Compute match %
        def match_percent(job_list, resume_list):
            matches = [word for word in job_list if word in resume_list]
            percent = int(len(matches) / len(job_list) * 100) if job_list else 0
            missing = [word for word in job_list if word not in resume_list]
            return percent, matches, missing
        match_stats = {
            category: match_percent(grouped_job[category], grouped_resume[category])
            for category in ["TOOLS", "TECH", "SOFT_SKILLS"]
        }
        experience_phrases = extract_experience_phrases(job_desc)
    return render_template("match.html", match_stats=match_stats, experience_phrases=experience_phrases)

if __name__ == "__main__":
    app.run(debug=True)
