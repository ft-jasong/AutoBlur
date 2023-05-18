#!/bin/bash

python ./src/check_yolo_installed.py | grep "not" > /dev/null
if [ $? -eq 0 ]; then
    echo "Yolo is not installed. Installing..."
    git clone https://github.com/ultralytics/yolov5.git src/yolov5
    cd src/yolov5
    pip install -r requirements.txt
    echo "Yolo installed."
else
    echo "Yolo is installed."
fi