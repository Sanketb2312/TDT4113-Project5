from rule import Rule
from inspect import isfunction


class FSM:

    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        if (isinstance(rule, Rule)):
            self.rules.append(rule)

    def get_next_signal(self):
        pass

    def get_start_state(self):
        pass

    def get_end_state(self):
        pass
