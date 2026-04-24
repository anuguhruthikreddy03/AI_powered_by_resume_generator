# 📄 AI Resume Builder

AI Resume Builder is a full-stack application that generates **professional, ATS-friendly resumes** using Artificial Intelligence.  
It converts user input into structured, job-ready resumes with minimal manual effort.

---

## 🚀 Features

- 🤖 AI-based resume generation  
- 🎯 Job-specific customization  
- 📊 ATS-friendly formatting  
- ✏️ Real-time preview and editing  
- 📄 Export to PDF/DOCX  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Language:** Python  
- **AI/NLP:** LLM APIs  

---

## 🏗️ Architecture
[ Streamlit UI ]
        │
        ▼
[ FastAPI Backend ]
        │
        ▼
[ LLM Service ]
        │
        ▼
[ Formatter + Export Engine ]


---

## ⚙️ Setup

### 1. Clone Repository

```bash
git clone https://github.com/anuguhruthikreddy03/AI_powered_by_resume_generator.git
cd AI_powered_by_resume_generator
2. Create Virtual Environment
python -m venv venv

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Environment Variables

Create a .env file in the root directory:

API_KEY=your_api_key
SECRET_KEY=your_secret_key

▶️ Run the Application
Start Backend

uvicorn main:app --reload

Start Frontend

streamlit run app.py

🧠 How It Works

User enters personal and professional details
Backend processes and validates input
AI generates optimized resume content
Resume is structured into sections
User previews and downloads the resume

🎥 Demo

📊 Impact
Reduces resume creation time
Improves content quality and structure
Helps beginners build professional resumes
