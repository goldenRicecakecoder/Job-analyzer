from flask import Flask, render_template, request 
from app.analyzer import extract_keywords

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    keywords = []
    if request.method == "POST":
        job_desc = request.form["job_description"]
        keywords = extract_keywords(job_desc)
    return render_template("index.html", keywords=keywords)

if __name__ == "__main__":
    app.run(debug=True)
