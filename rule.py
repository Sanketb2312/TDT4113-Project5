"""This module contains the Rule-class"""
from typing import Callable
from keypad import Keypad


def do_nothing():
    return True


class Rule:
    """Represents a rule in a FSM"""

    def __init__(self, source_state, next_state, expected_signal, action=do_nothing):
        self.source_state: str or Callable[[chr], bool] = source_state
        self.next_state: str = next_state
        self.expected_signal: chr or Callable = expected_signal
        self.action: Callable[[], bool] = action

    def match(self, state: str, signal: int) -> bool:
        def match_state() -> bool:
            if callable(self.source_state):
                return self.source_state(state)
            elif isinstance(self.source_state, str):
                return state == self.source_state
            return False

        def match_signal() -> bool:
            if callable(self.expected_signal):
                return self.expected_signal(signal)
            elif isinstance(self.expected_signal, int) or isinstance(self.expected_signal, str):
                return signal == self.expected_signal
            return False

        return match_state() and match_signal()

    @staticmethod
    def signal_is_digit(signal):
        l: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        return signal in l
