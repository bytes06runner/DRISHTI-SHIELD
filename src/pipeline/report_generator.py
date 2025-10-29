import json
import os
from openai import OpenAI # Using OpenAI as an example, can be any LLM

# It's best practice to load the API key from environment variables
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_intelligence_summary(report_context: dict, risk_score: float) -> str:
    """
    Generates a natural language summary from the richer V2 context.

    Args:
        report_context (dict): Structured JSON from the API.
        risk_score (float): The calculated risk score.

    Returns:
        str: A human-readable intelligence report.
    """
    
    # The system prompt sets the LLM's persona
    system_prompt = f"""
    You are DRISHTI-SHIELD, an AI Intelligence Analyst (Tier 2) for the Indian Armed Forces.
    Your mission is to provide a concise, factual, and actionable summary
    of satellite imagery analysis from a user-defined Area of Interest (AOI).
    
    Input data is a JSON object containing AOI coordinates, a list of detected
    anomalies (fused from ViT and change detection), and a risk score.
    
    Format your response in 3 sections:
    1. **BLUF (Bottom Line Up Front):** A single-sentence summary of the most critical finding.
    2. **Detailed Analysis:** A bulleted list of significant changes, referencing their class.
       Mention the *number* of new anomalies.
    3. **Analyst Recommendation:** A single, actionable recommendation.
    
    Be formal, precise, and use military-style language.
    """
    
    # The user prompt contains the data
    user_prompt = f"Analyze the following data and generate the report:\n\n{json.dumps(report_context, indent=2)}"

    try:
        # --- SIMULATED LLM CALL ---
        # In a real app, you'd make the API call here:
        # response = client.chat.completions.create(...)
        # return response.choices[0].message.content
        
        print("[LLM] Generating simulated report...")
        
        # Build a placeholder report from the context
        num_anomalies = len(report_context.get("detected_anomalies", []))
        aoi = report_context.get("aoi_coordinates", {})
        
        bluf = f"**BLUF (Bottom Line Up Front):** AI analysis of AOI [Lat: {aoi.get('south_west',{}).get('lat'):.4f}, Lng: {aoi.get('south_west',{}).get('lng'):.4f}] has identified {num_anomalies} high-confidence anomalies, indicating new activity."

        details = "**Detailed Analysis:**\n"
        if num_anomalies == 0:
            details += "* No significant changes or new objects detected in the specified AOI.\n"
        else:
            classes = [d.get('class') for d in report_context.get("detected_anomalies")]
            unique_classes = ", ".join(list(set(classes)))
            details += f"* A total of {num_anomalies} new anomalies were detected.\n"
            details += f"* Object classes include: {unique_classes}.\n"
            details += f"* Structural Similarity Score of {report_context.get('overall_ssim_score', 0):.2f} indicates moderate to high temporal change."

        rec = "**Analyst Recommendation:**\n"
        if risk_score > 7.0:
            rec += "* HIGH PRIORITY: Escalate to Tier 3 Analyst for immediate review. Correlate with regional SIGINT."
        elif risk_score > 4.0:
            rec += "* MEDIUM PRIORITY: Log detections and schedule for review by regional desk. Monitor AOI for 72 hours."
        else:
            rec += "* LOW PRIORITY: Logged. No immediate action required."

        return f"{bluf}\n\n{details}\n\n{rec}"

    except Exception as e:
        print(f"[Error] LLM report generation failed: {e}")
        return "ERROR: Failed to generate intelligence report."

if __name__ == "__main__":
    # Example data from the fusion step
    mock_fused_data = [
        {"type": "new_object", "class": "vehicle_convoy", "count": 12, "location": "Sector 4B"},
        {"type": "structure_change", "class": "building", "area_sq_m": 500, "location": "Sector 4B"},
    ]
    mock_risk_score = 9.2
    
    report = generate_intelligence_summary(mock_fused_data, mock_risk_score)
    print("\n--- GENERATED INTELLIGENCE REPORT ---")
    print(report)
