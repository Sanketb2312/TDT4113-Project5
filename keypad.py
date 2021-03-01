from GPIOSimulator_v5 import *
from time import sleep

GPIO = GPIOSimulator()
ROW_PINS = [PIN_KEYPAD_ROW_0, PIN_KEYPAD_ROW_1, PIN_KEYPAD_ROW_2, PIN_KEYPAD_ROW_3]
COL_PINS = [PIN_KEYPAD_COL_0, PIN_KEYPAD_COL_1, PIN_KEYPAD_COL_2]

# Setup
for row_pin in ROW_PINS:
    GPIO.setup(row_pin, GPIO.OUT)
for col_pin in COL_PINS:
    GPIO.setup(col_pin, GPIO.IN, state=GPIO.LOW)

KEYS = [i for i in range(1, 10)]
KEYS.extend(["*", 0, "#"])


class Keypad:

    def poll(self):
        for r in range(0, len(ROW_PINS)):
            row_pin = ROW_PINS[r]
            GPIO.output(row_pin, GPIO.HIGH)

            for c in range(0, len(COL_PINS)):
                col_pin = COL_PINS[c]
                if GPIO.input(col_pin) == GPIO.HIGH:
                    GPIO.output(row_pin, GPIO.LOW)
                    return KEYS[r * 3 + c]

            GPIO.output(row_pin, GPIO.LOW)
        return None

    def get_key_pressed(self):
        pass
