# Job Analyzer

This is a simple Python web app that extracts key skills and terms from a job description.

## What it does

- You paste in a job description
- It finds the top 10 keywords (like “Python”, “SQL”, “developer”)
- Built using Flask and spaCy

## How to run it

1. Install Python 3.10
2. Run:

pip install -r requirements.txt

markdown
Copy
Edit

3. Start the app:

python main.py

markdown
Copy
Edit

4. Go to `http://localhost:5000` in your browser

## Project files

- `app/analyzer.py` – the text analysis code
- `main.py` – the web app
- `templates/index.html` – the form and display