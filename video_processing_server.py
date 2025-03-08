import cv2
import numpy as np
from flask import Flask, render_template_string
import threading
import socket
import time
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Processing Server (Windows)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .status { padding: 10px; background-color: #e0e0e0; border-radius: 5px; }
        .log { 
            background-color: #f5f5f5; 
            padding: 10px; 
            border-radius: 5px;
            margin-top: 20px;
            height: 200px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Video Processing Server</h1>
        <div class="status">
            <p>Server Status: Running</p>
            <p>Server IP: {{ server_ip }}</p>
            <p>Processing rate: <span id="fps">0</span> FPS</p>
        </div>
        <div class="log" id="logArea">
            <h3>Processing Log:</h3>
            <div id="logContent"></div>
        </div>
    </div>
    
    <script>
        // Simple logging display
        function addLog(message) {
            const logContent = document.getElementById('logContent');
            const time = new Date().toLocaleTimeString();
            logContent.innerHTML += `<div>[${time}] ${message}</div>`;
            logContent.scrollTop = logContent.scrollHeight;
        }
    </script>
</body>
</html>
"""

class VideoProcessor:
    def __init__(self, save_path="processed_frames"):
        self.processing = False
        self.frame_count = 0
        self.last_time = time.time()
        self.save_path = save_path
        
        # Create directory for processed frames if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def process_frame(self, frame):
        # Basic image processing example
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply some blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Edge detection
        edges = cv2.Canny(blurred, 100, 200)
        
        return edges

    def start_processing(self):
        self.processing = True
        
        # Use OpenCV's VideoCapture for RTSP stream
        stream_url = "udp://0.0.0.0:8554"
        cap = cv2.VideoCapture(stream_url)
        
        print(f"Starting video processing on {stream_url}")
        
        while self.processing:
            ret, frame = cap.read()
            if not ret:
                print("No frame received. Waiting...")
                time.sleep(0.1)
                continue

            # Process frame
            processed_frame = self.process_frame(frame)

            # Save processed frame (optional)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            frame_path = os.path.join(self.save_path, f"processed_{timestamp}.jpg")
            cv2.imwrite(frame_path, processed_frame)

            # Calculate and print FPS
            self.frame_count += 1
            if time.time() - self.last_time >= 1:
                fps = self.frame_count
                print(f"Processing at {fps} FPS")
                self.frame_count = 0
                self.last_time = time.time()

        cap.release()

    def stop_processing(self):
        self.processing = False

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, server_ip=get_local_ip())

def start_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Start web interface in separate thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start video processing
    processor = VideoProcessor()
    try:
        processor.start_processing()
    except KeyboardInterrupt:
        processor.stop_processing() 