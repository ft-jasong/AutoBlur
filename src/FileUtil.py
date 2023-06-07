import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(CUR_DIR, '../asset/videos/')

def get_video_path(filename):
    return os.path.join(VIDEO_DIR, filename)

def get_image_paths(image_dir):
    image_paths = []
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_paths.append(os.path.join(image_dir, filename))
    return image_paths
