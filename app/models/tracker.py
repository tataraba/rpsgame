from pydantic import BaseModel

# TODO: Add timestamp field


class GameTracker(BaseModel):
    """
    Model for the GameTracker table.
    """

    player_1_name: str
    player_2_name: str
    save_file_name: str
    game_mode: str
    player_1_score: int
    player_2_score: int
    ties: int
    player_1_history: list
    player_2_history: list
    last_winner: str
