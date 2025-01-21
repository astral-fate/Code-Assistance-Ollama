import streamlit as st
import requests
import os

class OllamaHelper:
    def __init__(self, base_url='http://localhost:11434'):
        self.base_url = base_url

    def _generate(self, prompt):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "codellama",
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()['response']
        except requests.RequestException as e:
            st.error(f"Error communicating with Ollama: {str(e)}")
            return None

    def generate_code(self, prompt):
        return self._generate(f"Generate code for: {prompt}")

    def analyze_code(self, code):
        return self._generate(f"Analyze the following code and suggest improvements:\n\n{code}")

    def security_check(self, code):
        return self._generate(f"Perform a security check on the following code and identify potential issues:\n\n{code}")

    def generate_tests(self, code):
        return self._generate(f"Generate unit tests for the following code:\n\n{code}")

# Page configuration
st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="💻",
    layout="wide"
)

# Initialize Ollama helper
ollama_url = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
ollama = OllamaHelper(ollama_url)

# Title and description
st.title("AI Code Assistant")
st.markdown("""
This application helps you generate, analyze, and test code using AI assistance.
Choose an operation and enter your code or prompt below.
""")

# Create tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs([
    "Generate Code", 
    "Code Analysis", 
    "Security Check",
    "Generate Tests"
])

# Input area
code_input = st.text_area(
    "Enter your code or prompt here:",
    height=200,
    key="code_input"
)

# Generate Code tab
with tab1:
    if st.button("Generate Code", key="generate"):
        if code_input:
            with st.spinner("Generating code..."):
                result = ollama.generate_code(code_input)
                if result:
                    st.code(result, language="python")
        else:
            st.warning("Please enter a prompt.")

# Code Analysis tab
with tab2:
    if st.button("Analyze Code", key="analyze"):
        if code_input:
            with st.spinner("Analyzing code..."):
                result = ollama.analyze_code(code_input)
                if result:
                    st.markdown("### Analysis Results")
                    st.markdown(result)
        else:
            st.warning("Please enter code to analyze.")

# Security Check tab
with tab3:
    if st.button("Check Security", key="security"):
        if code_input:
            with st.spinner("Checking security..."):
                result = ollama.security_check(code_input)
                if result:
                    st.markdown("### Security Analysis")
                    st.markdown(result)
        else:
            st.warning("Please enter code to check.")

# Generate Tests tab
with tab4:
    if st.button("Generate Tests", key="tests"):
        if code_input:
            with st.spinner("Generating tests..."):
                result = ollama.generate_tests(code_input)
                if result:
                    st.markdown("### Generated Tests")
                    st.code(result, language="python")
        else:
            st.warning("Please enter code for test generation.")

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit and Ollama")
