import cv2
import requests
import json
from messaging import get_mqtt_client
# import threading

def resize(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def single_img():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread('concert.jpg')
    img = resize(img, 25)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey()


def webcam():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2400)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            loc = None
            if(0 < x < 500):
                loc = 99
            elif 500 <= x < 850:
                loc = 1
            elif x >= 850:
                loc = 2
            cv2.putText(img, f"Steve Dunstan, Location {loc}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()


def on_message(client, userdata, message):
    try:
        msg_data = message.payload.decode('utf-8')
        camera_request = json.loads(msg_data)
        # TODO: locate shopper ID by face
        shopper_id = 1
        tx = camera_request['tx']
        shopper_url = f"http://localhost:5000/shopper/{tx}/{shopper_id}"
        print("PUT", shopper_url)
        requests.put(shopper_url)
    except Exception as e:
        print(e)



mqtt = get_mqtt_client(on_message)
mqtt.loop_start()
# threading.Thread(target=mqtt.loop_forever).start()
webcam()