from inspect import isfunction
from rule import Rule
from fsm import FSM
from agent import KPCAgent
from keypad import Keypad
from ledboard import LEDBoard
from typing import Callable


def return_true(just_for_fun):
    return True


def main():
    # Skriv kode her

    agent = KPCAgent()

    # keypad = Keypad() # i Agent
    # ledboard = LEDBoard() # i Agent

    fsm = FSM(agent)
    fsm.add_rule(Rule("S-init", "S-Read", return_true, agent.reset_passcode_entry))
    fsm.add_rule(Rule("S-Read", "S-Read", Rule.signal_is_digit,
                      agent.append_next_password_digit))
    fsm.add_rule(Rule("S-Read", "S-Verify", '*', agent.verify_login))
    fsm.add_rule(Rule("S-Read", "S-Init", return_true, agent.reset_agent))
    fsm.add_rule(Rule("S-Verify", "S-Active", 'Y', agent.active_agent))
    fsm.add_rule(Rule("S-Verify", "S-init", return_true, agent.reset_agent))

    fsm.add_rule(Rule("S-Read-2", "S-Active", '@', agent.refresh_agent))
    fsm.add_rule(Rule("S-Read-3", "S-Active", '@', agent.refresh_agent))
    fsm.add_rule(Rule("S-Active", "S-Read-2", '*', agent.reset_passcode_accumulator))
    fsm.add_rule(Rule("S-Read-2", "S-Read-3", '*', agent.cache_first_password))
    fsm.add_rule(Rule("S-Read-2", "S-Read-2", Rule.signal_is_digit, agent.append_next_password_digit))
    fsm.add_rule(Rule("S-Read-3", "S-Read-3", Rule.signal_is_digit, agent.append_next_password_digit))
    fsm.add_rule(Rule("S-Read-3", "S-Active", '*', agent.compare_new_password))

    state = fsm.get_start_state()

    while not state == fsm.get_end_state():
        signal = agent.get_next_signal()
        for rule in fsm.rules:
            if rule.match(state, signal):
                state = rule.next_state
                print(rule.action)
                agent.do_action(rule.action, signal)
                break

    # agent keypad, led shutdown
    agent.exit_action()


if __name__ == '__main__':
    main()
