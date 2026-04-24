from app.services.groq_service import groq_completion


# -------------------------
# 🔥 BASE LLM CALL
# -------------------------
def call_llm(prompt: str):
    return groq_completion(prompt)


# -------------------------
# 🔥 RESUME OPTIMIZATION
# -------------------------
def optimize_resume(resume_text: str, job_role: str):

    prompt = f"""
You are an expert resume optimizer.

Rewrite the resume for the role: {job_role}

STRICT INSTRUCTIONS:
- Make it ATS-friendly
- Use strong action verbs (e.g., developed, built, optimized)
- Highlight relevant skills
- Improve bullet points
- Add industry keywords
- Keep it concise and professional

OUTPUT:
- Clean formatted resume
- No explanations

RESUME:
{resume_text}
"""

    return call_llm(prompt)


# -------------------------
# 🔥 RESUME IMPROVEMENT (FEEDBACK BASED)
# -------------------------
def improve_resume(resume_text: str, user_feedback: str):

    prompt = f"""
You are an AI resume assistant.

Improve the resume based on user feedback.

INSTRUCTIONS:
- Apply only relevant improvements
- Maintain professional format
- Do not add unnecessary content

USER FEEDBACK:
{user_feedback}

RESUME:
{resume_text}
"""

    return call_llm(prompt)


# -------------------------
# 🔥 JD SKILL EXTRACTION
# -------------------------
def extract_skills_from_text(text: str):

    prompt = f"""
Extract ONLY technical skills from the given text.

STRICT RULES:
- Return only Python list
- No explanation
- No sentences

TEXT:
{text}
"""

    return call_llm(prompt)