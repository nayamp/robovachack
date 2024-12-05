import RPi.GPIO as GPIO
import time
import serial
import struct
import math

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering

# Set up PWM on GPIO 18
pwm_pin = 18
GPIO.setup(pwm_pin, GPIO.OUT)

# Set up UART on GPIO 15
uart_port = '/dev/serial0'  # UART port on Raspberry Pi 4
baud_rate = 115200  # Baud rate for lidar (check your lidar's specification)

# Initialize PWM on GPIO 18 (spin speed control)
pwm_freq = 50  # 50 Hz frequency for controlling PWM
pwm_duty_cycle = 50  # 50% duty cycle (adjust this for speed control)
pwm = GPIO.PWM(pwm_pin, pwm_freq)
pwm.start(pwm_duty_cycle)

# Initialize UART for reading lidar data
ser = serial.Serial(uart_port, baud_rate, timeout=1)

# Variables for angle and distance
angle = 0  # Starting angle (in degrees)
distance_data = []  # To store the (x, y) points for the point cloud

def read_lidar_data():
    """
    Read a line of data from the lidar.
    The data is expected to be in binary format (not ASCII text).
    """
    try:
        if ser.in_waiting > 0:  # If there is data to read
            raw_data = ser.read(9)  # Read 9 bytes (assuming packet length of 9 bytes for example)
            if len(raw_data) == 9:
                return raw_data
        return None
    except Exception as e:
        print(f"Error reading lidar data: {e}")
        return None

def parse_lidar_data(raw_data):
    """
    Parse the raw lidar data.
    Assumption: The first 2 bytes represent the distance (little-endian, 16-bit unsigned integer).
    """
    try:
        # Assuming the first 2 bytes represent the distance in little-endian format
        distance = struct.unpack('<H', raw_data[:2])[0]  # '<H' for little-endian unsigned short
        # If more data follows, you can unpack additional fields here based on the lidar's protocol.
        return distance
    except Exception as e:
        print(f"Error parsing lidar data: {e}")
        return None

def generate_point_cloud(distance, angle):
    """
    Convert polar coordinates (distance, angle) to Cartesian coordinates (x, y).
    Angle is in degrees.
    """
    # Convert angle to radians
    angle_radians = math.radians(angle)

    # Convert polar to cartesian coordinates
    x = distance * math.cos(angle_radians)
    y = distance * math.sin(angle_radians)
    
    # Return the point as a tuple (x, y)
    return (x, y)

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
                    
                    # Generate the point cloud (x, y coordinates) for this distance and angle
                    point = generate_point_cloud(distance, angle)
                    distance_data.append(point)  # Save the point to the distance_data list
                    print(f"Point: {point}")  # Print the point (x, y)

                    # Optionally, you could save the point cloud to a file or process it further.
                else:
                    print("Failed to parse lidar data.")
            
            # Increment the angle (adjust as per your lidar's scanning speed)
            angle += 1  # Increase by 1 degree per reading (adjust for your lidar's rotation speed)
            if angle >= 360:
                angle = 0  # Reset angle after a full 360-degree rotation
            
            # Control the PWM to spin the lidar (adjust if necessary)
            pwm.ChangeDutyCycle(pwm_duty_cycle)
            
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
