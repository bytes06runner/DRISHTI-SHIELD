"""
DRISHTI-SHIELD API Server V2
Professional GEOINT Analysis Platform
"""

import os
import shutil
import cv2
import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any

# Import our pipeline modules
from src.pipeline.report_generator import generate_intelligence_summary
from src.utils.geo_utils import convert_pixels_to_geojson
from src.pipeline.change_detection import advanced_change_detection

# Define request/response models
class AoiBounds(BaseModel):
    north_east: Dict[str, float]  # {lat, lng}
    south_west: Dict[str, float]  # {lat, lng}

class AnalysisRequest(BaseModel):
    aoi_bounds: AoiBounds

# Create FastAPI App
app = FastAPI(title="DRISHTI-SHIELD API", version="2.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static File Server
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "DRISHTI-SHIELD API is running!", "version": "2.0.0"}


@app.post("/api/v1/analyze_aoi")
async def analyze_area_of_interest(request: AnalysisRequest):
    """
    The main V2 analysis endpoint. Receives Lat/Lng bounds,
    simulates image fetching, runs the pipeline, and returns GeoJSON.
    """
    try:
        aoi_bounds = request.aoi_bounds
        print(f"[API] Received analysis request for AOI: {aoi_bounds}")

        # --- 1. SIMULATE IMAGE FETCHING ---
        # In a real system, you'd use these bounds to query a service
        # (like Sentinel Hub or Google Earth Engine) to get "before"
        # and "after" GeoTIFF images for this *exact* AOI.
        
        # For our demo, we'll just use our dummy files.
        # These are now *assumed* to be the images for the requested AOI.
        before_path = "data/dummy_before.png"
        after_path = "data/dummy_after.png"
        
        if not os.path.exists(before_path) or not os.path.exists(after_path):
            raise HTTPException(status_code=500, detail="Demo images not found.")

        img_before = cv2.imread(before_path)
        img_after = cv2.imread(after_path)
        
        # Get image dimensions (H, W, C)
        image_height, image_width, _ = img_before.shape
        image_dims = (image_height, image_width)

        # --- 2. Run Upgraded ML Pipeline ---
        print("[API] Running advanced change detection...")
        # This new function is much smarter than cv2.absdiff
        change_mask, ssim_score = advanced_change_detection(before_path, after_path)
        
        # Save the mask so the frontend can fetch it
        mask_filename = "change_mask_latest.png"
        mask_save_path = f"static/{mask_filename}"
        cv2.imwrite(mask_save_path, change_mask)
        
        # URL for the frontend to access
        change_mask_url = f"http://127.0.0.1:8000/static/{mask_filename}"
        
        print("[API] Running object detection (Simulated)...")
        # In a real system, you'd run your ViT model here on img_after
        # For now, we'll mock the *output* of the ViT model
        mock_detections = [
            {"bbox_pixels": [100, 100, 150, 150], "class": "Vehicle", "confidence": 0.95},
            {"bbox_pixels": [300, 300, 400, 400], "class": "New Structure", "confidence": 0.88},
            {"bbox_pixels": [50, 400, 80, 430], "class": "Vehicle", "confidence": 0.91},
        ]

        # --- 3. Run Fusion & Risk Scoring ---
        print("[API] Fusing data and scoring risk...")
        # We'll fuse our mock ViT detections with our *real* change mask
        fused_data = []
        for det in mock_detections:
            x1, y1, x2, y2 = det["bbox_pixels"]
            # Check the *center* of the detected object
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            
            # Check if this pixel is "changed" in our mask
            if change_mask[cy, cx] == 255:
                det["type"] = "New Anomaly"
                fused_data.append(det)
            else:
                det["type"] = "Existing Object"
                # You could choose to ignore existing objects
                # fused_data.append(det) 

        # Calculate a simple risk score
        risk_score = (len(fused_data) * 3.0) + (1 - ssim_score) * 10.0
        risk_score = min(max(risk_score, 0), 10)  # Clamp between 0-10

        # --- 4. Convert Pixels to GeoJSON ---
        print("[API] Converting pixel coordinates to GeoJSON...")
        # This is now a critical function.
        anomalies_geojson = convert_pixels_to_geojson(
            fused_data, 
            aoi_bounds.dict(), 
            image_dims
        )

        # --- 5. Generate LLM Report ---
        print("[API] Generating final report...")
        # Create a richer context object for the LLM
        report_context = {
            "aoi_coordinates": aoi_bounds.dict(),
            "detected_anomalies": fused_data,
            "overall_ssim_score": ssim_score,
            "risk_score": risk_score
        }
        report_text = generate_intelligence_summary(report_context, risk_score)

        # --- 6. Send Response to Frontend ---
        print("[API] Analysis complete. Sending response.")
        return {
            "report_summary": report_text,
            "change_mask_url": change_mask_url,
            "anomalies_geojson": anomalies_geojson,
            "image_bounds": aoi_bounds.dict(),
            "risk_score": risk_score,
            "fused_data": fused_data
        }

    except Exception as e:
        print(f"[API Error] {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("--- Starting DRISHTI-SHIELD API v2 on http://127.0.0.1:8000 ---")
    # Ensure you have 'data/dummy_before.png' and 'data/dummy_after.png'
    uvicorn.run(app, host="127.0.0.1", port=8000)
