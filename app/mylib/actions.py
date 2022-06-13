import random

from models.tracker import GameTracker
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
    p1_choice: str, p2_choice: str, game_data: GameTracker
) -> dict[str, str]:
    """Compare the user and computer actions and determine the winner or tie.

    Args:
        p1_choice: Player 1's choice of rock, paper, or scissors (as r, p, or s).
        p2_choice: Player 2's choice of rock, paper, or scissors (as r, p, or s).
        game_data: The game data that's been loaded from db.
    """
    _p1_choice = user_action(p1_choice)
    _p2_choice = user_action(p2_choice)
    action = {"player_1_name": _p1_choice, "player_2_name": _p2_choice}
    return determine_outcome(action, game_data)


def get_db_stats() -> dict:
    return {"game": "stats"}


def p1_wins(player_choices: dict[str, str], game_data: GameTracker):
    """Use the `player_choices` to update the db `game_data` to
    keep track of the game stats.

    Args:
        player_choices: Dictionary of both player's choices.
        game_data: The game data that's been loaded from db.

    Returns:
        _dict_: Updated dictionary of game data to be saved to db.
    """

    updated_data = {
        "player_1_score": game_data.player_1_score + 1,
        "player_1_history": game_data.player_1_history
        | {game_data.total_games: player_choices["player_1_name"]},
        "player_2_history": game_data.player_2_history
        | {game_data.total_games: player_choices["player_2_name"]},
        "last_winner": "player_1",
    }

    return game_data.dict() | updated_data


def p2_wins(player_choices: dict[str, str], game_data: GameTracker):

    updated_data = {
        "player_2_score": game_data.player_2_score + 1,
        "player_1_history": game_data.player_1_history
        | {game_data.total_games: player_choices["player_1_name"]},
        "player_2_history": game_data.player_2_history
        | {game_data.total_games: player_choices["player_2_name"]},
        "last_winner": "player_2",
    }

    return game_data.dict() | updated_data


def tie(player_choices: dict[str, str], game_data: GameTracker):
    print(f"{game_data=}")
    updated_data = {
        "ties": game_data.ties + 1,
        "player_1_history": game_data.player_1_history
        | {game_data.total_games: player_choices["player_1_name"]},
        "player_2_history": game_data.player_2_history
        | {game_data.total_games: player_choices["player_2_name"]},
        "last_winner": "tie",
    }

    return game_data.dict() | updated_data


def determine_outcome(
    player_choices: dict[str, str], game_data: GameTracker
) -> dict[str, str]:
    """Determines the outcome of the game based on the different
    combinations of user and/or computer actions.

    Args:
        player_choices: Dictionary containing the user and/or computer actions.
        game_data: Corresponding data that will be updated accordingly.

    Returns:
        result: Dictionary of the updated game file based on who won.
    """

    result: dict[str, str]

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
            return {"error": "Invalid user action."}

    return result
