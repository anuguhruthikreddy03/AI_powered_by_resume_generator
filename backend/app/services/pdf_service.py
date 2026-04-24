from weasyprint import HTML


# -------------------------
# 🔹 HTML TEMPLATES
# -------------------------
def generate_resume_template(data: dict, template: str = "simple"):

    name = data.get("name", "")
    skills = data.get("skills", "")
    experience = data.get("experience", "")
    projects = data.get("projects", "")
    education = data.get("education", "")
    certifications = data.get("certifications", "")
    achievements = data.get("achievements", "")

    # -------------------------
    # 🟢 SIMPLE TEMPLATE
    # -------------------------
    if template == "simple":
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial; margin: 40px; }}
                h1 {{ color: black; }}
                h2 {{ margin-top: 20px; }}
            </style>
        </head>
        <body>

        <h1>{name}</h1>

        <h2>Skills</h2>
        <p>{skills}</p>

        <h2>Experience</h2>
        <p>{experience}</p>

        <h2>Projects</h2>
        <p>{projects}</p>

        <h2>Education</h2>
        <p>{education}</p>

        <h2>Certifications</h2>
        <p>{certifications}</p>

        <h2>Achievements</h2>
        <p>{achievements}</p>

        </body>
        </html>
        """

    # -------------------------
    # 🔵 MODERN TEMPLATE
    # -------------------------
    elif template == "modern":
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI';
                    margin: 30px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                }}
                h1 {{
                    color: #2563EB;
                    border-bottom: 2px solid #2563EB;
                    padding-bottom: 5px;
                }}
                h2 {{
                    color: #1e40af;
                }}
                p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>

        <div class="container">

        <h1>{name}</h1>

        <h2>Skills</h2>
        <p>{skills}</p>

        <h2>Experience</h2>
        <p>{experience}</p>

        <h2>Projects</h2>
        <p>{projects}</p>

        <h2>Education</h2>
        <p>{education}</p>

        <h2>Certifications</h2>
        <p>{certifications}</p>

        <h2>Achievements</h2>
        <p>{achievements}</p>

        </div>

        </body>
        </html>
        """

    else:
        raise ValueError("Invalid template type")

    return html


# -------------------------
# 🔥 CONVERT HTML → PDF
# -------------------------
def generate_pdf(data: dict, output_path: str, template: str = "simple"):

    html_content = generate_resume_template(data, template)

    HTML(string=html_content).write_pdf(output_path)

    return output_path