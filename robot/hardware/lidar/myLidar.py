import numpy as np
import time
import serial
import struct
import math
import RPi.GPIO as GPIO
##import open3d as o3d
import matplotlib.pyplot as plt

# GPIO Pin Setup
PWM_PIN = 18  # GPIO pin for controlling the lidar rotation
RX_PIN = 15   # GPIO pin for receiving lidar data
PWM_FREQUENCY = 50  # Frequency of PWM signal (Hz)

# Initialize serial connection for lidar
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)  # Set GPIO 18 as output for PWM
GPIO.setup(RX_PIN, GPIO.IN)    # Set GPIO 15 as input for lidar data

# Create a PWM instance and start it
pwm = GPIO.PWM(PWM_PIN, PWM_FREQUENCY)
pwm.start(50)  # Start PWM with 50% duty cycle (adjust based on your lidar)

# SLAM parameters
angle = 0  # Starting angle (in degrees)
scan_res = 1  # Scan resolution (degrees)
max_range = 10  # Maximum range for lidar
lidar_data = []  # Store (x, y) points for visualization

# Create an Open3D point cloud object for visualization

def read_lidar_data():
    """
    Read a line of data from the lidar via the serial connection.
    """
    try:
        if ser.in_waiting > 0:
            raw_data = ser.read(9)  # Read 9 bytes (assuming packet length)
            ##if len(raw_data) == 9:
            return raw_data
        return None
    except Exception as e:
        print(f"Error reading lidar data: {e}")
        return None

def parse_lidar_data(raw_data):
    """
    Parse the raw lidar data.
    Assumes the first 2 bytes represent the distance (little-endian, 16-bit unsigned integer).
    """
    try:
        data = struct.unpack('<H', raw_data[:2])[0]
        return data
    except Exception as e:
        print(f"Error parsing lidar data: {e}")
        return None
    
def main():
    global angle
    try:
        while True:
            # Read lidar data as raw bytes
            lidar_data = read_lidar_data()
            if lidar_data:
                # Parse the lidar data (extract meaningful values)
                distance = parse_lidar_data(lidar_data)
                if distance is not None:
                    print(f"Lidar Distance: {distance} mm")  # Example output, assuming distance is in mm
                else:
                    print("Failed to parse lidar data.")
            
            # Increment the angle (adjust as per your lidar's scanning speed)
            angle += 1  # Increase by 1 degree per reading (adjust for your lidar's rotation speed)
            if angle >= 360:
                angle = 0  # Reset angle after a full 360-degree rotation
            
            # Control the PWM to spin the lidar (adjust if necessary)
            ##pwm.ChangeDutyCycle(pwm_duty_cycle)
            
            # Sleep for a small amount of time to avoid flooding the output
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        # Cleanup GPIO and serial connections
        pwm.stop()
        GPIO.cleanup()
        ser.close()

if __name__ == "__main__":
    main()