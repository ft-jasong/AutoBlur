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

def blur_face_in_frame(frame, face_pos):
    x, y, width, height = face_pos
    frame[y:y+height, x:x+width] = cv2.blur(frame[y:y+height, x:x+width], (30, 30))

# debug
def draw_rect_face_in_person(frame, face_pos, person_pos, msg):
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

def draw_rect_face_in_frame(frame, face_pos, msg):
    x, y, width, height = face_pos
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (0, 0, 255)
    if msg == 'unknown':
        color = COLOR_RED
    else:
        color = COLOR_GREEN
    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
    cv2.putText(frame, msg, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def edit_video(video_path, src_image_paths, input_clothes_type):
    # 기본 변수들 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    source_faces = Face.get_source_faces(src_image_paths)
    # video Init 설정
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(os.path.join(OUTPUT_PATH, 'uquiz_output.mp4'), fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # detect person
        person = Person()
        person.detect(frame)
        detected_persons = person.get_detected_persons()
        all_faces = Face.detect_from_frame(frame) # 프레임에서 사람 얼굴 찾음
        all_clothes = Clothes.detect_from_frame(frame) # 프레임에서 사람 옷 찾음, 0 은 옷종류 1은 옷 위치
        no_blur_pos = [] # 블러 안당할 사람들의 위치
        for face in all_faces:
            face_pos = convert_pos_format(face['box'])
            euc_dist, ret = Face.is_video_face_in_source(face, source_faces)
            if ret:
                for p_row in detected_persons:
                    person_pos = Person.get_pos(p_row)
                    if Person.is_in_person(person_pos, face_pos) and person_pos not in no_blur_pos:
                        draw_rect_face_in_frame(frame, face['box'], str(euc_dist))
                        no_blur_pos.append(person_pos)
                        break
        for cloth_name, cloth_pos in all_clothes:
            for input_cloth in input_clothes_type:
                if cloth_name == input_cloth:
                    for p_row in detected_persons:
                        person_pos = Person.get_pos(p_row)
                        if Person.is_in_person(person_pos, cloth_pos) and person_pos not in no_blur_pos:
                            no_blur_pos.append(person_pos)
                            break
        # set_no_blur_pos = set(no_blur_pos)
        for face in all_faces:
            face_pos = convert_pos_format(face['box'])
            for p_row in detected_persons:
                person_pos = Person.get_pos(p_row)
                if Person.is_in_person(person_pos, face_pos):
                    if person_pos not in no_blur_pos:
                        blur_face_in_frame(frame, face['box'])
                        draw_rect_face_in_frame(frame, face['box'], 'unknown')
                    break
        out.write(frame)
    cap.release()
    out.release()
