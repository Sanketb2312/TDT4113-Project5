'Modul'

from agent import KPCAgent
from rule import Rule


class FSM:
    'FSM class'

    def __init__(self, agent: KPCAgent):
        'constructor'
        self.rules = []
        self.start_state: str = "S-init"
        self.end_state: str = "S-end"
        self.agent: KPCAgent = agent

    def add_rule(self, rule):
        'rule for adding method'
        if isinstance(rule, Rule):
            self.rules.append(rule)

    def get_start_state(self):
        'returns starting state'
        return self.start_state

    def get_next_signal(self):
        'returns the next signal'
        return self.agent.get_next_signal()

    def get_end_state(self):
        'returns the end state'
        return self.end_state
