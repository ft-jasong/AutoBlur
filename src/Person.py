import os
import torch
import cv2

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PERSON_MODEL_DIR = os.path.join(CUR_DIR, '../checkpoint/person_best.pt')

class Person:
    person_model = torch.hub.load('ultralytics/yolov5', 'custom', path=PERSON_MODEL_DIR)
    person_model.conf = 0.5
    person_model.iou = 0.5
    person_model.classes = [0]
    person_model.names = ['person']
    def __init__(self):
        self.detected_persons = []

    def detect(self, frame):
        person_results = self.person_model(frame)
        person_results = person_results.pandas().xyxy[0][person_results.pandas().xyxy[0]['name'] == 'person']
        for _, row in person_results.iterrows():
            if row['confidence'] > 0.5:
                self.detected_persons.append(row)
                # draw person bounding box in purple rgb
                cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (255, 0, 255), 2)
                cv2.putText(frame, 'person', (int(row['xmin']), int(row['ymin'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)


    def get_pos(self, p_row):
        return [p_row['xmin'], p_row['ymin'], p_row['xmax'], p_row['ymax']]
    
    def get_detected_persons(self):
        return self.detected_persons

    def clear_detected_persons(self):
        self.detected_persons = []
