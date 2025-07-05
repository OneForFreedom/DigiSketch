from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.rotary_encoder import RotaryEncoder
import board
import busio
from adafruit_sh1107 import SH1107_I2C  # Make sure you have this lib installed

class EtchASketchKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # I2C for SH1107 (adjust pins to your wiring)
        i2c = busio.I2C(board.GP15, board.GP14)
        self.oled_display = SH1107_I2C(128, 128, i2c)
        self.oled_display.fill(0)
        self.oled_display.show()

        self.x = 64
        self.y = 64
        self.canvas = [[0]*128 for _ in range(128)]

        self.encoder1 = RotaryEncoder(pin_a=board.GP0, pin_b=board.GP1)
        self.encoder2 = RotaryEncoder(pin_a=board.GP2, pin_b=board.GP3)
        self.modules = [self.encoder1, self.encoder2]

        self.reset_pin = board.GP4

    def process_encoder(self):
        delta_x = self.encoder1.get_delta()
        delta_y = self.encoder2.get_delta()

        if delta_x != 0:
            self.x = max(0, min(127, self.x + delta_x))
            self.canvas[self.y][self.x] = 1
        if delta_y != 0:
            self.y = max(0, min(127, self.y + delta_y))
            self.canvas[self.y][self.x] = 1

    def reset_canvas(self):
        self.canvas = [[0]*128 for _ in range(128)]
        self.x = 64
        self.y = 64
        self.oled_display.fill(0)
        self.oled_display.show()

    def scan(self):
        super().scan()
        # Check reset button (active low assumed)
        if not self._pins[self.reset_pin].value:
            self.reset_canvas()

        self.process_encoder()

        for y in range(128):
            for x in range(128):
                color = 1 if self.canvas[y][x] else 0
                self.oled_display.pixel(x, y, color)
        self.oled_display.show()

keyboard = EtchASketchKeyboard()

if __name__ == "__main__":
    keyboard.go()
