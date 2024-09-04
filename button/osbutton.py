import os, time

class GPIOController:
    def __init__(self, gpio_id, gpio_index):
        """Initialize the GPIO controller with the specified GPIO ID and index."""
        self.gpio_id = gpio_id
        self.gpio_index = gpio_index
        self.gpio_base_path = "/sys/class/gpio"
        self.exported = False
        self.prev_value = "0"

    def export(self):
        """Export the GPIO pin to make it available."""
        if not os.path.exists(f"{self.gpio_base_path}/{self.gpio_index}"):
            try:
                with open(f"{self.gpio_base_path}/export", 'w') as f:
                    f.write(f"{self.gpio_id}")
                self.exported = True
            except IOError as e:
                print(f"Error exporting GPIO {self.gpio_id}: {e}")
                self.exported = False
        else:
            print(f"GPIO {self.gpio_id} is already exported.")
            self.exported = True

    def set_direction(self, direction):
        """Set the direction of the GPIO pin (in or out)."""
        if self.exported:
            try:
                with open(f"{self.gpio_base_path}/{self.gpio_index}/direction", 'w') as f:
                    f.write(direction)
            except IOError as e:
                print(f"Error setting direction for GPIO {self.gpio_index}: {e}")

    def read_value(self):
        """Read the current value of the GPIO pin."""
        if self.exported:
            try:
                with open(f"{self.gpio_base_path}/{self.gpio_index}/value", 'r') as f:
                    value = f.read().strip()
                    
                    return value
            except IOError as e:
                print(f"Error reading value from GPIO {self.gpio_index}: {e}")
                return False
        else:
            print(f"GPIO {self.gpio_id} is not exported.")
            return False
        
    def check_pushed(self):
        cur_value = self.read_value()
        print(cur_value, self.prev_value, type(cur_value), type(self.prev_value))
        if cur_value != None:
            if self.prev_value == "0" and cur_value == "1":
                self.prev_value = "1"
                return True
            elif self.prev_value == "1" and cur_value == "0":
                self.prev_value = "0"
        
        return False


    def unexport(self):
        """Unexport the GPIO pin to release it."""
        if self.exported:
            try:
                with open(f"{self.gpio_base_path}/unexport", 'w') as f:
                    f.write(f"{self.gpio_id}")
                self.exported = False
            except IOError as e:
                print(f"Error unexporting GPIO {self.gpio_id}: {e}")

    def cleanup(self):
        """Ensure the GPIO pin is unexported."""
        self.unexport()


# Example usage
if __name__ == "__main__":
    # GPIO ID 및 인덱스 설정
    gpio_id = 391
    gpio_index = "PH.00"

    # GPIOController 객체 생성
    gpio = GPIOController(gpio_id, gpio_index)

    try:
        # GPIO 내보내기 (export) 및 방향 설정
        gpio.unexport()
        gpio.export()
        gpio.set_direction("in")

        while True:
            print(gpio.check_pushed())
            # print(gpio.read_value())
            time.sleep(0.05)

        # # GPIO 값 읽기
        # value = gpio.read_value()
        # if value is not None:
        #     print(f"GPIO {gpio_index} value is: {value}")  # 1이면 HIGH, 0이면 LOW

    finally:
        # GPIO 해제 (unexport)
        gpio.cleanup()
        print(f"GPIO {gpio_index} has been unexported.")
