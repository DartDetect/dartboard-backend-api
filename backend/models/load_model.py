import os
import torch

# Absolute paths for the YOLOv5 directory and the trained model file
YOLOV5_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../yolov5")) # Path to YOLOv5 repo
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "best.pt")) # Path to trained model file

def load_yolov5_model():
  
    print(f"✅ Loading YOLOv5 from: {YOLOV5_PATH}")  
    print(f"✅ Loading model from: {MODEL_PATH}")

    try:
        model = torch.hub.load(YOLOV5_PATH, 'custom', path=MODEL_PATH, source='local', force_reload=True)    
        model.eval()
        print("✅ Model loaded successfully!")
        return model

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None