import sys
import os
import ExtractScene
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,QFileDialog,
    QVBoxLayout, QDialog,QTextEdit,QDoubleSpinBox)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.video_path = ""
        self.current_video_path = ""
        self.sensitivity  = 0.36
        self.loadVideoPathButton = QPushButton("Load Video")
        self.generateButton = QPushButton("Generate")
        self.feedback = QTextEdit("...")
        self.feedback.setReadOnly(True)
        self.inputSensitivity = QDoubleSpinBox()
        self.inputSensitivity.setRange(0,1)
        self.inputSensitivity.setSingleStep(0.1)

        #load previous user data 
        self.inputSensitivity.setValue(float(ExtractScene.get_user_data("sensitivity",0.3)))
        self.load_video_path(ExtractScene.get_user_data("video_path",""))

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.loadVideoPathButton)
        layout.addWidget(self.feedback)
        layout.addWidget(self.inputSensitivity)
        layout.addWidget(self.generateButton)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.generateButton.clicked.connect(self.generate_files)
        self.loadVideoPathButton.clicked.connect(self.load_video_path)

    # Greets the user
    def generate_files(self):
        if os.path.exists(self.current_video_path) and self.current_video_path!="":
            self.load_user_input()
            self.save_user_input()
            self.append_to_feedback("generating tile...")
            result = ExtractScene.create_tile_images(self.video_path , self.sensitivity )
            self.append_to_feedback(result)
            self.append_to_feedback("generating shot images...")
            result = ExtractScene.create_shot_images(self.video_path , self.sensitivity )
            self.append_to_feedback(result)
        else:
            self.append_to_feedback(f"wrong video path ! {self.video_path}")

    def load_user_input(self):
        self.sensitivity = self.inputSensitivity.value()
        self.video_path = self.current_video_path

    def save_user_input(self):
        ExtractScene.set_user_data("video_path",self.video_path)
        ExtractScene.set_user_data("sensitivity",self.sensitivity)

    def find_video_path(self):
        fileName = QFileDialog.getOpenFileName(self, 'OpenFile')
        path = fileName[0]
        self.load_video_path(fileName[0])

    def load_video_path(self,_path):
        if self.check_path(_path):
            self.current_video_path=_path 
            self.append_to_feedback(str(_path))            

    def append_to_feedback(self,_message):
        self.feedback.setHtml(_message)

    def check_path(self,_path):
        extension = os.path.basename(_path).split(".")[-1]
        video_formats = ['mov','mp4','wmv','mkv','avi']
        if extension in video_formats:
            return True
        else:
            self.append_to_feedback(f"ERROR the file should be a video ! {video_formats}")
            return False


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())

#python D:/1_TRAVAIL/WIP/ALARIGGER/CODING/PYTHON/REPOSITORIES/AL_ExtractScenes/python/main.py