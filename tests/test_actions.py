import pytest
from app.lib import actions


def test_user_action_correct_input():
    assert actions.user_action("R") == "r"
    assert actions.user_action("p") == "p"
    assert actions.user_action("S") == "s"


def test_invalid_user_action_input():
    with pytest.raises(ValueError) as exc_msg:
        actions.user_action("x")
    error = "Invalid user action."
    assert error in str(exc_msg.value)


def test_player_wins_message():
    assert actions.player_wins() == "You Win!"


def test_computer_wins_message():
    assert actions.computer_wins() == "You lost this time. Better luck next time!"


def test_tie_message():
    assert actions.tie() == "It's a tie!"


def test_compare_actions_computer_wins():
    _user_action = "p"
    _computer_action = "s"
    action = {"user": _user_action, "computer": _computer_action}
    outcome = actions.determine_outcome(action)
    assert outcome == actions.computer_wins()


def test_compare_actions_user_wins():
    _user_action = "r"
    _computer_action = "s"
    action = {"user": _user_action, "computer": _computer_action}
    outcome = actions.determine_outcome(action)
    assert outcome == actions.player_wins()


def test_compare_actions_tie():
    _user_action = "r"
    _computer_action = "r"
    action = {"user": _user_action, "computer": _computer_action}
    outcome = actions.determine_outcome(action)
    assert outcome == actions.tie()


def test_determine_outcome_combinations():
    combo_1 = {"user": "r", "computer": "s"}
    combo_2 = {"user": "p", "computer": "r"}
    combo_3 = {"user": "s", "computer": "p"}
    combo_4 = {"user": "r", "computer": "p"}
    combo_5 = {"user": "p", "computer": "s"}
    combo_6 = {"user": "s", "computer": "r"}
    combo_7 = {"user": "p", "computer": "p"}
    combo_8 = {"user": "r", "computer": "r"}
    combo_9 = {"user": "s", "computer": "s"}

    assert actions.determine_outcome(combo_1) == actions.player_wins()
    assert actions.determine_outcome(combo_2) == actions.player_wins()
    assert actions.determine_outcome(combo_3) == actions.player_wins()
    assert actions.determine_outcome(combo_4) == actions.computer_wins()
    assert actions.determine_outcome(combo_5) == actions.computer_wins()
    assert actions.determine_outcome(combo_6) == actions.computer_wins()
    assert actions.determine_outcome(combo_7) == actions.tie()
    assert actions.determine_outcome(combo_8) == actions.tie()
    assert actions.determine_outcome(combo_9) == actions.tie()
