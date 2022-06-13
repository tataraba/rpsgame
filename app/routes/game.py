from typing import Optional

from app.models.tracker import GameTracker
from app.mylib import db
from app.mylib.actions import compare_actions, user_action
from app.mylib.util import init_template
from fastapi import APIRouter, Form, Request, Response
from mylib import actions

router = APIRouter()
template = init_template()


@router.get("/")
def play_get(request: Request, first_game: bool = True) -> Response:
    """Front-end for the game. Checks if there are saved games to load,
    otherwise starts a new game."""

    if db.number_of_saved_games() != 0:
        first_game = False

    save_files = db.get_save_file_names()

    return template.TemplateResponse(
        "start_game.html",
        {
            "request": request,
            "games": save_files,
            "first_game": first_game,
        },
    )


@router.post("/play")
def play_post(
    request: Request,
    player_1: str = Form("Player 1", max_length=20),
    player_2: str | None = Form(None, max_length=20),
    computer_action: str | None = None,
    save_game_id: str | None = Form(None),
    doc_id: int | None = Form(None),
    game_data: db.Document | None = None,
    game_mode: str | None = None,
) -> Response:
    """Loads a saved game or starts a new game. Checks if game mode is
    single player or two player. If single player, computer_action is
    generated on post request.

    Args:
        request: Client request. Needed by Jinja.
        player_1: Defaults to "Player 1" if not provided.
        player_2: Defaults to None if not provided.
        computer_action: Result of computer generated action if single player.
        save_game_id: Save file name.
        doc_id: Unique document id of the TinyDB document.
        game_data: Key-value pair of game data.
        game_mode: `single_player` or `two_players`.

    Returns:
        Response: Jinja template response, including `context` passing parameters.
        to the template.
    """

    context = {
        "request": request,
        "game_data": game_data,
        "computer_action": computer_action,
        "doc_id": doc_id,
    }

    if save_game_id:  # Load a saved game
        game_data = db.load_game_by_name(save_game_id)
        context["game_loaded"] = True
        context["doc_id"] = game_data.doc_id if game_data else None

    else:  # Create a new game

        if not player_2:  # Add parameters for single player game only
            # TODO: Computer action not encrypted. Source be viewed by user.
            # TODO: Add safeguard against user input of "Computer"
            player_2 = "Computer"
            game_mode = "single_player"
            context["computer_action"] = actions.random_action()

        game_data = db.create_new_game(player_1, player_2, save_game_id)
        game_data["game_mode"] = game_mode

    context["game_data"] = game_data
    print(context)

    return template.TemplateResponse("play_game.html", context=context)


@router.post("/results")
def results_post(
    request: Request,
    player_1_action: str = Form(..., max_length=1),
    player_2_action: str = Form(..., max_length=1),
    doc_id: int = Form(None),
):

    if not user_action(player_1_action):
        return template.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": "Invalid player 1 action",
            },
        )
    if not user_action(player_2_action):
        return template.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": "Invalid player 2 action",
            },
        )

    game_data = db.load_game_by_id(doc_id) if doc_id else None
