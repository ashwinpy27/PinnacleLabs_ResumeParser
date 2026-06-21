# AI Resume Parser

An AI-powered resume parsing tool built for the Pinnacle Labs internship program. Upload a resume (PDF) and automatically extract structured information: name, email, phone, skills, and education.

## Features
- Upload any PDF resume and get instant structured extraction
- Uses spaCy NLP (Named Entity Recognition) to detect candidate names
- Regex-based extraction for email addresses and phone numbers
- Section-aware parsing for Skills and Education using rule-based text segmentation
- Built and validated on the [Resume Dataset (Kaggle)](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset) — 2,484 resumes across 24 job categories
- Interactive Streamlit web app

## Tech Stack
- Python
- spaCy (NLP / Named Entity Recognition)
- pdfplumber (PDF text extraction)
- pandas (data handling and EDA)
- Streamlit (web app)

## Dataset Insights (from EDA)
- IT resumes listed the most skills on average (~44 per resume)
- Most common skills across all resumes: Excel, client communication, sales, quality, meetings
- Education and Skills sections are reliably structured; contact info varies by resume source

## How to Run
1. Clone this repository
2. Install dependencies:
