#create the Easy Editor photo editor here!
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget, QFileDialog, QVBoxLayout, QHBoxLayout
import os
from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask)
app = QApplication([])
main_win = QWidget()
folder_btn = QPushButton("Folder")
file_list = QListWidget()
left_btn = QPushButton("Left")
right_btn = QPushButton("Right")
mirror_btn = QPushButton("Mirror")
sharpen_btn = QPushButton("Sharpen")
bw_btn = QPushButton("B&W")
img_display = QLabel()
h1 = QHBoxLayout()
h2 = QHBoxLayout()
v1 = QVBoxLayout()
v2 = QVBoxLayout()
def select_folder():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    filenames = os.listdir(workdir)
    extensions = ["jpg", "png", "bmp", "svg", "eps"]
    file_list.addItems(filter(filenames, extensions))
def filter(filenames, extensions):
    filtered_list = []
    for f in filenames:
        for e in extensions:
            if f.lower().endswith(e):
                filtered_list.append(f)
    return filtered_list
def show_chosen_image():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.load_image(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.show_image(image_path)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def show_image(self, path):
        img_display.hide()
        pixmapimage = QPixmap(path)
        w, h = img_display.width(), img_display.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        img_display.setPixmap(pixmapimage)
        img_display.show()
    def save_image(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
workimage = ImageProcessor()
workdir = ""
v1.addWidget(folder_btn)
v1.addWidget(file_list)
h2.addWidget(left_btn)
h2.addWidget(right_btn)
h2.addWidget(mirror_btn)
h2.addWidget(sharpen_btn)
h2.addWidget(bw_btn)
v2.addWidget(img_display)
v2.addLayout(h2)
h1.addLayout(v1, 20)
h1.addLayout(v2)
main_win.setLayout(h1)
folder_btn.clicked.connect(select_folder)
file_list.currentRowChanged.connect(show_chosen_image)
bw_btn.clicked.connect(workimage.do_bw)
left_btn.clicked.connect(workimage.do_left)
right_btn.clicked.connect(workimage.do_right)
mirror_btn.clicked.connect(workimage.do_flip)
sharpen_btn.clicked.connect(workimage.do_sharpen)
main_win.show()
app.exec_()