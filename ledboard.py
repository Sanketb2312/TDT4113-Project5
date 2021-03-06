from time import *
from GPIOSimulator_v5 import *

GPIO = GPIOSimulator()

# Format: (High, Low)
LED_MAP = [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)]
C_PINS = [PIN_CHARLIEPLEXING_0, PIN_CHARLIEPLEXING_1, PIN_CHARLIEPLEXING_2]


class LEDBoard:

    def get_pins(self, k):
        """Returns pins: (High, Low, Inactive)"""
        c_pin_h = C_PINS[(LED_MAP[k])[0]]
        c_pin_l = C_PINS[(LED_MAP[k])[1]]

        # Find inactive pin
        c_pin_inactive = None
        for i in range(3):
            if i != LED_MAP[k][0] and i != LED_MAP[k][1]:
                c_pin_inactive = C_PINS[i]
                break

        return c_pin_h, c_pin_l, c_pin_inactive

    def turn_on(self, k):
        pins = self.get_pins(k)
        GPIO.setup(pins[0], GPIO.OUT)
        GPIO.output(pins[0], GPIO.HIGH)
        GPIO.setup(pins[1], GPIO.OUT)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.setup(pins[2], GPIO.IN)

    def turn_off(self, k):
        pins = self.get_pins(k)
        GPIO.setup(pins[0], GPIO.IN)
        GPIO.setup(pins[1], GPIO.IN)

    def power_up(self):
        """Light up one led at a time"""
        leds = []
        for k in range(0, 6):
            leds.append(k)
            self.flash(leds, 0.2)

    def flash(self, leds=[k for k in range(6)], t_flash=1):
        """Twinkle fast to light up all"""
        start = time()
        while time() - start < t_flash:
            self.twinkle(leds=leds, t_sleep=0.01)

    def twinkle(self, leds=[k for k in range(6)], t_sleep=0.1):
        for k in leds:
            self.turn_on(k)
            GPIO.show_leds_states()
            sleep(t_sleep)
            self.turn_off(k)

    def power_down(self):
        """Light up all, then turn off one at a time"""
        leds = [k for k in range(0, 6)]
        for k in range(0, 6):
            self.flash(leds, 0.2)
            leds.pop(len(leds) - 1)

    def success(self):
        """Should light up if login succeeded"""
        pass

    def failure(self):
        """Should light up if failed"""
        pass
