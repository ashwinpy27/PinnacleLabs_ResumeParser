import spacy
import re
import pdfplumber
import streamlit as st

nlp = spacy.load("en_core_web_sm")

SECTION_HEADERS = ["Summary", "Highlights", "Accomplishments", "Experience",
                    "Education", "Skills", "Objective", "Certifications", "Interests"]

DEGREE_KEYWORDS = ["High School Diploma", "Associate", "Bachelor", "B.S.", "B.A.", "B.Tech",
                    "Master", "M.S.", "M.A.", "M.Tech", "MBA", "Ph.D.", "Doctorate",
                    "Diploma", "Certificate"]

INSTITUTION_KEYWORDS = ["University", "College", "Institute", "School", "Academy"]

def split_into_sections(text):
    pattern = r'\b(' + '|'.join(SECTION_HEADERS) + r')\b'
    matches = list(re.finditer(pattern, text))
    sections = {}
    for i, match in enumerate(matches):
        header = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[header] = text[start:end].strip()
    return sections

def extract_skills(text):
    sections = split_into_sections(text)
    skills_text = sections.get("Skills", "")
    if not skills_text:
        return []
    return [s.strip().rstrip('.') for s in skills_text.split(",") if s.strip()]

def extract_education(text):
    sections = split_into_sections(text)
    edu_text = sections.get("Education", "")
    if not edu_text:
        return {"degrees": [], "institutions": [], "years": []}
    years = re.findall(r'\b(?:19|20)\d{2}\b', edu_text)
    degrees = []
    for kw in sorted(DEGREE_KEYWORDS, key=len, reverse=True):
        if kw.lower() in edu_text.lower() and not any(kw.lower() in d.lower() for d in degrees):
            degrees.append(kw)
    institutions = re.findall(r"([A-Za-z&,.' ]+?)\s+[－-]\s+City", edu_text)
    institutions = [i.strip() for i in institutions]
    return {"degrees": degrees, "institutions": institutions, "years": years}

def extract_name(text):
    doc = nlp(text[:300])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_email(text):
    match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d{1,2}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text)
    return match.group(0) if match else None

def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text)
    }

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text

st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="centered")
st.title("📄 AI Resume Parser")
st.write("Upload a resume (PDF) and get structured information extracted automatically.")

uploaded_file = st.file_uploader("Upload a resume PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    if not text.strip():
        st.error("Could not extract text from this PDF. It may be a scanned image rather than text-based.")
    else:
        with st.spinner("Parsing resume..."):
            result = parse_resume(text)

        st.success("Resume parsed successfully!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("👤 Contact Info")
            name = result['name'] or 'Not found'
            email = result['email'] or 'Not found'
            phone = result['phone'] or 'Not found'
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Phone:** {phone}")

        with col2:
            st.subheader("🎓 Education")
            edu = result['education']
            if edu['degrees']:
                st.write(f"**Degree(s):** {', '.join(edu['degrees'])}")
            if edu['institutions']:
                st.write(f"**Institution(s):** {', '.join(edu['institutions'])}")
            if edu['years']:
                st.write(f"**Year(s):** {', '.join(edu['years'])}")
            if not edu['degrees'] and not edu['institutions']:
                st.write("Not found")

        st.subheader("🛠️ Skills")
        if result['skills']:
            st.write(", ".join(result['skills']))
        else:
            st.write("Not found")

        with st.expander("View raw extracted text"):
            st.text(text)
else:
    st.info("👆 Upload a PDF resume to get started.")
