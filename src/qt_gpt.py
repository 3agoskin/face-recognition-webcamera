import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

class BackgroundWidget(QGlPicamera2):
    def __init__(self):
        super().__init__(picam2)
        self.picamera2 = picam2
        self.width = 800
        self.height = 600
        self.keep_ar = False
        self.setWindowTitle("Qt Picamera2 App")

        # Установка размеров окна
        # self.setWindowTitle('Пример приложения с фоном')
        # self.setGeometry(100, 100, 800, 600)

        # # Создание QLabel для фона
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap('src/background.jpg')  # Укажите путь к вашему изображению
        self.background_label.setPixmap(self.background_pixmap)
        self.background_label.setScaledContents(True)  # Масштабировать содержимое по размеру QLabel
        self.background_label.resize(self.size())


        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        # Кнопка в левом верхнем углу
        top_left_button = QPushButton('Верхний Левый', self)
        top_left_button.move(10, 10)

        # Кнопка в правом верхнем углу
        top_right_button = QPushButton('Верхний Правый', self)
        top_right_button.move(self.width() - 150, 10)

        # Кнопка в левом нижнем углу
        bottom_left_button = QPushButton('Нижний Левый', self)
        bottom_left_button.move(10, self.height() - 50)

        # Кнопка в правом нижнем углу
        bottom_right_button = QPushButton('Нижний Правый', self)
        bottom_right_button.move(self.width() - 150, self.height() - 50)

        # Кнопка в центре
        center_button = QPushButton('Центр', self)
        center_button.move(self.width() // 2 - 30, self.height() // 2 - 15)

        # Добавляем все виджеты на фоновый QLabel
        self.background_label.lower()  # Перемещаем QLabel на задний план

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = BackgroundWidget()
    mainWin.show()
    sys.exit(app.exec_())
