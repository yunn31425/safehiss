import smbus
import time

class EasyLcd:
    # LCD I2C 주소 (i2cdetect 명령어로 확인한 주소)
    def __init__(self, bus_number=7, address=0x27):
        self.LCD_ADDRESS = address  # I2C 주소

        # 명령어 및 LCD 설정
        self.LCD_CHR = 1  # 문자 모드
        self.LCD_CMD = 0  # 명령어 모드

        # LCD 설정
        self.LCD_LINE_1 = 0x80  # LCD 첫 번째 라인
        self.LCD_LINE_2 = 0xC0  # LCD 두 번째 라인
        self.LCD_BACKLIGHT = 0x08  # 백라이트 켜기
        self.ENABLE = 0b00000100  # Enable 비트

        # I2C 인터페이스 초기화
        self.bus = smbus.SMBus(bus_number)  # I2C 버스 번호

        # LCD 초기화
        self.lcd_init()

    def lcd_byte(self, bits, mode):
        """Send byte to data pins."""
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.bus.write_byte(self.LCD_ADDRESS, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.bus.write_byte(self.LCD_ADDRESS, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        """Toggle enable."""
        time.sleep(0.0005)
        self.bus.write_byte(self.LCD_ADDRESS, (bits | self.ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.LCD_ADDRESS, (bits & ~self.ENABLE))
        time.sleep(0.0005)

    def lcd_init(self):
        """Initialize display."""
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)
        time.sleep(0.0005)

    def lcd_string(self, message, line):
        """Send string to display."""
        message = message.ljust(16, " ")
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(16):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def lcd_string_up(self, message, clear:bool = False):
        """Send string to the first line of the display."""
        if clear:
            self.lcd_clear()
        self.lcd_string(message, self.LCD_LINE_1)

    def lcd_string_down(self, message, clear:bool = False):
        """Send string to the second line of the display."""
        if clear:
            self.lcd_clear()
        self.lcd_string(message, self.LCD_LINE_2)

    def lcd_clear(self):
        self.lcd_string("                ", self.LCD_LINE_1)
        self.lcd_string("                ", self.LCD_LINE_2)

if __name__ == "__main__":
    # 객체 인스턴스 생성
    lcd = EasyLcd()

    # "Hello World" 출력
    lcd.lcd_string_up("Hello World!")
    lcd.lcd_string_down("Hello World!")
