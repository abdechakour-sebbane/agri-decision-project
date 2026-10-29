# app/Home.py
import streamlit as st

st.set_page_config(
    page_title="Smart Agri Decision System",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Smart Agriculture Decision Support System")
st.markdown("""
Welcome to our Precision Agriculture platform. This system combines computer vision, 
time-series forecasting, and decision trees to help farmers take action on crop diseases.

### 👈 Select a page in the sidebar to begin:
1. **Upload Leaf (P1):** Upload a single leaf image to detect disease and leaf damage severity.
2. **Field Map Dashboard (P3):** View the 5×5 field simulation, yield impact, and recommended actions.
""")

st.info("System Status: Running in Phase 1 Skeleton Mode (Mock Data Active)")