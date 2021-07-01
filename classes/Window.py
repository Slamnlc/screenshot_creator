import random
import string
import subprocess

from PIL import Image
from PyQt5 import QtWidgets, QtGui, QtCore

from classes.GraphicView import GraphicView, RectItem
from config import PEN_WIDTH, PLATFORM, SCREENSHOT_PATH, SCREENSHOT_FORMAT
from functions import copy_to_clipboard


class Window(QtWidgets.QMainWindow):
    def __init__(self, screen):
        super(Window, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.scene = GraphicView(screen)
        self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        view = QtWidgets.QGraphicsView()
        view.setScene(self.scene)
        view.setStyleSheet("background:transparent;")
        view.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        view.setMouseTracking(True)
        view.setAcceptDrops(True)

        # view.setStyleSheet(open('main_css.css', 'r').read())
        self.setCentralWidget(view)
        self.screen_size = screen

        QtWidgets.QShortcut(QtGui.QKeySequence('Esc'), self).activated.connect(self.close_app)
        QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+Z'), self).activated.connect(self.undo)
        QtWidgets.QShortcut(QtGui.QKeySequence('Space'), self).activated.connect(self.take_screenshot)

    def close_app(self):
        self.close()

    def undo(self):
        print('delete')
        if len(self.scene.graphic_items) > 0:
            # self.scene.graphic_items[-1].
            self.scene.removeItem(self.scene.graphic_items.pop(-1))

    def take_screenshot(self):
        if len(self.scene.graphic_items) > 0:
            item: RectItem = self.scene.graphic_items[-1]

            coord = item.rect().getCoords()
            print(coord)
            region = list(map(lambda x: int(coord[x]) + PEN_WIDTH if x < 2 else int(coord[x]) - PEN_WIDTH,
                              range(len(coord))))
            tmp_file_name = ''
            if PLATFORM == 'mac':
                tmp_file_name = f"{SCREENSHOT_PATH}{''.join(random.choices(string.ascii_letters, k=10))}." \
                                f"{SCREENSHOT_FORMAT.lower()}"
                subprocess.call(['screencapture', '-xr', tmp_file_name])

            image = Image.open(fp=tmp_file_name)
            width_correction = image.width / self.screen_size.width()
            height_correction = image.height / self.screen_size.height()
            print(region)
            region = tuple(map(
                lambda x: (region[x] + item.y()) * width_correction if x % 2
                else (region[x] + item.x()) * height_correction,
                range(len(region)))
            )
            image.crop(region).save(tmp_file_name)
            self.close()

            copy_to_clipboard(tmp_file_name)
