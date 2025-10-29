#!/bin/bash

#!/bin/bash

# DRISHTI-SHIELD V2 System Startup Script
# Professional GEOINT Analysis Platform

set -e  # Exit on any error

echo "🛡️  Starting DRISHTI-SHIELD V2 System..."

# Function to check if server is running
check_server() {
    curl -s http://127.0.0.1:8000/ > /dev/null 2>&1
}

# Function to stop existing server
stop_server() {
    echo "🔄 Stopping existing server processes..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "   No existing processes on port 8000"
    sleep 2
}

# Stop any existing server
stop_server

# Start the V2 API server in background
echo "🚀 Starting DRISHTI-SHIELD V2 API Server..."
/Users/srijeetbanerjee/DS_FINAL/DRISHTI-SHIELD/venv/bin/python /Users/srijeetbanerjee/DS_FINAL/DRISHTI-SHIELD/api_server.py &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to initialize..."
for i in {1..15}; do
    if check_server; then
        echo "✅ Server is ready!"
        break
    fi
    if [ $i -eq 15 ]; then
        echo "❌ Server failed to start within 15 seconds"
        kill $SERVER_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Open the V2 frontend in default browser
echo "🌐 Opening DRISHTI-SHIELD V2 Professional Interface..."
open frontend/index.html

echo ""
echo "🎯 DRISHTI-SHIELD V2 System Status:"
echo "   ✅ API Server: Running (PID: $SERVER_PID)"
echo "   ✅ Professional Frontend: Opened in browser"
echo "   📍 Server URL: http://127.0.0.1:8000"
echo "   📋 API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "🔬 V2 Features Active:"
echo "   • Advanced SSIM Change Detection"
echo "   • Interactive AOI Selection"
echo "   • Real-time Satellite Layer (NASA VIIRS)"
echo "   • Professional GEOINT Interface"
echo "   • Smarter AI Pipeline with Data Fusion"
echo ""
echo "🛑 To stop the system: kill $SERVER_PID"
echo "💡 V2 System ready for Smart India Hackathon demonstration!"
