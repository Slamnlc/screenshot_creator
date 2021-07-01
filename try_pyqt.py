import sys

from PyQt5.QtWidgets import QApplication

from classes.Window import Window

if __name__ == "__main__":
    App = QApplication(sys.argv)
    screen = App.primaryScreen().size()
    window = Window(screen=screen)
    window.showMaximized()
    sys.exit(App.exec())
