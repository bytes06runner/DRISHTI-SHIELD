import os
import sys
import shutil
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Add the project root to Python path to import modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Import your pipeline functions
try:
    from src.pipeline.object_detection import detect_objects
    from src.pipeline.change_detection import detect_changes
    from src.pipeline.report_generator import generate_intelligence_summary
    from src.utils.geo_utils import convert_to_geojson
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports with absolute paths
    import importlib.util
    
    # Load modules manually if needed
    def load_module(module_path, module_name):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- IMPORTANT: Add CORS middleware ---
# This allows your React frontend (on a different URL)
# to make requests to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for a hackathon)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "DRISHTI-SHIELD API is running!"}

@app.post("/api/v1/analyze")
async def analyze_imagery(
    image_before: UploadFile = File(...),
    image_after: UploadFile = File(...)
):
    """
    The main analysis endpoint. Receives "before" and "after" images,
    runs the full pipeline, and returns a JSON report.
    """
    try:
        # Ensure upload directory exists
        os.makedirs("data/uploads", exist_ok=True)
        os.makedirs("static", exist_ok=True)
        
        # Save uploaded files temporarily
        # (In production, you'd use a unique ID)
        before_path = "data/uploads/before.png"
        after_path = "data/uploads/after.png"
        
        with open(before_path, "wb") as buffer:
            shutil.copyfileobj(image_before.file, buffer)
        with open(after_path, "wb") as buffer:
            shutil.copyfileobj(image_after.file, buffer)

        # --- 1. Run the ML Pipeline ---
        print("[API] Running change detection...")
        change_mask_array = detect_changes(before_path, after_path)
        
        # Save the change mask as an image file
        change_mask_path = "static/change_mask.png"
        cv2.imwrite(change_mask_path, change_mask_array)
        change_mask_url = "/static/change_mask.png"
        
        print("[API] Running object detection...")
        detections = detect_objects(after_path) # Your ViT model

        # --- 2. Run Fusion & Risk Scoring ---
        # This is where you combine detections and changes
        # (This is your fusion logic from the blueprint)
        fused_data = [
            {"type": "new_object", "class": "vehicle", "count": 12, "bbox_pixels": [100, 100, 150, 150]},
            {"type": "new_structure", "class": "building", "area_pixels": 500, "bbox_pixels": [300, 300, 400, 400]}
        ]
        mock_risk_score = 9.2 # Placeholder

        # --- 3. CRITICAL UPGRADE: Convert to GeoJSON ---
        print("[API] Converting pixel coordinates to GeoJSON...")
        # We need the original image's geo-reference (lat/lng bounds)
        # For a demo, we can mock this.
        image_bounds_latlng = [[40.712, -74.227], [40.774, -74.125]] # Mock bounds (NYC area)
        anomalies_geojson = convert_to_geojson(fused_data, image_bounds_latlng)

        # --- 4. Generate LLM Report ---
        print("[API] Generating final report...")
        report_text = generate_intelligence_summary(fused_data, mock_risk_score)

        # --- 5. Send Response to Frontend ---
        return {
            "report_summary": report_text,
            "change_mask_url": change_mask_url,
            "anomalies_geojson": anomalies_geojson,
            "image_bounds": image_bounds_latlng, # Tell frontend where to draw the map
            "detections": detections,  # Include raw detection results
            "risk_score": mock_risk_score
        }

    except Exception as e:
        print(f"[API Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # This runs the backend server
    uvicorn.run(app, host="127.0.0.1", port=8000)
