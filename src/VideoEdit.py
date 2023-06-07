import os
import cv2
import sys
from Person import Person
from Clothes import Clothes
from Face import Face

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(CUR_DIR, '../')

# 기본 person offset을 더해줌
def add_offset(detect_pos, offset_pos):
    offset_x, offset_y, tmp1, tmp2 = offset_pos
    return (detect_pos[0] + offset_x, detect_pos[1] + offset_y, detect_pos[2] + offset_x, detect_pos[3] + offset_y)

def convert_pos_format(face_pos):
    x, y, width, height = face_pos
    return (x, y, x + width, y + height)

def blur_face(frame, face_pos, person_pos):
    face_pos = convert_pos_format(face_pos)
    xmin, ymin, xmax, ymax = map(int, add_offset(face_pos, person_pos))
    frame[ymin:ymax, xmin:xmax] = cv2.blur(frame[ymin:ymax, xmin:xmax], (30, 30))

# debug
def draw_rect_in_face(frame, face_pos, person_pos, msg):
    face_pos = convert_pos_format(face_pos)
    xmin, ymin, xmax, ymax = map(int, add_offset(face_pos, person_pos))
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (0, 0, 255)
    if msg == 'unknown':
        color = COLOR_RED
    else:
        color = COLOR_GREEN
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
    cv2.putText(frame, msg, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def edit_video(video_path, input_clothes_type):
    # 기본 변수들 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    source_faces = Face.get_source_faces()
    # video Init 설정
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(os.path.join(OUTPUT_PATH, 'output.mp4'), fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # detect person
        person = Person()
        person.detect(frame)
        detected_persons = person.get_detected_persons()
        for p_row in detected_persons:
            person_pos = person.get_pos(p_row)
            # detect face
            p_row['face'] = Face.detect_from_person_pos(frame, person_pos)
            # detect clothes
            p_row['clothes'] = Clothes.detect_from_person_pos(frame, person_pos)
            # edit face
            if len(p_row['face']) > 0:
                for face in p_row['face']:
                    # edit face
                    euc_val, ret = Face.is_video_face_in_source(face, source_faces)
                    if ret is True:
                        draw_rect_in_face(frame, face['box'], person_pos, str(euc_val))
                    # if Face.is_video_face_in_source(face, source_faces):
                    #     draw_rect_in_face(frame, face['box'], person_pos, 'known')                        
                    else:
                        blur_face(frame, face['box'], person_pos)
                        draw_rect_in_face(frame, face['box'], person_pos, str(euc_val))
                        # draw_rect_in_face(frame, face['box'], person_pos, 'unknown')
                    # check if input clothes type is in detected clothes
                        clothes_detected = False
                        for input_cloth in input_clothes_type:
                            if input_cloth in p_row['clothes']:
                                clothes_detected = True
                                break
                        if not clothes_detected:
                            blur_face(frame, face['box'], person_pos)
        # output
        out.write(frame)
    cap.release()
    out.release()
