import sys
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMainWindow, QWidget, QCheckBox
from VideoEdit import *


class FileConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('File Converter')
        self.setGeometry(300, 300, 500, 400)

        layout = QVBoxLayout()

        self.names = [
            'short sleeve top', 'long sleeve top', 'short sleeve outerwear',
            'long sleeve outerwear', 'vest', 'sling', 'shorts', 'trousers',
            'skirt', 'short sleeve dress', 'long sleeve dress', 'vest dress', 'sling dress'
        ]


        self.upload_video_button = QPushButton('Upload Video')
        self.upload_video_button.clicked.connect(self.upload_video)
        layout.addWidget(self.upload_video_button)

        self.upload_image_button = QPushButton('Upload Images')
        self.upload_image_button.clicked.connect(self.upload_images)
        layout.addWidget(self.upload_image_button)

        self.checkboxes = []
        for name in self.names:
            checkbox = QCheckBox(name)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_files)
        layout.addWidget(self.convert_button)

        self.label = QLabel('')
        layout.addWidget(self.label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.file_names = []

    def upload_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Videos (*.mp4)")
        if file_name:
            self.file_names = [file_name]
            self.label.setText(f'Selected video file: {file_name}')
        self.video_path = file_name

    def upload_images(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Image Files", "", "Images (*.jpg *.png)")
        if file_names:
            self.file_names = file_names
            self.label.setText(f'Selected image files: {", ".join(file_names)}')
        self.src_img_paths = file_names

    def convert_files(self):
        checked_names = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        edit_video(self.video_path, self.src_img_paths, checked_names)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileConverterApp()
    window.show()
    sys.exit(app.exec())
