# app/pages/2_Map.py
import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Field Map Dashboard", page_icon="🗺️", layout="wide")
st.title("🗺️ 5×5 Field Map & Decision Dashboard")

# 1. Load Fake P2 Data (LSTM)
with open("data/mock/fake_lstm_output.json", "r") as f:
    lstm_data = json.load(f)

# 2. Load Fake P1 Data (CNN 25 Zones)
with open("data/mock/fake_cnn_zones.json", "r") as f:
    zones_data = json.load(f)

# Top Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Selected Crop", lstm_data["crop_type"])
col2.metric("Baseline Predicted Yield (LSTM)", f"{lstm_data['predicted_yield']} t/ha")
col3.metric("Total Field Zones", len(zones_data))

st.divider()

# Skeleton Preview of the 5x5 Grid (We will add pipeline & colors on Day 3 & Day 5)
st.subheader("📋 Raw Zone Data Preview (From Fake JSON)")
df_zones = pd.DataFrame(zones_data)
st.dataframe(df_zones, use_container_width=True)