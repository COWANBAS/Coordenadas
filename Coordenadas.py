import sys
import pyautogui
from PIL import Image, ImageFilter
from PyQt5.QtWidgets import QApplication, QLabel  
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QClipboard  
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
        self.mode = None  

        self.clipboard = QApplication.clipboard()  

    def mousePressEvent(self, event):
        modifiers = event.modifiers()

        if modifiers == Qt.ShiftModifier:
            self.mode = "coords"
            self.start_point = event.pos()

        elif modifiers == Qt.ControlModifier:
            self.mode = "color"
            self.get_color(event.pos())

        else:
            self.mode = None
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.start_point and self.mode == "coords":
            self.pixmap = self.base_pixmap.copy()
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.white, 2)
            painter.setPen(pen)

            x = self.start_point.x()
            y = self.start_point.y()
            w = event.pos().x() - x
            h = event.pos().y() - y

            painter.drawRect(x, y, w, h)
            painter.end()
            self.setPixmap(self.pixmap)

        elif self.mode == "color":
            self.get_color(event.pos())

    def mouseReleaseEvent(self, event):
        if self.mode == "coords" and self.start_point:
            end_point = event.pos()

            x1, y1 = self.start_point.x(), self.start_point.y()
            x2, y2 = end_point.x(), end_point.y()

            x = min(x1, x2)
            y = min(y1, y2)
            w = abs(x2 - x1)
            h = abs(y2 - y1)

            coords = f"Coordenadas: ({x}, {y}, {w}, {h})"
            print(coords)
            self.copy_to_clipboard(coords)  

        self.start_point = None
        self.mode = None

    def get_color(self, pos):
        global_pos = self.mapToGlobal(pos)
        r, g, b = pyautogui.pixel(global_pos.x(), global_pos.y())
        hex_color = f"#{r:02X}{g:02X}{b:02X}"

        color_info = f"Cor em ({global_pos.x()}, {global_pos.y()}): {hex_color}"
        print(color_info)
        self.copy_to_clipboard(color_info)  

    def copy_to_clipboard(self, text):
        self.clipboard.setText(text)  

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


app = QApplication(sys.argv)
window = BlurScreen()
sys.exit(app.exec_())
