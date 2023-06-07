import cv2
import torch
import matplotlib.pyplot as plt
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PERSON_MODEL_PATH = os.path.join(CUR_DIR, '../checkpoint/person_best.pt')
CLOTHES_MODEL_PATH = os.path.join(CUR_DIR, '../checkpoint/clothes_best.pt')

print(PERSON_MODEL_PATH)
person_model = torch.hub.load('ultralytics/yolov5', 'custom', path=PERSON_MODEL_PATH)
person_model.conf = 0.5
person_model.iou = 0.5
person_model.classes = [0]
person_model.names = ['person']
clothes_model = torch.hub.load('ultralytics/yolov5', 'custom', path=CLOTHES_MODEL_PATH)

detected_persons = []

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    # print(f"frame : {frame}")
    clothes_result = clothes_model(frame)
    clothes_result = clothes_result.pandas().xyxy[0]
    for index, row in clothes_result.iterrows():
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

