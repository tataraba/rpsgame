import random

from tinydb.table import Document


def user_action(choice: str) -> str:
    """Define the choices that the user can make.

    Args:
        choice: The user's choice of rock, paper, or scissors (as r, p, or s).

    Returns:
        The user's choice of rock, paper, or scissors (as r, p, or s).

    """
    if choice.lower() in {"r", "p", "s"}:
        return choice.lower()
    else:
        raise ValueError("Invalid user action.")


def random_action() -> str:
    """Choose a random action for the computer."""
    return random.choice(["r", "p", "s"])


def compare_actions(
    p1_choice: str, p2_choice: str, game_data: Document
) -> dict[str, str | None] | None:
    """Compare the user and computer actions and determine the winner or tie."""
    _p1_choice = user_action(p1_choice)
    _p2_choice = user_action(p2_choice)
    action = {"player_1_name": _p1_choice, "player_2_name": _p2_choice}
    return determine_outcome(action, game_data)


def get_db_stats() -> dict:
    return {"game": "stats"}


def p1_wins(player_choices: dict[str, str], game_data: Document):

    updated_data = {
        "player_1_score": game_data.player_1_score + 1,
        "player_1_history": game_data.player_1_history.append(
            player_choices["player_1_name"]
        ),
        "player_2_history": game_data.player_2_history.append(
            player_choices["player_2_name"]
        ),
        "last_winner": "player_1",
    }

    return game_data.update(updated_data)


def p2_wins(player_choices: dict[str, str], game_data: Document):

    updated_data = {
        "player_2_score": game_data.player_2_score + 1,
        "player_1_history": game_data.player_1_history.append(
            player_choices["player_1_name"]
        ),
        "player_2_history": game_data.player_2_history.append(
            player_choices["player_2_name"]
        ),
        "last_winner": "player_2",
    }

    return game_data.update(updated_data)


def tie(player_choices: dict[str, str], game_data: Document):

    updated_data = {
        "ties": game_data.ties + 1,
        "player_1_history": game_data.player_1_history.append(
            player_choices["player_1_name"]
        ),
        "player_2_history": game_data.player_2_history.append(
            player_choices["player_2_name"]
        ),
        "last_winner": "tie",
    }

    return game_data.update(updated_data)


def determine_outcome(
    player_choices: dict[str, str], game_data: TinyDB
) -> dict[str, str | None]:
    """Determine the outcome of the game based on `compare_actions`.

    Args:
        game: Dictionary containing the user and computer actions.

    Returns:
        _type_: Result of the game.
    """
    # player_choices = {"player_1_name": p1_choice, "player_2_name": p2_choice}

    result: dict[str, str] | None = None
    match player_choices:
        case {"player_1_name": "r", "player_2_name": "s"}:
            result = p1_wins(player_choices, game_data)
        case {"player_1_name": "p", "player_2_name": "r"}:
            result = p1_wins(player_choices, game_data)
        case {"player_1_name": "s", "player_2_name": "p"}:
            result = p1_wins(player_choices, game_data)
        case {
            "player_1_name": player_1_name,
            "player_2_name": player_2_name,
        } if player_1_name == player_2_name:
            result = tie(player_choices, game_data)
        case {"player_1_name": "r", "player_2_name": "p"}:
            result = p2_wins(player_choices, game_data)
        case {"player_1_name": "p", "player_2_name": "s"}:
            result = p2_wins(player_choices, game_data)
        case {"player_1_name": "s", "player_2_name": "r"}:
            result = p2_wins(player_choices, game_data)
        case _:
            return None

    return result
