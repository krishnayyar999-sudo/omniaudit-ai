import streamlit as st
from google import genai

st.set_page_config(page_title="OmniAudit AI", page_icon="🛡️", layout="wide")

st.title("🛡️ OmniAudit: AI Code Security & Complexity Inspector")
st.caption("Catch bugs, calculate Big-O complexity, and optimize your code.")

# Left Sidebar for settings
with st.sidebar:
  st.header("Settings")
  api_key = st.text_input(
      "Paste your Gemini API Key here:",
      type="password",
      help="Get it free from aistudio.google.com",
  )
  language = st.selectbox("Language:", ["C++", "Python", "Other"])
  focus = st.radio(
      "Audit Focus:",
      ["Full Inspection", "Bugs & Security Only", "Time & Space (Big-O) Only"],
  )

# Main area split into two columns
col1, col2 = st.columns(2)

with col1:
  st.subheader("Your Code")
  code_input = st.text_area(
      "Paste your code here:",
      height=350,
      placeholder="// Paste C++ or Python code here...",
  )
  submit = st.button("🚀 Run Audit", use_container_width=True)

with col2:
  st.subheader("Audit Report")
  if submit:
    if not api_key:
      st.error("Please paste your Gemini API key in the left sidebar first!")
    elif not code_input.strip():
      st.warning("Please paste some code to audit!")
    else:
      with st.spinner("Analyzing code..."):
        try:
          client = genai.Client(api_key=api_key)

          prompt = f"""
                    You are an expert software engineer and code auditor.
                    Target Language: {language}
                    Focus: {focus}

                    Analyze this code:
                    ```{language}
                    {code_input}
                    ```

                    Format your response clearly:
                    ### 1. ⚠️ Potential Bugs & Edge Cases
                    ### 2. ⚡ Time & Space Complexity (Big-O)
                    ### 3. 🛠️ Optimized & Fixed Code
                    """

          response = client.models.generate_content(
              model="gemini-3.8-flash", contents=prompt
          )

          st.markdown(response.text)
          st.download_button(
              "📥 Download Report",
              response.text,
              file_name="audit_report.md",
              mime="text/markdown",
          )
        except Exception as e:
          st.error(f"Something went wrong: {e}")