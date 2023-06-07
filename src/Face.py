import cv2
import sys
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.spatial import distance
from mtcnn import MTCNN
from FileUtil import get_image_paths

SRC_IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../asset/images/')

class Face:
    mtcnn = MTCNN()

    def get_source_faces():
        source_faces = []
        img_paths = get_image_paths(SRC_IMG_PATH)
        for img_path in img_paths:
            img = cv2.imread(img_path)
            source_faces.append(Face.mtcnn.detect_faces(img))
        return source_faces

    def detect_from_person_pos(frame, person_pos):
        x_min, y_min, x_max, y_max = map(int, person_pos)
        face_results = Face.mtcnn.detect_faces(frame[y_min:y_max, x_min:x_max])
        return face_results
    
    def is_video_face_in_source(video_face, source_faces):
        target_landmarks = [video_face['keypoints']['left_eye'], video_face['keypoints']['right_eye'], video_face['keypoints']['nose'], video_face['keypoints']['mouth_left'], video_face['keypoints']['mouth_right']]
        target_landmarks_flat = [coord for landmark in target_landmarks for coord in landmark]
        lowest_euc_distance = sys.maxsize
        for source_face in source_faces:
            source_landmarks = [source_face[0]['keypoints']['left_eye'], source_face[0]['keypoints']['right_eye'], source_face[0]['keypoints']['nose'], source_face[0]['keypoints']['mouth_left'], source_face[0]['keypoints']['mouth_right']]
            source_landmarks_flat = [coord for landmark in source_landmarks for coord in landmark]
            euc_distance = distance.euclidean(target_landmarks_flat, source_landmarks_flat)
            if euc_distance < lowest_euc_distance:
                lowest_euc_distance = euc_distance
        return lowest_euc_distance, lowest_euc_distance < 1300