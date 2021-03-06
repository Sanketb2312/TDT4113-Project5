"""This module contains the main-function"""
from rule import Rule
from fsm import FSM
from agent import KPCAgent


def return_true(signal):
    """Returns always True if signal is not \" \" """
    return signal != ""

def logged_in(signal):
    tmp_list: list = ["S-Active", "S-Light-LED", "S-Light-LED-2", "S-Read-2", "S-Read-3"]
    return signal in tmp_list

def main():
    """The main function to be runned"""
    # Skriv kode her
    while True:
        agent = KPCAgent()
        fsm = FSM(agent)
        fsm.add_rule(Rule(logged_in, "S-verify-end", '#'))
        fsm.add_rule(Rule("S-verify-end", "S-end", '#'))
        fsm.add_rule(Rule("S-verify-end", "S-Active", return_true))
        fsm.add_rule(Rule(return_true, "S-end", '#'))
        fsm.add_rule(Rule("S-init", "S-Read", return_true, agent.reset_passcode_entry))
        fsm.add_rule(Rule("S-Read", "S-Read", Rule.signal_is_digit,
                          agent.append_next_password_digit))
        fsm.add_rule(Rule("S-Read", "S-Verify", '*', agent.verify_login))
        fsm.add_rule(Rule("S-Read", "S-Init", return_true, agent.reset_agent))
        fsm.add_rule(Rule("S-Verify", "S-Active", 'Y'))
        fsm.add_rule(Rule("S-Verify", "S-init", return_true, agent.reset_agent))
        fsm.add_rule(Rule("S-Read-2", "S-Active", '@', agent.refresh_agent))
        fsm.add_rule(Rule("S-Read-3", "S-Active", '@', agent.refresh_agent))
        fsm.add_rule(Rule("S-Active", "S-Read-2", '*', agent.reset_passcode_entry))
        fsm.add_rule(Rule("S-Active", "S-Light-LED", Rule.signal_is_led_id, agent.save_led_id))
        fsm.add_rule(Rule("S-Light-LED", "S-Light-LED-2", "*"))
        fsm.add_rule(Rule("S-Light-LED-2", "S-Light-LED-2", Rule.signal_is_digit, agent.append_led_duration))
        fsm.add_rule(Rule("S-Light-LED-2", "S-Active", '*', agent.light_one_led))
        fsm.add_rule(Rule("S-Read-2", "S-Read-3", '*', agent.cache_first_password))
        fsm.add_rule(Rule("S-Read-2", "S-Read-2", Rule.signal_is_digit,
                          agent.append_next_password_digit))
        fsm.add_rule(Rule("S-Read-3", "S-Read-3", Rule.signal_is_digit,
                          agent.append_next_password_digit))
        fsm.add_rule(Rule("S-Read-3", "S-Active", '*', agent.compare_new_password))
        state = fsm.get_start_state()
        while state != fsm.get_end_state():
            signal = agent.get_next_signal()
            for rule in fsm.rules:
                if rule.match(state, signal):
                    agent.current_signal = signal
                    print(rule.source_state, rule.next_state, agent.override_signal)
                    state = rule.next_state
                    agent.do_action(rule.action)
                    break

        # agent keypad, led shutdown
        agent.exit_action()


if __name__ == '__main__':
    main()
