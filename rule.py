"""This module contains the Rule-class"""
from typing import Callable


class Rule:
    """Represents a rule in a FSM"""

    source_state: str or Callable
    next_state: str
    expected_signal: chr or Callable
    action: Callable

    def match(self, state: str or Callable, signal: chr or Callable) -> bool:
        pass
