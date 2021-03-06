"""This module contains KPCAgent-class"""

import time
from typing import Callable

from keypad import Keypad
from ledboard import LEDBoard


class KPCAgent:
    """This is the main agent connecting all of the classes together.
    The logic within the passcode-box is here."""

    def __init__(self):
        self.keypad: Keypad = Keypad()
        self.led_board: LEDBoard = LEDBoard(keypad=self.keypad)
        self.password_path: str = "password.txt"
        self.override_signal: int or str or None = None
        self.password_buffer: str = ""
        self.password_buffer_old: str = ""
        self.current_signal = None
        self.led_id: int or None = None
        self.led_duration_sec: int or None = None

    def reset_passcode_entry(self) -> None:
        """Clear the passcode-buffer and initiate a “power up”
        lighting sequence on the LED Board."""
        self.password_buffer = ""
        self.led_board.power_up()

    def append_next_password_digit(self):
        """Appends the next digit to the password."""
        self.password_buffer += str(self.current_signal)

    def reset_agent(self):
        """Resets the agent"""
        self.override_signal = None
        self.password_buffer = ""

    def get_next_signal(self) -> int:
        """Return the override signal, if it is non-blank;
        otherwise query the keypad for the next pressed key."""
        if self.override_signal is not None:
            override_signal = self.override_signal
            self.override_signal = None
            return override_signal
        return self.keypad.get_key_pressed()

    def verify_login(self) -> None:
        """Check that the password just entered via the keypad
        matches that in the password file.
        Also, this should call the LED Board to initiate
        the appropriate lighting pattern for login success
        or failure"""
        file = open(self.password_path, "r")
        correct_password: str = file.read()
        file.close()
        if self.password_buffer == correct_password:
            self.override_signal = 'Y'
            self.led_success()
        else:
            self.override_signal = 'N'
            self.led_failure()

    def validate_passcode_change(self, password: str) -> None:
        """Check that the new password is legal and changes it."""

        def valid_passcode() -> bool:
            if len(password) < 4:
                return False
            accepted_char: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            for char in password:
                if char not in accepted_char:
                    return False
            return True

        if valid_passcode():
            file = open(self.password_path, "w")
            file.write(self.password_buffer)
            self.led_success()
        else:
            self.led_failure()

    def light_one_led(self):
        """Lights the led specified with id and duration_sec."""
        self.led_board.turn_on(self.led_id)
        time.sleep(self.led_duration_sec)
        self.led_board.turn_off(self.led_id)
        self.led_id = None
        self.led_duration_sec = None

    def flash_leds(self):
        """Flashed all leds once"""
        self.led_board.flash()

    def twinkle_leds(self):
        """Twinkles all leds."""
        self.led_board.twinkle()

    def exit_action(self):
        """Call the LED Board to initiate the “power down”
        lighting sequence."""
        self.led_board.power_down()

    @staticmethod
    def do_action(action: Callable[[], bool]):
        """Executes the action"""
        return action()

    def led_success(self) -> None:
        """The LED-lighting pattern when succeeded"""
        self.led_board.twinkle()

    def led_failure(self) -> None:
        """The LED-lighting pattern when failed"""
        self.led_board.flash()

    def refresh_agent(self):
        """Resets the agent."""
        self.password_buffer_old = ""
        self.led_board.power_up()

    def cache_first_password(self):
        """Caches the first password typed."""
        self.password_buffer_old = self.password_buffer
        self.password_buffer = ""

    def compare_new_password(self):
        """Compares to passwords and saves it if they matched"""
        if self.password_buffer == self.password_buffer_old:
            file = open(self.password_path, "w")
            file.write(self.password_buffer)
        # print("new1", self.password_buffer_old)
        # print("new2", self.password_buffer)
        # print("alt i orden?", self.password_buffer == self.password_buffer_old)
        self.password_buffer_old = ""
        self.password_buffer = ""

    def save_led_id(self):
        self.led_id = self.current_signal

    def append_led_duration(self):
        if self.led_duration_sec is None:
            self.led_duration_sec = self.current_signal
        else:
            self.led_duration_sec = int(str(self.led_duration_sec) + str(self.current_signal))

