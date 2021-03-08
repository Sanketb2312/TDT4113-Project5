import time

from keypad import Keypad
from ledboard import LEDBoard


class KPCAgent:
    def __init__(self):
        self.keypad: Keypad = Keypad()
        self.led_board: LEDBoard = LEDBoard()
        self.password_path: str = "password.txt"
        self.override_signal: int or None = None
        self.password_buffer: str = ""

    def reset_passcode_entry(self) -> None:
        """Clear the passcode-buffer and initiate a “power up”
        lighting sequence on the LED Board."""
        self.password_buffer = ""
        self.led_board.power_up()


    def append_next_password_digit(self, signal):
        self.password_buffer += signal

    def reset_agent(self):
        self.override_signal = None
        self.password_buffer = ""


    def active_agent(self):
        return self.override_signal == "Y"


    def get_next_signal(self) -> int:
        """Return the override signal, if it is non-blank;
        otherwise query the keypad for the next pressed key."""
        if self.override_signal is not None:
            return self.override_signal
        return self.keypad.get_key_pressed()

    def verify_login(self) -> None:
        """Check that the password just entered via the keypad
        matches that in the password file.
        Also, this should call the LED Board to initiate
        the appropriate lighting pattern for login success
        or failure"""
        file = open(self.password_path, "r")
        correct_password: str = file.read()
        if self.password_buffer == correct_password:
            self.override_signal = 'Y'
        else:
            self.override_signal = 'N'
        self.led_board.success()

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
            self.led_board.success()
        else:
            self.led_board.failure()

    def light_one_led(self, led_id: int, duration_sec: int):
        """Lights the led specified with id and duration_sec."""
        self.led_board.turn_on(led_id)
        time.sleep(duration_sec)
        self.led_board.turn_off(led_id)

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