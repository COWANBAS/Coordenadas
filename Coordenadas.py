import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt

class BlurScreen(QLabel):
    def __init__(self):
        super().__init__()

        screenshot = pyautogui.screenshot()
        data = screenshot.tobytes("raw", "RGB")
        qimage = QImage(data, screenshot.width, screenshot.height, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(self.pixmap)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.start_point = None
        self.clipboard = QApplication.clipboard()

    def mousePressEvent(self, event):
        self.start_point = event.pos()  

        if event.modifiers() == Qt.ControlModifier:  
            self.get_color(event.pos())
       
        elif event.modifiers() == Qt.ShiftModifier:  
            self.get_color(event.pos())

    def mouseMoveEvent(self, event):
        if self.start_point:  
            self.update_pixmap_with_rect(event)

    def mouseReleaseEvent(self, event):
        if self.start_point:  
            self.handle_coords(event)
        self.start_point = None  

    def update_pixmap_with_rect(self, event):
        pixmap_copy = self.pixmap.copy()  
        painter = QPainter(pixmap_copy)
        pen = QPen(Qt.white, 2)
        painter.setPen(pen)

        x, y = self.start_point.x(), self.start_point.y()
        w, h = event.pos().x() - x, event.pos().y() - y
        painter.drawRect(x, y, w, h)
        painter.end()

        self.setPixmap(pixmap_copy) 

    def handle_coords(self, event):

        x1, y1 = self.start_point.x(), self.start_point.y()
        x2, y2 = event.pos().x(), event.pos().y()

        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        coords = f"Coordenadas: ({x}, {y}, {w}, {h})"
        print(coords)
        self.copy_to_clipboard(coords)

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
