"""This module contains the Rule-class"""
from typing import Callable
from keypad import Keypad


class Rule:
    """Represents a rule in a FSM"""

    def __init__(self, source_state, next_state, expected_signal, action):
        self.source_state: str or Callable[[chr], bool] = source_state
        self.next_state: str = next_state
        self.expected_signal: chr or Callable = expected_signal
        self.action: Callable[[], bool] = action

    def match(self, state: str, signal: int) -> bool:
        if(isinstance(self.source_state, Callable)):
            return self.source_state(state)
        if(isinstance(self.expected_signal, Callable)):
            return self.expected_signal(signal)
        if state == self.source_state and signal == self.expected_signal:
            return True
        return False

    def match(self, state: str or Callable, signal: int or Callable):
        if signal_is_digit(signal):
            if state == self.source_state and signal == self.expected_signal:
                return self.action
            else:
                state = self.source_state

    @staticmethod
    def signal_is_digit(signal):
        try:
            return 0 <=ord(0) <=9
        except:
            return False

