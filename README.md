# LLM-Powered User Manual Generator

This project is a web-based application that uses a Large Language Model (LLM) to convert technical specification documents into structured, user-friendly manuals. The generated manuals are tailored to the user's audience level and language preference and can be exported in multiple formats.

## Features

### Core Features
- Upload technical specification files in .txt, .pdf, .docx, or .md format
- Automatically generate step-by-step instructions from technical content
- Manual content is structured into Introduction, Setup, Usage, and Troubleshooting
- Supports different audience levels: Beginner, Intermediate, and Expert
- Offers language support for English, Spanish, Hindi, French, and German
- Allows revision and regeneration of individual manual sections for better clarity

### Bonus Features
- Interactive manual view with collapsible sections
- Visual aid suggestions based on manual content
- Export options available: DOCX, HTML, and PDF

## Tech Stack

- Python 3.11+
- Streamlit (frontend)
- Together.ai API (LLM backend)
- fpdf, python-docx, markdown2, PyMuPDF for file processing and exporting
- dotenv for secure API key management

## Installation

1. Clone this repository:

```bash
git clone https://github.com/meetali17/user-manual-generator.git
cd user-manual-generator
Set up a virtual environment and activate it:

bash
Copy
Edit
python -m venv venv
venv\\Scripts\\activate   # On Windows
Install all dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file in the root directory and add your Together.ai API key:

ini
Copy
Edit
TOGETHER_API_KEY=your_api_key_here
Running the Application
Start the Streamlit app with:

bash
Copy
Edit
streamlit run interface/app.py
Project Structure
bash
Copy
Edit
user-manual-generator/
├── interface/
│   └── app.py
├── models/
│   └── together_client.py
├── ingestion/
│   └── extract_text_from_file.py
├── requirements.txt
├── .env
├── README.md
Sample Output
Upload a technical document

Select target audience and output language

Review and regenerate specific sections if needed

Export the final manual as DOCX, HTML, or PDF
