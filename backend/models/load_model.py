import torch

def load_yolov5_model(model_path='backend/models/best.pt'):
    # Load the YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, source='local')
    model.eval()
    return model
