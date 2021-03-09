"""Keypad simulation"""
from time import sleep, time
from GPIOSimulator_v5 import GPIOSimulator, keypad_row_pins, keypad_col_pins

GPIO = GPIOSimulator()

for row_pin in keypad_row_pins:
    GPIO.setup(row_pin, GPIO.OUT)
for col_pin in keypad_col_pins:
    GPIO.setup(col_pin, GPIO.IN, state=GPIO.LOW)

KEYS = list(i for i in range(1, 10))
KEYS.extend(["*", 0, "#"])

MAX_PRESS_DURATION = 1


def poll():
    """Returns current key pressed, None is nothing is pressed"""
    for _r, r_pin in enumerate(keypad_row_pins):
        GPIO.output(r_pin, GPIO.HIGH)

        for _c, c_pin in enumerate(keypad_col_pins):
            if GPIO.input(c_pin) == GPIO.HIGH:
                GPIO.output(r_pin, GPIO.LOW)
                return KEYS[_r * 3 + _c]

        GPIO.output(r_pin, GPIO.LOW)
    return None


class Keypad:
    """Reads user input"""

    def __init__(self):
        self.__prev_pressed = None
        self.__t_prev_pressed = 0

    def get_key_pressed(self):
        """Polls until a key is pressed and returns the key. If the same key is pressed longer than
            MAX_PRESS_DURATION, it is seen as an extra key press."""
        pressed = None
        released = False
        while pressed is None or (
            self.__prev_pressed is not None and (
                self.__prev_pressed == pressed and (
                    not released and time() -
                self.__t_prev_pressed < MAX_PRESS_DURATION))):
            pressed = poll()
            if pressed is None:
                released = True
            sleep(0.008)

        self.__prev_pressed = pressed
        self.__t_prev_pressed = time()
        return pressed
