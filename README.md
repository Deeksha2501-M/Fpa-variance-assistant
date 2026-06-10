# 📊 AI-Powered FP&A Variance Assistant

An AI-powered financial planning and analysis tool that automates variance commentary — one of the most time-consuming tasks in corporate finance.

## What it does
- Upload any budget vs actual CSV file
- Automatically calculates variances by department
- Generates an interactive bar chart
- Uses AI (Groq + Llama 3) to write executive-ready variance commentary in seconds

## Built with
- Python
- Streamlit
- Pandas
- Plotly
- Groq API (Llama 3.3)

## How to run locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Groq API key to `.env` as `GROQ_API_KEY=your_key`
4. Run: `streamlit run app.py`

## Live Demo
(https://fpa-variance-assistant-e2aplqytfskkmfuydhuy6a.streamlit.app)
