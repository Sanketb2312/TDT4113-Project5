from agent import KPCAgent
from rule import Rule
from inspect import isfunction


class FSM:

    def __init__(self, agent: KPCAgent):
        self.rules = []
        self.start_state: str = "S-init"
        self.end_state: str = "S-end"
        self.agent: KPCAgent = agent

    def add_rule(self, rule):
        if (isinstance(rule, Rule)):
            self.rules.append(rule)

    def get_start_state(self):
        return self.start_state

    def get_next_signal(self):
        return self.agent.get_next_signal()

    def get_end_state(self):
        return self.end_state
