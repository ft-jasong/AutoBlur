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
    print(f"frame : {frame}")
    person_results = clothes_model(frame)
    person_results = person_results.pandas().xyxy[0][person_results.pandas().xyxy[0]['name'] == 'person']
    # add new detected persons confidence over 0.5
    # person_pos = []
    
    # # 옷 확인을 위해서 잠시 주석 삭ㅈ
    # for index, row in person_results.iterrows():
    #     if row['confidence'] > 0.5:
    #         detected_persons.append(row)
    #     # person_pos.append([row['xmin'], row['ymin'], row['xmax'], row['ymax']])
    # # draw rectangle
    # # for pos in person_pos:
    #     # cv2.rectangle(frame, (pos[0], pos[1]), (pos[2], pos[3]), (0, 255, 0), 2)
    # if len(person_results) > 0:
    #     print("Person detected!")
    #     for res in person_results:
    #         clothes_results = clothes_model(frame[int(res['ymin']):int(res['ymax']), int(res['xmin']):int(res['xmax'])])
            
    # else:
    #     print("No person detected.")
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()