# core/pipeline.py
import json
import os
import pickle
import numpy as np

# Mock loss table until P2 finishes the real one on Day 8
MOCK_LOSS_FACTORS = {
    "Potato___healthy": 0.0,
    "Potato___Early_blight": 0.25,  # Max 25% yield loss at 100% severity
    "Potato___Late_blight": 0.65,   # Max 65% yield loss at 100% severity
}

def calculate_adjusted_yield(baseline_yield: float, disease_class: str, severity_pct: float) -> dict:
    """Combines LSTM baseline yield + CNN disease + OpenCV severity."""
    loss_factor = MOCK_LOSS_FACTORS.get(disease_class, 0.20)
    # Effective loss scales with how much of the leaf is affected (severity_pct)
    effective_loss_ratio = loss_factor * (severity_pct / 100.0)
    expected_loss_tons = baseline_yield * effective_loss_ratio
    adjusted_yield = baseline_yield - expected_loss_tons
    
    return {
        "loss_factor": loss_factor,
        "effective_loss_pct": round(effective_loss_ratio * 100, 2),
        "expected_loss_tons": round(expected_loss_tons, 2),
        "adjusted_yield_tons": round(adjusted_yield, 2)
    }

def predict_action_and_explain(disease_class: str, severity_pct: float, effective_loss_pct: float) -> dict:
    """
    Placeholder rule/tree prediction + Day 7 'Why this decision' explanation.
    Once your Scikit-Learn DecisionTreeClassifier is trained on Day 9, 
    replace the if/else with `tree_model.predict(...)`.
    """
    if "healthy" in disease_class.lower() or severity_pct < 5.0:
        action = "No Action (Monitor)"
        urgency = "Green"
        reason = (
            f"Crop appears healthy or infection is negligible ({severity_pct}% severity). "
            f"Projected yield loss is minimal ({effective_loss_pct}%)."
        )
    elif severity_pct < 25.0 and effective_loss_pct < 15.0:
        action = "Targeted Organic / Preventive Spray"
        urgency = "Orange"
        reason = (
            f"Detected {disease_class} at moderate severity ({severity_pct}%). "
            f"Estimated yield loss is {effective_loss_pct}%. Localized treatment prevents spread."
        )
    else:
        action = "Immediate Fungicide Intervention"
        urgency = "Red"
        reason = (
            f"CRITICAL: High severity ({severity_pct}%) of {disease_class} detected! "
            f"Unchecked, this risks {effective_loss_pct}% yield loss. Immediate action required."
        )

    return {
        "decision": action,
        "status_color": urgency,
        "explanation": reason
    }

def run_full_pipeline(zone_data: dict) -> list:
    """Runs the pipeline across all 25 zones of the 5x5 grid."""
    crop = zone_data.get("crop_type", "Unknown")
    baseline_yield = zone_data.get("baseline_yield_tons_per_ha", 20.0)
    results = []

    for zone in zone_data.get("zones", []):
        yield_info = calculate_adjusted_yield(
            baseline_yield=baseline_yield,
            disease_class=zone["disease_class"],
            severity_pct=zone["severity_pct"]
        )
        decision_info = predict_action_and_explain(
            disease_class=zone["disease_class"],
            severity_pct=zone["severity_pct"],
            effective_loss_pct=yield_info["effective_loss_pct"]
        )
        results.append({
            **zone,
            "crop_type": crop,
            "baseline_yield": baseline_yield,
            **yield_info,
            **decision_info
        })
    return results