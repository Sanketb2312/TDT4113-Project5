"""This module contains the Rule-class"""
from typing import Callable



def do_nothing():
    """returns true"""
    return True


class Rule:
    """Represents a rule in a FSM"""

    def __init__(
            self,
            source_state,
            next_state,
            expected_signal,
            action=do_nothing):
        self.source_state: str or Callable[[chr], bool] = source_state
        self.next_state: str = next_state
        self.expected_signal: chr or Callable = expected_signal
        self.action: Callable[[], bool] = action

    def match(self, state: str, signal: int) -> bool:
        'match method'
        def match_state() -> bool:
            if callable(self.source_state):
                return self.source_state(state)
            if isinstance(self.source_state, str):
                return state == self.source_state
            return False

        def match_signal() -> bool:
            if callable(self.expected_signal):
                return self.expected_signal(signal)
            if isinstance(self.expected_signal, (int, str)):
                return signal == self.expected_signal
            return False

        return match_state() and match_signal()

    @staticmethod
    def signal_is_digit(signal):
        """Returns if a signal is a digit."""
        temp_list: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        return signal in temp_list

    @staticmethod
    def signal_is_led_id(signal) -> bool:
        return 0 <= signal <= 5
