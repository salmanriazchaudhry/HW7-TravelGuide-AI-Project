# ============================================
# 1. Imports and Dependency Checks
# ============================================
import os
import json
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# PDF generation
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# OpenAI
from openai import OpenAI
try:
    import streamlit
    import openai
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
except ImportError as e:
    raise SystemExit(
        "\n❌ Missing dependency.\n"
        "Run:\n"
        "  pip install -r requirements.txt\n\n"
        f"Details: {e}\n"
    )
# ============================================
# 2. Environment Setup
# ============================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in environment variables.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ============================================
# 3. Streamlit UI Configuration
# ============================================
st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("AI Travel Planner (LLM Powered)")

# Session state
if "result" not in st.session_state:
    st.session_state.result = None
if "raw_response" not in st.session_state:
    st.session_state.raw_response = None
if "model_used" not in st.session_state:
    st.session_state.model_used = None
if "token_usage" not in st.session_state:
    st.session_state.token_usage = None

# ============================================
# 4. Prompt Engineering
# ============================================
def build_system_prompt():
    return """
You are an expert travel planner AI.

RULES:
- Provide structured, factual, and actionable travel guidance.
- Do NOT assume user preferences beyond given inputs.
- Do NOT hallucinate unknown facts.
- Keep response concise and readable.
- Output strictly in Markdown format.
- Use bullet points.

FORMAT:
## Overview
## Day-by-Day Plan
## Key Recommendations
## Constraints Consideration
## Tips
"""

def build_user_prompt(destination, days, interests, avoid):
    return f"""
User Inputs:
- Destination: {destination}
- Duration: {days} days
- Interests: {interests}
- Avoid: {avoid}

Generate a structured travel plan following system instructions.
"""

# ============================================
# 5. OpenAI API Interaction with Fallback
# ============================================
def call_openai_with_fallback(system_prompt, user_prompt):
    models = ["gpt-5.3", "gpt-4.1", "gpt-4o-mini"]
    last_exception = None

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
            )

            return {
                "content": response.choices[0].message.content,
                "model": model,
                "usage": getattr(response, "usage", None)
            }

        except Exception as e:
            last_exception = e
            time.sleep(1)

    raise Exception(f"All models failed. Last error: {last_exception}")

# ============================================
# 6. Response Extraction and Validation
# ============================================
def validate_response(content):
    if not content or len(content.strip()) == 0:
        raise ValueError("Empty response from model.")
    return content

# ============================================
# 7. Output Rendering
# ============================================
def render_output(markdown_text):
    st.markdown(markdown_text)

# ============================================
# 8. PDF Generation
# ============================================
def generate_pdf(text):
    file_path = f"/tmp/travel_plan_{int(time.time())}.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []
    for line in text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    return file_path

# ============================================
# 9. Error Handling and Diagnostics
# ============================================
def show_diagnostics():
    with st.expander("Diagnostics"):
        st.write("Model Used:", st.session_state.model_used)
        st.write("Token Usage:", st.session_state.token_usage)
        st.write("Raw Response:")
        st.code(st.session_state.raw_response)

# ============================================
# UI Form
# ============================================
with st.form("travel_form"):
    destination = st.text_input("Provide Destination To Travel")
    days = st.number_input("How many days would you be spending there", min_value=1, max_value=30)
    interests = st.text_area("Provide your interests (museums, food, nightlife, etc.)")
    avoid = st.text_area("Provide things to avoid (less walking, kids friendly, etc.)")

    submitted = st.form_submit_button("Generate Plan")

# ============================================
# Input Validation
# ============================================
if submitted:
    if not destination or not interests:
        st.error("Please fill required fields.")
    else:
        with st.spinner("Generating travel plan..."):
            try:
                system_prompt = build_system_prompt()
                user_prompt = build_user_prompt(destination, days, interests, avoid)

                response = call_openai_with_fallback(system_prompt, user_prompt)
                validated = validate_response(response["content"])

                st.session_state.result = validated
                st.session_state.raw_response = response
                st.session_state.model_used = response["model"]
                st.session_state.token_usage = response["usage"]

                st.success("Plan generated successfully.")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================
# Display Output
# ============================================
if st.session_state.result:
    render_output(st.session_state.result)

    pdf_file = generate_pdf(st.session_state.result)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="Download as PDF",
            data=f,
            file_name="travel_plan.pdf",
            mime="application/pdf"
        )

    show_diagnostics()

# ============================================
# Optional Self-Test
# ============================================
if st.button("Run API Self-Test"):
    try:
        test = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say OK"}]
        )
        st.success("API connection successful.")
    except Exception as e:
        st.error(f"API test failed: {str(e)}")
