from flask import Flask, request, send_file, render_template_string
import cv2
import numpy as np
from PIL import Image
import io
import socket

app = Flask(__name__)

# HTML template for the index page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Processing Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .status {
            color: green;
            font-weight: bold;
        }
        code {
            background-color: #e0e0e0;
            padding: 2px 5px;
            border-radius: 3px;
        }
        form {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Image Processing Server</h1>
    
    <div class="container">
        <h2>Server Status</h2>
        <p class="status">✅ Server is running</p>
        <p>Server IP: <code>{{ server_ip }}</code></p>
        <p>Server Port: <code>5000</code></p>
    </div>

    <div class="container">
        <h2>Test Image Processing</h2>
        <form action="/process_image" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Process Image</button>
        </form>
    </div>

    <div class="container">
        <h2>API Usage</h2>
        <p>To process images programmatically, send a POST request to:</p>
        <code>http://{{ server_ip }}:5000/process_image</code>
        <p>Example using curl:</p>
        <code>curl -X POST -F "image=@your_image.jpg" http://{{ server_ip }}:5000/process_image > processed_image.png</code>
    </div>
</body>
</html>
"""

def get_local_ip():
    try:
        # Get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def process_image(image):
    # This is a sample image processing function
    # Here we're just converting to grayscale, but you can add your own processing
    img_array = np.array(image)
    processed = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    return Image.fromarray(processed)

@app.route('/')
def index():
    server_ip = get_local_ip()
    return render_template_string(HTML_TEMPLATE, server_ip=server_ip)

@app.route('/process_image', methods=['POST'])
def handle_image():
    if 'image' not in request.files:
        return 'No image file provided', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    # Read and process the image
    img = Image.open(file.stream)
    processed_img = process_image(img)
    
    # Convert processed image to bytes
    img_byte_arr = io.BytesIO()
    processed_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    # Run the server on your local network
    # '0.0.0.0' allows connections from other devices on the network
    app.run(host='0.0.0.0', port=5000, debug=True) 