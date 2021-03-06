from GPIOSimulator_v5 import *
from time import sleep, time

GPIO = GPIOSimulator()

# Setup, should be in init maybe?
for row_pin in keypad_row_pins:
    GPIO.setup(row_pin, GPIO.OUT)
for col_pin in keypad_col_pins:
    GPIO.setup(col_pin, GPIO.IN, state=GPIO.LOW)

KEYS = [i for i in range(1, 10)]
KEYS.extend(["*", 0, "#"])

MAX_PRESS_DURATION = 1

class Keypad:

    def __init__(self):
        self.prev_pressed = None
        self.t_prev_pressed = 0

    def poll(self):
        """Returns current key pressed, None is nothing is pressed"""
        for r in range(0, len(keypad_row_pins)):
            row_pin = keypad_row_pins[r]
            GPIO.output(row_pin, GPIO.HIGH)

            for c in range(0, len(keypad_col_pins)):
                col_pin = keypad_col_pins[c]
                if GPIO.input(col_pin) == GPIO.HIGH:
                    GPIO.output(row_pin, GPIO.LOW)
                    return KEYS[r * 3 + c]

            GPIO.output(row_pin, GPIO.LOW)
        return None

    def get_key_pressed(self):
        """Polls until a key is pressed and returns the key. If the same key is pressed longer than
            MAX_PRESS_DURATION, it is seen as an extra key press."""
        pressed = None
        released = False
        while pressed is None or (self.prev_pressed is not None and (self.prev_pressed == pressed and
                                  (not released and time() - self.t_prev_pressed < MAX_PRESS_DURATION))):
            pressed = self.poll()
            if pressed is None:
                released = True
            sleep(0.008)

        self.prev_pressed = pressed
        self.t_prev_pressed = time()
        return pressed

