# 🛡️ DRISHTI-SHIELD V2
## Professional GEOINT Analysis Platform

### 🎯 Overview
DRISHTI-SHIELD V2 is a cutting-edge satellite intelligence analysis platform designed for professional GEOINT operations. It features advanced AI technologies including SSIM-based change detection, interactive AOI selection, real-time satellite feeds, and comprehensive data fusion capabilities.

### 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Professional  │───▶│   FastAPI V2     │───▶│   Advanced AI   │
│   Frontend      │    │   Backend        │    │   Pipeline      │
│   (Leaflet.js)  │    │                  │    │   (SSIM/ViT)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Interactive AOI │    │ GeoJSON API      │    │ SSIM Detection  │
│ Drawing Tools   │    │ Satellite Layers │    │ Data Fusion     │
│ NASA VIIRS      │    │ Professional UI  │    │ Risk Scoring    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🚀 V2 Features

#### Advanced Backend (FastAPI V2)
- ✅ **AOI Analysis API** - Geographic bounds-based analysis
- ✅ **SSIM Change Detection** - Structural similarity analysis
- ✅ **Data Fusion Engine** - AI detection + change analysis
- ✅ **Professional Reporting** - Military-grade intelligence summaries
- ✅ **GeoJSON Integration** - Precise coordinate mapping
- ✅ **Risk Assessment** - Automated threat scoring
- ✅ **Interactive Documentation** - Swagger UI at `/docs`

#### Professional Frontend (Leaflet.js)
- ✅ **Interactive AOI Selection** - Draw rectangles on map
- ✅ **Real-time Satellite Layer** - NASA VIIRS integration
- ✅ **Professional UI** - Multi-panel military interface
- ✅ **Loading States** - Professional feedback system
- ✅ **Anomaly Mapping** - GeoJSON markers with popups
- ✅ **Intelligence Reports** - Modal-based report viewer
- ✅ **Responsive Design** - Tailwind CSS styling

#### Advanced ML Pipeline
- ✅ **SSIM-based Change Detection** - Structural similarity analysis
- ✅ **Vision Transformer** - Hugging Face object detection
- ✅ **Data Fusion** - Combines detection + change analysis
- ✅ **Risk Scoring Algorithm** - Automated threat assessment
- ✅ **LLM Report Generation** - Contextual intelligence summaries

### 📁 Project Structure

```
DRISHTI-SHIELD/
├── 🛡️ Backend V2 (Python/FastAPI)
│   ├── src/
│   │   ├── pipeline/
│   │   │   ├── object_detection.py     # Vision Transformer
│   │   │   ├── change_detection.py     # SSIM-based analysis
│   │   │   └── report_generator.py     # Enhanced LLM reports
│   │   └── utils/
│   │       └── geo_utils.py            # GeoJSON conversion
│   ├── api_server.py                   # V2 FastAPI server
│   ├── requirements.txt                # Updated dependencies
│   └── venv/                          # Virtual environment
│
├── 🌐 Professional Frontend (Leaflet.js)
│   └── frontend/
│       └── index.html                  # Professional UI
│
├── 📊 Demo Data
│   └── data/
│       ├── dummy_before.png           # Realistic before image
│       └── dummy_after.png            # After image with changes
│
├── 📁 Static Files
│   └── static/                        # Generated change masks
│
└── 🚀 Automation
    └── start_system.sh                # V2 startup script
```

### 🔧 Installation & Setup

#### 1. Backend Setup
```bash
cd DRISHTI-SHIELD
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

#### 2. Start the Backend Server
```bash
python api_server.py
```
Server will start at: **http://127.0.0.1:8000**

#### 3. Open the Frontend
Open `frontend/index.html` in your web browser or use:
```bash
open frontend/index.html
```

### 🎮 V2 Usage Instructions

#### 1. **Select Area of Interest (AOI)**
   - Use the rectangle drawing tool on the map
   - Draw over any geographic region of interest
   - Toggle satellite layer (NASA VIIRS) for context

#### 2. **Analyze AOI** 
   - Click "Analyze Selected AOI" button
   - Watch professional loading animation
   - SSIM-based change detection runs automatically

#### 3. **View Professional Results**
   - **Interactive Map**: GeoJSON anomaly markers with popups
   - **Risk Assessment**: Numerical threat scoring
   - **Key Detections**: Sidebar summary of findings
   - **Full LLM Report**: Modal with detailed intelligence analysis
   - **Change Mask Overlay**: Visual representation of detected changes

### 🛠️ V2 API Endpoints

#### `GET /`
Health check endpoint
```json
{"message": "DRISHTI-SHIELD API is running!", "version": "2.0.0"}
```

#### `POST /api/v1/analyze_aoi`
**NEW V2 Endpoint**: Area of Interest analysis
- **Input**: JSON with AOI bounds
- **Output**: Complete GEOINT analysis

**Request:**
```json
{
    "aoi_bounds": {
        "north_east": {"lat": 28.7041, "lng": 77.1025},
        "south_west": {"lat": 28.5355, "lng": 76.9906}
    }
}
```

**Response:**
```json
{
    "report_summary": "Professional intelligence report...",
    "change_mask_url": "http://127.0.0.1:8000/static/change_mask_latest.png",
    "anomalies_geojson": {
        "type": "FeatureCollection",
        "features": [...]
    },
    "image_bounds": {"north_east": {...}, "south_west": {...}},
    "risk_score": 7.8,
    "fused_data": [...]
}
```

#### `GET /docs`
Interactive API documentation (Swagger UI)

### 🧪 Testing

#### Sample Test Workflow:
1. **Start Backend**: `python api_server.py`
2. **Open Frontend**: Open `frontend/index.html` in browser
3. **Upload Test Images**: Use files from `test_images/` directory
4. **Analyze**: Click analyze button and observe results
5. **Verify**: Check map markers and intelligence report

#### API Testing:
```bash
# Test health endpoint
curl http://127.0.0.1:8000/

# Test analysis endpoint
curl -X POST "http://127.0.0.1:8000/api/v1/analyze" \
     -H "Content-Type: multipart/form-data" \
     -F "image_before=@test_images/satellite_before.png" \
     -F "image_after=@test_images/satellite_after.png"
```

How can we imporove it !! 

#### ✅ **Technical Excellence**
- Modern full-stack architecture (FastAPI + Interactive Web UI)
- Real AI/ML integration (Vision Transformers, Change Detection)
- Professional API design with documentation
- Responsive, military-grade user interface

#### ✅ **Innovation**
- Automated satellite imagery analysis
- LLM-powered intelligence reporting
- Real-time anomaly detection and mapping
- GeoJSON integration for precise coordinate mapping

#### ✅ **Scalability** 
- Modular Python backend architecture
- RESTful API design for integration
- Docker-ready containerization potential
- Cloud deployment ready

#### ✅ **User Experience**
- Intuitive drag-and-drop interface
- Real-time processing feedback
- Interactive map visualization
- Professional military-style reporting

### 🔮 Future Enhancements

#### Phase 2 Features:
- **Real GeoTIFF Support** - Actual satellite image georeferencing
- **Advanced ML Models** - Custom trained Siamese UNet++
- **Multi-spectral Analysis** - Beyond RGB imagery
- **Historical Tracking** - Time-series analysis
- **Alert System** - Automated threat notifications
- **Mobile App** - React Native companion

#### Deployment Options:
- **Cloud Deployment** - AWS/Azure containerized deployment
- **Edge Computing** - On-premises military installation
- **Hybrid Architecture** - Classified/unclassified data separation

### 🏆 Competition Advantages

1. **Complete Working System** - Not just concepts, but functioning software
2. **Modern Tech Stack** - Industry-standard technologies
3. **Defense-Focused** - Specifically designed for military use cases
4. **Scalable Architecture** - Ready for production deployment
5. **Professional UI/UX** - Polished user experience
6. **Comprehensive Documentation** - Complete setup and usage guides

### 📞 Support & Documentation

- **Live Demo**: Open `frontend/index.html` in any modern browser
- **API Docs**: Visit `http://127.0.0.1:8000/docs` when server is running
- **Source Code**: Fully documented Python modules
- **Test Data**: Sample images provided in `test_images/` directory

---

**🛡️ DRISHTI-SHIELD V2 - Professional GEOINT Analysis Platform**

*Built for Smart India Hackathon 2025*
