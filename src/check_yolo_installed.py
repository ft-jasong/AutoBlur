try:
    import torch
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    print("YOLOv5 is installed.")
except ImportError:
    print("YOLOv5 is not installed.")
