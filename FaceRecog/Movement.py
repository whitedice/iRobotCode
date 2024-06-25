
import subprocess
import random
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


def run_script(script_name):
    python37_path = 'C:\\Users\\eisen\\AppData\\Local\\Microsoft\\WindowsApps\\python3.7.exe' 

    command = [python37_path, script_name]

    result = subprocess.run(command, text=True, capture_output=True)

    if result.returncode == 0:
        if (result.stdout == "runAway"):
            runAway()
        elif (result.stdout == "randomManeuver"):
            random_maneuver()
        elif (result.stdout == "stopMovement"):
            stop_movement()
        else:
            # Script beenden
            print("Das Skript wurde beendet.")
            exit()
            
    else:
        print("Fehler bei der Ausführung des Skripts:")
        print(result.stderr)

    return result.stdout


while True:
    run_script("ImageAnalysis.py")