import os

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *

from Core.image_crop import image_crop

form_class = uic.loadUiType("./static/ui/main.ui")[0]



class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.left_edit.setText("216")
        self.top_edit.setText("134")
        self.right_edit.setText("216")
        self.bottom_edit.setText("138")

        self.target_folder_path = ""
        self.save_folder_path = ""

        # button 연결
        self.btn_target_path.clicked.connect(self.set_target_path)
        self.btn_save_path.clicked.connect(self.set_save_path)

        self.worker = Worker()
        self.worker.finished.connect(self.update_progress_bar)

        self.files = []
        self.file_list_model = QStandardItemModel()

        self.execute_button.clicked.connect(self.execute)

    def set_target_path(self):
        folder_path = False
        try:
            folder_path = QFileDialog.getExistingDirectory(None, '폴더 선택', os.path.expanduser("~"))
        except Exception as e:
            print(e)
        if folder_path:
            self.target_path.setText(folder_path)
            self.target_folder_path = folder_path
            save_path = folder_path + "_처리결과"
            self.save_path.setText(save_path)
            self.save_folder_path = save_path

            self.files = os.listdir(folder_path)
            self.file_list_model = QStandardItemModel();
            for file in self.files:
                q_standard_item = QStandardItem(file)
                self.file_list_model.appendRow(q_standard_item)
            self.fileList.setModel(self.file_list_model)

    def set_save_path(self):
        folder_path = QFileDialog.getExistingDirectory(None, '폴더 선택', os.path.expanduser("~"))
        if folder_path:
            self.save_path.setText(folder_path)
            self.save_folder_path = folder_path

    def update_progress_bar(self, data):
        self.progressBar.setValue(int((data["now"] / data["total"]) * 100))

    def execute(self):
        try:
            left = int(self.left_edit.text())
            right = int(self.right_edit.text())
            top = int(self.top_edit.text())
            bottom = int(self.bottom_edit.text())

            left_top_right_bottom = [left, top, right, bottom]
            self.worker.init(self.target_folder_path, self.save_folder_path, self.files, left_top_right_bottom)
            self.worker.start()
        except Exception as e:
            print(e)


class Worker(QThread):
    finished = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.target_path = None
        self.save_path = None
        self.file_list = None
        self.left_top_right_bottom = []

    def init(self, target_path, save_path, file_list, left_top_right_bottom):
        self.target_path = target_path
        self.save_path = save_path
        self.file_list = file_list
        self.left_top_right_bottom = left_top_right_bottom

        if not os.path.isdir(self.save_path):
            os.mkdir(save_path)

    def run(self):
        try:
            for now, file in enumerate(self.file_list):
                ext = file.split('.')[-1]
                if ext != "jpg" and ext != "png":
                    result = False
                else:
                    result = image_crop(file, self.target_path, self.save_path, self.left_top_right_bottom)
                if result:
                    print("success")
                else:
                    print("fail")
                data = {
                    "now": now+1,
                    "total": len(self.file_list)
                }
                self.finished.emit(data)

        except Exception as e:
            print(e)


