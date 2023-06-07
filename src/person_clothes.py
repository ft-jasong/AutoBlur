import os
import cv2
import torch
import matplotlib.pyplot as plt
from Person import Person

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PERSON_MODEL_PATH = os.path.join(CUR_DIR, '../checkpoint/person_best.pt')
CLOTHES_MODEL_PATH = os.path.join(CUR_DIR, '../checkpoint/new_best.pt')

person_model = torch.hub.load('ultralytics/yolov5', 'custom', path=PERSON_MODEL_PATH)
person_model.conf = 0.5
person_model.iou = 0.5
person_model.classes = [0]
person_model.names = ['person']

clothes_model = torch.hub.load('ultralytics/yolov5', 'custom', path=CLOTHES_MODEL_PATH)
clothes_model.conf = 0.5
clothes_model.iou = 0.5

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    persons = []
    person_results = person_model(frame)
    person_results = person_results.pandas().xyxy[0][person_results.pandas().xyxy[0]['name'] == 'person']
    for index, row in person_results.iterrows():
        if row['confidence'] > 0.5:
            persons.append(Person((int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']))))
            # draw person bounding box in red
            cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 0, 255), 2)
            cv2.putText(frame, f"person {len(persons)}", (int(row['xmin']), int(row['ymin'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    ## 생각보다 인식률이 저조해서 전체 frame을 clothes model에 넣어준 경우
    # clothes_results = clothes_model(frame)
    # clothes_results = clothes_results.pandas().xyxy[0]
    # for index, row in clothes_results.iterrows():
    #     if row['confidence'] > 0.5:
    #         for p in persons:
    #             if p.isInside((int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']))):
    #                 p.addClothes(row['name'])
    #                 # draw clothes bounding box
    #                 cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 255, 0), 2)
    #                 cv2.putText(frame, row['name'], (int(row['xmin']), int(row['ymin'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # 사람 부분만 slice해서 해당 부분만 clothes model에 입력한 경우
    for p in persons:
        # clothes detection in person position
        x_min, y_min, x_max, y_max = p.getPos()
        clothes_results = clothes_model(frame[y_min:y_max, x_min:x_max])
        clothes_results = clothes_results.pandas().xyxy[0]
        for index, row in clothes_results.iterrows():
            if row['confidence'] > 0.5:
                p.addClothes(row['name'])
                # draw clothes bounding box
                cv2.rectangle(frame, (x_min + int(row['xmin']), y_min + int(row['ymin'])), (x_min + int(row['xmax']), y_min + int(row['ymax'])), (0, 255, 0), 2)
                cv2.putText(frame, row['name'], (x_min + int(row['xmin']), y_min + int(row['ymin'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    for idx, person in enumerate(persons):
        print(f"Person {idx + 1}: {person.clothes}")

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
