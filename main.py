from inspect import isfunction
from rule import Rule
from fsm import FSM
from agent import KPCAgent
from keypad import Keypad
from ledboard import LEDBoard

def main():
    # Skriv kode her
    rule = Rule() # Skal vel være i FSM?
    fsm = FSM()
    agent = KPCAgent()
    #keypad = Keypad() # i Agent
    #ledboard = LEDBoard() # i Agent
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
