import Jetson.GPIO as GPIO
import time

# GPIO 핀 설정
BUTTON_PIN = 31  # 버튼 핀 번호를 실제 GPIO 핀 번호로 변경

# 변수 초기화
counter = 0

# GPIO 모드 설정
GPIO.setmode(GPIO.BOARD)  # 또는 GPIO.BOARD, 핀 번호 모드에 맞게 설정

# 핀 설정
GPIO.setup(BUTTON_PIN, GPIO.IN)  # 버튼 핀을 입력으로 설정하고 풀업 저항 사용

def button_pressed(channel):
    """버튼 눌림 핸들러"""
    global counter
    counter += 1
    print(f"Button pressed! Counter: {counter}")

# 인터럽트 설정
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed)

try:
    while True:
        time.sleep(1)  # 1초 대기
except KeyboardInterrupt:
    print("Program exited cleanly")
finally:
    GPIO.cleanup()
