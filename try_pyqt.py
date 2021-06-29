import random
import string
import subprocess
import sys

from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QKeySequence, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QShortcut

from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLATFORM, SCREENSHOT_PATH, SCREENSHOT_FORMAT, PEN_WIDTH
from functions import copy_to_clipboard


class GraphicView(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(GraphicView, self).__init__(QtCore.QRectF(-16, -74, screen.width(), screen.height()))
        self.begin, self.end = QPointF(), QPointF()
        self.graphic_items = []

    def mousePressEvent(self, event):
        self.begin, self.end = event.scenePos(), event.scenePos()

        rect_item = QtWidgets.QGraphicsRectItem()
        rect_item.setPen(QPen(Qt.red, PEN_WIDTH, Qt.SolidLine))
        self.addItem(rect_item)
        self.graphic_items.append(rect_item)
        rect = QtCore.QRectF(self.begin, self.end).normalized()
        self.graphic_items[-1].setRect(rect)

    def mouseMoveEvent(self, event):
        self.graphic_items[-1].setRect(QtCore.QRectF(self.begin, event.scenePos()).normalized())

    def mouseReleaseEvent(self, event):
        self.begin, self.end = QPointF(), QPointF()


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(SCREEN_HEIGHT, SCREEN_WIDTH)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setMouseTracking(True)
        self.setDockNestingEnabled(True)
        # self.setAutoFillBackground(True)

        self.scene = GraphicView()
        view = QtWidgets.QGraphicsView(self.scene)
        # view.setStyleSheet("background:transparent;")

        view.setStyleSheet(open('main_css.css', 'r').read())
        self.setCentralWidget(view)

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close_app)
        QShortcut(QKeySequence('Ctrl+Z'), self).activated.connect(self.undo)
        QShortcut(QKeySequence('Space'), self).activated.connect(self.take_screenshot)

    def close_app(self):
        self.close()

    def undo(self):
        if len(self.scene.graphic_items) > 0:
            self.scene.removeItem(self.scene.graphic_items.pop(-1))

    def take_screenshot(self):
        if len(self.scene.graphic_items) > 0:
            coord = self.scene.graphic_items[-1].rect().getCoords()
            region = tuple(map(lambda x: int(coord[x]) + PEN_WIDTH if x < 2 else int(coord[x]) - PEN_WIDTH,
                               range(len(coord))))
            tmp_file_name = ''
            if PLATFORM == 'mac':
                tmp_file_name = f"{SCREENSHOT_PATH}{''.join(random.choices(string.ascii_letters, k=10))}." \
                                f"{SCREENSHOT_FORMAT.lower()}"
                subprocess.call(['screencapture', '-xr', tmp_file_name])

            image = Image.open(fp=tmp_file_name)
            image.resize((screen.width(), screen.height())).crop(region).save(tmp_file_name)
            self.close()

            copy_to_clipboard(tmp_file_name)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    screen = App.primaryScreen().size()
    window = Window()
    window.showMaximized()
    sys.exit(App.exec())
