import os
import torch
import cv2

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
CLOTHES_MODEL_DIR = os.path.join(CUR_DIR, '../checkpoint/')

class Clothes:
    clothes_model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join(CLOTHES_MODEL_DIR, 'new_best.pt'))
    clothes_model.conf = 0.5
    clothes_model.iou = 0.5
    
    def detect_from_person_pos(frame, person_pos):
        x_min, y_min, x_max, y_max = map(int, person_pos)
        clothes_results = Clothes.clothes_model(frame[y_min:y_max, x_min:x_max])
        clothes_results = clothes_results.pandas().xyxy[0]
        clothes = []
        for _, row in clothes_results.iterrows():
            if row['confidence'] > 0.5:
                clothes.append(row['name'])
                # draw clothes bounding box
                cv2.rectangle(frame, (x_min + int(row['xmin']), y_min + int(row['ymin'])), (x_min + int(row['xmax']), y_min + int(row['ymax'])), (0, 255, 0), 2)
                cv2.putText(frame, row['name'], (x_min + int(row['xmin']), y_min + int(row['ymin'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return clothes
