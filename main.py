from inspect import isfunction
from rule import Rule
from fsm import FSM
from agent import KPCAgent
from keypad import Keypad
from ledboard import LEDBoard
from typing import Callable
def main():
    # Skriv kode her

    agent = KPCAgent()
    #keypad = Keypad() # i Agent
    #ledboard = LEDBoard() # i Agent


    fsm = FSM()
    fsm.add_rule(Rule("S-init", "S-Read",callable(Rule.signal_is_digit), agent.reset_passcode_entry()))
    fsm.add_rule(Rule("S-Read", "S-Read", callable(Rule.signal_is_digit), agent.append_next_password_digit()))
    fsm.add_rule(Rule("S-Read", "S-Verify", callable(), agent.verify_login()))
    fsm.add_rule(Rule("S-Read", "S-Init", callable(Rule.signal_is_digit), agent.reset_agent()))
    fsm.add_rule(Rule("S-Verify", "S-Active", callable(),agent.active_agent()))
    fsm.add_rule(Rule("S-Verify", "S-Active", callable(Rule.signal_is_digit), agent.reset_agent()))

    state = fsm.get_start_state()


    while not state == fsm.get_end_state():
        signal = agent.get_next_signal()
        for rule in fsm.rules:
            if rule.match(state, signal):
                state = rule.state2
                agent.do_action(rule.action, signal)
                #go to
            break
        break


    #agent keypad, led shutdown
    agent.led_board.turn_off()


if __name__ == '__main__':
    main()
