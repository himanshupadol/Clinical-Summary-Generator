import streamlit as st
import time

# Manually add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import generate_summary_for_patient

st.set_page_config(page_title="Clinical Summary Generator", layout="wide")
st.title("🩺 Clinical Summary Generator")

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("Patient Input")
    patient_id = st.text_input("Enter Patient ID", placeholder="e.g. P12345")
    generate_btn = st.button("Generate Summary")

with right_col:
    st.subheader("Clinical Summary")
    summary_placeholder = st.empty()
    status_text = st.empty() # [cite: 6]

if generate_btn:
    if not patient_id.strip():
        st.warning("Please enter a valid patient ID.")
    else:
        try:
            with st.spinner("Processing request via API..."):
                # [cite: 7, 8] The data is built locally, then summary is fetched from cloud
                summary = generate_summary_for_patient(patient_id)
                
            summary_placeholder.markdown(
                f'<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; white-space: pre-wrap;">{summary}</div>',
                unsafe_allow_html=True # [cite: 10]
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")
