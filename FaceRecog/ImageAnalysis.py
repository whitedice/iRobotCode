import face_recognition
import cv2
import numpy as np
import json


def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def load_encodings(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return {name: np.array(encoding) for name, encoding in data.items()}


def image_Analysis(image):
    image = cv2.imread(image)
    if image is None:
        print("Das Bild konnte nicht gefunden werden.")
        exit()

    small_image = resize_image(image, scale_percent= 50)

    _, compressed_image = cv2.imencode('.jpg', small_image, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    compressed_image = cv2.imdecode(compressed_image, cv2.IMREAD_COLOR)

    face_encoding = face_recognition.face_encodings(compressed_image)[0]

    return face_encoding


# Liste mit Namen die der Roboter Mag
liked = ["Nhan"]


if __name__ == '__main__':
    unknown_encoding = image_Analysis('picture.jpg')
    loaded_encodings = load_encodings('known_faces.json')

    found = 0

    results = []
    for name, encoding in loaded_encodings.items():
        if unknown_encoding is None:
            break
        result = face_recognition.compare_faces([encoding], unknown_encoding)
        if result[0]:
            if (name in liked):
                found = 1
            else:
                found = 2

    if found == 0:
        print("randomManeuver")
    elif found == 1:
        print("stopMovement")
    elif found == 2:
        print("runAway")