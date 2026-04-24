import streamlit as st
import requests
import re
from streamlit_quill import st_quill

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="AI Resume Builder", layout="wide")

# -------------------------
# MODERN UI CSS
# -------------------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.resume-box {
    background: #020617;
    padding: 30px;
    border-radius: 15px;
    border: 1px solid #334155;
    font-size: 16px;
    line-height: 1.7;
}

.tag {
    display: inline-block;
    padding: 6px 12px;
    margin: 5px;
    border-radius: 20px;
    font-size: 13px;
}

.green {
    background-color: #064e3b;
    color: #6ee7b7;
}

.red {
    background-color: #7f1d1d;
    color: #fca5a5;
}

/* ATS CARD */
.ats-card {
    background: linear-gradient(135deg, #1e293b, #020617);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #334155;
    text-align: center;
    margin-bottom: 20px;
}

.ats-score {
    font-size: 48px;
    font-weight: bold;
    color: #38bdf8;
}

.ats-label {
    font-size: 18px;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("<div class='title'>🚀 AI Resume Builder</div>", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
menu = st.sidebar.radio("Navigation", [
    "📝 Input Details",
    "🧠 Skill Analysis",
    "📄 Generate Resume",
    "✏️ Resume Editor",
    "📚 Resume History",
    "📥 Download"
])

# -------------------------
# SESSION STATE
# -------------------------
if "resume" not in st.session_state:
    st.session_state["resume"] = ""

if "data" not in st.session_state:
    st.session_state["data"] = {}

# -------------------------
# INPUT PAGE
# -------------------------
if menu == "📝 Input Details":

    st.markdown("### 📋 Enter Your Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Name",
            placeholder="Enter your full name "
        )

        skills = st.text_area(
            "Skills",
            placeholder="e.g., Python, Machine Learning, SQL, AWS"
        )
        st.caption("💡 Tip: Add 5–10 relevant skills")

        projects = st.text_area(
            "Projects",
            placeholder="e.g., AI Resume Builder, Fraud Detection System"
        )

    with col2:
        experience = st.text_area(
            "Experience",
            placeholder="e.g., Intern at XYZ company, worked on ML models"
        )

        education = st.text_area(
            "Education",
            placeholder="e.g., B.Tech in Computer Science, XYZ College (2021–2025)"
        )

        job_description = st.text_area(
            "Job Description",
            placeholder="Paste job description here..."
        )

    certifications = st.text_area(
        "Certifications",
        placeholder="e.g., AWS Certified, Google Data Analytics"
    )

    achievements = st.text_area(
        "Achievements",
        placeholder="e.g., Hackathon Winner, Top 5 coder"
    )

    template = st.selectbox(
        "Template",
        ["Professional", "Modern", "Minimal"]
    )

    st.session_state["data"] = {
        "name": name,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education,
        "job_description": job_description,
        "certifications": certifications,
        "achievements": achievements,
        "template": template
    }

    

# -------------------------
# SKILL ANALYSIS (UPDATED 🔥)
# -------------------------
elif menu == "🧠 Skill Analysis":

    st.markdown("### 🧠 Skill Analysis")

    if st.button("Analyze Skills"):

        data = st.session_state.get("data", {})

        try:
            res = requests.post(
                "http://127.0.0.1:8000/analysis/skills",
                json={
                    "skills": data.get("skills", ""),
                    "job_description": data.get("job_description", "")
                }
            )

            result = res.json()

            score = result.get("ats_score", 0)

            # -------------------------
            # ATS CARD
            # -------------------------
            st.markdown(f"""
                <div class="ats-card">
                    <div class="ats-label">ATS SCORE</div>
                    <div class="ats-score">{score}%</div>
                </div>
            """, unsafe_allow_html=True)

            # -------------------------
            # PROGRESS BAR
            # -------------------------
            st.progress(score)

            # -------------------------
            # FEEDBACK
            # -------------------------
            if score >= 80:
                st.success("🚀 Excellent Match")
            elif score >= 60:
                st.warning("⚡ Good Match - Improve Few Skills")
            else:
                st.error("❗ Low Match - Improve Your Skills")

            st.info(result.get("summary", ""))

            # -------------------------
            # SKILLS
            # -------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Matched Skills")
                for s in result.get("matched_skills", []):
                    st.markdown(f"<span class='tag green'>{s}</span>", unsafe_allow_html=True)

            with col2:
                st.markdown("### ❌ Missing Skills")
                for s in result.get("missing_skills", []):
                    st.markdown(f"<span class='tag red'>{s}</span>", unsafe_allow_html=True)

        except Exception as e:
            st.error(str(e))

# -------------------------
# GENERATE RESUME
# -------------------------
elif menu == "📄 Generate Resume":

    st.markdown("### 📄 Generate Resume")

    data = st.session_state.get("data", {})
    template = data.get("template", "Professional")

    if st.button("Generate Resume 🚀"):

        try:
            res = requests.post(
                "http://127.0.0.1:8000/ai/generate",
                json=data
            )

            result = res.json()
            resume = result.get("resume", "")

            if resume:
                resume = re.sub(r"\*\*", "", resume)
                resume = resume.replace("\\n", "\n")
                st.session_state["resume"] = resume
            else:
                st.error("❌ Resume not generated")

        except Exception as e:
            st.error(str(e))

    resume = st.session_state.get("resume", "")

    if resume:
        st.markdown("### 📄 Resume Preview")

        st.markdown("<div class='resume-box'>", unsafe_allow_html=True)
        st.write(resume)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("💾 Save Resume"):

            try:
                res = requests.post(
                    "http://127.0.0.1:8000/resume/save",
                    json={"content": resume, "template": template}
                )

                if res.status_code == 200:
                    st.success("Saved successfully ✅")
                else:
                    st.error("Failed to save")

            except Exception as e:
                st.error(str(e))


elif menu == "✏️ Resume Editor":

    st.markdown("### ✏️ Resume Editor (Rich Text)")

    resume = st.session_state.get("resume", "")

    if not resume:
        st.warning("⚠️ Generate resume first")
    else:

        # -------------------------
        # RICH TEXT EDITOR
        # -------------------------
        edited_resume = st_quill(
            value=resume,
            html=True,
            toolbar=[
                ["bold", "italic", "underline"],
                [{"header": [1, 2, 3, False]}],
                [{"list": "ordered"}, {"list": "bullet"}],
                ["clean"]
            ]
        )

        # -------------------------
        # UPDATE BUTTON
        # -------------------------
        if st.button("💾 Update Resume"):
            st.session_state["resume"] = edited_resume
            st.success("Updated successfully ✅")

        # -------------------------
        # SAVE TO DATABASE
        # -------------------------
        if st.button("📤 Save to Database"):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/resume/save",
                    json={
                        "content": edited_resume,
                        "template": "Rich Editor"
                    }
                )

                if res.status_code == 200:
                    st.success("Saved successfully ✅")
                else:
                    st.error("Failed to save")

            except Exception as e:
                st.error(str(e))

        # -------------------------
        # AI IMPROVE
        # -------------------------
        if st.button("🤖 Improve with AI"):

            try:
                res = requests.post(
                    "http://127.0.0.1:8000/ai/improve",
                    json={
                        "resume": edited_resume,
                        "feedback": "Make it more professional, ATS optimized"
                    }
                )

                result = res.json()
                improved = result.get("improved_resume", "")

                if improved:
                    st.session_state["resume"] = improved
                    st.success("Improved 🚀")
                    st.rerun()

            except Exception as e:
                st.error(str(e))

        # -------------------------
        # LIVE PREVIEW
        # -------------------------
        st.markdown("### 📄 Live Preview")

        st.markdown("<div class='resume-box'>", unsafe_allow_html=True)
        st.markdown(st.session_state["resume"], unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# HISTORY
# -------------------------
elif menu == "📚 Resume History":

    st.markdown("### 📚 Resume History")

    if st.button("Load Previous Resumes"):

        try:
            res = requests.get("http://127.0.0.1:8000/resume/all")

            if res.status_code != 200:
                st.error("Backend error")
            else:
                data = res.json()

                if not data:
                    st.warning("No resumes found")
                else:
                    for r in data:
                        st.markdown("---")
                        st.markdown(r.get("content", ""))

        except Exception as e:
            st.error(str(e))

# -------------------------
# DOWNLOAD
# -------------------------
elif menu == "📥 Download":

    resume = st.session_state.get("resume", "")

    if not resume:
        st.warning("Generate resume first")

    else:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Download PDF"):
                res = requests.post(
                    "http://127.0.0.1:8000/ai/download",
                    json={"resume": resume}
                )
                with open("resume.pdf", "wb") as f:
                    f.write(res.content)
                st.success("Downloaded PDF")

        with col2:
            if st.button("Download DOCX"):
                res = requests.post(
                    "http://127.0.0.1:8000/ai/download-docx",
                    json={"resume": resume}
                )
                with open("resume.docx", "wb") as f:
                    f.write(res.content)
                st.success("Downloaded DOCX")