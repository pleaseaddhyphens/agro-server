# Video Processing Server

A real-time video processing server that receives video streams from Raspberry Pi and processes frames using OpenCV.

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/video-processing-project
cd video-processing-project
```

2. Build and run using Docker Compose:
```bash
docker-compose up --build
```

The server will be available at:
- Web interface: http://localhost:5000
- Video stream endpoint: udp://localhost:8554

## Manual Setup

### Prerequisites

- Python 3.9+
- GStreamer (for video streaming)
- OpenCV dependencies

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python src/video_processing_server.py
```

## Raspberry Pi Setup

1. Install required packages:
```bash
sudo apt-get update
sudo apt-get install -y \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    python3-picamera2
```

2. Run the streaming script:
```bash
python src/pi_camera_stream.py
```

## Configuration

Edit `config.py` to modify:
- Processing parameters
- Video quality settings
- Storage locations
- Network ports

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Troubleshooting

1. If the stream doesn't connect:
   - Check firewall settings
   - Verify network connectivity
   - Ensure correct IP addresses

2. If frames are dropping:
   - Reduce resolution/framerate
   - Check network bandwidth
   - Monitor system resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 