# data/mock/generate_mock_data.py
import json
import random
import os

# Ensure we save inside data/mock/
os.makedirs("data/mock", exist_ok=True)

# 1. Fake P2 Output: LSTM Baseline Yield & Loss Factors
# Loss factor = maximum fraction of yield lost if severity reaches 100%
fake_lstm_and_loss = {
    "crop_type": "Potato",
    "predicted_yield": 28.5,  # Tons per hectare (if healthy)
    "loss_factors": {
        "Potato___healthy": 0.0,
        "Potato___Early_blight": 0.30,  # Up to 30% yield loss
        "Potato___Late_blight": 0.70    # Up to 70% yield loss
    }
}

with open("data/mock/fake_lstm_output.json", "w") as f:
    json.dump(fake_lstm_and_loss, f, indent=4)

# 2. Fake P1 Output: 25 Zones (5x5 Grid) from CNN + OpenCV Severity
random.seed(42)  # Fixed seed so you get the same testable grid every time
disease_options = [
    ("Potato___healthy", 0.0, 2.0),         # Healthy leaves have near 0% severity
    ("Potato___Early_blight", 8.0, 35.0),   # Moderate severity range
    ("Potato___Late_blight", 25.0, 75.0)    # High severity range
]

zones = []
for row in range(5):
    for col in range(5):
        # Pick a random state (60% chance healthy, 25% early blight, 15% late blight)
        disease, min_sev, max_sev = random.choices(
            disease_options, weights=[0.60, 0.25, 0.15]
        )[0]
        
        zones.append({
            "zone_id": f"Z_{row}_{col}",
            "row": row,
            "col": col,
            "disease_class": disease,
            "confidence": round(random.uniform(0.82, 0.99), 2),
            "severity_pct": round(random.uniform(min_sev, max_sev), 1)
        })

with open("data/mock/fake_cnn_zones.json", "w") as f:
    json.dump(zones, f, indent=4)

print("Success! Created fake_lstm_output.json and fake_cnn_zones.json in data/mock/")