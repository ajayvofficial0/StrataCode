# StrataCode
Overview

StrataCode v2.10 is an AI-driven legacy code analysis and modernization tool. It analyzes uploaded Python source files and generates:

Risk & vulnerability assessment

Business logic explanation

Flowcharts & sequence diagrams

Function dependency call graphs

Python 3.12 rewritten modern code

Exportable JSON reports

Built using Streamlit + Google Gemini 2.5 Flash.

Features

✔ Upload any Python file
✔ Automated risk detection
✔ Business logic summarization
✔ Architecture diagrams (Mermaid)
✔ Function-level call graph
✔ Automatic modernization to Python 3.12
✔ Downloadable full report
✔ Hosted on Streamlit Cloud

Tech Stack

Frontend/UI: Streamlit

Backend Model: Gemini 

Language: Python

Visualization: Mermaid.js

Report Format: JSON

System Architecture
┌──────────────┐
│ User Upload  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Gemini Engine│
└──────┬───────┘
  Risk │ Logic │ Graph │ Modernization
       │
       ▼
┌──────────────┐
│ Streamlit UI │
└──────┬───────┘
       ▼
   JSON Export

Installation
pip install streamlit google-generativeai
streamlit run app.py


Set your API key in .streamlit/secrets.toml:

GEMINI_API_KEY = "your_key_here"

Usage

Open the web app.

Upload a .py file.

Wait for the 4-step analysis pipeline to complete.

View:

Risks

Business Logic

Diagrams

Modernized Code

Download JSON.

File Structure
app.py
streamlit/
 └── secrets.toml
requirements.txt
README.md

Limitations

Supports only single-file Python analysis

Complex inter-file relationships not yet handled

Modernization accuracy depends on LLM output

Future Scope

Multi-file project analysis

Multi-language support

Integration with GitHub/Bitbucket

Offline LLM support using open-source models
