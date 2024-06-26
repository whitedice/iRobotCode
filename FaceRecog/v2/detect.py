import cv2
import os
import numpy as np

def detect_face(img):
    """ Funktion zum Erkennen von Gesichtern im Bild. """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if len(faces) == 0:
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):
    """ Funktion zum Vorbereiten der Trainingsdaten. """
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    label = 0
    label_names = {}
    
    for dir_name in dirs:
        if not dir_name.startswith("person"):
            continue
        label_names[label] = dir_name
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face, rect = detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(label)
        label += 1
    return faces, labels, label_names

def predict(test_img):
    """ Funktion zur Vorhersage der Person im Bild. """
    face, rect = detect_face(test_img)
    if face is not None:
        label, confidence = face_recognizer.predict(face)
        label_text = label_names[label] if confidence < 100 else "Unbekannt"
        return label_text
    return "Unbekannt"

# Trainingsdaten vorbereiten und das Modell trainieren
faces, labels, label_names = prepare_training_data("train_images")
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

# Bild laden, das getestet werden soll
test_img1 = cv2.imread('image.png')

# Das Ergebnis vorhersagen
person_identified = predict(test_img1)
print(f"Person: {person_identified}")
