import time
import os

from picamera2 import Picamera2, Preview
import pyzbar
import cv2 as cv
import numpy as np
import tensorflow as tf
import pickle
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


facenet = FaceNet()
encoder = LabelEncoder()

faces_embeddings = np.load("./src/embeddings.npz")
Y = faces_embeddings["arr_1"]

encoder.fit(Y)

face_detector = cv.CascadeClassifier("./src/haarcascade_frontalface_default.xml")
model = pickle.load(open("./src/my_svm_model_160x160.pkl", "rb"))


cam = Picamera2()
width = 1024
height = 768

cam.configure(
    cam.create_video_configuration(main={"format": "RGB888", "size": (width, height)})
)

cam.start()

fps = 0
labels = []
start_time = time.time()

while True:
    frame = cam.capture_array()
    rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    gray_img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    faces = face_detector.detectMultiScale(
        gray_img, 1.3, 5, minSize=(int(width / 7), int(height / 7))
    )

    qrs = pyzbar.pyzbar.decode(gray_img)

    for qr in qrs:
        (x, y, w, h) = qr.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 4)
        qr_data = qr.data.decode("utf-8")
        qr_type = qr.type
        qr_text = f"{qr_data}"
        labels.append(qr_text)
        cv.putText(
            frame,
            qr_text,
            (x, y - 10),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3,
        )

    for x, y, w, h in faces:
        if (w > (width / 4)) & (h > (height / 4)):

            img = rgb_img[y : y + h, x : x + w]
            img = cv.resize(img, (160, 160))
            img = np.expand_dims(img, axis=0)
            ypred = facenet.embeddings(img)
            face_name = model.predict(ypred)
            label = encoder.inverse_transform(face_name)[0]
            labels.append(label)
            color = (14, 227, 46)
            description = label
            font_scale = 1
            thickness_lines = 3
        else:
            color = (222, 67, 29)
            description = "Please move closer"
            font_scale = 1.25
            thickness_lines = 4

        cv.rectangle(frame, (x, y), (x + w, y + h), color, 4)
        cv.putText(
            frame,
            str(f"{description}"),
            (x + 10, y - 20),
            cv.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color,
            thickness_lines,
            cv.LINE_AA,
        )

    fps += 1
    cv.imshow("Face Recognition", frame)
    elapsed_time = time.time() - start_time

    if elapsed_time >= 1.0:
        fps = fps / elapsed_time
        print(f"FPS: {fps:.2f}")
        print(f"Find: {len(labels)}, {labels}")

        fps = 0
        labels = []
        start_time = time.time()

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

    cv.imshow("Face Recognition", frame)
    if cv.waitKey(1) & ord("q") == 27:
        break

cam.stop()
cv.destroyAllWindows()
