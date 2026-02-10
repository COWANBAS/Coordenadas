import sys
import pyautogui
from PIL import Image, ImageFilter
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint


class BlurScreen(QLabel):
    def __init__(self):
        super().__init__()

        screenshot = pyautogui.screenshot()
        blurred = screenshot.filter(ImageFilter.GaussianBlur(radius=8))

        data = blurred.tobytes("raw", "RGB")
        qimage = QImage(data, blurred.width, blurred.height, QImage.Format_RGB888)

        self.base_pixmap = QPixmap.fromImage(qimage)
        self.pixmap = self.base_pixmap.copy()
        self.setPixmap(self.pixmap)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.start_point = None
        self.end_point = None

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.pixmap = self.base_pixmap.copy()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.pixmap = self.base_pixmap.copy()
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.red, 2)
            painter.setPen(pen)

            rect_x = self.start_point.x()
            rect_y = self.start_point.y()
            rect_w = event.pos().x() - rect_x
            rect_h = event.pos().y() - rect_y

            painter.drawRect(rect_x, rect_y, rect_w, rect_h)
            painter.end()

            self.setPixmap(self.pixmap)

    def mouseReleaseEvent(self, event):
        self.end_point = event.pos()

        x1 = self.start_point.x()
        y1 = self.start_point.y()
        x2 = self.end_point.x()
        y2 = self.end_point.y()

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        print(f"Local = ({x}, {y}, {w}, {h})")

        self.start_point = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


app = QApplication(sys.argv)
window = BlurScreen()
sys.exit(app.exec_())
