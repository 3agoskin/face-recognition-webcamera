from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2
picam2 = Picamera2()
width = 1024
height = 768

picam2.configure(
    picam2.create_video_configuration(main={"format": "XRGB8888", "size": (width, height)})
)
# picam2.configure(picam2.create_preview_configuration())
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
qpicamera2 = QGlPicamera2(picam2, width=800, height=600, keep_ar=False)
window.setWindowTitle("Qt Picamera2 App")
layout.addWidget(qpicamera2)
label = QLabel()
label.move(10,10)
label.setText('sadasd')
window.setLayout(layout)

picam2.start()
# qpicamera2.
# qpicamera2.show()
window.show()
app.exec_()