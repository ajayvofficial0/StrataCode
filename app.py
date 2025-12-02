import streamlit as st
import google.generativeai as genai
import json
import re

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="StrataCode v2.0", layout="wide")

# 🔑 IMPORTANT: Replace this with your own working API Key from Google AI Studio
# The one below is a placeholder and might not work.
# Try to get key from Streamlit Secrets (Cloud) or Environment Variable
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
# genai.configure(api_key="") 

# Use a standard stable model
MODEL_NAME = "models/gemini-2.5-flash"

# ---------------------------------------------------------
# HELPER FUNCTIONS (The Fix is Here)
# ---------------------------------------------------------
def clean_json_text(text):
    """
    Gemini often returns markdown code blocks (```json ... ```).
    We must strip them before parsing.
    """
    # Remove ```json and ``` at start/end
    cleaned = re.sub(r"```json", "", text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()

def get_gemini_json(prompt, source_code):
    """
    Sends a prompt + code to Gemini and handles errors robustly.
    """
    full_prompt = f"""
    {prompt}

    IMPORTANT: RETURN RAW JSON ONLY. DO NOT USE MARKDOWN BLOCK. DO NOT EXPLAIN.
    
    CODE TO ANALYZE:
    {source_code}
    """
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            full_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # CLEAN THE RESPONSE BEFORE PARSING
        raw_text = response.text
        cleaned_text = clean_json_text(raw_text)
        
        return json.loads(cleaned_text)

    except Exception as e:
        # If API fails, return an error dictionary so the app doesn't crash
        return {"error": str(e), "raw_response": "API Call Failed"}

# ---------------------------------------------------------
# UI HEADER
# ---------------------------------------------------------
st.title("⭐ StrataCode v2.0")
st.caption("Automated Legacy Code Analysis & Modernization Pipeline")

uploaded = st.file_uploader("Upload a Python file (.py)", type=["py"])

if uploaded:
    source = uploaded.read().decode("utf-8")

    # Layout: 2 Columns
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("📄 Source Code")
        st.code(source, language="python", line_numbers=True)

    with col2:
        st.subheader("🔍 Analysis Pipeline")
        
        # Status Container
        with st.status("Running StrataCode Pipeline...", expanded=True) as status:
            
            # 1. RISK
            st.write("1️⃣ Scanning for Risks & Vulnerabilities...")
            prompt_risk = """
            You are a Senior Security Engineer. Analyze this code.
            Return a JSON object with strictly these fields:
            - risk_level (String: "HIGH", "MEDIUM", or "LOW")
            - risk_score (Integer: 0-100)
            - reasons (List of strings)
            - vulnerabilities (List of strings)
            - bad_practices (List of strings)
            """
            risk_data = get_gemini_json(prompt_risk, source)
            
            # 2. LOGIC
            st.write("2️⃣ Extracting Business Logic...")
            prompt_logic = """
            You are a System Architect. Explain conceptual logic.
            Return a JSON object with strictly these fields:
            - business_logic (String summary)
            - high_level_flowchart (String: Mermaid JS 'flowchart TD' code only)
            - sequence_diagram (String: Mermaid JS 'sequenceDiagram' code only)
            """
            logic_data = get_gemini_json(prompt_logic, source)

            # 3. GRAPH
            st.write("3️⃣ Mapping Dependencies...")
            prompt_graph = """
            You are a Code Analyst. Map function calls.
            Return a JSON object with strictly these fields:
            - functions (List of strings)
            - call_graph_mermaid (String: Mermaid JS 'graph TD' code showing calls)
            """
            graph_data = get_gemini_json(prompt_graph, source)

            # 4. MODERNIZATION
            st.write("4️⃣ Modernizing Code...")
            prompt_modern = """
            You are a Python Expert. Rewrite code to Python 3.12+.
            Return a JSON object with strictly these fields:
            - modern_python_code (String: The full rewritten code)
            - improvements (List of strings)
            - why_it_is_better (List of strings)
            """
            modern_data = get_gemini_json(prompt_modern, source)

            status.update(label="Analysis Complete!", state="complete", expanded=False)

    # ---------------------------------------------------------
    # RESULTS DISPLAY
    # ---------------------------------------------------------
    st.divider()

    # CHECK FOR ERRORS FIRST
    if "error" in risk_data:
        st.error(f"❌ API Error: {risk_data['error']}")
        st.warning("Please check your API Key in the code.")
    else:
        # SECTION 1: RISK
        risk_level = risk_data.get("risk_level", "UNKNOWN")
        color = "red" if risk_level == "HIGH" else "orange" if risk_level == "MEDIUM" else "green"
        
        with st.expander(f"🔥 Risk & Vulnerabilities (Level: {risk_level})", expanded=True):
            st.markdown(f":{color}[**Risk Score: {risk_data.get('risk_score', 0)}/100**]")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🚨 Vulnerabilities**")
                for v in risk_data.get("vulnerabilities", []):
                    st.error(f"- {v}")
            with c2:
                st.markdown("**⚠️ Bad Practices**")
                for b in risk_data.get("bad_practices", []):
                    st.warning(f"- {b}")

        # SECTION 2: BUSINESS LOGIC
        with st.expander("🧠 Business Logic & Diagrams", expanded=False):
            st.info(logic_data.get("business_logic", "No logic extracted."))
            tab_flow, tab_seq = st.tabs(["Flowchart", "Sequence Diagram"])
            with tab_flow:
                st.code(logic_data.get("high_level_flowchart", ""), language="mermaid")
            with tab_seq:
                st.code(logic_data.get("sequence_diagram", ""), language="mermaid")

        # SECTION 3: CALL GRAPH
        with st.expander("🕸 Call Graph Architecture", expanded=False):
            st.write("**Detected Functions:**", graph_data.get("functions", []))
            st.code(graph_data.get("call_graph_mermaid", ""), language="mermaid")

        # SECTION 4: MODERNIZATION
        with st.expander("🛠 Modernized Code (Python 3.12)", expanded=False):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.code(modern_data.get("modern_python_code", "# Error"), language="python")
            with c2:
                st.success("**Improvements:**")
                for imp in modern_data.get("improvements", []):
                    st.write(f"✅ {imp}")

        # REPORT DOWNLOAD
        full_report = {
            "risk": risk_data,
            "logic": logic_data,
            "graph": graph_data,
            "modern": modern_data
        }
        st.download_button("📥 Download Report", json.dumps(full_report, indent=4), "report.json")