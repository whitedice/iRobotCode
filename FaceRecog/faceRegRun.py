import face_recognition
import cv2
import numpy as np
import json
import random
from PIL import Image

import asyncio
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import Create3

device_name = "Jonny"

color_forward = (0x00, 0xFF, 0x00)
color_backward = (0xFF, 0x00, 0x80)
color_left = (0x00, 0x59, 0xFF)
color_right = (0xFF, 0xAE, 0x00)
color_none = (0xFF, 0xFF, 0xFF)

# Create a robot instance
robot = Create3(Bluetooth(device_name))

wheel_speed_in_cm = 500
wheel_speed_in_cm_180_Drehung = 3000

async def rotate_180():
    await robot.set_wheel_speeds(wheel_speed_in_cm, -wheel_speed_in_cm)
    await asyncio.sleep(1.5)  
    print("Completed 180 degree rotation")

async def move_away():
    await robot.set_wheel_speeds(wheel_speed_in_cm, wheel_speed_in_cm)
    await asyncio.sleep(1)  # Move forward for 1 second
    await robot.stop()
    print("Moved forward for 1 second")

async def runAway():
    await rotate_180()
    await move_away()

async def stop_movement():
    await robot.stop()
    event_is_moving.clear()
    print("Stopped")

def generate_random_integer(min_val, max_val):
    return random.randint(min_val, max_val)

async def random_maneuver():
    # Ensure no other movements are happening
    if not event_is_moving.is_set():
        event_is_moving.set()

        # First random maneuver
        random_numberLeft1 = generate_random_integer(-500, 500)
        random_numberRight1 = generate_random_integer(-500, 500)
        print("Random maneuver 1")
        await robot.set_wheel_speeds(random_numberLeft1, random_numberRight1)
        await robot.play_tone(1600, 0.2)
        await asyncio.sleep(0.5)

        # Second random maneuver
        random_numberLeft2 = generate_random_integer(-500, 500)
        random_numberRight2 = generate_random_integer(-500, 500)
        print("Random maneuver 2")
        await robot.set_wheel_speeds(random_numberLeft2, random_numberRight2)
        await robot.play_tone(800, 0.3)
        await asyncio.sleep(0.5)

        await stop_movement()

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


while True:
    unknown_encoding = image_Analysis('obama.jpg')
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
        print("Keine Übereinstimmung gefunden.")
        asyncio.run(random_maneuver())
    elif found == 1:
        print("Der Roboter mag diese Person.")
    elif found == 2:
        print("Der Roboter mag diese Person nicht.")
        asyncio.run(runAway())