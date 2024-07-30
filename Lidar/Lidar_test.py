from Lidar_sensor import *
import time

def main():
    sensor = Lidar(port='/dev/ttyUSB0', baudrate=115200, timeout=2)
    
    try:
        sensor.enable_modbus()  # Enable Modbus mode and save settings
        #time.sleep(2)  # Ensure settings take effect

        while True:
            distance = sensor.read_distance()
            if distance != -1:
                print(f"Distance = {distance} cm")
            else:
                print("Failed to read distance")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()

if __name__ == "__main__":
    main()
