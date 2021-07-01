import random
import string
import subprocess
import sys

import PyQt5
from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QKeySequence, QPen, QBrush, QColor, QPainter, QCursor
from PyQt5.QtWidgets import QApplication, QShortcut, QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout, QMainWindow

from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLATFORM, SCREENSHOT_PATH, SCREENSHOT_FORMAT, PEN_WIDTH, \
    SELECT_RECTANGLE_COLOR
from dasdas import randomBetween
from functions import copy_to_clipboard


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.begin, self.end = QPointF(), QPointF()
        self.graphic_items = []
        self.new_item = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background:transparent;")
        self.setMouseTracking(True)

        scene = QGraphicsScene()
        self.scene = scene
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.se

        view = QGraphicsView()
        layout.addWidget(view)
        view.resize(screen.width(), screen.height())
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.setCacheMode(QGraphicsView.CacheBackground)
        view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        view.setMouseTracking(True)


        scene.setSceneRect(0, 0, self.size().width(), self.size().height())

    def mousePressEvent(self, event):
        print('mousePressEvent')
        self.new_item = True
        self.begin, self.end = event.pos(), event.pos()
        rect_item = RectItem(self)
        rect_item.setPos(self.begin.x(), self.begin.y())
        self.scene.addItem(rect_item)
        self.graphic_items.append(QtCore.QRectF(self.begin, self.end).normalized())

    def mouseMoveEvent(self, event: PyQt5.QtGui.QMouseEvent):
        print('mouseMoveEvent')
        if self.new_item:
            self.graphic_items[-1].setRect(self.begin.x(), self.begin.y(), event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):
        print('mouseReleaseEvent')
        self.new_item = False
        self.begin, self.end = QPointF(), QPointF()


class RectItem(QtWidgets.QGraphicsItem):
    def __init__(self, parent: Widget):
        super().__init__()
        self.parent = parent
        self.pen = QPen(SELECT_RECTANGLE_COLOR, PEN_WIDTH, Qt.DashDotLine)

    def mouseMoveEvent(self, event):
        self.setPos(self.mapToScene(event.pos()))

    def boundingRect(self):
        print('boundingRect')
        return QRectF(-30,-30,60,60)
        # return self.parent.graphic_items[-1]

    def paint(self, painter, option, widget):
        print('paint')
        painter.setPen(Qt.black)
        painter.setBrush(Qt.green)
        # painter.drawRect(self.parent.graphic_items[-1])
        painter.drawRect(-30, -30, 60, 60)

    def mousePressEvent(self, event):
        self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    screen = app.primaryScreen().size()
    w = Widget()
    w.showMaximized()

    # Run the main Qt loop
    sys.exit(app.exec_())