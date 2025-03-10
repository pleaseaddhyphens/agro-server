# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Install system dependencies including GStreamer
RUN apt-get update && apt-get install -y \
    libgstreamer1.0-0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    libgstreamer-plugins-base1.0-0 \
    python3-gst-1.0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports
EXPOSE 5000
EXPOSE 8554/udp

# Command to run the server
CMD ["python", "video_processing_server.py"] 