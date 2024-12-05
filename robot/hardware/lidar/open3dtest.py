import numpy as np
import time
import serial
import struct
import math
import RPi.GPIO as GPIO
import open3d as o3d
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
point_cloud = o3d.geometry.PointCloud()

def read_lidar_data():
    """
    Read a line of data from the lidar via the serial connection.
    """
    try:
        if ser.in_waiting > 0:
            raw_data = ser.read(9)  # Read 9 bytes (assuming packet length)
            if len(raw_data) == 9:
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
        distance = struct.unpack('<H', raw_data[:2])[0]
        return distance
    except Exception as e:
        print(f"Error parsing lidar data: {e}")
        return None

def polar_to_cartesian(distance, angle):
    """
    Convert polar coordinates (distance, angle) to Cartesian (x, y).
    Angle is in degrees.
    """
    angle_rad = math.radians(angle)
    x = distance * math.cos(angle_rad)
    y = distance * math.sin(angle_rad)
    return x, y

def update_point_cloud():
    """
    Collect lidar data, process it, and update the point cloud.
    """
    global angle
    raw_data = read_lidar_data()
    if raw_data:
        distance = parse_lidar_data(raw_data)
        if distance and distance <= max_range:
            x, y = polar_to_cartesian(distance, angle)
            lidar_data.append([x, y])  # Store the data
            # Add to Open3D point cloud
            point_cloud.points = o3d.utility.Vector3dVector(np.array(lidar_data))
            
            # Optionally, print the most recent point
            print(f"Point at {x:.2f}, {y:.2f} meters.")
            
        # Update the angle (e.g., assume each reading corresponds to a 1-degree step)
        angle += scan_res
        if angle >= 360:
            angle = 0

def visualize_point_cloud():
    """
    Visualize the lidar data in real-time using Open3D.
    """
    # Initialize the visualization window
    o3d.visualization.draw_geometries([point_cloud], window_name="Lidar SLAM", width=800, height=600)

def run_slam():
    """
    Run the SLAM loop: collect data, update point cloud, and visualize.
    """
    try:
        while True:
            update_point_cloud()
            visualize_point_cloud()
            time.sleep(0.1)  # Adjust as needed for your lidar's scanning speed
    except KeyboardInterrupt:
        print("SLAM finished.")

if __name__ == '__main__':
    try:
        run_slam()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pwm.stop()  # Stop PWM when done
        GPIO.cleanup()  # Clean up GPIO settings
