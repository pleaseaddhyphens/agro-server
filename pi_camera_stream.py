import subprocess
from picamera2 import Picamera2
import time

def start_streaming(windows_ip):
    # Initialize camera
    picam = Picamera2()
    config = picam.create_video_configuration(
        main={"size": (1280, 720)},
        controls={"FrameRate": 30}
    )
    picam.configure(config)
    picam.start()

    # Start streaming to Windows PC
    gst_command = (
        f'gst-launch-1.0 -v v4l2src device=/dev/video0 ! '
        f'video/x-raw,width=1280,height=720,framerate=30/1 ! '
        f'videoconvert ! x264enc tune=zerolatency ! '
        f'rtph264pay ! udpsink host={windows_ip} port=8554'
    )
    
    try:
        process = subprocess.Popen(gst_command, shell=True)
        print(f"Streaming to {windows_ip}:8554")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()
        picam.stop()

if __name__ == "__main__":
    WINDOWS_IP = "192.168.1.100"  # Replace with your Windows PC's IP
    start_streaming(WINDOWS_IP) 