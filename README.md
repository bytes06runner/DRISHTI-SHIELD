# 🛡️ DRISHTI-SHIELD
## Advanced Satellite Intelligence Analysis System

### 🎯 Overview
DRISHTI-SHIELD is a comprehensive satellite imagery analysis platform designed for the Indian Armed Forces. It leverages cutting-edge AI technologies including Vision Transformers, Change Detection, and Large Language Models to provide real-time intelligence analysis from satellite imagery.

### 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   FastAPI        │───▶│   ML Pipeline   │
│   (HTML/JS/     │    │   Backend        │    │   (PyTorch/     │
│   Leaflet)      │    │                  │    │   Transformers) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Interactive Map │    │ File Processing  │    │ Object Detection│
│ Visualization   │    │ & API Endpoints  │    │ Change Detection│
│                 │    │                  │    │ Report Generation│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🚀 Features

#### Backend (FastAPI)
- ✅ **File Upload API** - Accepts before/after satellite images
- ✅ **ML Pipeline Integration** - Vision Transformer object detection
- ✅ **Change Detection** - Pixel-level change analysis
- ✅ **Intelligence Reporting** - LLM-powered military-style reports
- ✅ **GeoJSON Conversion** - Pixel coordinates to lat/lng mapping
- ✅ **CORS Support** - Cross-origin requests enabled
- ✅ **Interactive Documentation** - Swagger UI at `/docs`

#### Frontend (Interactive Web App)
- ✅ **Drag & Drop Interface** - Easy image upload
- ✅ **Interactive Mapping** - Leaflet.js powered map
- ✅ **Real-time Analysis** - Live processing status
- ✅ **Anomaly Visualization** - Clickable map markers
- ✅ **Military-style UI** - Professional defense interface
- ✅ **Intelligence Reports** - Formatted analysis results

#### ML Pipeline
- ✅ **Vision Transformer** - Hugging Face transformers
- ✅ **Change Detection** - OpenCV-based analysis
- ✅ **Risk Scoring** - Automated threat assessment
- ✅ **Report Generation** - LLM-powered summaries

### 📁 Project Structure

```
DRISHTI-SHIELD/
├── 🛡️ Backend (Python/FastAPI)
│   ├── src/
│   │   ├── pipeline/
│   │   │   ├── object_detection.py     # Vision Transformer
│   │   │   ├── change_detection.py     # Change analysis
│   │   │   └── report_generator.py     # LLM reports
│   │   ├── api/
│   │   │   └── main.py                 # FastAPI routes
│   │   └── utils/
│   │       └── geo_utils.py            # GeoJSON conversion
│   ├── api_server.py                   # Main server file
│   ├── requirements.txt                # Python dependencies
│   └── venv/                          # Virtual environment
│
├── 🌐 Frontend (HTML/CSS/JS)
│   └── index.html                      # Complete web application
│
├── 📊 Test Data
│   └── test_images/
│       ├── satellite_before.png       # Sample before image
│       └── satellite_after.png        # Sample after image
│
└── 📁 Static Files
    └── static/                        # Served assets
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

### 🎮 Usage Instructions

#### 1. **Upload Images**
   - Click "📸 Before Image" to upload the first satellite image
   - Click "📸 After Image" to upload the second satellite image
   - Supported formats: PNG, JPG, JPEG

#### 2. **Analyze Imagery** 
   - Click "🔍 Analyze Imagery" button
   - Wait for processing (3-5 seconds)
   - Watch the status indicator for progress

#### 3. **View Results**
   - **Map View**: Interactive map with anomaly markers
   - **Intelligence Report**: Military-formatted analysis
   - **Risk Score**: Automated threat assessment
   - **Anomaly Details**: Click map markers for details

### 🛠️ API Endpoints

#### `GET /`
Health check endpoint
```json
{"message": "DRISHTI-SHIELD API is running!", "version": "1.0.0"}
```

#### `POST /api/v1/analyze`
Main analysis endpoint
- **Input**: `multipart/form-data` with `image_before` and `image_after`
- **Output**: Complete analysis results

```json
{
    "success": true,
    "report_summary": "Military intelligence report...",
    "change_mask_url": "/static/change_mask_demo.png",
    "anomalies_geojson": {
        "type": "FeatureCollection",
        "features": [...]
    },
    "image_bounds": [[40.712, -74.227], [40.774, -74.125]],
    "risk_score": 9.2,
    "processing_time": "3.4s"
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

### 🎯 SIH Demonstration Points

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

**🛡️ DRISHTI-SHIELD - Empowering National Security Through AI**

*Built for Smart India Hackathon 2025*
