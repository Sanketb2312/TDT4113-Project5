""" Project 5 Simulator """
from pynput.keyboard import Listener

PIN_CHARLIEPLEXING_0 = 0
PIN_CHARLIEPLEXING_1 = 1
PIN_CHARLIEPLEXING_2 = 2

PIN_KEYPAD_ROW_0 = 3
PIN_KEYPAD_ROW_1 = 4
PIN_KEYPAD_ROW_2 = 5
PIN_KEYPAD_ROW_3 = 6

PIN_KEYPAD_COL_0 = 7
PIN_KEYPAD_COL_1 = 8
PIN_KEYPAD_COL_2 = 9

charlieplexing_pins = [PIN_CHARLIEPLEXING_0, PIN_CHARLIEPLEXING_1, PIN_CHARLIEPLEXING_2]
keypad_row_pins = [PIN_KEYPAD_ROW_0, PIN_KEYPAD_ROW_1, PIN_KEYPAD_ROW_2, PIN_KEYPAD_ROW_3]
keypad_col_pins = [PIN_KEYPAD_COL_0, PIN_KEYPAD_COL_1, PIN_KEYPAD_COL_2]
keypad_pins = keypad_row_pins + keypad_col_pins
valid_pins = keypad_pins + charlieplexing_pins

N_LEDS = 6


class GPIOSimulator:
    """ Simulate Raspberry Pi GPIO for Project 5 """

    def __init__(self):
        # pin modes
        self.IN = 0
        self.OUT = 1
        self.__NO_SETUP = -1

        # pin states
        self.LOW = 0
        self.HIGH = 1
        self.__NO_SIGNAL = -1

        # led states
        self.OFF = 0
        self.ON = 1

        # private members
        self.__key_coord = {'1': (0, 0),
                            '2': (0, 1),
                            '3': (0, 2),
                            '4': (1, 0),
                            '5': (1, 1),
                            '6': (1, 2),
                            '7': (2, 0),
                            '8': (2, 1),
                            '9': (2, 2),
                            '*': (3, 0),
                            '0': (3, 1),
                            '#': (3, 2)}
        self.__valid_keys = self.__key_coord.keys()

        self.__pin_modes = [self.__NO_SETUP] * len(valid_pins)
        self.__pin_states = [self.__NO_SIGNAL] * len(valid_pins)
        self.__led_states = [self.OFF] * N_LEDS
        self.__key_states = [False] * len(self.__key_coord)

        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.__listener.start()

    def setup(self, pin, mode, state=None):
        """ setup the initial mode and state of a specific pin """
        if state is None:  # set the default state to self.LOW
            state = self.LOW
        assert pin in valid_pins, "Invalid pin!"
        assert mode in {self.IN, self.OUT}, "Invalid pin mode!"
        self.__pin_modes[pin] = mode
        assert state in {self.LOW, self.HIGH}, "'Invalid pin state!"
        self.__pin_states[pin] = state

    def cleanup(self):
        """ reset GPIO, i.e., clear mode and state of each pin """
        for pin in valid_pins:
            self.__pin_modes[pin] = self.__NO_SETUP
            self.__pin_states[pin] = self.__NO_SIGNAL

    def input(self, pin):
        """ Carry out hardware simulation and return the state of an input pin """
        assert pin in valid_pins, "Invalid input pin"
        assert self.__pin_modes[pin] == self.IN, "Pin{} is not in input mode!".format(pin)
        if pin in keypad_pins:
            self.__update_keypad_pin_states()
        return self.__pin_states[pin]

    def output(self, pin, state):
        """ set the state to an output pin, and carry out hardware simulation """
        assert pin in valid_pins, "Invalid output pin"
        assert self.__pin_modes[pin] == self.OUT, "Pin{} is not in output mode!".format(pin)
        if pin in keypad_pins:
            self.__pin_states[pin] = state
        else:
            self.__pin_states[pin] = state
            self.__update_led_states()

    def __update_keypad_pin_states(self):
        """
        internal function, called by GPIO.input
        Update the states of the keypad input pins
        """
        # reset all keypad pins whose mode is GPIO.IN to GPIO.LOW
        for pin in keypad_pins:
            if self.__pin_modes[pin] == self.IN:
                self.__pin_states[pin] = self.LOW

        # if there is at least a True in the key states
        if True in self.__key_states:
            # find the first True
            pressed_key_index = self.__key_states.index(True)

            # retrieve the coordinates of the pressed
            pressed_row, pressed_col = list(self.__key_coord.values())[pressed_key_index]

            # get the corresponding pins
            row_pin = pressed_row + PIN_KEYPAD_ROW_0
            col_pin = pressed_col + PIN_KEYPAD_COL_0

            # set the input pin state to True according to the connected lines
            # it could be row_pin IN and col_pin OUT
            # or row_pin OUT and col_pin IN
            if self.__pin_modes[row_pin] == self.OUT and \
                    self.__pin_states[row_pin] == self.HIGH and \
                    self.__pin_modes[col_pin] == self.IN:
                self.__pin_states[col_pin] = self.HIGH
            elif self.__pin_modes[col_pin] == self.OUT and \
                    self.__pin_states[col_pin] == self.HIGH and \
                    self.__pin_modes[row_pin] == self.IN:
                self.__pin_states[row_pin] = self.HIGH

    def __on_press(self, key):
        """ The callback function for a key pressing event """
        # We handle only valid keypad keys, while neglecting all others
        # still allowing Ctrl+C to quit
        if hasattr(key, 'char') and key.char in self.__valid_keys:
            # reset the key states
            self.__key_states = [False] * len(self.__key_coord)
            # set the pressed key's state to True
            index = list(self.__key_coord.keys()).index(key.char)
            self.__key_states[index] = True

    def __on_release(self, key):
        """ The callback function for any key releasing event """
        # For simplicity, we reset the key states whenever a key is released
        self.__key_states = [False] * len(self.__key_coord)

    def __update_led_states(self):
        """
        internal function, called by GPIO.output
        set self.__led_states according to the CharliePlexing circuit, charlieplexing pin modes and states
        """
        valid_modes = [[self.OUT, self.OUT, self.IN],
                       [self.IN, self.OUT, self.OUT],
                       [self.OUT, self.IN, self.OUT]]
        cp_pin_modes = self.__pin_modes[PIN_CHARLIEPLEXING_0:PIN_CHARLIEPLEXING_2 + 1]
        if cp_pin_modes in valid_modes:
            group_index = valid_modes.index(cp_pin_modes)
        else:
            return
        out_position = [i for i, v in enumerate(cp_pin_modes) if v == self.OUT]
        if self.__pin_states[out_position[0]] == self.HIGH and \
                self.__pin_states[out_position[1]] == self.LOW:
            index_in_group = 0
        elif self.__pin_states[out_position[0]] == self.LOW and \
                self.__pin_states[out_position[1]] == self.HIGH:
            index_in_group = 1
        else:
            return
        led_index = group_index * 2 + index_in_group
        self.__led_states[led_index] = self.ON

    def show_leds_states(self):
        """ Show the states of the six LEDs """
        self.__update_led_states()
        state_strs = ['OFF', 'ON ']
        msg = 'LEDs['
        for i in range(N_LEDS):
            comma = '' if i == 0 else ','
            msg += "%s  %d: %s" % (comma, i, state_strs[self.__led_states[i]])
        msg += ']'
        print(msg)
        self.__led_states = [self.OFF] * N_LEDS

