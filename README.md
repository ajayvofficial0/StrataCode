# 🚀 StrataCode v2.10

**Automated Legacy Code Analysis & Modernization Pipeline**  
*By Ajay Viswanagaraj*

StrataCode v2.10 is an AI-powered platform that analyzes legacy Python code and automatically produces:
- 🔥 Risk & vulnerability assessment  
- 🧠 Business logic extraction  
- 🕸 Call graph & dependency mapping  
- 📊 Flowchart & sequence diagram (Mermaid)  
- 🛠 Modernized Python 3.12 rewritten code  
- 📥 Downloadable JSON report  

This tool is built using **Streamlit** and **Google Gemini 2.5 Flash**, and deployed on **Streamlit Cloud**.

---

## 📌 Features

✔ Upload any `.py` file  
✔ Automatic security risk scoring  
✔ Extract high-level business logic  
✔ Generate Mermaid diagrams:  
   - Flowchart  
   - Sequence Diagram  
   - Call Graph  
✔ Rewrite legacy code into Python 3.12  
✔ Full JSON report export  
✔ Clean, interactive Streamlit UI  

---

## 🏗 System Architecture
┌──────────────────┐
│ Upload Code │
└─────────┬────────┘
▼
┌──────────────────┐
│ Gemini Processing │
│ 1. Risk Analysis │
│ 2. Logic Extract │
│ 3. Call Graph │
│ 4. Modernization │
└─────────┬────────┘
▼
┌──────────────────┐
│ Streamlit UI │
│ + JSON Export │
└──────────────────┘

text

---

## 🛠 Tech Stack

| Component         | Technology       |
|-------------------|------------------|
| **UI**            | Streamlit        |
| **LLM**           | Google Gemini    |
| **Language**      | Python 3         |
| **Visualization** | Mermaid.js       |
| **Deployment**    | Streamlit Cloud  |
| **Data Format**   | JSON             |

---

## 📦 Installation

### 1️⃣ Clone the repository

git clone https://github.com/<your-username>/stratacode.git
cd stratacode
---

2️⃣ Install dependencies

pip install -r requirements.txt

---
3️⃣ Add your Gemini API Key
Create the file: .streamlit/secrets.toml

Put inside:

toml
GEMINI_API_KEY = "your_api_key_here"

---

4️⃣ Run the app

streamlit run app.py
---

🎯 Usage
Open the Streamlit app in your browser

Upload a Python file

The pipeline automatically runs through four stages:

Risk Analysis

Business Logic Extraction

Call Graph Analysis

Modern Code Rewrite

View the diagrams and results

Export the JSON report

---

📁 Project Structure
text
├── app.py               # Main Streamlit application
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── .streamlit/
    └── secrets.toml    # Gemini API key (not committed)
---


---
⚠ Limitations
Only single-file Python uploads are supported

Multi-file / multi-language analysis not yet implemented

Modernization accuracy depends on LLM model output

---

🚧 Future Enhancements
Multi-file project analysis

Support for Java, C, C++, COBOL

GitHub repository scanning (auto-analyze repo)

VS Code / JetBrains extension

On-premise version using open-source LLMs

---

🤝 Contributing
Pull requests are welcome!
For major changes, please open an issue first.



📜 License
MIT License © 2025 Ajay Viswanagaraj


⭐ Support
If this project helped you, consider giving it a star ⭐ on GitHub!
