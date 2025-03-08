import cv2
import os

def test_opencv():
    print("OpenCV version:", cv2.__version__)
    
    # Test video capture
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("Successfully opened video capture")
        cap.release()
    else:
        print("Failed to open video capture")

def test_gstreamer():
    # Check if GStreamer is in PATH
    gst_path = os.environ.get('PATH').lower()
    if 'gstreamer' in gst_path:
        print("GStreamer found in PATH")
    else:
        print("Warning: GStreamer not found in PATH")

if __name__ == "__main__":
    test_opencv()
    test_gstreamer() 