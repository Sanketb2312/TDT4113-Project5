from time import *
from GPIOSimulator_v5 import *
from keypad import Keypad

GPIO = GPIOSimulator()

# Format: (High, Low)
LED_MAP = [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)]


class Charlieplexer:

    def __init__(self, keypad):
        self.keypad = keypad

    def get_pins(self, k):
        """Returns pins: (High, Low, Inactive)"""
        c_pin_h = charlieplexing_pins[(LED_MAP[k])[0]]
        c_pin_l = charlieplexing_pins[(LED_MAP[k])[1]]

        # Find inactive pin
        c_pin_inactive = None
        for i in range(3):
            if i != LED_MAP[k][0] and i != LED_MAP[k][1]:
                c_pin_inactive = charlieplexing_pins[i]
                break

        return c_pin_h, c_pin_l, c_pin_inactive

    def turn_on(self, k):
        """Turn on the specified LED"""
        pins = self.get_pins(k)
        GPIO.setup(pins[0], GPIO.OUT)
        GPIO.output(pins[0], GPIO.HIGH)
        GPIO.setup(pins[1], GPIO.OUT)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.setup(pins[2], GPIO.IN)

        GPIO.show_leds_states()

    def turn_off(self, k):
        """Turn off the specified LED"""
        pins = self.get_pins(k)
        GPIO.setup(pins[0], GPIO.IN)
        GPIO.setup(pins[1], GPIO.IN)

        GPIO.show_leds_states()

    def power_up(self):
        """Light up one LED at a time"""
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
        """Turn on and off LEDs in sequence"""
        for k in leds:
            self.turn_on(k)
            sleep(t_sleep)
            self.turn_off(k)

    def power_down(self):
        """"Light up all, then turn off one at a time"""
        leds = [k for k in range(0, 6)]
        for k in range(0, 6):
            self.flash(leds, 0.2)
            leds.pop(len(leds) - 1)

    def user_turn_on(self):
        """Turn one user-specified LED on for a user specified number of seconds"""

        print("Specify LED:")
        led = self.keypad.get_key_pressed()
        if not isinstance(led, int):
            print("Expecting an integer.")
            return
        elif led < 0 or led > 5:
            print("Choose a LED between 0 and 5")
            return

        print("Specify duration, finish with '*':")
        duration = ""
        while True:
            inp = self.keypad.get_key_pressed()
            if inp == "*":
                if len(duration) == 0:
                    duration = 0
                else:
                    duration = int(duration)

                self.turn_on(led)
                sleep(duration)
                self.turn_off(led)
                return

            elif isinstance(inp, int):
                duration += str(inp)
            else:
                print("Not a valid input.")
                return




