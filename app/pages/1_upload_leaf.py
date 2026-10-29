# app/pages/2_Field_Map_Dashboard.py
import streamlit as st
import random
from core.pipeline import run_full_pipeline

st.set_page_config(page_title="5x5 Field Map Dashboard", layout="wide")
st.title("🚜 Smart Agriculture — 5×5 Field Decision Map")

# Generate 25 fake zones if real CNN output isn't connected yet
def generate_mock_25_zones():
    classes = [
        ("Potato___healthy", 0.0, 3.0),
        ("Potato___Early_blight", 10.0, 30.0),
        ("Potato___Late_blight", 25.0, 70.0)
    ]
    zones = []
    for r in range(5):
        for c in range(5):
            cls, min_s, max_s = random.choices(classes, weights=[0.5, 0.3, 0.2])[0]
            zones.append({
                "zone_id": f"Z_{r}_{c}",
                "row": r,
                "col": c,
                "disease_class": cls,
                "cnn_confidence": round(random.uniform(0.85, 0.99), 2),
                "severity_pct": round(random.uniform(min_s, max_s), 1)
            })
    return {
        "crop_type": "Potato",
        "baseline_yield_tons_per_ha": 28.5,
        "zones": zones
    }

mock_input = generate_mock_25_zones()
processed_zones = run_full_pipeline(mock_input)

st.markdown(f"**Crop:** `{mock_input['crop_type']}` | **LSTM Baseline Yield:** `{mock_input['baseline_yield_tons_per_ha']} t/ha`")

# Color mapping for zones
COLOR_HEX = {
    "Green": "#2ecc71",
    "Orange": "#f39c12",
    "Red": "#e74c3c"
}

st.subheader("🗺️ 5×5 Field Grid Status")
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        idx = r * 5 + c
        z = processed_zones[idx]
        bg_color = COLOR_HEX[z["status_color"]]
        with cols[c]:
            st.markdown(
                f"""
                <div style="background-color:{bg_color}; padding:12px; border-radius:8px; color:white; text-align:center; margin-bottom:10px;">
                    <strong>{z['zone_id']}</strong><br>
                    <span style="font-size:12px;">{z['disease_class'].replace('Potato___', '')}</span><br>
                    <strong>Sev: {z['severity_pct']}%</strong><br>
                    <span style="font-size:11px;">Yield: {z['adjusted_yield_tons']} t/ha</span>
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()
st.subheader("🔍 Zone Decision & Explanation Inspector")
selected_zone_id = st.selectbox("Select a Zone to inspect:", [z["zone_id"] for z in processed_zones])
selected_zone = next(z for z in processed_zones if z["zone_id"] == selected_zone_id)

col1, col2 = st.columns(2)
with col1:
    st.metric("Recommended Decision", selected_zone["decision"])
    st.write(f"**Disease Detected:** {selected_zone['disease_class']} ({int(selected_zone['cnn_confidence']*100)}% conf)")
    st.write(f"**Leaf Severity (OpenCV):** {selected_zone['severity_pct']}%")
with col2:
    st.metric("Adjusted Yield Forecast", f"{selected_zone['adjusted_yield_tons']} t/ha", f"-{selected_zone['expected_loss_tons']} t/ha ({selected_zone['effective_loss_pct']}%)")
    st.info(f"**Why this decision?**\n\n{selected_zone['explanation']}")