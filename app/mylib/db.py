from pathlib import Path

from app.models.tracker import GameTracker
from tinydb import Query, TinyDB, where
from tinydb.table import Document

root_directory = Path(__file__).parent.parent.parent

db = TinyDB(root_directory / "data/game_history.json")


def number_of_saved_games() -> int:
    """Get the number of saved games.

    Returns:
        int: The number of saved games.
    """
    return len(db)


def game_exists(save_file_name) -> bool:
    """Check if a game exists with the corresponding `save_file_name`.

    Args:
        save_file_name: The name of the save file.
    """

    Game = Query()

    return db.contains(Game.save_file_name == save_file_name)


def create_new_game(
    player_1: str, player_2: str, save_file_name: str | None, **kwargs
) -> Document:
    """Create a new game with player names and `save_file_name`. Check to see
    if a game exists with the same file name. If so, append a `game_id` to
    chosen `save_file_name`. If no `save_file_name` is given, use a default.


    Args:
        player_1: Name of the first player.
        player_2: Name of the second player.
        save_file_name: Name of the save file.

    Returns:
        int: The new game's document id.
    """
    game_id: int = len(db) + 1

    if not save_file_name:
        save_file_name = f"Saved Game: ID {game_id}"

    if game_exists(save_file_name):
        save_file_name = f"{save_file_name}: ID {game_id}"

    game = GameTracker(
        player_1_name=player_1,
        player_2_name=player_2,
        save_file_name=save_file_name,
        game_mode="two_players",
        player_1_score=0,
        player_2_score=0,
        ties=0,
        player_1_history=[],
        player_2_history=[],
        last_winner="",
    )

    doc_id = db.insert(game.dict())

    if not doc_id:
        raise AttributeError("Failed to create new game.")

    data = db.get(doc_id=doc_id)
    if not data:
        raise AttributeError("Failed to load new game.")
    return data


def get_save_file_names() -> list[str]:
    """Get the names of all the save game entries.

    Returns:
        list: The names of all the save files.
    """
    return [game["save_file_name"] for game in db]


def load_game_by_id(doc_id: int):
    """Load the game stats.

    Args:
        game_id: The id of the game.
    """

    return db.get(doc_id=doc_id)


def load_game_by_name(save_file_name: str):
    """Load the game stats.

    Args:
        save_file_name: The name of the save file.
    """

    return db.get(where("save_file_name") == save_file_name)
