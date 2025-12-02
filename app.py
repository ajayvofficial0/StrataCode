import streamlit as st
import google.generativeai as genai
import json
import re

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="StrataCode v2.10", layout="wide")

# 🔑 REPLACE WITH YOUR API KEY
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
# genai.configure(api_key="") 

# NOTE: Using 1.5-flash for stability (2.5 often errors out on free keys)
MODEL_NAME = "models/gemini-2.5-flash"

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def clean_json_text(text):
    """Strips markdown code blocks from Gemini response."""
    cleaned = re.sub(r"```json", "", text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()

def get_gemini_json(prompt, source_code):
    """Sends prompt to Gemini and returns JSON object."""
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
        cleaned_text = clean_json_text(response.text)
        return json.loads(cleaned_text)
    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------------
# UI HEADER
# ---------------------------------------------------------
st.title("⭐ StrataCode v2.10")
st.caption("Automated Legacy Code Analysis & Modernization Pipeline")
st.divider()

uploaded = st.file_uploader("Upload a Python file (.py)", type=["py"])

if uploaded:
    source = uploaded.read().decode("utf-8")

    # ---------------------------------------------------------
    # TOP SECTION: CODE + STATUS
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1.5])

    # --- LEFT: SCROLLABLE SOURCE CODE ---
    with col1:
        st.subheader("📄 Source Code")
        # THIS IS THE CHANGE YOU WANTED: Fixed height container makes it scrollable
        with st.container(height=600):
            st.code(source, language="python", line_numbers=True)

    # --- RIGHT: PIPELINE STATUS ---
    with col2:
        st.subheader("🔍 Analysis Pipeline")
        
        # Initialize session state for results
        if "results" not in st.session_state:
            st.session_state.results = None

        # Logic to run the pipeline
        if st.session_state.results is None:
            with st.status("Running StrataCode Pipeline...", expanded=True) as status:
                
                # 1. RISK
                st.write("1️⃣ Scanning for Risks...")
                prompt_risk = """
                You are a Security Engineer. Return JSON:
                - risk_level ("HIGH"/"MEDIUM"/"LOW")
                - risk_score (0-100)
                - vulnerabilities (list of strings)
                - bad_practices (list of strings)
                """
                risk_data = get_gemini_json(prompt_risk, source)
                
                # 2. LOGIC
                st.write("2️⃣ Extracting Business Logic...")
                prompt_logic = """
                You are a Architect. Return JSON:
                - business_logic (String summary)
                - high_level_flowchart (Mermaid 'flowchart TD' code only)
                - sequence_diagram (Mermaid 'sequenceDiagram' code only)
                """
                logic_data = get_gemini_json(prompt_logic, source)

                # 3. GRAPH
                st.write("3️⃣ Mapping Dependencies...")
                prompt_graph = """
                You are a Code Analyst. Return JSON:
                - functions (List of strings)
                - call_graph_mermaid (Mermaid 'graph TD' code only)
                """
                graph_data = get_gemini_json(prompt_graph, source)

                # 4. MODERNIZATION
                st.write("4️⃣ Modernizing Code...")
                prompt_modern = """
                Rewrite to Python 3.12. Return JSON:
                - modern_python_code (String)
                - improvements (List of strings)
                - why_it_is_better (List of strings)
                """
                modern_data = get_gemini_json(prompt_modern, source)

                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                st.session_state.results = {
                    "risk": risk_data,
                    "logic": logic_data,
                    "graph": graph_data,
                    "modern": modern_data
                }

    # ---------------------------------------------------------
    # BOTTOM SECTION: FULL WIDTH RESULTS
    # ---------------------------------------------------------
    if st.session_state.results:
        st.divider()
        data = st.session_state.results
        risk = data["risk"]
        logic = data["logic"]
        graph = data["graph"]
        modern = data["modern"]

        if "error" in risk:
            st.error(f"❌ API Error: {risk['error']}")
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
            # DOWNLOAD BUTTON
            st.download_button(
                label="📥 Download Full Report (.json)",
                data=json.dumps(data, indent=4),
                file_name="stratacode_report.json",
                mime="application/json"
            )