import streamlit as st
import requests
import os
from typing import Optional

class LLMHelper:
    def __init__(self):
        # Get API configuration from environment variables
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

    def _generate(self, prompt: str) -> Optional[str]:
        """Generic method to generate responses using the configured LLM API."""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful programming assistant.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7
            }

            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
            
        except requests.RequestException as e:
            st.error(f"Error communicating with LLM API: {str(e)}")
            if not self.api_key:
                st.error("API key not configured. Please set the OPENAI_API_KEY environment variable.")
            return None

    def generate_code(self, prompt: str) -> Optional[str]:
        """Generate code based on the prompt."""
        return self._generate(
            f"Generate code for the following request. Provide only the code without explanations:\n\n{prompt}"
        )

    def analyze_code(self, code: str) -> Optional[str]:
        """Analyze code and suggest improvements."""
        return self._generate(
            f"Analyze the following code and suggest improvements. Be specific and detailed:\n\n{code}"
        )

    def security_check(self, code: str) -> Optional[str]:
        """Check code for security issues."""
        return self._generate(
            f"Perform a security analysis on the following code. Identify potential security issues and suggest fixes:\n\n{code}"
        )

    def generate_tests(self, code: str) -> Optional[str]:
        """Generate unit tests for the given code."""
        return self._generate(
            f"Generate comprehensive unit tests for the following code. Include test cases for edge cases:\n\n{code}"
        )

# Page configuration
st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="💻",
    layout="wide"
)

# Initialize LLM helper
@st.cache_resource
def get_llm_helper():
    return LLMHelper()

llm_helper = get_llm_helper()

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

# Check API key configuration
if not os.getenv('OPENAI_API_KEY'):
    st.warning("⚠️ OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable.")

# Generate Code tab
with tab1:
    if st.button("Generate Code", key="generate"):
        if code_input:
            with st.spinner("Generating code..."):
                result = llm_helper.generate_code(code_input)
                if result:
                    st.code(result, language="python")
        else:
            st.warning("Please enter a prompt.")

# Code Analysis tab
with tab2:
    if st.button("Analyze Code", key="analyze"):
        if code_input:
            with st.spinner("Analyzing code..."):
                result = llm_helper.analyze_code(code_input)
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
                result = llm_helper.security_check(code_input)
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
                result = llm_helper.generate_tests(code_input)
                if result:
                    st.markdown("### Generated Tests")
                    st.code(result, language="python")
        else:
            st.warning("Please enter code for test generation.")

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit and OpenAI")
