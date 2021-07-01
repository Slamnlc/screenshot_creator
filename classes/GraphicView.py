from PyQt5 import QtCore, QtWidgets, QtGui

from config import SELECT_RECTANGLE_COLOR, PEN_WIDTH


class GraphicView(QtWidgets.QGraphicsScene):
    def __init__(self, screen):
        super(GraphicView, self).__init__()
        self.setSceneRect(QtCore.QRectF(-16, -74, screen.width(), screen.height()))
        self.begin, self.end = QtCore.QPointF(), QtCore.QPointF()
        self.graphic_items = []
        self.new_item = False

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos().x(), event.scenePos().y(), QtGui.QTransform())
        if item is None:
            self.new_item = True
            self.begin, self.end = event.scenePos(), event.scenePos()
            for elem in self.items():
                for child in elem.childItems():
                    child.setParentItem(None)
            rect_item = RectItem(self)
            self.addItem(rect_item)
            self.graphic_items.append(rect_item)
        else:
            item.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        item = self.itemAt(event.scenePos().x(), event.scenePos().y(), QtGui.QTransform())
        if self.new_item:
            self.graphic_items[-1].setRect(QtCore.QRectF(self.begin, event.scenePos()).normalized())
        if item is not None:
            if isinstance(item, RectItem):
                if event.buttons() == QtCore.Qt.LeftButton:
                    item.mouseMoveEvent(event)
                else:
                    item.setCursor(QtCore.Qt.OpenHandCursor)
            elif isinstance(item, EllipseItem):
                item.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        item = self.itemAt(event.scenePos().x(), event.scenePos().y(), QtGui.QTransform())
        if self.new_item:
            self.begin, self.end, self.new_item = QtCore.QPointF(), QtCore.QPointF(), False
        if item is not None:
            item.mouseReleaseEvent(event)


class RectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, parent: GraphicView):
        super(RectItem, self).__init__()
        self.parent = parent
        self.setPen(QtGui.QPen(SELECT_RECTANGLE_COLOR, PEN_WIDTH, QtCore.Qt.DashDotLine))
        self.ellipses = tuple('')
        # self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        # self.updateHandlesPos()

    def mouseMoveEvent(self, event):
        x_offset = event.scenePos().x() - event.lastScenePos().x()
        y_offset = event.scenePos().y() - event.lastScenePos().y()
        self.moveBy(x_offset, y_offset)
        for child in self.childItems():
            child.moveBy(x_offset * 0.01, y_offset * 0.01)

    def mousePressEvent(self, event):
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        if len(self.childItems()) == 0:
            params = ['top_left', 'top_right', 'bottom_left', 'bottom_right',
                      'top_mid', 'bottom_mid', 'left_mid', 'right_mid']
            for param in params:
                EllipseItem(self, param)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def shape(self):

        path = QtGui.QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            path.addEllipse(10, 10, 10, 10)

        return path


class EllipseItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent: RectItem, param: str):
        super().__init__()
        self.setRect(20, 20, 20, 20)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine))
        self.setBrush(QtCore.Qt.white)
        self.setParentItem(parent)
        self.setCursor(QtCore.Qt.SizeFDiagCursor)
        self.name = param
        self.parent = parent

        coord = parent.rect()
        position_switcher = {
            'top_left': [coord.topLeft(), QtCore.Qt.SizeFDiagCursor],
            'top_right': [coord.topRight(), QtCore.Qt.SizeBDiagCursor],
            'bottom_left': [coord.bottomLeft(), QtCore.Qt.SizeBDiagCursor],
            'bottom_right': [coord.bottomRight(), QtCore.Qt.SizeFDiagCursor],
            'top_mid': [QtCore.QPointF(coord.center().x(), coord.top()), QtCore.Qt.SizeVerCursor],
            'bottom_mid': [QtCore.QPointF(coord.center().x(), coord.bottom()), QtCore.Qt.SizeVerCursor],
            'left_mid': [QtCore.QPointF(coord.left(), coord.center().y()), QtCore.Qt.SizeHorCursor],
            'right_mid': [QtCore.QPointF(coord.right(), coord.center().y()), QtCore.Qt.SizeHorCursor]
        }
        for elem in position_switcher:
            position_switcher[elem][0].setX(position_switcher[elem][0].x() - 30)
            position_switcher[elem][0].setY(position_switcher[elem][0].y() - 30)

        self.setPos(position_switcher[param][0])
        self.setCursor(position_switcher[param][1])

    def mousePressEvent(self, event):
        rect = self.parent.rect()
        # rect.moveTop(200)
        # for child in self.parent.childItems():
        #     child.moveBy(0, 200)
        # self.parent.setRect(rect)
        print('hi')

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            x_offset = event.scenePos().x() - event.lastScenePos().x()
            y_offset = event.scenePos().y() - event.lastScenePos().y()
            rect = self.parent.rect()

            if self.name == 'left_mid':
                rect.setLeft(event.scenePos().x())
            elif self.name == 'top_mid':
                rect.setTop(event.scenePos().y())
            elif self.name == 'right_mid':
                rect.setRight(event.scenePos().x())
            elif self.name == 'bottom_mid':
                rect.setBottom(event.scenePos().y())

            self.parent.setRect(rect)
            for child in self.parent.childItems():
                child.moveBy(x_offset, y_offset)
            pass
