# lidar_sensor.py

import serial
import time

class Lidar:
    OFFSET = 5  # cm    # 5cm의 오차보정을 위함

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=2):    #default Baudrate 115200bps
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout
        )

    def send_command(self, command) :
        self.ser.write(command)
        #time.sleep(0.5)  # 응답 대기 시간을 충분히 설정합니다
        response = self.ser.read(self.ser.in_waiting or 1)
        return response

    def enable_modbus(self):    #TF02-i 라이다 센서는 모드버스 활성화 우선적 시행해야함
        command = b'\x5A\x05\x15\x01\x75'  # Save settings and restart to take effect
        response = self.send_command(command)
        print(f"Sent: {command.hex()}, Received: {response.hex() if response else 'No response'}, Length: {len(response)}") #명령어 출력 함수(확인용)

    def read_distance(self) :
        command = b'\x01\x03\x00\x00\x00\x01\x84\x0A'  # Read distance command with provided CRC    (CRC는 문서에 적혀있는 default 값을 구성)
        response = self.send_command(command)
        print(f"Sent: {command.hex()}, Received: {response.hex() if response else 'No response'}, Length: {len(response)}")

        if len(response) < 7:
            print("Incomplete response")
            return -1

        addr, func, len_data, dh, dl, crc_low, crc_high = response[:7]  #거리값이 담겨있는 데이터 슬라이싱 및 파싱 

        if addr == 0x01 and func == 0x03 and len_data == 0x02:
            distance = (dh << 8) | dl   #dh == 거리값은 dh, dl로 나눠져있고 각각 distance의 상,하위 8비트로 구성되어있기에 반환된 거리값에서 distance를 파싱하는 부분
            return distance + self.OFFSET   #5cm 오차보정을 위해 OFFSET적용

        return -1

    def close(self):
        self.ser.close()
