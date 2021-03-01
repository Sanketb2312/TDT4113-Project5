"""This module contains the Rule-class"""
from typing import Callable
from keypad import Keypad


class Rule:
    """Represents a rule in a FSM"""

    source_state: str or Callable
    next_state: str
    expected_signal: chr or Callable
    action: Callable


    def match(self, state: str or Callable, signal: int or Callable):
        if signal_is_digit(signal):
            if state == self.source_state and signal == self.expected_signal:
                return self.action
            else:
                state = self.source_state



def signal_is_digit(signal):
    return 0 <=ord(signal) <=9


