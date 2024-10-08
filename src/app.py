import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2


picam2 = Picamera2()
preview_width = 1024
preview_height = int(
    picam2.sensor_resolution[1] * preview_width / picam2.sensor_resolution[0]
)
preview_config_raw = picam2.create_preview_configuration(
    main={"size": (preview_width, preview_height)},
    raw={"size": picam2.sensor_resolution},
)
picam2.configure(preview_config_raw)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = __file__
        self.left = 0
        self.top = 0
        self.setWindowTitle(self.title)

        self.validator_widget = ValidatorWidget(self)
        self.setCentralWidget(self.validator_widget)
        # self.showFullScreen()
        self.show()


class ValidatorWidget(QWidget):

    def capture_done(self, job):
        global picam2
        result = picam2.wait(job)
        self.btnCapture.setEnabled(True)
        print("- capture_done.")

    def __init__(self, parent):
        super().__init__(parent)
        self.tabCapture = QWidget()
        self.tabCapture.layout = QVBoxLayout()
        self.qpicamera2 = QGlPicamera2(
            picam2, width=preview_width, height=preview_height, keep_ar=True
        )

        self.tabCapture.layout.addWidget(self.qpicamera2)
        self.qpicamera2.done_signal.connect(self.capture_done)

        picam2.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
