from load_model import load_yolov5_model
import torch

try:
    #Load yolov5 model
    model = load_yolov5_model()
    if model is not None:
         # Check for GPU availability and assign to device if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Move model to GPU or CPU
        model.to(device)
        print("✅ Model loaded successfully and moved to:", device)
    else:
        print("❌ Model failed to load.")
except Exception as e: # Catch any errors
    print(f"❌ Error during model testing: {e}")
