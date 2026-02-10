import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
from rich.console import Console

console = Console()

class FaceTracker:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'detector.tflite')
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.detector = vision.FaceDetector.create_from_options(options)

    def get_face_data(self, frame):
        """Returns normalized (center_x, center_y, scale) of the face."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = self.detector.detect(mp_image)
        
        if not detection_result.detections:
            return 0.5, 0.5, 1.0
            
        detection = detection_result.detections[0]
        bbox = detection.bounding_box
        h, w, _ = frame.shape
        
        center_x = (bbox.origin_x + bbox.width / 2) / w
        center_y = (bbox.origin_y + bbox.height / 2) / h
        # Scale is relative to the frame height (how much of the screen the face takes)
        scale = bbox.height / h
        
        return center_x, center_y, scale

    def analyze_motion_path(self, video_path):
        """
        Generates a frame-by-frame path for the camera to follow.
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        path = []
        frame_idx = 0
        
        console.print(f'[bold blue]Extracting premium motion path ({total_frames} frames)...[/bold blue]')
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample every 2nd frame for speed, interpolate later
            if frame_idx % 2 == 0:
                last_pos = self.get_face_data(frame)
                path.append(last_pos)
            else:
                path.append(path[-1] if path else (0.5, 0.5, 1.0))
            
            frame_idx += 1
        cap.release()
        
        if not path:
            return np.array([[0.5, 0.5, 1.0]])

        # SMOOTHING
        path = np.array(path)
        smoothed_path = np.copy(path)
        
        # Adjust window size based on path length to avoid broadcast errors
        window = min(int(fps), len(path))
        if window < 1: window = 1
        
        for i in range(3):
            # Ensure window is odd for centered 'same' mode or handle small paths
            kernel = np.ones(window)/window
            smoothed_path[:, i] = np.convolve(path[:, i], kernel, mode='same')
            
        return smoothed_path