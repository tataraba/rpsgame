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
    total_games: int
    player_1_history: dict[int, str]
    player_2_history: dict[int, str]
    last_winner: str
