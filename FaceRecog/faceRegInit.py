import face_recognition
import cv2
import numpy as np
import json

def save_encodings(encodings_dict, filename):
    # Bereitet das Dictionary für das JSON-Format vor, indem es NumPy Arrays in Listen umwandelt
    json_ready_dict = {name: np.array(encoding).tolist() for name, encoding in encodings_dict.items()}
    with open(filename, 'w') as f:
        json.dump(json_ready_dict, f)

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def image_Analysis(image):
    image = cv2.imread(image)
    if image is None:
        print("Das Bild konnte nicht gefunden werden.")
        exit()

    small_image = resize_image(image, scale_percent = 50)

    _, compressed_image = cv2.imencode('.jpg', small_image, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    compressed_image = cv2.imdecode(compressed_image, cv2.IMREAD_COLOR)

    face_encoding = face_recognition.face_encodings(compressed_image)[0]

    return face_encoding

biden_encoding = image_Analysis("biden.jpg")
obama_encoding = image_Analysis("obama.jpg")

known_faces = {
    "Biden": biden_encoding,
    "Obama": obama_encoding
}

save_encodings(known_faces, "known_faces.json")
