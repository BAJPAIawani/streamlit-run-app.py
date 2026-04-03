import streamlit as st
import spacy
import PyPDF2

# ---------- CSS ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1 {
    color: #4CAF50;
    text-align: center;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px;
}

.tag {
    padding:6px 12px;
    border-radius:15px;
    margin:5px;
    display:inline-block;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------- Load Model ----------
nlp = spacy.load("en_core_web_sm")

# ---------- Title ----------
st.markdown("<h1>🚀 AI Resume Analyzer</h1>", unsafe_allow_html=True)

# ---------- Input Card ----------
st.markdown("""
<div style="background-color:white;padding:20px;border-radius:10px;margin-bottom:20px">
<h3>📄 Upload Resume & Job Description</h3>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste Job Description")

# ---------- Skills ----------
skills = [
    "Python","C","HTML","CSS","JavaScript",
    "SQL","Django","Excel","PowerPoint","Word"
]

# ---------- Button ----------
if st.button("Analyze Resume"):

    if uploaded_file is not None and job_description != "":

        # ---------- Read PDF ----------
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if text.strip() == "":
            st.error("❌ Could not extract text from PDF")
        else:
            st.subheader("📄 Resume Text")
            st.write(text)

            # ---------- Process Resume ----------
            doc = nlp(text)
            found_skills = set()

            skills_lower = [s.lower() for s in skills]

            for token in doc:
                if token.text.lower() in skills_lower:
                    found_skills.add(token.text)

            st.subheader("✅ Skills Found in Resume")
            for skill in found_skills:
                st.markdown(
                    f"<span class='tag' style='background-color:#4CAF50'>{skill}</span>",
                    unsafe_allow_html=True
                )

            # ---------- Resume Score ----------
            resume_score = (len(found_skills) / len(skills)) * 100
            st.write(f"📊 Resume Skill Score: {round(resume_score,2)}%")

            # ---------- Process Job Description ----------
            jd_doc = nlp(job_description)
            required_skills = set()

            for token in jd_doc:
                if token.text.lower() in skills_lower:
                    required_skills.add(token.text)

            st.subheader("📌 Skills Required in Job")
            for skill in required_skills:
                st.markdown(
                    f"<span class='tag' style='background-color:#2196F3'>{skill}</span>",
                    unsafe_allow_html=True
                )

            # ---------- Matched Skills ----------
            matched_skills = found_skills.intersection(required_skills)
            st.subheader("🎯 Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.markdown(
                        f"<span class='tag' style='background-color:#4CAF50'>{skill}</span>",
                        unsafe_allow_html=True
                    )
            else:
                st.write("No matched skills")

            # ---------- Missing Skills ----------
            missing_skills = required_skills - found_skills
            st.subheader("❌ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.markdown(
                        f"<span class='tag' style='background-color:#f44336'>{skill}</span>",
                        unsafe_allow_html=True
                    )
            else:
                st.write("None 🎉")

            # ---------- Match Score ----------
            if len(required_skills) == 0:
                st.warning("No skills found in Job Description")
            else:
                match_score = (len(matched_skills) / len(required_skills)) * 100

                st.markdown(f"""
                <div style="background-color:#e8f5e9;padding:20px;border-radius:10px;text-align:center;margin-top:20px">
                <h2>📊 Resume Match Score: {round(match_score,2)}%</h2>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please upload resume and enter job description")