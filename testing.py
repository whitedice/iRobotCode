from irobot_edu_sdk.backend.bluetooth import Bluetooth

# Connect to robot over Bluetooth Low Energy.
backend0 = Bluetooth('') # Connects to the first BLE robot detected.
backend1 = Bluetooth('ROOT') # Use robot named 'ROOT'
