import sys
import os
import io
import re
from docx import Document
from fpdf import FPDF

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from models.together_client import generate_manual
from ingestion import extract_text_from_file

st.set_page_config(page_title="LLM Manual Generator", layout="wide")
st.title("🛠️ LLM-Powered User Manual Generator")

# Upload
uploaded_file = st.file_uploader("📄 Upload your tech spec file", type=["txt", "pdf", "docx", "md"])
technical_level = st.selectbox("🎯 Select audience level", ["Beginner", "Intermediate", "Expert"])
language = st.selectbox("🌐 Select output language", ["English", "Spanish", "Hindi", "French", "German"])
st.caption("✏️ The manual will be translated and structured using AI.")

# If file is uploaded
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()
    raw_text = extract_text_from_file(uploaded_file, file_type)

    st.subheader("📃 Extracted Tech Spec")
    st.text_area("Tech Spec Text", raw_text, height=200)

    if st.button("🪄 Generate Manual"):
        with st.spinner("Generating structured manual..."):
            prompt = f"""
You are a helpful assistant. Convert the following technical document into a user manual suitable for a {technical_level} audience.

Structure the manual using the following sections:
1. Introduction
2. Setup
3. Usage
4. Troubleshooting

Translate the manual into {language}.
Use clear, step-by-step instructions and avoid technical jargon.

After each section, suggest where an image, diagram, or screenshot would be helpful.
Write it like this:
[Suggested Visual: description here]

Technical Document:
"""
            prompt += f"""{raw_text}
"""
            result = generate_manual(prompt)

            st.markdown("### 📘 Generated Manual (Collapsible View)")

            # Split manual into sections based on numbered headers
            sections = re.split(r"\n(?=\d+\.\s)", result)
            matches = [section.strip() for section in sections if section.strip()]

            updated_sections = []

            for idx, section in enumerate(matches):
                title = section.strip().split("\n")[0][:60]
                with st.expander(title, expanded=False):
                    st.markdown(section)
                    regenerate = st.button(f"🔁 Regenerate This Section", key=f"regen_{idx}")
                    if regenerate:
                        with st.spinner("Regenerating section..."):
                            feedback_prompt = f"""
You are a helpful assistant. Rewrite the following section of a user manual to improve clarity and simplicity for a {technical_level} audience in {language}.

Text:
"""
                            feedback_prompt += f"""{section.strip()}
"""
                            new_section = generate_manual(feedback_prompt)
                            st.success("✅ Section regenerated.")
                            st.markdown(new_section)
                            updated_sections.append(new_section)
                    else:
                        updated_sections.append(section)

            final_manual = "\n\n".join(updated_sections)

            # Display suggested visuals
            visual_lines = [line for line in final_manual.split("\n") if "[Suggested Visual:" in line]
            for v in visual_lines:
                desc = v.replace("[Suggested Visual:", "").replace("]", "").strip()
                st.image("https://via.placeholder.com/400x200.png?text=Suggested+Visual", caption=desc)

            # DOCX Export
            docx_file = io.BytesIO()
            doc = Document()
            for line in final_manual.split("\n"):
                doc.add_paragraph(line)
            doc.save(docx_file)
            docx_file.seek(0)

            # HTML Export
            html_file = io.BytesIO()
            html_file.write(final_manual.encode("utf-8"))
            html_file.seek(0)

            # PDF Export
            pdf_file = io.BytesIO()
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in final_manual.split("\n"):
                if line.strip():
                    pdf.multi_cell(0, 10, line)
                else:
                    pdf.ln()
            pdf_output = pdf.output(dest="S").encode("latin1")
            pdf_file.write(pdf_output)
            pdf_file.seek(0)

            st.markdown("### 📤 Export Manual")
            st.download_button("⬇️ Download as DOCX", data=docx_file, file_name="manual.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.download_button("⬇️ Download as HTML", data=html_file, file_name="manual.html", mime="text/html")
            st.download_button("⬇️ Download as PDF", data=pdf_file, file_name="manual.pdf", mime="application/pdf")

else:
    st.warning("📂 Please upload a technical document to begin.")
